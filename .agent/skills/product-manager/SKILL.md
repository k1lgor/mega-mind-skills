---
name: product-manager
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
