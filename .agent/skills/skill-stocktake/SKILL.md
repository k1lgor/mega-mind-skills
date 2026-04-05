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

## When NOT to Use

- During active feature development — the distraction cost outweighs the benefit mid-sprint
- When auditing a single skill in isolation — the value is in cross-library comparison, not single-skill review
- When the library has fewer than 5 skills — overhead exceeds return at that scale
- As a substitute for fixing a bad skill immediately — if you notice a problem, fix it now rather than scheduling a stocktake

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

## Anti-Patterns

- Never score a skill without reading it fully because skimming a skill and scoring it on the description alone produces inflated Keep verdicts that prevent the library from being cleaned up.
- Never remove a skill without checking if it is referenced elsewhere because deleting a skill that is referenced in a workflow chain or routing matrix leaves broken references that cause silent routing failures.
- Never defer upgrading a thin skill because a thin skill that does not change behaviour costs tokens in every session that loads it; the cumulative cost of inaction exceeds the cost of a one-time upgrade.
- Never add a new skill without checking for duplicates because a duplicate skill creates routing ambiguity, splits related instructions across two files, and produces inconsistent agent behaviour depending on which skill fires.
- Never evaluate all skills against a single rubric dimension because a skill that scores low on actionability but high on uniqueness and currency may still be worth keeping; single-dimension scoring discards valid skills.
- Never update a skill's score without editing the skill to justify it because a score that is not backed by observable content changes is an assertion without evidence, and future audits will contradict it.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Stocktake counts skills but misses skills in subdirectories | Script only scans the top-level `.agent/skills/` directory without recursion | Use `find .agent/skills -name SKILL.md` (or equivalent recursive glob) to count all files including subdirectory skills |
| Scoring rubric applied inconsistently across runs, scores not comparable | Reviewer applies different standards on different days; rubric criteria are vague | Anchor each rubric dimension with a concrete pass/fail example; re-score 3 randomly selected skills from the previous run to calibrate consistency |
| Weak skills identified but no remediation plan created | Stocktake produces verdicts but Phase 4 Action List is skipped under time pressure | For every non-Keep verdict, a concrete action item must be created before the stocktake is considered complete |
| Stocktake run on stale file cache, missing recently added skills | IDE or agent has a cached file listing; new SKILL.md files added after cache was built are invisible | Force a fresh directory listing with `git status` or `ls -R` before Phase 1 Inventory; count files before and after to detect mismatches |
| Score inflation from lenient rubric, masking actual weaknesses | Reviewer marks every skill "Keep" to avoid the work of improving them | Apply the Keep standard strictly: a skill scores Keep only if trigger phrases are unambiguous, examples are runnable, and content is current |

## Self-Verification Checklist

- [ ] Script counts all SKILL.md files including subdirectories — total count matches `find .agent/skills -name SKILL.md | wc -l`
- [ ] Scores are reproducible — re-scoring 3 randomly selected skills from this run produces the same verdict (within 1 rubric point)
- [ ] Remediation plan created for all skills scoring below 3.0 — Action List contains at least one concrete item per weak skill
- [ ] Every skill in the library has a verdict assigned — no skill skipped
- [ ] Each verdict's `reason` field is self-contained — readable without context from this session
- [ ] Trigger conflicts across all Keep skills have been checked and resolved

## Success Criteria

This skill is complete when: 1) Every skill in the library has a Keep/Improve/Update/Retire/Merge verdict with a self-contained reason. 2) All non-Keep verdicts have specific, actionable next steps in the Action List. 3) The summary table is complete and can serve as a standalone library health record.
