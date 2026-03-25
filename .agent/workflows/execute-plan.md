---
description: Execute a planned task with disciplined tracking and verification.
---

# Execute Plan Workflow

## Trigger

Use after a plan is approved and ready for implementation.

**Quick Start:** `/mega-mind execute execute-plan` or `/execute`

## Steps

### 1. Initialize Task

- Update `<project-root>/docs/plans/task.md`.
- Set task to `in_progress`.

### 2. Implement Step-by-Step

- For each atomic step in the plan:
  - Implement the code.
  - **De-Sloppify:** Immediately remove debug artifacts, console logs, and unused code.
  - Verify the specific change.

### 3. Continuous Verification

- Periodically run Phase 1 (Build) and Phase 2 (Types) to catch regressions early.

### 4. Final Quality Gate (verification-loop)

- Run `/verify` to trigger the **`verification-loop`**.
- Pass all 6 phases:
  1. Phase 0: De-Sloppify Check
  2. Phase 1: Build
  3. Phase 2: Types
  4. Phase 3: Lint
  5. Phase 4: Tests + Coverage
  6. Phase 5: Security Scan
  7. Phase 6: Diff Review

### 5. Task Completion

- Mark task as `completed` in `task.md`.
- Propose next steps or run `finishing-a-development-branch`.

## Related Skills

- `executing-plans` - The core execution engine
- `verification-loop` - The primary quality gate
- `plankton-code-quality` - For write-time enforcement
