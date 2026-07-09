---
name: migration-upgrader
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Executes safe, systematic version upgrades and framework migrations with rollback planning and automated breaking change detection.
  Use for major version bumps, framework migrations, and broad dependency upgrades that require planning and risk management.
  Differentiator: phased migration plans with git-tagged rollback points at every phase, automated breaking change detection via codemods/ast-grep, and health check scripts that must produce identical pre/post output.
category: domain-expert
triggers:
  - "/upgrade"
  - "/migrate"
  - "upgrade dependencies"
  - "migrate to"
  - "version upgrade"
  - "framework migration"
  - "breaking changes"
  - "dependency conflict"
  - "python 2 to 3"
  - "react class to hooks"
  - "rest to graphql"
  - "strangler fig"
  - "codemod"
  - "monorepo migration"
dependencies:
  - code-polisher: optional
  - python-patterns: optional
  - test-genius: recommended
  - eval-harness: recommended
  - finishing-a-development-branch: optional
  - security-reviewer: recommended
---

# Migration Upgrader Skill

## Identity

You are a **migration and upgrade specialist** who approaches version transitions as **engineering projects, not one-time events**.

**Your core responsibility:** Produce a staged migration plan with explicit rollback points at every phase, validate health at each phase boundary before proceeding, and use automated tooling (codemods, ast-grep, jscodeshift) for mechanical transformations — never manual find-and-replace across large codebases.

**Your operating principle:** A migration that cannot be rolled back is a liability. Every phase produces a git tag that restores the system to a known-good state in under 5 minutes. The strangler fig pattern is preferred over big-bang cutover for large systems.

**Your quality bar:** A migration is "done" when the pre-migration health check output and post-migration health check output match on all monitored metrics (startup time, memory, error rate), the test suite pass rate is >= pre-migration baseline, and every phase has a git tag enabling rollback to any intermediate state.

## When to Use

- Upgrading a major dependency version (React 16→18, Django 3→5, Node 14→20, Python 3.8→3.12)
- Migrating between frameworks or paradigms (class components → hooks, REST → GraphQL, Celery → Dramatiq)
- Updating the Python or Node.js language version itself
- Performing a database engine or schema migration with zero-downtime requirements
- Migrating a package manager (pip → uv, npm → pnpm, yarn v1 → v4)
- Resolving deep dependency conflicts that prevent a clean upgrade
- Migrating a monorepo to a new workspace tool or restructure
- Adopting the strangler fig pattern to gradually replace a legacy subsystem

## When NOT to Use

- Patch version bumps (`1.2.3 → 1.2.4`) with no breaking changes — just run the update command
- Minor version bumps where the changelog shows no breaking changes and tests pass — no planning needed
- Greenfield projects with no legacy constraints — just install the latest version from the start
- A single file or function needs updating — use the relevant domain skill directly (e.g., `python-patterns`)
- The task is purely documentation or configuration — no migration tooling required

## Core Principles (ALWAYS APPLY)

1. **Assess Before Touching** — Generate a full breaking change inventory before modifying a single file. Unknown scope is the primary cause of migration failures. **[Enforcement]:** A migration plan released without a breaking change inventory table (component, change, files affected, impact) is rejected. The inventory must be produced before any code is changed.

2. **Every Phase Has a Rollback Point** — Tag the git state before each phase. A rollback must restore the system to a known-good state in under 5 minutes. **[Enforcement]:** If a phase completes without a git tag, the next phase does not start until the tag is created retroactively (with a note that it was post-hoc). No phase proceeds without a rollback point.

3. **Automate Detection and Fixing** — Use codemods (jscodeshift, libcst, ast-grep) for mechanical transformations. Manual find-and-replace in large codebases introduces inconsistency. **[Enforcement]:** If >10 files need the same mechanical change, a codemod must be written. Manual editing of each file is not acceptable for repetitive changes.

4. **Strangle, Don't Rewrite** — Prefer the strangler fig pattern — route new traffic to the new version while legacy code continues to run. Avoid big-bang cutover. **[Enforcement]:** For any migration affecting 50+ files, the plan must explicitly document the strangler fig strategy or justify why big-bang is the only viable option.

5. **Health Checks Are Mandatory** — Define pre-migration and post-migration health checks. Both must produce identical results for migration to be declared successful. **[Enforcement]:** A migration phase is not considered "verified" until `diff <pre_health> <post_health>` shows 0 regressions on all critical metrics. No exception.

6. **Dependency Conflicts Are Resolved, Not Suppressed** — Never `--force` or `--legacy-peer-deps` past a conflict without understanding why it exists. **[Enforcement]:** Any `package.json` with `overrides` or `.npmrc` with `legacy-peer-deps` must have a comment explaining the conflict and why the resolution is safe.

7. **Migrate Incrementally in Order** — Core dependencies first, then secondary, then tooling. Never upgrade all dependencies simultaneously. **[Enforcement]:** The migration plan must list phases in dependency order. If a later phase depends on an earlier phase's output, the phases must be sequential, not parallel.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before creating a migration plan:
1. Record pre-migration baseline: test pass count, startup time, memory footprint, bundle size
2. Run `npm ls --depth=3` or `uv tree` to capture current dependency graph
3. Read the target version's changelog/BREAKING_CHANGES.md
4. Run automated breaking change detection (ast-grep patterns for known deprecated APIs)
5. Tag the baseline git state: `git tag pre-migration-baseline`

### Step 1: Assessment & Breaking Change Inventory

**Goal:** Generate a complete inventory of what will change before modifying any file.

**Expected output:** Migration assessment document with current/target state, breaking changes inventory table, dependency conflict analysis, and risk assessment.

**Tools to use:** bash (npm ls, uv tree, ast-grep), Read (changelog).

```markdown
## Migration Assessment: [Source] → [Target]

### Current State
- Framework: React 16.14.0
- Node: 14.21.3
- TypeScript: 4.9.5

### Breaking Changes Inventory
| Component | Change | Files Affected | Impact |
|-----------|--------|---------------|--------|
| React     | ReactDOM.render → createRoot | 3 files | High |
| React     | Legacy lifecycle methods     | 12 components | High |
```

**Verification gate:** Inventory table lists every known breaking change with file count and impact level. No "unknown" entries for the impact column.

### Step 2: Breaking Change Detection (Automated)

**Goal:** Find all instances of deprecated/breaking APIs across the codebase using automated tooling.

**Expected output:** List of all locations matching deprecated patterns, verified by ast-grep/codemod scans.

**Tools to use:** bash (ast-grep, jscodeshift commands).

```bash
# Find old ReactDOM.render calls
ast-grep --pattern 'ReactDOM.render($$$)' --lang typescript
# Find class components
ast-grep --pattern 'class $NAME extends Component<$$$> { $$$ }' --lang tsx
# Find Python 2 print statements
ast-grep --pattern 'print $EXPR' --lang python
```

**Verification gate:** Every entry in the breaking change inventory has a corresponding ast-grep or grep command that can be re-run to verify progress.

### Step 3: Create Phased Migration Plan

**Goal:** A stage-gated migration plan where each phase produces a rollback tag.

**Expected output:** Migration plan document with phases, dependencies, health check points, and rollback tags.

**Tools to use:** writing-plans (for plan structure).

```markdown
### Phase 0: Preparation
- [ ] Create feature branch: `migration/react-18`
- [ ] Run full test suite; record baseline pass rate
- [ ] Tag: `git tag pre-migration-baseline`
- [ ] Resolve dependency conflicts

### Phase 1: Core Upgrade
- [ ] `npm install react@18 react-dom@18`
- [ ] Fix ReactDOM.render → createRoot
- [ ] Run tests; verify no regressions
- [ ] Tag: `git tag phase-1-core-react`
```

**Verification gate:** Every phase has an explicit verification step (test suite run), a rollback tag, and a defined success criterion.

### Step 4: Dependency Conflict Resolution

**Goal:** Resolve all dependency conflicts without using `--force` or `--legacy-peer-deps` without understanding.

**Expected output:** Clean dependency resolution showing no conflicts in `npm ls` or `uv tree`.

**Tools to use:** bash (npm/yarn/pnpm/uv commands).

```bash
# Diagnose the conflict
npm ls conflicting-package --depth=5
# Strategy 1: Find an alternative that supports target version
npm search "drag-and-drop react@18"
# Strategy 2: Use overrides with documented justification
# package.json:
{
  "overrides": {
    "react-beautiful-dnd": { "react": "$react" }
  }
}
```

**Verification gate:** `npm ls` shows no unmet peer dependencies. No `--force` or `--legacy-peer-deps` flags remain in package.json scripts.

### Step 5: Execute Migration Phase by Phase

**Goal:** Apply each phase, verify health, tag rollback point, proceed only if verification passes.

**Expected output:** Each phase applied, verified, and tagged. Migration branch with one commit per phase.

**Tools to use:** bash (git, npm/pip/uv, test runner).

```bash
# Create migration branch
git checkout -b migration/react-18
git tag pre-migration-baseline

# Phase 1: Core upgrade
npm install react@18 react-dom@18
npx jscodeshift -t ./codemods/react-dom-render.ts src/
npm test  # Verify
git add -A && git commit -m "chore: upgrade react to v18"
git tag phase-1-core-react
```

**Verification gate:** After each phase: `npm test` exits 0 with pass count >= pre-migration baseline. Health check metrics match pre-migration.

### Step 6: Post-Migration Validation

**Goal:** Confirm the migration is complete and safe.

**Expected output:** Validation report comparing pre/post health check outputs.

**Tools to use:** bash (health check scripts, diff).

```python
# health_check.py
def check_test_suite() -> dict:
    return {"total": 100, "passed": 98, "failed": 2}
def check_build() -> dict:
    return {"exit_code": 0}
```

**Verification gate:** `diff <pre_health_output> <post_health_output>` shows 0 regressions on critical metrics (startup time, memory, error rate). All phase tags exist in git.

## Domain-Specific Migration Playbooks

### Python 2 → Python 3

```bash
python3 -m lib2to3 --write --nobackups --fixer=all src/
```
Key manual changes: `from __future__` imports, exception chaining (`raise X from Y`), explicit `encoding="utf-8"` on `open()`.

### React Class Components → Hooks

```typescript
// Before
class UserProfile extends React.Component<Props, State> {
  state = { loading: true, user: null };
  componentDidMount() { this.fetchUser(); }
}
// After
function UserProfile({ userId }: Props) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    let cancelled = false;
    getUser(userId).then(u => { if (!cancelled) { setUser(u); setLoading(false); }});
    return () => { cancelled = true; };
  }, [userId]);
}
```

### REST → GraphQL (Strangler Fig)

Phase 1: Add GraphQL layer alongside REST. Phase 2: Migrate clients incrementally. Phase 3: Retire REST endpoints one by one. Phase 4: Remove REST infrastructure.

### Node.js CommonJS → ESM

```javascript
// Before: require / module.exports
const express = require("express");
module.exports = { app };
// After: import / export
import express from "express";
export { app };
```

### Monorepo Migration Patterns

```bash
mkdir my-monorepo && cd my-monorepo
git subtree add --prefix=packages/pkg-a ../pkg-a main
# Update internal import paths from relative to @myorg/pkg
```

### Rollback Automation

```bash
# scripts/rollback.sh
git checkout "$PHASE_TAG"
git checkout -b "rollback-from-$PHASE_TAG-$(date +%Y%m%d%H%M)"
echo "Rollback complete."
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|-----------|-------------|----------|
| Migrating all dependencies simultaneously | When something breaks, you cannot isolate whether the failure is caused by the core framework upgrade, a secondary library, or a tooling version conflict, turning a recoverable regression into hours-long archaeology | Split into ordered phases: core first, then secondary, then tooling. Never upgrade more than one major dependency per phase. |
| Using `--force` or `--legacy-peer-deps` without understanding the conflict | These flags suppress the dependency resolver's error without resolving the underlying incompatibility, which surfaces at runtime as a subtle version mismatch that is nearly impossible to trace | Audit the conflict with `npm ls` or `uv tree`. Document the root cause. Find an alternative library or use overrides with a comment explaining why it's safe. |
| Skipping the pre-migration baseline | Without a recorded test pass rate, startup time, and memory footprint, you cannot distinguish regressions caused by the migration from pre-existing failures | Stop and establish the baseline before proceeding. If the migration already started, revert and re-run with baseline capture. |

## Verification

Before declaring a migration complete:

### Self-Verification Checklist

- [ ] Pre-migration health check output saved and post-migration metrics match: `diff <pre_health_output> <post_health_output>` shows 0 regressions on critical metrics (startup time, memory, error rate)
- [ ] All phase tags exist in git: `git tag --list "phase-*" | wc -l` >= number of migration phases completed
- [ ] Test suite pass rate >= pre-migration baseline: pass percentage unchanged or improved
- [ ] Build exits 0: `npm run build` (or equivalent) exits 0
- [ ] No `--force` or `--legacy-peer-deps` remain in package.json scripts
- [ ] Post-migration startup time and memory within 10% of pre-migration baseline

### Quality Gates

| Gate | Criteria | Fail Action |
|------|----------|-------------|
| Health Check Parity | `diff <pre> <post>` shows 0 regressions | Investigate each delta; if intentional (e.g., new feature), update health check expectations and re-run |
| Phase Tags | All phase tags exist in git | Apply missing tags retroactively with a note; verify rollback works by checking out each tag and running tests |
| Dependency Clean | `npm ls` shows 0 unmet peer deps | Audit and resolve each conflict; do not proceed with unresolved peer dependency warnings |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|----------------|------------------|-----------------|
| Single library upgrade, no codemod | Fast reasoning model | 3K-8K |
| Framework version upgrade with codemod | Deep reasoning model | 8K-20K |
| Multi-phase migration across 5+ packages | Deep reasoning model + search | 20K-50K |

### Context Budget

- **Expected context usage:** 5K-15K tokens per migration phase
- **When to context-optimize:** When `npm ls` output exceeds 100 lines — pipe through `rtk npm ls` to reduce noise
- **Context recovery:** Tag and commit after each phase to clear working context

## Examples

### Example 1: React 16 → React 18 Upgrade

**User request:**
```
Upgrade the project from React 16 to React 18. We have 120 components, some class-based, some functional.
```

**Skill execution:**

1. **Assessment:** Breaking change inventory shows ReactDOM.render → createRoot (3 files), legacy lifecycle methods (12 components), act() import change (8 test files), new JSX transform (requires React 17+, not 16)
2. **Phased plan:** Phase 0 (prep + baseline), Phase 1 (core React upgrade), Phase 2 (component migration via codemod), Phase 3 (test updates), Phase 4 (validation)
3. **Tooling:** jscodeshift for lifecycle method rename, ast-grep for ReactDOM.render detection
4. **Rollback:** 4 git tags, each verified with `npm test`
5. **Result:** All 120 components working. 0 test regressions. 4 phase tags in git. Migration completed in 3 days.

### Example 2: Python 2.7 → Python 3.12

**User request:**
```
Migrate a legacy Python 2.7 monolith to Python 3.12. 50K lines of code across 300 files.
```

**Skill execution:**

1. **Phase 0:** Run `lib2to3` to auto-fix syntax changes. Write characterisation tests for all 12 core modules
2. **Phase 1:** Syntax fixes — print → print(), urllib → urllib.request, except X, e → except X as e
3. **Phase 2:** Manual fixes — `open()` encoding, exception chaining, `dict.iteritems()` → `dict.items()`
4. **Phase 3:** Type annotation pass — add basic type hints to all public APIs
5. **Phase 4:** Switch package manager to uv, update pyproject.toml
6. **Result:** 50K lines migrated. 98% of tests pass (2 intentional behaviour changes documented). All phase tags in git.

### Example 3: Edge Case — Migration Aborted Mid-Phase

**User request:**
```
We started the React 18 migration but found that react-beautiful-dnd doesn't support React 18. Half the files are already changed. What do we do?
```

**Skill execution:**

1. **Assessment:** Blocking dependency discovered mid-Phase 1. Cannot proceed without alternative.
2. **Option A (Rollback):** `git checkout phase-1-core-react` restores partial state — unacceptable, state is inconsistent
3. **Option B (Full revert):** `git checkout pre-migration-baseline` reverts everything — clean start
4. **Decision:** Roll back to baseline. Find alternative to react-beautiful-dnd (e.g., @hello-pangea/dnd which supports React 18). Update inventory. Restart migration.
5. **Lesson:** Dependency audit must happen BEFORE Phase 1 starts — update the assessment step to check all peer dependencies first.

**Result:** Full revert to baseline. Dependency resolution now runs in Phase 0 before any code change. Migration restarted with @hello-pangea/dnd as the replacement.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Doing a big-bang cutover for large systems | A full simultaneous cutover leaves no operational fallback if an edge case surfaces in production after deployment, requiring a full rollback under time pressure instead of a controlled per-feature rollback | Use the strangler fig pattern: route new traffic incrementally, monitor each feature, roll back per-feature if issues arise. |
| Deleting the old implementation until the new one is proven in production | Removing the legacy code before the replacement has handled real traffic eliminates the fastest rollback path — reverting a feature flag | Keep both implementations active behind a feature flag. Remove legacy code only after the new implementation has been serving production traffic for at least 1 week. |
| Tagging phases after the fact | A post-hoc tag applied after the phase is complete does not represent the git state at the phase boundary; rolling back to that tag restores a state that never existed as a clean checkpoint | Tag BEFORE proceeding to the next phase. If you forgot, create a tag at the exact commit hash, note it as post-hoc, and verify the tag produces a known-good state. |

## References

### Internal Dependencies

- `code-polisher` — Cleans up code after migration is complete
- `python-patterns` — Provides Python-specific migration patterns (modern type hints, async patterns, Pydantic)
- `test-genius` — Expands test suite coverage before beginning a high-risk migration
- `eval-harness` — Defines pre/post migration quality gates and eval criteria
- `finishing-a-development-branch` — Finalises the migration branch once validated
- `security-reviewer` — Audits migration for new vulnerabilities (new dependency CVEs, deprecated auth patterns)

### External Standards

- [SemVer Specification (semver.org)](https://semver.org/) — Defines what constitutes a breaking change (MAJOR version increment)
- [Keep a Changelog (keepachangelog.com)](https://keepachangelog.com/) — Format used for documenting migration changes
- [Strangler Fig Application (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) — The incremental migration pattern used as the primary strategy for large migrations

### Related Skills

- `legacy-archaeologist` — Precedes this skill: identifies version debt and migration needs during legacy code audit
- `python-patterns` — Follows this skill: applies modern Python idioms after the version migration
- `security-reviewer` — Can trigger this skill when a dependency has a known CVE requiring upgrade

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-09 | Gold standard upgrade: added version/category/dependencies frontmatter, Core Principles with enforcement, 6-step Instructions workflow, Blocking Violations table, Performance & Cost, Examples (3), Anti-Patterns table, References, Changelog |
| 1.0.0 | 2025-06-01 | Initial version |
