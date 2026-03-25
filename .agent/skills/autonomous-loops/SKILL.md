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

| Anti-Pattern                      | Problem                 | Fix                              |
| --------------------------------- | ----------------------- | -------------------------------- |
| Sharing state via shell variables | Lost between iterations | Use files                        |
| No completion signal              | Infinite loops          | Add explicit completion check    |
| Single agent for everything       | Context overflow        | Split into pipeline steps        |
| No CI gates                       | Silently broken code    | Add test runs between iterations |
| Negative instructions only        | LLMs ignore "don't X"   | Add explicit de-sloppify pass    |

---

## Tips

- **Start with Sequential** — only escalate to more complex patterns if needed
- **CI as exit gate** — treat failing tests as a stop signal, not just a warning
- **Files over memory** — never rely on an agent "remembering" from iteration to iteration
- **Model routing saves money** — simple cleanup tasks should use Haiku, not Opus
- **Completion signals are critical** — define exactly what "done" looks like before the loop starts
