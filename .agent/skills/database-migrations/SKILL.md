---
name: database-migrations
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Zero-downtime database migration patterns for Prisma, Drizzle, Django, and Go. Use when altering tables, adding columns, creating indexes, or running data backfills on a live database.
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
---

# Database Migration Patterns

## Identity

You are a database migration specialist. You ensure schema changes are safe, reversible, and zero-downtime. You know that a migration that works on 100 rows may lock a 10M-row table for minutes — and you plan accordingly.

## When to Activate

- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfills, transforms)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

## When NOT to Use

- Seed data inserts or test fixture changes — these are not schema migrations
- Changes that only affect application logic with no schema impact (no new tables, columns, or indexes)
- Ad-hoc data fixes on a single row — use a targeted SQL script with a backup, not a migration
- When the schema is still being prototyped and changes daily (wait until the schema stabilizes before committing to migrations)

---

## Core Principles

1. **Every change is a migration** — never alter production databases manually
2. **Migrations are forward-only in production** — rollbacks use new forward migrations
3. **Schema and data migrations are separate** — never mix DDL and DML in one migration
4. **Test migrations against production-sized data** — a migration on 100 rows ≠ 10M rows
5. **Migrations are immutable once deployed** — never edit a migration that has run in production

---

## Migration Safety Checklist

Before applying any migration to production:

- [ ] Migration has UP and DOWN defined (or explicitly marked irreversible)
- [ ] No full table locks on large tables (use `CONCURRENTLY` / batch operations)
- [ ] New NOT NULL columns have defaults or will be backfilled first
- [ ] Indexes created with `CONCURRENTLY` keyword (not inline with CREATE TABLE on existing data)
- [ ] Data backfill is a **separate migration** from the schema change
- [ ] Tested against a copy of production data (not just dev fixtures)
- [ ] Rollback plan documented

---

## PostgreSQL Patterns

### Adding a Column Safely

```sql
-- ✅ GOOD: Nullable column — no lock, instant
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- ✅ GOOD: Column with default (Postgres 11+ — instant, no rewrite)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- ❌ BAD: NOT NULL without default on existing table
ALTER TABLE users ADD COLUMN role TEXT NOT NULL;
-- Requires full table rewrite → table lock for minutes on large tables
```

### Creating an Index Without Downtime

```sql
-- ❌ BAD: Blocks all writes on large tables for minutes
CREATE INDEX idx_users_email ON users (email);

-- ✅ GOOD: Non-blocking, allows concurrent reads AND writes
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- ⚠️ Note: CONCURRENTLY cannot run inside a transaction block.
-- Most ORMs need a custom SQL migration for this (see Prisma section).
```

### Renaming a Column (Zero-Downtime — 3 Deployments)

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
-- ❌ BAD: Updates all rows in a single transaction (locks table)
UPDATE users SET normalized_email = LOWER(email);

-- ✅ GOOD: Batch update — small locks, no full-table blocking
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
    RAISE NOTICE 'Updated % rows', rows_updated;
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

# Reset database (dev/test only — DESTROYS DATA)
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

Prisma cannot generate `CONCURRENTLY` index creation. Write it manually:

```bash
# Create an empty migration shell, then edit the SQL
npx prisma migrate dev --create-only --name add_email_index_concurrently
```

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

## Zero-Downtime Strategy: Expand → Migrate → Contract

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

**Never collapse these phases** — each requires a separate deployment so the running app always has valid data.

---

## Anti-Patterns

- Never add a NOT NULL column without a DEFAULT or a preceding backfill migration because the ALTER TABLE statement locks the table while it re-writes every existing row with the default value, causing write downtime proportional to table size.
- Never run a migration that drops a column while the old application version is still deployed because the old code still references the dropped column, causing immediate SELECT/INSERT failures until all application instances are updated.
- Never skip a rollback (DOWN) migration because without a tested rollback, a failed forward migration leaves the schema in an unknown intermediate state that requires manual intervention to recover.
- Never test migrations only against the development database because production databases have significantly larger tables, different indexes, and potentially divergent data distributions that cause acceptable dev-environment timings to become hour-long production locks.
- Never create a non-concurrent index inside a migration on a busy Postgres table because `CREATE INDEX` (without CONCURRENTLY) acquires a full table lock for the duration of the build, blocking all reads and writes during the migration window.
- Never deploy application and migration changes atomically without a compatibility window because a zero-downtime deployment requires the new schema to be compatible with the old code and the new code to be compatible with the old schema simultaneously during the rollout.

---

---

## Self-Verification Checklist

- [ ] Migration UP runs to completion with exit code 0: `psql -c "\d <table>"` (or equivalent) confirms the expected columns/indexes exist after applying
- [ ] NOT NULL column has a server-side DEFAULT or a preceding backfill migration: `grep -rn "NOT NULL" <migration_file>` — every NOT NULL column is accompanied by DEFAULT or a prior data migration
- [ ] Indexes created with `CONCURRENTLY`: `grep -n "CREATE INDEX" <migration_file>` returns 0 matches without `CONCURRENTLY` keyword
- [ ] Migration tested against production-sized data: row count of test dataset is >= 80% of production row count — confirmed via `SELECT COUNT(*) FROM <table>` on both environments
- [ ] Schema changes and data migrations are in separate files: `ls migrations/` shows DDL files and DML files with distinct timestamps — no single file contains both `ALTER TABLE` and `UPDATE`/`INSERT` statements (`grep -c "ALTER TABLE\|UPDATE\|INSERT" <file>` returns ≤ 1 statement type per file)
- [ ] Rollback migration tested: DOWN migration runs with exit code 0 and `psql -c "\d <table>"` confirms the schema reverted to the pre-migration state
- [ ] `lock_timeout` set: `grep -n "lock_timeout" <migration_file>` returns at least 1 match — missing lock_timeout is a blocking issue

## Success Criteria

This skill is complete when: 1) the migration file is tested against production-sized data and passes without table locks or timeouts, 2) schema changes and data backfills are in separate migrations, and 3) a rollback strategy is documented and tested in staging.

## Failure Modes

| Situation                          | Response                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------- |
| Output exceeds expectations        | Redirect to sandbox or context-optimizer. Log and truncate.                     |
| Skill conflicts with another skill | Define clear boundaries. Each skill owns one domain.                            |
| Agent ignores skill                | Rewrite description to contain ONLY triggers, no workflow summary.              |
| Generated output too verbose       | Apply conciseness check. Every line must earn its place.                        |
| Migration fails mid-way            | Have rollback migration ready. Use transactions where possible.                 |
| Schema change breaks running app   | Use expand-contract pattern. Add new column, migrate data, remove old.          |
| Large table migration times out    | Use batched migrations. Add progress logging. Consider pt-online-schema-change. |
| Data loss during migration         | Always backup before migration. Test on staging with production-size data.      |

## Tips

- **Use `EXPLAIN ANALYZE`** before any large migration to preview lock behavior
- **Test rollbacks** — run the DOWN migration in staging before applying UP in production
- **Set a lock timeout** in production: `SET lock_timeout = '5s'` — so a migration fails fast instead of queuing behind a long transaction
- **Monitor during migrations** — watch pg_locks, long-running queries, and error rate
- **Announce maintenance windows** for unavoidable locking operations
