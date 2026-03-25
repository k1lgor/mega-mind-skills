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

| Anti-Pattern                         | Why It Fails                             | Better Approach                             |
| ------------------------------------ | ---------------------------------------- | ------------------------------------------- |
| Manual SQL in production             | No audit trail, unrepeatable             | Always use migration files                  |
| Editing a deployed migration         | Causes drift between environments        | Create a new forward migration instead      |
| NOT NULL without default             | Locks table, rewrites every existing row | Add nullable, backfill, then add constraint |
| `CREATE INDEX` (not CONCURRENTLY)    | Blocks writes during index build         | Use `CREATE INDEX CONCURRENTLY`             |
| Schema + data in one migration       | Hard to rollback, long lock time         | Two separate migrations                     |
| Dropping column before removing code | Runtime errors on deployed app           | Remove code references first, then drop     |
| Testing on dev fixtures only         | Dev has 50 rows, production has 50M      | Always test against production-sized copy   |

---

## Tips

- **Use `EXPLAIN ANALYZE`** before any large migration to preview lock behavior
- **Test rollbacks** — run the DOWN migration in staging before applying UP in production
- **Set a lock timeout** in production: `SET lock_timeout = '5s'` — so a migration fails fast instead of queuing behind a long transaction
- **Monitor during migrations** — watch pg_locks, long-running queries, and error rate
- **Announce maintenance windows** for unavoidable locking operations
