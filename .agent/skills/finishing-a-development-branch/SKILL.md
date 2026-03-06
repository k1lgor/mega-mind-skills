---
name: finishing-a-development-branch
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
# Run full test suite
npm test

# Run linting
npm run lint

# Build for production
npm run build

# Start app and verify manually
npm start
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
npm test

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
$ npm test
✓ All tests pass

$ npm run lint
✓ No issues

$ npm run build
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
