---
name: k8s-orchestrator
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Kubernetes manifests and Helm charts. Use for Kubernetes deployment tasks.
triggers:
  - "kubernetes"
  - "k8s"
  - "deployment"
  - "helm chart"
  - "blue-green"
  - "canary deployment"
  - "health check"
  - "rollback"
  - "production readiness"
---

# K8s Orchestrator Skill

## Identity

You are a Kubernetes specialist focused on container orchestration, deployment, and cluster management.

## When to Use

- Creating Kubernetes manifests
- Setting up deployments
- Configuring services and ingress
- Managing Helm charts

## When NOT to Use

- Single-container apps that don't need orchestration — use Docker Compose or a simple PaaS instead
- Local development-only environments — `docker compose up` is simpler and faster
- When the team has no Kubernetes operational experience — misconfigured clusters cause outages, not just bugs
- Hobby or low-traffic projects where managed container services (Fly.io, Railway, Render) eliminate the operational overhead

## Deployment Strategies

### Rolling Deployment (Default — configured in Deployment manifest above)

Replace instances gradually — old and new versions run simultaneously during rollout.

```
Instance 1: v1 → v2  (update first)
Instance 2: v1        (still running v1)
Instance 3: v1        (still running v1)
```

**Pros:** Zero downtime, no extra infrastructure
**Cons:** Two versions run simultaneously — requires backward-compatible API changes
**Use when:** Standard deployments with backward-compatible changes

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # One extra pod during rollout
    maxUnavailable: 0  # Never reduce capacity below desired
```

### Blue-Green Deployment

Run two identical environments. Switch traffic atomically via Service selector update.

```
Blue  (v1) ← 100% traffic  (selector: version: v1)
Green (v2)   idle, running new version

# After smoke tests pass on Green:
kubectl patch service myapp -p '{"spec":{"selector":{"version":"v2"}}}'

Blue  (v1)   idle (instant rollback: patch selector back to v1)
Green (v2) ← 100% traffic
```

**Pros:** Instant rollback (just switch selector back), clean cutover, zero mixed-version traffic
**Cons:** Requires 2× pod count during deployment
**Use when:** Critical services, zero tolerance for mixed-version issues

### Canary Deployment

Route a small percentage of real traffic to the new version first using multiple Deployments + weighted Service/Ingress.

```
v1 Deployment: 19 replicas → v2 Deployment: 1 replica  (≈5% canary)
# Watch metrics. If error rate stable:
v1: 10 replicas → v2: 10 replicas  (50%)
v1:  0 replicas → v2: all replicas (full cutover)
```

**Pros:** Catches issues with real traffic before full rollout
**Cons:** Requires traffic splitting (Ingress weight annotations or service mesh)
**Use when:** High-traffic services, risky changes, when feature flags are available

```yaml
# Nginx Ingress canary annotation example
annotations:
  nginx.ingress.kubernetes.io/canary: "true"
  nginx.ingress.kubernetes.io/canary-weight: "5"
```

---

## Health Check Endpoint

### Application-Side Code (TypeScript)

```typescript
// Simple check (always available, even if DB is down — used by load balancer)
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

> **Rule:** `/health` returns 200 even if non-critical dependencies (Redis, external APIs) are down. Liveness probes use `/health`. Only the detailed endpoint checks dependencies.

### Kubernetes Probes (expanded)

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

startupProbe: # Allow slow startups (DB migrations, warm-up)
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
JWT_SECRET=${JWT_SECRET}       # injected from Kubernetes Secret
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

Map Kubernetes Secrets/ConfigMaps to env vars in the Deployment manifest:

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: myapp-secrets
        key: database-url
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: myapp-config
        key: LOG_LEVEL
```

---

## Rollback Strategy

### Instant Rollback Commands

```bash
# Kubernetes: point to previous image
kubectl rollout undo deployment/app

# Blue-Green: switch Service selector back
kubectl patch service myapp -p '{"spec":{"selector":{"version":"v1"}}}'

# Helm: rollback to previous release
helm rollback myapp 1

# Check rollout history before rolling back
kubectl rollout history deployment/app

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
- [ ] `/health` endpoint returns meaningful status independent of non-critical deps

### Infrastructure

- [ ] Docker image builds reproducibly with pinned version tags
- [ ] Environment variables documented and **validated at startup**
- [ ] Resource limits set (CPU, memory) on every container
- [ ] SSL/TLS enabled on all public endpoints
- [ ] Secrets stored in Kubernetes Secrets (not ConfigMaps or committed env files)

### Monitoring

- [ ] Application metrics exported (request rate, latency p99, error rate)
- [ ] Alerts configured: error rate > 1%, latency p99 > SLA
- [ ] Log aggregation set up (structured logs, searchable)
- [ ] Uptime monitoring on `/health` endpoint

### Security

- [ ] Dependencies scanned for CVEs (`npm audit` / `safety check`)
- [ ] CORS configured for allowed origins only
- [ ] Rate limiting enabled on public endpoints
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)

### Operations

- [ ] Rollback plan documented and tested in staging
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios (DB down, Redis down, OOM)
- [ ] On-call rotation and escalation path defined



### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - myapp
                topologyKey: kubernetes.io/hostname
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  API_URL: "https://api.example.com"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database-url: postgresql://user:password@postgres:5432/mydb
  api-key: "your-api-key"
```

## Helm Chart Structure

```
myapp/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── _helpers.tpl
└── charts/
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: My application Helm chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Common Commands

```bash
# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Get resources
kubectl get pods -l app=myapp
kubectl get services
kubectl get deployments

# Logs and exec
kubectl logs -f deployment/myapp
kubectl exec -it pod/myapp-xxx -- sh

# Scaling
kubectl scale deployment myapp --replicas=5

# Rollout
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
kubectl rollout history deployment/myapp

# Helm commands
helm install myapp ./chart
helm upgrade myapp ./chart
helm rollback myapp 1
helm uninstall myapp
```

## Best Practices

1. **Resource Limits** - Always set requests and limits
2. **Health Checks** - Implement liveness and readiness probes
3. **Pod Anti-Affinity** - Spread pods across nodes
4. **Rolling Updates** - Use for zero-downtime deployments
5. **Secrets Management** - Use external secrets operator
6. **Network Policies** - Restrict pod-to-pod communication
7. **RBAC** - Follow least privilege principle

## Tips

- Use namespaces for environment isolation
- Implement proper resource quotas
- Set up monitoring and alerting
- Use GitOps for deployments
- Regular security updates

## Anti-Patterns

- Never deploy to Kubernetes without resource requests and limits on every container because a container without limits can consume all node resources, triggering OOM kills on co-located pods and causing a cascading cluster failure.
- Never use `latest` as the image tag in a Kubernetes manifest because `latest` is mutable and a node pulling a new image silently changes the running version, making rollbacks and incident diagnosis impossible.
- Never expose a service with `type: LoadBalancer` without understanding the cloud cost implications because each LoadBalancer provisions a cloud load balancer that incurs per-hour charges even when idle, and a misconfigured service can accumulate hundreds of dollars per day.
- Never apply manifests directly to a production cluster with `kubectl apply` without a GitOps review process because direct applies bypass change tracking, make rollback difficult, and allow untested configuration to reach production.
- Never configure a Deployment without a `readinessProbe` because Kubernetes will route traffic to a pod immediately on container start, before the application is ready to serve requests, causing a percentage of requests to fail during every deployment.
- Never set `replicas: 1` for a production workload without documenting the reason because a single-replica deployment has zero tolerance for node failure or rolling updates, causing downtime during routine maintenance.
- Never skip canary error-rate monitoring before full cutover because a latent bug that only manifests under partial load is indistinguishable from normal variance without a baseline comparison, causing a full rollout of a broken release.
- Never disable health checks during a blue/green cutover because traffic routes to the new instance before it is warm, causing a burst of 5xx errors to real users instead of routing remaining on the old instance.
- Never use `latest` image tags in production deployments because `latest` can silently change between pulls, making rollbacks ambiguous and deployments non-reproducible.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Pod in CrashLoopBackOff due to missing env var or secret | Required environment variable not defined in the Deployment manifest or the referenced Secret does not exist in the namespace | Run `kubectl describe pod <name>` to read the exit reason; check `kubectl get secret` to confirm the secret exists; add the missing env var or create the secret |
| OOMKilled because resource limits set below actual memory footprint | `limits.memory` configured lower than the application's steady-state memory usage, causing the kernel OOM killer to terminate the container | Run `kubectl top pod` to measure actual usage; raise `limits.memory` above the P99 memory reading; set `requests.memory` to match measured baseline |
| ImagePullBackOff from wrong registry URL or missing pull secret | Image tag references a private registry but no `imagePullSecrets` is set, or the image path has a typo | Run `kubectl describe pod <name>` for the exact error; verify the image path with `docker pull`; create and reference an `imagePullSecret` for private registries |
| PersistentVolumeClaim stuck Pending because StorageClass not found | Manifest references a `storageClassName` that does not exist in the cluster, so no PV is provisioned | Run `kubectl get storageclass` to list available classes; update the PVC to use an existing class or create the missing StorageClass |
| Liveness probe too aggressive, killing healthy pod under startup load | `initialDelaySeconds` too short or `failureThreshold` too low; probe fires before the app finishes initializing under load | Increase `initialDelaySeconds` to exceed app startup time; use a `startupProbe` for slow-starting containers; validate with `kubectl describe pod` that the probe is not triggering restarts |

## Self-Verification Checklist

- [ ] All changed manifests pass dry-run validation: `kubectl apply --dry-run=client -f <manifest>` exits 0 with 0 validation errors for every changed file
- [ ] All pods in Running or Completed state: `kubectl get pods -n <namespace> --field-selector=status.phase!=Running,status.phase!=Succeeded | wc -l` returns 0 (header line only) — any pod in CrashLoopBackOff or Pending is a blocking failure
- [ ] Resource requests and limits set on all containers: `kubectl get pods -n <namespace> -o json | python -c "import sys,json; pods=json.load(sys.stdin); [print(c['name']) for p in pods['items'] for c in p['spec']['containers'] if not c.get('resources',{}).get('limits')]"` returns 0 lines
- [ ] Liveness and readiness probes configured on every Deployment: `kubectl get deployments -n <namespace> -o json | python -c "import sys,json; d=json.load(sys.stdin); [print(c['name']) for dep in d['items'] for c in dep['spec']['template']['spec']['containers'] if not c.get('livenessProbe')]"` returns 0 lines
- [ ] Secrets stored in Kubernetes Secret resources: `grep -rn "password\|secret\|token" <manifests_dir>/*.yaml | grep -v "kind: Secret\|secretKeyRef\|secretRef"` returns 0 matches — plaintext secrets in ConfigMap or env literals fail this check
- [ ] Pod anti-affinity rules set: `grep -rn "podAntiAffinity\|topologyKey" <manifests_dir>` returns at least 1 match per Deployment with replica count > 1
- [ ] No `latest` image tags: `grep -rn "image:.*:latest" <manifests_dir>` returns 0 matches — all images use a pinned version tag or SHA digest

## Success Criteria

This skill is complete when: 1) all Deployments have resource limits, liveness probes, and readiness probes configured, 2) secrets are stored in Kubernetes Secret resources with no plaintext in ConfigMaps or manifests, and 3) the deployment is namespaced correctly and follows least-privilege RBAC.
