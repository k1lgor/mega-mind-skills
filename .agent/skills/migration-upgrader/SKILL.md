---
name: migration-upgrader
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Safe, systematic version upgrades and framework migrations with rollback planning, automated breaking change detection, and staged execution. Covers dependency conflict resolution, monorepo migration patterns, the strangler fig pattern for gradual migration, pre/post health check scripts, and domain-specific playbooks for Python 2→3, React class→hooks, REST→GraphQL, and more. Use for major version bumps and framework migrations that require planning and risk management.
triggers:
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
---

# Migration Upgrader Skill

## Identity

You are a migration and upgrade specialist who approaches version transitions as engineering projects, not one-time events. You assess risk before touching a single file, produce a staged migration plan with explicit rollback points at every phase, and validate health at each phase boundary before proceeding. You know that a migration that cannot be rolled back is a liability. You use automated tooling (codemods, ast-grep, jscodeshift) to detect and fix breaking changes systematically, not manually — manual find-and-replace in large codebases introduces inconsistency. You design migrations to be incremental: the strangler fig pattern means new code uses the target version while legacy code is migrated gradually, keeping the system operational throughout.

## When to Activate

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

---

## Core Principles

1. **Assess before touching**: Generate a full breaking change inventory before modifying a single file. Unknown scope is the primary cause of migration failures.
2. **Every phase has a rollback point**: Tag the git state before each phase. A rollback must restore the system to a known-good state in under 5 minutes.
3. **Automate detection and fixing**: Use codemods (jscodeshift, libcst, ast-grep) for mechanical transformations. Manual find-and-replace in large codebases introduces inconsistency.
4. **Strangle, don't rewrite**: Prefer the strangler fig pattern — route new traffic to the new version while legacy code continues to run. Avoid big-bang cutover.
5. **Health checks are mandatory**: Define pre-migration and post-migration health checks. Both must produce identical results for migration to be declared successful.
6. **Dependency conflicts are resolved, not suppressed**: Never `--force` or `--legacy-peer-deps` past a conflict without understanding why it exists.
7. **Migrate incrementally in order**: Core dependencies first, then secondary, then tooling. Never upgrade all dependencies simultaneously.

---

## Migration Process

### Step 1: Assessment

Before creating a plan, generate a complete inventory of what will change.

```markdown
## Migration Assessment: [Source] → [Target]

### Current State
- Framework: React 16.14.0
- Node: 14.21.3
- TypeScript: 4.9.5
- Test runner: Jest 27

### Target State
- Framework: React 18.3.1
- Node: 20.11.0
- TypeScript: 5.4.5
- Test runner: Vitest 1.6

### Breaking Changes Inventory

| Component | Change | Files Affected | Impact |
| --- | --- | --- | --- |
| React | ReactDOM.render → createRoot | 3 files | High |
| React | Legacy lifecycle methods | 12 components | High |
| React | act() import changed | 8 test files | Medium |
| Node | require() ES modules | 2 config files | Medium |
| TypeScript | Strict null changes | 47 type errors | High |

### Dependency Conflict Analysis
Run: `npm ls --depth=3` or `uv tree` to find version conflicts
Conflicts: react-beautiful-dnd requires react@<=17 (incompatible)

### Risk Assessment
- High: 3 items | Medium: 2 items | Low: 0 items
- Estimated effort: 3-5 days
- Rollback complexity: Low (git tag per phase)
```

### Step 2: Breaking Change Detection with Automated Tools

```bash
# JavaScript/TypeScript: jscodeshift codemods
npx jscodeshift -t codemod-react-18-upgrade.ts src/

# Python: libcst or ast-grep for structural search
ast-grep --pattern 'ReactDOM.render($$$)' --lang typescript

# Python 2→3: 2to3 tool
python3 -m py_compile -W error  # Check for syntax errors first
python3 -m lib2to3 --write --nobackups src/

# Check for deprecated patterns (grep for known patterns)
ast-grep --pattern 'componentDidMount() { $$$ }' --lang tsx
```

#### ast-grep Pattern Examples for Common Migrations

```bash
# Find React class components
ast-grep --pattern 'class $NAME extends Component { $$$ }' --lang tsx

# Find old ReactDOM.render calls
ast-grep --pattern 'ReactDOM.render($JSX, $CONTAINER)' --lang tsx

# Find Python 2 print statements
ast-grep --pattern 'print $EXPR' --lang python

# Find deprecated string format
ast-grep --pattern '$VAR % $ARGS' --lang python
```

### Step 3: Create Migration Plan (Phased)

```markdown
## Migration Plan: React 16 → React 18

### Phase 0: Preparation (Day 1)
- [ ] Create feature branch: `migration/react-18`
- [ ] Run full test suite; record baseline pass rate
- [ ] Tag git state: `git tag pre-migration-baseline`
- [ ] Run pre-migration health check script; save output
- [ ] Resolve dependency conflict: find react-beautiful-dnd alternative

### Phase 1: Core React Upgrade (Day 2)
- [ ] `npm install react@18 react-dom@18`
- [ ] Update ReactDOM.render → createRoot in 3 files (see inventory)
- [ ] Run test suite; verify no regressions
- [ ] Tag git state: `git tag phase-1-core-react`

### Phase 2: Component Migrations (Day 2-3)
- [ ] Run jscodeshift codemod for legacy lifecycle methods
- [ ] Manually review and fix 12 affected components
- [ ] Update act() imports in 8 test files
- [ ] Run test suite; verify no regressions
- [ ] Tag git state: `git tag phase-2-components`

### Phase 3: TypeScript Upgrade (Day 3-4)
- [ ] `npm install typescript@5`
- [ ] Fix 47 strict null type errors (tsc --noEmit output)
- [ ] Run test suite; verify no regressions
- [ ] Tag git state: `git tag phase-3-typescript`

### Phase 4: Node Version Update (Day 4)
- [ ] Update .nvmrc / .tool-versions to node 20
- [ ] Fix 2 ES module config files
- [ ] Run test suite and build; verify
- [ ] Tag git state: `git tag phase-4-node`

### Phase 5: Validation (Day 5)
- [ ] Run full test suite; compare to baseline
- [ ] Run post-migration health check; compare to pre-migration output
- [ ] Manual smoke test of critical flows
- [ ] Performance benchmark vs baseline

### Rollback Plan
Each phase tag provides a rollback point:
`git checkout phase-1-core-react` → restores to post-phase-1 state
`git checkout pre-migration-baseline` → full revert
```

### Step 4: Dependency Conflict Resolution

```bash
# Diagnose the conflict
npm ls package-name --depth=5
npm explain package-name

# Strategy 1: Find an alternative that supports target version
npm search "drag-and-drop react@18"

# Strategy 2: Use overrides/resolutions (last resort — may break things)
# package.json:
{
  "overrides": {
    "react-beautiful-dnd": {
      "react": "$react"
    }
  }
}

# Strategy 3: Fork and patch
# Only if the package is unmaintained and critical

# uv (Python) dependency resolution:
uv add "package>=2.0,<3.0"  # Explicit range constraint
uv tree  # Visualize full dependency graph
uv lock --upgrade-package package-name  # Upgrade one package at a time
```

### Step 5: Execute Migration

```bash
# Create migration branch
git checkout -b migration/react-18

# Tag baseline
git tag pre-migration-baseline

# Phase 1: Core upgrade
rtk npm install react@18 react-dom@18 (or rtk bun install react@18 react-dom@18)
rtk npm test (or rtk bun test)

# Fix ReactDOM.render (automated with codemod)
npx jscodeshift -t ./codemods/react-dom-render.ts src/

# Verify fixes
rtk npm test

# Tag phase checkpoint
git add -A && git commit -m "chore: upgrade react to v18"
git tag phase-1-core-react
```

### Step 6: Health Check Scripts

Pre-migration and post-migration scripts must produce identical output for the migration to be declared successful.

```python
#!/usr/bin/env python3
# scripts/health_check.py
"""Run pre/post migration health checks. Output must match between runs."""
import subprocess
import json
from pathlib import Path

def check_test_suite() -> dict:
    result = subprocess.run(
        ["python", "-m", "pytest", "--tb=no", "-q", "--json-report"],
        capture_output=True, text=True
    )
    report = json.loads(Path(".report.json").read_text())
    return {
        "total": report["summary"]["total"],
        "passed": report["summary"]["passed"],
        "failed": report["summary"]["failed"],
    }

def check_build() -> dict:
    result = subprocess.run(
        ["python", "-m", "build", "--no-isolation"],
        capture_output=True, text=True
    )
    return {"exit_code": result.returncode, "dist_files": list(Path("dist").glob("*"))}

def check_import_times() -> dict:
    import time
    start = time.perf_counter()
    subprocess.run(["python", "-c", "import mypackage"], capture_output=True)
    return {"import_ms": int((time.perf_counter() - start) * 1000)}

if __name__ == "__main__":
    checks = {
        "tests": check_test_suite(),
        "build": check_build(),
        "import_performance": check_import_times(),
    }
    output_path = Path(f"health-check-{Path('.').resolve().name}.json")
    output_path.write_text(json.dumps(checks, indent=2, default=str))
    print(json.dumps(checks, indent=2, default=str))
```

---

## Domain-Specific Migration Playbooks

### Python 2 → Python 3

```bash
# 1. Detect 2.x patterns
python3 -m lib2to3 --list-fixes  # Show all fixers
python3 -m lib2to3 --write --nobackups --fixer=all src/

# 2. Key manual changes (lib2to3 does not handle these)
# - Remove: from __future__ import print_function, unicode_literals
# - Update: Exception chaining (raise X from Y)
# - Update: dict.items() returns view, not list (wrap in list() if needed)
# - Update: open() text mode encoding (explicit encoding="utf-8")
# - Remove: __metaclass__ = Meta → class Foo(metaclass=Meta)

# 3. Verify with pyright strict mode
uv run pyright --pythonVersion 3.10
```

### React Class Components → Hooks

```typescript
// Before (class component)
class UserProfile extends React.Component<Props, State> {
  state = { loading: true, user: null };
  componentDidMount() { this.fetchUser(); }
  componentDidUpdate(prevProps) {
    if (prevProps.userId !== this.props.userId) this.fetchUser();
  }
  async fetchUser() {
    const user = await getUser(this.props.userId);
    this.setState({ loading: false, user });
  }
  render() {
    if (this.state.loading) return <Spinner />;
    return <UserCard user={this.state.user} />;
  }
}

// After (function component with hooks)
function UserProfile({ userId }: Props) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getUser(userId).then(u => {
      if (!cancelled) { setUser(u); setLoading(false); }
    });
    return () => { cancelled = true; };  // Cleanup on userId change
  }, [userId]);

  if (loading) return <Spinner />;
  return <UserCard user={user!} />;
}
```

Automate discovery:

```bash
# Find all class components
ast-grep --pattern 'class $NAME extends Component<$$$> { $$$ }' --lang tsx
ast-grep --pattern 'class $NAME extends PureComponent<$$$> { $$$ }' --lang tsx
```

### REST → GraphQL (Strangler Fig Pattern)

```
Phase 1: Introduce GraphQL layer alongside REST
  - Add Apollo Server or graphql-yoga
  - Mirror existing REST endpoints as GraphQL queries
  - New features use GraphQL only

Phase 2: Migrate clients incrementally
  - Per-feature, migrate client from REST fetch → Apollo useQuery
  - REST endpoint remains active; deprecate with a header

Phase 3: Retire REST endpoints one by one
  - When no client calls a REST endpoint, remove it
  - Monitor access logs for 30 days before removal

Phase 4: Remove REST infrastructure
  - Remove REST router, controllers, REST-specific middleware
  - Keep only GraphQL layer
```

### Node.js CommonJS → ESM

```javascript
// Before (CommonJS)
const express = require("express");
const { readFile } = require("fs/promises");
module.exports = { app };

// After (ESM)
import express from "express";
import { readFile } from "fs/promises";
export { app };
```

```json
// package.json
{
  "type": "module"  // Enables ESM for .js files
}
```

```bash
# Detect all require() calls
ast-grep --pattern 'require($PATH)' --lang javascript
# Detect module.exports
ast-grep --pattern 'module.exports = $EXPR' --lang javascript
```

---

## Monorepo Migration Patterns

```bash
# Converting a multi-repo to monorepo (pnpm workspaces example)
# 1. Create workspace root
mkdir my-monorepo && cd my-monorepo
cat > pnpm-workspace.yaml << EOF
packages:
  - "packages/*"
  - "apps/*"
EOF

# 2. Move repos in as packages
git subtree add --prefix=packages/pkg-a ../pkg-a main

# 3. Update internal import paths
# Before: import { foo } from "../../shared/utils"
# After:  import { foo } from "@myorg/shared"

# Detect cross-package relative imports to fix:
ast-grep --pattern 'from "../../$$$"' --lang typescript
```

---

## Rollback Automation

```bash
#!/bin/bash
# scripts/rollback.sh — run on migration failure
set -e

PHASE=${1:-"pre-migration-baseline"}
echo "Rolling back to: $PHASE"

# Verify the tag exists
git rev-parse --verify "refs/tags/$PHASE" || {
  echo "ERROR: Tag '$PHASE' not found. Available tags:"
  git tag --list "pre-migration*" "phase-*"
  exit 1
}

# Hard reset to the tagged state
git checkout "$PHASE"
git checkout -b "rollback-from-$PHASE-$(date +%Y%m%d%H%M)"

echo "Rollback complete. Now on branch: $(git branch --show-current)"
echo "Run health check to verify:"
echo "  python scripts/health_check.py"
```

---

## Validation Checklist

```markdown
## Post-Migration Validation

### Functional
- [ ] All tests pass (compare count to pre-migration baseline)
- [ ] Build succeeds with zero warnings
- [ ] No new type errors (tsc --noEmit or pyright exits 0)
- [ ] Linter passes (ruff check / eslint)

### Performance
- [ ] Import/startup time within 10% of baseline
- [ ] Memory footprint within 10% of baseline
- [ ] P95 response latency within 5% of baseline (if applicable)

### Security
- [ ] `npm audit` or `uv audit` shows no new high/critical vulnerabilities
- [ ] No pinned-to-old-version packages with known CVEs

### Documentation
- [ ] README updated with new version requirements
- [ ] CHANGELOG entry written
- [ ] Any deprecated API patterns removed from docs
```

---

## Self-Verification Checklist

Before declaring a migration complete:

- [ ] Pre-migration health check output saved and post-migration metrics match: `diff <pre_health_output> <post_health_output>` shows 0 regressions on critical metrics (startup time, memory, error rate)
- [ ] All phase tags exist in git: `git tag --list "phase-*" | wc -l` >= number of migration phases completed — missing tags means rollback points are unavailable
- [ ] Test suite pass rate >= pre-migration baseline: `npm test (or pytest) 2>&1 | grep -c "FAIL"` post-migration <= pre-migration FAIL count; pass percentage unchanged or improved
- [ ] Build exits with code 0: `npm run build (or equivalent)` exits 0 — non-zero exit is a blocking failure
- [ ] No `--force` or `--legacy-peer-deps` used without justification: `grep -rn "\-\-force\|\-\-legacy-peer-deps" package.json scripts/ .npmrc` returns 0 matches, or each match has a corresponding comment explaining the reason
- [ ] Dependency conflict resolution documented: `grep -n "conflict\|resolution\|peer dep" <migration_plan>` returns at least 1 match per detected conflict — undocumented resolutions fail this check
- [ ] Rollback script tested against at least one phase tag: `git log --oneline | grep -c "rollback\|revert"` returns >= 1; rollback exits 0 and app starts cleanly
- [ ] Post-migration startup time and memory within 10% of pre-migration baseline: startup delta <= 10% and memory delta <= 10% — exceeding either threshold requires documented justification

---

## Success Criteria

A migration task is complete when:

1. All tests pass at a rate >= the pre-migration baseline (no regressions).
2. The build produces a deployable artifact with zero errors.
3. The post-migration health check output matches the pre-migration output on all monitored metrics within tolerance (10% for performance, 0% for functional correctness).
4. Every phase is tagged in git, enabling rollback to any intermediate state.
5. No unresolved dependency conflicts remain (no `--force` flags in `package.json` scripts).
6. The migration plan document is updated with actual outcomes and any deviations from plan.

---

## Anti-Patterns

- Never migrate all dependencies simultaneously because when something breaks — and it will — you cannot isolate whether the failure is caused by the core framework upgrade, a secondary library, or a tooling version conflict, turning a recoverable regression into an hours-long archaeology session.
- Never use `--force` or `--legacy-peer-deps` without understanding the conflict because these flags suppress the dependency resolver's error without resolving the underlying incompatibility, which will surface at runtime as a subtle version mismatch that fails only under specific conditions and is nearly impossible to trace back to the suppressed flag.
- Never skip the pre-migration baseline because without a recorded test pass rate, startup time, and memory footprint, you cannot distinguish regressions introduced by the migration from pre-existing failures, making the post-migration validation report meaningless.
- Never do a big-bang cutover for large systems because a full simultaneous cutover leaves no operational fallback if an edge case surfaces in production after deployment, requiring a full rollback under time pressure instead of a controlled per-feature rollback via the strangler fig pattern.
- Never delete the old implementation until the new one is proven in production because removing the legacy code before the replacement has handled real traffic eliminates the fastest rollback path — reverting a feature flag — and forces a full git revert and redeploy if an issue emerges.
- Never manually find-and-replace across a large codebase because inconsistent manual edits will miss occurrences in less-visited files and introduce subtle bugs where the pattern was almost-but-not-exactly matched, creating a codebase where some modules use the old API and others the new one without any systematic record.
- Never tag phases after the fact because a post-hoc tag applied after the phase is complete does not represent the git state at the phase boundary, which means rolling back to that tag restores a state that never actually existed as a clean checkpoint and may include partial work from the next phase.

---

## Failure Modes

| Situation | Response |
| --- | --- |
| Dependency conflict blocks upgrade | Audit the conflict graph with `npm ls` or `uv tree`. Identify the constraining package. Find an alternative or fork. Document the decision. |
| Test suite drops below baseline after phase | Do not proceed to the next phase. Isolate the regression to specific tests. Fix before continuing. |
| Codemod produces incorrect transformations | Review a sample of 10 transformed files manually. File a bug against the codemod. Apply manual corrections where needed. |
| Build fails after dependency upgrade | Run `tsc --noEmit` (TypeScript) or `pyright` to surface type errors separately from build errors. Fix type errors first. |
| Performance regression detected post-migration | Benchmark the critical path before reverting. Profile with `py-spy` or `clinic.js`. May be config, not the upgrade itself. |
| Rollback needed mid-migration | Run `scripts/rollback.sh phase-N`. Do not attempt to "fix forward" under time pressure unless the window is short. |
| Monorepo internal imports break after restructure | Run `ast-grep` to find all cross-package relative imports. Update to workspace package names systematically. |
| Health check script shows new failures | Compare output diffs carefully. Distinguish intentional behavior changes from regressions. Update health check expectations if change is intentional. |

---

## Integration with Mega-Mind

`migration-upgrader` is invoked by:

- `tech-lead` when the tech stack needs a version refresh
- `legacy-archaeologist` after a codebase audit reveals critical version debt
- `security-reviewer` when a dependency has a known CVE requiring upgrade

`migration-upgrader` hands off to:

- `python-patterns` when the migration involves Python idiom updates
- `test-genius` to expand the test suite coverage before beginning a high-risk migration
- `eval-harness` to define pre/post migration quality gates
- `finishing-a-development-branch` once migration is validated and ready to merge
