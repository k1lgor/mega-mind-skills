---
name: using-git-worktrees
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
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

## When NOT to Use

- Single-branch work with no concurrent development — worktrees add overhead with no benefit
- When a quick stash is sufficient — if you need to context-switch for less than 5 minutes, `git stash` is lower friction
- When disk space or Node.js/dependency install times are a concern — each worktree needs its own `node_modules`
- On shared machines or CI environments where worktree paths are not predictable

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

# Make fix, then commit using the finishing-a-development-branch skill
# (Do NOT run `git add` or `git commit` directly — use the skill)
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
rtk bun test (or rtk npm test)
rtk bun run lint (or rtk npm run lint)

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
rtk bun install (or rtk npm install)

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

## Anti-Patterns

- Never create a worktree on a branch that is already checked out elsewhere because git will refuse the operation with a "fatal: already checked out" error, and working around it by detaching HEAD in the wrong directory corrupts your active working state.
- Never leave worktrees orphaned after their branch is merged because each orphaned worktree consumes disk space and appears in `git worktree list`, making it impossible to tell which worktrees represent active work.
- Never run package install commands in one worktree expecting them to take effect in another because each worktree has an independent `node_modules` directory; packages installed in worktree A are not available in worktree B.
- Never share a build output directory between worktrees because concurrent builds from two worktrees writing to the same output directory produce interleaved, corrupted artifacts that neither worktree can reliably use.
- Never create a worktree inside the main repository directory because a worktree nested inside the repo's own working tree is picked up by git as untracked content, creating confusing `git status` output and potential recursive git operations.
- Never forget to `git worktree prune` after removing worktree directories manually because manually deleted worktree directories leave stale entries in the git worktree registry, causing `git worktree list` to show paths that no longer exist.

## Failure Modes

| Failure                                                                  | Cause                                                                                                          | Recovery                                                                                                                                     |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Worktree left behind after branch deleted, consuming disk space silently | Developer deletes remote branch and closes the PR but never runs `git worktree remove`                         | Run `git worktree prune` after each branch deletion; audit with `git worktree list` to confirm no stale entries remain                       |
| Same branch checked out in two worktrees, causing lock conflict          | Developer adds a new worktree for a branch that is already checked out in the main repo                        | Before adding a worktree, run `git worktree list` to confirm the branch is not already checked out; detach HEAD in the source worktree first |
| Worktree path contains spaces, breaking shell scripts referencing it     | Worktree directory named "my feature branch" with spaces; unquoted path in scripts fails                       | Always name worktrees with hyphens not spaces (e.g., `my-feature-branch`); audit existing worktree paths with `git worktree list`            |
| Shared `.env` file modified in worktree, affecting main checkout         | `.env` is not gitignored and is shared by symlink or located at project root accessible from all worktrees     | Add `.env` to `.gitignore`; use per-worktree `.env.local` files; never symlink shared mutable config files across worktrees                  |
| IDE opens wrong worktree root, running tests against stale code          | IDE session restored from previous project root; developer edits files in the wrong directory without noticing | Verify the active directory with `git branch --show-current` before running tests; use per-worktree IDE windows, not shared sessions         |

## Self-Verification Checklist

- [ ] `git worktree list` shows only expected worktrees — count matches the number of active feature branches being worked on
- [ ] All worktrees reference existing branches — `git worktree list` shows no entries with `(detached HEAD)` or deleted branch names
- [ ] No shared mutable files (`.env`, `node_modules`) symlinked across worktrees — `ls -la` in each worktree root shows no symlinks to parent directories
- [ ] Worktree directory names follow the `<project>-<branch>` convention (e.g., `myapp-feature-auth`)
- [ ] Worktrees for merged branches have been removed (`git worktree remove` run and `git worktree prune` confirms 0 stale entries)
- [ ] `git worktree prune` exits 0 with 0 pruned entries: all listed worktrees have valid directory paths
- [ ] No shared lock files between worktrees: `ls -la .git/index.lock` returns "No such file" in all worktrees (exits non-zero)

## Success Criteria

This skill is complete when: 1) Each active feature or context has its own worktree with a descriptive name, fully installed dependencies, and the correct branch checked out. 2) Worktrees for completed/merged branches are cleaned up promptly. 3) `git worktree list` reflects only the worktrees currently in active use.

```

```
