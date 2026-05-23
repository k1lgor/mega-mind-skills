---
name: requesting-code-review
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
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

## When NOT to Use

- When the self-review checklist has not been completed — don't request external review for work you haven't reviewed yourself
- When tests are failing — fix them first; reviewers shouldn't spend time on code with a broken test suite
- For WIP / draft PRs where the implementation is known to be incomplete
- When only asking for a rubber stamp on something already merged — review happens before merge, not after

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

## Self-Verification Checklist

grep -cE "what changed|why|how to verify|motivation|testing steps"
grep -cE "split rationale|must be larger"
grep -cE "fail|error"

- [ ] Self-review completed with all pre-review items ticked: `grep -c "\[x\]" <pr_checklist>` >= total checkbox count in the pre-review checklist — unticked items fail this check
      grep -rnE "console\.log|print(|TODO|FIXME"
      grep -inE "feature|refactor|bug fix|chore"

## Success Criteria

This skill is complete when: 1) the self-review checklist is completed with all tests passing, 2) the PR description is written with context for reviewers, and 3) the PR is submitted with appropriate reviewers tagged and no blocking issues remaining.

## Anti-Patterns

- Never request review on a PR with failing CI because sending a PR with a red build forces the reviewer to mentally filter out test failures from logic issues, making the review less effective and signalling a lack of self-review discipline.
- Never submit a PR larger than 400 lines without splitting it because large PRs receive rubber-stamp reviews; reviewers lose the ability to hold the full diff in working memory and critical defects are reliably missed.
- Never request review without a description of what changed and why because a context-free diff makes reviewers guess at intent, leading to comments that address the how rather than verifying the why.
- Never assign review to someone without checking their availability because assigning a reviewer who is on leave or deep in another task creates review latency that blocks the PR without any apparent reason.
- Never request review on a draft because a draft PR signals the work is incomplete; review comments on draft code are wasted if the implementation changes before the PR is marked ready.
- Never re-request review without summarising what changed since the last review because requiring the reviewer to re-read the entire diff to find what you changed disrespects their time and delays the second-round approval.

## Failure Modes

| Failure                                                                       | Cause                                                                                    | Recovery                                                                                                                                                         |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PR too large to meaningfully review, reviewer rubber-stamps it                | Feature, refactor, and bug fix bundled into one PR; diff exceeds 400 lines               | Split the PR into logical chunks (e.g., refactor first, feature second); if splitting is impossible, provide a guided review walkthrough with per-file context   |
| Blocking comment escalates but author and reviewer have no resolution path    | Technical disagreement with no escalation process; comment thread grows without progress | Timebox the async thread to 48 hours; if unresolved, escalate to a 15-minute synchronous meeting with a designated decision-maker                                |
| CI failing post-review causes delay because fix re-triggers full review cycle | Author merges CI fix after approval, requiring fresh review per branch protection rules  | Keep CI green before requesting review; if CI breaks post-approval, communicate to reviewer the exact change made and request targeted re-review of only the fix |
| Scope creep added to PR after approval, bypassing review                      | Author adds "one small thing" commit after approval without notifying reviewer           | Never push new logic after approval without re-requesting review; use a comment noting the addition and explicitly ping the reviewer                             |
| Reviewer ghosting blocks merge for >48h with no escalation path               | Reviewer assigned but no response; no SLA defined for review turnaround                  | Ping the reviewer after 24h; escalate to a second reviewer after 48h; document the escalation path in the team working agreement                                 |

## Tips

- Keep PRs small and focused (max ~400 lines)
- Provide context for reviewers
- Be open to feedback
- Thank your reviewers
- Don't take criticism personally
