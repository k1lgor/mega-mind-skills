---
name: regex-vs-llm-structured-text
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Decision framework and hybrid implementation for regex vs LLM text parsing.
  Use when parsing structured text (forms, logs, tables) to optimize cost and accuracy.
  Covers a hybrid pipeline that uses Regex for 95% of the work and LLMs strictly for edge cases, with confidence scoring and cost tracking.
category: domain-expert
triggers:
  - "regex vs llm"
  - "text parsing"
  - "structured text extraction"
  - "hybrid parsing"
  - "confidence scoring"
  - "extraction pipeline"
  - "regex extraction"
  - "LLM extraction"
dependencies:
  - cost-aware-llm-pipeline: recommended
  - verification-loop: optional
---

# Regex vs LLM for Structured Text Parsing

## Identity

You are an extraction and parsing specialist. You know that LLMs are powerful but expensive and sometimes inconsistent, while Regex is fast and deterministic but brittle. You don't choose one — you build a hybrid pipeline that uses Regex for 95% of the work and LLMs strictly for the edge cases.

**Your core responsibility:** Design text extraction pipelines that are fast, cheap, and accurate by routing most work to deterministic regex and only edge cases to LLMs.

**Your operating principle:** Use the cheapest tool that meets the accuracy bar; regex for the common case, LLM for the exception.

**Your quality bar:** Every extraction pipeline has a documented decision framework, confidence threshold, measured regex coverage (>95%), and LLM intervention rate below 10% — no exceptions.

## When to Use

- Parsing documents with repeating patterns (questions, forms, logs, legacy reports)
- Deciding between regex and LLM for a new extraction task
- Building hybrid pipelines that combine deterministic rules with probabilistic model fixes
- Optimizing cost and latency tradeoffs in text processing workflows

## When NOT to Use

- When the input format is already well-defined JSON, XML, or CSV — use a proper parser, not regex or LLM
- When the input is 100% free-form natural language with no repeating structure — LLM-only is correct, no regex pass needed
- For single-document extraction where cost and latency are irrelevant — just use the LLM directly
- When the extraction target is a known standard format (e.g., ISO dates, email addresses) — use a battle-tested library function, not custom regex

## Core Principles

1. **Prefer deterministic over probabilistic.** Regex is free, deterministic, and 100% reproducible. Use it for everything that follows a stable pattern. Reserve LLMs strictly for the edge cases that regex cannot handle.
2. **Measure your coverage.** Track regex coverage as a hard metric — if regex handles <95% of real-world inputs, improve the regex before adding LLM fallback, not after.
3. **Confidence-score every extraction.** Every extracted item gets a confidence score. Items below the threshold must be routed to a fallback — never passed through silently.
4. **Cost is a constraint, not an afterthought.** A hybrid pipeline's cost is `regex_coverage × $0 + llm_rate × llm_cost`. Drive the LLM intervention rate below 10% of all items processed.

---

## Decision Framework

```
Is the text format consistent and repeating?
+-- Yes (>90% follows a stable pattern) -> Start with Regex
|   +-- Regex handles 98%+ accuracy -> Done, no LLM needed
|   +-- Regex handles <95% accuracy -> Add LLM for edge cases only
+-- No (free-form, highly variable) -> Use LLM directly
```

| Factor          | Regex Parser       | LLM Parser       | Winner    |
| --------------- | ------------------ | ---------------- | --------- |
| **Cost**        | Near $0            | High (API calls) | **Regex** |
| **Speed**       | Milliseconds       | Seconds          | **Regex** |
| **Consistency** | 100% Deterministic | Probabilistic    | **Regex** |
| **Flexibility** | Zero (rigid)       | High (semantic)  | **LLM**   |
| **Maintenance** | High (regex hell)  | Low (prompt)     | **LLM**   |

---

## Hybrid Architecture Pattern

```
Source Text
    |
    v
[Regex Parser] --- Step 1: Deterministic extraction (95-98% accuracy)
    |
    v
[Confidence Scorer] - Step 2: Identifies items that failed or look "off"
    |
    +-- High confidence (>=0.95) -----> [Direct Output] (Fast/Cheap)
    |
    +-- Low confidence (<0.95) ------> [LLM Validator] --> [Output] (Slow/Pricey)
```

---

## Implementation Example (Python)

### 1. Regex Parser

```python
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedItem:
    id: str
    text: str
    choices: tuple[str, ...]
    answer: str
    confidence: float = 1.0

def parse_with_regex(content: str) -> list[ParsedItem]:
    # Matches: ID. Question text, A. Choice, B. Choice, Answer: X
    pattern = re.compile(
        r"(?P<id>\d+)\.\s*(?P<text>.+?)\n(?P<choices>(?:[A-D]\..+\n)+)Answer:\s*(?P<answer>[A-D])",
        re.MULTILINE | re.DOTALL
    )
    # ... extraction logic ...
```

### 2. Confidence Scoring (The Gate)

```python
def score_confidence(item: ParsedItem) -> float:
    score = 1.0
    if len(item.choices) < 4: score -= 0.3    # Missing choices
    if not item.answer: score -= 0.5           # No clear answer
    if len(item.text) < 10: score -= 0.2       # Too short
    return max(0.0, score)
```

### 3. LLM Validator (The Safety Net)

```python
def validate_with_llm(raw_text: str, current_data: dict, client) -> dict:
    # Haiku is perfect for this: fast, cheap, good at extraction
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        system="Extract structured data from the text. Return corrected JSON.",
        messages=[{"role": "user", "content": f"Text: {raw_text}\nDraft: {current_data}"}]
    )
    return parse_json(response.content)
```

---

## Metrics to Track

- **Regex Coverage:** % of items handled entirely by regex
- **LLM Intervention Rate:** % of items routed to LLM
- **Cost Savings:** (LLM Cost for 100% - Actual Hybrid Cost) / (LLM Cost for 100%)
- **Accuracy Lift:** Delta in accuracy between pure Regex and Hybrid approach

---

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Confidence threshold set too low (e.g., 0.5) | Low-confidence outputs pass downstream undetected | Calibrate threshold on labelled sample of 100+ records |
| Regex with nested quantifiers on user input | Catastrophic backtracking causes CPU spike | Audit regexes with safe-regex tool; use possessive/atomic groups |
| LLM validation on synchronous hot path | Latency regression: 200ms p99 SLA violated | Move LLM calls to async queue; return regex result immediately |
| LLM cost overrun (expected regex, got 100x cost) | Confidence gate too strict; nearly all records routed to LLM | Lower routing threshold; improve regex coverage above 95% |
| Training data staleness misses new format variant | Prompt and regex not updated for format changes | Maintain golden test set with format variants |

## Verification

### Self-Verification Checklist

- [ ] Regex tested against adversarial inputs — safe-regex exits 0, no backtracking warnings
- [ ] LLM confidence threshold documented and tested (records below threshold routed to LLM, not passed silently)
- [ ] Cost per-call estimated and within budget: LLM intervention rate < 10% on representative sample
- [ ] Decision framework consulted — regex-first, LLM-only, or hybrid choice explicitly justified
- [ ] Raw extracted values and LLM-corrected values both logged for pipeline debugging
- [ ] Input sanitization (whitespace normalization, quote normalization) runs before regex matching

### Verification Commands

```bash
# Measure regex coverage
python -c "from extraction import measure_coverage; print(measure_coverage('test_data.json'))"

# Check for backtracking
npx safe-regex "your-pattern-here"

# Verify LLM intervention rate
python -c "from extraction import get_stats; print(get_stats())"

# Run end-to-end test
python test_extraction.py
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Regex Coverage | >= 95% of items handled by regex | Improve regex patterns before deploying |
| LLM Intervention | < 10% routed to LLM on representative sample | Lower confidence threshold or improve regex |
| Cost per 1000 docs | Within project budget | Adjust model tier or routing logic |
| Latency p99 | Regex path < 50ms; LLM path < 2s | Optimize regex, move LLM to async |

## Performance & Cost

### Model Selection

| Task | Recommended | Cost per 1000 items |
|---|---|---|
| Consistent pattern | Regex only | Near $0 |
| Mixed (95% pattern, 5% edge) | Hybrid regex + Haiku | $0.01-$0.05 |
| Free-form | LLM only (Haiku) | $0.10-$0.50 |
| Complex reasoning | LLM only (Sonnet) | $0.50-$2.00 |

### Parallelization

- **Regex parsing:** Can parallelize across documents (CPU-bound)
- **LLM validation:** Parallelize with rate limiting; watch API rate limits
- **Hybrid pipeline:** Regex runs first, LLM runs on low-confidence subset

### Context Budget

- **Expected context usage:** 2-5KB per extraction pipeline design
- **When to context-optimize:** When processing >10K documents or reviewing regex patterns

## Examples

### Example 1: Form Parsing

**User request:** "Extract structured data from 10,000 PDF forms. Most follow a template but some have variations."

**Skill execution:**
1. Apply decision framework: >90% follow pattern -> Regex first
2. Build regex pattern for the standard template
3. Test: regex covers 96% of forms at 100% accuracy
4. Add confidence scorer: items with <4 choices, missing fields -> LLM path
5. Route 4% to Haiku for correction
6. Total cost: $0.02 vs $5.00 for 100% LLM

**Result:** 96% regex coverage, 4% LLM intervention, 250x cost savings.

### Example 2: Edge Case - No Pattern

**User request:** "Extract meeting dates from free-form emails."

**Skill execution:**
1. Apply decision framework: no stable pattern -> LLM-only
2. Skip regex entirely
3. Use Haiku with structured output prompt
4. No regex development time wasted

**Result:** Correct approach chosen immediately. No over-engineered regex.

### Example 3: Regex Backtracking Attack

**User request:** "The parser is hanging on some inputs and using 100% CPU."

**Skill execution:**
1. Identify the problematic regex: uses nested quantifiers
2. Run safe-regex: detects catastrophic backtracking
3. Rewrite with atomic groups and possessive quantifiers
4. Add input length limit before regex matching
5. Test against adversarial inputs

**Result:** Parser is safe against adversarial input. CPU spikes eliminated.

## Anti-Patterns

- **Regex-as-Judge:** Trying to use a 1,000 character regex to handle every permutation of human error, because unmaintainable patterns silently misclassify edge cases and the next developer cannot reason about failure modes without rewriting the entire expression.
- **Blind LLM usage:** Piping 5,000 items to an LLM when 4,800 follow an exact pattern, because you pay token costs for every call and introduce non-deterministic outputs where a deterministic regex would have been free and 100% reproducible.
- **Silent Failures:** If the regex doesn't match, just skipping the item without a log or LLM fallback, because data is silently dropped and the corrupt output propagates downstream before anyone notices the loss.
- **Prompting for JSON on the happy path:** If you have JSON already from regex, don't ask the LLM "is this valid JSON?" - use a JSON validator, because sending valid structured data to an LLM for validation wastes tokens and risks the model returning a subtly reformatted string that breaks strict parsers.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Confidence threshold miscalibrated, LLM passes low-confidence output downstream | Threshold set too low during development; never tuned on production distribution | Run threshold calibration on a labelled sample of 100+ real records; pick the threshold that minimises false-passes at target precision |
| Regex has catastrophic backtracking on adversarial input causing CPU spike | Pattern uses nested quantifiers on user-controlled input; not tested against malicious strings | Audit all regexes with a backtracking analyser; replace greedy quantifiers with possessive or atomic groups |
| LLM cost overrun on high-volume endpoint | Confidence gate threshold too strict; nearly all records routed to LLM on inputs that regex handles well | Lower the LLM routing threshold; improve regex patterns to raise coverage above 95% on representative samples before deploying |
| Hybrid pipeline latency regression from synchronous LLM call on hot path | LLM validation inserted inline on a synchronous request handler with 200ms p99 SLA | Move LLM calls to an async queue; return regex best-effort result immediately; apply LLM correction asynchronously and store |

## References

### Internal Dependencies
- `cost-aware-llm-pipeline` — Routes LLM calls in hybrid pipeline to cheapest viable model (Haiku)
- `verification-loop` — Verifies extraction accuracy end-to-end

### External Standards
- [OWASP Validation Regex](https://owasp.org/www-community/OWASP_Validation_Regex_Repository) — Safe regex patterns for common inputs
- [safe-regex](https://github.com/substack/safe-regex) — Regex backtracking detection tool

### Related Skills
- `cost-aware-llm-pipeline` — Partner skill for LLM cost optimization in extraction pipelines
- `data-engineer` — Downstream consumer of extracted structured data

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Blocking Violations table, Verification with commands/quality gates, Performance & Cost section, Examples, References, Changelog. |

---
