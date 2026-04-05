---
name: multi-plan
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Multi-model collaborative planning for high-complexity tasks. Distributes requirements to specialized analysis perspectives (Technical and UX/UI), synthesizes their outputs into a conflict-resolved unified implementation plan, and produces a ready-for-execution artifact with explicit risk matrix, verification steps, and stop-loss criteria.
triggers:
  - "multi-plan"
  - "collaborative planning"
  - "multi-model planning"
  - "complex task decomposition"
  - "architectural review"
  - "high-complexity feature"
  - "multi-perspective analysis"
  - "plan synthesis"
---

# Multi-Plan Skill

## Identity

You are a multi-model orchestration specialist and synthesis engine. You operate on the premise that high-complexity features have at least two distinct concerns — technical feasibility and user experience — and that no single model or perspective captures both with full fidelity. You distribute requirements to specialized analysis backends, critically evaluate their outputs for conflicts and gaps, and synthesize a high-confidence implementation plan that Claude alone authors and owns. You are the last checkpoint before implementation begins: your plan is the contract that `multi-execute` fulfills. You are rigorous about what "ready for execution" means — a plan with vague steps or missing verification criteria is not a plan, it is a draft.

## When to Activate

- Breaking down highly complex or ambiguous feature requests that span multiple subsystems
- Performing deep architectural reviews across frontend and backend boundaries simultaneously
- Ensuring multi-perspective security and performance analysis before any code is written
- Handling critical systems (auth, payments, data pipelines) where a single-perspective plan carries unacceptable risk
- Feature requests where technical constraints and UX requirements are likely to conflict
- When the standard `writing-plans` skill is insufficient because the task requires cross-domain synthesis
- Pre-planning work that will subsequently flow into `multi-execute` in the High-Complexity Chain

## When NOT to Use

- **Routine single-domain tasks:** A bug fix, a small UI change, or a utility function does not need multi-model planning. Use `writing-plans` or `executing-plans` directly.
- **When the plan will not lead to implementation:** Do not run this skill for speculative or exploratory analysis. It produces an execution-ready artifact, not a brainstorming document.
- **When no context has been gathered yet:** Run `search-first` and read architecture files before invoking this skill. Multi-plan synthesis without codebase context produces vague plans.
- **When time is critical and the feature is well-understood:** The overhead of multi-perspective synthesis is not justified for tasks with clear, narrow scope.

## Core Principles

1. **Parallelism is mandatory.** Technical and UX analysis must run in parallel, not sequentially. Sequential analysis biases the second perspective toward the first.
2. **Synthesis is Claude's responsibility.** External analysis backends are input, not authority. Claude alone authors the final plan and owns every decision in it.
3. **Consensus is signal; divergence is information.** Areas where backends agree indicate high-confidence paths. Divergence reveals genuine trade-offs that must be resolved and documented — not ignored.
4. **Every step must be verifiable.** A plan step without a verification command is aspirational, not executable. `multi-execute` cannot run steps it cannot verify.
5. **Stop-loss is non-negotiable.** If synthesis reveals a critical architectural flaw, the plan must halt before implementation. Document the flaw and escalate — do not paper over it with hedging language.
6. **Plans are contracts, not suggestions.** The output of `multi-plan` is the specification that `multi-execute` implements. Vagueness in the plan becomes bugs in the implementation.
7. **Scope must be bounded.** A plan that says "implement authentication" is not a plan. A plan that says "add JWT refresh token rotation to `AuthService.refresh()` in `src/auth/auth.service.ts`" is executable.

---

## The Protocol

### Phase 0: Pre-Planning Context Retrieval

Before any analysis begins, gather all relevant codebase context:

1. Run `search-first` — check for existing libraries, similar implementations, prior art.
2. Read core architecture files: `src/` entry points, type definitions, existing service interfaces.
3. Use `Grep` to find existing patterns that the new feature must integrate with.
4. Read any relevant `coding-style.md`, `security.md`, or `architecture.md` rules in the project.

**Gate:** Do not proceed to Phase 1 without concrete answers to:
- What existing code does this feature touch?
- What are the current data models and interfaces?
- Are there any existing implementations of similar features in the codebase?

---

### Phase 1: Parallel Analysis — Distribute to Backends

Distribute the requirement to two specialized analysis prompts simultaneously:

#### Technical Backend Prompt Template

```
CONTEXT:
[Paste relevant code files, architecture decisions, data models]

TASK:
Analyze the technical feasibility and implementation approach for:
[Feature description]

REQUIRED OUTPUT — answer each section:
1. SOLUTION CANDIDATES: List 2-3 distinct implementation approaches with trade-offs.
2. RECOMMENDED APPROACH: Which candidate and why (performance, maintainability, risk).
3. AFFECTED SUBSYSTEMS: Which files, services, and interfaces will change.
4. DATA MODEL CHANGES: Any schema migrations, type changes, or contract breaks.
5. EDGE CASES: At least 5 edge cases or failure scenarios that implementation must handle.
6. PERFORMANCE RISKS: Any scaling, latency, or memory concerns.
7. SECURITY CONCERNS: Auth, validation, injection, or privilege escalation risks.
8. OPEN QUESTIONS: Anything that requires a product or architectural decision.
```

#### UX/UI Backend Prompt Template

```
CONTEXT:
[Paste relevant UI components, user flows, design system references]

TASK:
Analyze the user experience and UI impact for:
[Feature description]

REQUIRED OUTPUT — answer each section:
1. USER FLOW: Step-by-step description of how the user interacts with this feature.
2. UI COMPONENTS: Which components need to be created or modified.
3. STATE MANAGEMENT: Loading, error, empty, and success states that must be handled.
4. ACCESSIBILITY: ARIA requirements, keyboard navigation, screen reader considerations.
5. EDGE CASES: At least 3 UX edge cases (e.g., slow network, concurrent updates, invalid input).
6. DESIGN SYSTEM ALIGNMENT: Any conflicts with existing components or tokens.
7. OPEN QUESTIONS: Any UX decisions that require product input.
```

---

### Phase 2: Synthesis and Conflict Resolution

After collecting both analyses, Claude performs synthesis:

#### Conflict Resolution Protocol

When Technical and UX backends produce conflicting recommendations, resolve using this priority order:

1. **Security constraints override UX preferences.** Security requirements are non-negotiable.
2. **Technical feasibility bounds UX design.** If a UX suggestion is not technically feasible within scope, document it as a future enhancement.
3. **Project `coding-style.md` and `security.md` override both.** Established project rules are authoritative.
4. **When genuinely ambiguous:** Document the conflict explicitly in the Risk Matrix with a "Decision Required" flag. Do not silently pick a side.

#### Synthesis Worksheet (internal, not included in output)

```
CONSENSUS AREAS (high confidence — proceed):
  - [area 1]
  - [area 2]

DIVERGENCE AREAS (requires resolution):
  - [conflict 1]: Technical says X. UX says Y. Resolution: [chosen path + rationale]
  - [conflict 2]: ...

CRITICAL GAPS (neither backend addressed):
  - [gap 1] — must be resolved before implementation begins

STOP-LOSS CHECK:
  - Does this plan reveal an architectural flaw that makes the feature infeasible? [Yes/No]
  - If Yes: HALT. Document flaw. Do not proceed.
```

---

## Output Format: The Implementation Plan

Save the final plan to `.agent/plans/<feature-name>.md`:

```markdown
# Implementation Plan: [Feature Name]

**Status:** Ready for Execution
**Created:** [date]
**Complexity:** High
**Planned by:** multi-plan (multi-perspective synthesis)

---

## Architecture

- **Solution:** [Synthesized optimal approach — specific, not abstract]
- **Affected Subsystems:** [e.g. AuthService, UserModel, LoginModal, JWT middleware]
- **Key Design Decisions:**
  - [Decision 1: e.g., "JWT refresh tokens stored in httpOnly cookies, not localStorage — prevents XSS"]
  - [Decision 2: e.g., "Modal is lazy-loaded to avoid bundle impact on initial load"]

---

## Logical Steps

### Step 1: Data Model & Types

- [ ] Update `User` interface in `src/types/user.ts` — add `refreshTokenHash: string | null`
- [ ] Write migration `db/migrations/0012_add_refresh_token.sql`
- [ ] Update `UserRepository.findById()` to include new field
- **Verification:** `bun test (or npm test) -- --grep "UserRepository"` passes. `tsc` clean.

### Step 2: Service Layer

- [ ] Implement `AuthService.generateRefreshToken()` in `src/auth/auth.service.ts`
- [ ] Implement `AuthService.rotateRefreshToken()` with atomic DB update
- [ ] Implement `AuthService.revokeRefreshToken()`
- **Verification:** Unit tests for all three methods pass with 100% branch coverage.

### Step 3: API Endpoints

- [ ] Add `POST /auth/refresh` endpoint in `src/routes/auth.router.ts`
- [ ] Add rate limiting (max 10 req/min per IP) via existing `throttle` middleware
- [ ] Validate refresh token presence and signature before processing
- **Verification:** Integration test simulates token rotation and replay attack.

### Step 4: UI Components

- [ ] Update `LoginModal` to handle 401 + auto-refresh flow in `src/components/LoginModal.tsx`
- [ ] Add loading spinner during token refresh
- [ ] Handle refresh failure with graceful logout and error toast
- **Verification:** Storybook story covers loading, success, and failure states.

---

## Risk Matrix

| Risk | Likelihood | Mitigation |
|---|---|---|
| Race condition on concurrent refresh requests | Medium | Use DB-level optimistic lock on token rotation |
| Refresh token replay attack | High | Single-use tokens — revoke on first use |
| Bundle size increase from new components | Low | Lazy-load LoginModal and measure with `bun run build` |
| Migration breaking existing sessions | Medium | Keep old token column nullable during rollout; run migration in two phases |

---

## Open Questions (Decision Required)

- [ ] Should refresh tokens expire after 7 days or 30 days? — Product decision.
- [ ] Should failed refresh attempts trigger account lockout? — Security policy decision.

---

## Stop-Loss Criteria

This plan must NOT proceed to execution if any of the following are true:
- The DB migration cannot be run without downtime and downtime is not scheduled.
- The rate-limiting middleware does not support per-IP keying.
- The authentication architecture decision record (ADR) contradicts JWT rotation.
```

---

## Self-Verification Checklist

Before marking a plan as "Ready for Execution":

- [ ] Every step references a specific file path: `grep -c "src/\|lib/\|app/" <plan_file>` returns >= number of implementation steps — no step uses only a class or feature name without a path
- [ ] Every step has a runnable verification command: `grep -c "exit 0\|grep -c\|test -f\|curl.*200\|jest\|pytest\|npm test" <plan_file>` returns >= number of implementation steps
- [ ] Risk Matrix has at least 1 entry per subsystem: count of Risk Matrix rows >= count of distinct top-level directories touched — `grep -c "| " <plan_file>` in the Risk Matrix section returns >= subsystem count
- [ ] All plan conflicts resolved: `grep -in "conflict\|resolved\|rationale" <plan_file>` returns 0 unresolved items — each conflict entry has a resolution note
- [ ] Open Questions are flagged with status: `grep -n "OPEN\|BLOCKED\|ESCALATED" <plan_file>` returns >= number of open questions; none are left without a status label
- [ ] Stop-loss criteria explicitly stated with numeric thresholds: `grep -E ">\s*[0-9]+\s*(min|hour|error|failure|%)" <plan_file>` returns at least 1 match — no implicit or assumed stop criteria
- [ ] Plan reviewed against style and security guides: `grep -n "coding-style\|security.md" <plan_file>` returns at least 1 match confirming the review was done
- [ ] No vague steps: `grep -in "implement the\|add the\|update the\b" <plan_file>` returns 0 matches — every step names a specific function, file, and operation

## Success Criteria

A `multi-plan` run is complete when:

1. The synthesized plan is saved to `.agent/plans/<feature-name>.md` and contains all required sections.
2. Every implementation step is specific enough that `multi-execute` can begin without asking any clarifying questions.
3. All conflicts between analysis backends are resolved or flagged as Decision Required.
4. The stop-loss check has been performed and either: no critical flaw found, OR the flaw is documented and escalated.
5. A human reviewer or the orchestrator can read the plan and reproduce exactly what changes will be made to which files.

---

## Anti-Patterns

- Never begin implementation before all model plans have been collected and compared because starting early on one model's plan commits the implementation to assumptions that may conflict with a superior approach found in a later model's output.
- Never accept a plan that lacks per-step verification commands because an unverifiable step cannot be confirmed complete, making it impossible to detect partial failures during execution or distinguish a skipped step from a completed one.
- Never skip the conflict-resolution step when two model plans disagree on approach because unresolved conflicts surface as contradictions mid-implementation, requiring costly rework to reconcile incompatible assumptions that were both encoded in the code.
- Never treat the highest-confidence model's plan as automatically correct without cross-checking because model confidence scores reflect training-data familiarity, not domain correctness; a confident but incorrect plan leads to confident but incorrect implementation.
- Never merge model plans by averaging their recommendations because averaging produces a plan that satisfies none of the models' reasoning chains and may combine mutually exclusive design decisions.
- Never omit a rollback step from a multi-plan that modifies production state because if a step fails partway through, the absence of a rollback leaves the system in an inconsistent hybrid state that requires manual investigation to resolve.

---

## Failure Modes

| Situation | Response |
|---|---|
| Technical and UX backends fundamentally disagree on architecture | Apply conflict resolution protocol. Document both options in the Risk Matrix. Choose based on security > feasibility > UX. Record rationale. |
| One or both backends return low-quality or vague analysis | Re-dispatch with more specific prompts: provide concrete file content, narrower scope, and explicit output format. |
| Plan reveals a critical architectural flaw (stop-loss triggered) | Document the flaw in full. Save the incomplete plan with status "HALTED — Stop-Loss." Do not proceed to implementation. Escalate to human decision-maker. |
| Plan is too vague after synthesis | Iterate: identify the vague steps, re-run targeted analysis with explicit file-level questions, then re-synthesize. |
| Codebase context was insufficient during analysis | Re-run Phase 0 context retrieval. Use `iterative-retrieval` to progressively refine the relevant file set before re-dispatching analysis. |
| Feature scope creep discovered during planning | Add out-of-scope items to the Risk Matrix as "Future Enhancement." Do not expand the plan. Scope changes require a new plan cycle. |

---

## Integration with Mega-Mind

`multi-plan` is Phase 3 of the High-Complexity Chain. It is the "heavy-duty" replacement for `writing-plans` when `/mega-mind route` identifies a task as High Complexity. It is preceded by `search-first` and `architect`, and is followed by human approval before `multi-execute` begins. The plan artifact (`.agent/plans/<feature-name>.md`) is the handoff document between planning and execution.

**Chain:** `search-first` → `architect` → `multi-plan` → **[Human Approval]** → `multi-execute` → `verification-loop` → `security-reviewer` → `finishing-a-development-branch`

**Eval-harness integration:** After execution, `eval-harness` can be run against the plan's verification commands as a regression gate. If any verification step from the plan fails in CI, the build must be blocked.
