---
name: executing-plans
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Disciplined plan execution with progress tracking and quality cleanup. Use when you have a plan to implement and need to track progress systematically.
triggers:
  - "execute the plan"
  - "implement the plan"
  - "follow the plan"
  - "start implementation"
  - "begin the work"
---

# Executing Plans Skill

## When to Use

- After a plan has been written and approved
- When implementing a multi-step feature
- When you need to track progress through a plan

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
3. **🧹 Run De-Sloppify pass** — clean up all artifacts from implementation (see below)
4. **Test locally** before moving on
5. **Update task tracker** when complete (DO NOT run `git add` or `git commit` here. Committing is reserved for the end of the workflow).
6. **Run verification** for the phase (if at a checkpoint)

### 🧹 The De-Sloppify Pass (MANDATORY after each step)

After every implementation step, do a quality cleanup pass on all changed files:

```
DE-SLOPPIFY CHECKLIST for each changed file:
- [ ] Remove console.log / print / debugger / breakpoints
- [ ] Remove TODO comments that were just resolved
- [ ] Remove unused imports
- [ ] Remove dead code paths
- [ ] Ensure consistent formatting (indentation, spacing)
- [ ] Ensure variable names are descriptive (no `x`, `temp`, `foo`)
- [ ] Remove commented-out old code
- [ ] Fix obvious inconsistencies introduced during implementation
```

> **Why a separate pass?** The implementing agent is focused on making things work. A separate cleanup phase is more effective at catching artifacts than asking the implementer to "also clean up" — the implementer is anchored to implementation choices. Clean code = fewer bugs.

**Do NOT** change behavior or logic during de-sloppify. If you find a logic bug, fix it as a named separate step.

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
5. ⏳ verification-before-completion

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
    - Debug issue (use systematic-debugging skill if needed)
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

## Verification Checklist

Before marking any phase complete:

- [ ] All steps in phase are marked completed
- [ ] All tests pass (`rtk bun test (or rtk npm test)` or equivalent)
- [ ] Code compiles without errors
- [ ] Linting passes (`rtk lint`)
- [ ] Feature works as expected manually
- [ ] No regressions in existing functionality

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

Step 1.3: Registration endpoint
[Implementing...]
[Testing...] ✓ Registration works
[Marking complete] ✓

Phase 1 Verification:
- [✓] All steps complete
- [✓] Tests pass
- [✓] Can register a user
- [✓] Passwords are hashed

Phase 1 Complete! Moving to Phase 2...
```

## Tips

- Never skip verification steps
- If you get blocked, document why and move to what you can do
- Keep the plan visible - refer back to it frequently
- Celebrate phase completions - they're meaningful milestones
- If a step is taking much longer than estimated, reassess the approach

## Token Optimization (RTK)

During plan execution, you will often run verbose commands like `ls`, `git status`, or `bun install (or npm install)`. Always prefer using **RTK-wrapped commands** to save 60-90% of tokens:

- Use `rtk ls` instead of `ls`
- Use `rtk git status` instead of `git status`
- Use `rtk bun test (or npm test)` instead of `bun test (or npm test)`

Run `rtk gain` periodically to check your cumulative token savings.
