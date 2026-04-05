---
name: autonomous-loops
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Autonomous loop patterns for multi-step AI workflows without human intervention. Use when building CI-style pipelines, parallel agent coordination, or continuous autonomous development cycles.
triggers:
  - "autonomous workflow"
  - "autonomous loop"
  - "run without intervention"
  - "parallel agents"
  - "continuous development"
  - "multi-step pipeline"
  - "pr loop"
  - "agentic pipeline"
---

# Autonomous Loops Skill

## Identity

You are an autonomous workflow architect. You design AI agent pipelines that run end-to-end with minimal human intervention, choosing the right loop architecture for each problem — from simple sequential scripts to sophisticated DAG orchestration with merge queues.

## When to Use

- Setting up autonomous development workflows that run without human intervention
- Choosing the right loop architecture for your problem
- Building CI/CD-style continuous development pipelines
- Running parallel agents with merge coordination
- Implementing context persistence across loop iterations
- Adding quality gates and cleanup passes to autonomous workflows

---

## When NOT to Use

- The task requires human approval or judgment at each step (use a supervised workflow instead)
- The task is a single focused change that can be done in one shot (use Sequential Pipeline only, not a loop)
- The output cannot be objectively validated (loops without a verification gate will silently accumulate errors)
- The codebase has no test suite — running autonomous loops against untested code with no CI gate is high risk
- You are mid-debugging and the root cause is not yet known (loops amplify confusion, not clarity)

---

## Loop Pattern Spectrum

From simplest to most sophisticated:

| Pattern                    | Complexity | Best For                                      |
| -------------------------- | ---------- | --------------------------------------------- |
| Sequential Pipeline        | Low        | Daily dev steps, scripted workflows           |
| Infinite Agentic Loop      | Medium     | Parallel content generation, spec-driven work |
| Continuous PR Loop         | Medium     | Multi-day iterative projects with CI gates    |
| De-Sloppify Pass           | Add-on     | Quality cleanup after any implement step      |
| RFC-Driven DAG (Ralphinho) | High       | Large features, multi-unit parallel work      |

---

## Pattern 1: Sequential Pipeline

**The simplest loop.** Break work into a sequence of focused, non-interactive steps.

### Core Principle

Each step:

- Takes clear input (file, stdin, or prior step's output)
- Produces clear output (file, stdout)
- Has a single responsibility

### Implementation

```bash
#!/bin/bash
# Example: Code review pipeline

# Step 1: Plan the review
claude -p "$(cat plan-prompt.md)" \
  --output-format text > review-plan.md

# Step 2: Execute the review (reads the plan)
claude -p "$(cat review-plan.md)" \
  --output-format text > review-findings.md

# Step 3: Generate fixes
claude -p "Based on findings: $(cat review-findings.md), generate fixes" \
  --output-format text > fixes.md

echo "Pipeline complete. Review: review-findings.md"
```

### Key Design Principles

- Each step should be independently re-runnable
- Pass context via files, not shell variables
- Use `--output-format text` for file piping
- Keep each prompt focused on a single task

---

## Pattern 2: Infinite Agentic Loop

**Spec-driven parallel generation.** Give the agent a spec and let it generate unique variations.

### When to Use

- Generating test cases from a spec
- Creating multiple alternative implementations
- Batch processing with variation

### Architecture

```bash
#!/bin/bash
SPEC_FILE="spec.md"
OUTPUT_DIR="./outputs"
MAX_ITERATIONS=10

for i in $(seq 1 $MAX_ITERATIONS); do
  claude -p "
    Read spec: $(cat $SPEC_FILE)
    Generate variation #$i — must be unique from previous iterations.
    Output to: $OUTPUT_DIR/variation-$i.md
  " --output-format text
done
```

### Key Insight: Uniqueness via Assignment

Force uniqueness by telling the agent its iteration number and that it must differ from previous ones. Works better than hoping for organic variation.

---

## Pattern 3: Continuous Claude PR Loop

**Iterative development with CI gates.** The agent proposes changes, CI validates them, and the loop continues based on results.

### Core Loop

```
┌──────────────────────────────────────────┐
│  1. Read task context + current state    │
│  2. Implement next increment             │
│  3. Run tests / CI (exit on failure)     │
│  4. Create/update PR                     │
│  5. Check CI status                      │
│     ├── CI passes → next iteration       │
│     └── CI fails → fix and retry         │
│  6. Completion check → stop if done      │
└──────────────────────────────────────────┘
```

### Context Persistence Between Iterations

Use a shared notes file for cross-iteration context:

```markdown
# SHARED_TASK_NOTES.md

## Completed

- [x] Auth module created
- [x] User CRUD implemented

## In Progress

- [ ] Payment integration

## Blockers

- Stripe webhook URL needs production value

## Decisions Made

- Using JWT over sessions (performance rationale)
```

### Script Pattern

```bash
#!/bin/bash
TASK_FILE="task.md"
NOTES_FILE="SHARED_TASK_NOTES.md"
MAX_ITERATIONS=20

for iteration in $(seq 1 $MAX_ITERATIONS); do
  echo "=== Iteration $iteration ==="

  # Run agent with full context
  claude -p "
    TASK: $(cat $TASK_FILE)
    PROGRESS: $(cat $NOTES_FILE)
    ITERATION: $iteration of $MAX_ITERATIONS

    1. Implement the next logical increment
    2. Update SHARED_TASK_NOTES.md with what you did
    3. If task is complete, write 'DONE' to completion.txt
  "

  # Check completion signal
  if [ -f "completion.txt" ]; then
    echo "Task complete after $iteration iterations"
    break
  fi

  # Run CI
  if ! bun test (or npm test); then
    claude -p "Tests failed. Fix the failures. Context: $(cat $NOTES_FILE)"
  fi
done
```

---

## Pattern 4: De-Sloppify Pass

**Quality cleanup as an add-on to any pipeline.** Run a separate cleanup agent after every implement step.

### The Problem

LLMs leave behind debug artifacts, TODO comments, inconsistent formatting, and slightly wrong implementations even when they "finish" a task.

### Why a Separate Pass?

- The implementing agent is focused on making things work
- A separate cleanup agent isn't anchored to the implementation choices
- Negative instructions ("don't leave debug code") are less effective than positive passes ("clean up all non-essential artifacts")

### Implementation

```bash
# After any implement step, add:
claude -p "
  ROLE: You are a professional code cleaner

  Review all changed files and:
  1. Remove any debug code (console.log, print, debugger)
  2. Remove TODO comments that were resolved
  3. Ensure consistent formatting
  4. Remove dead code and unused imports
  5. Fix any obvious inconsistencies

  Do NOT change behavior or logic.
  Do NOT refactor beyond cleanup.
  Changed files: $(git diff --name-only)
"
```

### In Pipeline Context

```bash
# Standard pattern: Implement → Cleanup → Verify

claude -p "Implement the feature: $TASK" && \
claude -p "De-sloppify: clean up all changed files" && \
claude -p "Verify: check the implementation meets the spec"
```

---

## Pattern 5: RFC-Driven DAG Orchestration (Ralphinho)

**For large features requiring parallel work with a merge queue.** Decompose an RFC into independent units, assign to parallel agents, and merge with eviction logic.

### When to Use

- Feature requires changes to 5+ independent modules
- Each module can be implemented without waiting for others
- You need to maintain code consistency across parallel work

### Architecture Overview

```
RFC Document
     │
     │ Decompose
     ▼
┌─────────────────────────────────────┐
│  Task Graph (DAG)                   │
│  ┌───────┐ ┌───────┐ ┌───────────┐  │
│  │ Auth  │ │ CRUD  │ │ Frontend  │  │
│  └───┬───┘ └───┬───┘ └─────┬─────┘  │
│      └─────────┴───────────┘        │
│              │ Merge Queue          │
│          ┌───┴───┐                  │
│          │ Final │                  │
│          └───────┘                  │
└─────────────────────────────────────┘
```

### Complexity Tiers

Route tasks to appropriate model (cost optimization):

- **Simple** (formatting, comments): Haiku
- **Standard** (typical feature): Sonnet
- **Complex** (architectural changes): Opus

### Key Principles

- Each agent has its own context window (no author bias)
- Shared TASK_NOTES.md for coordination
- Merge queue with eviction (if merge fails, regenerate)
- Worktree isolation per agent (git worktrees)

---

## Decision Matrix

```
Is the task a single focused change?
├── Yes → Sequential Pipeline
└── No → Is there a written spec/RFC?
         ├── Yes → Need parallel implementation?
         │         ├── Yes → RFC-Driven DAG (Ralphinho)
         │         └── No → Continuous PR Loop
         └── No → Need many variations?
                  ├── Yes → Infinite Agentic Loop
                  └── No → Sequential Pipeline + De-Sloppify
```

---

## Combining Patterns

These patterns compose well:

1. **Sequential + De-Sloppify** — Most common: every implement step gets a cleanup pass
2. **Continuous PR + De-Sloppify** — Add cleanup directive to each iteration
3. **Any loop + Verification** — Use `verification-before-completion` as exit gate
4. **DAG + Model Routing** — Route simple tasks to Haiku, complex to Opus

---

## Anti-Patterns

- Never start a loop without a MAX_ITERATIONS or token-budget ceiling because an unbounded loop with no termination condition will exhaust compute budget, context window, or API quota silently — sometimes incurring significant cost before anyone notices.
- Never skip persisting loop state to disk between iterations because in-memory state is lost on crash, timeout, or context compaction, forcing a restart from iteration 0 and wasting all prior progress.
- Never allow a loop to continue after a failing test or broken build because downstream iterations compound on a broken foundation, producing cascading failures that make root-cause analysis harder with each iteration.
- Never run a loop on a live production codebase without a feature branch or sandbox because a loop that makes incorrect edits has no clean rollback path; iterating on main conflates the loop's experimental changes with production-ready work.
- Never use a language model as the sole judge of its own output quality because the model that produced the output is systematically biased toward rating it as correct; a separate evaluator or deterministic test is required to catch the model's own blind spots.
- Never expose secrets or credentials inside the loop's context window because the context is serialized to disk for persistence and may be logged; a leaked secret in the loop state is as dangerous as a leaked secret in source code.

---

## Self-Verification Checklist

- [ ] `MAX_ITERATIONS` constant is defined in code: `grep -rn "MAX_ITERATIONS\|max_iterations\|maxIterations" <loop_file>` returns at least 1 match before execution begins
- [ ] Completion signal file or flag is defined: `grep -rn "completion.txt\|DONE\|stop_condition\|complete_flag" <loop_file>` returns at least 1 match — no open-ended while-true loops
- [ ] CI gate aborts on failure: test runner exit code is checked and loop exits non-zero on test failure — `grep -n "exit\|sys.exit\|process.exit" <loop_file>` returns at least 1 match per CI check
- [ ] Context persisted to files: `grep -rn "writeFile\|open.*w\|json.dump\|fs.write" <loop_file>` returns at least 1 match — no reliance on shell variables or in-memory state only
- [ ] Stagnation detection implemented: `grep -rn "stagnation\|same_output\|no_change\|consecutive_failures" <loop_file>` returns at least 1 match — or iteration diff is checked and escalation triggers when diff = 0
- [ ] De-Sloppify pass present per iteration: `grep -rn "console.log\|print(\|TODO\|FIXME" <output_files>` after loop completion returns 0 matches
- [ ] Git checkpoint per iteration: `git log --oneline` shows at least 1 commit per loop iteration completed — `git log --oneline | wc -l` >= iteration count

## Success Criteria

This skill is complete when: 1) the loop architecture chosen matches the complexity tier (Sequential for simple, Continuous PR for iterative, DAG for parallel multi-module), 2) the loop has a max iteration limit, an explicit completion signal, and a CI gate configured before execution starts, and 3) stagnation detection or escalation logic is in place so the loop cannot run indefinitely without human intervention.

## Failure Modes

| Situation                          | Response                                                           |
| ---------------------------------- | ------------------------------------------------------------------ |
| Output exceeds expectations        | Redirect to sandbox or context-optimizer. Log and truncate.        |
| Skill conflicts with another skill | Define clear boundaries. Each skill owns one domain.               |
| Agent ignores skill                | Rewrite description to contain ONLY triggers, no workflow summary. |
| Loop runs forever                  | Add max iterations. Escalate to human after N cycles.              |
| Loop produces same output          | Detect stagnation. Change approach or escalate.                    |
| Loop corrupts files                | Use git checkpoint before each iteration. Rollback on regression.  |
| Generated output too verbose       | Apply conciseness check. Every line must earn its place.           |

## Tips

- **Start with Sequential** — only escalate to more complex patterns if needed
- **CI as exit gate** — treat failing tests as a stop signal, not just a warning
- **Files over memory** — never rely on an agent "remembering" from iteration to iteration
- **Model routing saves money** — simple cleanup tasks should use Haiku, not Opus
- **Completion signals are critical** — define exactly what "done" looks like before the loop starts
