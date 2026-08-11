# Gold Standard SKILL.md Template v2.0

> **The universal template for creating world-class Agent Skills.**
> Every skill in Mega-Mind must meet or exceed this standard.
> Based on: Agent Skills specification, Fugu Conductor/Orchestrator patterns,
> Sakana AI TRINITY/Conductor research, and production-grade skill engineering.

---

## Template Structure (12 Required Sections)

Every SKILL.md MUST contain all 12 sections. Sections marked `[OPTIONAL]` are required for
complex skills (300+ lines) but may be condensed for simpler skills (under 200 lines).

---

## 1. YAML Frontmatter (REQUIRED)

```yaml
---
name: skill-name
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  [One sentence: WHAT this skill does].
  [One sentence: WHEN to use it].
  [One sentence: WHAT makes it unique/different].
category: [core-workflow | domain-expert | meta-learning | token-optimization]
triggers:
  - "/command-name"
  - "natural language trigger 1"
  - "natural language trigger 2"
  - "keyword"
dependencies:
  - skill-name: [required | optional | recommended]
  - context-mode: [required | optional]
  - rtk: [optional]
---
```

**Rules:**
- `version` MUST be present — semantic versioning (MAJOR.MINOR.PATCH)
- `description` MUST be exactly 3 sentences: WHAT, WHEN, DIFFERENTIATOR
- `triggers` MUST include at minimum: 1 slash command, 2 natural language phrases, 2 keywords
- `dependencies` MUST list all other skills/tools this skill depends on
- `category` MUST be one of: `core-workflow`, `domain-expert`, `meta-learning`, `token-optimization`

---

## 2. Identity (REQUIRED)

```markdown
# [Skill Name] Skill

## Identity

You are a **[ROLE]** specialist focused on **[DOMAIN/EXPERTISE]**.

**Your core responsibility:** [One-sentence mission statement].
**Your operating principle:** [One-sentence philosophy — how you approach work].
**Your quality bar:** [One-sentence standard — what "done" looks like for you].
```

**Rules:**
- MUST include ROLE, DOMAIN, MISSION, PRINCIPLE, and QUALITY BAR
- Must be written in second person ("You are...")
- Must distinguish from other similar skills (what makes THIS skill different)

---

## 3. When to Use (REQUIRED)

```markdown
## When to Use

- [Situation 1 with concrete example]
- [Situation 2 with concrete example]
- [Situation 3 with concrete example]
- [Situation 4+ as needed]

## When NOT to Use

- [Anti-situation 1 — when this skill would be wrong/overkill]
- [Anti-situation 2 — what OTHER skill should be used instead]
- [Anti-situation 3]
```

**Rules:**
- Minimum 3 "Use" situations, minimum 2 "NOT Use" situations
- Every "NOT Use" MUST redirect to the correct alternative skill
- Situations must be specific, not generic ("When adding OAuth to a Next.js app" not "When doing auth")

---

## 4. Core Principles (REQUIRED)

```markdown
## Core Principles (ALWAYS APPLY)

1. **[Principle Name]** — [What it means]. **[Enforcement]:** [What happens if violated].
2. **[Principle Name]** — [What it means]. **[Enforcement]:** [What happens if violated].
3. **[Principle Name]** — [What it means]. **[Enforcement]:** [What happens if violated].
...
```

**Rules:**
- Minimum 3 principles, maximum 7
- Each MUST have a name, explanation, AND enforcement mechanism
- Enforcement MUST describe the CONCRETE action taken when violated (not vague "be careful")
- Principles must be ordered by importance

---

## 5. Instructions / Workflow (REQUIRED)

```markdown
## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before starting work:
1. [Pre-check 1 — e.g., verify dependencies are available]
2. [Pre-check 2 — e.g., check for existing solutions via search-first]
3. [Pre-check 3 — e.g., assess scope and classify change risk]

### Step 1: [Phase Name]

**Goal:** [What this step accomplishes]
**Expected output:** [Concrete deliverable]
**Tools to use:** [Specific tool names]

[Detailed instructions — what to do, in what order, with what tools]

**Verification gate:** [How to confirm this step succeeded before moving on]

### Step 2: [Phase Name]

[Repeat structure for each step...]

### Step N: Handoff & Output

**Required output format:**
```
[Specific format for the skill's output — machine-readable when possible]
```
```

**Rules:**
- MUST start with Step 0: Pre-Flight (dependency check, scope assessment, search-first)
- Each step MUST have: Goal, Expected Output, Tools to Use, Verification Gate
- Minimum 2 steps, maximum 10 steps
- Last step MUST be a Handoff/Output section with a machine-readable format
- Steps that involve code MUST include concrete code snippets showing the pattern

---

## 6. Blocking Violations (REQUIRED)

```markdown
## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| [Specific forbidden action] | [What breaks] | [How to recover] |
| [Specific forbidden action] | [What breaks] | [How to recover] |
| [Specific forbidden action] | [What breaks] | [How to recover] |
```

**Rules:**
- Minimum 3 violations, maximum 10
- Each MUST have: Violation, Consequence, Recovery
- Violations must be SPECIFIC actions ("Using `as any` in TypeScript" not "Writing bad code")
- Recovery must be ACTIONABLE ("Run `git reset HEAD~1 --soft`" not "Fix it")

---

## 7. Verification (REQUIRED)

```markdown
## Verification

Before marking any task as complete:

### Self-Verification Checklist

- [ ] [Check 1 — e.g., Build passes with exit code 0]
- [ ] [Check 2 — e.g., All tests pass (0 failures)]
- [ ] [Check 3 — e.g., No new linter warnings]
- [ ] [Check 4 — e.g., De-Sloppify pass completed]
- [ ] [Check 5 — e.g., Security review completed (if applicable)]

### Verification Commands

```bash
# Run these commands to verify
[command 1]
[command 2]
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| [Gate name] | [Specific criteria] | [What to do if it fails] |
| [Gate name] | [Specific criteria] | [What to do if it fails] |
```

**Rules:**
- Minimum 4 self-verification checklist items
- Must include actual commands to run (not just "run tests")
- Quality Gates table with at least 2 gates
- Every gate must have a FAIL ACTION

---

## 8. Performance & Cost Considerations (REQUIRED for complex skills, OPTIONAL for simple)

```markdown
## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| [Simple task type] | [Model name] | [Token estimate] |
| [Standard task type] | [Model name] | [Token estimate] |
| [Complex task type] | [Model name] | [Token estimate] |

### Parallelization

- **[Task type]:** Can run N instances in parallel — [conditions]
- **[Task type]:** Must run sequentially — [reason]

### Context Budget

- **Expected context usage:** [estimate per task phase]
- **When to context-optimize:** [triggers]
- **Context recovery:** [what to do when context runs low]
```

---

## 9. Examples (REQUIRED)

```markdown
## Examples

### Example 1: [Scenario Name]

**User request:**
```
[Example user prompt]
```

**Skill execution:**
```
[What the skill does — step by step with expected outputs]
```

**Result:**
[What the user sees / gets]

### Example 2: [Scenario Name]

[Second example, different scenario]

### Example 3: [Edge Case]

[Example showing a tricky/edge case scenario]
```

**Rules:**
- Minimum 2 examples, recommended 3+
- At least 1 example MUST be an edge case / failure mode
- Examples MUST show actual user input → skill output flow
- Code in examples MUST be syntactically correct

---

## 10. Anti-Patterns (REQUIRED)

```markdown
## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| [Pattern name + example] | [Problem it causes] | [What to do instead] |
| [Pattern name + example] | [Problem it causes] | [What to do instead] |
```

**Rules:**
- Minimum 2 anti-patterns
- Each MUST show: the wrong way (concrete), why wrong, the right way (concrete)

---

## 11. References (REQUIRED)

```markdown
## References

### Internal Dependencies
- `[skill-name]` — [What it provides and how this skill uses it]
- `[shared-file]` — [What it contains]

### External Standards
- [Standard/Spec name] — [URL or citation]
- [Best practice guide] — [URL or citation]

### Related Skills
- `[related-skill]` — [How it relates: precedes / follows / alternatives]
```

**Rules:**
- MUST list all internal dependencies with role descriptions
- MUST cite at least 1 external standard or best practice
- MUST list related skills with relationship type

---

## 12. Changelog [OPTIONAL but recommended]

```markdown
## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | YYYY-MM-DD | [Major changes] |
| 1.0.0 | YYYY-MM-DD | Initial version |
```

---

## Quality Scorecard

Every skill is scored on completion against these dimensions:

| Dimension | Weight | Criteria |
|---|---|---|
| **Structure** | 20% | All 12 sections present, correctly ordered |
| **Clarity** | 20% | Instructions unambiguous, concrete examples |
| **Power** | 25% | Covers edge cases, failure modes, verification |
| **Actionability** | 20% | Every statement leads to concrete action |
| **Maintainability** | 15% | Versioned, has references, clear dependencies |

**Minimum passing score: 8/10 on each dimension, 8.5/10 overall.**

---

## Skill Size Guidelines

| Skill Type | Target Lines | Sections |
|---|---|---|
| Meta/Orchestrator | 400-600 | All 12 full |
| Domain Expert (complex) | 300-500 | All 12 (9 may be condensed) |
| Domain Expert (simple) | 200-350 | 1-8 + 11 (minimal 9, 10) |
| Utility/Helper | 150-250 | 1-7 + 11 (skip 8, 9, 10 if not applicable) |

---

## Anti-Pattern: What NOT to Do

```markdown
❌ VAGUE DESCRIPTION: "Helps with development tasks"
✅ SPECIFIC: "Runs structured 6-phase verification producing READY/NOT READY verdict"

❌ NO ENFORCEMENT: "Be careful with security"
✅ ENFORCED: "If auth code is committed without review, revert and run security-reviewer"

❌ SINGLE TRIGGER: triggers: ["/review"]
✅ RICH TRIGGERS: triggers: ["/review", "code review", "review this", "PR review", "check my code"]

❌ NO FAILURE MODE: "Do step 1, then step 2"
✅ FAILURE HANDLING: "Step 1 → if fails, check X. If still fails after 2 retries, escalate to Oracle"

❌ GENERIC HANDOFF: "Report what you did"
✅ MACHINE-READABLE: "Output: ## Handoff\n```yaml\nstatus: pass|fail\nfindings:\n  - file: path\n    issue: desc\n```"
```
