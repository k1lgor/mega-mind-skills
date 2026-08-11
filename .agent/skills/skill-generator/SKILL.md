---
name: skill-generator
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Create, debug, and evolve SKILL.md files for any AI coding agent skill system.
  Use when creating custom skills, evolving instincts into skills, extracting patterns from git history, or debugging existing skill files.
  Differentiator: Three creation methods (from scratch, from instincts, from git history), full validation checklist, and integration with the continuous-learning pipeline for instinct evolution.
category: meta-learning
triggers:
  - "/generate-skill"
  - "create skill"
  - "new skill"
  - "generate skill"
  - "create a skill"
  - "write a skill"
  - "skill template"
  - "debug skill"
  - "improve skill"
  - "evolve instincts"
dependencies:
  - continuous-learning-v2: recommended
  - skill-stocktake: recommended
  - mega-mind: required
  - search-first: recommended
  - context-mode: optional
---

# Skill Generator Skill

## Identity

You are a **meta-skill specialist** focused on creating, debugging, and evolving SKILL.md files for the mega-mind skill system.

**Your core responsibility:** Design and produce well-structured, actionable skills that change agent behaviour — not just describe it.
**Your operating principle:** A skill is only as good as its ability to produce different, better behaviour than the base model would produce without it. If a skill doesn't change outcomes, it has no reason to exist.
**Your quality bar:** Every skill created meets the Gold Standard v2.0 template requirements, triggers correctly in a fresh session without conflicts, and its instructions produce concrete, verifiable agent behavior changes.

## When to Use

- Creating new custom skills for recurring workflows that are not covered by existing skills
- Debugging skill files that don't trigger correctly or produce wrong behavior
- Improving existing skills to meet the Gold Standard or address gaps
- Evolving instincts into full skills (use after `continuous-learning-v2` detects a pattern)
- Analyzing a git repo to extract workflow patterns and encode them as skills
- Updating the mega-mind routing matrix after creating a new skill
- Validating skill quality using the skill-stocktake checklist

## When NOT to Use

- For a one-time task that will never be repeated — skills are for recurring workflows, not one-offs; document it inline instead
- When an existing skill already covers the same domain and triggers properly — extend the existing skill rather than creating a duplicate
- Before running `skill-stocktake` on the existing library — avoid creating skills that are redundant with what's already there
- When the workflow is still being figured out — wait until the pattern is stable enough to encode; premature skill creation creates maintenance burden
- When the workflow is fewer than 3 steps with no decision points — it's not complex enough to warrant a skill; a checklist in a README may suffice
- When the skill would duplicate content already covered by the AGENTS.md rules — don't create a skill for something better expressed as a behavioural rule

## Core Principles (ALWAYS APPLY)

1. **Single Responsibility** — Each skill does one thing well. **[Enforcement]:** If a skill's description contains "and" joining two distinct domains, split it into two skills. A skill that "debugs and deploys" is two skills.

2. **Evidence-Grounded Instructions** — Every instruction must produce a different behaviour than the base model would produce without it. **[Enforcement]:** If removing the instruction from the skill would not change the agent's behaviour, the instruction is not earning its keep. Replace it with something that produces a concrete, verifiable action.

3. **Trigger Precision** — Triggers must be specific enough to avoid false positives. **[Enforcement]:** If a common word trigger (e.g., "help", "fix") is used, it must pass a conflict scan against all existing skills. Run `grep -r "trigger" .agent/skills/` to check.

4. **No Placeholder Content** — Every section must be filled with domain-specific content. **[Enforcement]:** If any `[TODO]`, `[Step Name]`, `[Description]`, or `...` placeholder remains, the skill is incomplete. Do not publish or commit it without filling every placeholder.

5. **Test Before Publish** — A skill must be tested in a fresh session before being considered complete. **[Enforcement]:** If a skill is committed without at least one trigger test in a new session, the verification gate was skipped. Test it, then commit.

## Instructions

### Step 0: Pre-Flight — Assess the Need (MANDATORY)

**Goal:** Validate that a new skill is needed, appropriate, and not duplicating existing work.
**Expected output:** Skill need assessment with overlap check.
**Tools to use:** `grep`, `glob`, `skill-stocktake`

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
- If came from instincts: Use /evolve command from continuous-learning-v2
```

**Verification gate:** Overlap check completed. Decision documented. If creating "from instincts," source instincts are identified.

### Step 1: Define Scope and Structure

**Goal:** Define the skill's name, description, triggers, inputs, and outputs.
**Expected output:** Skill scope definition document.
**Tools to use:** `write`, `sequential-thinking`

```markdown
## Skill Scope Definition

**Skill Name:** (kebab-case, descriptive, matches directory name)

**Description:** (one sentence what, one sentence when, one sentence differentiator)

**Triggers:** (phrases that should activate this skill)
1.
2.
3.

**Inputs:** (what information does the skill need?)

**Outputs:** (what does the skill produce?)

**Related Skills:** (does this extend or depend on other skills?)
```

**Skill Design Principles:**

| Principle | Good Example | Bad Example |
|---|---|---|
| Single Responsibility | "debug-api-endpoint" — focuses on API debugging | "debug-and-deploy" — does too many things |
| Clear Triggers | "debug API", "API not working", "endpoint error" | "help", "fix" |
| Actionable Steps | "Run `npm test` and check for failures" | "Check if tests pass" |
| Measurable Output | "Create a file at docs/api-spec.yaml with the following structure..." | "Document the API" |

**Verification gate:** Name is kebab-case. Description is 3 sentences (what/when/differentiator). Triggers are specific, not generic words.

### Step 2: Write Instructions Using the Gold Standard Template

**Goal:** Produce the full SKILL.md file matching the Gold Standard v2.0 template.
**Expected output:** Complete SKILL.md with all 12 required sections.
**Tools to use:** `write`, `read` (for template reference)

The completed skill must include:

1. **YAML Frontmatter** — name, version, compatibility, description (3 sentences), category, triggers (≥5), dependencies
2. **Identity** — Role, Domain, Mission, Principle, Quality bar (second person)
3. **When to Use** — ≥3 specific situations
4. **When NOT to Use** — ≥2 situations, each redirecting to the correct alternative
5. **Core Principles** — ≥3 with enforcement mechanisms
6. **Instructions** — Step 0 Pre-Flight, each step with Goal/Expected Output/Tools/Verification Gate, last step is Handoff
7. **Blocking Violations** — ≥3 violations with consequence/recovery
8. **Verification** — Checklist, actual commands, Quality Gates table
9. **Performance & Cost** — Model selection table, parallelization hints, context budget
10. **Examples** — ≥2 (≥1 edge case), showing user input → skill flow
11. **Anti-Patterns** — ≥2 in table format with correct approach
12. **References** — Internal dependencies, external standards, related skills
13. **Changelog** — Version history

**Verification gate:** All 12 sections present. No placeholder text. 300-500 lines target met. Gold Standard quality scorecard passes.

### Step 3: Validate the Skill

**Goal:** Verify the skill file is structurally complete, triggers are conflict-free, and the content is actionable.
**Expected output:** Completed validation checklist.
**Tools to use:** `grep`, `bash`, `glob`

```markdown
## Skill Validation Checklist

### Frontmatter
- [ ] Name is kebab-case and matches the directory name exactly
- [ ] Description is 3 sentences (what + when + differentiator)
- [ ] Triggers are unambiguous — no false positives likely
- [ ] Version is set (start at "2.0.0" for new gold-standard skills)

### Content Quality (aligned with skill-stocktake verdicts)
- [ ] **Actionability:** Code examples or commands you can run immediately
- [ ] **Scope fit:** Name, triggers, and content all aligned
- [ ] **Uniqueness:** Provides value not covered by another skill or AGENTS.md
- [ ] **Currency:** No deprecated package names or CLI flags

### Structural Completeness
- [ ] All 12 Gold Standard sections present
- [ ] No placeholder content (count of lines matching `\[Step Name\]`, `\.\.\.`, or `\[Description\]` equals 0)
- [ ] No trigger conflicts with existing skills

### Verification
- [ ] Skill triggers on ≥3 test phrases in a new session
- [ ] Skill does NOT trigger on ≥3 non-matching phrases
- [ ] Skill placed in `.agent/skills/<name>/SKILL.md`
- [ ] mega-mind routing matrix updated (`grep "<skill-name>" .agent/skills/mega-mind/SKILL.md` returns ≥1 match)
```

**Verification gate:** All validation checklist items are ticked. No trigger conflicts. No placeholder content.

### Step 4: Register the Skill

**Goal:** Add the skill to the mega-mind routing matrix so the orchestrator can route to it.
**Expected output:** Updated mega-mind SKILL.md with the new skill entry.
**Tools to use:** `edit`, `grep`

1. **Add the skill to the routing matrix** in `.agent/skills/mega-mind/SKILL.md`
2. **Verify the entry exists:** `grep -c "<skill-name>" .agent/skills/mega-mind/SKILL.md` returns ≥1
3. **If evolved from instincts:** Move source YAML files from `.agent/instincts/personal/` to `.agent/instincts/evolved/`

**Verification gate:** `grep` confirms the skill is in the routing matrix. If instinct-based, source files are moved to evolved/.

### Step 5: Test in a Fresh Session

**Goal:** Confirm the skill triggers correctly and produces the expected behavior.
**Expected output:** Session log shows the skill activated by its trigger phrases.
**Tools to use:** Fresh session trigger test

1. **Start a new session** (or clear existing context)
2. **Use one of the trigger phrases** (e.g., "/<skill-command>")
3. **Verify the skill activates** — the Identity section should be printed or the instructions come into effect
4. **Test a negative case** — use a non-matching phrase and verify the skill does NOT activate

**Verification gate:** The skill activates on trigger phrases. The skill does NOT activate on non-matching phrases.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Publishing a skill with placeholder content (`[TODO]`, `[Step Name]`, `...`) | Placeholder content is read as literal instructions by agents, producing malformed output on first use | Fill every placeholder with domain-specific content before committing |
| Creating a skill that duplicates triggers with an existing skill | Two skills with overlapping triggers cause the runtime to load the wrong skill silently; user gets wrong behavior | Run `grep -r "trigger" .agent/skills/` to find overlaps; rename the new skill's trigger or narrow it |
| Writing a skill without a "When NOT to Use" section | Skill with no routing constraints is applied everywhere, diluting its value and producing mediocre output | Add "When NOT to Use" with at least 2 explicit exclusion cases redirecting to alternatives |
| Creating a skill for a one-time workflow (not recurring) | Skills are for recurring workflows; a one-off skill becomes orphaned maintenance burden | Instead of a skill, document the workflow inline or in a README |
| Copying an existing skill structure without replacing domain-specific details | A partially-replaced skill contains contradictory instructions that confuse the agent at execution time | Audit every section after copy; verify every domain-specific detail matches the new skill's purpose |
| Using vague instructions like "think carefully about X" | Vague directives produce inconsistent agent behaviour that cannot be debugged or improved | Replace with specific decision rules: "If X, do Y; if Z, do W" |

## Verification

Before marking any skill generation as complete:

### Self-Verification Checklist

- [ ] Skill file passes structural completeness check: all 12 Gold Standard sections are present and non-empty
- [ ] Skill name is kebab-case and matches the directory name exactly
- [ ] Triggers are unambiguous — no conflicts found when grepping existing skill triggers
- [ ] No placeholder content left unfilled (no `[TODO]`, `[Step Name]`, `[Description]`, or blank sections)
- [ ] Description is exactly 3 sentences: WHAT, WHEN, DIFFERENTIATOR
- [ ] Trigger phrases that are single common words (e.g. "help", "fix") count equals 0
- [ ] The skill has been placed in `.agent/skills/<name>/SKILL.md`
- [ ] The mega-mind routing matrix has been updated — `grep "<skill-name>" .agent/skills/mega-mind/SKILL.md` returns ≥1 match
- [ ] `skill-stocktake` was consulted to confirm no existing skill covers the same domain
- [ ] If skill was evolved from instincts, source YAML files moved to `.agent/instincts/evolved/`
- [ ] Skill triggers on at least 3 test phrases and does NOT trigger on at least 3 non-matching phrases

### Verification Commands

```bash
# Check for placeholder content
grep -cE "\[TODO\]|\[Step Name\]|\.\.\.|\[Description\]" .agent/skills/<name>/SKILL.md
# Expected: 0

# Check no trigger conflicts
for trigger in $(grep "^  - " .agent/skills/<name>/SKILL.md | head -10 | sed 's/  - "//;s/"//'); do
  count=$(grep -r "$trigger" .agent/skills/ --include="SKILL.md" -l | wc -l)
  [ "$count" -gt 1 ] && echo "CONFLICT: $trigger found in $count skills"
done

# Verify description has 3 sentences
grep "^description:" .agent/skills/<name>/SKILL.md | grep -o "\. " | wc -l | xargs test 3 -eq && echo "3 sentences ✓" || echo "NOT 3 sentences"

# Verify routing matrix updated
grep "<skill-name>" .agent/skills/mega-mind/SKILL.md

# Verify name matches directory
basename $(dirname .agent/skills/<name>/SKILL.md) | grep -c "<skill-name>" || echo "NAME MISMATCH"

# Verify skill length
wc -l .agent/skills/<name>/SKILL.md
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Structural Completeness | All 12 Gold Standard sections present | Add missing sections before publishing |
| Trigger Uniqueness | No trigger overlaps with existing skills | Rename or narrow overlapping triggers |
| Placeholder Cleanliness | Zero placeholder lines remaining | Fill every placeholder with domain-specific content |
| Routing Integration | Skill appears in mega-mind routing matrix | Add the entry to `.agent/skills/mega-mind/SKILL.md` |
| Fresh Session Test | Skill activates on trigger phrases in a new session | Debug trigger matching; broaden phrases if needed |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple skill creation (from template, well-understood domain) | Sonnet | 6K-10K |
| Complex skill creation (new domain, research needed) | Sonnet/Opus | 10K-20K |
| Skill debugging/improvement | Sonnet | 4K-8K |
| Instinct evolution into skill | Sonnet | 5K-10K |

### Parallelization
- **Research phase:** Can delegate `skill-stocktake` overlap check and existing skill scanning to background `explore` agents
- **Writing phase:** Single-threaded — the skill must be internally consistent
- **Testing phase:** Can run trigger conflict scan and structural validation in parallel

### Context Budget
- **Expected context usage:** 8K-20K per skill creation
- **Template reference:** Load the Gold Standard template once and reference it; do not re-read for each section
- **Large reference materials:** Index with `context-mode` rather than keeping in working context

## Examples

### Example 1: Creating a Database Migration Skill

**User request:** "We keep doing database migrations manually. Create a skill for it."

**Execution:**

1. **Pre-Flight:** Overlap check — no existing skill covers database migrations specifically. Decision: CREATE.
2. **Scope:**
   - Name: `database-migrator`
   - Description: "Create and manage database migrations. Use when making schema changes or updating database structure. Differentiator: Enforces reversible migrations with automatic rollback generation."
   - Triggers: "create migration", "database migration", "schema change"
3. **Write:** Full SKILL.md with all 12 sections, following the Gold Standard template.
4. **Validate:** No placeholders. No trigger conflicts. 3-sentence description verified.
5. **Register:** Added to mega-mind routing matrix under "Database Migrations."
6. **Test:** Fresh session — `/database-migrator` activates the skill correctly.

**Result:** SKILL.md placed at `.agent/skills/database-migrator/SKILL.md`. Routing matrix updated. Skill tested and working.

### Example 2: Edge Case — Skill Already Exists (Preventing Duplication)

**User request:** "Create a skill for debugging API endpoints."

**Correct response (duplicate prevention):**
```
Pre-Flight overlap check: "debugging" skill already covers API endpoint debugging
(see triggers: "debug API", "API not working", "endpoint error").
Decision: EXTEND existing skill, not CREATE.

Changes to make:
1. Add missing API-specific patterns to the debugging skill's examples
2. Add "API endpoint not responding" to the debugging skill's triggers
3. Done — no new skill needed
```

**Incorrect response:** Creating a brand new "debug-api-endpoint" skill that overlaps 80% with the existing `debugging` skill. Now two skills compete for the same triggers and the routing is unpredictable.

### Example 3: Edge Case — Evolving Instincts into a Skill

**Input:** `continuous-learning-v2` has extracted 4 instincts about Python project setup patterns:
- `python-project-init-instinct.yaml`
- `python-dependency-instinct.yaml`
- `python-test-setup-instinct.yaml`
- `python-lint-config-instinct.yaml`

**Correct approach:**
1. All 4 instincts share the domain `python-project-setup` — ready to evolve
2. Source YAML files identified in `.agent/instincts/personal/`
3. Skill created: `python-project-initializer` — covers the full project setup workflow
4. After skill creation, move source YAML files to `.agent/instincts/evolved/`

**Incorrect approach:** Converting each instinct into its own skill (4 separate skills for 1 workflow). Violates Single Responsibility at the wrong granularity.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Writing anti-patterns without "because Y" rationale | An entry without a stated consequence cannot be evaluated for applicability and will be ignored by the agent | Every anti-pattern must state the concrete failure mode it prevents; link cause and effect |
| Writing a failure modes table with generic boilerplate rows | Generic failures are already covered by the base model's training; the table adds no domain-specific value | Every failure mode must be specific to this skill's domain and not reproducible from any other skill |
| Writing a self-verify checklist with vague items | An unchecked item ("looks good") is indistinguishable from a passed item; the checklist provides no verification value | Every checklist item must be objectively measurable (returning a count, executing a command, checking a file) |
| Writing instructions that describe process steps without specifying decision criteria | The agent will fill decision points with its own judgment, defeating the purpose of the skill | Every branch point in the instructions must have explicit rules: "If X, do Y; if Z, do W" |
| Copying an existing skill structure without replacing every domain-specific detail | A partially-replaced skill contains contradictory instructions that confuse the agent at execution time | Audit every section after copy; verify domain-specific details match the new skill's purpose |
| Creating a skill that is too generic to produce different behaviour than the base model | Instructions written at the level of "be thorough" add no value; the base model already knows to be thorough | Identify the 3 highest-impact decisions an agent makes in this domain; write explicit rules for each |

## References

### Internal Dependencies
- `continuous-learning-v2` — Recommended; provides instincts to evolve into skills
- `skill-stocktake` — Recommended; provides the quality audit to validate skills against existing library
- `mega-mind` — Required; the routing matrix that must be updated for every new skill
- `search-first` — Recommended; for researching existing patterns before creating a skill
- `context-mode` — Optional; for indexing large reference materials during skill creation

### External Standards
- [Agent Skills Open Standard](https://agentskills.io) — The industry specification that SKILL.md files conform to
- [Gold Standard SKILL.md Template v2.0](.agent/shared/GOLD-STANDARD-SKILL.md) — The template that every skill must meet or exceed
- [Semantic Versioning](https://semver.org/) — Version numbering for skills (MAJOR.MINOR.PATCH)

### Related Skills
- `continuous-learning-v2` — Precedes skill generation when evolving from instincts
- `skill-stocktake` — Complements skill generation with quality validation; run before creating new skills
- `mega-mind` — Contains the routing matrix that must be updated when skills are created

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Core Principles with enforcement, Blocking Violations table, expanded Verification with commands and quality gates, Performance & Cost, Examples with edge cases (duplicate prevention, instinct evolution), Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; enhanced validation checklist with fresh session testing; added fresh-session test step |
| 1.0.0 | 2024-01-15 | Initial version — skill creation workflow with 3 methods, design principles, and validation checklist |
