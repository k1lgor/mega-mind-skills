# Mega-Mind Skills System

> **A unified superpowers + virtual company skill set for AI coding assistants**

This is a comprehensive skill-based workflow system that combines the disciplined development workflows of [Superpowers](https://github.com/obra/superpowers) with the domain expertise of [Virtual Company](https://github.com/k1lgor/virtual-company) and [Everything-Claude-Code](https://github.com/affaan-m/everything-claude-code). It provides structured, reliable behavior for AI coding assistants across the entire software development lifecycle.

**Compatible with:** Antigravity · GitHub Copilot (VS Code) · Claude Code · OpenCode · Codex · and any AI tool that supports the [Agent Skills open standard](https://agentskills.io)

## Overview

Mega-Mind brings together **53 active skills** organized into categories:

### The Mega-Mind Orchestrator (1 skill)

The master controller that routes requests and coordinates skill chains:

- `mega-mind` - Primary entry point via `/mega-mind` command

### Core Workflow Skills (9 skills)

Structured development discipline that ensures quality at every step:

- `brainstorming` - Explore approaches before committing
- `writing-plans` - Create detailed implementation plans
- `executing-plans` - Disciplined execution with tracking, including single-flow task mode
- `test-driven-development` - Write tests first, implement second
- `requesting-code-review` - Structured review requests
- `receiving-code-review` - Handle feedback systematically
- `finishing-a-development-branch` - Clean branch management
- `using-git-worktrees` - Parallel development workflows
- `skill-generator` - Create new custom skills

### Domain Expert Skills (29 skills)

Specialized expertise for specific technical domains:

- **Architecture**: tech-lead, frontend-architect, backend-architect, infra-architect
- **Development**: code-polisher, migration-upgrader, mobile-architect, legacy-archaeologist, python-patterns
- **Testing**: test-genius, e2e-test-specialist, debugging, eval-harness
- **DevOps**: ci-config-helper, docker-expert, k8s-orchestrator, observability-specialist
- **Data**: data-engineer, data-analyst, ml-engineer, search-vector-architect, database-migrations, regex-vs-llm-structured-text
- **Security**: security-reviewer
- **Performance**: performance-profiler
- **Documentation**: doc-writer
- **UX**: ux-designer
- **Product**: product-manager, workflow-orchestrator

### Meta & Learning Skills (11 skills)

Advanced patterns for efficiency and continuous improvement:

- `continuous-learning-v2` - Instinct extraction and evolution (The Learning Loop)
- `search-first` - Mandatory research and library check before coding
- `autonomous-loops` - Multi-step AI pipeline patterns without intervention
- `skill-stocktake` - Quality audit and library maintenance
- `cost-aware-llm-pipeline` - Model routing and token budget tracking
- `verification-loop` - 6-phase continuous verification pipeline
- `iterative-retrieval` - Progressive context refinement for subagents
- `content-hash-cache-pattern` - SHA-256 caching for file processing
- `multi-plan` - Collaborative multiple-model planning
- `multi-execute` - Orchestrated multi-model execution and audit
- `plankton-code-quality` - Write-time formatting and linting enforcement

### Token Optimization & Context (2 skills)

Reduce LLM Token consumption and manage context limits:

- `rtk` - CLI proxy for 60-90% token savings on common dev commands
- `context-optimizer` - Context offloading and session continuity

---

## Quick Start

### 1. Install the CLI

```bash
# pip
pip install mmo

# pipx (recommended — isolated, globally available)
pipx install mmo

# uv
uv tool install mmo

# Or run directly without installation
uvx mmo
```

### 2. Install the hook prerequisite: `context-mode`

`mmo init` writes `hooks.json` files for supported environments. Those hooks call the `context-mode` CLI, so hook integration will not work unless `context-mode` is installed first.

**Prerequisites:** Node.js 18+

```bash
npm install -g context-mode
context-mode doctor
```

If `context-mode doctor` fails, fix that before relying on the generated hooks.

### 3. Initialize skills in your project

```bash
# From your project root
cd /path/to/your/project

# Standard install (.agent/ only)
uvx mmo init

# Install only for Claude Code (no .agent/)
uvx mmo init --claude

# Install only for GitHub Copilot (no .agent/)
uvx mmo init --copilot

# Install only for OpenCode (no .agent/)
uvx mmo init --opencode

# Install only for Codex (no .agent/)
uvx mmo init --codex

# Overwrite an existing installation
uvx mmo init --force
uvx mmo init --copilot --claude --opencode --codex --force
```

Behavior summary:

- `mmo init` → creates `.agent/`
- `mmo init --claude` → creates `CLAUDE.md` and `.claude/`, not `.agent/`
- `mmo init --copilot --claude` → creates `.github/`, `CLAUDE.md`, and `.claude/`, not `.agent/`
- Only GitHub Copilot agent personas use the `.agent.md` suffix

The `--claude` flag adds:

- `CLAUDE.md` — project rules (mirrors `AGENTS.md`)
- `.claude/skills/` — all 53 skills in the Agent Skills standard directory
- `.claude/commands/` — Mega-Mind workflow files exposed as Claude slash commands
- `.claude/hooks/hooks.json` — context-mode hook integration

The `--copilot` flag adds a `.github/` directory with:

- `copilot-instructions.md` — global instructions loaded automatically
- `skills/<name>/SKILL.md` — all 53 skills available as `/` slash commands
- `agents/<name>.agent.md` — custom agent personas for VS Code
- `hooks/hooks.json` — context-mode hook integration

The `--opencode` flag adds:

- `AGENTS.md` and `CLAUDE.md` at project root
- `.opencode/skills/` — all skills
- `.opencode/commands/` — Mega-Mind workflow files exposed as OpenCode slash commands
- `.opencode/hooks/hooks.json` — context-mode hook integration

The `--codex` flag adds:

- `AGENTS.md` at project root
- `.codex/skills/` — all skills
- `.codex/hooks/hooks.json` — context-mode hook integration

The generated `hooks.json` files call commands such as:

```json
{
  "command": "context-mode hook claude-code pretooluse"
}
```

If `context-mode` is not installed and available on your PATH, those hooks will fail.

> 📖 For full details see [USAGE.md](./USAGE.md)

### 4. Verify the installation

Once initialized:

1. Run `context-mode doctor` to verify the hook dependency is installed correctly
2. Use the `/verify` command (triggered by the `verification-loop` skill) to ensure the Mega-Mind files are correctly installed

> 📖 For full installation details see [USAGE.md](./USAGE.md)

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
| `/debug`      | debugging                      | Debug systematically               |
| `/review`     | requesting-code-review         | Request code review                |
| `/ship`       | finishing-a-development-branch | Deploy to production               |
| `/tdd`        | test-driven-development        | Test-first development             |
| `/verify`     | verification-loop              | Verify before marking done         |

### Example Usage

```
User: /mega-mind I need to add user authentication with OAuth

🧠 Mega-Mind Orchestration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Request Analyzed: New feature - User Authentication with OAuth

🔄 Routed to skill chain:
   1. tech-lead                        → Define architecture
   2. brainstorming                    → Explore OAuth providers
   3. backend-architect                → Design auth API
   4. writing-plans                    → Create implementation plan
   5. test-driven-development          → Write auth tests
   6. backend-architect                → Implement auth service
   7. frontend-architect               → Implement login UI
   8. security-reviewer                → Security audit
   9. verification-loop                → Verify

📍 Starting with: tech-lead
```

---

## File Structure

```
mega-mind-skills/
├── README.md                    # Main documentation (this file)
├── USAGE.md                     # Installation guide
├── COMPLETE_REFERENCE.md        # Detailed reference
├── quick-install.sh             # Simple copy installer (legacy)
│
└── .agent/
    ├── AGENTS.md                # Master contract and rules
    ├── hooks/
    │   └── hooks.json           # context-mode hooks registry
    ├── instincts/               # Learned patterns & observations
    ├── skills/
    │   ├── mega-mind/           # 🧠 Master orchestrator
    │   │
    │   ├── # Core Workflow Skills
    │   ├── brainstorming/
    │   ├── writing-plans/
    │   ├── executing-plans/
    │   ├── test-driven-development/
    │   ├── debugging/
    │   ├── requesting-code-review/
    │   ├── receiving-code-review/
    │   ├── verification-loop/
    │   ├── finishing-a-development-branch/
    │   ├── using-git-worktrees/
    │   │
    │   ├── # Domain Expert Skills
    │   ├── tech-lead/
    │   ├── frontend-architect/
    │   ├── backend-architect/
    │   ├── infra-architect/
    │   ├── code-polisher/
    │   ├── migration-upgrader/
    │   ├── mobile-architect/
    │   ├── legacy-archaeologist/
    │   ├── python-patterns/
    │   ├── test-genius/
    │   ├── e2e-test-specialist/
    │   ├── debugging/
    │   ├── eval-harness/
    │   ├── ci-config-helper/
    │   ├── docker-expert/
    │   ├── k8s-orchestrator/
    │   ├── observability-specialist/
    │   ├── data-engineer/
    │   ├── data-analyst/
    │   ├── ml-engineer/
    │   ├── search-vector-architect/
    │   ├── database-migrations/
    │   ├── regex-vs-llm-structured-text/
    │   ├── security-reviewer/
    │   ├── performance-profiler/
    │   ├── doc-writer/
    │   ├── ux-designer/
    │   ├── product-manager/
    │   ├── workflow-orchestrator/
    │   └── skill-generator/
    │   │
    │   ├── # Meta & Learning Skills
    │   ├── continuous-learning-v2/
    │   ├── search-first/
    │   ├── autonomous-loops/
    │   ├── skill-stocktake/
    │   ├── cost-aware-llm-pipeline/
    │   ├── verification-loop/
    │   ├── iterative-retrieval/
    │   ├── content-hash-cache-pattern/
    │   ├── multi-plan/
    │   ├── multi-execute/
    │   └── plankton-code-quality/
    │   │
    │   └── # Token Optimization & Context
    │       ├── rtk/
    │       └── context-optimizer/
    │
    ├── shared/
    │   ├── routing.md
    │   ├── templates.md
    │   └── metadata.md
    │
    ├── workflows/
    │   ├── brainstorm.md
    │   ├── debug.md
    │   ├── execute-plan.md
    │   ├── high-complexity-dev.md
    │   ├── review.md
    │   ├── ship.md
    │   └── write-plan.md
    │
    ├── agents/
    │   ├── architect.md
    │   ├── code-reviewer.md
    │   ├── planner.md
    │   ├── qa-engineer.md
    │   ├── security-reviewer.md
    │   └── tech-lead.md
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
| Bug fix       | debugging               | -                               |
| Code quality  | code-polisher           | -                               |
| Performance   | performance-profiler    | -                               |
| Security      | security-reviewer       | -                               |
| Testing       | test-driven-development | test-genius                     |
| Documentation | doc-writer              | -                               |
| API design    | backend-architect       | -                               |
| Frontend      | frontend-architect      | ux-designer                     |
| Backend       | backend-architect       | -                               |
| DevOps        | infra-architect         | docker-expert, k8s-orchestrator |
| Data          | data-engineer           | data-analyst                    |
| ML/AI         | ml-engineer             | -                               |
| Mobile        | mobile-architect        | -                               |
| Legacy code   | legacy-archaeologist    | -                               |

---

## Workflows

### Standard Development Chain (The Z-Pattern)

```
search-first → tech-lead → brainstorming → writing-plans → test-driven-development →
executing-plans → verification-loop → requesting-code-review →
finishing-a-development-branch → continuous-learning-v2
```

### High-Complexity Chain (Phase 3 Orchestration)

```
search-first → architect → multi-plan → [Approval] → multi-execute →
verification-loop → security-reviewer → finishing-a-development-branch
```

### Autonomous Loop Chain

```
writing-plans → autonomous-loops → [Loop Execution] → verification-loop →
continuous-learning-v2
```

### Bug Fix

```
debugging → test-driven-development →
verification-loop → finishing-a-development-branch → continuous-learning-v2
```

### Code Improvement

```
plankton-code-quality → code-polisher → test-driven-development → verification-loop
```

---

## Key Concepts

### Task Tracking

All tasks are tracked in `<project-root>/docs/plans/task.md`:

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

### RTK Token Optimization

When [RTK](https://github.com/rtk-ai/rtk) is installed, CLI commands are automatically optimized:

| Original     | RTK-Optimized    | Savings |
| ------------ | ---------------- | ------- |
| `git log`    | `rtk git log`    | 85%     |
| `cargo test` | `rtk cargo test` | 90%     |
| `npm test`   | `rtk npm test`   | 90%     |
| `pytest`     | `rtk pytest`     | 90%     |

Install RTK:

```bash
cargo install rtk
# or
curl -sSL https://github.com/rtk-ai/rtk/releases/latest/download/rtk-$(uname -s)-$(uname -m) -o /usr/local/bin/rtk
chmod +x /usr/local/bin/rtk
```

---

## Installation

See [USAGE.md](./USAGE.md) for the full installation guide.

### CLI Reference

```bash
# Install skills into current directory (.agent/ only when no platform flags are used)
uvx mmo init

# Also install for GitHub Copilot (VS Code)
uvx mmo init --copilot

# Also install for Claude Code
uvx mmo init --claude

# Also install for OpenCode
uvx mmo init --opencode

# Also install for Codex
uvx mmo init --codex

# Install into a specific path
uvx mmo init /path/to/project
uvx mmo init /path/to/project --copilot

# Overwrite existing installation
uvx mmo init --force
uvx mmo init --copilot --claude --opencode --codex --force

# Show CLI version
uvx mmo --version
```

### Hook prerequisite

The installer writes `hooks.json` files for `.agent/`, `.github/`, `.claude/`, `.opencode/`, and `.codex/`. Those hooks invoke `context-mode`, so install it first:

```bash
npm install -g context-mode
context-mode doctor
```

If `context-mode` is missing from your PATH, the installed hooks will not work.

### Validate Installation

Use the internal `/verify` command within your AI assistant to run the verification protocol.

Tests verify:

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
- [Everything-Claude-Code](https://github.com/affaan-m/everything-claude-code) by affaan-m - Claude Code adaptation
- [RTK](https://github.com/rtk-ai/rtk) - Token optimization CLI

---

## License

MIT License - Free to use and modify.
