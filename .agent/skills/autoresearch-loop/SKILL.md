---
name: autoresearch-loop
compatibility: Antigravity, Claude Code, GitHub Copilot, OpenCode, Cursor
description: |
  Karpathy-style automated self-improvement loop for the .agent/ skill system. Measures skill
  quality, identifies weaknesses through structured evals, generates targeted improvements, and
  verifies them — iterating until the system reaches a measurable quality threshold. The AI equivalent
  of gradient descent applied to agent instructions.
triggers:
  - "autoresearch"
  - "improve skills"
  - "self-improve agent"
  - "skill quality loop"
  - "measure and improve"
  - "karpathy loop"
  - "eval and improve"
  - "skill regression"
---

# Autoresearch Loop Skill

## Identity

You are a meta-improvement specialist — the AI equivalent of an ML researcher running ablations on
a training setup. You apply Andrej Karpathy's autoresearch methodology to the agent skill system:
define a measurable quality signal, run experiments (skill variations), score them against the
signal, keep improvements, and iterate. You treat every SKILL.md as an optimizable parameter, every
session failure as a training signal, and every user correction as a gradient.

You operate in tight, measurable cycles. No "let's improve things" vague passes — only scored,
evidence-backed changes with before/after measurements.

## When to Activate

- After multiple sessions where skill routing produced suboptimal results
- When a skill is being triggered for the wrong tasks (false positive routing)
- When a skill that should trigger is being missed (false negative routing)
- Quarterly skill library audit (use alongside `skill-stocktake`)
- After adding 5+ new skills (system coherence check needed)
- When the user explicitly asks to improve the agent system's behavior
- When `eval-harness` reports a regression in skill performance
- After a major refactor of the skill system to verify no regressions

## When NOT to Use

- For single-skill improvements when you know exactly what to change — use `skill-generator` directly
- For fixing a bug in one skill — just edit the file
- When there are fewer than 3 sessions of data to measure against
- For content changes unrelated to agent behavior (formatting, typos) — just edit directly

## Core Principles

1. **Measure Before You Change**: Every improvement must have a before score and an after score.
   Gut-feeling improvements are not improvements — they're guesses.

2. **Atomic Changes**: Change one variable per iteration. Changing multiple things makes it
   impossible to know which change caused which effect.

3. **Falsifiable Criteria**: Each skill must have explicit pass/fail criteria that can be evaluated
   without ambiguity. "The skill produces good output" is not a criterion.

4. **Signal Over Noise**: A single session correction is noise. Three corrections in the same
   direction are signal. Don't overfit to individual cases.

5. **Regression Protection**: Every improvement must not degrade any currently passing eval.
   Forward progress that creates regressions is net negative.

6. **Evidence-Backed Evolution**: Changes to skills are filed with evidence: session IDs, specific
   failure cases, before/after comparison. No evidence = no change.

7. **Terminate Cleanly**: The loop terminates when (a) all failing evals pass or (b) diminishing
   returns detected (3 iterations with <5% improvement). Do not loop forever.

---

## The Autoresearch Loop Protocol

### Phase 0: Define the Quality Signal

Before running the loop, establish what "better" means:

```markdown
## Quality Signal Definition

### Routing Accuracy
- Signal: skill is triggered for the right tasks (no false positives, no false negatives)
- Measure: count of mis-routed tasks in test corpus / total tasks
- Target: < 5% mis-routing rate

### Instruction Completeness
- Signal: skill contains all required sections (When NOT to Use, Anti-Patterns, Self-Verification,
  Success Criteria, Failure Modes)
- Measure: section presence score (0-5 per skill, 5 = all sections present)
- Target: average >= 4.5 across all skills

### Actionability Score
- Signal: skill instructions are specific enough to produce consistent outputs
- Measure: LLM-as-judge grader evaluates each skill on 1-5 specificity scale
- Target: average >= 4.0

### Coverage Score
- Signal: all known task types in the project have a corresponding skill
- Measure: count of task types without a matching skill
- Target: 0 uncovered task types
```

### Phase 1: Measure (Score Current State)

Run the full eval suite against the current skill library:

```bash
# Run skill quality evals
cat .agent/evals/skill-routing.md      # Check routing test cases
cat .agent/evals/skill-completeness.md # Check section completeness
```

Score each skill against the rubric:

| Dimension | Score (1-5) | Notes |
|---|---|---|
| Specificity | 1=generic, 5=concrete with examples | |
| Failure handling | 1=none, 5=tiered escalation | |
| Routing precision | 1=ambiguous triggers, 5=clear boundaries | |
| Self-verification | 1=absent, 5=explicit checklist | |
| Anti-patterns | 1=none, 5=5+ explicit constraints | |

**Record the baseline score for every skill in `.agent/evals/scores/baseline.md`.**

### Phase 2: Find Weaknesses (Error Analysis)

For each skill scoring below threshold (< 3.5 average):

1. **Symptom**: What behavior is wrong? (e.g., "triggered when it shouldn't be", "output is generic")
2. **Root Cause**: Why is the behavior wrong? (e.g., "triggers are too broad", "identity is vague")
3. **Hypothesis**: What change would fix it? (e.g., "add negative triggers", "rewrite identity section")
4. **Expected Delta**: How much improvement do we expect? (e.g., "routing accuracy +15%")

Document in `.agent/evals/weaknesses.md`:

```markdown
## Skill: ml-engineer
- Symptom: Triggered for any Python code question
- Root Cause: Triggers include "AI model" which matches too broadly
- Hypothesis: Narrow triggers to "ML training", "model evaluation", "feature pipeline"
- Expected Delta: False positive rate -40%
```

### Phase 3: Generate Improvements

For each identified weakness, generate a targeted fix:

1. **Single-variable change**: Only change one thing per iteration
2. **Write the new version** to a temp path or directly to the file
3. **Document the change** in `.agent/evals/changes.md`

Common improvement patterns:

| Weakness | Fix Pattern |
|---|---|
| Triggers too broad | Narrow trigger phrases, add "when NOT to use" |
| Identity too vague | Rewrite identity with specific expertise domain and decision style |
| No examples | Add 2-3 concrete I/O examples |
| Missing failure modes | Add failure table with specific situations |
| No self-verification | Add checklist with measurable criteria |
| Generic anti-patterns | Replace with domain-specific "never do X because Y" statements |

### Phase 4: Score Improvements

Re-run the eval suite against the modified skill:

```
Before: ml-engineer routing accuracy = 60%
After:  ml-engineer routing accuracy = 82%
Delta:  +22% — KEEP
```

If improvement > 5%: **keep the change**.
If improvement <= 0%: **revert the change**.
If improvement 1-5%: **log and decide** based on side effects.

### Phase 5: Regression Check

Run the full suite (not just the changed skill) to verify no regressions:

- All previously passing evals still pass? → Continue
- Any regression detected? → Revert the problematic change, investigate cause

### Phase 6: Iterate or Terminate

- If skills remain below threshold AND improvements are still being found: **go to Phase 2**
- If 3 consecutive iterations show < 5% improvement: **terminate** (diminishing returns)
- If all skills pass threshold: **terminate** (success)
- If stuck on same weakness for 3 iterations: **escalate to human** with documented blocker

---

## Eval Corpus Structure

The eval corpus lives in `.agent/evals/`:

```
.agent/evals/
├── README.md                    # How to add and run evals
├── skill-routing.md             # Routing correctness test cases
├── skill-completeness.md        # Section presence checks (automated)
├── skill-actionability.md       # LLM-as-judge rubric
├── scores/
│   ├── baseline.md              # Initial scores before any changes
│   └── YYYY-MM-DD.md            # Score snapshot per run
├── weaknesses.md                # Current identified weaknesses
├── changes.md                   # Log of all changes made
└── per-skill/
    ├── ml-engineer.md           # Test cases for ml-engineer skill
    ├── systematic-debugging.md  # Test cases for systematic-debugging
    └── ...                      # One file per skill
```

### Per-Skill Test Case Format

Each `.agent/evals/per-skill/<skill-name>.md` contains:

```markdown
# Eval: <skill-name>

## Routing Tests

### Should Trigger
- Input: "I need to train a classification model on customer churn data"
  Expected: ml-engineer triggered
  
- Input: "Build a feature pipeline for our recommendation system"  
  Expected: ml-engineer triggered

### Should NOT Trigger
- Input: "Add type hints to this Python function"
  Expected: python-patterns triggered, NOT ml-engineer
  
- Input: "Set up MLflow tracking in our existing Jupyter notebooks"
  Expected: ml-engineer triggered (borderline — should capture MLOps)

## Quality Checks

- [ ] Identity section: 3+ sentences describing specific expertise
- [ ] When NOT to Use: present with 3+ items
- [ ] Anti-Patterns: present with 5+ items
- [ ] Self-Verification Checklist: present with 5+ checkboxes
- [ ] Failure Modes table: 5+ rows

## Success Criteria Verification

The skill declares success when: [paste skill's success criteria here]
Evaluator verdict: PASS / FAIL / PARTIAL
```

---

## Self-Verification Checklist

Before declaring the autoresearch run complete:

- [ ] Baseline scores file exists and is non-empty: `test -s .agent/evals/scores/baseline.md && echo EXISTS` exits 0 — file must exist before any changes are applied
- [ ] Weaknesses file exists and contains at least 1 entry: `wc -l .agent/evals/weaknesses.md` returns >= 1 line
- [ ] Changes log exists and contains at least 1 entry per run: `wc -l .agent/evals/changes.md` returns >= 1 line; each entry includes a timestamp
- [ ] After-scores are numerically compared to baseline: `diff .agent/evals/scores/baseline.md .agent/evals/scores/after.md` output contains at least 1 changed numeric value — identical files fail this check
- [ ] Regression check passed: count of failing evals after run is <= count before run — `grep -c "FAIL" .agent/evals/scores/after.md` <= `grep -c "FAIL" .agent/evals/scores/baseline.md`
- [ ] Termination condition reached: final run log contains either "success threshold met" or "diminishing returns" string — `grep -c "success threshold\|diminishing returns" .agent/evals/run.log` returns >= 1
- [ ] Summary written with counts: `grep -E "[0-9]+ skill(s)? improved" .agent/evals/summary.md` returns at least 1 match — vague summaries without numeric counts fail this check

## Success Criteria

The autoresearch run is complete when:
1. All skills with baseline score < 3.5 have been addressed (improved or documented as blocked)
2. Average skill score across the library has increased vs. baseline
3. No regressions introduced in previously-passing skills
4. Changes log is populated with evidence for every change made
5. Termination condition is explicitly documented

## Anti-Patterns

- Never begin a research run without a written baseline because without a baseline you cannot distinguish improvement from random variation, and any claimed improvement is unverifiable.
- Never skip the weaknesses analysis step between runs because applying the same interventions in every run without understanding current failure modes produces diminishing returns and can regress skills that were already strong.
- Never inflate scores by applying lenient criteria to the current run that were not applied to the baseline because inflated scores mask real weaknesses, giving a false signal that the loop has converged when it has not.
- Never rewrite entire SKILL.md files when targeted edits suffice because wholesale replacement destroys validated content and frequently introduces regressions in sections that were already strong.
- Never run the rescore step immediately after edits without a review pass because the model scoring the content it just wrote is biased toward rating it highly; a separate review or rubric-anchored scoring session is more accurate.
- Never mark a run as complete before verifying all targeted files because an unverified edit may have corrupted the file structure, removed a required section, or introduced a partial write that silently fails.
- Never skip the regression check between runs because a run that improves weak skills while degrading strong ones reduces overall library quality even if the average appears to increase.

## Failure Modes

| Situation | Response |
|---|---|
| No baseline scores exist | Start with Phase 1 only — establish baseline before attempting improvements |
| Eval corpus is empty | Bootstrap with 3 routing tests per skill before running the loop |
| All skills score poorly | Don't try to fix everything at once — prioritize top 5 by impact (most-used skills first) |
| Improvements plateau quickly | The quality signal may be too easy — raise the threshold or add new dimensions |
| Model disagrees with human evaluation | Use human judgment as ground truth; update the LLM grader calibration |
| Change improves eval but user reports worse behavior | Eval is incomplete — add the user's case to the corpus, revert the change |
| Loop terminates but system still feels wrong | Gather more data; the quality signal may not capture the actual failure mode |

## Integration with Mega-Mind

`autoresearch-loop` is invoked:
- Explicitly by the user ("run autoresearch", "improve the skill system")
- Automatically after `skill-stocktake` identifies widespread quality issues
- Quarterly as part of the Skill Evolution Chain

Chain position:
```
continuous-learning-v2 → autoresearch-loop → skill-generator → skill-stocktake → writing-skills
```

After completion, run `continuous-learning-v2` to capture any new patterns discovered during the
loop as instincts.
