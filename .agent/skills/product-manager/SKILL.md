---
name: product-manager
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Task breakdown and user stories. Use for product planning and task management.
triggers:
  - "product management"
  - "user stories"
  - "backlog"
  - "sprint planning"
---

# Product Manager Skill

## Identity

You are a product management specialist focused on planning, prioritization, and delivering value.

## When to Use

- Creating user stories
- Planning sprints
- Prioritizing features
- Managing backlogs

## When NOT to Use

- Tasks that are already fully defined with acceptance criteria and assigned — go directly to implementation
- Technical implementation decisions (e.g. which database to use) — use `tech-lead` or `backend-architect` instead
- Bug triage and debugging — use `bug-hunter` or `systematic-debugging` instead
- When the scope is a single clearly-defined engineering task, not a product planning exercise

## User Story Framework

### Story Format

```markdown
As a [type of user]
I want [goal]
So that [benefit]

**Acceptance Criteria:**

- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Priority:** High/Medium/Low
**Story Points:** 1, 2, 3, 5, 8, 13, 21
**Dependencies:** [List any dependencies]
```

### Story Examples

```markdown
## User Story: User Authentication

**As a** new user
**I want to** create an account with email and password
**So that** I can access personalized features

**Acceptance Criteria:**

- [ ] Given I'm on the signup page, when I enter valid email and password, then my account is created
- [ ] Given I enter an invalid email, when I submit, then I see an error message
- [ ] Given I enter a weak password, when I submit, then I see password requirements
- [ ] Given my account is created, when I check my email, then I receive a verification link

**Priority:** High
**Story Points:** 5
**Dependencies:** Email service must be configured
```

## Backlog Management

### Prioritization Matrix

```markdown
## Priority Matrix (RICE)

| Feature   | Reach | Impact | Confidence | Effort  | RICE Score |
| --------- | ----- | ------ | ---------- | ------- | ---------- |
| Feature A | 1000  | 3      | 80%        | 2 weeks | 120        |
| Feature B | 500   | 2      | 90%        | 1 week  | 90         |
| Feature C | 2000  | 1      | 70%        | 3 weeks | 47         |

RICE Score = (Reach × Impact × Confidence) / Effort

Higher score = Higher priority
```

### Backlog Template

```markdown
## Product Backlog

### Now (Current Sprint)

| ID     | Story          | Points | Status      | Assignee |
| ------ | -------------- | ------ | ----------- | -------- |
| US-101 | User login     | 5      | In Progress | @dev1    |
| US-102 | Password reset | 3      | To Do       | @dev2    |

### Next (Next Sprint)

| ID     | Story         | Points | Priority |
| ------ | ------------- | ------ | -------- |
| US-103 | Profile page  | 8      | High     |
| US-104 | Settings page | 5      | Medium   |

### Later (Backlog)

| ID     | Story         | Points | Priority |
| ------ | ------------- | ------ | -------- |
| US-105 | Notifications | 13     | Low      |
| US-106 | Export data   | 8      | Low      |
```

## Sprint Planning

### Sprint Goal Template

```markdown
## Sprint 23

**Duration:** 2 weeks (Jan 15 - Jan 26)
**Goal:** Enable users to manage their profiles

### Sprint Capacity

| Developer | Days Available | Velocity Points |
| --------- | -------------- | --------------- |
| Dev 1     | 9 days         | 15 points       |
| Dev 2     | 8 days         | 13 points       |
| Dev 3     | 10 days        | 17 points       |
| **Total** | 27 days        | 45 points       |

### Sprint Backlog

| ID        | Story          | Points | Assignee |
| --------- | -------------- | ------ | -------- |
| US-101    | User login     | 5      | Dev 1    |
| US-102    | Password reset | 3      | Dev 1    |
| US-103    | Profile page   | 8      | Dev 2    |
| US-104    | Settings page  | 5      | Dev 3    |
| **Total** |                | 21     |          |

### Risks

- Email service integration might be delayed
- Design review pending for profile page
```

## Definition of Done

```markdown
## Definition of Done

A story is done when:

### Development

- [ ] Code is complete and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] No regressions

### Quality

- [ ] QA tested and approved
- [ ] No critical or high bugs
- [ ] Performance acceptable

### Documentation

- [ ] Technical docs updated
- [ ] User docs updated (if needed)
- [ ] API docs updated (if needed)

### Deployment

- [ ] Deployed to staging
- [ ] Verified in staging
- [ ] Ready for production
```

## Roadmap Template

```markdown
## Product Roadmap Q1 2024

### January

- ✅ User Authentication
- ✅ Basic Dashboard
- 🔄 Profile Management

### February

- 📅 Notification System
- 📅 Search Functionality
- 📅 Export Data

### March

- 📅 Payment Integration
- 📅 Reporting Dashboard
- 📅 Mobile App v1

Legend:
✅ Complete | 🔄 In Progress | 📅 Planned
```

## Tips

- Write stories from user perspective
- Keep stories small enough to complete in a sprint
- Regularly groom the backlog
- Involve stakeholders in prioritization
- Track and learn from velocity

## Anti-Patterns

- Never write a user story without acceptance criteria because a story without Given/When/Then tests allows every developer to interpret the requirement differently, guaranteeing inconsistent implementation.
- Never prioritise a feature without a hypothesis about impact because a feature that cannot be connected to a measurable outcome cannot be evaluated after shipping and accumulates as unvalidated scope.
- Never skip defining "definition of done" before sprint planning because without an agreed DoD, "done" means different things to dev, QA, and product, and the sprint never actually closes.
- Never write requirements without consulting a technical stakeholder because requirements written without implementation input routinely contain hidden impossibilities that surface mid-sprint and collapse the estimate.
- Never scope an MVP by adding features rather than removing them because an MVP scoped by addition is a full product with a new label; the only honest MVP scoping technique is to cut until cutting more would invalidate the learning goal.
- Never ship without a rollback plan because a feature with no rollback path forces the team to choose between a bad user experience and an emergency forward fix under pressure, both of which are worse than a prepared rollback.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| User story has no acceptance criteria, developer implements wrong behaviour | Story written as a wish ("I want search") with no Given/When/Then tests defined | Halt implementation until at least 2 acceptance criteria in Given/When/Then format are written and reviewed with the developer |
| Feature scoped as MVP but stakeholders treat MVP as final product | "MVP" not explicitly defined as a learning milestone with a follow-up iteration planned | Document the MVP scope and explicitly call out the features deliberately excluded; schedule an iteration review before MVP ships |
| Priority stack-ranked without effort estimates, causing sprint overcommit | Product backlog ordered by value alone; team pulls stories until sprint feels full without checking velocity | Add story-point estimates to all top-10 backlog items before sprint planning; enforce a hard capacity limit (team velocity × 0.85) |
| "Done" definition missing, causing indefinite QA loop | No Definition of Done checklist agreed upon; "done" means different things to dev, QA, and product | Publish a Definition of Done checklist before sprint starts; any story without a DoD is blocked from moving to In Progress |
| Dependency on external team not surfaced in story, blocking release | Author assumed the external team would deliver; dependency not listed in the story's Dependencies field | Add a Dependencies field to every story template; flag any story with an external dependency as blocked until the dependency confirms its delivery date |

## Self-Verification Checklist

- [ ] Every user story has at least one acceptance criterion in Given/When/Then format — count of stories without acceptance criteria equals 0
- [ ] All stories in the sprint backlog have a story-point estimate — no unpointed stories pulled into sprint planning
- [ ] Definition of Done checklist is present, published, and reviewed with the team before sprint starts
- [ ] Every story follows the "As a [user], I want [goal], So that [benefit]" format with all three fields populated
- [ ] All stories in the sprint backlog fit within the team's velocity capacity (total points ≤ team velocity)
- [ ] Dependencies between stories are identified and sequenced correctly; external dependencies have confirmed delivery dates

## Success Criteria

This task is complete when:
1. The sprint backlog contains stories with clear acceptance criteria, estimates, and assignments within capacity
2. The product roadmap is updated to reflect the current sprint goals and upcoming priorities
3. All stakeholders have reviewed and signed off on the sprint goal and Definition of Done
