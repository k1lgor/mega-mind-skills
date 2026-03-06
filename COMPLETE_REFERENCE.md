# Mega-Mind Skills System - Complete Reference

## Overview

This document provides the complete file/folder structure, skills, workflows, scripts, and agents for the **Mega-Mind Skills System** - a unified skill set combining the best of:

- **antigravity-superpowers** (13 core workflow skills)
- **virtual-company** (27 domain expert skills)
- **mega-mind orchestrator** (1 master skill)

Total: **41 skills** designed for the Antigravity IDE.

---

## Complete File Structure

```
mega-mind-skills/
├── README.md                              # Main documentation
├── COMPLETE_REFERENCE.md                  # This file
├── install.sh                             # Full installer with options
├── quick-install.sh                       # Simple copy installer
│
└── .agent/
    ├── AGENTS.md                          # Master contract & rules
    │
    ├── skills/
    │   │
    │   │  # ═══════════════════════════════════════════
    │   │  # MEGA-MIND ORCHESTRATOR
    │   │  # ═══════════════════════════════════════════
    │   │
    │   ├── mega-mind/
    │   │   └── SKILL.md                   # Master orchestrator (/mega-mind)
    │   │
    │   │  # ═══════════════════════════════════════════
    │   │  # CORE WORKFLOW SKILLS (from Superpowers)
    │   │  # ═══════════════════════════════════════════
    │   │
    │   ├── brainstorming/
    │   │   └── SKILL.md                   # Structured exploration
    │   ├── writing-plans/
    │   │   └── SKILL.md                   # Implementation planning
    │   ├── executing-plans/
    │   │   └── SKILL.md                   # Plan execution
    │   ├── single-flow-task-execution/
    │   │   └── SKILL.md                   # Sequential task management
    │   ├── test-driven-development/
    │   │   └── SKILL.md                   # TDD workflow
    │   ├── systematic-debugging/
    │   │   └── SKILL.md                   # Bug diagnosis
    │   ├── requesting-code-review/
    │   │   └── SKILL.md                   # Review requests
    │   ├── receiving-code-review/
    │   │   └── SKILL.md                   # Handle feedback
    │   ├── verification-before-completion/
    │   │   └── SKILL.md                   # Pre-merge verification
    │   ├── finishing-a-development-branch/
    │   │   └── SKILL.md                   # Branch management
    │   ├── using-git-worktrees/
    │   │   └── SKILL.md                   # Parallel development
    │   ├── using-mega-mind/
    │   │   └── SKILL.md                   # Master skill router
    │   └── writing-skills/
    │       └── SKILL.md                   # Create new skills
    │
    │   │  # ═══════════════════════════════════════════
    │   │  # DOMAIN EXPERT SKILLS (from Virtual Company)
    │   │  # ═══════════════════════════════════════════
    │   │
    │   │  # Architecture & Design
    │   ├── tech-lead/
    │   │   └── SKILL.md                   # Project planning
    │   ├── frontend-architect/
    │   │   └── SKILL.md                   # UI/Components
    │   ├── backend-architect/
    │   │   └── SKILL.md                   # Server logic
    │   ├── infra-architect/
    │   │   └── SKILL.md                   # IaC/Cloud
    │   ├── api-designer/
    │   │   └── SKILL.md                   # REST/GraphQL
    │   │
    │   │  # Development
    │   ├── code-polisher/
    │   │   └── SKILL.md                   # Refactoring
    │   ├── migration-upgrader/
    │   │   └── SKILL.md                   # Version upgrades
    │   ├── mobile-architect/
    │   │   └── SKILL.md                   # iOS/Android
    │   ├── legacy-archaeologist/
    │   │   └── SKILL.md                   # Legacy code
    │   │
    │   │  # Testing & Quality
    │   ├── test-genius/
    │   │   └── SKILL.md                   # Unit tests
    │   ├── e2e-test-specialist/
    │   │   └── SKILL.md                   # Playwright/Cypress
    │   ├── bug-hunter/
    │   │   └── SKILL.md                   # Debugging
    │   │
    │   │  # DevOps & Infrastructure
    │   ├── ci-config-helper/
    │   │   └── SKILL.md                   # GitHub Actions
    │   ├── docker-expert/
    │   │   └── SKILL.md                   # Containerization
    │   ├── k8s-orchestrator/
    │   │   └── SKILL.md                   # Kubernetes
    │   ├── observability-specialist/
    │   │   └── SKILL.md                   # Monitoring
    │   │
    │   │  # Data & AI
    │   ├── data-engineer/
    │   │   └── SKILL.md                   # ETL/Pipelines
    │   ├── data-analyst/
    │   │   └── SKILL.md                   # Analytics
    │   ├── ml-engineer/
    │   │   └── SKILL.md                   # ML pipelines
    │   ├── search-vector-architect/
    │   │   └── SKILL.md                   # RAG/Vector search
    │   │
    │   │  # Security & Performance
    │   ├── security-reviewer/
    │   │   └── SKILL.md                   # Security audits
    │   ├── performance-profiler/
    │   │   └── SKILL.md                   # Optimization
    │   │
    │   │  # Product & UX
    │   ├── doc-writer/
    │   │   └── SKILL.md                   # Documentation
    │   ├── ux-designer/
    │   │   └── SKILL.md                   # UX design
    │   ├── product-manager/
    │   │   └── SKILL.md                   # User stories
    │   ├── workflow-orchestrator/
    │   │   └── SKILL.md                   # Task orchestration
    │   │
    │   │  # Meta
    │   └── skill-generator/
    │       └── SKILL.md                   # Create new skills
    │
    ├── workflows/
    │   ├── brainstorm.md                  # Brainstorming workflow
    │   ├── execute-plan.md                # Plan execution workflow
    │   ├── write-plan.md                  # Planning workflow
    │   ├── debug.md                       # Debugging workflow
    │   ├── review.md                      # Code review workflow
    │   └── ship.md                        # Deployment workflow
    │
    ├── agents/
    │   ├── code-reviewer.md               # Reviewer agent
    │   ├── tech-lead.md                   # Lead agent
    │   └── qa-engineer.md                 # QA agent
    │
    └── tests/
        └── run-tests.sh                   # Validation script
```

---

## Installation Scripts

### install.sh - Full Installer

Location: `/mega-mind-skills/install.sh`

**Usage:**

```bash
./install.sh [project-path]
```

**Features:**

- Interactive installation with options
- Detects existing `.agent` directory
- Provides backup/merge/overwrite options
- Creates `docs/plans/task.md` for tracking
- Runs validation tests automatically
- Displays quick start guide

**Options when existing installation found:**

- `[b]ackup` - Backup existing and install fresh
- `[m]erge` - Keep existing, add missing files
- `[o]verwrite` - Remove existing completely
- `[c]ancel` - Exit installation

### quick-install.sh - Simple Copy

Location: `/mega-mind-skills/quick-install.sh`

**Usage:**

```bash
./quick-install.sh [project-path]
```

**Features:**

- Non-interactive, simple copy operation
- Makes scripts executable
- Displays quick command reference

### run-tests.sh - Validation

Location: `/.agent/tests/run-tests.sh`

**Usage:**

```bash
bash .agent/tests/run-tests.sh
```

**Tests performed:**

1. Core workflow skills existence (13 skills)
2. Domain expert skills existence (27 skills)
3. Workflows existence (6 workflows)
4. Agent profiles existence (3 agents)
5. AGENTS.md validation
6. Skill frontmatter validation

---

## The Mega-Mind Orchestrator

### Location

`.agent/skills/mega-mind/SKILL.md`

### Trigger Commands

- `/mega-mind`
- `mega mind`
- `orchestrate`
- `coordinate`
- `master skill`

### Sub-Commands

```
/mega-mind status      - Show current session state
/mega-mind skills      - List all available skills
/mega-mind workflows   - List available workflows
/mega-mind route <request> - Analyze and route a request
/mega-mind execute <workflow> - Execute a named workflow
/mega-mind help        - Show help message
```

### Skill Routing Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                      REQUEST TYPE MAPPING                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ARCHITECTURE & DESIGN                                          │
│  ├── "design system"          → tech-lead                       │
│  ├── "design API"             → api-designer                    │
│  ├── "design database"        → data-engineer                   │
│  ├── "design frontend"        → frontend-architect              │
│  ├── "design backend"         → backend-architect               │
│  ├── "design infrastructure"  → infra-architect                 │
│  └── "design mobile app"      → mobile-architect                │
│                                                                  │
│  DEVELOPMENT                                                     │
│  ├── "implement feature"      → brainstorming → writing-plans   │
│  ├── "refactor code"          → code-polisher                   │
│  ├── "upgrade dependencies"   → migration-upgrader              │
│  ├── "work with legacy"       → legacy-archaeologist            │
│  └── "create skill"           → skill-generator                 │
│                                                                  │
│  TESTING & QUALITY                                               │
│  ├── "write tests"            → test-driven-development         │
│  ├── "unit tests"             → test-genius                     │
│  ├── "e2e tests"              → e2e-test-specialist             │
│  ├── "code review"            → requesting-code-review          │
│  └── "security audit"         → security-reviewer               │
│                                                                  │
│  DEBUGGING & FIXING                                              │
│  ├── "fix bug"                → systematic-debugging            │
│  ├── "debug error"            → bug-hunter                      │
│  ├── "performance issue"      → performance-profiler            │
│                                                                  │
│  DEVOPS & INFRASTRUCTURE                                        │
│  ├── "containerize"           → docker-expert                   │
│  ├── "deploy to k8s"          → k8s-orchestrator                │
│  ├── "CI/CD"                  → ci-config-helper                │
│  └── "monitoring"             → observability-specialist        │
│                                                                  │
│  DATA & AI                                                       │
│  ├── "build data pipeline"    → data-engineer                   │
│  ├── "analyze data"           → data-analyst                    │
│  ├── "train model"            → ml-engineer                     │
│  ├── "vector search"          → search-vector-architect         │
│  └── "RAG system"             → search-vector-architect         │
│                                                                  │
│  DOCUMENTATION & UX                                              │
│  ├── "write docs"             → doc-writer                      │
│  ├── "improve UX"             → ux-designer                     │
│  └── "plan feature"           → product-manager                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skills Quick Reference

### Orchestrator (1)

| Skill       | Purpose             | Trigger      |
| ----------- | ------------------- | ------------ |
| `mega-mind` | Master orchestrator | `/mega-mind` |

### Core Workflow Skills (13)

| Skill                            | Purpose                     | When to Use            |
| -------------------------------- | --------------------------- | ---------------------- |
| `brainstorming`                  | Explore approaches          | Before major decisions |
| `writing-plans`                  | Create implementation plans | After brainstorming    |
| `executing-plans`                | Execute with tracking       | When plan is ready     |
| `single-flow-task-execution`     | Sequential decomposition    | Complex tasks          |
| `test-driven-development`        | Write tests first           | New features           |
| `systematic-debugging`           | Root cause analysis         | Bug fixes              |
| `requesting-code-review`         | Submit for review           | Code complete          |
| `receiving-code-review`          | Handle feedback             | After review           |
| `verification-before-completion` | Verify before merge         | Before "done"          |
| `finishing-a-development-branch` | Clean merge                 | Ready to ship          |
| `using-git-worktrees`            | Parallel branches           | Multiple features      |
| `using-mega-mind`                | Route to skills             | Master router          |
| `writing-skills`                 | Create new skills           | Extending system       |

### Domain Expert Skills (27)

| Category             | Skills                                                                          |
| -------------------- | ------------------------------------------------------------------------------- |
| Architecture         | tech-lead, frontend-architect, backend-architect, infra-architect, api-designer |
| Development          | code-polisher, migration-upgrader, mobile-architect, legacy-archaeologist       |
| Testing              | test-genius, e2e-test-specialist, bug-hunter                                    |
| DevOps               | ci-config-helper, docker-expert, k8s-orchestrator, observability-specialist     |
| Data/AI              | data-engineer, data-analyst, ml-engineer, search-vector-architect               |
| Security/Performance | security-reviewer, performance-profiler                                         |
| Product/UX           | doc-writer, ux-designer, product-manager, workflow-orchestrator                 |
| Meta                 | skill-generator                                                                 |

---

## Workflow Chains

### Feature Development Chain

```
1. tech-lead                        → Analyze requirements
2. brainstorming                    → Explore approaches
3. writing-plans                    → Create implementation plan
4. test-driven-development          → Write tests first
5. executing-plans                  → Implement with tracking
6. verification-before-completion   → Verify it works
7. requesting-code-review           → Submit for review
8. finishing-a-development-branch   → Merge and deploy
```

### Bug Fix Chain

```
1. systematic-debugging             → Reproduce and analyze
2. bug-hunter                       → Find root cause
3. test-driven-development          → Write regression test
4. verification-before-completion   → Verify fix works
5. finishing-a-development-branch   → Ship the fix
```

### New Project Chain

```
1. tech-lead                        → Define architecture
2. [frontend-architect, backend-architect, api-designer, infra-architect] → Design
3. writing-plans                    → Create implementation plan
4. infra-architect                  → Setup infrastructure
5. [docker-expert, k8s-orchestrator, ci-config-helper] → DevOps setup
6. Execute development              → Feature chain for each component
7. observability-specialist         → Add monitoring
8. doc-writer                       → Document everything
```

### Security Audit Chain

```
1. security-reviewer                → Identify vulnerabilities
2. systematic-debugging             → Analyze each issue
3. test-driven-development          → Write security tests
4. verification-before-completion   → Verify fixes
5. finishing-a-development-branch   → Deploy patches
```

### Performance Optimization Chain

```
1. performance-profiler             → Identify bottlenecks
2. systematic-debugging             → Analyze causes
3. code-polisher                    → Optimize code
4. test-driven-development          → Verify improvements
5. verification-before-completion   → Ensure no regressions
```

---

## Session State Management

### State File: docs/plans/task.md

```markdown
# Mega-Mind Session State

## Current Task

| Task ID | Description  | Status      | Skill         | Started    |
| ------- | ------------ | ----------- | ------------- | ---------- |
| 1       | Example task | in_progress | brainstorming | 2024-01-15 |

## Skill Chain

1. ✅ tech-lead (completed)
2. 🔄 brainstorming (in_progress)
3. ⏳ writing-plans (pending)
4. ⏳ executing-plans (pending)
5. ⏳ verification-before-completion (pending)

## Context

- Project: [project name]
- Branch: [current branch]
- Last Action: [what was done]
```

---

## Command Reference

### Quick Commands

| Command             | Action                     |
| ------------------- | -------------------------- |
| `/mega-mind`        | Start orchestrator         |
| `/mega-mind status` | Show session state         |
| `/mega-mind skills` | List all skills            |
| `/brainstorm`       | Start brainstorming        |
| `/plan`             | Create implementation plan |
| `/execute`          | Execute with tracking      |
| `/debug`            | Start debugging            |
| `/review`           | Request code review        |
| `/ship`             | Deploy to production       |
| `/tdd`              | Test-driven development    |
| `/verify`           | Verify before completion   |

---

## Credits

- **Superpowers** by obra - Core workflow philosophy
- **antigravity-superpowers** by skainguyen1412 - Antigravity adaptation
- **virtual-company** by k1lgor - Domain expertise skills

---

## License

MIT License - Free to use and modify.
