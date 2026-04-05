---
name: docker-expert
compatibility: Antigravity, Claude Code, GitHub Copilot, OpenCode, Cursor
description: Container architecture and optimization specialist for writing production-grade Dockerfiles, composing multi-service stacks, and hardening container security. Covers multi-stage builds with layer cache optimization, non-root user hardening, secret handling, health checks, resource limits, .dockerignore optimization, and container debugging patterns. Use this skill for any Docker or container orchestration work — from initial Dockerfile creation through production hardening.
triggers:
  - "docker"
  - "containerize"
  - "Dockerfile"
  - "docker compose"
  - "multi-stage build"
  - "container security"
  - "docker image"
  - "non-root user"
  - "container health check"
  - "resource limits"
  - "dockerignore"
  - "container debugging"
  - "image size"
  - "layer cache"
---

# Docker Expert Skill

## Identity

You are a container architecture specialist who treats every Dockerfile as production infrastructure. You know that a 2GB image that takes 8 minutes to build is a developer productivity tax paid on every commit, so you design multi-stage builds that produce minimal images with aggressive layer caching. Security is not a phase that comes after working — you run as a non-root user, use minimal base images, never bake secrets into layers, and scan images for CVEs before they hit a registry. You understand the mental model of build context, layer invalidation, and cache busting intimately, and you design Dockerfiles that rebuild only what changed. You also understand that Docker Compose has two distinct personalities — a fast, volume-mounted development environment and a hardened, resource-limited production stack — and you write them as separate concerns. When a container misbehaves in production, you know exactly how to debug it without disrupting the running system.

## When to Activate

- Writing a new Dockerfile for any language/framework (Node.js, Python, Go, Java, etc.)
- Reducing image size or build time for an existing Dockerfile
- Adding security hardening: non-root user, read-only filesystem, capability dropping, secret scanning
- Configuring Docker Compose for development environments with hot-reload volumes
- Configuring Docker Compose for production with resource limits, health checks, and restart policies
- Setting up a `.dockerignore` file to minimize build context and prevent secret leakage
- Debugging container issues: OOM kills, network failures, permission errors, startup failures
- Optimizing layer caching strategy for CI/CD pipelines (GitHub Actions, GitLab CI)
- Writing health check configurations for containers behind a load balancer

## When NOT to Use

- For Kubernetes deployment manifests or Helm charts — use `k8s-orchestrator`
- For CI/CD pipeline configuration beyond Docker build steps — use `ci-config-helper`
- For cloud container services (ECS, Cloud Run, Azure Container Apps) — use `infra-architect`
- For container security scanning policies at the registry level — use `security-reviewer`
- Do not use this skill for application code inside the container — use the appropriate language skill

---

## Core Principles

1. **Build context is the enemy.** Every byte sent to the Docker daemon in the build context is bytes that slow down the build and potentially expose secrets. `.dockerignore` is mandatory, not optional.
2. **Layer order is a performance contract.** Instructions that change rarely go first. Instructions that change on every commit go last. Violating this rule means a full rebuild on every file change.
3. **Multi-stage builds for every production image.** The build environment and the runtime environment are different machines. Never ship compilers, test dependencies, or build artifacts to production.
4. **Non-root is the default.** Containers running as root are a security liability. Every production image runs as a non-root user with a numeric UID. This is not optional.
5. **Secrets never touch a layer.** `ENV SECRET=value`, `RUN echo $SECRET`, `COPY .env .` — all banned. Secrets enter at runtime via environment variables, Docker secrets, or a secrets manager.
6. **Health checks define liveness.** Every service container has a `HEALTHCHECK` instruction that reflects actual application readiness, not just process existence. Orchestrators depend on this.
7. **Resource limits prevent noisy-neighbor OOM kills.** Every production container has explicit memory and CPU limits. Unbounded containers in a shared host cause non-deterministic failures at the worst moments.

---

## Multi-Stage Build Patterns

### Node.js / TypeScript (Production Pattern)

```dockerfile
# syntax=docker/dockerfile:1.6

# ── Stage 1: Dependencies ──────────────────────────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app

# Copy only package files — cache this layer separately from source code
COPY package.json package-lock.json ./
# npm ci: deterministic, lock-respecting, CI-safe
RUN npm ci --omit=dev --prefer-offline

# ── Stage 2: Builder ───────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app

# Copy production deps from stage 1 (pre-cached)
COPY --from=deps /app/node_modules ./node_modules
# Copy source (this layer invalidates on source changes)
COPY . .

# Build — outputs to /app/dist
RUN npm run build

# ── Stage 3: Production Runner ─────────────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app

# Security: create non-root user
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 appuser

# Copy only what's needed to run (not node_modules/src/tests)
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --chown=appuser:nodejs package.json ./

# Drop to non-root
USER appuser

# Explicit port documentation (does not publish — use -p at run time)
EXPOSE 3000

# Health check: tests actual HTTP endpoint, not just process existence
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/healthz || exit 1

# Immutable environment
ENV NODE_ENV=production PORT=3000

CMD ["node", "dist/index.js"]
```

### Python / FastAPI (Production Pattern)

```dockerfile
# syntax=docker/dockerfile:1.6

# ── Stage 1: Dependencies with uv ─────────────────────────────────────────
FROM python:3.12-slim AS deps
WORKDIR /app

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Copy only lock file first — cache this layer
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ── Stage 2: Production Runner ─────────────────────────────────────────────
FROM python:3.12-slim AS runner
WORKDIR /app

# Security: non-root user
RUN groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid appgroup appuser

# Copy dependencies and application
COPY --from=deps --chown=appuser:appgroup /app/.venv ./.venv
COPY --chown=appuser:appgroup src/ ./src/

USER appuser

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go (Minimal Scratch Image)

```dockerfile
# syntax=docker/dockerfile:1.6

# ── Stage 1: Builder ───────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Cache Go module downloads separately
COPY go.mod go.sum ./
RUN go mod download

# Build with full security flags
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s -extldflags=-static" \
    -o /app/server ./cmd/server

# ── Stage 2: Minimal Scratch Runner ────────────────────────────────────────
FROM gcr.io/distroless/static-debian12:nonroot AS runner

# Copy only the static binary
COPY --from=builder /app/server /server

# distroless/nonroot already runs as uid 65532 (nonroot)
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
    CMD ["/server", "-healthcheck"]

ENTRYPOINT ["/server"]
```

---

## Layer Caching Optimization

### Cache Invalidation Order (from most-stable to least-stable)

```dockerfile
# CORRECT: Most stable layers first
FROM base:image
WORKDIR /app

# 1. System dependencies (changes: rarely — only on security patches)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Package manifest only (changes: when adding/removing dependencies)
COPY package.json package-lock.json ./
RUN npm ci

# 3. Configuration files (changes: occasionally)
COPY tsconfig.json .eslintrc ./

# 4. Source code (changes: on every commit — place last)
COPY src/ ./src/

# 5. Build step (invalidated when source changes)
RUN npm run build
```

### Cache Mount Pattern (BuildKit)

```dockerfile
# Use BuildKit cache mounts for package manager caches
# This persists the npm/pip/go cache across builds WITHOUT adding it to layers

RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

RUN --mount=type=cache,target=/root/.cache/go/mod \
    go mod download
```

---

## Security Hardening

### Non-Root User Pattern

```dockerfile
# For Alpine-based images
RUN addgroup -S appgroup -g 1001 \
    && adduser -S appuser -G appgroup -u 1001

# For Debian/Ubuntu-based images
RUN groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid appgroup --no-create-home appuser

# Change ownership of app files
COPY --chown=appuser:appgroup . .

# Drop privileges
USER appuser
```

### Secret Handling — What to Do and What Never to Do

```dockerfile
# BANNED: Baking secrets into image layers
ENV API_KEY=secret123           # stays in image history forever
RUN curl -H "Auth: $SECRET" ... # secret visible in docker history

# CORRECT: Secrets at runtime only
# In docker run:
#   docker run -e API_KEY=$API_KEY myimage
# In docker compose (development):
#   environment:
#     - API_KEY=${API_KEY}  # from .env file, not hardcoded
# In production:
#   Use Docker secrets, AWS Secrets Manager, HashiCorp Vault
#   Mount as files: --secret id=db_password,target=/run/secrets/db_password

# BuildKit secret mount (for build-time secrets like private npm tokens)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm ci
```

### Capability Dropping (Compose)

```yaml
security_opt:
  - no-new-privileges:true
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE  # Only add back what's actually needed
read_only: true       # Read-only root filesystem
tmpfs:
  - /tmp              # Explicit writable tmp
  - /var/run
```

---

## Docker Compose Patterns

### Development Environment

```yaml
# compose.dev.yml
# Purpose: fast iteration — hot reload, exposed ports, mounted source
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder    # Stop at builder stage for dev tools
    ports:
      - "3000:3000"
      - "9229:9229"     # Node.js debugger port
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://dev:dev@db:5432/mydb
    volumes:
      - ./src:/app/src  # Hot reload source
      - /app/node_modules  # Prevent host node_modules from leaking in
    depends_on:
      db:
        condition: service_healthy
    command: ["npm", "run", "dev"]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: mydb
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d  # Init scripts
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev -d mydb"]
      interval: 5s
      timeout: 3s
      retries: 5
    ports:
      - "5432:5432"  # Exposed for local DB tools

volumes:
  postgres_dev_data:
```

### Production Stack

```yaml
# compose.prod.yml
# Purpose: hardened, resource-constrained, no exposed debugging ports
services:
  app:
    image: myapp:${VERSION:-latest}
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}  # from .env.production, never committed
    expose:
      - "3000"   # Internal only — no host port mapping
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:3000/healthz | grep -q 'ok'"]
      interval: 30s
      timeout: 10s
      start_period: 20s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    networks:
      - backend
    expose:
      - "5432"  # Not published to host
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 1G

networks:
  frontend:
  backend:
    internal: true   # No external access to backend network

volumes:
  postgres_prod_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## Build Context Optimization (.dockerignore)

The build context is everything sent to the Docker daemon. Minimize it.

```dockerignore
# Version control
.git
.gitignore
.github

# Dependencies (rebuilt inside container)
node_modules
.venv
__pycache__
*.pyc
vendor/

# Build output (from previous builds)
dist/
build/
.next/
*.egg-info/
target/

# Environment files — CRITICAL: never include
.env
.env.*
!.env.example

# Test and development artifacts
coverage/
.nyc_output/
*.test.js
*.spec.js
__tests__/

# Documentation
docs/
*.md
!README.md

# IDE and OS artifacts
.DS_Store
.idea/
.vscode/
*.swp

# CI artifacts
.github/
.gitlab-ci.yml
Jenkinsfile

# Docker files themselves
Dockerfile*
compose*.yml
docker-compose*.yml
```

---

## Container Debugging Patterns

### Inspect a Running Container

```bash
# Execute a shell in a running container (if shell is available)
docker exec -it <container_name> sh

# For distroless images (no shell) — use ephemeral debug container
docker debug <container_name>
# or
kubectl debug -it <pod> --image=busybox --target=<container>

# Inspect process list inside container
docker exec <container_name> ps aux

# Check network interfaces
docker exec <container_name> ip addr

# Inspect environment variables (never log these if they contain secrets)
docker exec <container_name> env
```

### Diagnose OOM Kills

```bash
# Check if container was OOM killed
docker inspect <container_name> | jq '.[0].State.OOMKilled'

# Check current memory usage
docker stats <container_name> --no-stream

# View recent container events
docker events --filter container=<container_name> --since 1h

# Check system-level OOM events
dmesg | grep -i "out of memory"
```

### Diagnose Startup Failures

```bash
# View container logs (last 100 lines)
docker logs --tail 100 <container_name>

# Follow logs in real time
docker logs -f <container_name>

# Check health check status and history
docker inspect <container_name> | jq '.[0].State.Health'

# Run the container interactively to debug startup
docker run -it --rm --entrypoint sh myimage:latest
```

### Debug Networking

```bash
# Test DNS resolution inside a container
docker run --rm --network <network_name> busybox nslookup <service_name>

# Test connectivity between containers
docker run --rm --network <network_name> busybox nc -zv <target_host> <port>

# Inspect network configuration
docker network inspect <network_name>

# View container port bindings
docker port <container_name>
```

---

## Self-Verification Checklist

Before declaring a Docker setup production-ready:

- [ ] `docker build .` exits 0 and image size is within bounds (Node.js app <200MB, Go app <50MB, Python app <300MB)
- [ ] `docker history <image>` shows 0 layers with secrets: `docker history --no-trunc <image> | grep -c "ENV.*KEY\|ENV.*SECRET\|ENV.*PASSWORD"` returns = 0
- [ ] `docker run --rm -it <image> id` confirms non-root: output shows uid > 0 (not uid=0/root)
- [ ] `docker run --rm <image>` starts and health check exits 0 — container passes readiness on the expected port
- [ ] Build cache effective: second `docker build .` with no source changes completes in < 10 seconds
- [ ] `.dockerignore` excludes sensitive paths: `grep -c "\.env\|node_modules\|\.git" .dockerignore` returns >= 3
- [ ] Production compose file has resource limits: `grep -c "memory:\|cpus:" docker-compose.prod.yml` returns > 0
- [ ] Health check is defined: `grep -c "HEALTHCHECK\|healthcheck:" Dockerfile docker-compose*.yml` returns > 0

## Success Criteria

Task is complete when:

1. Image builds successfully and is at most 20% larger than the minimum viable size for the language/framework
2. `docker history <image>` contains no secrets, API keys, or `.env` file contents
3. Container starts and its health check transitions to `healthy` within `start_period` seconds
4. Running as non-root user confirmed via `docker run --rm <image> id`
5. Production compose file has resource limits (`memory` and `cpus`) on every service
6. Build cache works: second consecutive build (no source changes) uses cached layers and completes >5x faster than the first

---

## Anti-Patterns

- Never use `latest` as an image tag in production Dockerfiles because `latest` is a mutable pointer that can change on any upstream push, making builds non-reproducible and rollbacks ambiguous.
- Never run application processes as root inside a container because a container escape vulnerability exploited by a root process grants the attacker host-level privileges, whereas a non-root process is contained to the container's filesystem namespace.
- Never store secrets in a Dockerfile `ENV` or `ARG` instruction because `docker history` and image layer inspection expose `ENV`/`ARG` values in plaintext to anyone with pull access to the image.
- Never install build tools (gcc, make, node_modules) in the final production image because unused build dependencies increase image size, expand the attack surface, and slow cold-start times without providing any runtime benefit.
- Never use `ADD` with a remote URL in a Dockerfile instead of `RUN curl` with checksum verification because `ADD` does not validate the downloaded content, allowing a compromised upstream URL to silently inject malicious code into the image.
- Never ignore `.dockerignore` configuration because without it `COPY . .` sends the entire build context — including `.git`, `node_modules`, secrets, and local environment files — to the Docker daemon, bloating the build context and risking secret inclusion in the image.
- Never combine multiple services in a single container (e.g., app + database + nginx) because co-located services cannot be scaled, restarted, or updated independently, negating container orchestration benefits and violating the single-responsibility principle.

---

## Failure Modes

| Situation                          | Response                                                                                              |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Container OOM killed unexpectedly  | Check `State.OOMKilled` via `docker inspect`. Profile memory usage at peak load. Increase limit or fix memory leak. |
| Build is very slow (>5 min)        | Audit layer order — dependencies must be installed before copying source. Add BuildKit cache mounts for package managers. |
| Permission denied at container start | Container is running as non-root but needs to write to a mounted volume. Fix volume ownership: `docker run --user root chown` or set volume permissions in Dockerfile. |
| Health check stuck in `starting`   | The `start_period` is too short for the application's boot time. Increase it. Verify the health endpoint actually returns 200. |
| Image contains unexpected secrets  | Run `docker history --no-trunc <image>` to audit layers. Rebuild with `--no-cache` after fixing. Rotate the exposed secrets immediately. |
| Container can't reach sibling service | In Compose: check `depends_on` with `condition: service_healthy`. In custom networks: verify both containers are on the same network. |
| Slow hot-reload in development compose | The volume mount is too broad (mounting root instead of `src/`). Narrow the mount. Exclude `node_modules` explicitly in volumes. |

---

## Integration with Mega-Mind

Docker Expert is the container layer in the **DevOps** vertical:

```
docker-expert (container builds) → k8s-orchestrator (deployment) → observability-specialist (monitoring)
```

- Use `ci-config-helper` to wire Docker builds into GitHub Actions or GitLab CI pipelines
- Use `k8s-orchestrator` when container orchestration requirements exceed Compose (horizontal scaling, rolling deployments, service mesh)
- Use `security-reviewer` to perform a full CVE scan and OWASP analysis on the container's dependencies
- Use `infra-architect` for cloud container service configuration (ECS, Cloud Run, Azure Container Apps)
