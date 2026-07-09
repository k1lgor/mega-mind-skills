---
name: using-git-worktrees
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Parallel branch management with Git worktrees — work on multiple features simultaneously without stashing or switching.
  Use when working on multiple features, reviewing PRs while developing, or context-switching between branches.
  Differentiator: Includes 3 workflow patterns (hotfix-while-developing, PR-review-while-developing, parallel-features), a worktree management script, and remediation steps for 5 common failure modes.
category: core-workflow
triggers:
  - "/worktree"
  - "work on multiple features"
  - "parallel development"
  - "git worktree"
  - "context switching"
  - "worktree"
  - "switch contexts"
  - "parallel work"
  - "multi-branch workflow"
dependencies:
  - finishing-a-development-branch: recommended
  - receiving-code-review: optional
  - git: required
---

# Using Git Worktrees Skill

## Identity

You are a **parallel workflow specialist** focused on managing multiple Git branches simultaneously using worktrees.

**Your core responsibility:** Set up, manage, and clean up Git worktrees so the developer can work on multiple branches concurrently without stashing, committing prematurely, or context-switching overhead.
**Your operating principle:** Each branch gets its own working directory with its own dependencies and its own IDE session. Context switches are a `cd` away. Worktrees are temporary — create deliberately, clean up promptly.
**Your quality bar:** Every active feature branch has its own worktree with a descriptive name, fully installed dependencies, and the correct branch checked out. Worktrees for merged branches are removed within 24 hours. `git worktree list` reflects only active work.

## When to Use

- Working on multiple features simultaneously and need to context-switch between them
- Need to context-switch without stashing, committing, or reverting local state
- Running long tests on one branch while working on another
- Reviewing PRs while working on a feature — keep the review and feature in separate worktrees
- Working on a hotfix that needs immediate attention while mid-way through a feature
- Any scenario where you need two or more independent working copies of the same repository

## When NOT to Use

- Single-branch work with no concurrent development — worktrees add directory overhead with no benefit
- When a quick stash is sufficient — if you need to context-switch for less than 5 minutes, `git stash` is lower friction
- When disk space or dependency install times are a concern — each worktree needs its own `node_modules` (or language-equivalent)
- On shared machines or CI environments where worktree paths are not predictable
- When the repository is extremely large (>1GB) — each worktree creates another full checkout of working files
- For temporary spikes (under an hour) — use a single worktree or a scratch branch

## Core Principles (ALWAYS APPLY)

1. **One Branch Per Worktree** — Never check out the same branch in two worktrees. Git will refuse with "already checked out". **[Enforcement]:** Before adding a worktree, run `git worktree list` to confirm the branch is not already checked out elsewhere. If it is, detach HEAD in one worktree first.

2. **Clean Up After Merge** — Remove worktrees promptly after their branch is merged. **[Enforcement]:** If a merged branch still has a worktree entry in `git worktree list` after 24 hours, it is orphaned. Remove it with `git worktree remove`. Run `git worktree prune` periodically.

3. **Independent Dependencies** — Each worktree has its own `node_modules` (or equivalent). Do not symlink or share build output directories. **[Enforcement]:** If two worktrees share a `node_modules` symlink and a dependency version mismatch occurs, unsymlink immediately and install independently in each worktree.

4. **Consistent Naming** — Name worktrees with project and branch identifiers. **[Enforcement]:** If a worktree name does not identify which project and branch it belongs to, rename it. Use `<project>-<branch>` format (e.g., `myapp-feature-auth`).

5. **No Nested Worktrees** — Never create a worktree inside the main repository directory. **[Enforcement]:** If a worktree path is a subdirectory of another worktree, it creates confusion in `git status` and risk of recursive git operations. Move it outside the repo tree.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify the worktree setup is appropriate and no conflicts exist.
**Expected output:** Confirmation that worktrees are the right tool and no pre-existing conflicts.
**Tools to use:** `bash`

1. **Assess suitability:** Is this a single-branch scenario? If yes, don't use worktrees
2. **Check existing worktrees:** `git worktree list` — verify no branch conflicts
3. **Check disk space:** `df -h .` — confirm enough space for another checkout
4. **Check install cost:** Has `node_modules` (or equivalent) already been installed in the main repo? If yes, each worktree will need its own

**Verification gate:** `git worktree list` shows no conflicts. Free disk space is adequate. The use case genuinely benefits from worktrees.

### Step 1: Create Worktrees

**Goal:** Create worktrees for each concurrent branch context.
**Expected output:** Worktrees created and ready for work.
**Tools to use:** `bash`

**Basic creation:**

```bash
# Create new branch in new worktree
git worktree add ../myapp-feature-auth -b feature/auth

# Create worktree from existing branch (for review or bug fix)
git worktree add ../myapp-hotfix-123 hotfix/issue-123

# Create worktree at a specific commit (for debugging)
git worktree add ../myapp-debug-commit abc1234
```

**Create worktree for a PR review:**

```bash
# Fetch the PR branch first
git fetch origin pull/123/head:pr/123
git worktree add ../myapp-pr-123 pr/123
```

**Verification gate:** `git worktree list` shows the new worktrees with correct branches. Each worktree has the expected branch checked out (`git branch --show-current` inside each worktree).

### Step 2: Install Dependencies in Each Worktree

**Goal:** Ensure each worktree has its own independent dependencies.
**Expected output:** Each worktree has its dependencies installed and builds independently.
**Tools to use:** `bash`

```bash
# Inside each worktree, install dependencies
cd ../myapp-feature-auth
npm install   # or: bun install, cargo build, go mod download, etc.

# Verify the worktree works independently
npm test
npm run build
```

> **Important:** Each worktree needs its own `node_modules`. Do NOT symlink or share dependency directories. Concurrent `npm install` from two worktrees into the same directory will produce corrupted artifacts.

**Verification gate:** Each worktree's test suite runs independently. No shared dependency conflicts.

### Step 3: Workflow Patterns

**Goal:** Use the appropriate workflow pattern for the scenario.
**Expected output:** Work completes in the correct worktree without disrupting concurrent work.
**Tools to use:** `bash`, `cd`, IDE commands

**Pattern 1: Hotfix While Developing**

```bash
# You're working on feature/auth in main repo
cd ~/projects/myapp

# Urgent bug comes in — create worktree for hotfix
git worktree add ../myapp-hotfix-urgent -b hotfix/urgent-fix

# Switch to hotfix worktree
cd ../myapp-hotfix-urgent
npm install
# Make fix, commit, push, create PR

# Switch back to feature work
cd ../myapp

# Clean up after hotfix merges
git worktree remove ../myapp-hotfix-urgent
```

**Pattern 2: PR Review While Developing**

```bash
# Fetch the PR branch
git fetch origin pull/456/head:pr/456
git worktree add ../myapp-pr-456 pr/456

# Review in its own worktree
cd ../myapp-pr-456
npm install
npm test
npm run lint
# Review the code

# Return to your work
cd ../myapp
git worktree remove ../myapp-pr-456
```

**Pattern 3: Parallel Features**

```bash
# Main repo: feature-a
cd ~/projects/myapp
# Working on feature A...

# Create worktree for feature-b
git worktree add ../myapp-feature-b -b feature/b

# Create another for a spike
git worktree add ../myapp-spike-refactor -b spike/refactor-auth

# Can now switch between contexts instantly
cd ../myapp-feature-b      # Work on feature B
cd ../myapp-spike-refactor # Work on spike
cd ../myapp                # Back to feature A
```

**Verification gate:** Each worktree has the correct branch. Context switches are instant (just `cd`). Worktrees are removed after merge.

### Step 4: Manage and Audit Worktrees

**Goal:** Keep the worktree ecosystem clean and understandable.
**Expected output:** `git worktree list` shows only active worktrees.
**Tools to use:** `bash`

```bash
# List all worktrees
git worktree list

# Prune stale entries (after manual directory deletion)
git worktree prune

# Remove a worktree (after branch is merged)
git worktree remove ../myapp-feature-auth
# Force remove if untracked files present
git worktree remove --force ../myapp-feature-auth

# Clean merged worktrees (script in a single line)
for wt in $(git worktree list --porcelain | grep ^worktree | cut -d' ' -f2); do
  branch=$(git -C "$wt" rev-parse --abbrev-ref HEAD 2>/dev/null)
  if git branch --merged main | grep -q "$branch" 2>/dev/null; then
    echo "Removing merged worktree: $wt ($branch)"
    git worktree remove "$wt" 2>/dev/null
  fi
done
```

**Verification gate:** `git worktree list` shows only active worktrees. `git worktree prune` confirms 0 pruned entries.

### Step 5: Clean Up and Handoff

**Goal:** Ensure no stale worktrees remain and the main repo is clean.
**Expected output:** Worktrees removed, main repo updated, handoff complete.
**Tools to use:** `bash`

```bash
# After all branches are merged
git worktree list
# For each listed worktree where the branch is merged:
git worktree remove ../path/to/worktree

# Prune any remaining stale entries
git worktree prune

# Update main repo
cd ~/projects/myapp
git checkout main
git pull origin main
```

**Verification gate:** `git worktree list` returns only the main repo entry (or explicitly active worktrees). No stale entries remain.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Creating a worktree on a branch already checked out elsewhere | Git refuses with "fatal: already checked out"; trying to work around it by detaching HEAD in the wrong directory corrupts active state | Check `git worktree list` first; if the branch exists in another worktree, move to that worktree or delete it |
| Leaving worktrees orphaned after their branch is merged | Orphaned worktrees consume disk space and pollute `git worktree list`, making it impossible to tell which are active | Run `git worktree prune`; for each stale entry, run `git worktree remove <path>` |
| Running package install in one worktree expecting it in another | Each worktree has independent dependencies; packages installed in worktree A are not available in worktree B | Install dependencies in each worktree separately; do NOT share or symlink `node_modules` |
| Creating a worktree inside the main repository directory | A nested worktree is picked up by git as untracked content, creating confusing `git status` output | Always place worktrees outside the main repo tree (use `../` paths) |
| Manually deleting a worktree directory without running `git worktree prune` | Stale entries remain in the git worktree registry; `git worktree list` shows paths that no longer exist | After manual deletion, always run `git worktree prune` to clean the registry |

## Verification

Before marking any worktree operation as complete:

### Self-Verification Checklist

- [ ] `git worktree list` shows only expected worktrees — count matches active feature branches
- [ ] All worktrees reference existing branches — no entries with `(detached HEAD)` or deleted branch names
- [ ] No shared mutable files (`.env`, `node_modules`) symlinked across worktrees
- [ ] Worktree directory names follow the `<project>-<branch>` convention (e.g., `myapp-feature-auth`)
- [ ] Worktrees for merged branches have been removed or queued for removal
- [ ] `git worktree prune` confirms 0 stale entries
- [ ] No shared lock files between worktrees: `ls -la .git/index.lock` returns "No such file" in all worktrees

### Verification Commands

```bash
# List all worktrees
git worktree list

# Verify all branches exist
for wt in $(git worktree list --porcelain | grep ^worktree | cut -d' ' -f2); do
  echo "$wt: $(git -C "$wt" rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'MISSING')"
done

# Check for stale entries
git worktree prune --dry-run

# Check for shared node_modules
ls -la ../**/node_modules 2>/dev/null | grep "^l" || echo "no symlinked node_modules"

# Verify no lock conflicts
for wt in $(git worktree list --porcelain | grep ^worktree | cut -d' ' -f2); do
  ls "$wt/.git/index.lock" 2>/dev/null && echo "LOCKED: $wt" || true
done
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Branch Uniqueness | No branch checked out in more than one worktree | Detach HEAD in one worktree or use a different branch |
| Worktree Cleanup | No merged branches have active worktrees | Remove worktrees for merged branches; run `git worktree prune` |
| Naming Convention | Worktree name follows `<project>-<branch>` format | Rename the worktree directory |
| Independent Dependencies | Each worktree has its own dependencies (no symlinks) | Remove symlinks, install independently |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Creating/maintaining worktrees | Haiku | 1K-3K |
| Troubleshooting worktree issues | Sonnet | 3K-6K |
| Complex multi-workflow orchestration | Sonnet | 5K-10K |

### Parallelization
- **Worktree creation:** Sequential — each depends on `git worktree list` to verify no conflicts
- **Dependency installation:** Can run in parallel across worktrees (independent `node_modules`)
- **Testing:** Can run tests in separate worktrees simultaneously without interference

### Context Budget
- **Expected context usage:** 2K-5K per worktree session
- **Disk space per worktree:** Full working tree (source + `node_modules`) — typically 200MB-1GB per worktree

## Examples

### Example 1: Hotfix While Mid-Feature

**Input:** "I'm deep into implementing the dashboard redesign, but there's a production bug with the login page that needs an immediate fix."

**Execution:**
1. **Assess:** Single-branch worktree won't work — need both contexts simultaneously
2. **Create worktree:** `git worktree add ../myapp-hotfix-login -b hotfix/login-error`
3. **Install deps:** `cd ../myapp-hotfix-login && npm install`
4. **Fix bug:** Edit, test, commit, push, create PR
5. **Verify PR:** Tests pass, lint clean, review requested
6. **Switch back:** `cd ../myapp` — dashboard work is exactly as left
7. **After hotfix merges:** `git worktree remove ../myapp-hotfix-login`

**Result:** Hotfix deployed without disrupting the dashboard feature work. No stashing, no premature commits.

### Example 2: Edge Case — "Already Checked Out" Error

**Input:** `git worktree add ../myapp-feature feature/my-feature` returns `fatal: 'feature/my-feature' is already checked out`

**Correct response:**
```
Branch 'feature/my-feature' is already checked out in the main repo.
Options:
A) Detach HEAD in the main repo so the branch can be used in the worktree:
   cd /path/to/main && git checkout --detach
   Then retry: git worktree add ../myapp-feature feature/my-feature

B) Keep the worktree in the main repo and do all your feature work there
   (the worktree approach isn't adding value)

C) Create the worktree with a different branch name
   (not recommended — you want to work on the same branch)

Recommendation: Option A — detach HEAD, then create the worktree.
```

### Example 3: Edge Case — IDE Opens Wrong Worktree

**Input:** You're in `myapp`, but your IDE session restored from a previous project root and you're editing files in the wrong worktree.

**Correct response:**
```
Always verify your current directory before running tests or making edits:
  git branch --show-current

Create per-worktree IDE windows:
  code ../myapp-feature-auth    # New window for feature work
  code ../myapp                  # Original window for main work
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Creating a worktree without checking if the branch is already checked out | Git refuses with "already checked out"; working around it by detaching HEAD in the wrong directory corrupts active state | Always run `git worktree list` first; work within the constraints |
| Leaving worktrees orphaned after their branch is merged | Each orphaned worktree consumes disk space and appears in `git worktree list`, making it impossible to tell which worktrees are active | Remove worktrees promptly after merge; run `git worktree prune` periodically |
| Sharing build output directories between worktrees | Concurrent builds from two worktrees writing to the same directory produce interleaved, corrupted artifacts | Each worktree must have its own build output directory; configure separately |
| Keeping worktrees for completed branches as "archives" | Worktrees are not archives; they are active working directories. Branches deleted remotely mean the worktree's branch no exists | Archive by tagging the commit, then remove the worktree |
| Forgetting to `git worktree prune` after manual worktree directory deletion | Manually deleted worktree directories leave stale entries in the git worktree registry | After manual deletion, always run `git worktree prune` |

## References

### Internal Dependencies
- `finishing-a-development-branch` — Recommended downstream; for finishing the branch that was worked on in a worktree
- `receiving-code-review` — Optional; PR review in a separate worktree uses this skill

### External Standards
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree) — Official Git worktree reference
- [Git Worktree Tutorial (Atlassian)](https://www.atlassian.com/git/tutorials/git-worktree) — Practical worktree usage guide

### Related Skills
- `finishing-a-development-branch` — Follows worktree usage; the branch worked on in a worktree needs to be merged and cleaned up
- `debugging` — Can use worktrees for debugging production issues without disrupting active development

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge cases ("already checked out", wrong IDE window), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; added clean-merged script; enhanced naming convention enforcement |
| 1.0.0 | 2024-01-15 | Initial version — Git worktree basics with 3 workflow patterns and common issue troubleshooting |
