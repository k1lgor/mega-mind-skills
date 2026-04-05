---
name: backend-architect
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Server-side logic, architecture patterns, and API contract design. Use for backend architecture decisions, service/repository implementation, and designing REST/GraphQL API contracts.
triggers:
  - "backend architecture"
  - "server design"
  - "API backend"
  - "microservices"
  - "design API"
  - "REST API"
  - "GraphQL"
  - "OpenAPI"
  - "API conventions"
  - "pagination"
  - "cursor pagination"
  - "api versioning"
  - "error response format"
  - "API consistency"
---

# Backend Architect Skill

## Identity

You are a backend architecture specialist focused on server design, APIs, and system architecture.

## When to Use

- Designing backend systems
- Planning microservices
- Database architecture
- API implementation
- Designing new REST or GraphQL endpoints
- Creating OpenAPI/Swagger specifications
- Standardizing error response formats and pagination

## When NOT to Use

- Simple CRUD endpoints that follow an already-established pattern in the codebase — just replicate the existing pattern
- Frontend or UI concerns — use `frontend-architect` instead
- Infrastructure provisioning (VPCs, load balancers, etc.) — use `infra-architect` instead

## Architecture Patterns

### Layered Architecture

```
src/
├── controllers/    # HTTP handlers
├── services/       # Business logic
├── repositories/   # Data access
├── models/         # Domain entities
├── middleware/     # Cross-cutting concerns
└── utils/          # Utilities
```

### Clean Architecture

```
src/
├── domain/         # Core business logic
│   ├── entities/
│   └── usecases/
├── application/    # Application services
│   ├── services/
│   └── dto/
├── infrastructure/ # External services
│   ├── database/
│   ├── cache/
│   └── messaging/
└── presentation/   # API layer
    ├── controllers/
    └── routes/
```

## Service Layer Pattern

```typescript
// user.service.ts
export class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly eventBus: EventBus,
    private readonly cache: CacheService,
  ) {}

  async getUser(id: string): Promise<User> {
    // Check cache first
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;

    // Fetch from repository
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError("User not found");

    // Cache result
    await this.cache.set(`user:${id}`, user, 3600);

    return user;
  }

  async createUser(data: CreateUserDTO): Promise<User> {
    // Validate
    this.validateCreateData(data);

    // Check for duplicates
    const exists = await this.userRepo.findByEmail(data.email);
    if (exists) throw new ConflictError("Email already exists");

    // Create user
    const user = await this.userRepo.create(data);

    // Emit event
    await this.eventBus.emit("user.created", { userId: user.id });

    return user;
  }
}
```

## Repository Pattern

```typescript
// user.repository.ts
export interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: UpdateUserDTO): Promise<User>;
  delete(id: string): Promise<void>;
}

// postgres-user.repository.ts
export class PostgresUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.db.query("SELECT * FROM users WHERE id = $1", [id]);
    return row ? this.toDomain(row) : null;
  }

  private toDomain(row: UserRow): User {
    return {
      id: row.id,
      email: row.email,
      name: row.name,
      createdAt: row.created_at,
    };
  }
}
```

## Middleware Chain

```typescript
// Middleware composition
app.use(cors());
app.use(helmet());
app.use(rateLimiter());
app.use(authMiddleware);
app.use(requestLogger);
app.use(router);

// Custom middleware
export const authMiddleware = async (req, res, next) => {
  try {
    const token = extractToken(req.headers.authorization);
    const user = await verifyToken(token);
    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({ error: "Unauthorized" });
  }
};
```

## Error Handling

```typescript
// Custom errors
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code: string = "INTERNAL_ERROR",
  ) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, "NOT_FOUND");
  }
}

export class ValidationError extends AppError {
  constructor(errors: ValidationError[]) {
    super("Validation failed", 400, "VALIDATION_ERROR");
    this.details = errors;
  }
}

// Error handler middleware
export const errorHandler = (err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
    });
  }

  console.error(err);
  res.status(500).json({
    error: {
      code: "INTERNAL_ERROR",
      message: "An unexpected error occurred",
    },
  });
};
```

## API Contract Design

### RESTful API Design Principles

**URL Structure & Naming:**

```
GET    /api/v1/users           # list
GET    /api/v1/users/:id       # single resource
POST   /api/v1/users           # create
PUT    /api/v1/users/:id       # full replace
PATCH  /api/v1/users/:id       # partial update
DELETE /api/v1/users/:id       # delete

# Sub-resources for ownership relationships
GET    /api/v1/users/:id/orders

# Actions — use POST with a verb suffix
POST   /api/v1/orders/:id/cancel
```

Naming rules: ✅ `/api/v1/team-members` (kebab-case, plural)  ❌ `/api/v1/getUsers` (verb in URL)

**HTTP Methods & Status Codes:**

| Method | Purpose           | Idempotent |
| ------ | ----------------- | ---------- |
| GET    | Retrieve resource | ✅ Yes     |
| POST   | Create / Action   | ❌ No      |
| PUT    | Full replace      | ✅ Yes     |
| PATCH  | Partial update    | ❌ No      |
| DELETE | Remove resource   | ✅ Yes     |

| Code | Meaning              | Use Case                              |
| ---- | -------------------- | ------------------------------------- |
| 200  | OK                   | Successful GET, PUT, PATCH            |
| 201  | Created              | Successful POST (add `Location`)      |
| 204  | No Content           | Successful DELETE (no body)           |
| 400  | Bad Request          | Invalid data (validation error)       |
| 401  | Unauthorized         | Missing or invalid auth token         |
| 403  | Forbidden            | Authenticated but not allowed         |
| 404  | Not Found            | Resource doesn't exist                |
| 409  | Conflict             | State conflict (e.g. duplicate email) |
| 422  | Unprocessable Entity | Business rule violation               |
| 500  | Internal Error       | Unexpected server failure             |

### Response Formats

```json
{ "data": { "id": "abc-123", "name": "Alice", "created_at": "2025-01-15T10:30:00Z" } }
```

Error response (machine-readable):

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [{ "field": "email", "message": "Must be valid email", "code": "invalid_format" }]
  }
}
```

### Pagination Strategies

**Offset-Based:** `GET /api/v1/users?page=2&per_page=20` — simple, supports "jump to page N"; slow on large offsets, inconsistent with concurrent inserts.

**Cursor-Based:** `GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20` — O(1) performance, stable with concurrent inserts; cannot jump to arbitrary page.

### GraphQL Schema Example

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
}

type Query {
  user(id: ID!): User
  me: User
}

type Mutation {
  updateProfile(input: UpdateProfileInput!): User!
}
```

### API Design Checklist

- [ ] Resource URL uses plural nouns in kebab-case with no verbs
- [ ] Correct HTTP method used (GET for reads, POST for creates, etc.)
- [ ] Appropriate status codes returned (not 200 for everything)
- [ ] Error responses follow standard format with machine-readable `code`
- [ ] Pagination implemented for all list endpoints
- [ ] Authentication required (or explicitly marked as public)
- [ ] Authorization checked (user can only access their own resources)
- [ ] Response does not leak internal details (no stack traces, no DB field names)
- [ ] Consistent naming with existing endpoints
- [ ] OpenAPI/Swagger spec updated

## Database Patterns

### Connection Pooling

```typescript
import { Pool } from "pg";

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const query = (text: string, params: any[]) => pool.query(text, params);
```

### Transaction Management

```typescript
export const transferFunds = async (
  fromId: string,
  toId: string,
  amount: number,
) => {
  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    // Debit
    await client.query(
      "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
      [amount, fromId],
    );

    // Credit
    await client.query(
      "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
      [amount, toId],
    );

    await client.query("COMMIT");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
};
```

## Tips

- Keep business logic in services; use dependency injection
- Use connection pooling; cache strategically; log important events; validate all inputs
- Return the resource after POST/PUT/PATCH — avoid extra GET requests
- Use ISO 8601 for dates, snake_case for JSON keys, URL path versioning `/api/v1/`

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| N+1 query in ORM layer causing 10x DB load under traffic | ORM fetches related records one-by-one inside a loop instead of a single JOIN or `include` | Replace with eager loading (`include`/`select_related`) and verify query count drops to 1 in test with query logging enabled |
| Missing database index on join column causing full table scan | Foreign key or filter column has no index; invisible at low data volume but catastrophic at scale | Run `EXPLAIN ANALYZE` on the slow query, add index on the join/filter column, confirm sequential scan becomes index scan |
| Unhandled async rejection crashing Node/Python worker silently | `await` call inside an event emitter or background task with no `.catch()` or `try/catch` wrapper | Add a global `unhandledRejection` handler that logs and alerts; audit all fire-and-forget async calls for error handling |
| JWT secret hardcoded in source, leaking in git history | Secret pasted directly into source file and committed; rotation requires code change | Rotate the secret immediately, move to environment variable / secrets manager, run `git filter-repo` to purge from history |
| Rate limiter not applied to auth endpoint, enabling brute-force | Rate-limiting middleware placed after the auth route or only on non-auth paths | Move rate limiter middleware to apply before auth routes; confirm with a load test that >N requests/minute returns 429 |
| Breaking change in response schema silently accepted by client | Client uses loose deserialization and ignores unknown fields; downstream consumers not tested | Add contract tests (e.g. Pact) that fail on schema change; version the endpoint |
| Missing auth on new endpoint due to global middleware ordering | New route registered before auth middleware is applied | Audit middleware registration order; add integration test that hits the endpoint unauthenticated and expects 401 |
| Request body not validated, enabling injection | Validation schema omitted or `additionalProperties: true` left in place | Add JSON Schema / Zod validation for every incoming body; reject unknown fields by default |
| Pagination not implemented, causing full table scan on large dataset | Endpoint returns all rows; dataset size not anticipated at design time | Add `limit`/`offset` or cursor pagination to every list endpoint; document max page size |

## Anti-Patterns

- Never load an entire database table into application memory to filter in code because the query result set grows with the table, causing OOM crashes at scale that do not appear in development with small datasets.
- Never open a database connection per HTTP request without a connection pool because each new connection incurs TCP and TLS handshake overhead plus server-side resources; under moderate load the database connection limit is exhausted before CPU or memory, causing request queuing and timeouts.
- Never return raw database error messages in HTTP API responses because internal table names, column names, and SQL syntax details enable schema enumeration attacks and leak information useful for SQL injection probing.
- Never mix business logic into database migration files because migrations run sequentially and cannot be rolled back without a compensating migration; business logic in migrations is untestable in isolation and creates an irrevocable dependency on the schema state at that migration's point in time.
- Never implement authentication by comparing password strings directly instead of using a constant-time comparison function because standard string equality short-circuits on the first differing byte, enabling timing attacks that reveal password length or prefix.
- Never expose an internal gRPC or service-mesh API on a public network interface because internal protocols often lack authentication and rate limiting intended for public endpoints, allowing unauthenticated callers to invoke privileged operations.
- Never call a downstream service synchronously inside a database transaction because if the downstream call is slow or fails, the transaction holds locks for the entire duration, blocking other writers and causing cascading timeouts across the system.
- Never design an API endpoint that returns all records without pagination because a dataset that is small today will cause full table scans and memory exhaustion when it grows to millions of rows in production.
- Never accept arbitrary JSON without a strict schema validation layer because unvalidated input is the root cause of injection attacks, type confusion bugs, and downstream data corruption.
- Never break backward compatibility in a versioned API without incrementing the version identifier because existing clients will fail silently or with cryptic errors when their assumed contract changes under them.
- Never expose internal domain model field names directly in the API response because internal names leak implementation details, create a coupling between API consumers and database schema, and make future refactors breaking changes.
- Never omit error response schemas from the API contract because callers cannot write correct error handling code for errors whose shape they do not know, leading to unhandled exceptions in production.
- Never add authentication to individual routes ad hoc because inconsistent auth coverage creates gaps where new routes are accidentally left unauthenticated, bypassing access control entirely.
- Never design synchronous endpoints for operations that take more than 500ms because slow synchronous responses block client threads, degrade perceived performance, and cause cascading timeouts under load.

## Self-Verification Checklist

- [ ] `lsp_diagnostics` returns 0 errors on all changed files
- [ ] Build exits with code 0 (`tsc --noEmit` or equivalent compiler check passes)
- [ ] All existing tests pass — `npm test` (or equivalent) exits 0; any pre-existing failures are documented
- [ ] No hardcoded secrets: `grep -rn "secret\|password\|api_key" src/` returns 0 matches on literal string values
- [ ] Service layer is separated from controller/route layer — no business logic lives in request handlers
- [ ] All database queries use parameterized statements or ORM query builders (no raw string interpolation)
- [ ] Repository interfaces are defined and concrete implementations are injected (testable via mock)
- [ ] Custom error classes cover all domain error cases and map to correct HTTP status codes
- [ ] Connection pooling is configured with explicit `max` connections and `idleTimeoutMillis`
- [ ] Transactions are used for multi-table writes that must be atomic
- [ ] All resource URLs use plural nouns in kebab-case with no verbs
- [ ] All list endpoints have pagination: cursor or offset/limit implemented and documented
- [ ] OpenAPI spec validates without errors: `npx swagger-parser validate openapi.yaml` exits 0
- [ ] Error responses include a machine-readable `code` field
- [ ] All endpoints that return user-specific data enforce authorization (not just authentication)

## Success Criteria

This task is complete when:
1. The layered architecture is implemented with clear separation between controllers, services, and repositories
2. All public service methods have unit tests with 90%+ function coverage
3. Error handling is consistent: every error path returns a structured error response, not a raw stack trace
4. An OpenAPI specification exists for all designed endpoints with request/response schemas fully defined
5. The API Design Checklist above is completed with all items checked
