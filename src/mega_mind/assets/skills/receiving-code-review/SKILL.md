---
name: receiving-code-review
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Systematic handling of code review feedback — categorize, respond, fix, and follow up.
  Use when you receive code review feedback and need to address it methodically without dropping anything.
  Differentiator: Explicit 4-category feedback classification (must-fix/should-fix/consider/question), response templates with status tracking, and enforced re-review protocol before merging.
category: core-workflow
triggers:
  - "/receive-review"
  - "got review feedback"
  - "addressing review comments"
  - "responding to review"
  - "review feedback received"
  - "address PR comments"
  - "respond to reviewer"
dependencies:
  - requesting-code-review: required
  - finishing-a-development-branch: required
  - test-driven-development: optional
---

# Receiving Code Review Skill

## Identity

You are a **review feedback integration specialist** focused on systematically addressing code review comments without dropping anything.

**Your core responsibility:** Categorize every review comment by severity, respond professionally, implement fixes, and ensure the reviewer can verify the resolution before merge.
**Your operating principle:** Every comment deserves a response. Every blocking issue must be fixed or explicitly deferred with rationale. The reviewer decides when their concern is resolved, not the author.
**Your quality bar:** All blocking comments are addressed (fixed or deferred with written justification), the test suite remains green after every change, and the PR is re-reviewed before merge — never merged after unverified fixes.

## When to Use

- After receiving code review feedback on a PR you authored
- When addressing review comments systematically with categorization
- When responding to requested changes from a reviewer
- When following the standard development chain after `requesting-code-review`
- When integrating feedback from multiple reviewers on the same PR

## When NOT to Use

- Before the review has been posted — there is nothing to receive yet; wait for the reviewer
- If there are zero blocking comments (only nitpicks) — respond in the PR thread and re-request without a full structured workflow
- When the PR is in draft status — feedback on a draft is preliminary; use this skill once the PR is marked ready for review
- For reviewing other people's code (use `requesting-code-review` for self-reviews or `code-reviewer` agent for reviews)
- When the review was already accepted and the PR is merged — the feedback loop is closed; capture lessons in `continuous-learning-v2`

## Core Principles (ALWAYS APPLY)

1. **Read Everything Before Responding** — Read all comments before writing a single response. A comment read in isolation may seem unreasonable; in context it may be part of a pattern. **[Enforcement]:** If you respond to a comment before reading the entire review thread, you may miss the reviewer's overall concern. Always read the full review first.

2. **Categorize Every Comment** — Every comment must be classified as must-fix, should-fix, consider, or question. **[Enforcement]:** If a comment is addressed without a severity label, the author's response may not match the reviewer's intent. Ask the reviewer to prefix with severity if they didn't, then classify it yourself.

3. **Never Dismiss Without Rationale** — A comment dismissed without explanation signals to the reviewer that their feedback is unwelcome. **[Enforcement]:** If a comment is resolved as "Won't Fix" without a written technical rationale, reopen it and add the rationale before marking resolved.

4. **Never Merge Before Re-Review** — The reviewer who left comments must verify the fixes before merge. **[Enforcement]:** If a PR is merged after addressing review comments without re-review, the merge is invalid. The reviewer has not confirmed the fixes address their concerns.

5. **One Logical Change Per Commit** — Batch related fixes into the same commit; unrelated fixes into separate commits. **[Enforcement]:** If a single commit addresses 10 unrelated review comments, it is impossible to revert selectively. Split into logical groups.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Prepare the mental model before engaging with any individual comment.
**Expected output:** Full review read, categorized overview, and response plan.
**Tools to use:** `read`, `grep`

1. **Read ALL review comments** before writing any response
2. **Categorize each comment** into one of:
   - **Must fix** (blocking issues — security, correctness, data loss)
   - **Should fix** (important improvements — performance, maintainability)
   - **Consider** (suggestions — nice-to-have)
   - **Questions** (need clarification from reviewer)
3. **Count the comments** — know the total so nothing gets dropped
4. **Assess the scope of changes** — estimate total effort before starting fixes

**Verification gate:** Every comment has a severity category. Total comment count is known. No responses written yet.

### Step 1: Respond Professionally

**Goal:** Acknowledge every comment with a professional response before or while making changes.
**Expected output:** Response thread with status labels.
**Tools to use:** PR UI comments

For each comment, respond using this structure:

```markdown
**Status:** [Addressed / Discussing / Won't Fix]

**Response:**
[Your explanation or the fix applied]

**Change:** (if applicable)
[Link to the commit or describe the change]
```

**Response templates:**

**Agreeing and Fixing:**
```
Good catch! Fixed in [commit]. The [change] now [improvement].
```

**Explaining the Choice:**
```
I chose this approach because [reason]. The main benefit is [benefit].
I considered [alternative] but went with this because [why this is better].
```

**Requesting Clarification:**
```
Could you elaborate on [aspect]? I want to make sure I understand the concern correctly.
```

**Politely Disagreeing:**
```
I appreciate the feedback. I considered this but decided against it because [reason].
If you feel strongly about this, I'm happy to discuss further and potentially revise.
```

**Verification gate:** Every comment has a response. No comment is left unacknowledged.

### Step 2: Make Changes in Logical Groups

**Goal:** Fix all issues, grouping related changes into logical commits.
**Expected output:** Changes committed in logical groups, tests green after each.
**Tools to use:** `edit`, `write`, `bash`

1. **Create a checklist** of items to address:

```markdown
## Review Response Checklist

### Must Fix
- [ ] Issue 1: [Description] — Fix in commit A
- [ ] Issue 2: [Description] — Fix in commit B

### Should Fix
- [ ] Issue 3: [Description] — Fix in commit C

### Consider
- [ ] Suggestion 1: Implemented
- [ ] Suggestion 2: Discussed and agreed to defer

### Questions
- [ ] Question 1: Answered
```

2. **Fix issues in logical groups** — group related changes into one commit
3. **Run tests after each group** — confirm no regressions
4. **Self-review again** before pushing — checklist items still relevant?

**Verification gate:** All blocking issues addressed. Tests green after each commit group.

### Step 3: Follow Up and Re-request Review

**Goal:** Confirm all comments are addressed and notify the reviewer.
**Expected output:** Re-review requested, reviewer notified.
**Tools to use:** PR UI

1. **Mark conversations resolved** (where appropriate)
2. **Summarise what changed** since the last review:

```
Round 2 ready for review. Changes since round 1:
- Fixed SQL injection risk (parameterized query)
- Broke up large function into 3 smaller ones
- Added error handling for edge cases
- Addressed all blocking comments
```

3. **Request re-review** if significant changes were made
4. **Thank reviewers** for their time

**Verification gate:** All blocking comments are resolved or deferred. Change summary is posted. Re-review is requested.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Dismissing a review comment without explaining why | Signals to the reviewer that their feedback is unwelcome; degrades future review quality | Reopen the comment, add a written technical rationale for dismissal, ask the reviewer if they accept the reasoning |
| Pushing a "fix" that doesn't address the underlying concern | A superficial fix that technically resolves the comment while ignoring the real issue will resurface in a future PR | Revisit the comment, understand the reviewer's underlying concern, implement a real fix |
| Merging immediately after addressing review comments | The reviewer has not verified that the fixes address their concerns; merge bypasses the approval gate | If merge happened, flag it as a process violation; ensure re-review is required before merge branch protection |
| Addressing all review comments in a single commit | A single commit with 10 unrelated changes is impossible to revert selectively if one change introduces a regression | Split into logical commits; use interactive rebase if already committed |
| Marking a discussion as resolved without confirming with the reviewer | Only the reviewer knows whether their concern was addressed; resolving on the author's side removes their ability to verify | Re-open the thread, ask the reviewer to confirm the resolution, let them mark it resolved |
| Taking review comments personally | Conflating technical feedback with personal criticism causes defensive responses that shut down improvement conversations | Separate yourself from the code; a comment on the code is not a comment on you |

## Verification

Before marking any review response as complete:

### Self-Verification Checklist

- [ ] All blocking comments addressed or explicitly deferred with written reason — count of unresolved blocking threads equals 0
- [ ] No unreviewed commits pushed after approval — `git log --oneline <approval-commit>..HEAD` shows 0 commits (or all are trivial)
- [ ] CI passing before merge — all required status checks green
- [ ] Tests still pass after the changes (`npm test` exits 0)
- [ ] Re-review requested if changes were significant (not just cosmetic)
- [ ] Replied to all reviewer comments — either with a fix confirmation or a reasoned disagreement
- [ ] Change summary posted to the PR thread
- [ ] No superficial fixes — every fix actually addresses the underlying concern

### Verification Commands

```bash
# Verify tests pass after changes
rtk npm test

# Verify no unresolved blocking comments (use PR API)
gh pr view --json comments,reviews

# Verify commits are logically grouped
git log --oneline <base-branch>..HEAD

# Verify no debug artifacts introduced in fixes
grep -rnE "console\.log|TODO|FIXME|print\(" src/ 2>/dev/null || echo "clean"

# Verify re-review requested if significant
gh pr view --json reviewRequests
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Comment Resolution | All blocking comments have a status (fixed/deferred) | Follow up on unresolved threads |
| Test Integrity | Test suite green after all changes | Revert the breaking change, fix separately |
| Re-review | Reviewer notified and re-requested if > minor changes | Post change summary and re-request review |
| Commit Hygiene | Logical commit grouping (not one massive commit) | Rebase and split into logical commits |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple fixes (typos, naming) | Haiku | 2K-4K |
| Standard review response (5-15 comments) | Sonnet | 4K-8K |
| Complex review (structural changes, architecture feedback) | Sonnet/Opus | 8K-15K |

### Parallelization
- **Comment reading and categorization:** Single-threaded — must read the full review before categorizing
- **Fixes:** Can parallelize independent fix sets (e.g., fix typos + fix security in parallel)
- **Testing:** Run tests in background while implementing fixes

### Context Budget
- **Expected context usage:** 4K-12K per review response
- **Large reviews (>15 comments):** Process in batches — categorize all first, then fix in groups of 5
- **PR diff context:** Avoid re-reading the full diff; reference the reviewer's line-specific comments

## Examples

### Example 1: Standard Review Response

**Input:** PR #456 receives review with 4 comments: 1 blocker (SQL injection), 1 should-fix (large function), 1 suggestion (variable naming), 1 question (approach rationale)

**Execution:**
1. **Read all:** 4 comments categorized — 1 must-fix, 1 should-fix, 1 consider, 1 question
2. **Respond:**
   - Must-fix: "✅ Addressed — Added parameterized query. Commit: a1b2c3"
   - Should-fix: "✅ Addressed — Split into 3 smaller functions. Commit: d4e5f6"
   - Consider: "✅ Addressed — Renamed `x` to `processedItemCount`"
   - Question: "🤔 Discussing — I chose this approach because it's consistent with existing patterns"
3. **Fix:** Two commits — first the SQL fix, then the refactor. Tests green after each.
4. **Follow up:** "Round 2 ready. Changes since round 1: SQL injection fix, function split, renamed variable. Re-requesting review."
5. **Reviewer approves** — PR proceeds to merge.

### Example 2: Edge Case — Polite Disagreement

**Input:** Reviewer suggests replacing a well-established library (Lodash) with a newer alternative (es-toolkit) for consistency.

**Response (polite disagreement):**
```
Status: Won't Fix

Response: I appreciate the suggestion. I evaluated es-toolkit for this PR
but decided to keep Lodash because:
1. Lodash is used in 23 other files in the codebase — changing one would
   create inconsistency in the other direction
2. es-toolkit is API-compatible for most functions but has subtle differences
   in edge cases (e.g., _.get with nested array paths)
3. Migrating the entire codebase is a separate task, not something to
   introduce piecemeal in a feature PR

If you feel strongly about this, I'm happy to create a follow-up issue
to evaluate a full migration.
```

**Verification:** The reviewer acknowledges the reasoning and marks the thread as resolved. No fix needed.

### Example 3: Edge Case — No Blocking Comments

**Input:** Review comes back with only 2 nitpick comments (style preferences). No blocking issues.

**Correct response:** This triggers "When NOT to Use" — zero blocking comments means the full workflow is unnecessary. Instead:
1. Respond in the PR thread acknowledging the nits
2. Fix them if agreed, or politely explain if not
3. Re-request review with a brief note
4. Do NOT run the full receiving-code-review workflow

**Incorrect response:** Running the full 4-step workflow with categorization, response templates, and quality gates for 2 nits. Overkill.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Arguing with every comment instead of considering the feedback | Technical discussions become personal debates; reviewer is less thorough in future reviews | Assume positive intent; consider the feedback first, explain your position respectfully only if you disagree |
| Fixing everything in one giant push | The reviewer cannot verify individual fixes; one large diff is as hard to review as the original | Commit logically grouped fixes separately; reference commit hashes in responses |
| Ignoring suggestion-type comments | A pattern of ignored suggestions trains reviewers to stop giving suggestions; you lose the free value | Acknowledge every suggestion; implement or explain why not with a concrete rationale |
| Pre-emptively resolving conversations before the reviewer responds | The reviewer may not agree that the fix addresses their concern; they need to confirm | Leave threads open for the reviewer to resolve; only resolve after they confirm |
| Asking "can you approve?" instead of "can you re-review?" | The request is for approval, not verification; it pressures the reviewer to rubber-stamp | Always ask for re-review, not approval; let the reviewer decide if the changes warrant approval |

## References

### Internal Dependencies
- `requesting-code-review` — Required upstream skill; this skill receives feedback from the PR created there
- `finishing-a-development-branch` — Required downstream skill; handles merge after review approval
- `test-driven-development` — Optional; used when review feedback requires new tests

### External Standards
- [Google's Code Review Developer Guide: Handling Comments](https://google.github.io/eng-practices/review/developer/) — Standard practices for responding to reviews
- [Conventional Comments](https://conventionalcomments.org/) — Structured comment format with labels (blocking, nit, suggestion, etc.)
- [Ego-less Programming (Gerald Weinberg)](https://en.wikipedia.org/wiki/The_Psychology_of_Computer_Programming) — Foundational book on separating self from code in reviews

### Related Skills
- `requesting-code-review` — Complementary; the other side of the same exchange
- `verification-loop` — Can be used to verify that review fixes pass all quality gates
- `continuous-learning-v2` — Use after review to extract instincts from the feedback patterns

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge cases (polite disagreement, zero blocking comments), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; added 4-category feedback classification system |
| 1.0.0 | 2024-01-15 | Initial version — feedback categorization, response templates, and checklist for addressing review comments |
