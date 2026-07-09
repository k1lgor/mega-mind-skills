# Reference

> All skills conform to the **[Gold Standard SKILL.md v1.0](https://github.com/k1lgor/mega-mind-skills/blob/main/.agent/shared/GOLD-STANDARD-SKILL.md)** specification. Every skill includes: Blocking Violations table, Verification with quality gates, Performance & Cost model, structured Examples, Anti-Patterns tables, and full References/Changelog.

## Skills

### Core Workflow (9)

| Skill                            | Description                                            |
| -------------------------------- | ------------------------------------------------------ |
| `brainstorming`                  | Structured exploration before committing               |
| `writing-plans`                  | Detailed step-by-step implementation plans             |
| `executing-plans`                | Disciplined execution with dependency graph resolution |
| `test-driven-development`        | Red-Green-Refactor cycle                               |
| `debugging`                      | Rapid Fix + Systematic root cause analysis             |
| `requesting-code-review`         | Structured review requests with severity tags          |
| `receiving-code-review`          | Handle feedback systematically                         |
| `finishing-a-development-branch` | Clean merge, branch cleanup, release notes             |
| `using-git-worktrees`            | Parallel development on multiple branches              |

### Domain Expert (30)

**Architecture**

| Skill                | Description                                     |
| -------------------- | ----------------------------------------------- |
| `tech-lead`          | Architecture, planning, tech debt assessment    |
| `frontend-architect` | Component design, state management, performance |
| `backend-architect`  | API design, service boundaries, data flow       |
| `infra-architect`    | Infrastructure design, scalability, DR          |

**Development**

| Skill                  | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `code-polisher`        | Refactoring, dead code removal, consistency     |
| `migration-upgrader`   | Dependency upgrades, breaking change management |
| `mobile-architect`     | Platform-specific design, offline, performance  |
| `legacy-archaeologist` | Understand and safely modify legacy code        |
| `python-patterns`      | Typing, async, packaging, testing idioms        |

**Testing**

| Skill                 | Description                                  |
| --------------------- | -------------------------------------------- |
| `test-genius`         | Unit test design, edge cases, testability    |
| `e2e-test-specialist` | Playwright/Cypress, user journeys, flakiness |
| `eval-harness`        | AI feature evaluation with Pass@K metrics    |

**DevOps**

| Skill                      | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `ci-config-helper`         | Pipeline configuration, caching, matrix builds |
| `docker-expert`            | Multi-stage builds, security, compose patterns |
| `k8s-orchestrator`         | Deployments, services, ingress, autoscaling    |
| `observability-specialist` | Metrics, traces, logs, alerting, dashboards    |

**Data & AI**

| Skill                          | Description                                        |
| ------------------------------ | -------------------------------------------------- |
| `data-engineer`                | Schema design, ETL patterns, data quality          |
| `data-analyst`                 | Statistical validation, visualization, A/B testing |
| `ml-engineer`                  | MLOps pipeline, model evaluation, bias detection   |
| `search-vector-architect`      | Embedding models, hybrid search, RAG               |
| `database-migrations`          | Expand-Migrate-Contract, zero-downtime, rollback   |
| `regex-vs-llm-structured-text` | Choosing between regex and LLM for extraction      |

**Security & Performance**

| Skill                  | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `security-reviewer`    | OWASP Top 10, injection, secret detection       |
| `performance-profiler` | CPU, memory, network profiling and optimization |

**Documentation & UX**

| Skill         | Description                                      |
| ------------- | ------------------------------------------------ |
| `doc-writer`  | API docs, READMEs, architecture documentation    |
| `ux-designer` | Accessibility, responsive design, design systems |

**Product & Meta**

| Skill                   | Description                                     |
| ----------------------- | ----------------------------------------------- |
| `product-manager`       | Feature planning, stakeholder communication     |
| `workflow-orchestrator` | Step functions, retry, compensation logic       |
| `skill-generator`       | Create new SKILL.md files with proper structure |
| `multi-plan`            | Multi-model collaborative planning synthesis    |
| `multi-execute`         | Parallel prototyping + refactoring + audit      |

### Meta & Learning (12)

| Skill                        | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| `continuous-learning-v2`     | Instinct extraction and evolution from sessions |
| `search-first`               | Research-before-coding discipline               |
| `autonomous-loops`           | Multi-step AI pipeline patterns                 |
| `skill-stocktake`            | Quality audit and library maintenance           |
| `cost-aware-llm-pipeline`    | Model routing and token budget tracking         |
| `verification-loop`          | Tiered verification (Surface / Standard / Deep) |
| `iterative-retrieval`        | Progressive context refinement for subagents    |
| `content-hash-cache-pattern` | SHA-256 caching for file processing             |
| `plankton-code-quality`      | Write-time formatting and linting enforcement   |
| `autoresearch-loop`          | Karpathy-style self-improvement eval loop       |

### Token Optimization (2)

| Skill               | Description                               |
| ------------------- | ----------------------------------------- |
| `rtk`               | CLI proxy for 60-90% token savings        |
| `context-optimizer` | Context offloading and session continuity |

## Agent Personas

| Category              | Persona                 | Purpose                                             |
| --------------------- | ----------------------- | --------------------------------------------------- |
| Development           | `tech-lead`             | Architecture, planning, tech debt assessment        |
|                       | `planner`               | Z-Pattern decomposition, dependency mapping         |
|                       | `architect`             | System design, ADRs, trade-off analysis             |
| Quality & Testing     | `code-reviewer`         | Code quality, severity-tagged feedback              |
|                       | `qa-engineer`           | Test strategy, coverage gates, flakiness prevention |
|                       | `accessibility-auditor` | WCAG A/AA/AAA, screen reader, contrast, ARIA        |
|                       | `adversarial-tester`    | Chaos experiments, fuzz testing, race conditions    |
| Security & Compliance | `security-reviewer`     | OWASP Top 10, secret detection, CVE audit           |
|                       | `data-privacy-officer`  | GDPR/CCPA/SOC2, PII discovery, consent, retention   |
| Operations & Releases | `incident-commander`    | SEV1-4 classification, mitigation, postmortem       |
|                       | `release-manager`       | Semver, changelog, rollout strategy, monitoring     |

## Workflow Chains

### Feature Development

```
search-first → tech-lead → brainstorming → writing-plans →
test-driven-development → executing-plans → verification-loop →
requesting-code-review → finishing-a-development-branch →
continuous-learning-v2
```

### Bug Fix

```
debugging → test-driven-development →
verification-loop → finishing-a-development-branch →
continuous-learning-v2
```

### Incident Response

```
incident-commander → [Mitigation] → debugging →
test-driven-development → verification-loop →
finishing-a-development-branch
```

### Release

```
release-manager → verification-loop →
finishing-a-development-branch → observability-specialist →
continuous-learning-v2
```

### High-Complexity

```
search-first → architect → multi-plan → [Approval] →
multi-execute → verification-loop → security-reviewer →
finishing-a-development-branch
```

### Accessibility Audit

```
accessibility-auditor → [Fixes] → verification-loop →
requesting-code-review → finishing-a-development-branch
```

### Adversarial Test

```
adversarial-tester → [Chaos/Fuzz] → debugging →
executing-plans → verification-loop →
finishing-a-development-branch
```

## Commands

| Command                      | Skill                          | Purpose                    |
| ---------------------------- | ------------------------------ | -------------------------- |
| `/mega-mind`                 | mega-mind                      | Orchestrator entry point   |
| `/brainstorm`                | brainstorming                  | Explore approaches         |
| `/plan`                      | writing-plans                  | Create implementation plan |
| `/execute`                   | executing-plans                | Execute plan with tracking |
| `/debug`                     | debugging                      | Debug systematically       |
| `/review`                    | requesting-code-review         | Request code review        |
| `/ship`                      | finishing-a-development-branch | Deploy to production       |
| `/tdd`                       | test-driven-development        | Test-first development     |
| `/verify`                    | verification-loop              | Verify before marking done |
| `/mega-mind route <request>` | mega-mind                      | Analyze and route          |
| `/mega-mind status`          | mega-mind                      | Show session state         |
