---
name: writing-skills
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Create new skills that follow the system's conventions. Use when creating custom skills.
triggers:
  - "create a skill"
  - "write a skill"
  - "new skill"
---

# Writing Skills Skill

## When to Use

- Creating a new custom skill
- Extending the mega-mind system
- Documenting a new workflow

## Skill Structure

Every skill consists of:

```
skill-name/
└── SKILL.md       # Main skill file (required)
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Clear description of what this skill does and when to use it.
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
  - "keyword"
---

# Skill Name Skill

## When to Use

- Situation 1
- Situation 2

## Instructions

### Step 1: [Step Name]

Instructions for step 1...

### Step 2: [Step Name]

Instructions for step 2...

## Examples

Examples of using the skill...

## Tips

Best practices and tips...
```

## Frontmatter Fields

| Field         | Required | Description                            |
| ------------- | -------- | -------------------------------------- |
| `name`        | Yes      | Unique skill identifier (kebab-case)   |
| `description` | Yes      | What the skill does and when to use    |
| `triggers`    | No       | Phrases that should trigger this skill |

## Creating a New Skill

### Phase 0: Extracting Instincts (Optional but Recommended)

Before creating a skill from scratch, check if you've already learned the pattern:

1.  **Check Observations**: Run `rtk ls .agent/instincts/observations/` to see recent session captures.
2.  **Review Raw Instincts**: Read `.agent/instincts/personal/*.yaml` for existing behavioral triggers.
3.  **Identify Clusters**: If 3+ instincts share the same `domain` (e.g., `testing`, `api-design`), they are ready to be evolved into a formal skill.

### Phase 1: Identify the Need

Ask yourself:

- What problem does this skill solve?
- Is this already covered by an existing skill?
- Will this skill be reused?

### Step 2: Define the Workflow

Document the steps:

1. What information is needed to start?
2. What are the decision points?
3. What is the output/deliverable?

### Step 3: Write the Skill

Create the SKILL.md file:

```markdown
---
name: my-custom-skill
description: Description of what this skill does. Use when [specific situations].
triggers:
  - "custom trigger"
  - "another trigger"
---

# My Custom Skill

## When to Use

- When situation A occurs
- When you need to do B

## Instructions

### Step 1: Gather Information

- What to collect
- Where to find it

### Step 2: Analyze

- How to process the information
- What to look for

### Step 3: Execute

- What actions to take
- How to verify

## Output Format

Template for the output...

## Examples

Example usage scenarios...

## Tips

- Tip 1
- Tip 2
```

### Phase 4: Test the Skill

1. Place in `.agent/skills/my-custom-skill/SKILL.md`
2. Start a new session
3. Test with trigger phrases
4. Verify the workflow makes sense
5. Iterate and improve

### Phase 5: Closing the Loop (Continuous Learning)

1.  **Mark as Evolved**: If this skill was created from instincts, move those source YAML files to `.agent/instincts/evolved/`.
2.  **Update Mega-Mind**: Add the new skill to the `mega-mind` routing matrix in `.agent/skills/mega-mind/SKILL.md`.

## Skill Design Principles

### 1. Single Responsibility

Each skill should do one thing well.

```
Good: "debug-api-endpoint" - Focuses on API debugging
Bad: "debug-and-deploy" - Does too many things
```

### 2. Clear Triggers

Triggers should be unambiguous.

```markdown
Good:
triggers:

- "debug API"
- "API not working"
- "endpoint error"

Bad:
triggers:

- "help"
- "fix"
```

### 3. Actionable Steps

Steps should be concrete actions, not vague suggestions.

```
Good: "Run `bun test (or npm test)` and check for failures"
Bad: "Check if tests pass"
```

### 4. Measurable Output

The skill should produce verifiable output.

```
Good: "Create a file at docs/api-spec.yaml with the following structure..."
Bad: "Document the API"
```

## Example: Creating a Deployment Skill

````markdown
---
name: deploy-to-staging
description: Deploy the current branch to staging environment. Use when ready to test changes in a production-like environment.
triggers:
  - "deploy to staging"
  - "push to staging"
  - "test on staging"
---

# Deploy to Staging Skill

## When to Use

- Feature is ready for QA
- Need to test in production-like environment
- Before final production deployment

## Prerequisites

- All tests pass
- Code has been reviewed
- Branch is up to date with main

## Instructions

### Step 1: Pre-Deployment Check

```bash
rtk bun test (or rtk npm test)
rtk bun run lint (or rtk npm run lint)
rtk bun run build (or rtk npm run build)
```
````

All must pass before proceeding.

### Step 2: Create Deployment PR

- Push branch to origin
- Create PR with "staging" label
- Wait for CI to pass

### Step 3: Trigger Deployment

```bash
# Via CI/CD
gh workflow run deploy.yml -f environment=staging -f branch=$(git branch --show-current)
```

### Step 4: Verify Deployment

1. Check deployment status
2. Run smoke tests
3. Verify key functionality

## Verification Checklist

- [ ] App loads on staging URL
- [ ] Health check passes
- [ ] Key user flows work
- [ ] No errors in logs

## Rollback

If issues found:

```bash
gh workflow run rollback.yml -f environment=staging
```

## Tips

- Deploy early and often
- Always verify after deployment
- Have rollback plan ready

```

## Tips for Skill Writers

1. **Use existing skills as templates** - Copy structure from similar skills
2. **Keep it focused** - One clear purpose per skill
3. **Test with real scenarios** - Use the skill on actual work
4. **Iterate** - Improve based on usage patterns
5. **Document edge cases** - Add tips for unusual situations
6. **Include examples** - Make it easy to understand
```
