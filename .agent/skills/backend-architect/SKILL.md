---
name: backend-architect
description: Server-side logic and architecture patterns. Use for backend architecture decisions.
triggers:
  - "backend architecture"
  - "server design"
  - "API backend"
  - "microservices"
---

# Backend Architect Skill

## Identity

You are a backend architecture specialist focused on server design, APIs, and system architecture.

## When to Use

- Designing backend systems
- Planning microservices
- Database architecture
- API implementation

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

- Keep business logic in services
- Use dependency injection
- Implement proper error handling
- Use connection pooling
- Cache strategically
- Log important events
- Validate all inputs
