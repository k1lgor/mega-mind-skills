---
name: skill-generator
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Creating and debugging new SKILL.md files. Use for creating custom skills.
triggers:
  - "create skill"
  - "new skill"
  - "generate skill"
---

# Skill Generator Skill

## Identity

You are a meta-skill specialist focused on creating new skills for the mega-mind system. You can create skills from scratch, evolve them from instincts, or extract them from git history analysis.

## When to Use

- Creating new custom skills
- Debugging skill files
- Improving existing skills
- Evolving instincts into full skills (use after `continuous-learning-v2`)
- Analyzing a git repo to extract workflow patterns into skills

## Skill Creation Methods

| Method               | When to Use                   | Work Required |
| -------------------- | ----------------------------- | ------------- |
| **From scratch**     | You know the workflow         | High          |
| **From instincts**   | You have 3+ related instincts | Low           |
| **From git history** | Existing repo with patterns   | Automated     |

## Skill Template

````markdown
---
name: skill-name
description: Clear, concise description of what this skill does and when to use it. One sentence for what, one for when.
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
  - "keyword"
---

# Skill Name Skill

## Identity

You are a [role] specialist focused on [domain/expertise].

## When to Use

- Situation 1
- Situation 2
- Situation 3

## Instructions

### Step 1: [First Step]

Detailed instructions for the first step...

### Step 2: [Second Step]

Detailed instructions for the second step...

### Step 3: [Third Step]

Detailed instructions for the third step...

## Examples

### Example 1: [Scenario]

```
Input: [example input]
Output: [example output]
```

### Example 2: [Another Scenario]

...

## Templates

```markdown
## Template Name

| Field | Description |
| ----- | ----------- |
| ...   | ...         |
```

## Tips

- Tip 1
- Tip 2
- Tip 3
````

## Skill Creation Process

### Step 1: Identify the Need

```markdown
## Skill Need Assessment

**Problem:** What specific problem does this skill solve?

**Method:** How will this skill be created?

- [ ] From scratch (new workflow)
- [ ] From instincts (see continuous-learning-v2 for /evolve)
- [ ] From git history analysis

**Frequency:** How often will this skill be needed?

- [ ] Frequently (daily)
- [ ] Occasionally (weekly)
- [ ] Rarely (monthly)

**Complexity:** How complex is the task?

- [ ] Simple (can be explained briefly)
- [ ] Medium (needs structured approach)
- [ ] Complex (needs detailed steps)

**Overlap Check:** Run `skill-stocktake` quick scan — does a skill already cover this?

- [ ] Checked existing skills — no overlap found
- [ ] Similar skill found: [name] — consider extending instead of creating new

**Decision:** Is this worth a new skill?

- If the task is unique and will be repeated: YES
- If similar to existing skill: Enhance existing (don't duplicate)
- If one-time task: Skip skill creation
- If came from instincts: Use `/evolve` command from `continuous-learning-v2`
```

### Step 2: Define Scope

```markdown
## Skill Scope Definition

**Skill Name:** (kebab-case, descriptive)

**Description:** (one sentence what, one sentence when)

**Triggers:** (phrases that should activate this skill)

1.
2.
3.

## **Inputs:** (what information does the skill need?)

## **Outputs:** (what does the skill produce?)

## **Related Skills:** (does this extend or depend on other skills?)
```

### Step 3: Write Instructions

```markdown
## Writing Guidelines

1. **Start with Identity** - Define the role clearly
2. **List When to Use** - Be specific about scenarios
3. **Number the Steps** - Clear sequence of actions
4. **Provide Examples** - Real-world scenarios
5. **Include Templates** - Reusable formats
6. **Add Tips** - Best practices and gotchas
```

## Validation Checklist

```markdown
## Skill Validation Checklist

### Frontmatter

- [ ] Name is kebab-case
- [ ] Description is clear and concise (what + when)
- [ ] Triggers are unambiguous (test: would you say this phrase to mean something else?)

### Content Quality (aligned with skill-stocktake verdicts)

- [ ] **Actionability**: Code examples or commands you can run immediately
- [ ] **Scope fit**: Name, triggers, and content all aligned
- [ ] **Uniqueness**: Provides value not covered by another skill or CLAUDE.md
- [ ] **Currency**: No deprecated package names or CLI flags

### Structure

- [ ] Identity section present
- [ ] When to Use section clear with specific scenarios
- [ ] Instructions are numbered and concrete
- [ ] Examples are realistic (not "foo"/"bar" placeholder examples)
- [ ] At least one runnable code block
- [ ] Tips section with non-obvious best practices

### Anti-Patterns to Avoid

- [ ] No vague instructions like "think carefully about X"
- [ ] No placeholder content that wasn't filled in
- [ ] No duplicate triggers that conflict with existing skills
- [ ] No content > 300 lines without strong justification
```

## Example: Creating a Database Migration Skill

````markdown
---
name: database-migrator
description: Create and manage database migrations. Use when making schema changes or updating database structure.
triggers:
  - "create migration"
  - "database migration"
  - "schema change"
---

# Database Migrator Skill

## Identity

You are a database migration specialist focused on safely managing database schema changes.

## When to Use

- Creating new migrations
- Applying schema changes
- Rolling back migrations
- Managing database versions

## Instructions

### Step 1: Analyze Required Changes

Review the required schema changes:

- What tables need modification?
- What columns need adding/removing?
- Are there data transformations needed?

### Step 2: Create Migration File

Generate migration file with up and down methods:

```typescript
// migrations/YYYYMMDD_description.ts
export async function up(knex: Knex) {
  // Apply changes
}

export async function down(knex: Knex) {
  // Reverse changes
}
```

### Step 3: Test Migration

Always test both directions:

- Run up migration on test database
- Verify schema changes
- Run down migration
- Verify rollback works

## Examples

```typescript
export async function up(knex: Knex) {
  await knex.schema.createTable("users", (table) => {
    table.uuid("id").primary().defaultTo(knex.raw("gen_random_uuid()"));
    table.string("email").notNullable().unique();
    table.string("name").notNullable();
    table.timestamps(true, true);
  });
}

export async function down(knex: Knex) {
  await knex.schema.dropTable("users");
}
```

## Tips

- Always create reversible migrations
- Use transactions for safety
- Test on backup before production
- Document breaking changes

```

```
````

## Tips for Skill Creators

1. **Keep skills focused** - One clear purpose
2. **Use consistent formatting** - Follow the template
3. **Include practical examples** - Show, don't just tell
4. **Test your skills** - Use them yourself
5. **Iterate based on usage** - Improve over time
