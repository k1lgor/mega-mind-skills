# Mega-Mind Agent Skills System

> **A unified superpowers + virtual company skill set for Antigravity IDE**

This is a comprehensive skill-based workflow system that combines the disciplined development workflows of Superpowers with the domain expertise of Virtual Company. It provides structured, reliable behavior for AI coding assistants across the entire software development lifecycle.

## Quick Start

```
/mega-mind [command]    # Primary entry point for all operations
```

Commands: `status`, `skills`, `workflows`, `route <request>`, `execute <workflow>`, `help`

## What's Included

### Mega-Mind Orchestrator (1 skill)

The master controller that routes requests and coordinates skill chains:

- `mega-mind` - Primary entry point via `/mega-mind` command

### Core Workflow Skills (13 skills)

Structured development discipline from Superpowers:

- `brainstorming` - Structured exploration before committing to an approach
- `writing-plans` - Detailed, step-by-step implementation plans
- `executing-plans` - Disciplined plan execution with progress tracking
- `single-flow-task-execution` - Ordered task decomposition with review gates
- `test-driven-development` - Write tests first, implement second
- `systematic-debugging` - Root cause tracing with supporting techniques
- `requesting-code-review` - Structured review flow with checklists
- `receiving-code-review` - Handling feedback systematically
- `verification-before-completion` - Prove it works before claiming it's done
- `finishing-a-development-branch` - Clean branch wrap-up with workflow options
- `using-git-worktrees` - Parallel branch management
- `using-mega-mind` - Internal skill routing logic
- `writing-skills` - Create new skills that follow the system's conventions

### Domain Expert Skills (27 skills)

Specialized expertise from Virtual Company:

- Architecture: `tech-lead`, `frontend-architect`, `backend-architect`, `infra-architect`, `api-designer`
- Development: `code-polisher`, `migration-upgrader`, `mobile-architect`, `legacy-archaeologist`
- Testing: `test-genius`, `e2e-test-specialist`, `bug-hunter`
- DevOps: `ci-config-helper`, `docker-expert`, `k8s-orchestrator`, `observability-specialist`
- Data: `data-engineer`, `data-analyst`, `ml-engineer`, `search-vector-architect`
- Security: `security-reviewer`
- Performance: `performance-profiler`
- Documentation: `doc-writer`
- UX: `ux-designer`
- Product: `product-manager`, `workflow-orchestrator`
- Meta: `skill-generator`

## Session Rules

### Tool Translation Contract

When using this system, translate platform-specific references:

| Original                 | Antigravity                      |
| ------------------------ | -------------------------------- |
| `Claude` / `Claude Code` | `Antigravity`                    |
| `Skill` tool             | `view_file`                      |
| `TodoWrite`              | Update `docs/plans/task.md`      |
| `mega-mind:<skill>`      | `.agent/skills/<skill>/SKILL.md` |
| `CLAUDE.md`              | `.agent/AGENTS.md`               |

### Execution Model

1. **Session starts** — loads `.agent/AGENTS.md` rules
2. **User invokes** `/mega-mind` or a specific skill command
3. **Request gets routed** to the most relevant skill(s)
4. **Design work** flows through brainstorming → planning → execution
5. **Every task** is tracked in `docs/plans/task.md` (created at runtime)
6. **Nothing is marked done** without running verification commands first

### Workflow Flowchart

```
Session Start → Load AGENTS.md
                       ↓
                   User Request
                       ↓
┌───────────────────────────────────────────────────────┐
│                    /mega-mind                         │
│         (Master Orchestrator Entry Point)             │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │  ANALYZE → ROUTE → EXECUTE → VERIFY → REPORT    │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
                       ↓
                Route to skill(s)
                       ↓
┌───────────── Design change? ───────────────┐
│ yes                                        │ no
↓                                            ↓
brainstorming                         Direct execution
↓                                            │
writing-plans                                │
↓                                            │
executing-plans                              │
↓                                            │
verification-before-completion  ←────────────┘
↓
finishing-a-development-branch
```

## The `/mega-mind` Command

### Purpose

The `/mega-mind` command is the **primary entry point** for interacting with the skill system. It acts as an intelligent orchestrator that:

1. **Analyzes** your request to understand intent
2. **Routes** to the appropriate skill(s)
3. **Coordinates** skill chains for complex tasks
4. **Tracks** progress throughout the session

### Sub-Commands

| Command                         | Description                             |
| ------------------------------- | --------------------------------------- |
| `/mega-mind status`             | Show current session state and progress |
| `/mega-mind skills`             | List all available skills               |
| `/mega-mind workflows`          | List available workflows                |
| `/mega-mind route <request>`    | Analyze and route a request             |
| `/mega-mind execute <workflow>` | Execute a named workflow                |
| `/mega-mind help`               | Show help message                       |

### Direct Skill Commands

| Command       | Skill                          | Purpose                            |
| ------------- | ------------------------------ | ---------------------------------- |
| `/brainstorm` | brainstorming                  | Explore approaches before deciding |
| `/plan`       | writing-plans                  | Create implementation plan         |
| `/execute`    | executing-plans                | Execute plan with tracking         |
| `/debug`      | systematic-debugging           | Debug systematically               |
| `/review`     | requesting-code-review         | Request code review                |
| `/ship`       | finishing-a-development-branch | Deploy to production               |
| `/tdd`        | test-driven-development        | Test-first development             |
| `/verify`     | verification-before-completion | Verify before marking done         |

### Example Usage

```
User: /mega-mind I need to add user authentication with OAuth

🧠 Mega-Mind Orchestration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request Analyzed: New feature - User Authentication with OAuth

🔄 Routed to skill chain:
   1. tech-lead                         → Define architecture
   2. brainstorming                     → Explore OAuth providers
   3. api-designer                      → Design auth API
   4. writing-plans                     → Create implementation plan
   5. test-driven-development           → Write auth tests
   6. backend-architect                 → Implement auth service
   7. frontend-architect                → Implement login UI
   8. security-reviewer                 → Security audit
   9. verification-before-completion    → Verify

📍 Starting with: tech-lead
```

## Skill Routing Rules

When a request comes in, `/mega-mind` routes to the appropriate skill:

```
┌─────────────────────────────────────────────────────────────────┐
│                      REQUEST TYPE MAPPING                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ARCHITECTURE & DESIGN                                          │
│  ├── "design system"          → tech-lead                       │
│  ├── "design API"             → api-designer                    │
│  ├── "design database"        → data-engineer                   │
│  ├── "design frontend"        → frontend-architect              │
│  ├── "design backend"         → backend-architect               │
│  ├── "design infrastructure"  → infra-architect                 │
│  └── "design mobile app"      → mobile-architect                │
│                                                                 │
│  DEVELOPMENT                                                    │
│  ├── "implement feature"      → brainstorming → writing-plans   │
│  ├── "refactor code"          → code-polisher                   │
│  ├── "upgrade dependencies"   → migration-upgrader              │
│  ├── "work with legacy"       → legacy-archaeologist            │
│  └── "create skill"           → skill-generator                 │
│                                                                 │
│  TESTING & QUALITY                                              │
│  ├── "write tests"            → test-driven-development         │
│  ├── "unit tests"             → test-genius                     │
│  ├── "e2e tests"              → e2e-test-specialist             │
│  ├── "code review"            → requesting-code-review          │
│  └── "security audit"         → security-reviewer               │
│                                                                 │
│  DEBUGGING & FIXING                                             │
│  ├── "fix bug"                → systematic-debugging            │
│  ├── "debug error"            → bug-hunter                      │
│  └── "performance issue"      → performance-profiler            │
│                                                                 │
│  DEVOPS & INFRASTRUCTURE                                        │
│  ├── "containerize"           → docker-expert                   │
│  ├── "deploy to k8s"          → k8s-orchestrator                │
│  ├── "CI/CD"                  → ci-config-helper                │
│  └── "monitoring"             → observability-specialist        │
│                                                                 │
│  DATA & AI                                                      │
│  ├── "build data pipeline"    → data-engineer                   │
│  ├── "analyze data"           → data-analyst                    │
│  ├── "train model"            → ml-engineer                     │
│  ├── "vector search"          → search-vector-architect         │
│  └── "RAG system"             → search-vector-architect         │
│                                                                 │
│  DOCUMENTATION & UX                                             │
│  ├── "write docs"             → doc-writer                      │
│  ├── "improve UX"             → ux-designer                     │
│  └── "plan feature"           → product-manager                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Traditional Routing (Pre-defined Chains)

1. **Design/Architecture decisions** → `brainstorming` → `writing-plans`
2. **Bug fixes** → `systematic-debugging` → `bug-hunter`
3. **New features** → `tech-lead` → `writing-plans` → `single-flow-task-execution`
4. **Code quality** → `code-polisher` → `verification-before-completion`
5. **Testing** → `test-driven-development` → `test-genius`
6. **Security audits** → `security-reviewer` → `verification-before-completion`
7. **Performance issues** → `performance-profiler` → `systematic-debugging`
8. **Documentation** → `doc-writer`
9. **DevOps/Infrastructure** → `infra-architect` → `docker-expert` / `k8s-orchestrator`
10. **API work** → `api-designer` → `backend-architect`
11. **Frontend work** → `frontend-architect` → `ux-designer`
12. **Data work** → `data-engineer` → `data-analyst`
13. **ML/AI work** → `ml-engineer`
14. **Code review** → `requesting-code-review` → `receiving-code-review`

## Task Tracking

All tasks are tracked in a live table at `<project-root>/docs/plans/task.md`:

| Task ID | Description  | Status  | Priority | Dependencies |
| ------- | ------------ | ------- | -------- | ------------ |
| 1       | Example task | pending | high     | -            |

Status values: `pending`, `in_progress`, `completed`, `blocked`

## Verification Before Completion

Never mark a task as complete without verification:

1. **Run tests**: `npm test`, `pytest`, etc.
2. **Lint code**: `npm run lint`, `ruff check`, etc.
3. **Build check**: `npm run build`, `cargo build`, etc.
4. **Manual verification**: Check the actual functionality works
5. **Document changes**: Update relevant docs

## Best Practices

### When to Use Which Skill

- **Starting fresh?** → Use `/mega-mind` for automatic routing
- **Need to explore?** → Use `brainstorming` to explore approaches
- **Have a plan?** → Use `executing-plans` for disciplined execution
- **Fixing a bug?** → Use `systematic-debugging` for root cause analysis
- **Writing tests?** → Use `test-driven-development` for test-first approach
- **Need expertise?** → Route to the appropriate domain expert skill
- **Completing work?** → Use `verification-before-completion` then `finishing-a-development-branch`

### Anti-Patterns to Avoid

- ❌ Skipping brainstorming for complex features
- ❌ Writing implementation before tests (when TDD is appropriate)
- ❌ Marking tasks complete without verification
- ❌ Ignoring code review feedback
- ❌ Not documenting architectural decisions
- ❌ Bypassing `/mega-mind` for complex multi-skill tasks

## File Structure

```
.agent/
├── AGENTS.md                    # This file - master contract
│
├── skills/
│   ├── mega-mind/               # 🧠 Master orchestrator
│   │
│   ├── # Core Workflow Skills
│   ├── brainstorming/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── single-flow-task-execution/
│   ├── test-driven-development/
│   ├── systematic-debugging/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── verification-before-completion/
│   ├── finishing-a-development-branch/
│   ├── using-git-worktrees/
│   ├── using-mega-mind/
│   └── writing-skills/
│   │
│   ├── # Domain Expert Skills
│   ├── tech-lead/
│   ├── frontend-architect/
│   ├── backend-architect/
│   ├── infra-architect/
│   ├── api-designer/
│   ├── code-polisher/
│   ├── migration-upgrader/
│   ├── mobile-architect/
│   ├── legacy-archaeologist/
│   ├── test-genius/
│   ├── e2e-test-specialist/
│   ├── bug-hunter/
│   ├── ci-config-helper/
│   ├── docker-expert/
│   ├── k8s-orchestrator/
│   ├── observability-specialist/
│   ├── data-engineer/
│   ├── data-analyst/
│   ├── ml-engineer/
│   ├── search-vector-architect/
│   ├── security-reviewer/
│   ├── performance-profiler/
│   ├── doc-writer/
│   ├── ux-designer/
│   ├── product-manager/
│   ├── workflow-orchestrator/
│   └── skill-generator/
│
├── workflows/
│   ├── brainstorm.md
│   ├── execute-plan.md
│   ├── write-plan.md
│   ├── debug.md
│   ├── review.md
│   └── ship.md
│
├── agents/
│   ├── code-reviewer.md
│   ├── tech-lead.md
│   └── qa-engineer.md
│
└── tests/
    └── run-tests.sh
```

## Workflow Chains

### Feature Development Chain

```
/mega-mind route → tech-lead → brainstorming → writing-plans →
test-driven-development → executing-plans → verification-before-completion →
requesting-code-review → finishing-a-development-branch
```

### Bug Fix Chain

```
/mega-mind route → systematic-debugging → bug-hunter →
test-driven-development → verification-before-completion →
finishing-a-development-branch
```

### New Project Chain

```
/mega-mind route → tech-lead → [architects] → writing-plans →
[docker-expert, k8s-orchestrator, ci-config-helper] → development chains
```
