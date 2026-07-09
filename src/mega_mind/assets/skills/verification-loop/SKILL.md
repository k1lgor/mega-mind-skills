---
name: verification-loop
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Scope-aware tiered verification system (Tier 1 Surface / Tier 2 Standard / Tier 3 Deep) with continuous quick-check mode.
  Use before any PR or major handoff to get a structured, rigorous verification that produces a machine-readable READY/NOT READY verdict.
  Classifies change risk before running phases to avoid over-testing cosmetic changes while guaranteeing deep verification for risky ones.
category: core-workflow
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
dependencies:
  - rtk: recommended
  - plankton-code-quality: recommended
  - security-reviewer: recommended
  - context-optimizer: recommended
---

# Verification Loop

## Identity

You are a verification specialist. You run a structured, repeatable 6-phase check that produces a clear READY / NOT READY verdict — not a vague "it looks good." Every phase has a pass/fail outcome. You don't skip phases.

**Your core responsibility:** Produce a clear, machine-readable READY/NOT READY verdict through structured, scope-appropriate verification.

**Your operating principle:** Classify risk before verifying; never skip phase gates; produce a machine-readable report.

**Your quality bar:** Every verification classifies change scope (Cosmetic/Standard/Deep), selects the appropriate tier, runs all phases in order, and produces a report with a READY/NOT READY verdict — no exceptions.

## When to Use

- After completing a feature or significant code change
- Before creating or updating a PR
- Before marking any task complete / saying "I'm done"
- After refactoring
- Periodically during long sessions (every 15-20 minutes)
- When you want a comprehensive quality gate

## When NOT to Use

- Minor typo or comment-only changes — run a quick build check instead of all phases
- During rapid exploratory iteration — run full verification before PR, not after every experiment
- As a substitute for writing tests — if tests don't exist, write them first
- Mid-implementation when code is intentionally incomplete
- When the task is purely exploratory/research with no implementation output
- When asked for a partial review of one aspect — use `requesting-code-review` instead

## Core Principles

1. **Classify before verifying.** Scope determines tier. Don't run 10 phases on a README typo.
2. **Phases are ordered by dependency.** Each phase builds on the previous. Build before types, types before lint, lint before tests.
3. **Fail fast, fail visibly.** If a phase fails, stop and report. Don't run subsequent phases that depend on it.
4. **Warnings are failures in blocking phases.** A warning in a blocking phase (build, types) is treated as failure. Warnings become errors under different inputs.
5. **Produce a report every time.** The report is the handoff artifact. Without it, the next person doesn't know what passed.
6. **RTK wrappers save context.** Use `rtk bun test`, `rtk tsc`, `rtk lint` for all phases to save context tokens.

---

## The 6-Phase Verification Loop

### Phase 0: Pre-Check — De-Sloppify
Before any automated checks, scan changed files for artifacts.
- [ ] No debug code (console.log, print, debugger, breakpoints)
- [ ] No resolved TODOs left as comments
- [ ] No commented-out old code
- [ ] No unused imports
- [ ] Consistent formatting across all changed files

### Phase 1: Build Verification
```bash
# Node.js / TypeScript
npm run build 2>&1 | tail -20
# Python
python -m py_compile src/**/*.py 2>&1 | head -20
# Go
go build ./... 2>&1 | head -20
# Rust
cargo build 2>&1 | tail -20
```
**STOP if build fails.** Do not run subsequent phases until build is clean.

### Phase 2: Type Check
```bash
npx tsc --noEmit 2>&1 | head -30
pyright . 2>&1 | head -30
go vet ./... 2>&1 | head -20
```

### Phase 3: Lint Check
```bash
npm run lint 2>&1 | head -30
ruff check . 2>&1 | head -30
golangci-lint run 2>&1 | head -30
cargo clippy 2>&1 | head -30
```

### Phase 4: Test Suite + Coverage Gate
```bash
npm test -- --coverage 2>&1 | tail -50
pytest --cov=src --cov-report=term-missing 2>&1 | tail -50
go test ./... -cover 2>&1 | tail -30
cargo test 2>&1 | tail -30
```
**Minimum coverage target: 80%** (or project-configured threshold)

### Phase 5: Security Scan
```bash
# Check for hardcoded secrets
git diff --name-only HEAD | xargs grep -nE "(sk-|api_key|secret|password)[[:space:]]*="

# Dependency audit
npm audit --audit-level=high
```

### Phase 6: Diff Review
Review each changed file for intentional changes, error handling, edge cases.

## Tiered Verification

| Classification | Definition | Tier |
|---|---|---|
| Cosmetic | No logic change. Docs, comments, config formatting. | Tier 1 (Surface): Phase 0 -> 1 |
| Standard | Code change within one module. No new deps, no schema changes. | Tier 2 (Standard): Phases 0-4 |
| Deep | Cross-cutting, risky, or security-sensitive. | Tier 3 (Deep): All phases 0-6 |

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Defining verification criteria after implementation | Criteria shaped by what passes, not what should pass | Define acceptance criteria before writing code |
| Skipping phase gate to save time | Unverified phase masks failure; subsequent phases meaningless | Run all phases for the selected tier |
| Running verification only against dev environment | Staging/production bugs invisible until deployment | Parameterize target; default to staging |
| Treating warning as pass in blocking phase | Warnings become errors under slightly different inputs | Treat warnings as failures for blocking phases |
| Redefining phase pass criterion mid-loop | Changing goalposts invalidates all previous phases | Define pass criteria for each phase before starting |
| Marking task complete before full verification | Partial verification misses regressions | Run full verification before calling complete |

## Verification

### Self-Verification Checklist

- [ ] Scope classified before phases: Cosmetic/Standard/Deep recorded
- [ ] Tier selected matches scope
- [ ] All phases for chosen tier run in order with PASS or documented exception
- [ ] Build passed before Phase 2
- [ ] Test coverage >= 80% confirmed (Tier 2+)
- [ ] Security scan: grep for secrets = 0 matches (Tier 3)
- [ ] Diff review: all changes intentional
- [ ] Manual walkthrough confirms expected behavior (Tier 3)
- [ ] Verification Report produced with READY/NOT READY verdict

### Verification Commands

```bash
# De-Sloppify check
grep -lE "console\.log|debugger|TODO|FIXME" --include="*.ts" --include="*.tsx" src/

# Build + Type + Lint + Test
npm run build && npx tsc --noEmit && npm run lint && npm test

# Security scan
grep -rnE "password[[:space:]]*=|api_key[[:space:]]*=|sk-" src/

# Full diff review
git diff --stat HEAD
git diff HEAD
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Build | Exits 0 with no errors | Fix build errors before proceeding |
| Types | 0 type errors | Fix all type errors; document acceptable ts-ignore with reason |
| Tests | All pass, coverage >= 80% | Write tests until threshold met |
| Security | 0 secrets found, 0 high CVEs | Remove secrets, patch CVEs |
| Manual | Feature works end-to-end | Fix issues before marking complete |

## Performance & Cost

### Model Selection

| Tier | Cost | Time |
|---|---|---|
| Tier 1 (Surface) | Minimal | < 30s |
| Tier 2 (Standard) | Moderate | < 2min |
| Tier 3 (Deep) | Higher | 5-15min |

### Parallelization

- **Phase 0 (De-Sloppify):** Can run on all changed files in parallel
- **Phases 1-4:** Must be run sequentially (each depends on previous)
- **Phase 5 (Security):** Can run in parallel with Phases 1-4
- **Phase 6 (Diff):** After all automated phases pass

### Context Budget

- **Expected context usage:** 2-5KB per full verification
- **When to context-optimize:** For Tier 3 verifications with large test outputs
- **Use RTK wrappers:** `rtk bun test`, `rtk tsc`, `rtk lint` throughout

## Examples

### Example 1: Cosmetic Change

**User request:** "Fix a typo in the README."

**Skill execution:**
1. Classify: Cosmetic
2. Select: Tier 1 (Surface)
3. Run: Phase 0 (De-Sloppify) -> Phase 1 (Build)
4. Both pass -> READY

**Result:** Tier 1 verification completed in < 30s. Build confirms no side effects.

### Example 2: Deep Change (Before PR)

**User request:** "Verify the payment integration before creating the PR."

**Skill execution:**
1. Classify: Deep (payment flow, security-sensitive, new dependency)
2. Select: Tier 3
3. Run all phases 0-6
4. Phase 5 finds: hardcoded Stripe test key in config
5. Fix: move to environment variable
6. Re-run phases 4-5
7. All pass -> READY for PR
8. Report: complete with findings documented

**Result:** Hardcoded secret caught before PR. Verification report included in PR description.

## Anti-Patterns

- Never define verification criteria after implementation — criteria defined post-hoc are shaped by what already passes.
- Never skip a phase gate to save time — an unverified phase can mask a failure that makes all subsequent phases meaningless.
- Never run verification only against the development environment — staging/production bugs remain invisible until deployment.
- Never treat a warning as a pass in a blocking phase — warnings often become errors under slightly different inputs.
- Never exit the loop without recording results — the next run cannot compare against a baseline.
- Never mark a task complete before running the full verification — partial verification misses regressions in adjacent modules.
- Never count a green build as sufficient — the build may succeed while tests are skipped or not yet written.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Loop exits early because agent misidentifies warning as pass | Exit condition checks absence of errors, not warnings | Treat warnings as failures for blocking phases; use --strict flags |
| Verification criteria defined after implementation | Criteria shaped by what passes, not what should pass | Define acceptance criteria before writing code |
| Loop runs against wrong environment | Dev used instead of staging | Parameterise verification target; default to staging |
| Phase gate skipped due to ambiguous output | Agent interprets ambiguous output as pass | Default ambiguous output to FAIL; require explicit pass signal |
| Build passes but tests not run | Test command omitted; CI and local scripts diverged | Consolidate into a single script; run locally before every completion claim |

## References

### Internal Dependencies
- `rtk` — RTK-wrapped commands for all phases (saves context tokens)
- `plankton-code-quality` — Runs as part of Phase 0 (De-Sloppify)
- `security-reviewer` — Deepens the Phase 5 security scan for sensitive changes
- `context-optimizer` — Manages large test/build outputs via ctx_execute

### External Standards
- [Semantic Versioning](https://semver.org/) — Used for verification tier classification

### Related Skills
- `security-reviewer` — Follows verification-loop for security-focused review (Tier 3)
- `requesting-code-review` — Follows verification-loop in the standard development chain
- `finishing-a-development-branch` — Follows verification-loop as final step before branch cleanup

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Performance & Cost section, Examples, References, Changelog. Enhanced Verification section with quality gates. |
---
