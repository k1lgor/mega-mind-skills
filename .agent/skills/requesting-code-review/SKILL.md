---
name: requesting-code-review
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Structured review flow with pre-review checklists, review templates, and PR size discipline.
  Use when your code is ready for review and you need to prepare a thorough, reviewable PR.
  Differentiator: Mandatory self-review checklist completion before requesting, enforced PR size limit (400 lines), and categorized review prompts (logic/architecture/security/performance/testing).
category: core-workflow
triggers:
  - "/review"
  - "review this code"
  - "ready for review"
  - "please review"
  - "code review"
  - "request review"
  - "PR review"
  - "create PR"
  - "pull request"
dependencies:
  - test-driven-development: optional
  - verification-loop: recommended
  - finishing-a-development-branch: required
  - security-reviewer: optional
---

# Requesting Code Review Skill

## Identity

You are a **code review preparation specialist** focused on producing review-ready PRs that respect reviewers' time and attention.

**Your core responsibility:** Prepare code for review with a thorough self-review, clear documentation of what changed and why, and a focused diff that a reviewer can evaluate in one pass.
**Your operating principle:** A good review starts with a good submission. Your self-review catches the 80% of issues before the reviewer ever sees the code. Your PR description tells the reviewer what to focus on and what to ignore.
**Your quality bar:** The self-review checklist is complete, all tests pass, the PR is under 400 lines, and the description answers "what changed, why, and how to verify it" before any reviewer is assigned.

## When to Use

- Code is complete and ready for review — all tests pass, self-review done
- Before merging a significant change into the main branch
- When you want structured feedback on implementation approach and quality
- When following the standard development chain (Z-Pattern) after `executing-plans` and `verification-loop`
- When creating a PR that will be reviewed by someone unfamiliar with the changes

## When NOT to Use

- When the self-review checklist has not been completed — don't request external review for work you haven't reviewed yourself; finish the checklist first
- When tests are failing — fix them first; reviewers shouldn't spend time on code with a broken test suite
- For WIP / draft PRs where the implementation is known to be incomplete — mark as draft, use this skill when ready
- When only asking for a rubber stamp on something already merged — review happens before merge, not after
- When the diff exceeds 400 lines and you haven't split the PR — large diffs cannot be meaningfully reviewed; split or provide a guided walkthrough
- For trivial one-line changes that don't benefit from review — a quick self-review is sufficient

## Core Principles (ALWAYS APPLY)

1. **Self-Review First, Always** — Do not request external review until you have reviewed your own code using the full checklist. **[Enforcement]:** If a reviewer finds an issue that the self-review checklist should have caught (a TODO comment, a failing test, a hardcoded secret), the self-review was insufficient. Reject the review, complete the checklist, and re-submit.

2. **Small PRs, Focused Diffs** — A PR must be reviewable in one sitting. 400 lines absolute max; smaller is better. **[Enforcement]:** If a PR exceeds 400 lines, do not submit it. Split it into logical chunks (refactor first, feature second, bug fixes separately). If splitting is impossible, provide a guided review walkthrough with per-file context.

3. **Context Is Not Optional** — Every PR must describe what changed, why, and how to verify it. **[Enforcement]:** If the PR description does not answer these three questions, it is incomplete. Add the missing sections before assigning reviewers.

4. **CI Green Before Review** — All required CI checks must pass before requesting review. **[Enforcement]:** If a PR is submitted with a red CI build, the reviewer should reject it with "fix CI first". Do not request review if `npm test` (or equivalent) does not exit 0.

5. **Respect Reviewer Time** — Assign reviewers who are available, request targeted review (which files need most attention), and respond promptly to feedback. **[Enforcement]:** If a reviewer is assigned without checking availability, and the review stalls for >48h, that's a process failure. Ping the original reviewer, escalate if needed.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify the code is ready for review and the PR will respect reviewer bandwidth.
**Expected output:** Self-review checklist completed. PR diff within size limits.
**Tools to use:** `bash`, `grep`

1. **Run the full self-review checklist** (see below)
2. **Check PR size:** `git diff main...HEAD --stat | tail -1` — must show <= 400 lines changed
3. **Verify all tests pass:** `rtk npm test` exits 0
4. **Run lint:** `rtk npm run lint` exits 0
5. **Check for debug artifacts:** `grep -rnE "console\.log|debugger|TODO|FIXME|print\(" src/` must return zero matches
6. **Confirm CI status** (if applicable): check GitHub Actions/CI for green status

**Verification gate:** Self-review checklist 100% complete. Diff <= 400 lines. `npm test` exits 0. No debug artifacts.

### Step 1: Complete the Self-Review Checklist

**Goal:** Catch 80% of issues before the reviewer sees the code.
**Expected output:** All checklist items confirmed.
**Tools to use:** `grep`, `read`, manual review

```markdown
## Self-Review Checklist

### Code Quality
- [ ] Code follows project style guide
- [ ] No commented-out code
- [ ] No debug logging left in
- [ ] Meaningful variable and function names
- [ ] Functions are focused and small (< 50 lines)

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

**Verification gate:** Every checkbox is ticked. No unchecked items remain.

### Step 2: Write the PR Description

**Goal:** Give reviewers the context they need to evaluate the change efficiently.
**Expected output:** Complete PR description.
**Tools to use:** `write`, `edit`

```markdown
## Pull Request: [Title]

### Summary
Brief description of what this PR does and why.

### Changes
- Change 1 (file: path/to/file)
- Change 2 (file: path/to/file)
- Change 3 (file: path/to/file)

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

**Must answer:** What changed? Why did it change? How can the reviewer verify it?

**Verification gate:** PR description answers "what changed", "why", and "how to verify". Related issues are linked.

### Step 3: Categorize the Review Focus

**Goal:** Tell reviewers which aspects need most attention.
**Expected output:** Review category annotations in the PR body.
**Tools to use:** Categorization

Annotate the PR or comment with focus areas:

```markdown
## Review Focus

🔴 **High Priority:** Architecture review of the new service layer (files: src/services/)
🟡 **Medium Priority:** Security review of the auth middleware changes
🟢 **Standard:** Everything else
```

**Review Categories:**

1. **Logic Review** — Does the code do what it's supposed to? Are edge cases handled?
2. **Architecture Review** — Is the design appropriate? Are responsibilities clear?
3. **Security Review** — Are there security vulnerabilities? Is sensitive data protected?
4. **Performance Review** — Are there performance concerns? N+1 queries?
5. **Testing Review** — Are tests comprehensive? Do they cover edge cases?

**Verification gate:** Review focus areas are communicated. Reviewers know which files need most scrutiny.

### Step 4: Submit the PR

**Goal:** Create the PR with proper assignment and labels.
**Expected output:** PR submitted, reviewers assigned.
**Tools to use:** `gh` CLI, GitHub UI

1. **Push the branch** if not already pushed
2. **Create the PR** via `gh pr create` or GitHub UI
3. **Assign reviewers** — check availability before assigning
4. **Add labels** — `needs-review`, `size/<small|medium|large>`, relevant categories
5. **Add milestone** if applicable
6. **Notify reviewers** with a brief ping

**Verification gate:** PR is created, reviewers are assigned, labels are applied. The PR status is "Ready for Review" (not Draft).

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Requesting review on a PR with failing CI | Reviewer must mentally filter test failures from logic issues; review is less effective | Fix CI first; re-request review only after all checks pass |
| Submitting a PR larger than 400 lines without splitting | Reviewer loses ability to hold the full diff in working memory; critical defects are reliably missed | Split the PR into logical chunks; if splitting is impossible, provide a guided walkthrough |
| Requesting review without a description of what changed and why | Reviewer must guess at intent from the diff alone; comments address the "how" rather than verifying the "why" | Add the missing description before assigning reviewers |
| Re-requesting review without summarising what changed since the last review | Reviewer must re-read the entire diff to find the changes; wastes their time and delays approval | Always summarise changes since last review when re-requesting |
| Assigning a reviewer without checking their availability | Review latency blocks the PR without any apparent reason | Check reviewer availability first; have a backup reviewer identified |
| Requesting review on a draft PR | Comments on draft code are wasted if the implementation changes before the PR is marked ready | Mark the PR as "Ready for Review" before requesting; use Draft only for early feedback |

## Verification

Before marking any review request as complete:

### Self-Verification Checklist

- [ ] Self-review completed with all pre-review items ticked
- [ ] All tests pass (`npm test` exits 0)
- [ ] Lint passes (`npm run lint` exits 0)
- [ ] No debug artifacts remain (`grep -rnE "console\.log|TODO|FIXME" src/` returns 0)
- [ ] PR description answers "what changed", "why", and "how to verify"
- [ ] PR diff <= 400 lines (or split with guided walkthrough)
- [ ] Related issues are linked
- [ ] Reviewers are assigned (with availability checked)
- [ ] PR status is "Ready for Review" (not Draft)

### Verification Commands

```bash
# Verify tests pass
rtk npm test

# Verify lint passes
rtk npm run lint

# Check PR diff size
git diff main...HEAD --stat | tail -1

# Check for debug artifacts
grep -rnE "console\.log|print\(|TODO|FIXME" src/ 2>/dev/null || echo "clean"

# Verify no hardcoded secrets
grep -rnE "password=|secret=|api_key=|api-key=" src/ --include="*.ts" --include="*.js" 2>/dev/null || echo "no secrets found"

# Verify PR description fields (if using gh)
gh pr view --json title,body
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Self-Review Completeness | All checklist items ticked | Complete missing items before assigning reviewers |
| PR Size | <= 400 lines diff | Split PR or provide guided walkthrough |
| CI Status | All required checks pass (green) | Fix issues, re-run CI, re-request only after green |
| Description Completeness | Answers "what changed", "why", "how to verify" | Add missing sections before proceeding |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Self-review and checklist | Haiku | 2K-4K |
| PR description writing | Sonnet | 3K-6K |
| PR with complex architecture decisions | Sonnet | 5K-10K |

### Parallelization
- **Self-review:** Single-threaded — each file reviewed sequentially
- **PR preparation:** Can run verification commands in parallel (`npm test` + `npm run lint` simultaneously)

### Context Budget
- **Expected context usage:** 4K-8K per review request
- **PR size management:** Diffs > 400 lines should be split to avoid overwhelming the reviewer's context

## Examples

### Example 1: Standard PR Submission

**Input:** "I've completed the notification preferences feature. Requesting review."

**Execution:**
1. **Pre-Flight:** Self-review checklist completed. `npm test` exits 0. Diff is 235 lines (under 400). No debug artifacts.
2. **PR Description:**
   ```markdown
   ## Pull Request: Add user notification preferences
   ### Summary
   Implements user notification preferences, allowing users to control which notifications they receive.
   ### Changes
   - Added NotificationPreferences model (src/models/preferences.ts)
   - Created /settings/notifications page (src/pages/settings/notifications.tsx)
   - Updated notification service to check preferences (src/services/notification.ts)
   ### Testing
   1. Create a new user
   2. Navigate to Settings > Notifications
   3. Toggle preferences and verify behavior matches
   ### Questions for Reviewers
   - Is the preference structure flexible enough for future types?
   ```
3. **Review Focus:** 🔴 Architecture review of the model design; 🟡 Security review of user input
4. **Submit:** `gh pr create --assignee @reviewer --label needs-review`

### Example 2: Edge Case — PR Exceeds 400 Lines (Preventing Violation)

**Input:** "Requesting review on the dashboard refactor. It's 800 lines."

**Correct response (blocking violation prevented):**
```
⚠️  PR is 800 lines — exceeds the 400-line limit.

I'll split this into two PRs:
1. **PR 1:** Data layer refactoring (320 lines) — the model and query changes
2. **PR 2:** UI components (480 lines) — the dashboard presentation changes

PR 2 is still >400 lines but cannot be split further without breaking coherence.
I'll provide a guided walkthrough:
- Files to focus on: src/components/DashboardGrid.tsx (the main structural change)
- Files you can skim: src/components/charts/* (mostly renamed props)
```

**Incorrect response:** Submitting the 800-line PR and expecting a meaningful review. The reviewer will rubber-stamp it because they cannot hold 800 lines in working memory.

### Example 3: Edge Case — Self-Review Catches Issue

**Input:** Ready to submit, but self-review checklist reveals a TODO comment left in the code.

**Correct response:**
```
Self-review flagged: TODO comment in src/services/notification.ts line 42.
- Fixed: Implemented the TODO (added rate limiting for notification dispatch)
- Re-ran tests: ✓ All pass
- Re-checked for artifacts: ✓ Clean
- Now ready for review
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Bundling feature, refactor, and bug fix in one PR | Reviewer cannot evaluate each change on its merits; the diff is confusing and likely too large | Separate into distinct PRs — one per concern |
| Submitting with "minor changes" not described in the PR | Unmentioned changes bypass reviewer scrutiny; the reviewer approved code they didn't know existed | Every change, however small, must be listed in the PR description |
| Requesting review without specifying what kind of review is needed | The reviewer doesn't know whether to focus on architecture, logic, security, or style | Prefix review focus with priority (🔴 architecture, 🟡 security, 🟢 style) |
| Requesting review at end of day Friday | Review sits in the reviewer's queue for 72+ hours; momentum is lost | Request review early in the week when reviewers are available |

## References

### Internal Dependencies
- `verification-loop` — Recommended before requesting review; ensures the code passes all quality gates
- `test-driven-development` — Optional; if TDD was used, the test coverage is already strong
- `finishing-a-development-branch` — Required downstream skill; handles the merge and branch cleanup after review
- `security-reviewer` — Optional but recommended for security-sensitive changes

### External Standards
- [Google's Code Review Developer Guide](https://google.github.io/eng-practices/review/) — Industry-standard review practices
- [SmartBear's Code Review Best Practices](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/) — PR size limits and review checklists
- [Conventional Commits](https://www.conventionalcommits.org/) — Commit message standard for PR titles

### Related Skills
- `receiving-code-review` — Complementary; handles the other side of the review exchange
- `code-polisher` — Can run a quality pass before the self-review checklist
- `finishing-a-development-branch` — Follows after review approval; merges and cleans up

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge cases (PR size violation, self-review catch), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; added review focus categorization |
| 1.0.0 | 2024-01-15 | Initial version — structured review flow with pre-review checklist and PR template |
