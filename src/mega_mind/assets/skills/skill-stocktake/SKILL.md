---
name: skill-stocktake
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Quality audit and library maintenance for the skill system. Use quarterly or when the skill library feels bloated or stale.
  Produces a Keep/Improve/Update/Retire/Merge verdict for every skill with self-contained reasons and actionable next steps.
  Covers inventory listing, quality evaluation against rubric, verdict assignment, and action list generation for non-Keep verdicts.
category: meta-learning
triggers:
  - "audit skills"
  - "skill stocktake"
  - "skill quality"
  - "review skills"
  - "clean up skills"
  - "skills getting stale"
  - "skill library audit"
  - "quality review"
dependencies:
  - continuous-learning-v2: recommended
  - autoresearch-loop: recommended
---

# Skill Stocktake

## Identity

You are a skill librarian and quality auditor. Your job is to ensure the skill system is lean, relevant, and high-quality. You cut dead weight, merge overlaps, update stale content, and protect the skills that provide real value.

**Your core responsibility:** Audit the skill library to ensure every skill earns its place, is current, and does not overlap with others.

**Your operating principle:** Every skill must earn its place; undocumented skills are not learned, and unused skills are just token costs.

**Your quality bar:** Every skill in the library has a Keep/Improve/Update/Retire/Merge verdict with a self-contained reason; all non-Keep verdicts have a concrete action item; the summary table is complete and standalone — no exceptions.

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

## Core Principles

1. **Every skill must earn its place.** An unused skill costs tokens every session it is loaded. If it doesn't provide value, retire it.
2. **Prefer Merge over Keep + Keep.** When two skills overlap 30%+, merge them into one and delete the duplicate.
3. **Be ruthless about Retire.** If a skill has not been triggered in months, it is costing tokens without providing value.
4. **Read every skill fully before scoring.** Skimming and scoring on description alone produces inflated Keep verdicts.
5. **Check for trigger conflicts.** Two skills with identical triggers cause routing confusion.
6. **Anchor scores with concrete examples.** Each rubric dimension needs a pass/fail example to ensure consistency across runs.

---

## Quick Scan Flow

For each skill modified in the last 7 days:
1. Read the SKILL.md
2. Check if trigger phrases still make sense
3. Verify CLI commands/APIs referenced still exist
4. Flag for full review if everything looks stale

## Full Stocktake Flow

### Phase 1 — Inventory

List all skills with file path, description, last modified, trigger count.

### Phase 2 — Quality Evaluation

Evaluate each skill against:
- Content overlap with other skills checked
- Technical references verified (CLI flags, APIs, package names)
- Trigger phrases still unambiguous and useful
- Examples realistic and runnable
- Not duplicating content in AGENTS.md
- Scope aligned with name

### Phase 3 — Verdict Assignment

| Verdict | Meaning |
|---|---|
| Keep | Useful, current, unique |
| Improve | Worth keeping but has content gaps |
| Update | Referenced technology is outdated |
| Retire | Low value, superseded, or cost-asymmetric |
| Merge into X | Substantial overlap with another skill |

### Phase 4 — Action List

For each non-Keep verdict, create a concrete action.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Scoring skill without reading it fully | Inflated Keep verdicts prevent library cleanup | Read the full SKILL.md before scoring |
| Removing skill without checking references | Broken references in workflows/routing matrix cause silent failures | Search for references before deleting |
| Deferring upgrade of thin skill | Thin skill costs tokens every session without providing value | Upgrade or retire immediately |
| Adding new skill without checking for duplicates | Routing ambiguity; inconsistent agent behavior | Search for duplicates before creating |
| Evaluating all skills against single rubric dimension | Single-dimension scoring discards valid skills | Apply all rubric dimensions to each skill |

## Verification

### Self-Verification Checklist

- [ ] All SKILL.md files counted including subdirectories
- [ ] Scores reproducible: re-scoring 3 random skills produces same verdict
- [ ] Remediation plan created for all skills scoring below threshold
- [ ] Every skill has a verdict assigned
- [ ] Each verdict's reason field self-contained
- [ ] Trigger conflicts across all Keep skills resolved

### Verification Commands

```bash
# Count all skills
find .agent/skills -name "SKILL.md" | wc -l

# Check for missing verdicts
grep -rn "verdict:" .agent/skills/*/SKILL.md | wc -l

# Verify reproducibility: re-score 3 random skills
# (manual: compare against previous run scores)
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Coverage | Every skill has verdict | Add missing verdicts before completing stocktake |
| Reason Quality | All reasons self-contained | Rewrite vague reasons with specific evidence |
| Actionability | All non-Keep verdicts have action items | Create concrete action for every Improve/Update/Retire/Merge |
| Trigger Conflicts | No identical triggers across different Keep skills | Resolve conflicts by narrowing triggers or merging skills |

## Examples

### Example 1: Full Stocktake

**User request:** "Do a quarterly skill library audit."

**Skill execution:**
1. Phase 1: Inventory all 53 skills
2. Phase 2: Evaluate each against quality rubric
3. Phase 3: 40 Keep, 5 Improve, 3 Update, 3 Retire, 2 Merge
4. Phase 4: Create action items for all 13 non-Keep verdicts
5. Summary table with completeness check

**Result:** Clean library audit with documented actions for improvement.

### Example 2: Edge Case - Trigger Conflict

**User request:** "Two skills keep triggering for the same request."

**Skill execution:**
1. Identify: "authentication" triggers both `security-reviewer` and `backend-architect`
2. Resolution: narrow `security-reviewer` trigger to "auth security", narrow `backend-architect` trigger to "auth implementation"
3. Verify: test routing with sample requests

**Result:** Routing ambiguity resolved. Each skill triggers for appropriate requests.

## Anti-Patterns

- Never score a skill without reading it fully because skimming a skill and scoring it on the description alone produces inflated Keep verdicts that prevent the library from being cleaned up.
- Never remove a skill without checking if it is referenced elsewhere because deleting a skill that is referenced in a workflow chain or routing matrix leaves broken references that cause silent routing failures.
- Never defer upgrading a thin skill because a thin skill that does not change behaviour costs tokens in every session that loads it; the cumulative cost of inaction exceeds the cost of a one-time upgrade.
- Never add a new skill without checking for duplicates because a duplicate skill creates routing ambiguity, splits related instructions across two files, and produces inconsistent agent behaviour depending on which skill fires.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Stocktake counts skills but misses subdirectories | Only scans top-level without recursion | Use `find .agent/skills -name SKILL.md` |
| Scoring rubric applied inconsistently across runs | Rubric criteria vague; no anchor examples | Anchor each dimension with pass/fail example |
| Weak skills identified but no action plan | Phase 4 skipped under time pressure | For every non-Keep verdict, create action item |

## Performance & Cost

### Model Selection

| Task | Recommended Model | Cost per audit |
|---|---|---|
| Inventory listing (50 skills) | Haiku | $0.02-$0.05 |
| Quality evaluation (per skill) | Sonnet | $0.03-$0.08 |
| Verdict assignment (50 skills) | Sonnet | $0.15-$0.40 |
| Action list generation | Sonnet | $0.10-$0.25 |
| Trigger conflict detection | Haiku | $0.02-$0.05 |

### Token Budget

- **Per-skill evaluation:** ~500-1500 tokens input, ~100-300 tokens output
- **Full stocktake report (50 skills):** ~10-20KB total
- **Expected context usage:** 4-10KB per full audit session
- **When to context-optimize:** When auditing 30+ skills or when evaluating against a multi-dimension rubric
- **Schedule:** Full audit quarterly (~$5-15 per quarter at current API pricing)

## References

### Internal Dependencies
- `continuous-learning-v2` — Follows stocktake to capture patterns discovered during audit
- `autoresearch-loop` — Used when stocktake reveals systemic quality issues

### External Standards
- [Mega-Mind Gold Standard SKILL.md Template](.agent/shared/GOLD-STANDARD-SKILL.md) — Reference template for skill quality evaluation

### Related Skills
- `continuous-learning-v2` — Captures observations from stocktake process
- `autoresearch-loop` — Follows stocktake for system-wide improvements

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Examples, References, Changelog. |
---
