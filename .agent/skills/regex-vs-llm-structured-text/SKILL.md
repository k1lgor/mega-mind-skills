---
name: regex-vs-llm-structured-text
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Decision framework and hybrid implementation for regex vs LLM text parsing. Use when parsing structured text (forms, logs, tables) to optimize cost and accuracy.
triggers:
  - "regex vs llm"
  - "text parsing"
  - "structured text extraction"
  - "hybrid parsing"
  - "confidence scoring"
  - "extraction pipeline"
---

# Regex vs LLM for Structured Text Parsing

## Identity

You are an extraction and parsing specialist. You know that LLMs are powerful but expensive and sometimes inconsistent, while Regex is fast and deterministic but brittle. You don't choose one — you build a hybrid pipeline that uses Regex for 95% of the work and LLMs strictly for the edge cases.

## When to Activate

- Parsing documents with repeating patterns (questions, forms, logs, legacy reports)
- Deciding between regex and LLM for a new extraction task
- Building hybrid pipelines that combine deterministic rules with probabilistic model fixes
- Optimizing cost and latency tradeoffs in text processing workflows

## When NOT to Use

- When the input format is already well-defined JSON, XML, or CSV — use a proper parser, not regex or LLM
- When the input is 100% free-form natural language with no repeating structure — LLM-only is correct, no regex pass needed
- For single-document extraction where cost and latency are irrelevant — just use the LLM directly
- When the extraction target is a known standard format (e.g., ISO dates, email addresses) — use a battle-tested library function, not custom regex

---

## Decision Framework

```
Is the text format consistent and repeating?
├── Yes (>90% follows a stable pattern) → Start with Regex
│   ├── Regex handles 98%+ accuracy → Done, no LLM needed
│   └── Regex handles <95% accuracy → Add LLM for edge cases only
└── No (free-form, highly variable) → Use LLM directly
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
    │
    ▼
[Regex Parser] ─── Step 1: Deterministic extraction (95-98% accuracy)
    │
    ▼
[Confidence Scorer] ─ Step 2: Identifies items that failed or look "off"
    │
    ├── High confidence (≥0.95) ─────▶ [Direct Output] (Fast/Cheap)
    │
    └── Low confidence (<0.95) ──────▶ [LLM Validator] ──▶ [Output] (Slow/Pricey)
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

## Best Practices

- **Log raw vs corrected:** Always store what the regex found and what the LLM fixed to improve your regex over time.
- **Use Haiku for validation:** You don't need Opus/Sonnet to re-parse a specific line of text; Haiku is 10x cheaper and usually sufficient.
- **Fail fast:** If the text is 100% free-form, don't waste time on a complex regex that will always fail.
- **Sanitize Input:** Run a simple cleaner (strip whitespace, normalize quotes) before regex to improve match rates.

---

---

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Confidence threshold miscalibrated, LLM passes low-confidence output downstream | Threshold set too low (e.g., 0.5) during development; never tuned on production distribution | Run threshold calibration on a labelled sample of 100+ real records; pick the threshold that minimises false-passes at target precision |
| Regex has catastrophic backtracking on adversarial input causing CPU spike | Pattern uses nested quantifiers (e.g., `(.+)+`) on user-controlled input; not tested against malicious strings | Audit all regexes with a backtracking analyser (e.g., `safe-regex` for Node.js); replace greedy quantifiers with possessive or atomic groups |
| LLM cost overrun on high-volume endpoint (expected regex, got 100× cost) | Confidence gate threshold too strict; nearly all records routed to LLM on inputs that regex handles well | Lower the LLM routing threshold; improve regex patterns to raise coverage above 95% on representative samples before deploying |
| Hybrid pipeline latency regression from synchronous LLM call on hot path | LLM validation inserted inline on a synchronous request handler with 200ms p99 SLA | Move LLM calls to an async queue; return regex best-effort result immediately; apply LLM correction asynchronously and store |
| Training data staleness causes LLM to miss newly introduced format variant | Document format changed (new field added, date format shifted); LLM prompt not updated; regex pattern misses new structure | Maintain a golden test set with format variants; run it on every prompt change; add the new variant as a test case before deploying |

## Self-Verification Checklist

- [ ] Regex tested against adversarial inputs — `safe-regex` (or equivalent) exits 0 with no catastrophic-backtracking warnings
- [ ] LLM confidence threshold documented (e.g., `CONFIDENCE_GATE = 0.85`) and tested: records below threshold are verifiably routed to LLM, not passed silently
- [ ] Cost per-call estimated and within budget: LLM intervention rate < 10% on representative sample (confirmed by logging actual intervention rate)
- [ ] Decision framework consulted — the choice between regex-first, LLM-only, or hybrid is explicitly justified
- [ ] Raw extracted values and LLM-corrected values are both logged for pipeline debugging
- [ ] Input sanitization (whitespace normalization, quote normalization) runs before regex matching

## Success Criteria

This skill is complete when: 1) the decision framework has been applied and the correct parsing strategy is documented, 2) the hybrid pipeline logs both raw regex output and LLM corrections, and 3) LLM intervention rate is below the project's cost threshold for pattern-heavy inputs.

## Anti-Patterns

- **Regex-as-Judge:** Trying to use a 1,000 character regex to handle every permutation of human error, because unmaintainable patterns silently misclassify edge cases and the next developer cannot reason about failure modes without rewriting the entire expression.
- **Blind LLM usage:** Piping 5,000 items to an LLM when 4,800 follow an exact pattern, because you pay token costs for every call and introduce non-deterministic outputs where a deterministic regex would have been free and 100% reproducible.
- **Silent Failures:** If the regex doesn't match, just skipping the item without a log or LLM fallback, because data is silently dropped and the corrupt output propagates downstream before anyone notices the loss.
- **Prompting for JSON on the happy path:** If you have JSON already from regex, don't ask the LLM "is this valid JSON?" – use a JSON validator, because sending valid structured data to an LLM for validation wastes tokens and risks the model returning a subtly reformatted string that breaks strict parsers.
