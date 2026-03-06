---
description:
---

# Write Plan Workflow

## Trigger

Use after brainstorming to create an implementation plan.

**Quick Start:** `/mega-mind execute write-plan` or `/plan`

## Prerequisites

- Completed brainstorming session
- Clear understanding of the approach
- Defined scope and constraints

## Steps

### 1. Define Scope

- Review brainstorming output
- Understand constraints
- Define starting point and end goal

### 2. Structure the Plan

Create sections:

- Overview
- Goals and Non-Goals
- Dependencies
- Implementation Phases
- Testing Strategy
- Rollback Plan

### 3. Break Down into Steps

Each step should be:

- Atomic (one clear action)
- Verifiable (can be tested)
- Time-boxed (has estimate)
- Independent (minimal dependencies)

### 4. Create Verification Checkpoints

Define what "done" means for each phase.

## Next Steps After Planning

After completing this workflow, typically continue with:

```
/tdd → Write tests first
/execute → Execute the plan
```

Or use:

```
/mega-mind execute execute-plan
```

## Output

- Detailed implementation plan
- Phase breakdown with estimates
- Verification checkpoints

## Related Skills

- `writing-plans` - The core planning skill
- `brainstorming` - Previous step in workflow
- `executing-plans` - Next step in workflow
- `test-driven-development` - For test-first approach
