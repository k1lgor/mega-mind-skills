---
name: skill-generator
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Creating and debugging new SKILL.md files. Use for creating custom skills.
triggers:
  - "create skill"
  - "new skill"
  - "generate skill"
  - "create a skill"
  - "write a skill"
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

## When NOT to Use

- For a one-time task that will never be repeated — skills are for recurring workflows, not one-offs
- When an existing skill already covers the same domain and triggers — create a duplicate only if the existing skill is structurally incompatible
- Before running `skill-stocktake` on the existing library — avoid creating skills that are redundant with what's already there
- When the workflow is still being figured out — wait until the pattern is stable enough to encode
- When the workflow is fewer than 3 steps with no decision points — it's not complex enough to warrant a skill

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

### Phase 0: Extracting Instincts (Optional but Recommended)

Before creating a skill from scratch, check if you've already learned the pattern:

1. **Check Observations**: Run `rtk ls .agent/instincts/observations/` to see recent session captures.
2. **Review Raw Instincts**: Read `.agent/instincts/personal/*.yaml` for existing behavioral triggers.
3. **Identify Clusters**: If 3+ instincts share the same `domain` (e.g., `testing`, `api-design`), they are ready to be evolved into a formal skill.

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

### Phase 4: Test the Skill

1. Place in `.agent/skills/my-custom-skill/SKILL.md`
2. Start a new session
3. Test with trigger phrases
4. Verify the workflow makes sense
5. Iterate and improve

### Phase 5: Closing the Loop (Continuous Learning)

1. **Mark as Evolved**: If this skill was created from instincts, move those source YAML files to `.agent/instincts/evolved/`.
2. **Update Mega-Mind**: Add the new skill to the `mega-mind` routing matrix in `.agent/skills/mega-mind/SKILL.md`.

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
```

## Anti-Patterns

- Never write a skill without a "When NOT to Use" section because a skill with no routing constraints is applied everywhere, diluting its value and producing mediocre output for tasks that don't need it.
- Never write anti-patterns without "because Y" rationale because an entry without a stated consequence cannot be evaluated for applicability and will be ignored by the agent.
- Never write a failure modes table with generic boilerplate rows because generic failures are already covered by the base model's training and the table adds no domain-specific value.
- Never write a self-verify checklist with vague items because an unchecked item ("looks good") is indistinguishable from a passed item and the checklist provides no verification value.
- Never write a skill that describes process steps without specifying what constitutes a good decision at each branch point because the agent will fill decision points with its own judgment, defeating the purpose of the skill.
- Never copy an existing skill structure without replacing every domain-specific detail because a partially-replaced skill contains contradictory instructions that confuse the agent at execution time.
- Never use vague instructions like "think carefully about X" because vague directives produce inconsistent agent behavior that cannot be debugged or improved without guessing at the intended interpretation.
- Never leave placeholder content unfilled because unfilled placeholders get read as literal instructions by agents, producing malformed or nonsensical output on first use.
- Never add duplicate triggers that conflict with existing skills because overlapping triggers cause the runtime to load the wrong skill silently, producing behavior the user never intended with no visible error.

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

Review the required schema changes and determine what tables/columns need modification.

### Step 2: Create Migration File

```typescript
// migrations/YYYYMMDD_description.ts
export async function up(knex: Knex) {
  await knex.schema.createTable("users", (table) => {
    table.uuid("id").primary().defaultTo(knex.raw("gen_random_uuid()"));
    table.string("email").notNullable().unique();
    table.timestamps(true, true);
  });
}

export async function down(knex: Knex) {
  await knex.schema.dropTable("users");
}
```

### Step 3: Test Migration

- Run up migration on test database, verify schema changes
- Run down migration, verify rollback works

## Tips

- Always create reversible migrations
- Use transactions for safety
- Test on backup before production
````

## Self-Verification Checklist

- [ ] Skill triggers on at least 3 test phrases and does NOT trigger on at least 3 non-matching phrases — tested in a new session
- [ ] Skill file passes structural completeness check: When to Use, When NOT to Use, and Self-Verify sections are all present and non-empty
- [ ] Skill name is kebab-case and matches the directory name exactly
- [ ] Triggers are unambiguous — no conflicts found when grepping existing skill triggers
- [ ] No placeholder content left unfilled (no `[TODO]`, `[add content here]`, or blank sections)
- [ ] No placeholder text remains — count of lines matching `\[Step Name\]`, `\.\.\.`, or `\[Description\]` in SKILL.md equals 0
- [ ] Trigger phrases are unambiguous — count of trigger phrases that are single common words (e.g. "help", "fix") equals 0
- [ ] The skill has been placed in `.agent/skills/<name>/SKILL.md` and tested with a fresh session trigger — session log shows the trigger activated the skill
- [ ] The `mega-mind` routing matrix has been updated — `grep "<skill-name>" .agent/skills/mega-mind/SKILL.md` returns ≥1 match
- [ ] `skill-stocktake` was consulted to confirm no existing skill covers the same domain — stocktake verdict shows "New" or "Keep"
- [ ] If skill was evolved from instincts, source YAML files moved to `.agent/instincts/evolved/` — `ls .agent/instincts/personal/<name>.yaml` returns "No such file"

## Success Criteria

This skill is complete when: 1) the SKILL.md file is fully filled out with domain-specific, non-placeholder content, 2) the triggers have been validated against the existing skill library for conflicts, 3) a fresh session correctly activates the skill via its trigger phrases, and 4) the mega-mind routing matrix reflects the new skill.

## Failure Modes

| Failure                                                                 | Cause                                                                                                 | Recovery                                                                                                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Skill never triggers in practice because trigger phrases too narrow     | Trigger phrases are exact strings the author would say, not phrases users naturally use               | Test the skill with 5 different phrasings a user might actually type; broaden triggers to natural-language variants              |
| Skill triggers conflict with existing skill, causing ambiguous routing  | Two skills share a trigger phrase; routing is undefined                                               | Run `grep -r "trigger" .agent/skills/` to find overlaps; rename the new skill's trigger or narrow it with a more specific phrase |
| Skill too broad (matches everything), displacing more specific skills   | Description contains generic words like "coding", "development", "fix"                                | Rewrite description with domain-specific nouns rather than generic verbs                                                         |
| Skill prompt is too long, eating context before agent begins work       | Skill includes full implementation examples, large tables, and repeated boilerplate; total >300 lines | Trim to instructions + one minimal example; move exhaustive reference to a linked doc                                            |
| Self-verify section omitted, no way to know if skill applied correctly  | Skill created from template but self-verify section left as placeholder or deleted                    | Add a self-verify section with at least 3 measurable checkboxes before publishing the skill                                      |
| Skill is too generic to produce different behaviour than the base model | Instructions written at the level of "be thorough"; no domain-specific decision rules                 | Identify the 3 highest-impact decisions an agent makes in this domain; write explicit rules for each                             |
| Anti-patterns section has no "because Y" rationale                      | Entries written as "Never do X" without explaining the consequence                                    | Every anti-pattern must state the concrete failure mode it prevents; add "because Y" to every entry                              |
| Skill routing section missing or too permissive                         | No "When NOT to Use" section; skill applied in every situation                                        | Add "When NOT to Use" with at least 2 explicit exclusion cases                                                                   |

## Tips for Skill Creators

1. **Keep skills focused** - One clear purpose
2. **Use consistent formatting** - Follow the template
3. **Include practical examples** - Show, don't just tell
4. **Test your skills** - Use them yourself
5. **Iterate based on usage** - Improve over time
6. **Use existing skills as templates** - Copy structure from similar skills
7. **Document edge cases** - Add tips for unusual situations
