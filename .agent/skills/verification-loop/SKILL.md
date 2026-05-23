---
name: verification-loop
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Scope-aware tiered verification system (Tier 1 Surface / Tier 2 Standard / Tier 3 Deep) with continuous quick-check mode. Classifies change risk before running phases to avoid over-testing cosmetic changes while guaranteeing deep verification for risky ones. Replaces ad-hoc "does this work?" checks with a rigorous, structured verification that produces a machine-readable report. Use before any PR or major handoff.
triggers:
  - "/verify"
  - "verification loop"
  - "run verification"
  - "is this ready for PR"
  - "pre-PR check"
  - "quality gate"
  - "verify all checks pass"
  - "mark as done"
  - "complete this task"
  - "is this done"
  - "verify this works"
---

# Verification Loop

## Identity

You are a verification specialist. You run a structured, repeatable 6-phase check that produces a clear READY / NOT READY verdict — not a vague "it looks good." Every phase has a pass/fail outcome. You don't skip phases.

## When to Use

- After completing a feature or significant code change
- Before creating or updating a PR
- Before marking any task complete / saying "I'm done"
- After refactoring
- Periodically during long sessions (every 15–20 minutes)
- When you want a comprehensive quality gate

## When NOT to Use

- Minor typo or comment-only changes — run a quick build check instead of all 6 phases
- During rapid exploratory iteration — run full verification before PR, not after every experiment
- As a substitute for writing tests — if Phase 4 fails because tests don't exist, write them
- Mid-implementation when code is intentionally incomplete
- When the task is purely exploratory/research with no implementation output
- When asked for a partial review of one aspect — use `requesting-code-review` instead

---

## The 6-Phase Verification Loop

### Phase 0: Pre-Check — De-Sloppify

Before running any automated checks, scan all changed files for artifacts.

> See: `.agent/shared/DE-SLOPPIFY.md` for the full checklist.

```bash
grep -lE "console\.log|debugger|TODO|FIXME|pdb\.set_trace|import pdb"
```

- [ ] No debug code (console.log, print, debugger, breakpoints)
- [ ] No resolved TODOs left as comments
- [ ] No commented-out old code
- [ ] No unused imports
- [ ] Consistent formatting across all changed files

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

```bash
# Check for hardcoded secrets / API keys
git diff --name-only HEAD | xargs grep -nE "(sk-|api_key|API_KEY|secret|password)[[:space:]]*=[[:space:]]*['\"][^'\"]{10}" 2>/dev/null | head -10

# Check for console.log in source (not test) files
grep -rn "console\.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | grep -v ".test." | head -10

# JavaScript projects
rtk bun pm untrusted (or rtk npm audit) --audit-level=high 2>&1 | tail -20

# Python safety check
safety check 2>&1 | tail -20
```

---

### Phase 6: Diff Review

```bash
git diff --stat HEAD
git diff --name-only HEAD
git diff HEAD
```

Review checklist for each changed file:

- [ ] Changes are intentional (no accidental whitespace or debug edits)
- [ ] Error handling covers new code paths
- [ ] Edge cases considered (empty input, null, 0, max values)
- [ ] No obvious performance issues (N+1 queries, unbounded loops)

---

### Phase 7: Manual Verification

Actually use the feature:

- [ ] Feature works as expected
- [ ] Edge cases handled (empty input, error states, boundary values)
- [ ] Error states are graceful
- [ ] Loading states are appropriate
- [ ] Mobile/responsive (if applicable)
- [ ] Accessibility (if applicable)
- [ ] No console errors in browser/runtime

### Phase 8: Integration Check

Verify the change doesn't break other parts:

- [ ] Related features still work
- [ ] Navigation still works
- [ ] API integrations still work
- [ ] Database operations still work

> See: `.agent/shared/VERIFICATION-GATE.md` for the canonical gate definition.

---

### Phase 9: Eval Harness (Complex Features)

For features with acceptance criteria, run a structured eval:

```markdown
## Eval: [Feature Name]

### Acceptance Criteria (from plan)

- [ ] AC1: [criterion from original plan]
- [ ] AC2: [criterion]

### Evaluation

| Criterion | Status | Evidence                         | Notes          |
| --------- | ------ | -------------------------------- | -------------- |
| AC1       | ✅     | Test #14 passes, manual verified |                |
| AC2       | ✅     | API returns expected shape       |                |
| AC3       | ⚠️     | Works but edge case X uncovered  | Add to backlog |

### Result

- PASS: All required criteria met
- PARTIAL: [list unmet criteria]
- FAIL: [blocking criteria not met]
```

**Only non-blocking gaps are acceptable for PASS.**

---

## Output: Verification Report

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
Phase 7 - Manual:       ✅ PASS  (feature verified end-to-end)
Phase 8 - Integration:  ✅ PASS  (related features unaffected)
Phase 9 - Eval:         ✅ PASS  (all AC met)

Overall:  ✅ READY for PR
```

## Failure Template

```
VERIFICATION REPORT
═══════════════════════════════════════════

Phase 0 - De-Sloppify:  ✅ PASS
Phase 1 - Build:        ✅ PASS
Phase 2 - Types:        ❌ FAIL  (3 errors — see below)
Phase 3 - Lint:         [skipped — fix types first]
Phase 4 - Tests:        [skipped]
...

Overall:  ❌ NOT READY

Type Errors to Fix:
1. src/auth/tokens.ts:47 — Type 'string | undefined' not assignable to 'string'
2. src/api/users.ts:103 — Property 'avatarUrl' does not exist on type 'User'
```

---

## Common Verification Failures

| Failure Type   | Example                                                 | Fix                               |
| -------------- | ------------------------------------------------------- | --------------------------------- |
| Tests Failing  | New field in model not in test fixtures                 | Update fixtures to match model    |
| Build Failing  | `Type 'string \| undefined' not assignable to 'string'` | Add null check with default value |
| Manual Failure | Feature works but shows console error                   | Add error boundary component      |

---

## Tiered Verification (Scope-Based Depth Selection)

Instead of always running all 10 phases, assess the change scope first and pick the
appropriate tier. This prevents a one-line CSS fix from running 10 phases, while still
guaranteeing deep verification for high-risk changes.

### Step 0: Scope Classification

Classify the change before running any phase:

| Classification | Definition                                                             | Examples                                                                      |
| -------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Cosmetic**   | No logic change. Docs, comments, whitespace, config formatting.        | README typo, `.gitignore` entry, comment update, indentation fix              |
| **Standard**   | Code change within one module. No new dependencies, no schema changes. | New component, utility function, bug fix in existing logic                    |
| **Deep**       | Cross-cutting, risky, or security-sensitive.                           | Schema migration, auth logic, payment flow, new dependency, public API change |

### Step 1: Pick the Tier

| Tier                  | When                         | Phases to Run                                  |
| --------------------- | ---------------------------- | ---------------------------------------------- |
| **Tier 1 — Surface**  | Cosmetic changes only        | Phase 0 (De-Sloppify) → Phase 1 (Build)        |
| **Tier 2 — Standard** | Standard changes             | Phase 0 → 1 → 2 (Types) → 3 (Lint) → 4 (Tests) |
| **Tier 3 — Deep**     | Deep changes + before any PR | All 10 phases (0-9)                            |

```
DECISION RULES:
- Change touches ONLY .md, .yml, .gitignore?  → Tier 1 (Surface)
- Change touches ONLY one module, no migrations?  → Tier 2 (Standard)
- Change adds/changes: auth, payments, DB schema, deps, public API?  → Tier 3 (Deep)
- Unsure?  → Default to Tier 3 (Deep)
- Running before a PR?  → Always Tier 3 (Deep)
```

### Quick Reference

```
TIER 1 (Surface — <30s):
  0. De-Sloppify → 1. Build

TIER 2 (Standard — <2min):
  0. De-Sloppify → 1. Build → 2. Types → 3. Lint → 4. Tests

TIER 3 (Deep — before PR):
  All 10 phases (0-9)
```

---

## Decision Matrix

| Build | Types | Lint | Tests | Manual | PR Ready?                |
| ----- | ----- | ---- | ----- | ------ | ------------------------ |
| ❌    | —     | —    | —     | —      | **NO — fix build first** |
| ✅    | ❌    | —    | —     | —      | **NO — fix types**       |
| ✅    | ✅    | ❌   | —     | —      | **NO — fix lint**        |
| ✅    | ✅    | ✅   | ❌    | —      | **NO — fix tests**       |
| ✅    | ✅    | ✅   | ✅    | ❌     | **NO — manual verify**   |
| ✅    | ✅    | ✅   | ✅    | ✅     | **YES**                  |

---

## Failure Modes

| Failure                                                      | Cause                                                | Recovery                                                                    |
| ------------------------------------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| Loop exits early because agent misidentifies warning as pass | Exit condition checks absence of errors not warnings | Treat warnings as failures for blocking phases; use `--strict` flags        |
| Verification criteria defined after implementation           | Criteria shaped by what passes, not what should pass | Define acceptance criteria before writing code                              |
| Loop runs against wrong environment                          | Dev used instead of staging                          | Parameterise verification target; default to staging                        |
| Results not recorded after loop                              | Agent runs phases but does not persist outcome       | Write phase results to structured log after each phase                      |
| Phase gate skipped due to ambiguous output                   | Agent interprets ambiguous output as pass            | Default ambiguous output to FAIL; require explicit pass signal              |
| Build passes but tests not run                               | Test command omitted; CI and local scripts diverged  | Consolidate into a single script; run locally before every completion claim |
| Coverage threshold met by trivial tests                      | Tests execute code without asserting behaviour       | Require meaningful assertions; check assertion-to-line ratio                |
| Regression in adjacent module not caught                     | Verification scoped to changed files only            | Run full integration test suite; check import graph for affected consumers  |

## Anti-Patterns

- Never define verification criteria after implementation — criteria defined post-hoc are shaped by what already passes.
- Never skip a phase gate to save time — an unverified phase can mask a failure that makes all subsequent phases meaningless.
- Never run verification only against the development environment — staging/production bugs remain invisible until deployment.
- Never treat a warning as a pass in a blocking phase — warnings often become errors under slightly different inputs.
- Never exit the loop without recording results — the next run cannot compare against a baseline.
- Never redefine a phase's pass criterion mid-loop — changing goalposts invalidates all previous phases.
- Never mark a task complete before running the full verification — partial verification misses regressions in adjacent modules.
- Never count a green build as sufficient — the build may succeed while tests are skipped or not yet written.
- Never skip verification because "it's a small change" — change size has no correlation with regression probability.
- Never accept a passing linter as proof of correctness — linting checks style, not logic.

## Self-Verification Checklist

- [ ] Scope classified before phases: classification is recorded (Cosmetic / Standard / Deep)
- [ ] Tier selected matches scope: Tier 1 for Cosmetic, Tier 2 for Standard, Tier 3 for Deep or PR
- [ ] All phases for chosen tier run in order and each has PASS or documented exception
- [ ] Build passed before Phase 2 (exits 0)
- [ ] Test coverage >= 80% confirmed (Tier 2+)
- [ ] Security scan: `grep -rnE "password[[:space:]]*=|api_key[[:space:]]*=|sk-" src/` = 0 matches (Tier 3)
- [ ] Diff review confirmed all changes intentional
- [ ] `rtk bun test` exits code 0 (zero test failures); `rtk tsc` zero type errors; `rtk lint` no errors
- [ ] Manual walkthrough confirms expected behavior end-to-end (Tier 3)
- [ ] Verification Report produced with READY / NOT READY verdict

## Success Criteria

This skill is complete when: 1) All phases have been run and each has a PASS or documented acceptable exception. 2) The Verification Report is produced and shows an overall READY verdict. 3) Any NOT READY verdict has specific fixes listed and the loop is re-run after fixing. 4) The **Handoff block** has been emitted with `next_skill` pointing to `requesting-code-review` (or the next chain step) and `status: completed`.

## Tips

> **Run phases in order** — each phase builds on the previous.
> **Phases 0-5 are automated** (code + build + type + lint + test + security).
> **Phases 6-9 are manual/eval** (diff review + manual walkthrough + integration check + eval harness).

- **Never open a PR without Phase 4 passing** — failing tests are resolved by authors, not reviewers
- **Use RTK wrappers** for all phases to save context: `rtk bun test`, `rtk tsc`, `rtk lint`
- **Save the report** — paste it in the PR description so reviewers see it immediately
- **Phase 5 is the most overlooked** — hardcoded API keys in code are embarrassing and dangerous
- **Don't skip manual testing** — automated tests don't catch everything; check in different environments if possible
