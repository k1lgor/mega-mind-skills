---
name: brainstorming
description: Structured exploration before committing to an approach. Use when facing ambiguous problems, new features, architectural decisions, or any situation where multiple approaches are possible.
triggers:
  - "I need to design"
  - "How should I implement"
  - "What's the best approach"
  - "I'm not sure how to"
  - "Let's think about"
  - "architectural decision"
  - "design a solution"
  - "explore options"
---

# Brainstorming Skill

## When to Use

- Starting a new feature or project
- Making architectural decisions
- Exploring multiple implementation approaches
- Solving complex problems with no obvious solution
- Deciding between competing technologies or patterns

## Instructions

### Step 1: Understand the Problem Space

Before generating solutions, thoroughly understand the problem:

1. **Define the problem clearly**
   - What are we trying to solve?
   - What are the success criteria?
   - What constraints exist?

2. **Identify stakeholders and requirements**
   - Who will use this?
   - What are their needs?
   - What are the non-negotiables?

3. **Research existing solutions**
   - What has been tried before?
   - What worked? What didn't?
   - Are there industry standards or best practices?

### Step 2: Generate Multiple Approaches

Create at least 3 different approaches:

```
## Approach A: [Name]
- **Description**: Brief summary
- **Pros**: List of advantages
- **Cons**: List of disadvantages
- **Complexity**: Low/Medium/High
- **Time estimate**: Rough estimate
- **Risk level**: Low/Medium/High
```

### Step 3: Evaluate Approaches

For each approach, consider:

1. **Technical Feasibility**
   - Can this be implemented with current tech stack?
   - Are there any blockers?
   - What dependencies are needed?

2. **Maintainability**
   - How easy will this be to maintain?
   - What's the learning curve for the team?
   - How well does it scale?

3. **Performance Impact**
   - What's the runtime cost?
   - What's the memory footprint?
   - Are there any bottlenecks?

4. **Risk Assessment**
   - What could go wrong?
   - What are the unknowns?
   - How can risks be mitigated?

### Step 4: Make a Recommendation

After evaluation:

1. **Select the best approach** based on weighted criteria
2. **Document the rationale** for the choice
3. **Identify next steps** for implementation
4. **Note any assumptions** that need validation

## Output Format

```markdown
# Brainstorming Session: [Topic]

## Problem Statement

[Clear description of what we're solving]

## Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Approaches Considered

### Approach A: [Name]

**Description**: ...
**Pros**: ...
**Cons**: ...
**Score**: X/10

### Approach B: [Name]

...

### Approach C: [Name]

...

## Recommendation

**Selected**: Approach X
**Rationale**: ...
**Next Steps**: ...
**Assumptions**: ...
```

## Example Usage

**Input**: "I need to implement a caching layer for our API"

**Output**:

```markdown
# Brainstorming Session: API Caching Layer

## Problem Statement

Our API is experiencing high latency under load. We need to implement a caching layer to reduce response times and database load.

## Requirements

- [x] Reduce average response time by 50%
- [x] Handle 10,000 requests/second
- [x] Support cache invalidation
- [x] Work with existing infrastructure

## Approaches Considered

### Approach A: Redis Cache

**Description**: Use Redis as a distributed cache
**Pros**: High performance, supports TTL, pub/sub for invalidation
**Cons**: Additional infrastructure, memory costs
**Score**: 8/10

### Approach B: In-Memory Cache (Node-cache)

**Description**: Use in-memory caching within the application
**Pros**: Simple, no extra infrastructure
**Cons**: Doesn't scale horizontally, lost on restart
**Score**: 5/10

### Approach C: CDN Edge Caching

**Description**: Use CloudFlare or similar for edge caching
**Pros**: Fast for static content, reduces origin load
**Cons**: Less control, harder to cache dynamic content
**Score**: 6/10

## Recommendation

**Selected**: Approach A (Redis Cache)
**Rationale**: Best balance of performance, scalability, and control. Team has Redis experience.
**Next Steps**:

1. Set up Redis instance
2. Implement cache layer
3. Add cache invalidation logic
   **Assumptions**:

- Budget available for Redis hosting
- Team can manage Redis operations
```

## Tips

- Don't jump to the first solution that comes to mind
- Consider the long-term implications, not just immediate needs
- Involve relevant stakeholders when appropriate
- Document the decision-making process for future reference
- Be willing to revisit decisions if new information emerges
