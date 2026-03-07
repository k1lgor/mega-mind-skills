---
name: single-flow-task-execution
description: Ordered task decomposition with review gates for sequential execution. Use for complex tasks that need to be broken down and executed in order.
triggers:
  - "break this down and implement"
  - "execute this task"
  - "implement step by step"
---

# Single-Flow Task Execution Skill

## When to Use

- Complex tasks that need decomposition
- Features that require ordered implementation
- When you need review gates between phases
- When parallel execution isn't possible or needed

## Instructions

### Step 1: Decompose the Task

Break the task into ordered subtasks:

```markdown
## Task: [Main Task]

### Subtasks (Ordered)

1. [Subtask 1] - Foundation
2. [Subtask 2] - Core logic
3. [Subtask 3] - Integration
4. [Subtask 4] - Testing
5. [Subtask 5] - Documentation
```

### Step 2: Define Review Gates

Identify points where review is needed:

- After foundational changes
- Before breaking changes
- After security-sensitive code
- Before integration with external systems

### Step 3: Execute Sequentially

```
WHILE tasks remain:
  1. Get next task from queue
  2. Mark as in_progress
  3. Implement
  4. Test locally
  5. Mark as completed
  6. IF at review gate:
     - Pause for review
     - Address feedback
     - Continue
  7. Update tracker
```

### Step 4: Maintain Context

Keep context across tasks:

- Track what was learned in previous tasks
- Note decisions made for future reference
- Update shared state as needed

## Task Queue Format

```markdown
# Task Queue (Mega-Mind Session State)

## Current Task

| Task ID | Task                   | Status      | Skill                      | Started    |
| ------- | ---------------------- | ----------- | -------------------------- | ---------- |
| 1       | Set up database schema | completed   | single-flow-task-execution | 2024-01-15 |
| 2       | Create API endpoints   | in_progress | single-flow-task-execution | 2024-01-15 |
| 3       | Add validation         | pending     | single-flow-task-execution | 2024-01-15 |
| 4       | Write tests            | pending     | single-flow-task-execution | 2024-01-15 |
| 5       | Document API           | pending     | single-flow-task-execution | 2024-01-15 |

## Review Gates

- [ ] After task 2: API design review
- [ ] After task 4: Test coverage review
```

## Example Execution

```
Starting Single-Flow Execution: Build User Dashboard

Task 1: Set up database schema
→ Creating users table
→ Creating posts table
→ Running migrations
✓ Task 1 complete

Task 2: Create API endpoints
→ GET /users/:id
→ GET /users/:id/posts
→ POST /users/:id/posts
✓ Task 2 complete

*** REVIEW GATE: API Design Review ***
> Please review the API endpoints before continuing...
[Feedback addressed]
✓ Review passed

Task 3: Add validation
→ Request validation middleware
→ Input sanitization
✓ Task 3 complete

Task 4: Write tests
→ Unit tests for services
→ Integration tests for endpoints
✓ Task 4 complete

*** REVIEW GATE: Test Coverage Review ***
> Coverage at 85%, target is 80%
✓ Review passed

Task 5: Document API
→ OpenAPI spec updated
→ README updated
✓ Task 5 complete

All tasks complete! Running final verification...
✓ All tests pass
✓ Coverage: 85%
✓ Documentation complete
```

## Tips

- Keep subtasks small enough to complete in one sitting
- Use review gates strategically - not too many, not too few
- If a subtask grows too large, break it down further
- Document learnings as you go for the final summary
