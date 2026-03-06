---
description:
---

# Execute Plan Workflow

## Trigger

Use when you have a plan ready to implement.

**Quick Start:** `/mega-mind execute execute-plan` or `/execute`

## Prerequisites

- A completed plan from `writing-plans` skill
- All dependencies available
- Development environment ready

## Steps

### 1. Load the Plan

- Read the full plan end-to-end
- Verify dependencies are available
- Check for any blockers

### 2. Execute Phase by Phase

For each phase:

- Mark step as in-progress
- Implement following plan guidance
- Test locally
- Mark as completed
- Update task tracker

### 3. Run Phase Verification

After each phase:

- Run tests
- Verify integration
- Check for regressions

### 4. Handle Deviations

If plan doesn't match reality:

- Document the deviation
- Assess impact
- Update plan if needed

## Next Steps After Execution

After completing this workflow, typically continue with:

```
/verify → Verify the implementation works
/review → Request code review
```

Or use:

```
/mega-mind execute review
```

## Output

- Completed implementation
- Updated task tracker
- Verification results

## Related Skills

- `executing-plans` - The core execution skill
- `verification-before-completion` - Verify before done
- `requesting-code-review` - Submit for review
- `single-flow-task-execution` - For simpler tasks
