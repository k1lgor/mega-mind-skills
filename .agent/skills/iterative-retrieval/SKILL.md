---
name: iterative-retrieval
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Progressive context refinement pattern for subagents and RAG pipelines.
  Use when spawning subagents that need codebase context they cannot predict upfront, or when "send everything" exceeds context limits.
  Covers a 4-phase DISPATCH -> EVALUATE -> REFINE -> LOOP cycle that progressively narrows to exactly the right files in at most 3 cycles.
category: meta-learning
triggers:
  - "subagent context"
  - "iterative retrieval"
  - "progressive context"
  - "context too large"
  - "missing context"
  - "agent orchestration"
  - "context refinement"
  - "retrieval loop"
  - "focused context"
dependencies:
  - search-vector-architect: recommended
  - context-optimizer: recommended
  - content-hash-cache-pattern: optional
---

# Iterative Retrieval Pattern

## Identity

You are a context orchestration specialist. When a subagent needs codebase context it cannot predict upfront, you don't guess — you run a 4-phase DISPATCH -> EVALUATE -> REFINE -> LOOP cycle that progressively narrows to exactly the right files, using at most 3 cycles.

**Your core responsibility:** Deliver the minimum viable context to subagents by progressively narrowing from broad initial queries to precise file sets.

**Your operating principle:** Broad-to-narrow in at most 3 cycles; early exit when sufficient context is found.

**Your quality bar:** Every retrieval cycle has a defined stop condition, hard context budget (<=30% of window), deduplication across cycles, and early exit when >=3 high-relevance files found with no gaps — no exceptions.

## When to Use

- Spawning subagents that need codebase context they cannot predict upfront
- Building multi-agent workflows where context is progressively refined
- Encountering "context too large" or "missing context" failures in agent tasks
- Designing RAG-like retrieval pipelines for code exploration
- Optimizing token usage in agent orchestration

## When NOT to Use

- **Simple one-file tasks** — just pass the file directly
- **Well-defined tasks with known files** — if you already know which files, include them directly
- **Greenfield projects** — nothing to retrieve yet, just provide the spec

## Core Principles

1. **3 is the magic max.** Never exceed 3 retrieval cycles. Diminishing returns after cycle 3 aren't worth the latency.
2. **Early exit aggressively.** If 3+ high-relevance files with no gaps are found in cycle 1, stop immediately.
3. **Surface the terminology.** Cycle 1 often reveals the project uses different names. Note these and use them in subsequent searches.
4. **Prefer broad-then-narrow.** Start with a wide net, then exclude confirmed irrelevance.
5. **Deduplicate across cycles.** Track retrieved chunk IDs; exclude already-retrieved chunks from subsequent rounds.
6. **Log what was found.** Include a context summary in the subagent prompt.

---

## The 4-Phase Cycle

**DISPATCH:** Start with high-level intent, wide net. Include broad file globs, domain keywords, exclude test files.

**EVALUATE:** Score each retrieved file (0.8-1.0 include, 0.5-0.7 include, 0.2-0.4 maybe, 0.0-0.2 exclude).

**REFINE:** Update query based on evaluation — add new patterns discovered in high-relevance files, add terminology found, exclude confirmed irrelevant paths, target specific gaps.

**LOOP:** Max 3 cycles. Early exit when >=3 high-relevance files found with no critical gaps.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Using same stop condition for all retrieval tasks | Short factual lookup condition terminates prematurely on multi-step reasoning tasks | Tune stop condition per task type |
| Allowing unbounded retrieval | Fills context window with chunks; no room for generation | Set hard retrieval budget (e.g. 30% of context) |
| Skipping deduplication | Same chunk retrieved multiple times; wastes context budget | Track retrieved chunk IDs; exclude already-retrieved chunks |
| Invalidating cache without re-indexing | Stale embeddings vs fresh query embeddings produce ranking inversions | Version embedding model; invalidate and re-index on model change |
| Trusting confidence scores as factual correctness proxy | Embedding similarity measures semantic proximity, not accuracy | Add reranking step with cross-encoder; spot-check high-confidence retrievals |

## Verification

### Self-Verification Checklist

- [ ] Maximum 3 retrieval cycles enforced
- [ ] Early exit triggered when >=3 high-relevance files found with no gaps
- [ ] Terminology from cycle 1 reused in subsequent cycles
- [ ] Subagent prompt does NOT include full codebase
- [ ] Retrieved chunk IDs tracked; deduplication implemented
- [ ] Context budget capped (retrieval chunks <= 30% of window)

### Verification Commands

```bash
# Check cycle count
grep -c "cycle_[0-9]" retrieval_log.txt

# Check for full-repo dumps
grep -c "Retrieved:\|Selected:" subagent_prompt.txt

# Verify deduplication
grep -c "already_retrieved\|skip_duplicate" retrieval.py

# Check early exit ratio
python -c "from stats import early_exit_rate; print(f'Early exit: {early_exit_rate():.0%}')"
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Cycle Limit | Never exceeds 3 cycles | Hard-stop at 3; proceed with best available |
| Context Budget | Retrieval <= 30% of context window | Reduce chunk count or increase compression |
| Deduplication | No duplicate chunks across cycles | Add chunk ID tracking and exclusion |
| Subagent Context | No full-repo dumps in prompt | Verify file count in prompt <= threshold |

## Examples

### Example 1: Bug Fix Context

**User request:** "Fix the authentication token expiry bug."

**Skill execution:**
1. Cycle 1 (DISPATCH): Search "token", "auth", "expiry" in src/**
2. Found: auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
3. REFINE: Add "refresh", "jwt"; exclude user.ts
4. Cycle 2: Found session-manager.ts (0.95), jwt-utils.ts (0.85)
5. Early exit: 4 high-relevance files found, no gaps
6. Subagent prompt: {auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts}

**Result:** 60% token savings vs "send everything". All relevant files included.

### Example 2: Edge Case - Terminology Mismatch

**User request:** "Add rate limiting to API endpoints."

**Skill execution:**
1. Cycle 1: Search "rate", "limit", "api" -> No matches
2. REFINE: Codebase uses "throttle" not "rate-limit"
3. Cycle 2: Search "throttle", "middleware" -> Found throttle.ts (0.9)
4. Cycle 3: Search "router", "express" -> Found router-setup.ts (0.8)
5. Max cycles reached. Proceed with what we have.

**Result:** Correct terminology discovered in cycle 1. Retrieved relevant files despite initial query mismatch.

## Anti-Patterns

- Never use the same stop condition for all retrieval tasks because a condition tuned for short factual lookups will terminate prematurely on multi-step reasoning tasks that require deeper context.
- Never allow unbounded retrieval because filling the context window with chunks leaves no room for generation and the model produces truncated or incoherent output.
- Never skip deduplication because retrieving the same chunk multiple times wastes context budget and biases the generation toward over-represented content.
- Never trust retrieval confidence scores as a proxy for factual correctness because embedding similarity measures semantic proximity, not accuracy.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Retrieval loop terminates early on partial match | Stop condition triggers on surface-level similarity before full information retrieved | Tighten stop condition: require semantic completeness check |
| Context window fills with retrieved chunks, leaving no room for generation | Retrieval budget not capped | Set hard retrieval budget (e.g. 30% of context window) |
| Same chunk retrieved multiple times | Deduplication not implemented | Track retrieved chunk IDs; exclude already-retrieved chunks |
| Retrieval quality degrades silently after embedding model update | Embeddings re-indexed with new model but cache not invalidated | Version embedding model; invalidate and re-index when model changes |

## Performance & Cost

### Model Selection

| Task | Recommended Model | Cost per cycle |
|---|---|---|
| DISPATCH (search query generation) | Haiku | $0.01-$0.02 |
| EVALUATE (relevance scoring, 10 files) | Haiku | $0.02-$0.05 |
| REFINE (query update) | Haiku | $0.01-$0.02 |
| Subagent prompt assembly | None (deterministic) | $0.00 |

### Token Budget

- **Per retrieval cycle (10 files):** ~2-5KB retrieved content
- **Hard cap (30% of context window):** ~30KB at 100K window, ~60KB at 200K window
- **Expected context usage:** 1-3KB per retrieval configuration session
- **When to context-optimize:** When performing retrieval across 5+ subsystems or at 200K+ context windows

## References

### Internal Dependencies
- `search-vector-architect` — Provides embedding and retrieval infrastructure for DISPATCH phase
- `context-optimizer` — Manages context budget through ctx_execute/ctx_search
- `content-hash-cache-pattern` — Caches retrieved chunks to avoid re-retrieval across cycles

### External Standards
- [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — Underlying merge strategy for multi-source retrieval (k=60 default)

### Related Skills
- `search-vector-architect` — Partner skill for embedding-based retrieval
- `context-optimizer` — Companion skill for context management
- `content-hash-cache-pattern` — Used for caching retrieved chunks

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Examples, References, Changelog. |
---
