---
name: cost-aware-llm-pipeline
compatibility: Antigravity, Claude Code, GitHub Copilot
description: LLM cost optimization patterns for model routing, budget tracking, and prompt caching. Use when building AI pipelines where cost matters or when routing tasks to the right model tier.
triggers:
  - "cost optimization"
  - "model routing"
  - "llm cost"
  - "budget tracking"
  - "prompt caching"
  - "which model should I use"
  - "reduce api costs"
  - "haiku vs sonnet vs opus"
---

# Cost-Aware LLM Pipeline

## Identity

You are an LLM cost optimization specialist. Your job is to ensure AI pipelines stay within budget while maximizing output quality — by routing tasks to the cheapest model that can handle them, tracking costs immutably, retrying only on transient errors, and caching long prompts.

## When to Activate

- Building multi-step AI pipelines where cost matters
- Choosing which model to use for a task
- Implementing retry logic with LLM calls
- Setting up prompt caching for repeated system prompts
- When a pipeline is spending more than expected

---

## Core Concept: The 4 Levers

```
┌─────────────────────── Cost Optimization ───────────────────────┐
│                                                                  │
│  1. MODEL ROUTING     Route by complexity (Haiku vs Sonnet)     │
│  2. COST TRACKING     Immutable records of every API call       │
│  3. NARROW RETRY      Retry only transient errors, fail fast    │
│  4. PROMPT CACHING    Cache long system prompts                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Lever 1: Model Routing by Task Complexity

Automatically select cheaper models for simple tasks, reserving expensive models for complex reasoning.

### Model Tiers (2025-2026)

| Model             | Cost (input/1M) | Best For                                  |
| ----------------- | --------------- | ----------------------------------------- |
| claude-haiku-3-5  | ~$0.80          | Extraction, formatting, simple transforms |
| claude-sonnet-4-5 | ~$3.00          | Standard coding, analysis, most tasks     |
| claude-opus-4     | ~$15.00         | Deep architectural reasoning, research    |

**Rule of thumb**: Use Haiku for 60%+ of tasks in a pipeline. Reserve Opus for only the most complex reasoning.

### Routing Logic

```python
HAIKU = "claude-haiku-3-5-20251001"
SONNET = "claude-sonnet-4-5"
OPUS = "claude-opus-4-5"

# Complexity signals
COMPLEX_TEXT_THRESHOLD = 10_000   # characters
COMPLEX_ITEM_THRESHOLD = 30       # items to process

def select_model(
    text_length: int = 0,
    item_count: int = 0,
    requires_deep_reasoning: bool = False,
    force_model: str | None = None
) -> str:
    if force_model:
        return force_model
    if requires_deep_reasoning:
        return OPUS
    if text_length >= COMPLEX_TEXT_THRESHOLD or item_count >= COMPLEX_ITEM_THRESHOLD:
        return SONNET
    return HAIKU  # 3-4x cheaper than Sonnet
```

### Task → Model Mapping

| Task                               | Model  | Rationale           |
| ---------------------------------- | ------ | ------------------- |
| Extract JSON fields from text      | Haiku  | Simple extraction   |
| Format/clean data                  | Haiku  | Deterministic       |
| Write a utility function           | Haiku  | Simple coding       |
| Review code for bugs               | Sonnet | Needs reasoning     |
| Design a system architecture       | Opus   | Deep reasoning      |
| Summarize long documents           | Sonnet | Complex synthesis   |
| Classify items (simple)            | Haiku  | Low complexity      |
| Security audit with exploit chains | Opus   | Complex adversarial |

---

## Lever 2: Immutable Cost Tracking

Track cumulative spend with frozen dataclasses. Never mutate — always create new records.

```python
from dataclasses import dataclass

PRICING = {
    "claude-haiku-3-5-20251001": {"input": 0.80, "output": 4.00},     # per 1M tokens
    "claude-sonnet-4-5":          {"input": 3.00, "output": 15.00},
    "claude-opus-4-5":            {"input": 15.00, "output": 75.00},
}

@dataclass(frozen=True, slots=True)
class CostRecord:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

    @classmethod
    def from_response(cls, model: str, usage) -> "CostRecord":
        prices = PRICING.get(model, PRICING["claude-sonnet-4-5"])
        cost = (
            usage.input_tokens * prices["input"] / 1_000_000 +
            usage.output_tokens * prices["output"] / 1_000_000
        )
        return cls(model=model, input_tokens=usage.input_tokens,
                   output_tokens=usage.output_tokens, cost_usd=cost)

@dataclass(frozen=True, slots=True)
class CostTracker:
    budget_limit: float = 1.00
    records: tuple[CostRecord, ...] = ()

    def add(self, record: CostRecord) -> "CostTracker":
        """Return new tracker with added record (never mutates self)."""
        return CostTracker(
            budget_limit=self.budget_limit,
            records=(*self.records, record),
        )

    @property
    def total_cost(self) -> float:
        return sum(r.cost_usd for r in self.records)

    @property
    def over_budget(self) -> bool:
        return self.total_cost > self.budget_limit

    def summary(self) -> str:
        return f"${self.total_cost:.4f} / ${self.budget_limit:.2f} ({len(self.records)} calls)"
```

### Using the Tracker

```python
tracker = CostTracker(budget_limit=0.50)

# After each API call
response = client.messages.create(model=model, ...)
record = CostRecord.from_response(model, response.usage)
tracker = tracker.add(record)

if tracker.over_budget:
    raise BudgetExceededError(f"Budget exceeded: {tracker.summary()}")

print(tracker.summary())  # "$0.0234 / $0.50 (3 calls)"
```

---

## Lever 3: Narrow Retry Logic

Retry **only** on transient errors. Fail fast on permanent ones.

```python
import time
from anthropic import (
    APIConnectionError,    # Transient: network issue
    InternalServerError,   # Transient: server error
    RateLimitError,        # Transient: slow down
    AuthenticationError,   # Permanent: wrong key
    BadRequestError,       # Permanent: invalid request
)

RETRYABLE = (APIConnectionError, RateLimitError, InternalServerError)
MAX_RETRIES = 3

def call_with_retry(func, max_retries: int = MAX_RETRIES):
    """Retry only transient errors. Fail fast on auth/bad request."""
    for attempt in range(max_retries):
        try:
            return func()
        except RETRYABLE as e:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"Retry {attempt + 1}/{max_retries} after {wait}s: {e}")
            time.sleep(wait)
    # AuthenticationError, BadRequestError → not caught → raise immediately
```

### Error Classification

| Error                 | Retry? | Why                              |
| --------------------- | ------ | -------------------------------- |
| `APIConnectionError`  | ✅ Yes | Network blip                     |
| `RateLimitError`      | ✅ Yes | Slow down                        |
| `InternalServerError` | ✅ Yes | Anthropic server issue           |
| `AuthenticationError` | ❌ No  | Wrong API key — fix it first     |
| `BadRequestError`     | ❌ No  | Bad prompt — retrying won't help |
| `NotFoundError`       | ❌ No  | Model name wrong                 |

---

## Lever 4: Prompt Caching

Cache long system prompts to avoid resending (and paying for) them on every request.

```python
# Without caching: Pay for system_prompt on EVERY call
# With caching: Pay full price once, then 10% on subsequent calls

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": system_prompt,          # Long, static content
                "cache_control": {"type": "ephemeral"},  # ← Cache this!
            },
            {
                "type": "text",
                "text": user_input,             # Variable content (not cached)
            }
        ],
    }
]
```

### When to Cache

| Cache?    | Content Type                                            |
| --------- | ------------------------------------------------------- |
| ✅ Always | System prompts (role, rules, guidelines)                |
| ✅ Always | Reference documents included in every call              |
| ✅ Always | Few-shot examples that don't change                     |
| ❌ Never  | User-specific or per-request content                    |
| ❌ Never  | Content shorter than 1,024 tokens (minimum for caching) |

---

## Pipeline Template

```python
async def cost_aware_pipeline(tasks: list[dict], budget: float = 1.00):
    client = anthropic.Anthropic()
    tracker = CostTracker(budget_limit=budget)

    for task in tasks:
        # 1. Route to cheapest viable model
        model = select_model(
            text_length=len(task.get("content", "")),
            requires_deep_reasoning=task.get("complex", False)
        )

        # 2. Check budget before proceeding
        if tracker.over_budget:
            print(f"Budget exceeded at task {task['id']}. Cost: {tracker.summary()}")
            break

        # 3. Call with retry
        response = call_with_retry(lambda: client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": task["prompt"]
            }]
        ))

        # 4. Track cost immutably
        tracker = tracker.add(CostRecord.from_response(model, response.usage))

        # 5. Log progress
        print(f"Task {task['id']} [{model}]: {tracker.summary()}")

    return tracker
```

---

## Cost Optimization Checklist

Before running any LLM pipeline:

- [ ] Am I using the cheapest model that can handle this task?
- [ ] Do I have a budget limit set?
- [ ] Are my long system prompts cached?
- [ ] Is my retry logic narrowed to transient errors only?
- [ ] Am I tracking costs per-call (not just total)?
- [ ] Do I have an early exit when budget is exceeded?

---

## Tips

- **Profile before optimizing**: Run one test call and check the response usage fields
- **Haiku is underrated**: For extraction/formatting tasks, accuracy is nearly identical to Sonnet at 3-4x lower cost
- **Cache early**: The minimum cache size is 1,024 tokens — most system prompts qualify
- **Budget gates**: Stop the pipeline when budget is 80% consumed (leave 20% for error recovery)
- **Log per-call**: Aggregate cost is less useful than seeing which step is expensive
