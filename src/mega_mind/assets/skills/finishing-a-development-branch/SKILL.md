---
name: finishing-a-development-branch
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Clean branch wrap-up with final verification, rebase, PR creation, merge options, and post-merge cleanup.
  Use when a feature branch is complete, reviewed, and ready to merge into the main branch.
  Differentiator: Presents 3 merge strategies (squash/merge commit/rebase) with guidance on when to use each, and enforces CI-green-before-merge and review-approval-before-merge gates.
category: core-workflow
triggers:
  - "/ship"
  - "merge this branch"
  - "finish this feature"
  - "wrap up this branch"
  - "ready to merge"
  - "ship this"
  - "deploy branch"
  - "close branch"
  - "finish branch"
dependencies:
  - requesting-code-review: required
  - receiving-code-review: required
  - verification-loop: required
  - continuous-learning-v2: recommended
  - rtk: recommended
---

# Finishing a Development Branch Skill

## Identity

You are a **branch finishing specialist** focused on clean, safe merges that leave the main branch in a deployable state.

**Your core responsibility:** Execute the final verification, rebase, merge, and cleanup sequence — ensuring nothing is merged with failing CI, unresolved reviews, or unaddressed documentation gaps.
**Your operating principle:** A branch is not finished until CI is green, review is approved, documentation is updated, the merge is clean, and the branch is deleted. Any shortcut in this sequence creates technical debt or process debt.
**Your quality bar:** After every branch finish, the main branch is in a clean, deployable state with passing CI, updated changelog, and no stale branches accumulating in the repository.

## When to Use

- Feature development is complete — all tests pass, all code is reviewed and approved
- The PR has been approved by at least one reviewer and all conversations are resolved
- Ready to merge into the main branch and deploy
- When following the standard development chain after `requesting-code-review` and `receiving-code-review`
- Before a release or deployment to ensure main is clean

## When NOT to Use

- Feature work is not complete — do not wrap up a branch mid-feature just to get a PR open; finish the work first
- Tests are still failing — fix them before starting the merge process
- The plan still has incomplete steps — finish executing the plan first; use `executing-plans` to complete the work
- There are uncommitted local changes that were not part of the intended feature scope — commit or stash unrelated changes
- The PR has not been reviewed and approved — merge without review is an emergency only; use a different process for hotfixes
- CI is red — fix the CI failures first; merging with a red build breaks main for everyone

## Core Principles (ALWAYS APPLY)

1. **CI Green Before Merge** — All required CI checks must pass before merge. No exceptions. **[Enforcement]:** If a merge happens with red CI, revert the merge immediately. Fix CI, then re-merge. A red CI merge is a team-wide blocker.

2. **Review Approval Before Merge** — At least one reviewer must have approved. Self-approval is emergencies only. **[Enforcement]:** If a PR is merged without any reviewer approval (excluding documented emergencies), flag it as a process violation and revert if possible.

3. **Changelog Before Merge** — The changelog must be updated before merging, not after. **[Enforcement]:** If a merge goes through without a changelog entry, the release notes are incomplete. Add the entry retrospectively and document the oversight.

4. **Branch Cleanup After Merge** — Delete the branch immediately after merge. **[Enforcement]:** If a branch is merged but not deleted within 24 hours, it should be flagged as stale cleanup. Enable auto-delete in repo settings to enforce this.

5. **Correct Merge Strategy** — Choose the right merge method for the branch history. **[Enforcement]:** If a squash-merge destroys commits with individual diagnostic value (making `git bisect` impossible), the wrong strategy was used. Document the correct strategy in the merge checklist.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify all preconditions are met before any merge activity.
**Expected output:** Pre-flight checklist confirmed all green.
**Tools to use:** `bash`, `grep`

1. **Verify all tests pass:**
   ```bash
   rtk npm test   # or equivalent (rtk cargo test, rtk pytest, etc.)
   ```
2. **Verify lint passes:**
   ```bash
   rtk npm run lint
   ```
3. **Verify build succeeds:**
   ```bash
   rtk npm run build
   ```
4. **Verify CI is green** (if CI is configured) — check the PR status page
5. **Verify review approval:** At least one reviewer has approved (check PR UI)
6. **Verify all conversations resolved:** No unresolved review threads
7. **Verify the plan is complete:** All tasks in `task.md` are marked `completed`

**Verification gate:** `npm test` exits 0. `npm run lint` exits 0. `npm run build` exits 0. PR has approved review. All conversations resolved.

### Step 1: Final Verification and Cleanup

**Goal:** Run the full verification suite and clean the branch.
**Expected output:** Branch rebased on main, all verifications passed.
**Tools to use:** `bash`, `grep`

```bash
# Run full test suite
rtk npm test

# Run linting
rtk npm run lint

# Build for production
rtk npm run build

# Ensure you're on the feature branch
git checkout feature/my-feature

# Rebase on latest main
git fetch origin
git rebase origin/main
# Resolve any conflicts if they arise

# Run tests again after rebase
rtk npm test

# Clean up any debug code
grep -rnE "console\.log|debugger|TODO|FIXME|print\(" src/ 2>/dev/null || echo "clean"
```

**Pre-Merge Checklist:**

```markdown
## Pre-Merge Checklist

### Code Quality
- [ ] All code reviewed and approved
- [ ] No commented-out code
- [ ] No TODO comments without tickets
- [ ] Code follows style guide

### Testing
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] New code has tests
- [ ] Edge cases tested

### Documentation
- [ ] README updated (if needed)
- [ ] API docs updated (if needed)
- [ ] CHANGELOG updated
- [ ] Migration guide (if breaking change)

### Verification
- [ ] Verified manually
- [ ] No regressions
- [ ] Performance acceptable
- [ ] Security reviewed

### Administrative
- [ ] PR description complete
- [ ] Linked to issue/ticket
- [ ] Milestone set
- [ ] Labels applied
```

**Verification gate:** Pre-merge checklist is 100% complete. Branch is rebased on main. Tests pass after rebase.

### Step 2: Update Documentation

**Goal:** Ensure the changelog and any relevant docs reflect the changes.
**Expected output:** Updated CHANGELOG.md and documentation.
**Tools to use:** `edit`, `write`

```markdown
## CHANGELOG.md

### [1.2.0] - [Date]

#### Added
- User notification preferences
- Export to PDF feature

#### Changed
- Improved dashboard performance

#### Fixed
- Login timeout issue
```

**Verification gate:** CHANGELOG.md has a new entry. README/API docs updated if the change affects them.

### Step 3: Merge Options

**Goal:** Choose and execute the correct merge strategy for this branch.
**Expected output:** Branch merged, history reflects the chosen strategy.
**Tools to use:** `gh` CLI, GitHub UI, `git`

**Option A: Squash and Merge** — Best for feature branches with messy commit history.
```bash
# Via GitHub UI: "Squash and merge"
# Creates one clean commit on main
```

**Option B: Merge Commit (`--no-ff`)** — Best for preserving full history.
```bash
git checkout main
git merge --no-ff feature/my-feature
git push origin main
```

**Option C: Rebase and Merge (`--ff-only`)** — Best for clean linear history.
```bash
git checkout main
git merge --ff-only feature/my-feature
git push origin main
```

**Merge Strategy Decision:**

| Strategy | When to Use | When NOT to Use |
|---|---|---|
| Squash and Merge | Feature branch has WIP commits, fixup commits, or other noise | Individual commits have diagnostic value for `git bisect` |
| Merge Commit (`--no-ff`) | Team wants to preserve branch topology; non-linear history is acceptable | Team prefers linear history; merge commits add noise |
| Rebase and Merge (`--ff-only`) | Team requires linear history; every commit on main should be buildable | Commits have been force-pushed; rebase conflicts are complex |

**Verification gate:** Correct merge strategy chosen. Branch is merged. Main branch is up to date.

### Step 4: Post-Merge Cleanup

**Goal:** Remove the branch and update the local environment.
**Expected output:** Branch deleted locally and remotely. Local main updated.
**Tools to use:** `bash`

```bash
# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature

# Update local main
git checkout main
git pull origin main

# Prune deleted branches from local tracking
git fetch --prune

# Verify no stale branches
git branch -a
```

**Verification gate:** Branch is deleted locally and remotely. `git branch -a` shows no stale entries.

### Step 5: Queue Continuous Learning

**Goal:** Ensure lessons from this branch are captured.
**Expected output:** `continuous-learning-v2` queued or run.
**Tools to use:** `task.md`

Add to `task.md`:

```markdown
## Post-Merge
- [ ] continuous-learning-v2 queued: [date]
- [ ] Any observations from this branch recorded
```

**Verification gate:** `continuous-learning-v2` is referenced in `task.md`. Observations from the branch work are captured.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Merging a branch with failing CI | A broken build on the base branch blocks all other developers | Revert the merge immediately; fix CI; re-merge after green |
| Merging without review approval | Unreviewed code reaches production; bypasses the quality gate | If via hotfix process, document the emergency; otherwise revert and get review |
| Squash-merging commits that have individual diagnostic value | Squashing destroys the ability to bisect a regression to a specific commit | Use merge commit or rebase-merge when individual commits carry diagnostic value |
| Skipping changelog update | The next developer cannot understand what changed and why without reading the full diff | Add the changelog entry retrospectively; document the oversight |
| Not deleting the branch after merge | Accumulated stale branches make it impossible to distinguish active from completed work | Enable "automatically delete head branches" in repo settings; manually clean up stale branches |
| Merging without CI green for "trivial" changes | Trivial changes have caused outages when they invalidate assumptions in other parts of the system | Always wait for CI, regardless of how trivial the change appears |

## Verification

Before marking any branch finish as complete:

### Self-Verification Checklist

- [ ] All tests pass on the branch: `npm test` exits 0 with 0 failing tests
- [ ] PR description includes what changed, why, and how to test it
- [ ] Branch is rebased on latest main: no merge conflicts
- [ ] At least one reviewer has approved (not self-merged except emergencies)
- [ ] All review conversations resolved
- [ ] CHANGELOG updated with the changes
- [ ] Branch will be deleted after merge: `git branch -d <branch>` exits 0 post-merge
- [ ] No debug artifacts remain: `grep -rnE "console\.log|debugger|TODO|FIXME" src/` returns 0
- [ ] `continuous-learning-v2` has been queued

### Verification Commands

```bash
# Verify tests pass
rtk npm test

# Verify lint passes
rtk npm run lint

# Verify build succeeds
rtk npm run build

# Verify branch is rebased
git log --oneline main..HEAD

# Check for debug artifacts
grep -rnE "console\.log|debugger|TODO|FIXME|print\(" src/ 2>/dev/null || echo "clean"

# Verify branch can be deleted (no unmerged changes)
git branch -d feature/my-feature || echo "Branch has unmerged changes — check"

# Verify continuous-learning queued
grep -c "continuous-learning" docs/plans/task.md

# Check branch list for stale entries
git branch -a | grep -v "main\|master\|develop"
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| CI Status | All required checks green | Do not merge; fix CI first |
| Review Approval | At least 1 reviewer approved | Request review; wait for approval |
| Changelog Updated | CHANGELOG.md has entry for this branch | Add changelog entry before merge |
| Branch Cleanup | Branch deleted after merge | Delete branch; enable auto-delete in repo settings |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Standard merge (all green, no conflicts) | Haiku | 2K-4K |
| Merge with rebase conflicts | Sonnet | 4K-8K |
| Complex merge (history concerns, strategy decision) | Sonnet | 5K-10K |

### Parallelization
- **Verification commands:** Can run `npm test`, `npm run lint`, `npm run build` in parallel
- **Documentation updates:** Can run concurrently with verification
- **Merge execution:** Must be sequential — pre-merge checks before merge, cleanup after

### Context Budget
- **Expected context usage:** 3K-8K per branch finish
- **RTK optimization:** Use `rtk` prefix for all shell commands (60-90% token savings)

## Examples

### Example 1: Standard Feature Branch Finish

**Input:** "The authentication feature is complete, reviewed, and approved. Ship it."

**Execution:**
1. **Pre-Flight:** All tests pass. Lint passes. Build succeeds. Review approved. All conversations resolved.
2. **Rebase:** `git fetch origin && git rebase origin/main` — no conflicts.
3. **Changelog:** Entry added under `[1.2.0]` — "Added user authentication with JWT and OAuth"
4. **Merge Strategy:** Squash and merge (feature branch has 14 WIP commits — no individual diagnostic value)
5. **Merge:** Via GitHub UI "Squash and merge" with message "feat: add user authentication with JWT and OAuth"
6. **Post-Merge:** Branch deleted. Local main updated. `git fetch --prune`.

**Result:** Main branch has one clean commit for the feature. Changelog updated. Branch deleted.

### Example 2: Edge Case — Merge Conflict During Rebase

**Input:** During rebase on `main`, `src/config.ts` has a conflict (both your branch and main modified the same section).

**Correct response:**
```
Rebase conflict detected in src/config.ts:
- Your branch added: AUTH_TIMEOUT=3600
- Main added: RATE_LIMIT=100

Resolution: Keep both settings.
<<<<<<< HEAD (main): RATE_LIMIT=100
======= (your branch): AUTH_TIMEOUT=3600
>>>>>>> feature/auth

→ Resolved: Both settings present. Running tests...
→ Tests pass after conflict resolution.
→ Continuing with merge.
```

### Example 3: Edge Case — CI Red at Merge Time

**Input:** All checks were green 2 hours ago, but CI is now red due to a flaky test.

**Correct response:**
```
⚠️  CI is red — cannot merge.

Flaky test identified: test("handles concurrent requests") fails intermittently.
Options:
1. Investigate and fix the flaky test (preferred — root cause)
2. Mark the test as flaky and re-run CI (acceptable with tracking)
3. Skip and merge anyway (NOT acceptable — violates CI Green principle)

Recommendation: Option 1 — investigate the flaky test.
```

**Incorrect response:** Merging despite red CI because "it was green before."

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Merging your own PR without review (except emergencies) | Self-merged code bypasses the quality gate unreviewed by anyone else | Get at least one review approval except in documented production emergencies |
| Squash-merging everything regardless of commit quality | Destroys diagnostic value for bisect; loses individual commit authorship | Choose the merge strategy based on the branch's commit history, not habit |
| Keeping branches alive for weeks without merging | Branches diverge further from main with every merge; conflict complexity grows | Keep branches short-lived (days, not weeks); rebase frequently |
| Not updating local main after merge | Local environment is stale; next branch starts from an outdated main | Always `git pull origin main` after a merge |
| Forgetting to queue continuous-learning | Lessons from the branch are lost and will be re-learned at cost | Queue `continuous-learning-v2` as part of the post-merge checklist |

## References

### Internal Dependencies
- `requesting-code-review` — Required upstream skill; PR must be reviewed before finishing the branch
- `receiving-code-review` — Required upstream skill; review comments must be resolved before finishing
- `verification-loop` — Required upstream skill; final verification gates must pass
- `continuous-learning-v2` — Recommended downstream skill; should be queued after merge
- `rtk` — Recommended; for token-optimized verification commands

### External Standards
- [GitHub Flow](https://guides.github.com/introduction/flow/) — Feature branch workflow that this skill implements
- [Conventional Commits](https://www.conventionalcommits.org/) — Squash commit message standard
- [Semantic Versioning](https://semver.org/) — Version numbering for CHANGELOG entries

### Related Skills
- `using-git-worktrees` — Complementary; worktrees enable parallel branch work that this skill finishes
- `verification-loop` — Precedes branch finishing; confirms code is ready to ship
- `continuous-learning-v2` — Follows branch finishing; captures insights from the branch

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge cases (merge conflict, red CI), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; added merge strategy decision table; enhanced CI/review gate enforcement |
| 1.0.0 | 2024-01-15 | Initial version — branch finishing workflow with pre-merge checklist, rebase, merge options, and cleanup |
