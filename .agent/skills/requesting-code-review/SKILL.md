---
name: requesting-code-review
description: Structured review flow with checklists. Use when your code is ready for review.
triggers:
  - "review this code"
  - "ready for review"
  - "please review"
  - "code review"
---

# Requesting Code Review Skill

## When to Use

- Code is complete and ready for review
- Before merging a significant change
- When you want feedback on implementation

## Pre-Review Checklist

Before requesting review, ensure:

```markdown
## Self-Review Checklist

### Code Quality

- [ ] Code follows project style guide
- [ ] No commented-out code
- [ ] No debug logging left in
- [ ] Meaningful variable and function names
- [ ] Functions are focused and small

### Testing

- [ ] All tests pass
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Test coverage maintained or improved

### Documentation

- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Complex logic has comments
- [ ] Type definitions are complete

### Security

- [ ] No hardcoded secrets
- [ ] Input validation in place
- [ ] No SQL injection risks
- [ ] Authentication/authorization correct
```

## Review Request Template

```markdown
## Pull Request: [Title]

### Summary

Brief description of what this PR does and why.

### Changes

- Change 1
- Change 2
- Change 3

### Testing

- How to test this change
- What tests were added

### Screenshots (if applicable)

Before/After screenshots

### Checklist

- [ ] All tests pass
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No security issues

### Questions for Reviewers

- Any concerns about the approach?
- Any suggestions for improvement?

### Related Issues

Fixes #123
Relates to #456
```

## Review Categories

### 1. Logic Review

- Does the code do what it's supposed to?
- Are edge cases handled?
- Is error handling appropriate?

### 2. Architecture Review

- Is the design appropriate?
- Are responsibilities clear?
- Is the code maintainable?

### 3. Security Review

- Are there security vulnerabilities?
- Is sensitive data protected?
- Are permissions correct?

### 4. Performance Review

- Are there performance concerns?
- Is the code efficient?
- Are there N+1 queries?

### 5. Testing Review

- Are tests comprehensive?
- Do tests cover edge cases?
- Are tests maintainable?

## Example Review Request

```markdown
## Pull Request: Add user notification preferences

### Summary

Implements user notification preferences, allowing users to control which notifications they receive and how (email, push, in-app).

### Changes

- Added NotificationPreferences model
- Created /settings/notifications page
- Updated notification service to check preferences
- Added preference checkboxes to existing notifications

### Testing

1. Create a new user
2. Navigate to Settings > Notifications
3. Toggle preferences
4. Trigger notifications and verify behavior matches preferences

### Tests Added

- Unit tests for NotificationPreferences model
- Integration tests for preference checking
- E2E test for settings page

### Questions for Reviewers

- Is the preference structure flexible enough for future notification types?
- Should we have a "notification digest" feature?

### Related Issues

Fixes #234
```

## Responding to Feedback

When you receive review feedback:

1. **Read carefully** - Understand the concern
2. **Address promptly** - Don't let reviews stall
3. **Discuss if needed** - Ask for clarification
4. **Mark resolved** - Track what's been addressed

## Tips

- Keep PRs small and focused (max ~400 lines)
- Provide context for reviewers
- Be open to feedback
- Thank your reviewers
- Don't take criticism personally
