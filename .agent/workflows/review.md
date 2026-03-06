---
description:
---

# Review Workflow

## Trigger

Use when code is ready for review.

**Quick Start:** `/mega-mind execute review` or `/review`

## Prerequisites

- Code is complete
- All tests pass locally
- Code has been self-reviewed

## Steps

### 1. Self-Review

Before requesting review:

- Run all tests
- Run linting
- Build check
- Manual testing

### 2. Prepare Review Request

- Write clear PR description
- Document changes made
- List testing performed
- Note any questions for reviewers

### 3. Submit for Review

- Create PR with all context
- Request appropriate reviewers
- Link related issues

### 4. Address Feedback

- Read all comments carefully
- Categorize feedback
- Address each comment
- Request re-review if needed

## Next Steps After Review

After completing this workflow, typically continue with:

```
/ship → Merge and deploy
```

Or use:

```
/mega-mind execute ship
```

## Output

- Reviewed and approved code
- All feedback addressed
- Ready for merge

## Related Skills

- `requesting-code-review` - Submit for review
- `receiving-code-review` - Handle feedback
- `code-reviewer` - Agent for reviewing code
- `finishing-a-development-branch` - Merge and deploy
