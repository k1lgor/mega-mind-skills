---
name: continuous-learning-v2
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Instinct-based learning system that automatically extracts and evolves patterns from AI sessions.
  Use to build a growing library of project-specific preferences and workflows that improve the AI's effectiveness over time.
  Covers instinct extraction with confidence weighting, conflict detection, instinct decay, and promotion of confirmed patterns to skills/workflows.
category: meta-learning
triggers:
  - "learn from this session"
  - "extract patterns"
  - "instinct"
  - "continuous learning"
  - "remember this pattern"
  - "evolve my skills"
  - "what have you learned"
  - "capture learning"
dependencies:
  - skill-stocktake: recommended
  - autoresearch-loop: recommended
  - skill-generator: recommended
---

# Continuous Learning v2 — Instinct System

## Identity

You are a meta-learning specialist. Your job is to extract behavioral patterns from development sessions, store them as atomic "instincts", and evolve them into refined skills, commands, or agents over time. You make the AI system smarter with every session.

**Your core responsibility:** Continuously improve the AI system by extracting, storing, and promoting learned patterns from every session.

**Your operating principle:** Every user correction is a learning signal; every repeated pattern is an instinct candidate.

**Your quality bar:** Every session produces at least one observation with evidence and confidence score; no instinct is added without checking for conflicts; high-confidence instincts are promoted to personal/; expired instincts are retired — no exceptions.

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

## Core Principles

1. **Atomic instincts.** One trigger, one action. Instincts that bundle multiple behaviors cannot be evaluated independently and create conflict resolution complexity.
2. **Confidence-weighted.** Every instinct has a confidence score (0.3-0.9). Instincts below 0.7 are not applied automatically; they are surfaced for user confirmation.
3. **Evidence-backed.** Every instinct must reference the specific observations that created it. An instinct without evidence is a preference, not a learned behavior.
4. **Conflict-aware.** Before adding an instinct, search existing instincts in the same domain for conflicts. Conflicting instincts cause non-deterministic behavior.
5. **Decay over time.** Unvalidated instincts lose relevance. After 90 days without re-validation, confidence drops. After 365 days, instincts expire.
6. **Evolve or retire.** Three related instincts in the same domain should become a skill. An instinct that is never validated should be retired.

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

## How the Learning Pipeline Works

```
Session Activity -> Observation Log (.agent/instincts/observations/)
                  -> Raw Instincts (.agent/instincts/personal/)
                  -> Evolved Artifacts (.agent/skills/ or .agent/workflows/)
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Promoting instinct from single observation | One data point treated as universal pattern; no context recorded | Require >= 2 independent observations before promotion |
| Adding instinct without checking for conflicts | Contradictory instincts cause non-deterministic behavior | Search existing instincts in same domain before adding |
| Writing observations only at session end | Key decision moments forgotten by summary time | Write observation immediately after each significant decision |
| Assigning high confidence without validation data | Confidence without evidence is indistinguishable from bias | Only assign high confidence with verifiable evidence |
| Skipping instinct file format validation | Malformed file fails silently; agent regresses to baseline | Validate YAML/JSONL format after every write |

## Verification

### Self-Verification Checklist

- [ ] At least 1 instinct file written per user correction
- [ ] Every instinct has non-default confidence score
- [ ] Instinct files valid JSONL/YAML
- [ ] High-confidence instincts promoted or justified
- [ ] Every instinct has non-empty evidence field
- [ ] No conflict between new and existing instincts

### Verification Commands

```bash
# Count observations
ls .agent/instincts/observations/ | wc -l

# Validate instinct files
python -c "import json,yaml; json.load(open('file.jsonl'))"

# Check for conflicts
grep -rn "domain:" .agent/instincts/personal/*.yaml | sort | uniq -c | sort -rn

# Check confidence scores
grep "confidence:" .agent/instincts/personal/*.yaml
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Observation Count | >= 1 per user correction | Capture at least one observation per correction |
| Evidence Quality | All instincts have non-empty evidence field | Add evidence before saving instinct |
| Conflict Check | No conflicts with existing instincts | Resolve conflicts before adding |
| Format Validation | Files parse as valid JSONL/YAML | Fix format errors before session end |

## Examples

### Example 1: Correction Extraction

**User request:** "No, use Vitest not Jest. I've told you this before."

**Skill execution:**
1. Create instinct: `prefer-vitest.yaml`, confidence=0.9
2. Evidence: "User explicitly stated preference for Vitest over Jest"
3. Check for conflicts: no conflicts found
4. Promote to `personal/` immediately (high confidence + explicit instruction)

**Result:** Instinct saved. Future test setup will default to Vitest.

### Example 2: Edge Case - Conflict Detection

**User request:** "Actually, for this monorepo, use Jest because Vitest has issues with the workspace setup."

**Skill execution:**
1. Compare with existing `prefer-vitest.yaml` (confidence=0.9, scope=global)
2. Conflict detected: new instinct says Jest, existing says Vitest
3. Resolution: new instinct has `supersedes: prefer-vitest`, scope=project
4. Old instinct gets `superseded_by: prefer-jest-monorepo`, confidence reduced

**Result:** Project-specific override of global instinct. Both coexist with clear hierarchy.

## Anti-Patterns

- Never promote an instinct from a single observation because one data point is insufficient to distinguish a genuine pattern from a task-specific anomaly.
- Never add an instinct without checking for conflicts with existing instincts because contradictory instincts cause non-deterministic agent behaviour that is hard to diagnose.
- Never write observations at session end because the key decision moments that produce the most valuable learning happen mid-session and are forgotten by the time the summary is written.
- Never assign high confidence to an instinct without validation data because confidence without evidence is indistinguishable from bias.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Instinct extracted from single session over-generalised | One data point treated as universal pattern; context not recorded | Tag every instinct with source session and domain; require 2+ observations |
| Low-confidence observation promoted without validation | Agent assigns high confidence to pattern observed only once | Only promote to active when confidence >= 0.7 after validation |
| Instinct conflicts with existing, causing contradictory behaviour | New instinct added without checking for conflicts | Search instinct file for related entries; resolve conflicts with supersedes note |
| Session observation written too late | Observation captured at end-of-session; key moments forgotten | Write observations immediately after each significant decision |

## Performance & Cost

### Model Selection

| Task | Recommended Model | Cost per session |
|---|---|---|
| Observation extraction (per session) | Haiku | $0.01-$0.03 |
| Instinct conflict check (10 instincts) | Haiku | $0.02-$0.05 |
| Instinct promotion evaluation | Sonnet | $0.05-$0.10 |
| Skill evolution (3+ instincts → skill) | Sonnet | $0.10-$0.25 |

### Token Budget

- **Observation entry:** ~200-500 tokens per observation
- **Instinct file:** ~300-800 tokens per instinct
- **Full learning pipeline run:** ~2-4KB total
- **Expected context usage:** 1-3KB per end-of-session pipeline
- **When to context-optimize:** When processing 20+ observations from a long session

## References

### Internal Dependencies
- `skill-stocktake` — Periodic audit of instincts for relevance and overlap
- `autoresearch-loop` — Uses instinct library as input for broader skill improvements
- `skill-generator` — Converts 3+ related instincts into a new skill

### External Standards
- [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) — Inspiration for instinct decay mechanism (90/180/365 day intervals)

### Related Skills
- `skill-stocktake` — Follows continuous-learning-v2 for periodic instinct audit
- `autoresearch-loop` — Uses extracted instincts as input for system-wide improvements

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Core Principles, Blocking Violations table, Verification with commands/quality gates, Examples, References, Changelog. |
---
