---
name: ci-config-helper
compatibility: Antigravity, Claude Code, GitHub Copilot
description: CI/CD (GitHub Actions, GitLab) setup. Use for configuring continuous integration and deployment.
triggers:
  - "CI/CD"
  - "github actions"
  - "gitlab ci"
  - "pipeline"
  - "deployment pipeline"
---

# CI Config Helper Skill

## Identity

You are a CI/CD specialist focused on setting up automated pipelines for building, testing, and deploying applications.

## When to Use

- Setting up CI/CD pipelines
- Configuring GitHub Actions
- Creating GitLab CI
- Automating deployments

## When NOT to Use

- Local developer tooling setup (pre-commit hooks, editor config, local Docker Compose) — those are dev environment concerns, not CI concerns
- Infrastructure provisioning (VPCs, databases, cloud resources) — use `infra-architect` instead
- Application deployment logic itself (Kubernetes manifests, Helm charts) — use `k8s-orchestrator` instead
- Debugging a failing build where the issue is in application code, not the pipeline config — fix the code first

## GitHub Actions Templates

### Basic Node.js Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"

      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### Deploy to Production

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Build and push Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

### Security Scanning

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 0 * * 0" # Weekly

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run npm audit
        run: npm audit --audit-level=high
```

## GitLab CI Templates

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+/'

deploy:
  stage: deploy
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run deploy
  only:
    - main
  environment:
    name: production
    url: https://myapp.example.com
```

## Pipeline Stage Reference

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → tests → build image → deploy staging → smoke tests → deploy prod
```

### Full Release Pipeline (GitHub Actions)

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
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
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

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            --context staging-cluster
      - name: Run smoke tests
        run: |
          sleep 15  # wait for rollout
          curl --fail https://staging.example.com/health

  deploy-prod:
    needs: deploy-staging
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

## Best Practices

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Secrets Management

```yaml
# Never hardcode secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# Use GitHub environments for production
environment: production
```

### Matrix Builds

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [18, 20]
    exclude:
      - os: macos-latest
        node: 18
```

## Tips

- Use caching to speed up builds
- Run tests in parallel
- Use matrix builds for multiple environments
- Never expose secrets in logs, because CI log output is stored in plaintext by most providers and is readable by anyone with repo access, meaning a leaked token or password can be harvested immediately and used to compromise production systems before the pipeline even finishes
- Set up proper notifications

## Anti-Patterns

- Never store secrets in CI environment variables defined in the pipeline YAML file because YAML files are committed to version control and any secret visible in the file history is permanently compromised even after rotation.
- Never run all CI jobs unconditionally on every push because running expensive jobs (e.g. end-to-end tests, Docker builds) on every commit to every branch wastes compute budget and slows feedback loops for trivial changes.
- Never pin a CI action or Docker image to a mutable tag like `latest` or `main` because a silent upstream update can change the behaviour of your pipeline without any change to your repository, making failures non-reproducible.
- Never define CI configuration without a local validation step because a syntax error in CI config is only discovered after a push, blocking the entire team's pipeline until the fix is merged.
- Never skip caching for package install steps because reinstalling all dependencies from scratch on every run multiplies pipeline duration by 5–10x and exhausts bandwidth quotas on large dependency trees.
- Never configure CI to send notifications to the entire team on every failure because alert fatigue causes engineers to ignore notifications, and a real production-blocking failure goes unnoticed in the noise.
- Never allow a flaky test to remain in CI without a tracking issue and a skip annotation because a flaky test poisons the signal of the entire suite — when it fails, engineers assume it is the known flake and ignore it, masking real failures.
- Never deploy directly to production without a staging validation step because environment-specific configuration errors (missing env vars, wrong service endpoints) only surface under production load, causing an outage instead of a contained staging failure.
- Never deploy database schema changes in the same release as application code changes because a failed app deploy cannot be rolled back independently of the schema change, leaving the database in an inconsistent state with the previous application version.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Pipeline runs but tests never fail (false green) because test runner exits 0 on syntax errors | Test framework swallows parse errors and reports 0 tests run as a passing suite | Add an explicit check that at least N tests ran: assert `test-count > 0` in the pipeline step; run a known-failing test to confirm the pipeline goes red |
| Secrets leaking via env vars printed in step output | Debug `echo` or verbose logging in a step prints the value of a secret env var to the public log | Audit all `run:` steps for `echo $SECRET` patterns; enable log masking in the CI provider; rotate any exposed secrets immediately |
| Cache invalidation misconfigured causing stale build artifacts | Cache key does not include lockfile hash, so dependency changes do not bust the cache | Set cache key to `${{ hashFiles('**/package-lock.json') }}`; add a manual cache-clear run after the fix to confirm fresh install |
| Workflow triggers on every push including draft PRs causing quota burn | `on: pull_request` without `types` filter triggers on draft open, synchronize, and reopen events | Add `types: [opened, synchronize, reopened]` and exclude draft PRs with `if: github.event.pull_request.draft == false` |
| Matrix build passes but one OS combination never ran | `exclude:` rule accidentally excludes a required combination, or matrix entry has a typo in the OS name | Print the matrix strategy in a debug step; verify all expected combinations appear in the workflow run summary |

## Self-Verification Checklist

- [ ] Pipeline YAML lints without error: `actionlint` (GitHub Actions) or `gitlab-ci-lint` exits 0
- [ ] Pipeline runs to completion on a test branch and exits with code 0 for a known-good commit
- [ ] At least one step fails when injecting a known bad input (e.g., a deliberate lint error causes the lint step to exit non-zero)
- [ ] No secrets appear in plaintext in step logs: `grep -rn "password\s*=\|api_key\s*=\|secret\s*=" .github/workflows/` returns 0 matches
- [ ] Dependency cache key includes lockfile hash: `grep -c "hashFiles" .github/workflows/*.yml` returns > 0
- [ ] Deployment jobs are gated: `grep -c "main\|production\|manual" .github/workflows/*.yml` returns > 0 for deployment jobs
- [ ] Build matrix covers all required runtime versions: `grep -c "node-version\|python-version\|java-version" .github/workflows/*.yml` returns >= 1

## Success Criteria

This task is complete when:
1. The pipeline passes on the `main` branch with zero failures, running all lint/test/build steps
2. A PR against `main` triggers CI and reports a passing status check before merge is allowed
3. Production deployments are gated behind a branch protection rule or manual approval step
