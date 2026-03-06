---
description:
---

# Ship Workflow

## Trigger

Use when ready to merge and deploy.

**Quick Start:** `/mega-mind execute ship` or `/ship`

## Prerequisites

- All tests pass
- Code reviewed and approved
- Documentation updated
- No blockers

## Steps

### 1. Final Verification

- All tests pass
- Code reviewed and approved
- Documentation updated
- No blockers

### 2. Pre-Merge Checklist

- Branch up to date with main
- No conflicts
- CI passes
- Ready for merge

### 3. Merge

- Choose appropriate merge method
- Squash and merge for clean history
- Or merge commit to preserve history

### 4. Post-Merge

- Delete feature branch
- Update local environment
- Deploy if automated
- Monitor for issues

## Output

- Merged code
- Clean branch state
- Deployed feature (if applicable)

## Related Skills

- `finishing-a-development-branch` - The core shipping skill
- `verification-before-completion` - Final verification
- `ci-config-helper` - CI/CD configuration
- `observability-specialist` - Post-deploy monitoring

## Full Development Cycle

The complete workflow from start to finish:

```
/mega-mind route → brainstorming → writing-plans → tdd →
executing-plans → verification-before-completion → review → ship
```

Or simply:

```
/mega-mind "I need to implement [feature]"
```

And let the orchestrator guide you through each step.
