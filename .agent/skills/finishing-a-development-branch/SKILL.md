---
name: finishing-a-development-branch
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Clean branch wrap-up with workflow options. Use when a feature branch is complete and ready to merge.
triggers:
  - "merge this branch"
  - "finish this feature"
  - "wrap up this branch"
  - "ready to merge"
---

# Finishing a Development Branch Skill

## When to Use

- Feature development is complete
- All verifications have passed
- Ready to merge into main branch

## When NOT to Use

- Feature work is not complete — do not wrap up a branch mid-feature just to get a PR open
- Tests are still failing — fix them before starting the merge process
- The plan still has incomplete steps — finish executing the plan first
- There are uncommitted local changes that were not part of the intended feature scope

## Pre-Merge Checklist

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

## Branch Finishing Workflow

### Step 1: Final Verification

```bash
# Run full test suite (90% token savings)
rtk bun test (or rtknpm test)

# Run linting (84% token savings)
rtk bun run lint (or rtk npm run lint)

# Build for production
rtk proxy bun run build (or rtk npm run build)

# Start app and verify manually
rtk bun start (or rtk npm start)
```

### Step 2: Clean Up

```bash
# Ensure you're on the feature branch
git checkout feature/my-feature

# Rebase on latest main
git fetch origin
git rebase origin/main

# Resolve any conflicts
# Run tests again after rebase
rtk bun test (or rtk npm test)

# Clean up any debug code
# Remove console.logs, commented code, etc.
```

### Step 3: Update Documentation

```markdown
## CHANGELOG.md

### [1.2.0] - 2024-01-15

#### Added

- User notification preferences
- Export to PDF feature

#### Changed

- Improved dashboard performance

#### Fixed

- Login timeout issue
```

### Step 4: Create Pull Request

```markdown
## Pull Request Template

### What does this PR do?

Brief description of changes

### Why is this change needed?

Business justification

### How was this tested?

- Unit tests
- Integration tests
- Manual testing steps

### Screenshots

Before/After if applicable

### Breaking Changes

List any breaking changes

### Checklist

- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
```

### Step 5: Merge Options

#### Option A: Squash and Merge

Best for: Feature branches with messy commit history

```bash
# Via GitHub UI: "Squash and merge"
# Creates one clean commit on main
```

#### Option B: Merge Commit

Best for: Preserving full history

```bash
git checkout main
git merge --no-ff feature/my-feature
git push origin main
```

#### Option C: Rebase and Merge

Best for: Clean linear history

```bash
git checkout main
git merge --ff-only feature/my-feature
git push origin main
```

### Step 6: Post-Merge Cleanup

```bash
# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature

# Update local main
git checkout main
git pull origin main

# Prune deleted branches
git fetch --prune
```

## Example Workflow

```bash
# 1. Final verification
$ rtk bun test (or rtk npm test)
✓ All tests pass

$ rtk bun run lint (or rtk npm run lint)
✓ No issues

$ rtk bun run build (or rtk npm run build)
✓ Build successful

# 2. Rebase on main
$ git checkout feature/user-preferences
$ git fetch origin
$ git rebase origin/main
✓ No conflicts

# 3. Push and create PR
$ git push origin feature/user-preferences
# Create PR via GitHub

# 4. After approval, merge
# Via GitHub UI: "Squash and merge"

# 5. Cleanup
$ git checkout main
$ git pull origin main
$ git branch -d feature/user-preferences
$ git push origin --delete feature/user-preferences
```

## Merge Checklist

```markdown
## Merge Checklist

### Before Merge

- [ ] All approvals received
- [ ] All conversations resolved
- [ ] CI/CD passes
- [ ] Branch up to date with main

### During Merge

- [ ] Correct merge method chosen
- [ ] Commit message is clear
- [ ] Any required tags/labels applied

### After Merge

- [ ] Branch deleted
- [ ] Local environment updated
- [ ] Team notified (if needed)
- [ ] Deployment triggered (if applicable)
```

## Tips

- Don't merge your own PR without review (except emergencies)
- Keep branches short-lived (days, not weeks)
- Rebase frequently to avoid large conflicts
- Write good commit messages for future reference
- Delete branches promptly after merge

## Failure Modes

| Failure                                                                    | Cause                                                                        | Recovery                                                                                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Branch merged without CI passing because merge done manually               | Branch protection not enforced; developer bypasses merge queue               | Enable required status checks on the base branch; make CI a required check before merge is possible                             |
| PR merged with unresolved review comments                                  | Author dismissed comments without addressing them; reviewer not re-requested | Require all comments to be resolved before merge; use GitHub's "require conversation resolution" setting                        |
| Release notes omitted, leaving next developer unable to understand changes | Release notes treated as optional; skipped under time pressure               | Add release notes to the PR template as a required field; block merge if the section is empty                                   |
| Branch not deleted after merge, accumulating stale branch noise            | No automatic branch deletion configured; developer forgets                   | Enable "automatically delete head branches" in repo settings; add branch cleanup to the merge checklist                         |
| Squash-merge loses individual commit history needed for bisect debugging   | Squash-merge used by default; team relies on git bisect for debugging        | Use merge commit or rebase-merge when individual commits carry diagnostic value; document the merge strategy in CONTRIBUTING.md |

## Anti-Patterns

- Never merge a branch with failing CI because a broken build on the base branch blocks all other developers and the fix adds another unreviewed commit to the history.
- Never dismiss review comments without addressing them because unaddressed comments represent unresolved concerns that will resurface as bugs or tech debt.
- Never skip release notes because the next developer to diagnose a production issue needs to know what changed and when, and git log alone does not provide that context.
- Never leave stale branches after merge because accumulated branches make it impossible to distinguish active from completed work and pollute branch listings.
- Never squash-merge a branch with commits that have individual diagnostic value because squashing destroys the ability to bisect a regression to a specific commit.
- Never merge without a passing CI run even for "trivial" changes because trivial changes have caused outages when they invalidate assumptions made by other parts of the system.

## Self-Verification Checklist

- [ ] All tests pass on the branch: `bun test` or `npm test` exits 0 with 0 failing tests
- [ ] PR description includes what changed, why, and how to test it
- [ ] Branch is rebased on latest main: `git log --oneline main..HEAD` count matches expected commits only
      grep -rnE "console\.log|debugger|TODO|FIXME|print("
- [ ] At least one reviewer has approved (not self-merged except emergencies)
- [ ] Branch will be deleted after merge: `git branch -d <branch>` exits 0 post-merge
- [ ] `continuous-learning-v2` has been queued: `grep -c "continuous-learning" docs/plans/task.md` returns > 0

## Success Criteria

This skill is complete when: 1) all CI checks pass on the PR, 2) at least one reviewer has approved, and 3) the branch is merged and deleted — leaving main in a clean, deployable state.
