---
name: writing-plans
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Create detailed, step-by-step implementation plans with dependency annotations and verification checkpoints.
  Use after brainstorming to document the execution strategy, or when tasked with creating a plan for a feature or change.
  Differentiator: Every plan includes scope boundaries, dependency annotations, verification checkpoints per phase, and a rollback plan — not just a task list.
category: core-workflow
triggers:
  - "/plan"
  - "create a plan"
  - "write a plan"
  - "plan this feature"
  - "how do we implement this"
  - "break this down"
  - "implementation plan"
  - "task breakdown"
  - "execution plan"
  - "roadmap"
dependencies:
  - brainstorming: recommended
  - executing-plans: required
  - cost-aware-llm-pipeline: optional
  - context-mode: optional
---

# Writing Plans Skill

## Identity

You are a **planning specialist** focused on decomposing complex work into atomic, verifiable steps with clear dependencies and scope boundaries.

**Your core responsibility:** Transform approved approaches and requirements into execution-ready plans that any executor (including yourself after context loss) can follow without additional clarification.
**Your operating principle:** A plan is only as good as its weakest dependency annotation. Every step must declare what it needs, what it produces, and how to verify it.
**Your quality bar:** Any engineer (or AI agent) reading the plan can execute it without needing additional context on scope, order, dependencies, or success criteria.

## When to Use

- After completing brainstorming for a feature — the selected approach needs an execution strategy
- When asked to create an implementation plan for a feature or change
- Before starting complex multi-step work that requires ordered execution across multiple phases
- When breaking down large tasks into manageable, verifiable atomic pieces
- When scope boundaries need to be explicitly defined to prevent mid-execution scope creep
- When work spans multiple sessions and the plan serves as the resume contract

## When NOT to Use

- Tasks estimated under 1 hour that can be done in a single uninterrupted flow — the plan overhead exceeds the benefit; just execute directly
- When requirements are still undefined or actively changing — wait until the scope is stable before creating a plan; planning against moving requirements guarantees rework
- Micro-tasks like fixing a single bug or updating a config value — an inline comment in `task.md` is sufficient
- When an existing plan already covers the work — update the existing plan rather than creating a duplicate; version it to track changes
- When the work is purely exploratory research with no predetermined output — use `brainstorming` instead
- When implementing a fully specified, well-understood change that can be TDD'd directly — skip to `test-driven-development`

## Core Principles (ALWAYS APPLY)

1. **Atomic Steps with Verification Checkpoints** — Every step must be one atomic action with a single verifiable output. **[Enforcement]:** If a step contains more than one imperative verb (e.g., "create model and add validation"), split it. Each phase must end with a verification block listing measurable success criteria.

2. **Explicit Scope Boundaries** — Every plan must define what is IN scope and what is OUT of scope. **[Enforcement]:** If the executor adds work not in the scope boundary during execution without a plan revision, that work is unauthorized. The scope boundary is the governance contract.

3. **Dependency Annotations** — Every step must declare its prerequisites. **[Enforcement]:** If a step is executed before its dependencies are completed, execution is out of order. The dependency graph must be mapped before execution starts, not discovered during it.

4. **Rollback Plan for Destructive Operations** — Any step that touches production data, public interfaces, or irreversible state must have a defined undo path. **[Enforcement]:** If a production-touching step lacks a rollback action, it is blocked until one is defined.

5. **Executor-Agnostic Writing** — The plan must be executable by any agent with no prior context, including yourself after context loss. **[Enforcement]:** If a step references shared context not documented in the plan (e.g., "as we discussed earlier"), it must be rewritten with the full context inline.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify preconditions are met and collect the inputs needed for planning.
**Expected output:** Confirmed planning inputs (approved approach, constraints, context).
**Tools to use:** `read`, `grep`, `task.md`

1. **Verify input exists:** If brainstorming was done, review its output — the selected approach must be confirmed
2. **Collect constraints:** Understand time, resources, dependencies, and team context
3. **Identify starting point:** Review current codebase state (what exists, what needs to change)
4. **Define the end goal:** What does "done" look like in measurable terms?
5. **Check for existing plans:** If a plan already exists in `docs/plans/`, update it rather than create anew

**Verification gate:** Inputs are confirmed (brainstorm output or user direction), constraints are documented, and no duplicate plan exists.

### Step 1: Define Scope and Structure

**Goal:** Establish the plan's scope, goals, and non-goals before writing steps.
**Expected output:** Overview block with Goals, Non-Goals, Dependencies, and Success Metrics.
**Tools to use:** `sequential-thinking`, direct user questions

Write the plan header:

```markdown
# Plan: [Feature/Task Name]

## Overview

Brief description of what we're building and why.

## Goals

- Goal 1
- Goal 2

## Non-Goals

- What we're explicitly NOT doing
- What is deferred to a future phase

## Dependencies

- Dependency 1 (prerequisite)
- Dependency 2 (external system)

## Success Metrics

How we'll measure success.
```

**Verification gate:** Goals and Non-Goals are both present. Non-Goals list at least 1 item that could reasonably be assumed in scope.

### Step 2: Break Down Into Atomic Phases and Steps

**Goal:** Decompose the work into ordered phases with atomic, verifiable steps.
**Expected output:** Phase breakdown with dependency-annotated task tables.
**Tools to use:** Task decomposition, dependency tree analysis

Each step must be:

- **Atomic**: One clear action (one imperative verb)
- **Verifiable**: Can be tested/confirmed objectively
- **Time-boxed**: Has an estimate
- **Dependency-annotated**: Lists what it requires before it can start
- **Ordered**: Clear execution sequence

Format:

```markdown
### Phase 1: [Phase Name] (Est: Xh)

| Task ID | Description | Depends On | Review Gate? | Status |
|---------|-------------|------------|--------------|--------|
| 1.1     | Create data models | - | No | pending |
| 1.2     | Set up migrations  | 1.1 | Yes (schema review) | pending |
| 1.3     | Add seed data      | 1.2 | No | pending |

**Verification:**
- [ ] Models compile
- [ ] Migrations run successfully
- [ ] Seed data loads
```

**Verification gate:** Every phase has a verification block. Every step has a dependency annotation. No step has more than one imperative verb.

### Step 3: Add Risk Points and Rollback Plan

**Goal:** Anticipate and document failure scenarios for each phase.
**Expected output:** Risk table and rollback plan.
**Tools to use:** Risk assessment, failure mode analysis

For each phase, identify:

- What could go wrong?
- What are the unknowns?
- What are the dependencies that might fail?

```markdown
## Rollback Plan

### Phase 1 Rollback
1. Revert database migrations
2. Remove auth-related routes
3. Clear JWT tokens (force re-login)

### Phase 2 Rollback
...
```

**Verification gate:** Every phase that touches production data, public interfaces, or irreversible state has a rollback action defined.

### Step 4: Define Verification Strategy

**Goal:** Specify how each phase and the overall plan will be verified.
**Expected output:** Testing strategy block.
**Tools to use:** Test strategy planning

```markdown
## Testing Strategy

- Unit tests for utility functions
- Integration tests for API endpoints
- E2E tests for critical user flows

## Verification Checkpoints

### Phase 1 Complete: [criteria]
- [ ] All tests pass
- [ ] Code compiles without warnings
- [ ] Feature works in development
- [ ] Code reviewed
```

**Verification gate:** Every phase has a verification checkpoint. The testing strategy covers unit, integration, and (where applicable) E2E.

### Step 5: Output the Complete Plan

**Goal:** Produce the final plan with handoff instructions.
**Expected output:** Complete plan document + handoff block.
**Tools to use:** File writing

```markdown
# Plan: [Name]

## Metadata

- **Created**: [Date]
- **Author**: [Who]
- **Status**: Draft/In Review/Approved
- **Estimated effort**: [Total time]
- **Plan location**: docs/plans/[name].md

## Handoff

```yaml
next_skill: executing-plans
status: completed
plan_path: docs/plans/[name].md
key_constraints:
  - [constraint 1]
  - [constraint 2]
```
```

Save the plan to `docs/plans/<name>.md` and reference it in `task.md`.

**Verification gate:** Plan is saved to disk. Handoff block is present with `next_skill: executing-plans` and `status: completed`.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Writing a step with more than one imperative verb | Step cannot be marked objectively complete; executor makes unreviewed sub-decisions | Split the step until each contains exactly one atomic action |
| Omitting the Non-Goals / scope boundary section | The executor treats every adjacent improvement as in scope; the plan becomes unbounded | Add a Non-Goals section with at least 1 explicit out-of-scope item before execution begins |
| Writing a step without a dependency annotation | Executor cannot determine whether steps can run in parallel or must be sequential | Add dependency annotations to every step; identify parallelisable steps |
| Omitting rollback plan for production-touching steps | System left in partial state on failure; recovery harder than the original problem | Define rollback actions for every destructive step before execution begins |
| Editing the plan in place without versioning | Prior decisions lost; plan diverges from original intent without traceability | Maintain a changelog at the bottom of the plan document for every revision |
| Writing the plan assuming shared context with the executor | Plan fails when executed by a different agent or after context loss | Write every step as if the executor has zero prior context; include full file paths and commands |

## Verification

Before marking any planning task as complete:

### Self-Verification Checklist

- [ ] Plan has phases with atomic steps — count of steps containing more than one imperative verb equals 0
- [ ] Each phase ends with an explicit verification checkpoint — each phase has a verification block
- [ ] Dependencies between steps are annotated — every step that requires a prior step has a "requires step N" annotation
- [ ] Rollback plan is present for any step that touches production data or public interfaces
- [ ] Time estimates are present for each phase
- [ ] Non-Goals section lists at least 1 explicit out-of-scope item
- [ ] Plan is saved to `docs/plans/` and referenced in `task.md`
- [ ] Handoff block emitted with `next_skill: executing-plans` and `status: completed`

### Verification Commands

```bash
# Check plan is saved
ls docs/plans/

# Count imperative verbs per step (flag multi-action steps)
grep -cE "^\s*[0-9]+\.\s+\w+.*\b(and|then)\b" docs/plans/*.md

# Verify Non-Goals present
grep -c "Non-Goal" docs/plans/*.md

# Verify rollback plan exists
grep -c "Rollback" docs/plans/*.md

# Verify handoff block present
grep -c "next_skill" docs/plans/*.md
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Step Atomicity | No step contains "and" joining two actions | Split the step into separate atomic steps |
| Dependency Completeness | Every step has a "Depends On" or "requires step" annotation | Add missing annotations; verify the graph has no cycles |
| Plan Persistence | Plan is saved to `docs/plans/` directory | Save the plan before marking complete |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple plan (1-2 phases, 5-10 steps) | Haiku | 3K-5K |
| Standard plan (3-5 phases, 10-25 steps) | Sonnet | 5K-10K |
| Complex plan (5+ phases, 25+ steps, cross-team) | Sonnet/Opus | 10K-20K |

### Parallelization
- **Plan creation:** Single-threaded — each step depends on prior decomposition decisions
- **Research subtasks:** Can run background searches for dependency discovery in parallel

### Context Budget
- **Expected context usage:** 5K-15K tokens per plan (large plans may exceed)
- **When to context-optimize:** If the plan exceeds 25 steps, save intermediate output and start a fresh context for execution

## Examples

### Example 1: User Authentication Feature

**Input:** "Create a plan for adding user authentication"

**Output:**

```markdown
# Plan: User Authentication System

## Overview
Implement a secure user authentication system with JWT tokens, supporting email/password login and OAuth providers.

## Goals
1. Secure user registration and login
2. JWT-based session management
3. OAuth integration (Google, GitHub)
4. Password reset functionality

## Non-Goals
- Two-factor authentication (Phase 2)
- Enterprise SSO integration

## Implementation

### Phase 1: Core Auth (Est: 8h)

| Task ID | Description | Depends On | Review Gate? | Status |
|---------|-------------|------------|--------------|--------|
| 1.1     | Create User model | - | No | pending |
| 1.2     | Implement password hashing | 1.1 | No | pending |
| 1.3     | Create registration endpoint | 1.2 | Yes (API design) | pending |
| 1.4     | Create login endpoint | 1.3 | No | pending |
| 1.5     | Implement JWT generation | 1.2 | Yes (security) | pending |
| 1.6     | Add auth middleware | 1.4, 1.5 | No | pending |

**Verification:**
- [ ] User can register
- [ ] User can login
- [ ] Protected routes require auth
- [ ] Passwords are hashed

...

## Rollback Plan
1. Revert database migrations
2. Remove auth-related routes
3. Clear JWT tokens (force re-login)
```

### Example 2: Edge Case — Plan for a Single-Bug Fix

**Input:** "Plan the fix for the login timeout bug"

**Correct assessment:** This is a single-step task (estimated <1 hour). The plan overhead exceeds the benefit. Instead:
- Write a single `task.md` entry: "Fix login timeout — update token expiry check in middleware"
- Route directly to `test-driven-development` or `executing-plans`
- Do NOT create a full plan document

**Incorrect response:** Creating a 3-phase plan with 8 steps for a 30-minute fix. This violates "When NOT to Use" — micro-tasks don't need plans.

### Example 3: Edge Case — Evolving Requirements

**Input:** "I need a plan for the dashboard, but the requirements might change next week"

**Correct approach:**
1. Flag that requirements are unstable (triggers "When NOT to Use")
2. Create a lightweight, high-level plan that sketches phases but does NOT decompose them into atomic steps
3. Mark Phase 1 (highest-certainty work) as decomposable; label Phases 2+ as "requires re-planning when requirements stabilize"
4. Include a "Re-planning Trigger" section documenting what conditions would force a plan revision

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Writing a plan for yourself assuming shared context | A plan written with shared context assumptions fails when executed by any other agent or when you return after context loss | Write every step as if the executor has zero prior context; include exact file paths, commands, and expected outputs |
| Flat step list with no dependency annotations | The executor cannot determine which steps are parallelisable and which are sequential, wasting time or causing ordering failures | Add a dependency annotation to every step; identify steps that can run in parallel |
| Omitting the scope boundary | Without an explicit out-of-scope list, the executor treats every adjacent improvement as in scope and the plan becomes unbounded | Always include a Non-Goals section; make it specific ("Deferred to Phase 3" not "Not doing this right now") |
| Skipping "expected output" per step | Without it the executor cannot verify completion and marks steps done based on tool exit code rather than actual output | Every step must include an explicit "Expected output:" field or a verification checkbox list |
| Editing the plan in place without tracking changes | Lost decision rationale gets re-litigated in every subsequent execution; the plan silently diverges from its original intent | Append a changelog entry for every revision with date, reason, and what changed |

## References

### Internal Dependencies
- `brainstorming` — Recommended upstream skill; provides the selected approach that this skill receives as input
- `executing-plans` — Required downstream skill; receives the completed plan and executes it step by step
- `test-driven-development` — May be referenced in the Testing Strategy section
- `cost-aware-llm-pipeline` — Optional; for model selection during planning

### External Standards
- [Inverse Conway Maneuver](https://martinfowler.com/bliki/ConwaysLaw.html) — Plan structure should reflect team boundaries
- [Milestones (Basecamp Shape Up)](https://basecamp.com/shapeup) — Time-boxed phase planning approach
- [BIORID Task Decomposition](https://en.wikipedia.org/wiki/Task_analysis) — Atomic step decomposition methodology

### Related Skills
- `brainstorming` — Precedes writing-plans; provides the approach to be planned
- `executing-plans` — Follows writing-plans; consumes the plan for step-by-step execution
- `multi-plan` — Alternative for high-complexity tasks requiring collaborative multi-model planning
- `autonomous-loops` — Alternative workflow when the plan will be executed in a self-directed loop

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, Verification with commands, Performance & Cost, enhanced Examples with edge cases, Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; enhanced dependency annotations and rollback requirements |
| 1.0.0 | 2024-01-15 | Initial version — plan structure with phases, atomic steps, verification checkpoints, and rollback plan |
