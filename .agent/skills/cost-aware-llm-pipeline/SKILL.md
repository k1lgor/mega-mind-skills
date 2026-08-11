---
name: cost-aware-llm-pipeline
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  LLM cost optimization patterns for model routing, budget tracking, and prompt caching.
  Use when building AI pipelines where cost matters or when routing tasks to the right model tier.
  Covers immutable cost tracking, narrow retry logic, prompt caching, and model routing by task complexity with budget enforcement.
category: meta-learning
triggers:
  - "cost optimization"
  - "model routing"
  - "llm cost"
  - "budget tracking"
  - "prompt caching"
  - "which model should I use"
  - "reduce api costs"
  - "haiku vs sonnet vs opus"
  - "token budget"
dependencies:
  - ml-engineer: recommended
  - search-vector-architect: recommended
  - rtk: optional
---

# Cost-Aware LLM Pipeline

## Identity

You are an LLM cost optimization specialist. Your job is to ensure AI pipelines stay within budget while maximizing output quality — by routing tasks to the cheapest model that can handle them, tracking costs immutably, retrying only on transient errors, and caching long prompts.

**Your core responsibility:** Design AI pipelines that deliver maximum quality per dollar by routing tasks to the cheapest viable model.

**Your operating principle:** 4 levers — model routing, cost tracking, narrow retry, prompt caching — applied in order.

**Your quality bar:** Every pipeline step has an explicit model assignment based on task complexity, per-call costs are logged immutably, budget ceiling is enforced, and retry logic only fires on transient errors — no exceptions.

## When to Use

- Building multi-step AI pipelines where cost matters
- Choosing which model to use for a task
- Implementing retry logic with LLM calls
- Setting up prompt caching for repeated system prompts
- When a pipeline is spending more than expected

## When NOT to Use

- Single-call scripts where total cost is < $0.01 — overhead of routing logic exceeds savings
- When all tasks are uniformly complex (e.g., all require Opus) — routing adds complexity with no benefit
- For prototyping — add cost controls after the pipeline logic is proven correct, not before
- When the team has no visibility into API spend (cost controls without observability are theater)

## Core Principles

1. **Route by complexity, not by habit.** Always start with the cheapest model that could plausibly handle the task. Test Haiku before Sonnet, Sonnet before Opus. Escalate only when quality fails, not as a default.
2. **Track costs immutably.** Every API call produces a frozen cost record — never mutate, always append. Immutable records are auditable; mutable counters hide the source of cost spikes.
3. **Retry narrow, fail fast.** Only retry transient errors (connection, rate limit, server error). Authentication and bad-request errors must fail immediately — no retry budget wasted on permanent failures.
4. **Cache long prompts, never short ones.** System prompts and reference documents over 1,024 tokens should use `cache_control`. The first call pays full price; subsequent calls pay ~10% of the prompt cost. Content under 1,024 tokens never qualifies.
5. **Enforce budget before every call.** Check the cumulative cost against the budget ceiling before making any API call. Stop the pipeline when budget is exceeded — mid-pipeline cost spikes are the most expensive failure mode.

---

## Core Concept: The 4 Levers

```
+----------------------- Cost Optimization -----------------------+
|                                                                  |
|  1. MODEL ROUTING     Route by complexity (Haiku vs Sonnet)     |
|  2. COST TRACKING     Immutable records of every API call       |
|  3. NARROW RETRY      Retry only transient errors, fail fast    |
|  4. PROMPT CACHING    Cache long system prompts                 |
|                                                                  |
+------------------------------------------------------------------+
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

### Task to Model Mapping

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
    # AuthenticationError, BadRequestError -> not caught -> raise immediately
```

### Error Classification

| Error                 | Retry? | Why                              |
| --------------------- | ------ | -------------------------------- |
| `APIConnectionError`  | Yes    | Network blip                     |
| `RateLimitError`      | Yes    | Slow down                        |
| `InternalServerError` | Yes    | Server issue                     |
| `AuthenticationError` | No     | Wrong API key - fix it first     |
| `BadRequestError`     | No     | Bad prompt - retrying won't help |
| `NotFoundError`       | No     | Model name wrong                 |

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
                "cache_control": {"type": "ephemeral"},  # Cache this!
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
| Always    | System prompts (role, rules, guidelines)                |
| Always    | Reference documents included in every call              |
| Always    | Few-shot examples that don't change                     |
| Never     | User-specific or per-request content                    |
| Never     | Content shorter than 1,024 tokens (minimum for caching) |

---

## Pipeline Template

```python
async def cost_aware_pipeline(tasks: list[dict], budget: float = 1.00):
    client = anthropic.Anthropic()
    tracker = CostTracker(budget_limit=budget)

    for task in tasks:
        model = select_model(
            text_length=len(task.get("content", "")),
            requires_deep_reasoning=task.get("complex", False)
        )

        if tracker.over_budget:
            print(f"Budget exceeded at task {task['id']}. Cost: {tracker.summary()}")
            break

        response = call_with_retry(lambda: client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": task["prompt"]}]
        ))

        tracker = tracker.add(CostRecord.from_response(model, response.usage))
        print(f"Task {task['id']} [{model}]: {tracker.summary()}")

    return tracker
```

---

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Sending same prompt to most expensive model without testing cheaper option | 20x cost difference; cheaper model often sufficient | Test Haiku first; escalate to Sonnet/Opus only if quality fails |
| Building pipeline without per-call cost logging | Cannot identify which stage caused cost spike | Instrument every call with cost tag (stage name, model, tokens) |
| Using unbounded context as pipeline input | Cost multiplied by ratio of irrelevant tokens | Compress context; only send relevant subset |
| Retrying failed model call without exponential backoff | Naive retry during outage exhausts monthly budget in minutes | Implement exponential backoff with jitter; cap at 3 retries |
| Hardcoding model names as string literals | Swapping models requires changes in every call site | Use single configuration entry for model assignment |

## Verification

### Self-Verification Checklist

- [ ] Cheapest viable model selected for each task type (Haiku for extraction, Sonnet for reasoning, Opus for architecture)
- [ ] Long system prompts cached with `cache_control`
- [ ] Retry logic narrowed to transient errors only
- [ ] Budget limit set and enforced (pipeline stops when exceeded)
- [ ] Per-call costs logged immutably
- [ ] Cost-per-step visible: pipeline output includes cost summary table

### Verification Commands

```bash
# Check model routing
python -c "from routing import select_model; print(select_model(text_length=500))"

# Verify cost tracking
python -c "from cost_tracker import CostTracker; t = CostTracker(budget_limit=0.50); print(t.summary())"

# Run pipeline with dry-run budget check
python pipeline.py --dry-run --budget 0.50

# Check cumulative savings
python -c "from cost_tracker import get_session_costs; print(get_session_costs().summary())"
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Model Selection | Cheapest model that passes quality bar used for each task | Add routing logic; downgrade over-provisioned tasks |
| Budget Enforcement | Pipeline stops when budget exceeded | Add budget gate check before each call |
| Retry Safety | Only transient errors retried, max 3 attempts | Audit error handling; remove permanent-error retries |
| Cost Visibility | Per-stage cost report generated | Add cost instrumentation to each pipeline step |

## Performance & Cost

### Model Selection

| Task Type | Recommended Model | Cost/1K calls |
|---|---|---|
| Extraction/formatting | Haiku | $0.01-$0.05 |
| Standard coding/review | Sonnet | $0.05-$0.30 |
| Architecture/research | Opus | $0.30-$1.50 |

### Parallelization

- **Independent tasks:** Can parallelize with separate budget trackers
- **Sequential pipeline:** Must run sequentially (each step depends on prior)
- **Retry calls:** Always sequential with backoff

### Context Budget

- **Expected context usage:** 3-6KB per pipeline configuration session
- **When to context-optimize:** When configuring complex multi-stage pipelines with budget constraints

## Examples

### Example 1: Multi-Stage Document Processing

**User request:** "Process 1000 support tickets. Classify, summarize, and route them."

**Skill execution:**
1. Task 1 (Classify): Route to Haiku — simple intent classification
2. Task 2 (Summarize): Route to Sonnet — needs reasoning and synthesis
3. Task 3 (Route): Rules-based post-processing — no model needed
4. Budget: $1.00 limit
5. Result: 600 Haiku calls ($0.48), 400 Sonnet calls ($1.20) — over budget!
6. Optimization: Use Haiku for summarization — quality check passes at $0.80 total

**Result:** Pipeline within budget. $0.80 vs $3.50 for all-Sonnet.

### Example 2: Edge Case - Retry Storm

**User request:** "Our pipeline cost $50 yesterday instead of the usual $2. What happened?"

**Skill execution:**
1. Check cost logs: Retry loop ran 10x on each of 500 items
2. Root cause: API had a brief outage; no backoff implemented
3. Fix: Add exponential backoff with jitter, cap at 3 retries
4. Result: Cost back to $2/day

**Result:** Retry storm prevented. Cost spike eliminated.

### Example 3: Prompt Caching Savings

**User request:** "We send the same 2000-token system prompt to Haiku 10,000 times a day."

**Skill execution:**
1. Add `cache_control: {"type": "ephemeral"}` to system prompt block
2. First call: full price. Subsequent 9,999 calls: 10% of prompt cost
3. Daily savings: ~$16/day (from $16 to $1.60 for prompt tokens)

**Result:** 90% cost reduction on prompt tokens.

## Anti-Patterns

- Never send the same prompt to the most expensive model without first testing if a cheaper model meets the quality bar because the cost difference between Opus and Haiku is 20x, and most classification and extraction tasks are solved correctly by the cheaper model.
- Never build a pipeline without per-call cost logging because without granular cost data you cannot identify which stage is responsible for a cost spike and the only remediation available is to reduce quality across the entire pipeline.
- Never use unbounded context as pipeline input because sending an entire codebase or document corpus to a model call when only a subset is relevant multiplies cost by the ratio of irrelevant to relevant tokens.
- Never retry a failed model call without exponential backoff and a cost cap because a naive retry loop during a model provider outage can exhaust your monthly budget in minutes.
- Never hardcode model names as string literals throughout the pipeline because when you need to swap a model for cost or quality reasons, a hardcoded name requires changes in every call site instead of one configuration entry.
- Never cache model outputs without including the full prompt hash in the cache key because a prompt change that is invisible to a partial cache key causes stale cached responses to be served for semantically different inputs.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Expensive model used for task cheap model handles | No routing logic; all requests sent to most capable model by default | Add task complexity classifier; route simple tasks to cheapest model |
| Token budget exhausted mid-pipeline, truncating output | Input context not estimated before sending; no budget gate | Add pre-flight token count check; apply context compression |
| Cost spike from prompt triggering verbose output | Open-ended instructions on high-token-price model | Use constrained output prompts; validate length before accepting |
| Model downgrade silently degrades quality | Cheaper model selected for cost but quality not re-validated | Define minimum quality bar; run eval after model routing change |
| Retry storm multiplies cost 3-10x during API outage | Exponential backoff not implemented | Implement backoff with jitter; cap at 3 retries; fail fast after budget exceeded |

## References

### Internal Dependencies
- `ml-engineer` — Uses cost-aware routing for LLM-based model evaluation and GenAI pipelines
- `search-vector-architect` — Routes LLM calls in RAG pipeline to cheapest viable model

### External Standards
- [Anthropic Pricing](https://www.anthropic.com/pricing) — Current model pricing (verify periodically)
- [OpenAI Pricing](https://openai.com/api/pricing/) — Alternative provider pricing reference

### Related Skills
- `ml-engineer` — Partner skill for model evaluation and selection
- `rtk` — Companion skill for token optimization in CLI commands

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Blocking Violations table, Verification with commands/quality gates, Performance & Cost section, Examples, References, Changelog. |
---
