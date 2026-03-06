---
name: using-git-worktrees
description: Parallel branch management with Git worktrees. Use when working on multiple features simultaneously.
triggers:
  - "work on multiple features"
  - "parallel development"
  - "git worktree"
  - "context switching"
---

# Using Git Worktrees Skill

## When to Use

- Working on multiple features simultaneously
- Need to context-switch without stashing
- Running long tests on one branch while working on another
- Reviewing PRs while working on a feature

## What Are Git Worktrees?

Git worktrees allow you to have multiple working directories from the same repository, each checked out to a different branch.

```
main-repo/           # Main working directory (main branch)
├── src/
├── tests/
└── ...

worktrees/
├── feature-a/       # Worktree for feature-a branch
└── feature-b/       # Worktree for feature-b branch
```

## Basic Commands

### Create a Worktree

```bash
# Create new branch in new worktree
git worktree add ../my-feature -b feature/my-feature

# Create worktree from existing branch
git worktree add ../existing-feature feature/existing-feature

# Create worktree for a PR
git worktree add ../pr-123 pr/123
```

### List Worktrees

```bash
git worktree list

# Output:
# /path/to/main-repo        abc1234 [main]
# /path/to/my-feature       def5678 [feature/my-feature]
# /path/to/existing-feature ghi9012 [feature/existing-feature]
```

### Remove a Worktree

```bash
# Remove worktree after branch is merged
git worktree remove ../my-feature

# Force remove if untracked files
git worktree remove --force ../my-feature
```

## Workflow Patterns

### Pattern 1: Hotfix While Developing

```bash
# You're working on feature-A
cd ~/projects/my-app

# Urgent bug comes in - create worktree for hotfix
git worktree add ../my-app-hotfix -b hotfix/urgent-fix

# Switch to hotfix
cd ../my-app-hotfix

# Make fix, commit, push, create PR
git add .
git commit -m "Fix urgent bug"
git push origin hotfix/urgent-fix

# Return to feature work
cd ../my-app

# Clean up after hotfix merges
git worktree remove ../my-app-hotfix
```

### Pattern 2: PR Review While Developing

```bash
# Create worktree to review PR
git worktree add ../pr-review pr/123

cd ../pr-review

# Run tests, review code
npm test
npm run lint

# Return to your work
cd ../my-app

# Clean up
git worktree remove ../pr-review
```

### Pattern 3: Parallel Features

```bash
# Main repo: feature-a
cd ~/projects/my-app
# Working on feature A...

# Create worktree for feature-b
git worktree add ../my-app-feature-b -b feature/b

# Create another for spike
git worktree add ../my-app-spike -b spike/refactor-auth

# Can now switch between contexts instantly
cd ../my-app-feature-b  # Work on feature B
cd ../my-app-spike      # Work on spike
cd ../my-app            # Back to feature A
```

## Worktree Directory Structure

```
project/
├── .git/                    # Git directory
├── src/                     # Main branch files
└── ...

# Worktrees (can be anywhere)
../project-feature-a/
├── .git                     # File pointing to main .git
├── src/                     # Feature-a branch files
└── ...

../project-feature-b/
├── .git                     # File pointing to main .git
├── src/                     # Feature-b branch files
└── ...
```

## Tips for Managing Worktrees

### Naming Convention

```bash
# Include project name and branch name
git worktree add ../myapp-feature-auth feature/auth
git worktree add ../myapp-hotfix-123 hotfix/issue-123
```

### Shared Dependencies

```bash
# If using Node.js, each worktree needs its own node_modules
cd ../myapp-feature-auth
npm install

# Or use workspaces for shared dependencies
```

### IDE Setup

```bash
# Each worktree can be opened in its own IDE window
code ../myapp-feature-auth
code ../myapp-feature-b

# Or use multi-root workspace
```

## Best Practices

1. **Clean up after merging** - Remove worktrees when branches are deleted
2. **Use descriptive names** - Include project and branch in worktree name
3. **Keep worktrees nearby** - Use consistent parent directory
4. **Document active worktrees** - Keep a note of what's where

## Common Issues

### Issue: "already checked out"

```bash
$ git worktree add ../feature feature/my-feature
fatal: 'feature/my-feature' is already checked out at '/path/to/main'

# Solution: First detach HEAD in main repo
git checkout --detach
git worktree add ../feature feature/my-feature
```

### Issue: Untracked Files

```bash
$ git worktree remove ../feature
fatal: cannot remove a worktree with untracked files

# Solution: Force remove or clean first
git worktree remove --force ../feature
# or
cd ../feature && git clean -fd
```

## Worktree Management Script

```bash
#!/bin/bash
# worktree-manager.sh

# Create worktree
create_worktree() {
    local branch=$1
    local name=$(basename "$PWD")-$branch
    git worktree add ../$name -b $branch
    echo "Created worktree at ../$name"
}

# List worktrees
list_worktrees() {
    echo "Active worktrees:"
    git worktree list
}

# Clean merged worktrees
clean_merged() {
    for wt in $(git worktree list --porcelain | grep worktree | cut -d' ' -f2); do
        cd $wt
        branch=$(git rev-parse --abbrev-ref HEAD)
        if git branch --merged main | grep -q $branch; then
            echo "Removing merged worktree: $wt ($branch)"
            git worktree remove $wt
        fi
    done
}
```
