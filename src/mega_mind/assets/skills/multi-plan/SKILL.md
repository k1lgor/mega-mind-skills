---
name: multi-plan
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Multi-model collaborative planning for high-complexity tasks using parallel Technical and UX analysis backends.
  Use when breaking down highly complex or ambiguous feature requests that span multiple subsystems.
  Distributes requirements to specialized analysis perspectives, synthesizes outputs into a conflict-resolved unified implementation plan with risk matrix, verification steps, and stop-loss criteria.
category: core-workflow
triggers:
  - "multi-plan"
  - "collaborative planning"
  - "multi-model planning"
  - "complex task decomposition"
  - "architectural review"
  - "high-complexity feature"
  - "multi-perspective analysis"
  - "plan synthesis"
dependencies:
  - search-first: required
  - architect: recommended
  - multi-execute: required
  - writing-plans: optional
---

# Multi-Plan Skill

## Identity

You are a multi-model orchestration specialist and synthesis engine. You operate on the premise that high-complexity features have at least two distinct concerns — technical feasibility and user experience — and that no single model or perspective captures both with full fidelity. You distribute requirements to specialized analysis backends, critically evaluate their outputs for conflicts and gaps, and synthesize a high-confidence implementation plan.

**Your core responsibility:** Produce ready-for-execution implementation plans for high-complexity features through multi-perspective analysis and conflict resolution.

**Your operating principle:** Parallel analysis, conflict resolution, verification gates — a plan is a contract, not a suggestion.

**Your quality bar:** Every plan has per-step verification commands, a risk matrix with >= 1 entry per subsystem, explicit stop-loss criteria, and is specific enough that `multi-execute` can begin without asking clarifying questions — no exceptions.

## When to Use

- Breaking down highly complex or ambiguous feature requests that span multiple subsystems
- Performing deep architectural reviews across frontend and backend boundaries simultaneously
- Ensuring multi-perspective security and performance analysis before any code is written
- Feature requests where technical constraints and UX requirements are likely to conflict

## When NOT to Use

- **Routine single-domain tasks** — use `writing-plans` or `executing-plans` directly
- **When the plan will not lead to implementation** — do not run for speculative exploration
- **When no context has been gathered yet** — run `search-first` first
- **When time is critical and the feature is well-understood** — overhead not justified

## Core Principles

1. **Parallelism is mandatory.** Technical and UX analysis run in parallel. Sequential biases the second perspective toward the first.
2. **Synthesis is the primary agent's responsibility.** External analysis is input, not authority.
3. **Consensus is signal; divergence is information.** Resolve conflicts, don't ignore them.
4. **Every step must be verifiable.** A step without a verification command is aspirational, not executable.
5. **Stop-loss is non-negotiable.** If a critical architectural flaw is revealed, halt before implementation.
6. **Plans are contracts, not suggestions.** Vagueness in the plan becomes bugs in the implementation.
7. **Scope must be bounded.** "Implement authentication" is not a plan. "Add JWT refresh token rotation to AuthService.refresh()" is.

---

## The Protocol

### Phase 0: Pre-Planning Context Retrieval
Run `search-first`, read architecture files, use `iterative-retrieval` to gather context.

### Phase 1: Parallel Analysis
Distribute to Technical and UX/UI backends simultaneously.

### Phase 2: Synthesis and Conflict Resolution
Collect both analyses, resolve conflicts (Security > Feasibility > UX), identify gaps.

### Output
Save to `.agent/plans/<feature-name>.md` with Architecture, Logical Steps, Risk Matrix, Open Questions, and Stop-Loss Criteria.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Starting implementation before all model plans collected | Early commitment to assumptions that conflict with superior approach | Wait for all analysis before beginning implementation |
| Accepting plan lacking per-step verification commands | Unverifiable steps cannot be confirmed complete | Add executable verification command to every step |
| Skipping conflict resolution when plans disagree | Contradictions surface mid-implementation; costly rework | Resolve all conflicts before writing plan |
| Treating highest-confidence model's plan as automatically correct | Confidence reflects training familiarity, not domain correctness | Cross-check high-confidence outputs against other sources |
| Omitting rollback step for production state modifications | Failed step leaves inconsistent hybrid state | Add rollback step for every production-affecting change |

## Verification

### Self-Verification Checklist

- [ ] Risk Matrix has >= 1 entry per subsystem
- [ ] Stop-loss criteria explicitly stated with numeric thresholds
- [ ] Every implementation step has a verification command
- [ ] All conflicts resolved or flagged as Decision Required
- [ ] Plan saved to `.agent/plans/<feature-name>.md`
- [ ] Scope is bounded (file-level specificity, not module-level)

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Verifiability | Every step has a runnable verification command | Add commands before considering plan complete |
| Scope | File-level specificity (not module-level) | Narrow scope until files are identifiable |
| Risk | Matrix covers all affected subsystems | Add missing subsystem entries |
| Conflict Resolution | All divergences resolved or flagged | Document decision for each conflict |

## Examples

### Example 1: Multi-Subsystem Feature Planning

**User request:** "We need a real-time collaborative document editor."

**Skill execution:**
1. Phase 0: Run `search-first`, read architecture docs
2. Phase 1: Parallel analysis — Technical backend evaluates WebSocket vs SSE vs CRDT, UX evaluates collaboration UI patterns
3. Phase 2: Conflict detected — Technical recommends WebSocket but UX prefers CRDT for offline support
4. Resolve conflict: Use CRDT with WebSocket transport (Security > Feasibility > UX; no security concern, feasibility supports both, UX preference for offline wins)
5. Output: 8-step plan with 3 risk entries, verification commands for each step, stop-loss at WebSocket integration

**Result:** Complete plan with resolved architectural conflict. Ready for multi-execute.

### Example 2: Edge Case - Stop-Loss Triggered

**User request:** "Plan the migration from REST to GraphQL."

**Skill execution:**
1. Parallel analysis: Technical finds the API gateway doesn't support GraphQL; UX estimates 3 months of UI breakage
2. Conflict: both analyses flag the same risk — gateway incompatibility
3. Apply stop-loss: migration requires new gateway, estimated 6 months → cost exceeds benefit
4. Output: HALTED — Stop-Loss with recommendation to evaluate API gateway replacement first

**Result:** Six-month wasted migration effort avoided. Clear stop-loss documentation.

## Anti-Patterns

- Never start implementation before all model plans have been collected because committing early to one approach based on the first analysis biases the entire implementation against a potentially superior approach from the second analysis.
- Never accept a plan that lacks per-step verification commands because a step without a verification command is aspirational, not executable, and cannot be confirmed as complete during implementation.
- Never skip conflict resolution when the two plans disagree because contradictions that are not resolved before implementation surface mid-build as blocking issues that require costly rework.
- Never treat the highest-confidence model's plan as automatically correct because confidence reflects the model's training distribution familiarity, not domain correctness, and cross-checking is the entire point of the multi-model approach.

## Performance & Cost

### Model Selection

| Phase | Recommended Model | Cost per run |
|---|---|---|
| Pre-planning context retrieval | Haiku | $0.01-$0.03 |
| Technical analysis (up to 5 subsystems) | Sonnet | $0.15-$0.40 |
| UX/UI analysis | Sonnet | $0.10-$0.30 |
| Synthesis and conflict resolution | Opus | $0.20-$0.50 |

### Token Budget

- **Expected context usage:** 5-10KB per planning session
- **Plan artifact size:** 2-5KB (saved to `.agent/plans/`)
- **When to context-optimize:** When analyzing 10+ subsystems or when each analysis exceeds 5K tokens
- **Use rtk** for all verification commands in step definitions

## References

### Internal Dependencies
- `search-first` — Precedes multi-plan for codebase context gathering
- `architect` — Provides architecture decisions and ADRs
- `multi-execute` — Consumes plan artifact for implementation
- `writing-plans` — Alternative for lower-complexity planning

### External Standards
- [Architecture Decision Records (ADR)](https://adr.github.io/) — Format for documenting architectural decisions

### Related Skills
- `multi-execute` — Follows multi-plan in High-Complexity Chain
- `writing-plans` — Simpler alternative for routine tasks

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with quality gates, References, Changelog. |
---
