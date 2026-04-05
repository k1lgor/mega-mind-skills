---
name: iterative-retrieval
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Progressive context refinement pattern for subagents and RAG pipelines. Use when spawning subagents that need codebase context they cannot predict upfront, or when "send everything" exceeds context limits.
triggers:
  - "subagent context"
  - "iterative retrieval"
  - "progressive context"
  - "rag pipeline"
  - "context too large"
  - "missing context"
  - "agent orchestration"
  - "context refinement"
---

# Iterative Retrieval Pattern

## Identity

You are a context orchestration specialist. When a subagent needs codebase context it cannot predict upfront, you don't guess — you run a 4-phase DISPATCH → EVALUATE → REFINE → LOOP cycle that progressively narrows to exactly the right files, using at most 3 cycles.

## When to Activate

- Spawning subagents that need codebase context they cannot predict upfront
- Building multi-agent workflows where context is progressively refined
- Encountering "context too large" or "missing context" failures in agent tasks
- Designing RAG-like retrieval pipelines for code exploration
- Optimizing token usage in agent orchestration

---

## The Problem

Subagents start with limited context and don't know:

- Which files contain relevant code
- What patterns exist in the codebase
- What terminology the project uses

**Standard approaches fail:**

- **Send everything** → Exceeds context limits (100K+ tokens)
- **Send nothing** → Agent lacks critical information, hallucinates
- **Guess what's needed** → Often wrong, expensive to fix

---

## The Solution: 4-Phase Iterative Retrieval

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ DISPATCH │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3 cycles → proceed with best     │
└─────────────────────────────────────────────┘
```

---

## Phase 1: DISPATCH — Initial Broad Query

Start with high-level intent, wide net:

```javascript
const initialQuery = {
  patterns: ["src/**/*.ts", "lib/**/*.ts"], // broad file globs
  keywords: ["authentication", "user", "session"], // domain terms
  excludes: ["*.test.ts", "*.spec.ts"], // skip test files
};

const candidates = await retrieveFiles(initialQuery);
```

**Goal:** Cast a wide net. It's okay to retrieve too much here.

---

## Phase 2: EVALUATE — Score Relevance

Rate each retrieved file against the task:

```javascript
function evaluateRelevance(files, task) {
  return files.map((file) => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task),
  }));
}
```

### Scoring Criteria

| Score   | Meaning                                  | Action                  |
| ------- | ---------------------------------------- | ----------------------- |
| 0.8–1.0 | Directly implements target functionality | Include                 |
| 0.5–0.7 | Related patterns or types                | Include                 |
| 0.2–0.4 | Tangentially related                     | Maybe                   |
| 0.0–0.2 | Not relevant                             | Exclude from next cycle |

---

## Phase 3: REFINE — Update Search Criteria

Update the query based on what you learned:

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    // Add new patterns discovered in high-relevance files
    patterns: [
      ...previousQuery.patterns,
      ...extractPatterns(evaluation), // e.g. found imports from "utils/"
    ],

    // Add terminology found in the codebase (it may differ from your assumptions)
    keywords: [
      ...previousQuery.keywords,
      ...extractKeywords(evaluation), // e.g. codebase says "throttle" not "rate-limit"
    ],

    // Exclude confirmed irrelevant paths
    excludes: [
      ...previousQuery.excludes,
      ...evaluation.filter((e) => e.relevance < 0.2).map((e) => e.path),
    ],

    // Target specific gaps identified by EVALUATE
    focusAreas: evaluation.flatMap((e) => e.missingContext).filter(unique),
  };
}
```

---

## Phase 4: LOOP — Repeat Until Sufficient (Max 3 Cycles)

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    // Check if we have sufficient context
    const highRelevance = evaluation.filter((e) => e.relevance >= 0.7);
    const noGaps = !hasCriticalGaps(evaluation);

    if (highRelevance.length >= 3 && noGaps) {
      return highRelevance; // Early exit: good enough context found
    }

    // Refine and continue
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  // Max cycles reached — proceed with best available context
  return bestContext;
}
```

**Max 3 cycles** — if you haven't found sufficient context by cycle 3, proceed with what you have. Infinite refinement loops are an anti-pattern.

---

## Practical Examples

### Example 1: Bug Fix Context

```
Task: "Fix the authentication token expiry bug"

Cycle 1:
  DISPATCH: Search "token", "auth", "expiry" in src/**
  EVALUATE: Found auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  REFINE: Add "refresh", "jwt"; exclude user.ts

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: Found session-manager.ts (0.95), jwt-utils.ts (0.85)
  STOP: Sufficient context (2+ high-relevance files, no critical gaps)

Result: auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
Token savings: ~60% vs "send everything"
```

### Example 2: Project uses Different Terminology

```
Task: "Add rate limiting to API endpoints"

Cycle 1:
  DISPATCH: Search "rate", "limit", "api" in routes/**
  EVALUATE: No matches — codebase uses "throttle" not "rate-limit"
  REFINE: Add "throttle", "middleware" keywords

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: Found throttle.ts (0.9), middleware/index.ts (0.7)
  REFINE: Need router integration patterns

Cycle 3 (max):
  DISPATCH: Search "router", "express" patterns
  EVALUATE: Found router-setup.ts (0.8)
  STOP: Max cycles reached

Result: throttle.ts, middleware/index.ts, router-setup.ts
Key insight: Cycle 1 revealed the project uses "throttle" not "rate-limit"
```

---

## Integration with Agent Orchestration

When spawning a subagent, run iterative retrieval first:

```
ORCHESTRATOR:
1. Receive task: "Implement JWT refresh token rotation"
2. Run iterative retrieval with task as context
3. Collect {auth.ts, tokens.ts, session-manager.ts}
4. Spawn subagent with:
   - Task description
   - Retrieved high-relevance files as context
   - Explicitly NOT full codebase
5. Subagent implements with focused, relevant context
```

---

## When NOT to Use This Pattern

- **Simple one-file tasks** — just pass the file directly
- **Well-defined tasks with known files** — if you already know which files, include them directly
- **Greenfield projects** — nothing to retrieve yet, just provide the spec

---

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Retrieval loop terminates early on partial match | Stop condition triggers on surface-level similarity before the needed information is fully retrieved | Tighten stop condition: require semantic completeness check, not just presence of related chunks |
| Context window fills with retrieved chunks, leaving no room for generation | Retrieval budget not capped; agent keeps retrieving until context is full | Set a hard retrieval budget (e.g. 30% of context window); prioritise highest-relevance chunks and discard the rest |
| Same chunk retrieved multiple times | Deduplication not implemented; relevance score is recalculated identically on each iteration | Track retrieved chunk IDs; exclude already-retrieved chunks from subsequent retrieval rounds |
| Retrieval quality degrades silently after embedding model update | Embeddings re-indexed with new model but cache not invalidated; old embeddings compared against new query embeddings | Version the embedding model in the index metadata; invalidate and re-index when model changes |
| Semantically similar but factually incorrect chunks returned with high confidence | Embedding similarity does not capture factual correctness; hallucinated or outdated chunks score highly | Add a re-ranking step with a cross-encoder; spot-check high-confidence retrievals against ground truth |

---

## Anti-Patterns

- Never use the same stop condition for all retrieval tasks because a condition tuned for short factual lookups will terminate prematurely on multi-step reasoning tasks that require deeper context.
- Never allow unbounded retrieval because filling the context window with chunks leaves no room for generation and the model produces truncated or incoherent output.
- Never skip deduplication because retrieving the same chunk multiple times wastes context budget and biases the generation toward over-represented content.
- Never invalidate the retrieval cache without re-indexing because stale embeddings compared against fresh query embeddings produce ranking inversions and surface irrelevant results.
- Never trust retrieval confidence scores as a proxy for factual correctness because embedding similarity measures semantic proximity, not accuracy.
- Never retrieve without logging the query and returned chunks because without a retrieval log you cannot diagnose why the agent produced an incorrect answer.

## Self-Verification Checklist

- [ ] Maximum 3 retrieval cycles enforced: cycle count = 0 overruns (never exceeds 3 even if results are ambiguous)
- [ ] Early exit triggered when >= 3 high-relevance files found with no context gaps remaining
- [ ] Terminology from cycle 1 reused: `grep -c "<project-term>" queries_cycle2.log` returns > 0 where applicable
- [ ] Context summary explicitly names retrieved files: `grep -c "Retrieved:\|Selected:" subagent_prompt.md` returns > 0
- [ ] Subagent prompt does NOT include full codebase: total file count in prompt = 0 full-repo dumps
- [ ] Broad-then-narrow strategy applied: `grep -c "cycle_1\|initial_query" retrieval.log` returns >= 1

## Success Criteria

This skill is complete when: 1) the highest-relevance files for the task are identified in at most 3 cycles, 2) the subagent prompt includes an explicit context summary of what was retrieved and why, and 3) the subagent receives only the focused, relevant context — not a dump of the full codebase.

## Best Practices

- **3 is the magic max** — never run more than 3 cycles; the diminishing returns aren't worth the extra latency
- **Early exit aggressively** — if 3+ high-relevance files with no gaps are found in cycle 1, stop
- **Surface the terminology** — cycle 1 often reveals that the project uses different names for things. Note these and use them in subsequent searches
- **Prefer broad-then-narrow** — broad initial query, then exclude confirmed irrelevance
- **Log what was found** — include a context summary in the subagent prompt: "These files were retrieved as most relevant: ..."
