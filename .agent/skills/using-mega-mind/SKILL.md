---
name: using-mega-mind
description: Internal skill routing logic used by the mega-mind orchestrator. This skill handles session bootstrap and request routing to appropriate skills.
triggers:
  - "start session"
  - "which skill"
  - "route this"
  - "help me with"
---

# Using Mega-Mind Skill

## Purpose

This is the **internal routing skill** that powers the `/mega-mind` orchestrator. It:

1. Boots up at session start
2. Analyzes incoming requests
3. Routes to the appropriate skill
4. Maintains session context

## Relationship with mega-mind

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│                                                             │
│   /mega-mind [command]                                      │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────────────────────────────────────────────────┐   │
│   │           mega-mind (Orchestrator Skill)            │   │
│   │                                                     │   │
│   │   • Command parsing                                 │   │
│   │   • User interaction                                │   │
│   │   • Status display                                  │   │
│   │   • Workflow execution                              │   │
│   └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│   ┌─────────────────────────────────────────────────────┐   │
│   │           using-mega-mind (This Skill)              │   │
│   │                                                     │   │
│   │   • Session bootstrap                               │   │
│   │   • Request analysis                                │   │
│   │   • Skill routing logic                             │   │
│   │   • State tracking                                  │   │
│   └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│                         ▼                                   │
│              ┌─────────────────────┐                        │
│              │   Target Skill(s)   │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Session Bootstrap

When a session starts:

```
1. Load AGENTS.md rules
2. Initialize task tracker (docs/plans/task.md)
3. Scan available skills
4. Ready to receive requests
```

## Skill Routing Decision Tree

```
INCOMING REQUEST
       │
       ├─── Design/Architecture? ───→ brainstorming
       │                              │
       │                              └──→ writing-plans
       │
       ├─── Bug/Error? ───→ systematic-debugging
       │                     │
       │                     └──→ bug-hunter
       │
       ├─── New Feature? ───→ tech-lead
       │                        │
       │                        ├──→ brainstorming
       │                        └──→ writing-plans
       │
       ├─── Code Quality? ───→ code-polisher
       │
       ├─── Testing? ───→ test-driven-development
       │                    │
       │                    └──→ test-genius
       │
       ├─── Security? ───→ security-reviewer
       │
       ├─── Performance? ───→ performance-profiler
       │
       ├─── Documentation? ───→ doc-writer
       │
       ├─── DevOps/Infra? ───→ infra-architect
       │                           │
       │                           ├──→ docker-expert
       │                           └──→ k8s-orchestrator
       │
       ├─── API? ───→ api-designer
       │
       ├─── Frontend? ───→ frontend-architect
       │
       ├─── Backend? ───→ backend-architect
       │
       ├─── Data? ───→ data-engineer
       │                 │
       │                 └──→ data-analyst
       │
       ├─── ML/AI? ───→ ml-engineer
       │
       ├─── Mobile? ───→ mobile-architect
       │
       ├─── Legacy Code? ───→ legacy-archaeologist
       │
       ├─── Code Review? ───→ requesting-code-review
       │
       ├─── Verification? ───→ verification-before-completion
       │
       └─── Merge/Finish? ───→ finishing-a-development-branch
```

## Routing Examples

### Example 1: New Feature Request

```
Request: "I need to add user notifications"

Analysis:
- Type: New feature
- Domain: Backend + Frontend
- Complexity: Medium

Route:
1. tech-lead (project planning)
2. brainstorming (explore approaches)
3. writing-plans (create implementation plan)
4. api-designer (design notification API)
5. backend-architect (implement backend)
6. frontend-architect (implement UI)
7. test-driven-development (write tests)
8. verification-before-completion (verify)
9. finishing-a-development-branch (merge)
```

### Example 2: Bug Fix

```
Request: "Users are getting logged out randomly"

Analysis:
- Type: Bug fix
- Domain: Authentication
- Urgency: High

Route:
1. systematic-debugging (investigate)
2. bug-hunter (find root cause)
3. test-driven-development (write regression test)
4. executing-plans (implement fix)
5. verification-before-completion (verify)
```

### Example 3: Performance Issue

```
Request: "The dashboard is slow"

Analysis:
- Type: Performance
- Domain: Frontend + Backend
- Complexity: Medium

Route:
1. performance-profiler (analyze)
2. brainstorming (solutions)
3. writing-plans (optimization plan)
4. executing-plans (implement)
5. verification-before-completion (verify improvement)
```

### Example 4: Infrastructure

```
Request: "Set up Kubernetes deployment"

Analysis:
- Type: Infrastructure
- Domain: DevOps
- Complexity: High

Route:
1. infra-architect (plan infrastructure)
2. k8s-orchestrator (create manifests)
3. ci-config-helper (set up CI/CD)
4. observability-specialist (add monitoring)
5. verification-before-completion (verify deployment)
```

## Session State Tracking (docs/plans/task.md)

```markdown
# Mega-Mind Session State

## Current Task

| Task ID | Description  | Status      | Skill         | Started    |
| ------- | ------------ | ----------- | ------------- | ---------- |
| 1       | Example task | in_progress | brainstorming | 2024-01-15 |

## Skill Chain

1. ✅ tech-lead
2. 🔄 brainstorming (current)
3. ⏳ writing-plans
4. ⏳ executing-plans
5. ⏳ verification-before-completion

## Context

- Project: [project name]
- Branch: [current branch]
- Last Action: [what was done]
```

## Skill Combination Patterns

### Full Feature Development

```
brainstorming → writing-plans → test-driven-development →
executing-plans → verification-before-completion →
requesting-code-review → finishing-a-development-branch
```

### Bug Fix Workflow

```
systematic-debugging → bug-hunter → test-driven-development →
verification-before-completion → finishing-a-development-branch
```

### Code Improvement

```
code-polisher → test-driven-development → verification-before-completion
```

### Security Audit

```
security-reviewer → systematic-debugging (if issues found) →
test-driven-development → verification-before-completion
```

## Quick Reference

| Request Type  | Primary Skill                  | Secondary Skills                |
| ------------- | ------------------------------ | ------------------------------- |
| New feature   | tech-lead                      | brainstorming, writing-plans    |
| Bug fix       | systematic-debugging           | bug-hunter                      |
| Code quality  | code-polisher                  | -                               |
| Performance   | performance-profiler           | -                               |
| Security      | security-reviewer              | -                               |
| Testing       | test-driven-development        | test-genius                     |
| Documentation | doc-writer                     | -                               |
| API design    | api-designer                   | backend-architect               |
| Frontend      | frontend-architect             | ux-designer                     |
| Backend       | backend-architect              | api-designer                    |
| DevOps        | infra-architect                | docker-expert, k8s-orchestrator |
| Data          | data-engineer                  | data-analyst                    |
| ML/AI         | ml-engineer                    | -                               |
| Mobile        | mobile-architect               | -                               |
| Legacy code   | legacy-archaeologist           | -                               |
| Code review   | requesting-code-review         | -                               |
| Verification  | verification-before-completion | -                               |
| Merge         | finishing-a-development-branch | -                               |

## Tips

- Start with `/mega-mind` for automatic routing
- Start with the primary skill for the request type
- Let each skill guide you to the next appropriate skill
- Use verification-before-completion before any merge
- Track all work in docs/plans/task.md
