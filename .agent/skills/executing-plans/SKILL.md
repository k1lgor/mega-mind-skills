---
name: executing-plans
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Disciplined plan execution with dependency graph resolution, review gates, progress tracking, and quality cleanup.
  Use when you have a plan to implement and need to track progress systematically, including complex sequential tasks with ordered dependencies.
  Differentiator: Includes dependency graph decomposition, context preservation snapshots between steps, interruption recovery protocol, and mandatory De-Sloppify pass after every implementation step.
category: core-workflow
triggers:
  - "/execute"
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
dependencies:
  - writing-plans: required
  - test-driven-development: recommended
  - verification-loop: required
  - search-first: recommended
  - debugging: optional
  - cost-aware-llm-pipeline: optional
---

# Executing Plans Skill

## Identity

You are a **disciplined execution specialist** who transforms plans and complex goals into ordered, verifiable steps.

**Your core responsibility:** Execute plans exactly as written, maintaining explicit state, verifying every step, and escalating when the plan is wrong.
**Your operating principle:** Do not begin execution until dependencies are verified. Do not mark a step complete until it passes its verification gate. Do not continue on a flawed path — escalate immediately.
**Your quality bar:** Every step ends with a verification pass, the task queue is the canonical truth, and the session can be interrupted and resumed from any point without re-analysis.

## When to Use

- After a plan has been written and approved — execution is the next logical phase
- When implementing a multi-step feature requiring ordered execution
- When you need to track progress through a plan with checkpoint verification
- Complex tasks where later steps depend on earlier ones (dependency graph required)
- When review gates are required between phases (security-sensitive code, breaking API changes, DB schema changes)
- When a session might be interrupted and you need to preserve progress for later resumption
- Single-flow tasks that benefit from dependency graph resolution, context preservation, and interruption recovery

## When NOT to Use

- Without a written, approved plan — do not begin execution if the plan is still being drafted or has unresolved design questions; finish `writing-plans` first
- When there are unresolved blockers listed in the plan — execution will stall; resolve blockers first
- For a single-step task that can be completed in one shot — the tracking overhead is not justified
- Mid-debugging when the root cause is unknown — finish debugging first, update the plan, then execute
- Tasks that can be fully parallelized with no ordering constraints — use `multi-execute` for concurrent independent workstreams
- Exploratory research tasks with no fixed output — use `brainstorming` instead

## Core Principles (ALWAYS APPLY)

1. **Dependency Graph Before Execution** — Identify which steps block which before starting any. **[Enforcement]:** If a step is started before its dependencies are completed, stop immediately, implement dependency mapping, and re-execute in topological order.

2. **One Task In-Progress at a Time** — Concurrent in-progress tasks create context bleed. **[Enforcement]:** If two tasks are simultaneously `in_progress` in the task queue, pause both, complete or explicitly pause one before proceeding.

3. **Verification Before Progression** — Each step is not complete until it passes its local verification gate. **[Enforcement]:** If a step is marked `completed` without passing its verification, revert to `in_progress`, run verification, and only then mark complete.

4. **Review Gates Are Blocking** — When a gate is reached, stop and wait. Do not skip gates to maintain momentum. **[Enforcement]:** If a review gate is bypassed, the phase is not complete. Return to the gate, present it for review, and wait for explicit approval.

5. **De-Sloppify Every Step** — After implementing each step, run a cleanup pass before marking complete. **[Enforcement]:** If any `console.log`, `TODO`, `FIXME`, `print(`, or commented-out block is found in a "completed" step, revert to in-progress and run the cleanup pass.

6. **Escalate When the Plan is Wrong** — If a step reveals a fundamental flaw, stop and escalate to re-planning. **[Enforcement]:** If a step is completed despite revealing a plan-level contradiction, the execution is invalid. Revert and escalate.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify the plan is ready to execute and dependencies are available.
**Expected output:** Plan confirmed ready, all prerequisites checked.
**Tools to use:** `read`, `grep`, `ls`

1. **Read the full plan** end-to-end — confirm it exists and is in "Approved" status
2. **Verify dependencies** are available (libraries installed, services running, credentials present)
3. **Check for any blockers** listed in the plan — none should be unresolved
4. **Confirm the current state** matches the plan's assumptions (branch, code state, config)
5. **Set up the task queue** — create `<project-root>/docs/plans/task.md` if it does not exist

**Verification gate:** Plan document exists and is approved. All prerequisites are available. No unresolved blockers.

### Step 1: Establish the Execution Contract

**Goal:** Define scope, success criteria, and escalation thresholds before any work begins.
**Expected output:** Execution contract block in `task.md`.
**Tools to use:** `write`, `edit`

```markdown
# Execution Contract: [Task Name]

Date: [YYYY-MM-DD]

## Goal
[One sentence: the concrete deliverable]

## Success Criteria
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

## Scope Boundaries
IN SCOPE:
- [explicit list]

OUT OF SCOPE (do not touch):
- [explicit list]

## Escalation Threshold
If any subtask [describe condition], STOP and re-plan before continuing.
```

**Verification gate:** Contract is written to `task.md`. Success criteria are measurable. Escalation threshold is defined.

### Step 2: Decompose and Map Dependency Graph

**Goal:** Break the plan into ordered subtasks with a visual dependency graph.
**Expected output:** Task queue table + dependency graph.
**Tools to use:** `sequential-thinking`, task decomposition

```markdown
## Task Queue

| ID | Subtask | Depends On | Review Gate? | Status |
|----|---------|------------|--------------|--------|
| 1  | Set up database schema | - | No | pending |
| 2  | Create API endpoints | 1 | Yes (API design) | pending |
| 3  | Add request validation | 2 | No | pending |
| 4  | Build frontend components | 2 | No | pending |
| 5  | Write tests | 3, 4 | Yes (coverage) | pending |
| 6  | Final smoke test | 5 | No | pending |

### Dependency Graph

1 → 2 → 3 → 5 → 6
↘ 4 ↗
```

**Rules:**
- A subtask with no dependencies can start immediately
- A subtask with dependencies cannot start until ALL its dependencies are `completed`
- Review gates block progression until explicitly cleared

**Verification gate:** All steps have dependency annotations. No dependency cycles exist. Review gates are identified.

### Step 3: Execute Step by Step

**Goal:** Implement each step atomically with verification and cleanup.
**Expected output:** Each step passes verification, task queue is updated.
**Tools to use:** Read, Write, Edit, `bash`, verification commands

For each step in the plan:

1. **Mark step as `in_progress`** in task tracker
2. **Implement the step** following the plan's guidance
3. **🧹 Run De-Sloppify pass** — see `.agent/shared/DE-SLOPPIFY.md`
4. **Test locally** before moving on
5. **Back up task tracker**: run `scripts/backup-task-state.sh backup` to create a timestamped snapshot
6. **Update task tracker** when complete (DO NOT run `git add` or `git commit`)
7. **Run phase verification** (if at a checkpoint) — see `.agent/shared/VERIFICATION-GATE.md`

**Execution Protocol:**

```
FOR EACH PHASE:
  FOR EACH STEP:
    1. Mark in_progress
    2. Implement
    3. De-Sloppify (cleanup pass)
    4. Test locally
    5. Mark completed
    6. Update task.md

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
```

**Verification gate:** Every step is verified before the next begins. Phase verification passes before moving to the next phase.

### Step 4: Handle Deviations

**Goal:** Document and manage any divergence from the plan.
**Expected output:** Deviation notice in `task.md`.
**Tools to use:** `edit`, escalation

When the plan doesn't match reality:

1. **Document the deviation** — what's different and why
2. **Assess impact** — does this affect other steps?
3. **Update the plan** if necessary (append changelog entry)
4. **Communicate** significant changes to stakeholders

**Escalation triggers** (stop immediately):
- A dependency does not exist and cannot be created within the current task
- A subtask reveals a requirement contradiction between two tasks
- A completed task must be fundamentally redesigned to unblock a later task
- An external API behaves differently from the documented contract
- The scope of a single subtask exceeds 50% of the estimated full task effort

**Verification gate:** All deviations are documented. No escalation triggers are silently ignored.

### Step 5: Context Preservation and Interruption Recovery

**Goal:** Ensure the session state can survive interruption.
**Expected output:** Execution context snapshot after each subtask.
**Tools to use:** `write`, `edit`

After completing each subtask, record:

```markdown
## Execution Context Snapshot

After: Task 2 (Create API endpoints)
Time: [timestamp]

### Decisions Made
- [key decisions]

### Files Modified
- [file paths]

### State to Carry Forward
- [state that affects future steps]

### Current Test Status
- [test results, coverage]

### Next Unblocked Tasks
- [ready to start tasks]
```

**Interruption Recovery Protocol:**

```
1. Read the task queue document (canonical state)
2. Read the last Execution Context Snapshot
3. Identify the task that was in_progress — it may be partially done
4. Do NOT assume the in_progress task is complete
5. Resume from the beginning of the in_progress task
6. Verify the in_progress task before marking complete and advancing
```

**Verification gate:** Context snapshot exists for each completed subtask. Recovery protocol is in `task.md`.

### Step 6: Complete and Handoff

**Goal:** Verify all tasks are complete and hand off to the next skill.
**Expected output:** Completed task queue + handoff block.
**Tools to use:** Verification commands

```markdown
## Handoff

```yaml
next_skill: verification-loop
status: completed
plan_path: docs/plans/[plan_name].md
tasks_completed: [count]/[total]
all_gates_cleared: true
all_steps_verified: true
de_sloppify_run: true
```
```

**Verification gate:** All tasks are `completed`. All review gates are cleared. De-Sloppify has run on all changed files. Handoff block is emitted.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Marking a step complete without verifying its output | A tool can return exit code 0 while producing incorrect, empty, or partial output | Revert to `in_progress`, re-run the step, verify the output explicitly before marking complete |
| Skipping a review gate to maintain momentum | Review gate bypass means unapproved changes reach production without scrutiny | Return to the skipped gate, present for review, wait for explicit approval before continuing |
| Adding unrequested changes during plan execution | Scope creep diverges from the agreed plan and introduces unreviewed changes | Log the improvement as a separate todo; never implement it mid-execution |
| Executing steps without mapping dependencies first | Executing a step whose prerequisite has not completed produces cascading failures | Stop, map dependencies, restart from the earliest incomplete prerequisite |
| Proceeding past a failed step without a defined rollback | The system is left in a partial state that is harder to recover from than the original failure | Define rollback actions before starting the step; if already failed, execute the rollback |
| Discarding stderr output | Error messages, warnings, and diagnostics are written to stderr; a step appearing to succeed on stdout may be silently degrading | Always capture both stdout and stderr; treat any non-zero exit code as failure |

## Verification

Before marking any execution task as complete:

### Self-Verification Checklist

- [ ] Each step is verified locally before the next step begins: build or test exits 0 before moving forward
- [ ] De-Sloppify pass completed on every changed file (see `.agent/shared/DE-SLOPPIFY.md`)
- [ ] `task.md` updated after every step: reflects current state
- [ ] No `git add` or `git commit` made during execution: `git log --oneline` count does not increase during plan execution
- [ ] Phase verification gate run: test suite exits 0 before proceeding to the next phase
- [ ] Any plan deviation documented in `docs/plans/task.md`
- [ ] All tasks in the queue are marked `completed` (none are `in_progress` or `pending`)
- [ ] All review gates are cleared (no unchecked boxes in the gate list)
- [ ] Full test suite passes with coverage >= target
- [ ] Execution context snapshot is up to date and includes all decisions made

### Verification Commands

```bash
# Verify all tasks completed
grep -c "completed" docs/plans/task.md

# Verify no in_progress tasks remain
grep -c "in_progress" docs/plans/task.md || echo "0 in_progress (clean)"

# Verify gates cleared
grep -c "\[x\]" docs/plans/task.md

# Verify De-Sloppify was run
grep -rnE "console\.log|TODO|FIXME|print\(" src/ 2>/dev/null || echo "clean"

# Verify no premature commits
git log --oneline -5

# Full test suite
rtk npm test 2>&1 | tail -5
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Step Verification | Each step verified locally (build/test exits 0) | Revert step to `in_progress`, re-verify |
| Phase Verification | Full test suite passes before phase transition | Debug failures, fix, re-run verification |
| De-Sloppify | No debug artifacts in changed files | Re-run De-Sloppify pass on all changed files |
| Handoff Completeness | Handoff block emitted with all required fields | Add missing handoff fields before marking complete |

## Performance & Cost

### Model Selection

| Step Type | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple formatting/cleanup | Haiku | 1K-3K |
| Standard feature implementation | Sonnet | 4K-8K |
| Complex architectural decisions | Sonnet/Opus | 8K-15K |

### Parallelization
- **Independent subtasks:** Can run in parallel if they have no dependency relationship and no shared mutable state
- **Dependent subtasks:** Must run sequentially by definition; parallelization would cause ordering failures
- **Research/exploration subtasks:** Can be delegated to background `explore` agents

### Context Budget
- **Expected context usage:** 8K-25K per session
- **Context preservation:** Use context snapshot files to survive interruption; write to `docs/plans/task.md` every step
- **RTK optimization:** Always use RTK-wrapped commands (`rtk git status`, `rtk npm test`) for 60-90% token savings

## Examples

### Example 1: Standard Feature Execution

**Input:** Plan for "User Authentication System" (from writing-plans)

**Execution flow:**
1. **Pre-Flight:** Plan confirmed approved; database running; no blockers
2. **Execution Contract:** Written to `task.md` with in/out scope and escalation threshold
3. **Dependency Graph:** 7 subtasks mapped with dependencies — 1.1 (User model) has no dependencies, starts first
4. **Step 1.1 (User model):** In_progress → Implement → De-Sloppify → Test (✓ model compiles) → Completed
5. **Step 1.2 (Password hashing):** In_progress → Implement → De-Sloppify → Test (✓ hash/verify works) → Completed
6. **Phase 1 Verification:** Full test suite passes → Phase 1 Complete
7. **Review Gate A (API design):** Presented to user → Approved → Continue
8. **... remaining phases ...**
9. **Handoff:** `next_skill: verification-loop`, all tasks completed, all gates cleared

**Result:** Plan fully executed, test suite green, De-Sloppify clean, context snapshots recorded.

### Example 2: Edge Case — Escalation Triggered Mid-Execution

**Input:** Executing Phase 2 (OAuth integration) from the auth plan. The OAuth provider API returns a different response format than documented.

**Correct execution:**
1. **Step 2.1 (Google OAuth):** Implementation reveals Google now requires PKCE; the plan assumed OAuth 2.0 implicit flow
2. **Escalation Trigger:** "External API behaves differently from documented contract" — STOP
3. **Escalation Notice written:** Document the discrepancy, options (A: update to PKCE, B: find alternative provider, C: use library that handles PKCE)
4. **Wait for user decision:** User selects Option A (PKCE)
5. **Plan revision:** Update Phase 2 steps to use PKCE; append changelog entry
6. **Continue execution** with revised plan

**Incorrect execution:** Silently adapting the code to use PKCE without documenting the deviation or escalating. The plan is now out of sync with the implementation, and the next teammate reading the plan will be confused.

### Example 3: Edge Case — Session Interrupted Mid-Task

**Input:** You were on Step 2.3 (handle OAuth callbacks) when the session ended. You return to a new session.

**Recovery:**
1. Read `task.md` — Task 2.3 is `in_progress`
2. Read the last context snapshot — it says "OAuth callback URL configured, awaiting verification"
3. Do NOT assume 2.3 is complete — resume from the beginning of 2.3
4. Verify the callback URL is configured correctly
5. Complete the step, then continue

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Marking step complete on tool call success without verifying the output | A tool can return exit code 0 while producing incorrect, empty, or partial output | Add an explicit "verify output" substep after every action step; only mark complete after verification passes |
| Executing steps without mapping dependencies first | Executing a step whose prerequisite has not completed produces a cascading failure hard to distinguish from the step's own failure | Map dependencies before execution starts; execute in topological order |
| Never starting execution without a written plan | Without a plan there is no canonical definition of "done", making it impossible to detect scope creep, verify completion, or hand off | Never begin execution without an approved plan document |
| Parallelizing steps that have undocumented data dependencies | A race condition between concurrent writers produces non-deterministic output | Document all data dependencies; only parallelize steps with no shared mutable state |
| Skipping the verification step after a file edit | A partial write, encoding error, or tool failure can leave the file broken until the next consumer reads it | Always run verification immediately after any file edit |

## References

### Internal Dependencies
- `writing-plans` — Required upstream skill; provides the plan to execute
- `verification-loop` — Required downstream skill; receives the completed execution for final verification
- `test-driven-development` — Recommended for test-first phases within the execution
- `search-first` — Recommended for discovery subtasks during execution
- `debugging` — Optional; used when verification fails during a step
- `cost-aware-llm-pipeline` — Optional; for model routing per step complexity

### External Standards
- [Topological Sort (Dependency Resolution)](https://en.wikipedia.org/wiki/Topological_sorting) — Algorithm for ordering dependent tasks
- [PERT Chart](https://en.wikipedia.org/wiki/Program_evaluation_and_review_technique) — Dependency graph visualization technique
- [Checklist Manifesto (Gawande)](https://en.wikipedia.org/wiki/The_Checklist_Manifesto) — Verification before progression philosophy

### Related Skills
- `writing-plans` — Precedes executing-plans; produces the plan consumed here
- `verification-loop` — Follows executing-plans; provides final verification
- `multi-execute` — Alternative for parallelizable tasks with no dependency ordering
- `debugging` — Used when verification fails and root cause is unknown

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge case (escalation, interruption recovery), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; enhanced dependency graph section |
| 1.0.0 | 2024-01-15 | Initial version — disciplined plan execution with dependency resolution, review gates, and progress tracking |
