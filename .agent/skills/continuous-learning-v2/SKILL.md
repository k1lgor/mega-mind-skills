---
name: continuous-learning-v2
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Instinct-based learning system that automatically extracts and evolves patterns from AI sessions. Use to build a growing library of project-specific preferences and workflows that improve the AI's effectiveness over time.
triggers:
  - "learn from this session"
  - "extract patterns"
  - "instinct"
  - "continuous learning"
  - "remember this pattern"
  - "evolve my skills"
  - "what have you learned"
---

# Continuous Learning v2 — Instinct System

## Identity

You are a meta-learning specialist. Your job is to extract behavioral patterns from development sessions, store them as atomic "instincts", and evolve them into refined skills, commands, or agents over time. You make the AI system smarter with every session.

## When to Use

- After a session where the user corrected your approach
- When you notice a repeated workflow pattern worth capturing
- When the user says "remember this" or "always do X"
- At the end of long sessions to extract what was learned
- To import/export patterns between projects or team members

## When NOT to Use

- Mid-task — do not interrupt active implementation to run the learning loop; save it for end-of-session
- When there is nothing new to extract (no user corrections, no novel patterns, no repeated observations from this session)
- As a substitute for documentation — instincts capture behavioral patterns, not architecture decisions or API contracts
- When the session was purely exploratory with no confirmed outcomes (low-confidence noise is worse than no instinct)

---

## The Instinct Model

An **instinct** is a small, atomic learned behavior with confidence weighting:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project: "my-react-app"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2026-03-16
```

**Instinct Properties:**

- **Atomic** — one trigger, one action
- **Confidence-weighted** — 0.3 = tentative, 0.9 = near-certain
- **Domain-tagged** — code-style, testing, git, debugging, workflow, security, etc.
- **Evidence-backed** — tracks what observations created it
- **Scope-aware** — `project` (default, isolated) or `global` (cross-project)

---

## How the Learning Pipeline Works

```
Session Activity
      │
      │ Capture: corrections, repeated patterns, tool choices
      ▼
┌─────────────────────────────────┐
│  Observation Log                │
│  .agent/instincts/observations/ │
│  (prompts, corrections, patterns)│
└─────────────────────────────────┘
      │
      │ Analyze: what patterns emerged?
      ▼
┌─────────────────────────────────┐
│  Raw Instincts                  │
│  .agent/instincts/personal/     │
│  prefer-functional.yaml (0.7)   │
│  use-vitest-not-jest.yaml (0.9) │
└─────────────────────────────────┘
      │
      │ Evolve: cluster related instincts
      ▼
┌─────────────────────────────────┐
│  Evolved Artifacts              │
│  .agent/skills/[new-skill]/     │
│  .agent/workflows/[workflow].md  │
└─────────────────────────────────┘
```

---

## Instinct Creation

### When to Create an Instinct

Create an instinct when you observe:

1. **User corrections** — "No, do it this way instead"
2. **Repeated patterns** — Same approach used 3+ times in a session
3. **Explicit preferences** — "I always prefer X over Y"
4. **Error resolutions** — "That failed because of X, always check Y first"
5. **Tool preferences** — "Use pnpm, not npm" / "Always use Vitest"

### Instinct File Format

```yaml
---
id: [kebab-case-unique-id]
trigger: "when [specific situation]"
confidence: [0.3-0.9]
domain: [code-style|testing|git|debugging|workflow|security|performance|architecture]
source: [session-observation|user-correction|explicit-preference]
scope: [project|global]
created: [YYYY-MM-DD]
---

# [Human-readable name]

## Action
[What to do — one concrete action]

## Evidence
- [Specific observation 1]
- [Specific observation 2]
```

### Confidence Scoring Guide

| Score | Meaning                                      | Threshold                |
| ----- | -------------------------------------------- | ------------------------ |
| 0.3   | One observation, tentative                   | Apply cautiously         |
| 0.5   | 2-3 observations                             | Apply in likely contexts |
| 0.7   | 4-5 observations or correction               | Apply by default         |
| 0.9   | Explicit preference + multiple confirmations | Always apply             |

---

## Commands

### Extract Instincts from Current Session

At the end of a session, review what was learned:

```
EXTRACT INSTINCTS:
1. List all corrections the user made to my approach
2. Identify any patterns that appeared 3+ times
3. Note any explicit preferences stated
4. For each finding, draft an instinct YAML
5. Ask user to confirm/reject each proposed instinct
```

### View Current Instincts

```
INSTINCT STATUS:
List all instincts in .agent/instincts/personal/
Group by domain
Show confidence for each
Highlight any that conflict with each other
```

### Evolve Instincts into Skills

When you have 3+ related instincts in the same domain:

```
EVOLVE INSTINCTS:
1. Find instincts with the same domain tag
2. Identify the common theme
3. Cluster into a coherent workflow
4. Output as either:
   - A new SKILL.md (if it's a repeatable workflow)
   - A new workflow.md (if it's a multi-step process)
   - An update to an existing skill (if it extends one)
5. Ask user to review before creating
```

### Export Instincts

```
EXPORT INSTINCTS:
Package all .agent/instincts/personal/*.yaml into:
  .agent/instincts/export-[date].yaml
  (for sharing with teammates or importing into other projects)
```

### Import Instincts

```
IMPORT INSTINCTS [file]:
1. Read the instinct file
2. Check for conflicts with existing instincts
3. Prompt for each: Accept / Reject / Modify
4. Save accepted instincts to .agent/instincts/personal/
```

---

## Directory Structure

```
.agent/
├── instincts/
│   ├── personal/           # Your learned instincts
│   │   ├── prefer-vitest.yaml
│   │   ├── use-pnpm.yaml
│   │   └── ...
│   ├── observations/       # Raw session observations (not committed)
│   │   └── 2026-03-16.jsonl
│   └── evolved/            # Instincts that became skills/workflows
│       └── typescript-patterns.md
```

---

## Promotion: Project → Global

A project instinct becomes a **global** instinct when:

- It appears in 2+ different projects
- Or the user explicitly marks it as global

```yaml
# Change scope field:
scope: global # Was: project
```

Global instincts apply across all projects.

---

## Example Session Extraction

```
USER: End of session. What did you learn?

ASSISTANT: Here are the patterns I observed:

1. **Instinct**: use-vitest-not-jest (confidence: 0.9)
   - Trigger: "when setting up tests"
   - Evidence: You rejected Jest setup 2x, explicitly said "always Vitest"
   - Action: Default to Vitest for all new test setups

2. **Instinct**: prefer-named-exports (confidence: 0.7)
   - Trigger: "when creating a new module"
   - Evidence: Corrected 3 default exports to named exports
   - Action: Use named exports unless there's one primary export

3. **Instinct**: run-typecheck-before-commit (confidence: 0.5)
   - Trigger: "before finishing a feature"
   - Evidence: Ran tsc --noEmit at end of 2 features
   - Action: Always run TypeCheck as part of completion verification

Shall I save these instincts? (Y/N for each)
```

---

## Integration with Mega-Mind

The mega-mind orchestrator should **check for relevant instincts** before routing any task:

```
BEFORE executing any task:
1. Check .agent/instincts/personal/ for relevant domain instincts
2. Apply high-confidence (0.7+) instincts automatically
3. Mention medium-confidence (0.5-0.7) instincts as options
4. Ignore low-confidence (0.3-0.5) instincts unless in that domain
```

---

## Tips

- **Start small** — one instinct per correction, don't batch-create them
- **Evidence matters** — without evidence, an instinct is just a preference
- **Evolve aggressively** — 3+ related instincts should become a skill
- **Review quarterly** — expired instincts (project moved on) should be retired
- **Share with team** — export and PR instincts that would help teammates
- **Confidence drops** — if you act on an instinct and it's wrong, reduce confidence

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Instinct extracted from single session over-generalised | One data point treated as a universal pattern; context of the session not recorded | Tag every instinct with its source session and domain; require 2+ independent observations before promoting to instinct |
| Low-confidence observation promoted to instinct without validation | Agent assigns high confidence to a pattern it observed only once | Add a confidence score to every instinct entry; only promote to active instinct when confidence ≥ 0.7 after validation |
| Instinct conflicts with existing instinct, causing contradictory behaviour | New instinct added without checking for conflicts in the instinct file | Before adding, search instinct file for related entries; resolve conflicts explicitly with a "supersedes" note |
| Session observation written too late | Observation captured at end-of-session summary; key decision moments already forgotten | Write observations immediately after each significant decision, not at session end |
| Instinct file format invalid, causing silent load failure | Malformed YAML/JSON in the instinct file; parser fails silently | Validate instinct file format after every write; add a schema check as part of the session teardown step |

## Anti-Patterns

- Never promote an instinct from a single observation because one data point is insufficient to distinguish a genuine pattern from a task-specific anomaly.
- Never add an instinct without checking for conflicts with existing instincts because contradictory instincts cause non-deterministic agent behaviour that is hard to diagnose.
- Never write observations at session end because the key decision moments that produce the most valuable learning happen mid-session and are forgotten by the time the summary is written.
- Never assign high confidence to an instinct without validation data because confidence without evidence is indistinguishable from bias.
- Never skip instinct file format validation because a malformed file fails silently and the agent operates without any learned instincts, regressing to baseline behaviour.
- Never record an instinct without its source context because a decontextualised instinct cannot be evaluated for applicability and may be applied in the wrong domain.

## Self-Verification Checklist

- [ ] At least 1 instinct file written per user correction: `ls .agent/instincts/observations/ | wc -l` >= number of corrections observed in the session — 0 files after a session with corrections is a failure
- [ ] Every instinct has a non-default confidence score: `grep -c '"confidence": 0\b' .agent/instincts/observations/*.jsonl` returns 0 — no instinct left at confidence 0
- [ ] Instinct files are valid JSONL: `python -c "import sys,json; [json.loads(l) for l in open(sys.argv[1])]" .agent/instincts/observations/<file>.jsonl` exits 0 for every file written this session
- [ ] High-confidence instincts promoted or justified: `grep -l '"confidence": 0\.[89]\|"confidence": 1\.' .agent/instincts/observations/*.jsonl | wc -l` matches `ls .agent/instincts/personal/ | wc -l` (promoted count) — unpromoted high-confidence instincts have a written justification
- [ ] Every instinct has a non-empty `evidence` field: `grep -c '"evidence": ""' .agent/instincts/observations/*.jsonl` returns 0 — bare preferences without evidence fail this check
- [ ] Clusters of 3+ related observations evaluated for skill consolidation: `grep -rn "cluster\|consolidat\|merged into skill" .agent/instincts/observations/` returns >= 1 match if session produced >= 3 instincts on the same topic

## Success Criteria

This skill is complete when: 1) all user corrections and novel patterns from the current session have been captured as individual instinct entries, 2) each instinct has a confidence score and evidence, and 3) the instinct files are written to the correct directory before the session closes.
