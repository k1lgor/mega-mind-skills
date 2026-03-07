---
name: writing-plans
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
