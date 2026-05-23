---
name: executing-plans
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Disciplined plan execution with dependency graph resolution, review gates, progress tracking, and quality cleanup. Use when you have a plan to implement and need to track progress systematically, including complex sequential tasks with ordered dependencies.
triggers:
  - "execute the plan"
  - "implement the plan"
  - "follow the plan"
  - "start implementation"
  - "begin the work"
  - "execute step by step"
  - "execute this task"
  - "implement step by step"
  - "sequential execution"
  - "ordered tasks"
  - "task decomposition"
  - "review gate"
  - "resuming interrupted task"
  - "task blocked by"
---

# Executing Plans Skill

## Identity

You are a disciplined execution specialist who transforms plans and complex goals into ordered, verifiable steps. You do not begin execution until you have verified dependencies, because executing steps out of order creates rework. You maintain explicit execution state so that if a session is interrupted, work can be resumed without re-analysis. You treat review gates as mandatory checkpoints, not optional pauses. When a step reveals the overall plan is wrong, you escalate immediately rather than continue on a flawed path. Every step ends with a verification pass, and the task is not declared complete until the full success checklist is satisfied.

## When to Use

- After a plan has been written and approved
- When implementing a multi-step feature
- When you need to track progress through a plan
- Complex tasks requiring ordered implementation where later steps depend on earlier ones
- When review gates are required between phases (security-sensitive code, breaking API changes, DB schema changes)
- When a session might be interrupted and you need to preserve progress for later resumption

## When NOT to Use

- Without a written, approved plan — do not begin execution if the plan is still being drafted or has unresolved design questions
- When there are unresolved blockers listed in the plan — execution will stall; resolve blockers first
- For a single-step task that can be completed in one shot — the tracking overhead is not justified
- Mid-debugging when the root cause is unknown — finish debugging first, update the plan, then execute
- Tasks that can be fully parallelized — use `multi-execute` for concurrent independent workstreams
- Exploratory research tasks with no fixed output — use `brainstorming` instead

## Core Principles

1. **Dependency graph before execution**: Identify which steps block which before starting any.
2. **One task in-progress at a time**: Concurrent in-progress tasks create context bleed. Complete or explicitly pause before starting the next.
3. **State is explicit, not implicit**: The task queue document is the canonical source of truth.
4. **Verification before progression**: Each step is not complete until it passes its local verification step.
5. **Review gates are blocking**: When a gate is reached, stop and wait. Do not skip gates to maintain momentum.
6. **Escalate when the plan is wrong**: If a step reveals a fundamental flaw, stop and escalate to re-planning.
7. **De-Sloppify every step**: After implementing each step, run a cleanup pass before marking complete.

## Instructions

### Step 1: Load and Review the Plan

Before starting execution:

1. **Read the full plan** end-to-end
2. **Verify dependencies** are available
3. **Check for any blockers** before starting
4. **Confirm the current state** matches the plan's assumptions

### Step 2: Execute Step by Step

For each step in the plan:

1. **Mark step as in-progress** in task tracker
2. **Implement the step** following the plan's guidance
3. **🧹 Run De-Sloppify pass** — see `.agent/shared/DE-SLOPPIFY.md`
4. **Test locally** before moving on
5. **Back up task tracker** before modifying: run `scripts/backup-task-state.sh backup` to create a timestamped snapshot in `docs/plans/backups/`. This prevents the single-point-of-failure from losing session state on interruption.
6. **Update task tracker** when complete (DO NOT run `git add` or `git commit` here. Committing is reserved for the end of the workflow).
7. **Run verification** for the phase (if at a checkpoint) — see `.agent/shared/VERIFICATION-GATE.md`

### Step 3: Handle Deviations

When the plan doesn't match reality:

1. **Document the deviation** - what's different and why
2. **Assess impact** - does this affect other steps?
3. **Update the plan** if necessary
4. **Communicate** significant changes to stakeholders

### Step 4: Track Progress

Update `<project-root>/docs/plans/task.md` after each step, ensuring you preserve the **Mega-Mind Session State** structure:

```markdown
# Mega-Mind Session State

## Current Task

| Task ID | Description       | Status      | Skill           | Started    |
| ------- | ----------------- | ----------- | --------------- | ---------- |
| 1.1     | Create User model | completed   | executing-plans | 2024-01-15 |
| 1.2     | Password hashing  | in_progress | executing-plans | 2024-01-15 |

## Skill Chain

1. ✅ tech-lead
2. ✅ brainstorming
3. ✅ writing-plans
4. 🔄 executing-plans (current)
5. ⏳ verification-loop

## Context

- Project: [project name]
- Branch: [current branch]
- Last Action: [what was done]
```

## Execution Protocol

```
FOR EACH PHASE:
  FOR EACH STEP:
    1. Mark in_progress
    2. Implement
    3. De-Sloppify (cleanup pass)
    4. Test locally
    5. Mark completed
    6. Update <project-root>/docs/plans/task.md

  RUN PHASE VERIFICATION:
    - Run tests
    - Check integration
    - Verify behavior vs. acceptance criteria

  IF VERIFICATION FAILS:
    - Debug issue (use debugging skill if needed)
    - Fix implementation
    - Re-run de-sloppify
    - Re-run verification
    - DO NOT proceed to next phase

PROCEED TO NEXT PHASE
```

## Cost-Aware Model Usage

For long execution runs, select models based on step complexity:

| Step Type                       | Model  | Rationale                            |
| ------------------------------- | ------ | ------------------------------------ |
| Simple formatting/cleanup       | Haiku  | 3-4x cheaper for deterministic tasks |
| Standard feature implementation | Sonnet | Good balance of quality/cost         |
| Complex architectural decisions | Opus   | Deep reasoning only when needed      |

Refer to `cost-aware-llm-pipeline` skill for full model routing guidance.

## Token Optimization (RTK)

During plan execution, always prefer **RTK-wrapped commands** to save 60-90% of tokens:

- Use `rtk ls` instead of `ls`
- Use `rtk git status` instead of `git status`
- Use `rtk bun test (or npm test)` instead of `bun test (or npm test)`

Run `rtk gain` periodically to check your cumulative token savings.

## Example Session

```
> Executing Phase 1: Core Auth

Step 1.1: Create User model
[Implementing...]
[Testing...] ✓ User model compiles
[Marking complete] ✓

Step 1.2: Password hashing
[Implementing...]
[Testing...] ✓ Hash and verify work
[Marking complete] ✓

Phase 1 Verification:
- [✓] All steps complete
- [✓] Tests pass
- [✓] Can register a user

Phase 1 Complete! Moving to Phase 2...
```

---

## Advanced: Single-Flow Execution Mode

Use this mode for complex tasks that require a dependency graph, review gates, context preservation across sessions, and interruption recovery.

### Execution Contract

Every single-flow session must establish an explicit contract before starting:

```markdown
# Execution Contract: [Task Name]

Date: [YYYY-MM-DD]
Session ID: [if resuming, include prior session reference]

## Goal

[One sentence: what is the concrete deliverable when this is done?]

## Success Criteria

[Measurable: "task is complete when X, Y, Z are all true"]

1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

## Scope Boundaries

IN SCOPE:

- [explicit list]

OUT OF SCOPE (do not touch):

- [explicit list — prevents scope creep mid-execution]

## Escalation Threshold

If any subtask [describe condition], STOP and re-plan before continuing.
Example: "If the API response schema differs from the documented spec, stop."
```

### Dependency Graph Decomposition

Break the task into ordered subtasks and identify the dependency graph:

```markdown
## Task: Build User Dashboard

### Subtasks (Ordered)

| ID  | Subtask                        | Depends On | Review Gate?     |
| --- | ------------------------------ | ---------- | ---------------- |
| 1   | Set up database schema         | -          | No               |
| 2   | Create API endpoints           | 1          | Yes (API design) |
| 3   | Add request validation         | 2          | No               |
| 4   | Build frontend components      | 2          | No               |
| 5   | Write unit + integration tests | 3, 4       | Yes (coverage)   |
| 6   | Document API (OpenAPI spec)    | 2, 3       | No               |
| 7   | Final smoke test               | 5, 6       | No               |

### Dependency Graph (visual)

1 → 2 → 3 → 5 → 7
↘ 4 ↗
6 ↗
```

**Rules:**

- A subtask with no dependencies can start immediately
- A subtask with dependencies cannot start until ALL its dependencies are marked `completed`
- Review gates block progression until explicitly cleared

### Review Gates

A review gate is a hard stop where human judgment is required before proceeding.

Place review gates:

- After any API design decision (contract changes are expensive to reverse)
- After any database schema change (migrations are expensive to undo)
- After security-sensitive code (auth, crypto, payments)
- After any change that affects external integrations
- After test coverage phase (verify threshold is met before declaring done)

```markdown
## Review Gates

### Gate A: API Design Review (after Subtask 2)

Review: Do the endpoint contracts match the original spec?
Decision: Approve to continue | Reject to revise Task 2

### Gate B: Test Coverage Review (after Subtask 5)

Review: Is coverage >= 80% on all new code paths?
Decision: Approve if yes | Reject if below threshold (add more tests)
```

### Task Queue Format

```markdown
# Task Queue: [Task Name]

Last Updated: [YYYY-MM-DD HH:MM]
Session: [session reference for resumability]

## Status: in_progress | completed | blocked

## Tasks

| ID  | Subtask                   | Status      | Skill             | Started    | Completed  | Notes           |
| --- | ------------------------- | ----------- | ----------------- | ---------- | ---------- | --------------- |
| 1   | Set up database schema    | completed   | python-patterns   | 2025-04-03 | 2025-04-03 | Used Alembic    |
| 2   | Create API endpoints      | in_progress | backend-architect | 2025-04-03 | -          |                 |
| 3   | Add request validation    | pending     | -                 | -          | -          | Blocked by 2    |
| 4   | Build frontend components | pending     | -                 | -          | -          | Blocked by 2    |
| 5   | Write tests               | pending     | -                 | -          | -          | Blocked by 3, 4 |
| 6   | Document API              | pending     | -                 | -          | -          | Blocked by 2, 3 |
| 7   | Final smoke test          | pending     | -                 | -          | -          | Blocked by 5, 6 |

## Review Gates

- [ ] Gate A: API Design Review (blocks 3, 4, 6) — after Task 2
- [ ] Gate B: Coverage Review (blocks 7) — after Task 5
```

### Context Preservation Between Steps

After completing each subtask, record the execution context. This enables resumption if the session ends:

```markdown
## Execution Context Snapshot

After: Task 2 (Create API endpoints)
Time: 2025-04-03 14:32

### Decisions Made

- Used FastAPI with async endpoints (not Flask — see ADR-001)
- Auth uses Bearer token in Authorization header (not cookie)
- Pagination: cursor-based (not offset) — decision locked

### Files Modified

- src/api/routes/users.py (created)
- src/api/routes/posts.py (created)
- src/api/dependencies.py (modified — added auth dependency)

### State to Carry Forward

- The User model was extended with `last_active_at` (affects Task 4 frontend)
- API base URL is `/api/v2/` (not `/v1/` as originally planned — check docs)

### Current Test Status

- 12 new tests added; all passing
- Coverage: 67% (target 80% — Tasks 3 and 5 will close this gap)

### Next Unblocked Tasks

- Task 3: Add request validation (ready to start)
- Gate A review: pending (present to user before starting Task 3)
```

### Interruption Recovery Protocol

If a session is interrupted before all tasks are complete:

```
RECOVERY PROTOCOL:
1. Read the task queue document (canonical state)
2. Read the last Execution Context Snapshot (decisions and state)
3. Identify the task that was in_progress — it may be partially done
4. Do NOT assume the in_progress task is complete
5. Resume from the beginning of the in_progress task, or
   from the last checkpoint if subtask checkpoints were recorded
6. Do not re-analyze the full codebase — trust the context snapshot
7. Verify the in_progress task before marking complete and advancing
```

### Escalation Protocol

Escalate immediately when a subtask reveals the overall plan is wrong.

**Escalation triggers:**

- A dependency does not exist and cannot be created within the current task
- A subtask reveals a requirement contradiction that makes two other tasks mutually exclusive
- A completed task must be fundamentally redesigned (not just patched) to unblock a later task
- An external API or system behaves differently from the documented contract
- The scope of a single subtask exceeds 50% of the estimated full task effort

**Escalation procedure:**

```markdown
## ESCALATION NOTICE

Triggered by: Task 4 (Build frontend components)
Reason: The API response shape from Task 2 is incompatible with the component library's
required data format. This is a design mismatch, not an implementation bug.

Options:
A) Revise Task 2 API to match component library expectations (affects Tasks 3, 6)
B) Add a transformation layer between API and components (adds new Task 4.5)
C) Replace component library with one compatible with the current API shape

Recommendation: Option B (least rework, isolated change)

Required decision before continuing: [USER INPUT]
```

Do not continue executing after a valid escalation trigger. Stop, document, and wait.

---

## Tips

- Never skip verification steps — unverified steps create cascading failures
- If you get blocked, document why and move to what you can do
- Keep the plan visible - refer back to it frequently
- If a step is taking much longer than estimated, reassess the approach

## Failure Modes

| Failure                                                                  | Cause                                                                                                                            | Recovery                                                                                                                                         |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Step marked complete before output verified                              | Agent marks todo done on tool call success, not on output validation                                                             | Add an explicit "verify output" substep after every action step; only mark complete after verification passes                                    |
| Plan executed out of order because dependencies not identified           | Step list treated as unordered; agent picks next available step without checking prerequisites                                   | Map dependencies between steps before execution starts; execute in topological order                                                             |
| Step fails silently because error output not captured                    | Tool returns non-zero exit but agent checks stdout only; stderr discarded                                                        | Capture both stdout and stderr; treat any non-zero exit code as a step failure regardless of stdout content                                      |
| Rollback path not defined, leaving system in partial state after failure | Plan written without failure scenarios; no undo steps specified                                                                  | Define rollback actions for every destructive step before execution begins; test rollback path in a dry run                                      |
| Plan step scope creep: agent adds unrequested changes during execution   | Agent identifies "improvements" while executing a step and implements them inline                                                | Execute the plan exactly as written; log improvements as separate todos for a follow-up task; never expand scope mid-execution                   |
| Session interrupted mid-task                                             | Work state lost without context snapshot                                                                                         | Read task queue + last context snapshot. Resume from start of the in_progress task. Verify before advancing.                                     |
| Review gate rejected                                                     | Gate rejected without re-work path                                                                                               | Re-open the affected subtask(s) (set back to pending). Clear the gate checkbox. Implement the feedback. Re-run verification. Re-present to gate. |
| Subtask verification fails after multiple attempts                       | Fix requires changing a prior completed task                                                                                     | Escalate. Do not hack around the root cause.                                                                                                     |
| Dependency graph contains a cycle                                        | Two tasks cannot both depend on each other                                                                                       | Decompose one into smaller units to break the cycle.                                                                                             |
| Subtask scope explodes during execution                                  | Undiscovered requirements                                                                                                        | Stop. Update the task queue with new subtasks. Re-analyze the dependency graph. Do not absorb the scope expansion silently.                      |
| Task queue document is missing (session lost)                            | Reconstruct from git log, file modification times, and code inspection. Do not assume any task is complete without verification. |

## Anti-Patterns

- Never mark a step complete on tool call success without verifying the output because a tool can return exit code 0 while producing incorrect, empty, or partial output.
- Never execute steps without mapping dependencies first because executing a step whose prerequisite has not completed produces a cascading failure that is hard to distinguish from the step's own failure.
- Never proceed past a failed step without a defined rollback because leaving the system in a partial state makes recovery harder than the original failure.
- Never add unrequested changes during plan execution because scope creep during execution diverges from the agreed plan and introduces unreviewed changes.
- Never discard stderr because error messages, warnings, and diagnostics are written to stderr and a step that appears to succeed on stdout may be silently degrading.
- Never start execution without a defined "done" signal for each step because without a measurable completion criterion you cannot distinguish a running step from a hung step.
- Never begin task execution without a written plan because without a plan there is no canonical definition of "done", making it impossible to detect scope creep, verify completion, or hand off to another session.
- Never parallelize steps that have undocumented data dependencies because a race condition between concurrent writers produces non-deterministic output; the result depends on execution order, making the task non-reproducible.
- Never allow a single task to grow beyond the context window without checkpointing because work done after the context limit is exceeded is not recoverable; state that is not explicitly saved to disk is lost on compaction or session end.
- Never skip the verification step after a file edit because a partial write, encoding error, or tool failure can leave the file in a broken state that is not visible until the next consumer reads it.
- Never start a task whose dependencies are not completed because out-of-order execution creates rework when the earlier task is corrected, invalidating all work that was built on the incomplete foundation.

## Self-Verification Checklist

- [ ] Each step is verified locally before the next step begins: build or test exits 0 before moving forward
- [ ] De-Sloppify pass completed on every changed file (see `.agent/shared/DE-SLOPPIFY.md`)
- [ ] `task.md` updated after every step: reflects current state
- [ ] No `git add` or `git commit` made during execution: `git log --oneline` count does not increase during plan execution
- [ ] Phase verification gate run: test suite exits 0 before proceeding to the next phase
- [ ] Any plan deviation documented: noted in `docs/plans/task.md` if scope changed
- [ ] All tasks in the queue are marked `completed` (none are `in_progress` or `pending`)
- [ ] All review gates are cleared (no unchecked boxes in the gate list)
- [ ] Full test suite passes with coverage >= the target defined in the execution contract
- [ ] Execution context snapshot is up to date and includes all decisions made

## Success Criteria

This skill is complete when: 1) every step in the plan is marked completed in task.md with verification confirmed, 2) all phase verification gates have passed (tests, linting, build), 3) the De-Sloppify pass has been run after every implementation step with no debug artifacts remaining, 4) all review gates are cleared, 5) the execution context snapshot captures all non-obvious decisions made during execution, and 6) the **Handoff block** has been emitted with `next_skill` pointing to `verification-loop` (or the next chain step) and `status: completed`.
