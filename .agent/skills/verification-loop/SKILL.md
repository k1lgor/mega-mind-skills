---
name: verification-loop
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Comprehensive 6-phase verification system with continuous mode. Replaces ad-hoc "does this work?" checks with a rigorous, structured verification that produces a machine-readable report. Use before any PR or major handoff.
triggers:
  - "/verify"
  - "verification loop"
  - "run verification"
  - "is this ready for PR"
  - "pre-PR check"
  - "quality gate"
  - "verify all checks pass"
---

# Verification Loop

## Identity

You are a verification specialist. You run a structured, repeatable 6-phase check that produces a clear READY / NOT READY verdict — not a vague "it looks good." Every phase has a pass/fail outcome. You don't skip phases.

## When to Use

- After completing a feature or significant code change
- Before creating or updating a PR
- After refactoring
- Periodically during long sessions (every 15–20 minutes)
- When you want a comprehensive quality gate

---

## The 6-Phase Verification Loop

### Phase 0: Pre-Check — De-Sloppify

Before running any automated checks, scan all changed files for artifacts:

```bash
# Find debug artifacts in changed files
git diff --name-only HEAD | xargs grep -l "console\.log\|debugger\|TODO\|FIXME\|pdb\.set_trace\|import pdb" 2>/dev/null
```

- [ ] No debug code (console.log, print, debugger, breakpoints)
- [ ] No resolved TODOs left as comments
- [ ] No commented-out old code
- [ ] No unused imports

> Fix these NOW. Running tests against messy code just makes the output harder to read.

---

### Phase 1: Build Verification

```bash
# Node.js / TypeScript
bun run build (or npm run build) 2>&1 | tail -20

# Python
python -m py_compile src/**/*.py 2>&1 | head -20

# Go
go build ./... 2>&1 | head -20

# Rust
cargo build 2>&1 | tail -20
```

**STOP if build fails.** Do not run subsequent phases until build is clean.

---

### Phase 2: Type Check

```bash
# TypeScript
npx tsc --noEmit 2>&1 | head -30

# Python (pyright)
pyright . 2>&1 | head -30

# Go (included in build)
go vet ./... 2>&1 | head -20
```

Report all type errors. Fix critical ones. Document any acceptable `@ts-ignore` with a reason comment.

---

### Phase 3: Lint Check

```bash
# JavaScript / TypeScript
bun run lint (or npm run lint) 2>&1 | head -30
# or: npx eslint src/ --max-warnings 0

# Python
ruff check . 2>&1 | head -30

# Go
golangci-lint run 2>&1 | head -30

# Rust
cargo clippy 2>&1 | head -30
```

---

### Phase 4: Test Suite + Coverage Gate

```bash
# JavaScript / TypeScript
bun test (or npm test) -- --coverage 2>&1 | tail -50

# Python
pytest --cov=src --cov-report=term-missing 2>&1 | tail -50

# Go
go test ./... -cover 2>&1 | tail -30

# Rust
cargo test 2>&1 | tail -30
```

**Minimum coverage target: 80%** (or project-configured threshold)

Report format:

```
Total tests:  47
  Passed:     47
  Failed:      0
  Skipped:     2

Coverage:    84% (target: 80%) ✅
```

If coverage is below target → write tests before proceeding.

---

### Phase 5: Security Scan

Quick automated checks for common issues:

```bash
# Check for hardcoded secrets / API keys
git diff --name-only HEAD | xargs grep -nE "(sk-|api_key|API_KEY|secret|password)\s*=\s*['\"][^'\"]{10}" 2>/dev/null | head -10

# Check for console.log in source (not test) files
grep -rn "console\.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | grep -v ".test." | head -10

# rtk bun pm untrusted (or rtk npm audit) (JavaScript projects)
rtk bun pm untrusted (or rtk npm audit) --audit-level=high 2>&1 | tail -20

# Python safety check
safety check 2>&1 | tail -20
```

---

### Phase 6: Diff Review

```bash
# Summary of what changed
git diff --stat HEAD

# Changed file list
git diff --name-only HEAD

# Show full diff for review
git diff HEAD
```

Review checklist for each changed file:

- [ ] Changes are intentional (no accidental whitespace or debug edits)
- [ ] Error handling covers new code paths
- [ ] Edge cases considered (empty input, null, 0, max values)
- [ ] No obvious performance issues (N+1 queries, unbounded loops)

---

## Output: Verification Report

After running all phases, produce this summary:

```
VERIFICATION REPORT
═══════════════════════════════════════════

Phase 0 - De-Sloppify:  ✅ PASS  (no artifacts found)
Phase 1 - Build:        ✅ PASS
Phase 2 - Types:        ✅ PASS  (0 errors)
Phase 3 - Lint:         ✅ PASS  (0 errors, 2 warnings — documented)
Phase 4 - Tests:        ✅ PASS  (47/47, 84% coverage)
Phase 5 - Security:     ✅ PASS  (no secrets found, 0 high CVEs)
Phase 6 - Diff:         ✅ PASS  (8 files changed, all intentional)

Overall:  ✅ READY for PR

Notes:
- ESLint warning on line 42: "no-unused-vars" for debug variable — removed
- Coverage on new auth module: 91% (well above threshold)
```

---

## Failure Template

When a phase fails:

```
VERIFICATION REPORT
═══════════════════════════════════════════

Phase 0 - De-Sloppify:  ✅ PASS
Phase 1 - Build:        ✅ PASS
Phase 2 - Types:        ❌ FAIL  (3 errors — see below)
Phase 3 - Lint:         [skipped — fix types first]
Phase 4 - Tests:        [skipped]
Phase 5 - Security:     [skipped]
Phase 6 - Diff:         [skipped]

Overall:  ❌ NOT READY

Type Errors to Fix:
1. src/auth/tokens.ts:47 — Type 'string | undefined' not assignable to 'string'
   Fix: Add null check → `token ?? ""` or make param `token?: string`
2. src/api/users.ts:103 — Property 'avatarUrl' does not exist on type 'User'
   Fix: Add avatarUrl to User type in types.ts
3. src/api/users.ts:104 — (same cause as #2)
```

---

## Continuous Mode

For long development sessions, run a lighter check every 15 minutes or after major changes:

```
QUICK CHECK (every 15 min or after each function/component):
  1. Build ─ does it compile?
  2. Types ─ any new type errors?
  3. Tests ─ do existing tests still pass?

FULL VERIFY (before PR):
  All 6 phases
```

Set a mental checkpoint:

- After completing each function or component
- Before moving to the next logical task
- Before ending a session

---

## Decision Matrix

| Build | Types | Lint | Tests | Security | PR Ready?                |
| ----- | ----- | ---- | ----- | -------- | ------------------------ |
| ❌    | —     | —    | —     | —        | **NO — fix build first** |
| ✅    | ❌    | —    | —     | —        | **NO — fix types**       |
| ✅    | ✅    | ❌   | —     | —        | **NO — fix lint**        |
| ✅    | ✅    | ✅   | ❌    | —        | **NO — fix tests**       |
| ✅    | ✅    | ✅   | ✅    | ❌       | **NO — fix security**    |
| ✅    | ✅    | ✅   | ✅    | ✅       | **YES**                  |

---

## Tips

- **Run phases in order** — each phase builds on the previous
- **Never open a PR without Phase 4 passing** — failing tests are resolved by reviewers, not authors
- **Use RTK wrappers** for all phases to save context: `rtk bun test (or npm test)`, `rtk tsc`, `rtk lint`
- **Save the report** — paste it in the PR description so reviewers see it immediately
- **Phase 5 is the most overlooked** — hardcoded API keys in code are embarrassing and dangerous
