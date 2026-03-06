# Mega-Mind Skills System

> **A unified superpowers + virtual company skill set for Antigravity IDE**

This is a comprehensive skill-based workflow system that combines the disciplined development workflows of [Superpowers](https://github.com/obra/superpowers) with the domain expertise of [Virtual Company](https://github.com/k1lgor/virtual-company). It provides structured, reliable behavior for AI coding assistants across the entire software development lifecycle.

## Overview

Mega-Mind brings together **41 skills** organized into categories:

### The Mega-Mind Orchestrator (1 skill)

The master controller that routes requests and coordinates skill chains:

- `mega-mind` - Primary entry point via `/mega-mind` command

### Core Workflow Skills (13 skills)

Structured development discipline that ensures quality at every step:

- `brainstorming` - Explore approaches before committing
- `writing-plans` - Create detailed implementation plans
- `executing-plans` - Disciplined execution with tracking
- `single-flow-task-execution` - Sequential task decomposition
- `test-driven-development` - Write tests first, implement second
- `systematic-debugging` - Root cause analysis methodology
- `requesting-code-review` - Structured review requests
- `receiving-code-review` - Handle feedback systematically
- `verification-before-completion` - Prove it works before done
- `finishing-a-development-branch` - Clean branch management
- `using-git-worktrees` - Parallel development workflows
- `using-mega-mind` - Master skill routing
- `writing-skills` - Create new custom skills

### Domain Expert Skills (27 skills)

Specialized expertise for specific technical domains:

- **Architecture**: tech-lead, frontend-architect, backend-architect, infra-architect, api-designer
- **Development**: code-polisher, migration-upgrader, mobile-architect, legacy-archaeologist
- **Testing**: test-genius, e2e-test-specialist, bug-hunter
- **DevOps**: ci-config-helper, docker-expert, k8s-orchestrator, observability-specialist
- **Data**: data-engineer, data-analyst, ml-engineer, search-vector-architect
- **Security**: security-reviewer
- **Performance**: performance-profiler
- **Documentation**: doc-writer
- **UX**: ux-designer
- **Product**: product-manager, workflow-orchestrator
- **Meta**: skill-generator

---

## Quick Start

### Option 1: Full Installation (Recommended)

Run the full installation script with interactive options:

```bash
# Navigate to mega-mind-skills directory
cd mega-mind-skills

# Run installer with your project path
./install.sh /path/to/your/project

# Or run from the target project directory
cd /path/to/your/project
/path/to/mega-mind-skills/install.sh .
```

The installer provides options for:

- **[b]ackup** existing `.agent` and install fresh
- **[m]erge** with existing installation
- **[o]verwrite** completely
- **[c]ancel** installation

### Option 2: Quick Install

For a simple copy operation:

```bash
# From your project directory
/path/to/mega-mind-skills/quick-install.sh .
```

### Option 3: Manual Installation

```bash
# Copy the .agent directory to your project
cp -r mega-mind-skills/.agent /path/to/your/project/

# Make scripts executable
chmod +x /path/to/your/project/.agent/tests/run-tests.sh
```

### Verify Installation

```bash
cd /path/to/your/project
bash .agent/tests/run-tests.sh
```

---

## Using Mega-Mind

### The `/mega-mind` Command

The `/mega-mind` command is your primary entry point to the skill system. It acts as an intelligent orchestrator that:

1. **Analyzes** your request to understand intent
2. **Routes** to the appropriate skill(s)
3. **Coordinates** skill chains for complex tasks
4. **Tracks** progress throughout

### Available Commands

```
/mega-mind status             - Show current session state
/mega-mind skills             - List all available skills
/mega-mind workflows          - List available workflows
/mega-mind route <request>    - Analyze and route a request
/mega-mind execute <workflow> - Execute a named workflow
/mega-mind help               - Show help message
```

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
   1. tech-lead                        → Define architecture
   2. brainstorming                    → Explore OAuth providers
   3. api-designer                     → Design auth API
   4. writing-plans                    → Create implementation plan
   5. test-driven-development          → Write auth tests
   6. backend-architect                → Implement auth service
   7. frontend-architect               → Implement login UI
   8. security-reviewer                → Security audit
   9. verification-before-completion   → Verify

📍 Starting with: tech-lead
```

---

## File Structure

```
mega-mind-skills/
├── README.md                    # Main documentation (this file)
├── COMPLETE_REFERENCE.md        # Detailed reference
├── install.sh                   # Full installer with options
├── quick-install.sh             # Simple copy installer
│
└── .agent/
    ├── AGENTS.md                # Master contract and rules
    │
    ├── skills/
    │   ├── mega-mind/           # 🧠 Master orchestrator
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
    │
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

---

## Skill Routing Matrix

The `mega-mind` orchestrator automatically routes requests to appropriate skills:

| Request Type  | Primary Skill           | Secondary Skills                |
| ------------- | ----------------------- | ------------------------------- |
| New feature   | tech-lead               | brainstorming, writing-plans    |
| Bug fix       | systematic-debugging    | bug-hunter                      |
| Code quality  | code-polisher           | -                               |
| Performance   | performance-profiler    | -                               |
| Security      | security-reviewer       | -                               |
| Testing       | test-driven-development | test-genius                     |
| Documentation | doc-writer              | -                               |
| API design    | api-designer            | backend-architect               |
| Frontend      | frontend-architect      | ux-designer                     |
| Backend       | backend-architect       | api-designer                    |
| DevOps        | infra-architect         | docker-expert, k8s-orchestrator |
| Data          | data-engineer           | data-analyst                    |
| ML/AI         | ml-engineer             | -                               |
| Mobile        | mobile-architect        | -                               |
| Legacy code   | legacy-archaeologist    | -                               |

---

## Workflows

### Feature Development

```
brainstorming → writing-plans → test-driven-development →
executing-plans → verification-before-completion →
requesting-code-review → finishing-a-development-branch
```

### Bug Fix

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
security-reviewer → systematic-debugging → test-driven-development →
verification-before-completion
```

### New Project

```
tech-lead → brainstorming → [architects] → writing-plans →
[docker-expert, k8s-orchestrator, ci-config-helper] → development chains
```

---

## Key Concepts

### Task Tracking

All tasks are tracked in `docs/plans/task.md`:

| Task ID | Description  | Status  | Priority | Dependencies |
| ------- | ------------ | ------- | -------- | ------------ |
| 1       | Example task | pending | high     | -            |

Status values: `pending`, `in_progress`, `completed`, `blocked`

### Verification Before Completion

Never mark a task as complete without:

1. Running tests
2. Running linting
3. Building successfully
4. Manual verification
5. Checking for regressions

### Execution Model

1. Session loads `.agent/AGENTS.md` rules
2. `/mega-mind` analyzes and routes requests
3. Design work flows through brainstorming → planning → execution
4. All work tracked in task tracker
5. Nothing marked done without verification

---

## Installation Scripts

### install.sh (Full Installer)

The full installer provides:

- Interactive installation options
- Backup/merge/overwrite choices
- Automatic validation
- Quick start guide output

```bash
./install.sh [project-path]
```

### quick-install.sh (Simple Copy)

For non-interactive installation:

```bash
./quick-install.sh [project-path]
```

### run-tests.sh (Validation)

Validates your installation:

```bash
bash .agent/tests/run-tests.sh
```

Tests include:

- Core workflow skills existence
- Domain expert skills existence
- Workflows existence
- Agent profiles existence
- AGENTS.md validation
- Skill frontmatter validation

---

## Contributing

To add new skills:

1. Create a new directory in `.agent/skills/`
2. Add a `SKILL.md` file with proper frontmatter:
   ```markdown
   ---
   name: skill-name
   description: What this skill does
   triggers:
     - "/trigger"
     - "keyword"
   ---
   ```
3. Include instructions and examples
4. Run tests to verify

---

## Credits

This project combines and adapts:

- [Superpowers](https://github.com/obra/superpowers) by obra - Core workflow philosophy
- [antigravity-superpowers](https://github.com/skainguyen1412/antigravity-superpowers) by skainguyen1412 - Antigravity adaptation
- [virtual-company](https://github.com/k1lgor/virtual-company) by k1lgor - Domain expertise skills

---

## License

MIT License - Free to use and modify.
