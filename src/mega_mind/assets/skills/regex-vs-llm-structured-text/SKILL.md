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

## Anti-Patterns

- **Regex-as-Judge:** Trying to use a 1,000 character regex to handle every permutation of human error.
- **Blind LLM usage:** Piping 5,000 items to an LLM when 4,800 follow an exact pattern.
- **Silent Failures:** If the regex doesn't match, just skipping the item without a log or LLM fallback.
- **Prompting for JSON on the happy path:** If you have JSON already from regex, don't ask the LLM "is this valid JSON?" – use a JSON validator.
