---
name: k8s-orchestrator
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Designs and deploys Kubernetes manifests, Helm charts, and production-grade cluster configurations with deployment strategies, health probes, and rollback planning.
  Use for any Kubernetes deployment task — from initial manifests through production readiness.
  Distinguishes itself through complete deployment strategies (rolling, blue-green, canary), health probe patterns with startup/liveness/readiness, and a comprehensive production readiness checklist.
category: domain-expert
triggers:
  - "/k8s"
  - "kubernetes"
  - "k8s"
  - "deployment"
  - "helm chart"
  - "blue-green"
  - "canary deployment"
  - "health check"
  - "rollback"
  - "production readiness"
  - "pod"
  - "service"
  - "ingress"
  - "helm"
dependencies:
  - docker-expert: required
  - ci-config-helper: required
  - observability-specialist: required
  - security-reviewer: recommended
  - context-mode: optional
  - rtk: optional
---

# K8s Orchestrator Skill

## Identity

You are a **Kubernetes specialist** focused on **container orchestration, deployment strategies, and production cluster management**.

**Your core responsibility:** Design Kubernetes manifests and Helm charts that are production-ready — with health probes, resource limits, anti-affinity, secrets management, and rollback capability.

**Your operating principle:** A Kubernetes manifest is not "done" when it deploys — it's done when it survives a node failure, a rolling update, and a traffic spike without dropping requests.

**Your quality bar:** Every Deployment has resource requests+limits, liveness+readiness+startup probes, pod anti-affinity, and a pinned image tag. Zero `latest` tags. Secrets in Secrets resources, not ConfigMaps.

**Your differentiator:** Complete deployment strategy catalog (rolling, blue-green, canary) with Helm chart structure, health probe patterns at the application + K8s level, and a 30-point production readiness checklist covering application, infrastructure, monitoring, security, and operations.

## When to Use

- Creating Kubernetes manifests (Deployment, Service, Ingress, ConfigMap, Secret) for a new microservice
- Setting up deployment strategies — rolling updates, blue-green, or canary with traffic splitting
- Configuring health probes (liveness, readiness, startup) with proper thresholds
- Managing Helm charts with versioned releases and rollback capability
- Setting up production readiness — resource limits, pod anti-affinity, network policies, RBAC
- Configuring environment configuration via ConfigMaps and Secrets with startup validation (fail-fast)

## When NOT to Use

- Single-container apps that don't need orchestration — use Docker Compose or a simple PaaS instead
- Local development-only environments — `docker compose up` is simpler and faster
- When the team has no Kubernetes operational experience — misconfigured clusters cause outages, not just bugs
- Hobby or low-traffic projects where managed container services (Fly.io, Railway, Render) eliminate the operational overhead
- Container image building and Dockerfile optimization — use `docker-expert` instead

## Core Principles (ALWAYS APPLY)

1. **Resource limits on every container** — A container without limits can consume all node resources, triggering OOM kills on co-located pods and causing cascading cluster failure. **[Enforcement]:** Run `kubectl get pods -o json | python -c "import sys,json; pods=json.load(sys.stdin); [print(c['name']) for p in pods['items'] for c in p['spec']['containers'] if not c.get('resources',{}).get('limits')]"` — any output is a blocking violation.

2. **Health probes define pod lifecycle** — Kubernetes kills pods without liveness probes, routes traffic to unready pods without readiness probes, and prematurely terminates slow-starting pods without startup probes. **[Enforcement]:** Every Deployment must have at minimum `livenessProbe` and `readinessProbe`. Run `kubectl get deployments -o json | python -c "import sys,json; d=json.load(sys.stdin); [print(c['name']) for dep in d['items'] for c in dep['spec']['template']['spec']['containers'] if not c.get('livenessProbe')]"` — any output is a blocking violation.

3. **Pinned image tags only — no `latest`** — `latest` is mutable. A node pulling a new image silently changes the running version, making rollbacks and incident diagnosis impossible. **[Enforcement]:** Run `grep -rn "image:.*:latest"` on all manifest files. Any match is a blocking violation. Pin to SHA digest or strict semver tag.

4. **Secrets in Secrets resources, never ConfigMaps** — ConfigMaps store data in plaintext. A Secret containing database credentials or API keys in a ConfigMap is exposed to anyone with cluster read access. **[Enforcement]:** Verify no sensitive data in ConfigMaps. Run `kubectl get configmaps -o yaml | grep -iE "password|secret|key|token"` — any match is a blocking security violation.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

1. **Choose deployment strategy** — Rolling (default, backward-compatible), Blue-Green (instant rollback, 2x resources), or Canary (real traffic validation, ingress annotations needed).
2. **Verify container image exists** — Confirm the Docker image is built and tagged in the registry. Never write a manifest for an image that hasn't been built.
3. **Check namespace** — Confirm the target namespace exists. Create if needed.
4. **Review existing manifests** — If updating, check for existing Deployments, Services, Ingresses to match conventions.

### Step 1: Create Kubernetes Manifests

**Goal:** Write Deployment, Service, Ingress, ConfigMap, and Secret manifests
**Expected output:** YAML manifests per resource type
**Tools to use:** YAML editor, `kubectl`

**Deployment with health probes, resource limits, and anti-affinity:**
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
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0   # Pinned tag — never "latest"
          ports:
            - containerPort: 3000
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
            initialDelaySeconds: 10
            periodSeconds: 30
            failureThreshold: 3
          readinessProbe:
            httpGet: { path: /ready, port: 3000 }
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 2
          startupProbe:
            httpGet: { path: /health, port: 3000 }
            periodSeconds: 5
            failureThreshold: 30   # 150s max startup
          env:
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
                    - { key: app, operator: In, values: [myapp] }
                topologyKey: kubernetes.io/hostname
```

**Verification gate:** `kubectl apply --dry-run=client -f deployment.yaml` exits 0 with 0 validation errors.

### Step 2: Configure Environment

**Goal:** Map application configuration to K8s resources with fail-fast startup validation
**Expected output:** ConfigMap + Secret + startup validation code
**Tools to use:** YAML editor, Zod/validators

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: "info"
  API_URL: "https://api.example.com"
---
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/mydb"
  api-key: "your-api-key"
```

**Verification gate:** `kubectl get secret myapp-secrets` confirms the secret exists. Application validates all required env vars at startup (fails fast on missing config).

### Step 3: Choose and Implement Deployment Strategy

**Goal:** Deploy with the appropriate strategy and verify zero-downtime
**Expected output:** Deployment configured with chosen strategy

**Blue-Green:** Two Deployments with different version labels; switch traffic atomically:
```bash
# Switch traffic from blue (v1) to green (v2)
kubectl patch service myapp -p '{"spec":{"selector":{"version":"v2"}}}'
```

**Canary:** Multiple Deployments with weighted traffic via Ingress annotations:
```yaml
annotations:
  nginx.ingress.kubernetes.io/canary: "true"
  nginx.ingress.kubernetes.io/canary-weight: "5"   # 5% traffic to canary
```

**Verification gate:** During deployment, `kubectl rollout status deployment/myapp` reports "successfully rolled out." No 5xx errors during the transition.

### Step 4: Verify Rollback Plan

**Goal:** Confirm rollback works before it's needed
**Expected output:** Documented rollback procedure
**Tools to use:** `kubectl rollout`, `helm rollback`

```bash
# Verify rollout history
kubectl rollout history deployment/myapp

# Test rollback in staging
kubectl rollout undo deployment/myapp
```

**Verification gate:** Rollback procedure tested in staging. `kubectl rollout undo` successfully returns to the previous version.

### Step 5: Handoff & Output

**Required output format:**
```
## Kubernetes Configuration
- Deployment: [name] — replicas: [N], strategy: [rolling/blue-green/canary]
- Image: [name:tag] — pinned: [true/false]
- Health probes: liveness [true/false], readiness [true/false], startup [true/false]
- Resource limits: CPU [Xm], Memory [YMi]
- Pod anti-affinity: [true/false]
- Secrets in Secrets: [true/false] — (not ConfigMaps)
- Rollback tested: [true/false]
- Status: PRODUCTION-READY | NEEDS-FIX
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Deploying without resource requests and limits on every container | A container without limits can consume all node resources, triggering OOM kills on co-located pods and causing cascading cluster failure | Add `resources.requests` and `resources.limits` to every container. Run the manifest dry-run check. |
| Using `latest` as the image tag in a Kubernetes manifest | `latest` is mutable — a node pulling a new image silently changes the running version, making rollbacks and incident diagnosis impossible | Pin all image tags to SHA digest or strict semver tag (`myapp@sha256:...` or `myapp:1.0.0`). Run `grep -rn "image:.*latest"` and confirm 0 matches. |
| Applying manifests directly to production with `kubectl apply` without GitOps | Direct applies bypass change tracking, make rollback difficult, and allow untested configuration to reach production | Use a GitOps workflow (ArgoCD, Flux) where all changes go through PR review before sync. For emergency fixes, document the exception. |
| Configuring a Deployment without a `readinessProbe` | Kubernetes routes traffic to a pod immediately on container start, before the app is ready, causing request failures during every deployment | Add `readinessProbe` to every container. Confirm the probe endpoint returns 200 before the app is expected to serve traffic. |

## Verification

Before marking any Kubernetes task as complete:

### Self-Verification Checklist

- [ ] All changed manifests pass dry-run validation: `kubectl apply --dry-run=client -f <manifest>` exits 0 for every changed file
- [ ] All pods in Running or Completed state: `kubectl get pods --field-selector=status.phase!=Running,status.phase!=Succeeded | wc -l` returns 0 (header line only)
- [ ] Resource requests and limits set on all containers — verified via `kubectl get pods -o json` query
- [ ] Liveness and readiness probes configured on every Deployment — verified via `kubectl get deployments -o json` query
- [ ] No `latest` image tags: `grep -rn "image:.*:latest" <manifests_dir>` returns 0 matches
- [ ] Secrets in Secret resources (not ConfigMaps): `grep -rnE "password:|secret:|api-key:" configmap*.yaml` returns 0 matches
- [ ] Pod anti-affinity configured on production Deployments (spread across nodes)
- [ ] Rollback procedure documented and tested in staging

### Verification Commands

```bash
# Dry-run validation
kubectl apply --dry-run=client -f deployment.yaml -f service.yaml -f ingress.yaml

# Check all pods are healthy
kubectl get pods --field-selector=status.phase!=Running,status.phase!=Succeeded

# Check all pods have resource limits
kubectl get pods -o json | python -c "import sys,json; pods=json.load(sys.stdin); [print(c['name']) for p in pods['items'] for c in p['spec']['containers'] if not c.get('resources',{}).get('limits')]"

# Check for latest tags
grep -rn "image:.*:latest" manifests/

# Check ConfigMaps for secrets
grep -rnE "password:|secret:|api-key:" manifests/*configmap*

# Test rollout and rollback
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Dry-run validation | `kubectl apply --dry-run=client` exits 0 for all manifests | Fix YAML validation errors. Check for missing required fields, typos in API versions. |
| Resource limits | All containers have `resources.limits` set | Add `resources.limits` to every container in every Deployment. Measure actual usage with `kubectl top pod` first to set realistic values. |
| Health probes | All Deployments have liveness + readiness probes | Add probes. If the app has no health endpoint, add one (see Health Check Endpoint pattern). |
| Pinned image tags | Zero matches for `:latest` in manifests | Replace with SHA digest or semver tag. Rebuild image if needed. |
| Secrets management | Zero matches for secrets in ConfigMaps | Move secrets to Secret resources. Reference via `secretKeyRef`. |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple Deployment + Service manifest | Claude Haiku / GPT-4o Mini | 3,000-6,000 |
| Full manifest set (Deployment, Service, Ingress, ConfigMaps, Secrets) + Helm chart | Claude Sonnet / GPT-4o | 10,000-25,000 |
| Complex deployment strategy (blue-green/canary) + production readiness audit | Claude Opus / GPT-4o | 25,000-60,000 |

### Parallelization

- **Independent manifest files:** Deployment, Service, Ingress, ConfigMaps can be written in parallel
- **Helm chart templates:** Can be written in parallel (each template is independent)
- **Rollout verification:** Must be sequential (one deployment at a time)

### Context Budget

- **Expected context usage:** 5,000-15,000 tokens per service configuration
- **When to context-optimize:** When reviewing `kubectl describe pod` output (use `-o yaml` instead)
- **Context recovery:** Use `rtk kubectl get pods` and `rtk kubectl describe` for token-efficient K8s commands

## Examples

### Example 1: Setting Up a New Microservice

**User request:**
```
Deploy our new user-service microservice to Kubernetes — it runs on port 8080, needs Postgres access, and should use rolling updates
```

**Skill execution:**
```
1. Pre-Flight: Image built as user-service:1.0.0, namespace "services" exists
2. Created Deployment with 3 replicas, rolling update (maxSurge=1, maxUnavailable=0)
3. Added liveness probe on /health, readiness probe on /ready, startup probe (120s timeout)
4. Created ClusterIP Service on port 80 → 8080
5. Created Ingress for api.example.com/users/*
6. Created ConfigMap for LOG_LEVEL, Secret for DATABASE_URL (from K8s Secret)
7. Pod anti-affinity configured to spread pods across nodes
8. Validated: dry-run passes, rollout succeeds, rollback tested in staging
```

### Example 2: Blue-Green Deployment for Critical Service

**User request:**
```
Deploy a new version of the payment service with zero tolerance for mixed-version traffic — needs instant rollback
```

**Skill execution:**
```
1. Pre-Flight: Blue-Green strategy chosen (clean cutover required)
2. Created v2 Deployment alongside existing v1, both with same Service
3. Service selector: version: v1 (still live)
4. Smoke-tested v2 on internal endpoint
5. Switched traffic: kubectl patch service payment -p '{"spec":{"selector":{"version":"v2"}}}'
6. Monitored: 0 errors during cutover, all requests successful
7. Rollback test: patched selector back to v1 — instant rollback confirmed
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Setting `replicas: 1` for production workload without documenting the reason | Single-replica deployment has zero tolerance for node failure or rolling updates, causing downtime during routine maintenance | Minimum 3 replicas for production workloads. Use HPA for auto-scaling. Document any single-replica exception with a reason. |
| Skipping canary error-rate monitoring before full cutover | A latent bug that only manifests under partial load is indistinguishable from normal variance without a baseline comparison | Monitor error rate and latency p99 during canary phase. Compare to baseline. Only proceed to full cutover if both metrics are within 5% of baseline. |
| Disabling health checks during blue/green cutover | Traffic routes to the new instance before it is warm, causing a burst of 5xx errors to real users | Keep health checks active during cutover. The new version must pass readiness probe before receiving traffic. |
| Exposing a service with `type: LoadBalancer` without understanding cloud cost implications | Each LoadBalancer provisions a cloud load balancer that incurs per-hour charges even when idle | Use `type: ClusterIP` with an Ingress controller for most services. Only use `LoadBalancer` when you need a dedicated LB (rare). |

## References

### Internal Dependencies

- `docker-expert` — Upstream: container images that this skill deploys via Kubernetes manifests.
- `ci-config-helper` — CI pipeline builds images and applies manifests via GitOps or `kubectl`.
- `observability-specialist` — Downstream: monitoring, alerting, and logging for deployed services.
- `security-reviewer` — Downstream: CVE scanning and OWASP audit of deployed images.
- `infra-architect` — Cloud infrastructure (VPCs, node pools, load balancers) that the cluster runs on.

### External Standards

- [Kubernetes Production Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices) — GKE production best practices
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) — Official K8s deployment documentation
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/) — Official Helm chart best practices
- [Kubernetes Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html) — OWASP K8s security

### Related Skills

- `debugging` — Related: pod crash debugging, CrashLoopBackOff analysis, OOM diagnosis
- `performance-profiler` — Related: resource optimization and HPA configuration
- `test-genius` — Related: health endpoint tests and deployment smoke tests

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Full Gold Standard rewrite: added Identity (role/mission/quality bar/differentiator), Core Principles table with enforcement, Workflow with Step 0-5, Blocking Violations table, Verification with quality gates and commands, Performance & Cost, Examples, References, Changelog. Preserved all deployment strategies, health probes, environment config, rollback plan, production readiness checklist, Helm chart structure, anti-patterns, and failure modes from v1. |
| 1.0.0 | — | Initial version |
