# Mega-Mind Agent Skills System

> **A unified superpowers + virtual company skill set for AI coding assistants**

This is a comprehensive skill-based workflow system that combines the disciplined development workflows of Superpowers with the domain expertise of Virtual Company.

**Compatible with:** Antigravity · Claude Code · GitHub Copilot · Cursor · OpenCode

---

## Quick Start

```
/mega-mind [command]    # Primary entry point for all operations
```

Commands: `status`, `skills`, `workflows`, `route <request>`, `execute <workflow>`, `help`

## What's Included

### Mega-Mind Orchestrator (1 skill)

The master controller that routes requests and coordinates skill chains:

- `mega-mind` - Primary entry point via `/mega-mind` command

### Core Workflow Skills (9 skills)

Structured development discipline:

- `brainstorming` - Structured exploration before committing to an approach
- `writing-plans` - Detailed, step-by-step implementation plans
- `executing-plans` - Disciplined plan execution with "De-Sloppify" pass
- `test-driven-development` - Write tests first, implement second
- `requesting-code-review` - Structured review flow with checklists
- `receiving-code-review` - Handling feedback systematically
- `finishing-a-development-branch` - Clean branch wrap-up with workflow options
- `using-git-worktrees` - Parallel branch management
- `using-mega-mind` - Internal skill routing logic

### Domain Expert Skills (29 skills) ✨ UPDATED

Specialized expertise for complex development tasks:

- **Architecture:** `planner`, `architect`, `tech-lead`, `frontend-architect`, `backend-architect`, `infra-architect`
- **Development:** `code-polisher`, `migration-upgrader`, `mobile-architect`, `legacy-archaeologist`, `python-patterns`
- **Testing:** `test-genius`, `e2e-test-specialist`, `debugging`, `eval-harness`
- **DevOps:** `ci-config-helper`, `docker-expert`, `k8s-orchestrator`, `observability-specialist`
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

> **Enforcement:** If this rule is violated, immediately unstage any auto-committed files (`git reset HEAD~1 --soft`), explain what happened, and wait for explicit user confirmation before proceeding. A commit made without user direction is a contract violation and must be reversed.

**2. MANDATORY TASK TRACKING:**
Update `<project-root>/docs/plans/task.md` after EVERY significant action.

> **Enforcement:** If no task file exists at session start, create it before writing any code. If a task is marked complete without a corresponding task.md update, the session is considered "unsaved" and the next action MUST be a task.md sync. Skipping this rule means the user cannot reliably resume a session — treat it as data loss.

**3. SEARCH FIRST:**
Always check for existing libraries or prior art using `search-first` before implementation.

> **Enforcement:** If code is written for a problem that a well-known library solves (e.g., writing a custom date formatter instead of using `date-fns`), stop immediately, document the oversight in task.md, and refactor to use the existing solution. Proceeding past this violation compounds technical debt.

**4. DE-SLOPPIFY:**
Every implementation step must include a cleanup pass to remove debug code and ensure readability.

> **Enforcement:** Any `console.log`, `TODO`, `FIXME`, `print(`, or commented-out block left in a "completed" implementation is a blocking issue. Run `plankton-code-quality` before marking any step done. Sloppy code that passes review is a process failure, not a quality success.

**5. SECURITY BY DESIGN:**
Invoke `security-reviewer` proactively after implementing sensitive logic (auth, payments, APIs).

> **Enforcement:** If a PR or feature touches authentication, user input handling, secrets, or external API calls without a security review, it MUST be flagged as incomplete. Do not mark any security-sensitive task as "done" without at least executing the OWASP Top 10 checklist from `security-reviewer`. Skipping security review in sensitive code is a critical process failure.

---

### AUTORESEARCH RULES (MANDATORY)

**6. AUTORESEARCH LOOP:**
At the end of any non-trivial session (i.e., any session that involved code changes, architectural decisions, or debugging), you MUST run the continuous-learning pipeline before the session is closed.

Protocol:

1. Run `continuous-learning-v2` to extract instincts from session observations.
2. Run `eval-harness` to record any eval definitions that emerged during the session.
3. Save extracted instincts to `.agent/instincts/observations/` (JSONL format).
4. Promote confirmed instincts to `.agent/instincts/personal/` if confidence >= 0.8.

> **Enforcement:** A session that ends without this loop is an opportunity lost. If context is running out, write a brief observation file before closing. A 3-line observation is better than nothing.

**7. SELF-EVAL BEFORE DONE:**
Before marking ANY task as complete, you MUST run the self-verification checklist from the active skill. If no skill is active, use the default `verification-loop` checklist.

Minimum self-eval steps:

- [ ] Build passes (no compile errors)
- [ ] Tests pass (or test coverage added for new logic)
- [ ] No regressions in adjacent systems
- [ ] De-Sloppify pass completed
- [ ] Security review completed (if applicable)
- [ ] task.md updated to "completed"

> **Enforcement:** The word "done" or "complete" MUST NOT appear in any response unless all checklist items above are confirmed. If any item fails, the task status is "blocked" not "done".

**8. EVAL-DRIVEN DEVELOPMENT:**
For any non-trivial feature (estimated >1 hour of implementation), create an eval definition in `.agent/evals/` BEFORE writing implementation code.

Eval definition format (save to `.agent/evals/<feature-name>.eval.md`):

```markdown
# Eval: [Feature Name]

## Success Criteria

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Pass Threshold

- Unit tests: 100% of defined scenarios
- Integration: [specific metric]

## Regression Guard

- [ ] Existing tests still pass
- [ ] Performance baseline not degraded by >10%
```

> **Enforcement:** Implementation code written without a corresponding eval definition in `.agent/evals/` is considered "unverifiable work." When discovered, pause implementation, write the eval definition first, then continue. This is the "test-first" principle applied at the feature level.

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
├── skills/                      # 53 Active skills (+ 8 redirects)
│   └── debugging/               # Merged debugging skill
├── workflows/                   # Pre-defined executable chains
├── evals/                       # Eval definitions (EVAL-DRIVEN DEVELOPMENT)
└── instincts/                   # Learned patterns & observations
    ├── personal/                # Active instinct files (YAML)
    ├── observations/            # Raw session observations (JSONL)
    └── evolved/                 # Graduated instincts (promoted to skills/workflows)
```
