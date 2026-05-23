---
name: writing-plans
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Create detailed, step-by-step implementation plans. Use after brainstorming to document the execution strategy, or when tasked with creating a plan for a feature or change.
triggers:
  - "create a plan"
  - "write a plan"
  - "plan this feature"
  - "how do we implement this"
  - "break this down"
  - "implementation plan"
---

# Writing Plans Skill

## When to Use

- After completing brainstorming for a feature
- When asked to create an implementation plan
- Before starting complex multi-step work
- When breaking down large tasks into manageable pieces

## When NOT to Use

- Tasks estimated under 1 hour that can be done in a single uninterrupted flow — the plan overhead exceeds the benefit
- When requirements are still undefined or actively changing — wait until the scope is stable before creating a plan
- Micro-tasks like fixing a single bug or updating a config value — an inline comment is sufficient
- When an existing plan already covers the work — update the existing plan rather than creating a duplicate

## Instructions

### Step 1: Define Scope and Context

Before writing the plan:

1. **Review the brainstorming output** (if available)
2. **Understand the constraints** (time, resources, dependencies)
3. **Identify the starting point** (current state of the codebase)
4. **Define the end goal** (what does "done" look like?)

### Step 2: Structure the Plan

Every plan should follow this structure:

```markdown
# Plan: [Feature/Task Name]

## Overview

Brief description of what we're building and why.

## Goals

- Goal 1
- Goal 2
- Goal 3

## Non-Goals

- What we're explicitly NOT doing

## Dependencies

- Dependency 1
- Dependency 2

## Implementation Steps

### Phase 1: [Phase Name]

- [ ] Step 1.1: Description
  - Details: ...
  - Files: ...
  - Estimated time: ...
- [ ] Step 1.2: Description

### Phase 2: [Phase Name]

...

## Testing Strategy

How we'll verify each phase works.

## Rollback Plan

What to do if things go wrong.

## Success Metrics

How we'll measure success.
```

### Step 3: Break Down Into Atomic Steps

Each step should be:

- **Atomic**: One clear action
- **Verifiable**: Can be tested/confirmed
- **Time-boxed**: Has an estimate
- **Independent**: Minimal dependencies on other steps
- **Ordered**: Clear sequence of execution

### Step 4: Identify Risk Points

For each phase, identify:

- What could go wrong?
- What are the unknowns?
- What are the dependencies that might fail?

### Step 5: Create Verification Checkpoints

Define what "done" means for each phase:

```markdown
### Verification: Phase 1 Complete

- [ ] All tests pass
- [ ] Code compiles without warnings
- [ ] Feature works in development
- [ ] Code reviewed
```

## Output Format

```markdown
# Plan: [Name]

## Metadata

- **Created**: [Date]
- **Author**: [Who]
- **Status**: Draft/In Review/Approved
- **Estimated effort**: [Time]

## Context

[Background and motivation]

## Goals

1. [Goal 1]
2. [Goal 2]

## Implementation

### Phase 1: Foundation (Est: 2h)

| Task ID | Description        | Status  | Skill         | Started    |
| ------- | ------------------ | ------- | ------------- | ---------- |
| 1.1     | Create data models | pending | writing-plans | 2024-01-15 |
| 1.2     | Set up migrations  | pending | writing-plans | 2024-01-15 |
| 1.3     | Add seed data      | pending | writing-plans | 2024-01-15 |

**Verification:**

- [ ] Models compile
- [ ] Migrations run successfully
- [ ] Seed data loads

### Phase 2: Core Logic (Est: 4h)

| Step | Description             | Files         | Status  |
| ---- | ----------------------- | ------------- | ------- |
| 2.1  | Implement service layer | src/services/ | pending |
| 2.2  | Add business logic      | src/logic/    | pending |

...

## Testing Plan

...

## Rollback Plan

...

## Notes

...
```

## Example Usage

**Input**: "Create a plan for adding user authentication"

**Output**:

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

## Dependencies

- Database schema for users
- Email service for verification
- OAuth app credentials

## Implementation

### Phase 1: Core Auth (Est: 8h)

| Task ID | Description                  | Status  | Skill         | Started    |
| ------- | ---------------------------- | ------- | ------------- | ---------- |
| 1.1     | Create User model            | pending | writing-plans | 2024-01-15 |
| 1.2     | Implement password hashing   | pending | writing-plans | 2024-01-15 |
| 1.3     | Create registration endpoint | pending | writing-plans | 2024-01-15 |
| 1.4     | Create login endpoint        | pending | writing-plans | 2024-01-15 |
| 1.5     | Implement JWT generation     | pending | writing-plans | 2024-01-15 |
| 1.6     | Add auth middleware          | pending | writing-plans | 2024-01-15 |

**Verification:**

- [ ] User can register
- [ ] User can login
- [ ] Protected routes require auth
- [ ] Passwords are hashed

### Phase 2: OAuth (Est: 6h)

| Step | Description            | Files           | Status  |
| ---- | ---------------------- | --------------- | ------- |
| 2.1  | Add Google OAuth       | routes/oauth.ts | pending |
| 2.2  | Add GitHub OAuth       | routes/oauth.ts | pending |
| 2.3  | Handle OAuth callbacks | routes/oauth.ts | pending |

### Phase 3: Password Reset (Est: 4h)

| Step | Description               | Files             | Status  |
| ---- | ------------------------- | ----------------- | ------- |
| 3.1  | Create reset token model  | models/token.ts   | pending |
| 3.2  | Implement forgot password | routes/auth.ts    | pending |
| 3.3  | Implement reset password  | routes/auth.ts    | pending |
| 3.4  | Send reset emails         | services/email.ts | pending |

## Testing Strategy

- Unit tests for auth utilities
- Integration tests for auth endpoints
- E2E tests for auth flows

## Rollback Plan

1. Revert database migrations
2. Remove auth-related routes
3. Clear JWT tokens (force re-login)

## Success Metrics

- Registration time < 5 seconds
- Login time < 2 seconds
- Zero security vulnerabilities in audit
```

## Tips

- Plans are living documents - update them as you learn
- Each phase should deliver working, testable code
- Include time estimates but treat them as approximations
- Review plans with the team before starting implementation
- Keep plans granular enough to track progress but not so detailed they become outdated quickly

## Failure Modes

| Failure                                                                   | Cause                                                                                                    | Recovery                                                                                                                   |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Plan steps are too coarse, causing agent to make unreviewed sub-decisions | Steps written at feature level, not task level; each step contains multiple implicit sub-steps           | Decompose each step until it is a single, atomic action with a single verifiable output                                    |
| Plan has no dependency graph, causing steps to execute out of order       | Steps listed as a flat sequence; parallelisable steps not identified; sequential dependencies not marked | Add a dependency annotation to each step (e.g. "requires step 3"); identify steps that can run in parallel                 |
| Plan written for the author, not the executor                             | Assumes shared context; omits file paths, tool names, and expected outputs                               | Write every step as if the executor has no prior context; include exact file paths, commands, and expected outputs         |
| Plan scope creep: executor adds unrequested work mid-execution            | Steps are underspecified; executor fills gaps with its own judgment                                      | Add a "scope boundary" section listing what is explicitly out of scope; executor must not cross it without a plan revision |
| Plan not versioned when requirements change                               | Plan edited in place without tracking what changed and why; prior decisions lost                         | Treat the plan as a versioned document; append a changelog entry for every revision with a reason                          |

## Anti-Patterns

- Never write a plan step without a verifiable output because a step without a success criterion cannot be marked complete objectively and the executor will self-report done without checking.
- Never write a plan for yourself because a plan written with shared context assumptions fails when executed by any other agent or when you return to the task after context loss.
- Never omit the scope boundary because without an explicit out-of-scope list, the executor treats every adjacent improvement as in scope and the plan becomes unbounded.
- Never edit a plan in place without versioning because lost decision rationale is re-litigated in every subsequent execution and the plan diverges from its original intent.
- Never write a flat step list without dependency annotations because the executor cannot determine which steps are parallelisable and which are sequential, wasting execution time or causing ordering failures.
- Never skip the "expected output" field for each step because without it the executor cannot verify completion and will mark a step done based on the tool returning exit code 0 rather than on the actual output.

## Self-Verification Checklist

- [ ] Plan has phases with atomic steps — count of steps containing more than one imperative verb equals 0
- [ ] Each phase ends with an explicit verification checkpoint — count of phases without a verification block equals 0
- [ ] Dependencies between steps are annotated — every step that requires a prior step has a "requires step N" annotation
- [ ] Rollback plan is present for any step that touches production data or public interfaces — count of production-touching steps without rollback equals 0
- [ ] Time estimates are present for each phase — count of phases without an estimate equals 0
- [ ] Non-Goals section lists ≥1 explicit out-of-scope item

## Success Criteria

This skill is complete when: 1) The plan has phases with atomic steps, each with a verification checkpoint. 2) Any engineer reading the plan can execute it without needing additional clarification on scope, order, or success criteria. 3) The plan is saved to `docs/plans/` and referenced in `task.md`. 4) The **Handoff block** has been emitted with `next_skill` pointing to `executing-plans` (or the next chain step) and `status: completed`.
