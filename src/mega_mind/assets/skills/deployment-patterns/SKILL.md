---
name: deployment-patterns
compatibility: Antigravity, Claude Code, GitHub Copilot
description: CI/CD pipelines, Docker multi-stage builds, deployment strategies, health checks, and rollback procedures for production. Use when preparing to deploy, Dockerizing, or setting up CI/CD.
triggers:
  - "set up CI/CD"
  - "deploy to production"
  - "dockerize"
  - "deployment pipeline"
  - "blue-green"
  - "canary deployment"
  - "health check"
  - "rollback"
  - "production readiness"
---

# Deployment Patterns

## Identity

You are a deployment architect. You know how to take code from a developer's machine to production safely, with zero downtime, instant rollback capability, and proper observability at every stage.

## When to Activate

- Setting up CI/CD pipelines for a new project
- Dockerizing an application
- Planning deployment strategy (blue-green, canary, rolling)
- Implementing health checks and readiness probes
- Preparing for a production release
- Configuring environment-specific settings

---

## Deployment Strategies

### Rolling Deployment (Default)

Replace instances gradually — old and new versions run simultaneously during rollout.

```
Instance 1: v1 → v2  (update first)
Instance 2: v1        (still running v1)
Instance 3: v1        (still running v1)
```

**Pros:** Zero downtime, no extra infrastructure
**Cons:** Two versions run simultaneously — requires backward-compatible API changes
**Use when:** Standard deployments with backward-compatible changes

### Blue-Green Deployment

Run two identical environments. Switch traffic atomically.

```
Blue  (v1) ← 100% traffic
Green (v2)   idle, running new version

# After smoke tests pass on Green:
Blue  (v1)   idle (instant rollback available)
Green (v2) ← 100% traffic
```

**Pros:** Instant rollback (just switch back), clean cutover
**Cons:** Requires 2× infrastructure during deployment
**Use when:** Critical services, zero tolerance for mixed-version issues

### Canary Deployment

Route a small percentage of real traffic to the new version first.

```
v1: 95% → v2: 5%  (canary, watch metrics)
v1: 50% → v2: 50% (ramp if metrics look good)
v1:  0% → v2: 100% (full cutover)
```

**Pros:** Catches issues with real traffic before full rollout
**Cons:** Requires traffic splitting infrastructure
**Use when:** High-traffic services, risky changes, when feature flags are available

---

## Docker: Multi-Stage Dockerfiles

### Node.js

```dockerfile
# Stage 1: Install deps
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN bun install --frozen-lockfile (or npm ci) --production=false

# Stage 2: Build
FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bun run build (or npm run build) && npm prune --production

# Stage 3: Production image (minimal)
FROM node:22-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
USER appuser
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/package.json ./
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

### Go (scratch-based — smallest possible image)

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

FROM alpine:3.19 AS runner
RUN apk --no-cache add ca-certificates
RUN adduser -D -u 1001 appuser
USER appuser
COPY --from=builder /server /server
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["/server"]
```

### Python / Django

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
RUN useradd -r -u 1001 appuser
USER appuser
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### Docker Best Practices

```
✅ DO
- Use specific version tags (node:22-alpine, not node:latest)
- Multi-stage builds to minimize final image size
- Run as non-root user (adduser/useradd)
- Copy dependency files first to leverage layer caching
- Use .dockerignore (exclude node_modules, .git, tests, coverage)
- Add HEALTHCHECK instruction to every image
- Set resource limits in docker-compose or k8s manifests

❌ DON'T
- Run as root
- Use :latest tags in production
- Copy entire repo before installing dependencies
- Include dev dependencies in production image
- Embed secrets in image layers (use env vars or secrets manager)
```

---

## CI/CD Pipeline

### GitHub Actions (Standard Pipeline)

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: bun install --frozen-lockfile (or npm ci)
      - run: bun run lint (or npm run lint)
      - run: npm run typecheck
      - run: bun test (or npm test) -- --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage
          path: coverage/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy to production
        run: |
          # Railway: railway up
          # Vercel:  vercel --prod
          # K8s:     kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          echo "Deploying ${{ github.sha }}"
```

### Pipeline Stage Reference

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → tests → build image → deploy staging → smoke tests → deploy prod
```

---

## Health Checks

### Health Check Endpoint

```typescript
// Simple check (always available, even if DB is down)
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

// Detailed check (for internal monitoring, not load balancer)
app.get("/health/detailed", async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
  };
  const allHealthy = Object.values(checks).every((c) => c.status === "ok");
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? "ok" : "degraded",
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION ?? "unknown",
    uptime: process.uptime(),
    checks,
  });
});

async function checkDatabase(): Promise<{ status: string }> {
  try {
    await db.query("SELECT 1");
    return { status: "ok" };
  } catch {
    return { status: "error" };
  }
}
```

### Kubernetes Probes

```yaml
livenessProbe: # Kill + restart if this fails
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 30
  failureThreshold: 3

readinessProbe: # Remove from load balancer if this fails
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 2

startupProbe: # Allow slow startups (migrate DB etc.)
  httpGet:
    path: /health
    port: 3000
  periodSeconds: 5
  failureThreshold: 30 # 30 × 5s = 150s max startup time
```

---

## Environment Configuration

### Twelve-Factor App Pattern

```bash
# All config via environment variables — never hardcoded
DATABASE_URL=postgres://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
JWT_SECRET=${JWT_SECRET}       # injected from secrets manager
LOG_LEVEL=info
PORT=3000
NODE_ENV=production
```

### Validate Config at Startup (Fail Fast)

```typescript
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "staging", "production"]),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

// Crash immediately on startup with clear error if config is wrong
export const env = envSchema.parse(process.env);
```

---

## Rollback Strategy

### Instant Rollback Commands

```bash
# Kubernetes: point to previous image
kubectl rollout undo deployment/app

# Vercel: promote previous deployment
vercel rollback

# Railway: redeploy previous commit
railway up --commit <previous-sha>

# Database: rollback a migration (Prisma)
npx prisma migrate resolve --rolled-back <migration-name>
```

### Rollback Checklist

- [ ] Previous image/artifact is tagged and available in registry
- [ ] Database migrations are backward-compatible (no destructive DDL)
- [ ] Feature flags can disable new features without a deploy
- [ ] Monitoring alerts configured for error rate spikes
- [ ] Rollback procedure tested in staging at least once

---

## Production Readiness Checklist

### Application

- [ ] All tests pass (unit, integration, E2E)
- [ ] No hardcoded secrets in code or config files
- [ ] Error handling covers all edge cases (no unhandled promise rejections)
- [ ] Logging is structured JSON and does not contain PII
- [ ] `/health` endpoint returns meaningful status

### Infrastructure

- [ ] Docker image builds reproducibly with pinned version tags
- [ ] Environment variables documented and **validated at startup**
- [ ] Resource limits set (CPU, memory) in k8s / docker-compose
- [ ] SSL/TLS enabled on all public endpoints
- [ ] Secrets stored in secrets manager (not env files in repo)

### Monitoring

- [ ] Application metrics exported (request rate, latency p99, error rate)
- [ ] Alerts configured: error rate > 1%, latency p99 > SLA
- [ ] Log aggregation set up (structured logs, searchable)
- [ ] Uptime monitoring on `/health` endpoint

### Security

- [ ] Dependencies scanned for CVEs (rtk bun pm untrusted (or rtk npm audit) / safety check)
- [ ] CORS configured for allowed origins only
- [ ] Rate limiting enabled on public endpoints
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)

### Operations

- [ ] Rollback plan documented and tested in staging
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios (DB down, Redis down, OOM)
- [ ] On-call rotation and escalation path defined

---

## Tips

- **Tag images with git SHA**, not `latest` — you need to know exactly what's in prod
- **Smoke test staging** before promoting to production, every time
- **Never deploy on Friday afternoon** — give yourself time to monitor and rollback
- **Validate env vars at startup** — a missing `DATABASE_URL` should crash immediately, not silently fail on first request
- **Health checks ≠ liveness checks** — `/health` should return 200 even if a non-critical dependency is down
