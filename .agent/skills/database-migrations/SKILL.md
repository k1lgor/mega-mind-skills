---
name: database-migrations
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Zero-downtime database migration patterns for Prisma, Drizzle, Django, and Go.
  Use when altering tables, adding columns, creating indexes, or running data backfills on a live database.
  Covers Expand-Migrate-Contract strategy, CONCURRENTLY index creation, batched data migrations, and safety protocols for schema changes.
category: domain-expert
triggers:
  - "database migration"
  - "schema change"
  - "alter table"
  - "add column"
  - "create index"
  - "zero downtime migration"
  - "backfill data"
  - "rename column"
  - "prisma migrate"
  - "drizzle migration"
dependencies:
  - data-engineer: optional
  - verification-loop: recommended
  - observability-specialist: optional
---

# Database Migration Patterns

## Identity

You are a database migration specialist. You ensure schema changes are safe, reversible, and zero-downtime. You know that a migration that works on 100 rows may lock a 10M-row table for minutes-and you plan accordingly.

**Your core responsibility:** Execute schema changes on live databases with zero downtime and zero data loss.

**Your operating principle:** Every change is a reversible migration; never alter production databases manually.

**Your quality bar:** Every migration has a tested rollback, production-sized data verification, CONCURRENTLY for indexes, and separate schema/data migrations-no exceptions.

## When to Use

- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfills, transforms)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

## When NOT to Use

- Seed data inserts or test fixture changes-these are not schema migrations
- Changes that only affect application logic with no schema impact (no new tables, columns, or indexes)
- Ad-hoc data fixes on a single row-use a targeted SQL script with a backup, not a migration
- When the schema is still being prototyped and changes daily (wait until the schema stabilizes before committing to migrations)

---

## Core Principles

1. **Every change is a migration**-never alter production databases manually
2. **Migrations are forward-only in production**-rollbacks use new forward migrations
3. **Schema and data migrations are separate**-never mix DDL and DML in one migration
4. **Test migrations against production-sized data**-a migration on 100 rows is not 10M rows
5. **Migrations are immutable once deployed**-never edit a migration that has run in production

---

## Migration Safety Checklist

Before applying any migration to production:

- [ ] Migration has UP and DOWN defined (or explicitly marked irreversible)
- [ ] No full table locks on large tables (use CONCURRENTLY / batch operations)
- [ ] New NOT NULL columns have defaults or will be backfilled first
- [ ] Indexes created with CONCURRENTLY keyword (not inline with CREATE TABLE on existing data)
- [ ] Data backfill is a **separate migration** from the schema change
- [ ] Tested against a copy of production data (not just dev fixtures)
- [ ] Rollback plan documented

---

## PostgreSQL Patterns

### Adding a Column Safely

```sql
-- GOOD: Nullable column-no lock, instant
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- GOOD: Column with default (Postgres 11+-instant, no rewrite)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- BAD: NOT NULL without default on existing table
ALTER TABLE users ADD COLUMN role TEXT NOT NULL;
-- Requires full table rewrite -> table lock for minutes on large tables
```

### Creating an Index Without Downtime

```sql
-- BAD: Blocks all writes on large tables for minutes
CREATE INDEX idx_users_email ON users (email);

-- GOOD: Non-blocking, allows concurrent reads AND writes
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- Note: CONCURRENTLY cannot run inside a transaction block.
-- Most ORMs need a custom SQL migration for this (see Prisma section).
```

### Renaming a Column (Zero-Downtime-3 Deployments)

Never rename directly on a live system. Use the expand-contract pattern:

```sql
-- Migration 001: Add new column (nullable)
ALTER TABLE users ADD COLUMN display_name TEXT;

-- Migration 002: Backfill existing rows (batched)
UPDATE users SET display_name = username WHERE display_name IS NULL;

-- (Deploy app that reads BOTH columns and writes to the new one)

-- Migration 003: Drop old column (after app no longer references it)
ALTER TABLE users DROP COLUMN username;
```

### Removing a Column Safely

```sql
-- Step 1: Remove ALL application references to the column first
-- Step 2: Deploy the application without the column reference
-- Step 3: Then drop the column in the next migration

ALTER TABLE orders DROP COLUMN legacy_status;
```

> **Why this order?** If you drop the column first, deployed app code that references it will throw errors on every request.

### Large Data Migrations (Batched Updates)

```sql
-- BAD: Updates all rows in a single transaction (locks table)
UPDATE users SET normalized_email = LOWER(email);

-- GOOD: Batch update-small locks, no full-table blocking
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET normalized_email = LOWER(email)
    WHERE id IN (
      SELECT id FROM users
      WHERE normalized_email IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED  -- Skip rows locked by other transactions
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE ''Updated % rows'', rows_updated;
    EXIT WHEN rows_updated = 0;
    COMMIT;           -- Release lock between batches
  END LOOP;
END $$;
```

---

## Prisma (TypeScript / Node.js)

### Workflow

```bash
# Create migration from schema changes
npx prisma migrate dev --name add_user_avatar

# Apply pending migrations in production
npx prisma migrate deploy

# Regenerate Prisma client after schema changes
npx prisma generate

# Reset database (dev/test only-DESTROYS DATA)
npx prisma migrate reset
```

### Schema Example

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  avatarUrl String?  @map("avatar_url")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  orders    Order[]

  @@map("users")
  @@index([email])
}
```

### Custom SQL Migration (for CONCURRENTLY, raw DML)

Prisma cannot generate CONCURRENTLY index creation. Write it manually:

```bash
# Create an empty migration shell, then edit the SQL
npx prisma migrate dev --create-only --name add_email_index_concurrently
``'

```sql
-- prisma/migrations/20260317_add_email_index_concurrently/migration.sql
-- Prisma cannot generate CONCURRENTLY, so we write raw SQL
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);
```

---

## Drizzle (TypeScript / Node.js)

### Workflow

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema directly to DB (dev only)
npx drizzle-kit push
```

### Schema Example

```typescript
import { pgTable, text, boolean, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name"),
  avatarUrl: text("avatar_url"),
  isActive: boolean("is_active").notNull().default(true),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
```

---

## Django (Python)

### Workflow

```bash
# Create migration from model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Preview SQL without applying
python manage.py sqlmigrate myapp 0003

# Run a specific data migration
python manage.py migrate myapp 0003
```

### Data Migration (RunPython)

```python
# myapp/migrations/0004_backfill_display_name.py
from django.db import migrations

def backfill_display_name(apps, schema_editor):
    User = apps.get_model("myapp", "User")
    # Process in batches to avoid locking
    batch_size = 1000
    qs = User.objects.filter(display_name="").values_list("id", flat=True)
    for i in range(0, qs.count(), batch_size):
        ids = list(qs[i : i + batch_size])
        User.objects.filter(id__in=ids).update(
            display_name=models.F("username")
        )

class Migration(migrations.Migration):
    dependencies = [("myapp", "0003_add_display_name")]
    operations = [
        migrations.RunPython(backfill_display_name, migrations.RunPython.noop),
    ]
```

---

## golang-migrate (Go)

### Workflow

```bash
# Install
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Create new migration
migrate create -ext sql -dir db/migrations -seq add_user_avatar

# Apply all pending migrations
migrate -path db/migrations -database $DATABASE_URL up

# Rollback one migration
migrate -path db/migrations -database $DATABASE_URL down 1
```

### Migration Files

```sql
-- db/migrations/000003_add_user_avatar.up.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;
CREATE INDEX CONCURRENTLY idx_users_avatar ON users (avatar_url) WHERE avatar_url IS NOT NULL;

-- db/migrations/000003_add_user_avatar.down.sql
DROP INDEX CONCURRENTLY IF EXISTS idx_users_avatar;
ALTER TABLE users DROP COLUMN IF EXISTS avatar_url;
```

---

## Zero-Downtime Strategy: Expand -> Migrate -> Contract

For any breaking schema change, use 3 separate deployments:

```
Phase 1: EXPAND
  Migration: Add new column/table (nullable or with default)
  App deploy: Write to BOTH old and new column

Phase 2: MIGRATE
  Migration: Backfill all existing rows to new column
  App deploy: Read from NEW, write to BOTH (verify data integrity)

Phase 3: CONTRACT
  App deploy: Only use new column (remove old column references)
  Migration: DROP old column in a separate, later migration
```

**Never collapse these phases**-each requires a separate deployment so the running app always has valid data.

---

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Adding NOT NULL column without DEFAULT on existing table | Full table rewrite l lock for minutes | Add DEFAULT first, then set NOT NULL |
| Dropping column while old app version is deployed | Immediate SELECT/INSERT failures | Remove app references first, then drop column |
| Skipping rollback (DOWN) migration | Failed forward migration leaves unknown intermediate state | Always define and test DOWN migration |
| Testing only against development database | Dev timings != production timings; hour-long locks hidden | Test against production-sized data copy |
| Non-concurrent index on busy table | Blocks all reads/writes for duration of build | Always use CONCURRENTLY on production tables |
| Deploying app + migration atomically without compatibility window | Zero-downtime requires both old schema + new code and new schema + old code to work simultaneously | Phase deployments: schema first, app second, cleanup third |

## Verification

### Self-Verification Checklist

- [ ] Migration UP runs to completion with exit code 0
- [ ] NOT NULL column has server-side DEFAULT or preceding backfill migration
- [ ] Indexes created with CONCURRENTLY
- [ ] Migration tested against production-sized data (>=80% of production row count)
- [ ] Rollback migration tested: DOWN runs with exit code 0
- [ ] `lock_timeout` set for production migrations

### Verification Commands

```bash
# Verify schema after migration
psql -c "\d <table>"

# Check for CONCURRENTLY usage
grep -n "CREATE INDEX" migration.sql | grep -v "CONCURRENTLY"

# Test rollback
psql -f down_migration.sql
psql -c "\d <table>"  # confirm revert

# Set lock timeout for safety
psql -c "SET lock_timeout = '5s';" -f migration.sql
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Rollback | DOWN migration tested in staging | Do not deploy UP until DOWN is verified |
| Lock Safety | `lock_timeout` set on all production migrations | Add `SET lock_timeout = '5s'` before DDL |
| Data Integrity | Row counts match before/after migration | Investigate mismatch; restore from backup |
| Production Parity | Test dataset >= 80% of production size | Scale up test data until threshold met |

## Performance & Cost

### Model Selection

| Task | Approach | Cost |
|---|---|---|
| Simple column add | Direct DDL (instant for nullable) | Free |
| Index on large table | CONCURRENTLY | CPU cost, no downtime |
| Data backfill (million rows) | Batched UPDATE (10K per batch) | DB CPU, no lock contention |

### Parallelization

- **Schema + Data migrations:** Must be sequential (never mix DDL and DML)
- **Multiple data backfills:** Can run in parallel if on different tables
- **Index creation:** Run `CREATE INDEX CONCURRENTLY` in parallel for different tables

### Context Budget

- **Expected context usage:** 3-6KB per migration design session
- **When to context-optimize:** When reviewing multi-step expand-contract migration plans

## Examples

### Example 1: Adding a Column with Backfill

**User request:** "Add `display_name` to users table (1M rows) and populate from `username`."

**Skill execution:**
1. Migration 001: `ALTER TABLE users ADD COLUMN display_name TEXT;` (instant, nullable)
2. Migration 002: Batched UPDATE (10K rows per batch, SKIP LOCKED)
3. Deploy app: write to both `username` and `display_name`
4. Migration 003: `ALTER TABLE users DROP COLUMN username;` (after 30 days)

**Result:** Column added and backfilled with zero downtime.

### Example 2: Edge Case-CONCURRENTLY in Prisma

**User request:** "Add an index on `orders.user_id` (50M rows) using Prisma."

**Skill execution:**
1. Create empty migration: `npx prisma migrate dev --create-only --name add_orders_user_id_idx`
2. Replace generated SQL with `CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id);`
3. Note: cannot run in a transaction block
4. Set `lock_timeout = '30s'` for safety

**Result:** Index created with zero locking. Prisma limitation worked around.

### Example 3: Rollback Failure Recovery

**User request:** "Our migration failed halfway through. What now?"

**Skill execution:**
1. Check which part of the migration succeeded/failed
2. Run the DOWN migration to revert to pre-migration state
3. Investigate: was it a timeout, lock contention, or data integrity issue?
4. Fix the issue, test on staging, re-apply

**Result:** Safe rollback without data corruption.

## Anti-Patterns

- Never add a NOT NULL column without a DEFAULT or a preceding backfill migration because the ALTER TABLE statement locks the table while it re-writes every existing row with the default value, causing write downtime proportional to table size.
- Never run a migration that drops a column while the old application version is still deployed because the old code still references the dropped column, causing immediate SELECT/INSERT failures until all application instances are updated.
- Never skip a rollback (DOWN) migration because without a tested rollback, a failed forward migration leaves the schema in an unknown intermediate state that requires manual intervention to recover.
- Never test migrations only against the development database because production databases have significantly larger tables, different indexes, and potentially divergent data distributions that cause acceptable dev-environment timings to become hour-long production locks.
- Never create a non-concurrent index inside a migration on a busy Postgres table because `CREATE INDEX` (without CONCURRENTLY) acquires a full table lock for the duration of the build, blocking all reads and writes during the migration window.
- Never deploy application and migration changes atomically without a compatibility window because a zero-downtime deployment requires the new schema to be compatible with the old code and the new code to be compatible with the old schema simultaneously during the rollout.

---

## Failure Modes

| Situation                          | Response                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| Migration fails mid-way            | Have rollback migration ready. Use transactions where possible.                 |
| Schema change breaks running app   | Use expand-contract pattern. Add new column, migrate data, remove old.          |
| Large table migration times out    | Use batched migrations. Add progress logging. Consider pt-online-schema-change. |
| Data loss during migration         | Always backup before migration. Test on staging with production-size data.      |

## Tips

- **Use `EXPLAIN ANALYZE`** before any large migration to preview lock behavior
- **Test rollbacks**-run the DOWN migration in staging before applying UP in production
- **Set a lock timeout** in production: `SET lock_timeout = '5s'`-so a migration fails fast instead of queuing behind a long transaction
- **Monitor during migrations**-watch pg_locks, long-running queries, and error rate
- **Announce maintenance windows** for unavoidable locking operations

## References

### Internal Dependencies
- `data-engineer` — Handles OLAP/warehouse schema evolution (partner skill)
- `verification-loop` — Verifies migration correctness end-to-end
- `observability-specialist` — Monitors migration execution and lock contention

### External Standards
- [PostgreSQL Documentation: CREATE INDEX CONCURRENTLY](https://www.postgresql.org/docs/current/sql-createindex.html) — Non-blocking index creation
- [Prisma Migrate Documentation](https://www.prisma.io/docs/orm/prisma-migrate) — Migration patterns for Prisma
- [Expand-Contract Pattern](https://www.prisma.io/dataguide/types/relational/expand-contract-pattern) — Zero-downtime schema changes

### Related Skills
- `data-engineer` — Partner skill for OLAP schema changes
- `verification-loop` — Follows database-migrations for verification

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Blocking Violations table, Verification with commands/quality gates, Performance & Cost section, Examples, References, Changelog. |
