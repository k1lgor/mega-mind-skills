---
name: receiving-code-review
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Handling feedback systematically. Use when you receive code review feedback.
triggers:
  - "got review feedback"
  - "addressing review comments"
  - "responding to review"
---

# Receiving Code Review Skill

## When to Use

- After receiving code review feedback
- When addressing review comments
- When responding to requested changes

## When NOT to Use

- Before the review has been posted — there is nothing to receive yet
- If there are zero blocking comments (only nitpicks) — respond in the PR thread and re-request without a full structured workflow
- When the PR is in draft status — feedback on a draft is preliminary; use this skill once the PR is marked ready for review
- For reviewing other people's code (use `requesting-code-review` for self-reviews or `code-polisher` for quality passes)

## Instructions

### Step 1: Read and Understand

1. **Read all comments** before responding
2. **Understand the intent** behind each comment
3. **Categorize feedback** by type:
   - Must fix (blocking issues)
   - Should fix (important improvements)
   - Consider (suggestions)
   - Questions (need clarification)

### Step 2: Respond Professionally

For each comment:

```markdown
**Status:** [Addressed / Discussing / Won't Fix]

**Response:**
[Your explanation or the fix applied]

**Change:** (if applicable)
[Link to the commit or describe the change]
```

### Step 3: Make Changes

1. **Create a checklist** of items to address
2. **Fix issues** in logical groups
3. **Add new tests** if needed
4. **Self-review** again before pushing

### Step 4: Follow Up

1. **Mark conversations resolved**
2. **Request re-review** if significant changes
3. **Thank reviewers** for their time

## Feedback Categories and Responses

### Must Fix (Blocking)

```markdown
**Comment:** "This has a security vulnerability - user input isn't validated"

**Response:**
✅ **Addressed**
Added input validation using the validateInput middleware. All user-provided strings are now sanitized.

**Change:** Commit abc123
```

### Should Fix (Important)

```markdown
**Comment:** "This function is doing too much - consider breaking it up"

**Response:**
✅ **Addressed**
Split into three smaller functions: parseInput, validateData, and saveRecord. Each has a single responsibility.

**Change:** Commit def456
```

### Consider (Suggestion)

```markdown
**Comment:** "Could use a more descriptive variable name"

**Response:**
✅ **Addressed**
Renamed `x` to `processedItemCount` for clarity.

**Alternative:** Kept as is because this is a loop iterator and `i` is conventional. Open to changing if you feel strongly.
```

### Questions

```markdown
**Comment:** "Why did you choose this approach?"

**Response:**
🤔 **Discussing**
I chose this approach because:

1. It's consistent with the existing pattern
2. It's more performant for our use case
3. It's easier to test

Happy to discuss alternatives if you have concerns.
```

## Response Templates

### Agreeing and Fixing

```
Good catch! Fixed in [commit]. The [change] now [improvement].
```

### Explaining the Choice

```
I chose this approach because [reason]. The main benefit is [benefit]. I considered [alternative] but went with this because [why this is better].
```

### Requesting Clarification

```
Could you elaborate on [aspect]? I want to make sure I understand the concern correctly before making changes.
```

### Politely Disagreeing

```
I appreciate the feedback. I considered this but decided against it because [reason]. If you feel strongly about this, I'm happy to discuss further and potentially revise.
```

## Checklist for Addressing Feedback

```markdown
## Review Response Checklist

### Critical Issues

- [ ] Issue 1: [Description] - Fixed in commit X
- [ ] Issue 2: [Description] - Fixed in commit Y

### Suggestions

- [ ] Suggestion 1: Implemented
- [ ] Suggestion 2: Discussed and agreed to defer

### Questions

- [ ] Question 1: Answered
- [ ] Question 2: Clarified

### Self-Review After Changes

- [ ] All tests still pass
- [ ] New code follows style guide
- [ ] No new issues introduced
```

## Example Response Session

```markdown
## Review Response for PR #456

### Must Fix Items

**Comment 1:** SQL injection risk on line 45
✅ **Addressed** - Added parameterized query. Commit: a1b2c3

**Comment 2:** Missing error handling
✅ **Addressed** - Added try/catch with proper error logging. Commit: d4e5f6

### Suggestions

**Comment 3:** Consider using async/await
✅ **Addressed** - Refactored to async/await for better readability. Commit: g7h8i9

**Comment 4:** Add more descriptive names
🤔 **Discussing** - I kept the short names because they're local loop variables. Open to changing if you prefer longer names.

### Follow-up

- [ ] All critical items addressed
- [ ] Tests pass
- [ ] Ready for re-review

Thanks for the thorough review! Please let me know if you have any other concerns.
```

## Tips

- Don't take feedback personally
- Assume positive intent from reviewers
- Address all comments - don't skip any
- Ask for clarification if you don't understand
- Thank reviewers for catching issues
- Learn from patterns in feedback

## Anti-Patterns

- Never dismiss a review comment without explaining why because a comment dismissed without rationale signals to the reviewer that their feedback is unwelcome, degrading future review quality and thoroughness.
- Never push a "fix" to a review comment that doesn't address the underlying concern because a superficial fix that technically resolves the comment while ignoring the real issue will resurface as the same problem in a future PR.
- Never merge immediately after addressing review comments because the reviewer who left the comments has not verified the fixes; merging before re-review silently bypasses the approval gate.
- Never take review comments personally because conflating technical feedback with personal criticism causes defensive responses that shut down legitimate improvement conversations and create team friction.
- Never address all review comments in a single commit because a single commit making 10 unrelated changes is impossible to revert selectively if one change introduces a regression.
- Never mark a discussion as resolved without confirming with the reviewer because only the reviewer knows whether their concern was addressed; resolving on the author's behalf removes the reviewer's ability to verify the fix.

## Failure Modes

| Failure                                                                        | Cause                                                                                                               | Recovery                                                                                                                                       |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Reviewer leaves nit comments without distinguishing blockers from suggestions  | Reviewer uses a flat list with no severity label; author treats all comments as equally optional                    | Ask reviewer to prefix comments with `blocker:`, `suggestion:`, or `nit:` before addressing any; re-read the thread with that lens             |
| Reviewer approves without reading critical path changes                        | Large PR; reviewer only skimmed the summary and approved to unblock                                                 | Request a targeted re-review of the specific critical files; add a comment pointing the reviewer to the files that need scrutiny               |
| Author pushes new commits during active review, invalidating previous comments | Author receives first round of feedback and immediately starts fixing and pushing without waiting for all reviewers | Batch all fixes from a single review round before pushing; note in the PR thread "addressing round 1 feedback" with a single consolidated push |
| Review focused on style not logic, missing semantic bugs                       | Reviewer fixates on formatting/naming while the algorithmic logic is wrong                                          | Explicitly ask reviewer to focus on correctness of the business logic; run the feature through the `debugging` checklist independently         |
| Stale approval after force-push, merging unreviewed changes                    | Author force-pushed a rebase or amended commits; GitHub kept the old approval; unreviewed diff merged               | Enable "dismiss stale reviews on push" in branch protection rules; never merge after a force-push without fresh approval                       |

## Self-Verification Checklist

- [ ] All blocking comments addressed or explicitly deferred with written reason — count of unresolved blocking threads equals 0
- [ ] No unreviewed commits pushed after approval — `git log --oneline <approval-commit>..HEAD` shows 0 commits (or all commits are trivial merge commits)
- [ ] CI passing before merge — all required status checks green (exit code 0 on CI run)
- [ ] All blocking (must-fix) comments have been addressed — none skipped
- [ ] Tests still pass after the changes (`bun test` or `npm test` exits 0)
- [ ] Re-review requested if the changes were significant (not just cosmetic)
- [ ] Replied to all reviewer comments — either with a fix confirmation or a reasoned disagreement

## Success Criteria

This skill is complete when: 1) every blocking reviewer comment has a documented resolution (fixed, deferred with justification, or disputed with counter-argument), 2) the test suite still passes after all changes, and 3) the PR is re-submitted for review or merged with all participants notified.
