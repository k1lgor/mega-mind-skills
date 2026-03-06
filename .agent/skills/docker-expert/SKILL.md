---
name: docker-expert
description: Dockerfiles and container orchestration. Use for Docker-related tasks.
triggers:
  - "docker"
  - "containerize"
  - "Dockerfile"
  - "docker compose"
---

# Docker Expert Skill

## Identity

You are a containerization specialist focused on Docker best practices and container orchestration.

## When to Use

- Writing Dockerfiles
- Configuring Docker Compose
- Container optimization
- Multi-stage builds

## Dockerfile Best Practices

### Multi-Stage Build

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV NODE_ENV=production

CMD ["node", "server.js"]
```

### Optimized Dockerfile

```dockerfile
# Use specific version
FROM node:20.10-alpine

# Install dependencies only when needed
WORKDIR /app

# Copy package files first (better caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy source code
COPY . .

# Build arguments for versioning
ARG VERSION=latest
ENV APP_VERSION=$VERSION

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Expose port
EXPOSE 3000

# Non-root user
USER node

# Start command
CMD ["node", "src/index.js"]
```

## Docker Compose Templates

### Development Setup

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Production Setup

```yaml
version: "3.8"

services:
  app:
    image: myapp:${VERSION:-latest}
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## Common Commands

```bash
# Build
docker build -t myapp:latest .
docker build --build-arg VERSION=1.0.0 -t myapp:1.0.0 .

# Run
docker run -d -p 3000:3000 --name myapp myapp:latest
docker run -it --rm myapp:latest sh

# Compose
docker-compose up -d
docker-compose down -v
docker-compose logs -f app

# Cleanup
docker system prune -a --volumes
docker image prune -a

# Debug
docker exec -it myapp sh
docker logs -f myapp
docker inspect myapp
```

## Dockerfile Optimization Tips

1. **Use .dockerignore**

```
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
.env
coverage
.nyc_output
```

2. **Layer Caching**

```dockerfile
# Good: Dependencies cached separately
COPY package*.json ./
RUN npm install
COPY . .

# Bad: Invalidates cache on any file change
COPY . .
RUN npm install
```

3. **Minimize Layers**

```dockerfile
# Bad: Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good: Single layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Security Best Practices

```dockerfile
# Use specific version tags
FROM node:20.10-alpine  # Good
FROM node:latest        # Bad

# Run as non-root
USER node

# Don't store secrets
# Use environment variables or secrets management

# Scan for vulnerabilities
# docker scan myapp:latest

# Use minimal base images
FROM alpine:3.19  # Smaller attack surface
```

## Tips

- Use multi-stage builds for smaller images
- Leverage build cache with proper layer ordering
- Always use specific version tags
- Run containers as non-root users
- Implement health checks
- Use .dockerignore to reduce context size
