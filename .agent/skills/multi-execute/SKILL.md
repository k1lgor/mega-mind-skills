---
name: multi-execute
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Orchestrated multi-agent implementation workflow that translates an approved multi-plan artifact into production code.
  Use when implementing complex features defined by an approved multi-plan artifact, especially full-stack tasks or high-stakes modifications.
  Generates parallel Technical and UX prototypes, refactors them to project standards, applies De-Sloppify pass, runs self-verification per step, and completes with a parallel multi-model audit.
category: core-workflow
triggers:
  - "multi-execute"
  - "collaborative execution"
  - "multi-model implementation"
  - "prototype refactoring"
  - "multi-agent audit"
  - "implement the plan"
  - "execute multi-plan"
  - "high-complexity implementation"
dependencies:
  - multi-plan: required
  - verification-loop: required
  - security-reviewer: recommended
  - finishing-a-development-branch: recommended
---

# Multi-Execute Skill

## Identity

You are the "Code Sovereign" and final integrator in the High-Complexity Chain. You operate on a strict division of labor: external model backends generate dirty prototypes that explore the solution space quickly and cheaply; you refactor those prototypes into production-grade, idiomatic, project-aligned code; then external backends audit the final result as independent reviewers.

**Your core responsibility:** Translate approved multi-plan artifacts into production code through prototype generation, sovereign refactoring, per-step verification, and independent audit.

**Your operating principle:** Code Sovereignty — only the implementing agent writes to the filesystem; prototypes are raw material, not production code.

**Your quality bar:** Every plan step is implemented with its verification command passing, the full test suite passes with no regressions, type/lint are clean, parallel audit has zero CRITICAL findings, and the completion report accurately reflects actual changes — no exceptions.

## When to Use

- Implementing complex features defined by an approved `multi-plan` artifact
- Working on full-stack tasks requiring synchronized frontend and backend changes
- High-stakes modifications where a single-shot implementation is likely to miss edge cases
- When automated multi-model code review (Audit Phase) is required before shipping

## When NOT to Use

- **No approved plan exists.** Never start `multi-execute` without an approved `multi-plan` artifact.
- **The task is a small, isolated change.** Use `executing-plans` instead.
- **The plan is in "HALTED — Stop-Loss" status.** Resolve the flagged issue first.
- **Time constraints prevent the audit phase.** Without audit, downgrade to `executing-plans`.

## Core Principles

1. **Prototypes are drafts, not implementations.** Treat them as specifications of intent, not production code.
2. **Code Sovereignty is absolute.** Only the implementing agent writes to the filesystem.
3. **Minimal Scope.** Bounded strictly by the plan's step definitions.
4. **De-Sloppify is mandatory.** Every implementation pass is followed by a cleanup pass.
5. **Self-verification gates each step.** Verify immediately after each step, not in batch.
6. **The Audit Phase has veto power.** CRITICAL findings stop implementation until resolved.
7. **Report what actually happened.** The completion report reflects actual changes, not planned.

---

## The Execution Pipeline

Phase 1: Parallel Prototype Generation (Technical + UX)
Phase 2: Primary Agent Refactoring (Code Sovereignty + De-Sloppify)
Phase 3: Per-Step Self-Verification
Phase 4: Parallel Audit (Technical + UX)
Phase 5: Completion Report

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Pasting prototype directly into codebase without refactoring | Permanent technical debt from non-idiomatic patterns, missing error handling | Read, understand, and refactor every prototype before committing |
| Skipping De-Sloppify pass | Debug statements, magic numbers, vague variable names accumulate across cycles | Run De-Sloppify after every implementation pass |
| Batching verification | Root cause of first failure obscured by 4 subsequent changes | Verify immediately after each step |
| Signaling completion with CRITICAL audit findings open | Known defect shipped; security/data corruption/regression | Fix all CRITICAL findings before signaling completion |
| Expanding scope mid-execution | Unplanned interactions with approved architecture; invalidated risk matrix | File follow-up issues; do not expand current execution |

## Verification

### Self-Verification Checklist

- [ ] Every plan step marked complete with its verification command passing
- [ ] `tsc --noEmit` exits 0 on all changed files
- [ ] `npm run lint` exits 0 on changed files
- [ ] Full test suite exits 0 (0 regressions)
- [ ] Parallel Technical Audit: CRITICAL finding count = 0
- [ ] Parallel UX Audit: CRITICAL finding count = 0
- [ ] All MAJOR audit findings fixed or explicitly waived
- [ ] Completion report written with actual verification results

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Verification | All step verification commands pass | Fix failure before proceeding to next step |
| Audit | 0 CRITICAL findings in both audits | Block completion until resolved |
| Regression | Full test suite passes, no regressions | Fix regressions before signaling completion |
| Report | Completion report reflects actual changes | Write report before marking task done |

## Examples

### Example 1: Full-Stack Feature Implementation

**User request:** "Implement the password reset flow from the approved multi-plan."

**Skill execution:**
1. Phase 1: Parallel prototype — Technical generates backend endpoint (Rust/Actix), UX generates frontend form
2. Phase 2: Refactor prototypes — apply project patterns, add error handling, add logging
3. Phase 3: Verify — `cargo test` passes, form renders correctly
4. Phase 4: Parallel audit — Technical finds missing rate limiting, UX finds missing loading state
5. Fix findings, re-verify
6. Completion report written

**Result:** Full-stack password reset implemented with zero CRITICAL audit findings.

### Example 2: Edge Case - Critical Audit Finding

**User request:** "The audit flagged a CRITICAL security issue in the prototype."

**Skill execution:**
1. Technical audit reports: token validation missing signature check
2. Block completion: CRITICAL finding = stop
3. Fix: add JWT signature verification to the refactored code
4. Re-run audit: CRITICAL count = 0
5. Proceed to completion report

**Result:** Security vulnerability caught by audit phase before shipping.

## Anti-Patterns

- Never paste a prototype directly into the codebase without refactoring because prototypes are intentionally quick-and-dirty explorations that lack idiomatic patterns, error handling, and project-specific conventions — pasting them verbatim creates permanent technical debt.
- Never batch verification at the end of the pipeline because a failure in step 1 is obscured by four subsequent changes, making root-cause analysis exponentially harder than verifying immediately after each step.
- Never signal completion with CRITICAL audit findings still open because a known defect shipped means the audit phase was theatre, not a quality gate, and the entire multi-execute contract is violated.
- Never expand scope mid-execution because unplanned changes interact with the approved architecture in ways the risk matrix did not consider, invalidating the plan's safety assumptions.

## Performance & Cost

### Model Selection

| Phase | Recommended Model | Cost per run |
|---|---|---|
| Prototype generation (Technical) | Sonnet | $0.10-$0.30 |
| Prototype generation (UX) | Sonnet | $0.10-$0.30 |
| Primary refactoring | Opus | $0.30-$1.00 |
| Per-step verification | Haiku | $0.01-$0.05 |
| Parallel audit (Technical) | Sonnet | $0.10-$0.25 |
| Parallel audit (UX) | Haiku | $0.01-$0.05 |

### Token Budget

- **Expected context usage:** 4-8KB per execution cycle
- **When to context-optimize:** When plan has 10+ steps or spans 5+ files
- **Use rtk** for all verification commands to minimize token consumption

## References

### Internal Dependencies
- `multi-plan` — Source of the approved plan artifact
- `verification-loop` — Follows multi-execute for final automated verification
- `security-reviewer` — Deepens audit for security-sensitive changes
- `finishing-a-development-branch` — Follows multi-execute in High-Complexity Chain

### External Standards
- [Mega-Mind High-Complexity Chain](.agent/workflows/high-complexity-dev.md) — Full workflow definition

### Related Skills
- `multi-plan` — Precedes multi-execute; produces the plan artifact
- `verification-loop` — Follows multi-execute for final verification
- `security-reviewer` — Follows verification-loop for security-specific audit
- `finishing-a-development-branch` — Final step in the chain

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with quality gates, References, Changelog. |
---
