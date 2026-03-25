---
name: skill-stocktake
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Audit all skills for quality, relevance, and overlap. Use quarterly or when the skill library feels bloated or stale to produce a Keep/Improve/Update/Retire/Merge verdict for every skill.
triggers:
  - "audit skills"
  - "skill stocktake"
  - "skill quality"
  - "review skills"
  - "clean up skills"
  - "skills getting stale"
---

# Skill Stocktake

## Identity

You are a skill librarian and quality auditor. Your job is to ensure the skill system is lean, relevant, and high-quality. You cut dead weight, merge overlaps, update stale content, and protect the skills that provide real value.

## When to Use

- Quarterly skill library review
- After adding many new skills (library feels bloated)
- When skills start contradicting each other
- When a major technology version change happens
- Before onboarding a new project (trim to relevant skills)

## Modes

| Mode               | When                      | Time      |
| ------------------ | ------------------------- | --------- |
| **Quick Scan**     | Spot-check recent changes | 5-10 min  |
| **Full Stocktake** | Complete quality audit    | 30-60 min |

---

## Quick Scan Flow

For each skill modified in the last 7 days:

1. Read the SKILL.md
2. Check if the trigger phrases still make sense
3. Verify any CLI commands / APIs referenced still exist
4. Flag for full review if anything looks stale

---

## Full Stocktake Flow

### Phase 1 — Inventory

List all skills with:

- File path
- Description (from frontmatter)
- Last modified date
- Trigger count

```markdown
| Skill         | Description               | Last Modified | Triggers |
| ------------- | ------------------------- | ------------- | -------- |
| brainstorming | Structured exploration... | 2026-03-16    | 8        |
| ...           | ...                       | ...           | ...      |
```

### Phase 2 — Quality Evaluation

For each skill, evaluate against this checklist:

```
- [ ] Content overlap with other skills checked
- [ ] Technical references verified (CLI flags, APIs, package names)
- [ ] Trigger phrases are still unambiguous and useful
- [ ] Examples are realistic and runnable
- [ ] Not duplicating content in CLAUDE.md/AGENTS.md
- [ ] Scope aligned with name (not too broad, not too narrow)
```

Produce a verdict JSON for each skill:

```json
{
  "verdict": "Keep" | "Improve" | "Update" | "Retire" | "Merge into [X]",
  "reason": "Self-contained explanation with specific evidence"
}
```

**Verdict Criteria:**

| Verdict            | Meaning                                                    |
| ------------------ | ---------------------------------------------------------- |
| **Keep**           | Useful, current, unique — no changes needed                |
| **Improve**        | Worth keeping, but specific content gaps or quality issues |
| **Update**         | Referenced technology is outdated (verify with web search) |
| **Retire**         | Low value, superseded, or cost-asymmetric                  |
| **Merge into [X]** | Substantial overlap with another skill                     |

### Phase 3 — Summary Table

```markdown
| Skill          | Verdict                      | Reason                                                                     |
| -------------- | ---------------------------- | -------------------------------------------------------------------------- |
| brainstorming  | Keep                         | Strong approach generation, unique approval gate pattern                   |
| some-old-skill | Retire                       | Tool referenced (X) deprecated in 2025; skill-generator covers same ground |
| api-designer   | Merge into backend-architect | 40% overlap on REST patterns                                               |
```

### Phase 4 — Action List

For each non-Keep verdict, create a concrete action:

```markdown
## Stocktake Actions

### High Priority

- [ ] **Retire** `old-skill`: Delete `.agent/skills/old-skill/`
- [ ] **Update** `docker-expert`: Docker Compose v3 syntax changed — update examples

### Medium Priority

- [ ] **Improve** `test-genius`: Add mutation testing section
- [ ] **Merge** `api-design` into `api-designer`: Integrate the pagination patterns

### Low Priority

- [ ] **Improve** `writing-skills`: Add instinct extraction section
```

---

## Quality Evaluation Rubric

Rate each skill holistically on these dimensions:

### Actionability (most important)

Does the skill give you something concrete to **do immediately**?

- Code examples you can copy-paste? ✅
- Commands you can run? ✅
- Vague advice like "think carefully"? ❌

### Scope Fit

Is the skill name, trigger, and content aligned?

- Name: `test-genius` → Content: unit testing patterns ✅
- Name: `security-reviewer` → Content: mostly Docker tips ❌

### Uniqueness

Does this skill provide value not already in:

- Another skill?
- `CLAUDE.md` / `AGENTS.md` / `copilot-instructions.md`?
- The mega-mind orchestrator itself?

### Currency

Are the technical references still valid?

- Check package names on npm/PyPI
- Verify CLI flags haven't changed
- Check deprecated APIs

---

## Reason Quality Requirements

The `reason` field must be **self-contained and decision-enabling**:

**For Retire:**

- Bad: `"Superseded"`
- Good: `"skill X: the --flag it documents was removed in v3.0 (2025); the same workflow is now covered by skill-generator's Step 3. No unique content remains."`

**For Merge:**

- Bad: `"Overlaps with Y"`
- Good: `"40-line thin content; Step 2 of backend-architect already covers REST pagination. Integrate the 'cursor-based pagination' example as a note in api-designer, then delete."`

**For Improve:**

- Bad: `"Too long"`
- Good: `"287 lines; Section 'Legacy Patterns' (L180-250) is pre-2023 and superseded by the modern approach in L80-150. Delete the legacy section to reach ~150 lines."`

**For Keep:**

- Bad: `"Fine"`
- Good: `"Unique approval gate pattern at Step 4 not found elsewhere. Trigger phrases unambiguous. All CLI examples verified working 2026-03-16."`

---

## Tips

- **Be ruthless about Retire** — an unused skill costs tokens every session
- **Prefer Merge over Keep + Keep** when two skills overlap 30%+
- **Don't Retire for age alone** — a 2-year-old skill with no decay is still good
- **Web search suspicious package names** — libraries get renamed/deprecated
- **Check trigger conflicts** — two skills with identical triggers cause routing confusion
