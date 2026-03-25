# Mega-Mind Agent Skills System

> **A unified superpowers + virtual company skill set for AI coding assistants**

This is a comprehensive skill-based workflow system that combines the disciplined development workflows of Superpowers with the domain expertise of Virtual Company.

**Compatible with:** Antigravity · Claude Code · GitHub Copilot · Cursor · OpenCode · Codex

---

## Quick Start

```
/mega-mind [command]    # Primary entry point for all operations
mmo init [--copilot] [--claude] [--opencode] [--codex]
```

Commands: `status`, `skills`, `workflows`, `route <request>`, `execute <workflow>`, `help`

## What's Included

### Mega-Mind Orchestrator (1 skill)

The master controller that routes requests and coordinates skill chains:

- `mega-mind` - Primary entry point via `/mega-mind` command

### Core Workflow Skills (13 skills)

Structured development discipline:

- `brainstorming` - Structured exploration before committing to an approach
- `writing-plans` - Detailed, step-by-step implementation plans
- `executing-plans` - Disciplined plan execution with "De-Sloppify" pass
- `single-flow-task-execution` - Ordered task decomposition with review gates
- `test-driven-development` - Write tests first, implement second
- `systematic-debugging` - Root cause tracing with supporting techniques
- `requesting-code-review` - Structured review flow with checklists
- `receiving-code-review` - Handling feedback systematically
- `verification-before-completion` - Integrated with eval-harness and coverage gates
- `finishing-a-development-branch` - Clean branch wrap-up with workflow options
- `using-git-worktrees` - Parallel branch management
- `using-mega-mind` - Internal skill routing logic
- `writing-skills` - Create new skills following system conventions

### Domain Expert Skills (35+ skills) ✨ UPDATED

Specialized expertise for complex development tasks:

- **Architecture:** `planner`, `architect`, `tech-lead`, `frontend-architect`, `backend-architect`, `infra-architect`, `api-designer`, `api-design`
- **Development:** `code-polisher`, `migration-upgrader`, `mobile-architect`, `legacy-archaeologist`, `python-patterns`
- **Testing:** `test-genius`, `e2e-test-specialist`, `bug-hunter`, `eval-harness`
- **DevOps:** `ci-config-helper`, `docker-expert`, `k8s-orchestrator`, `observability-specialist`, `deployment-patterns`
- **Data:** `data-engineer`, `data-analyst`, `ml-engineer`, `search-vector-architect`, `database-migrations`
- **Security:** `security-reviewer`
- **Performance:** `performance-profiler`
- **Documentation:** `doc-writer`
- **UX:** `ux-designer`
- **Product:** `product-manager`, `workflow-orchestrator`
- **Meta:** `skill-generator`

### Meta & Learning Skills (12 skills) ✨ NEW

Advanced patterns for efficiency and continuous improvement:

- `continuous-learning-v2` - Instinct extraction and evolution (The Learning Loop)
- `search-first` - Mandatory research and library check before coding
- `autonomous-loops` - Multi-step AI pipeline patterns without intervention
- `skill-stocktake` - Quality audit and library maintenance
- `cost-aware-llm-pipeline` - Model routing and token budget tracking
- `verification-loop` - 6-phase continuous verification pipeline
- `iterative-retrieval` - Progressive context refinement for subagents
- `strategic-compact` - Logical context window management
- `content-hash-cache-pattern` - SHA-256 caching for file processing
- `multi-plan` - Collaborative multiple-model planning
- `multi-execute` - Orchestrated multi-model execution and audit
- `plankton-code-quality` - Write-time formatting and linting enforcement

### Token Optimization & Context (2 skills)

- `rtk` - Rust Token Killer for 60-90% token reduction on CLI commands
- `context-optimizer` - Context offloading and session continuity

---

## Session Rules

### CORE BEHAVIOR RULES (MANDATORY)

**1. NO PROACTIVE COMMITS:**
You MUST NOT proactively run `git add` or `git commit` until the `finishing-a-development-branch` phase.

**2. MANDATORY TASK TRACKING:**
Update `<project-root>/docs/plans/task.md` after EVERY significant action.

**3. SEARCH FIRST:**
Always check for existing libraries or prior art using `search-first` before implementation.

**4. DE-SLOPPIFY:**
Every implementation step must include a cleanup pass to remove debug code and ensure readability.

**5. SECURITY BY DESIGN:**
Invoke `security-reviewer` proactively after implementing sensitive logic (auth, payments, APIs).

---

## Agent Personas

Invoke specialized agents via `.agent/agents/<name>.md`:

- **`planner`** - Technical task architect; uses Z-Pattern decomposition.
- **`architect`** - System design specialist; produces ADRs (Architecture Decision Records).
- **`tech-lead`** - Senior technical lead; focus on modularity and patterns.
- **`code-reviewer`** - Quality gate specialist; focus on readability and standards.
- **`security-reviewer`** - Vulnerability hunter; focus on OWASP Top 10.
- **`qa-engineer`** - Testing specialist; focus on edge cases and coverage.

---

## Workflow Chains (The Sequences)

### Standard Development Chain (The Z-Pattern)

`search-first` ➔ `tech-lead` ➔ `brainstorming` ➔ `writing-plans` ➔ `test-driven-development` ➔ `executing-plans` ➔ `verification-loop` ➔ `requesting-code-review` ➔ `finishing-a-development-branch` ➔ `continuous-learning-v2`

### High-Complexity Chain (Phase 3 Orchestration)

`search-first` ➔ `architect` ➔ `multi-plan` ➔ **[Approval]** ➔ `multi-execute` ➔ `verification-loop` ➔ `security-reviewer` ➔ `finishing-a-development-branch`

### Autonomous Loop Chain

`writing-plans` ➔ `autonomous-loops` ➔ `[Loop Execution]` ➔ `verification-loop` ➔ `continuous-learning-v2`

---

## RTK MANDATORY USAGE RULE

**You MUST use RTK-wrapped commands for all supported CLI operations if RTK is installed.**
Usage: `rtk <command>` (e.g., `rtk bun test (or npm test)`, `rtk git status`, `rtk tsc`).
Check status via `rtk gain`.

---

## File Structure

```
.agent/
├── AGENTS.md                    # Master contract
├── agents/                      # Specialized personas (.md)
├── skills/                      # 61 Atomic skills & controllers
├── workflows/                   # Pre-defined executable chains
└── instincts/                   # Learned patterns & observations
```
