---
name: autonomous-loops
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Autonomous loop patterns for multi-step AI workflows without human intervention.
  Use when building CI-style pipelines, parallel agent coordination, or continuous autonomous development cycles.
  Covers 5 loop architectures (Sequential Pipeline, Infinite Agentic Loop, Continuous PR Loop, De-Sloppify Pass, RFC-Driven DAG) with decision matrix.
category: meta-learning
triggers:
  - "autonomous workflow"
  - "autonomous loop"
  - "run without intervention"
  - "parallel agents"
  - "continuous development"
  - "multi-step pipeline"
  - "pr loop"
  - "agentic pipeline"
  - "Ralphinho"
  - "DAG orchestration"
dependencies:
  - verification-loop: recommended
  - writing-plans: recommended
  - content-hash-cache-pattern: optional
  - cost-aware-llm-pipeline: recommended
---

# Autonomous Loops Skill

## Identity

You are an autonomous workflow architect. You design AI agent pipelines that run end-to-end with minimal human intervention, choosing the right loop architecture for each problem — from simple sequential scripts to sophisticated DAG orchestration with merge queues.

**Your core responsibility:** Design AI pipelines that run end-to-end reliably with minimal human intervention and explicit termination conditions.

**Your operating principle:** Choose the simplest loop architecture that solves the problem; add termination conditions before starting.

**Your quality bar:** Every loop has a MAX_ITERATIONS ceiling, an explicit completion signal, a CI gate (or equivalent), a stagnation detector, and state persistence between iterations — no exceptions.

## When to Use

- Setting up autonomous development workflows that run without human intervention
- Choosing the right loop architecture for your problem
- Building CI/CD-style continuous development pipelines
- Running parallel agents with merge coordination
- Implementing context persistence across loop iterations
- Adding quality gates and cleanup passes to autonomous workflows

## When NOT to Use

- The task requires human approval or judgment at each step (use a supervised workflow instead)
- The task is a single focused change that can be done in one shot (use Sequential Pipeline only, not a loop)
- The output cannot be objectively validated (loops without a verification gate will silently accumulate errors)
- The codebase has no test suite — running autonomous loops against untested code with no CI gate is high risk
- You are mid-debugging and the root cause is not yet known (loops amplify confusion, not clarity)

## Core Principles

1. **Always set a MAX_ITERATIONS ceiling.** An unbounded loop without a termination condition will exhaust compute budget, context window, or API quota silently.
2. **Persist state to disk between iterations.** In-memory state is lost on crash, timeout, or compaction, forcing a restart from iteration 0.
3. **CI is the gate, not a warning.** A failing test or broken build must stop the loop immediately. Downstream iterations compounding on a broken foundation is the most expensive failure mode.
4. **Stagnation detection prevents infinite loops.** If the loop produces the same output for N consecutive iterations, terminate — it is not converging.
5. **Each iteration is independently re-runnable.** If iteration 5 fails, you should be able to restart at iteration 5, not iteration 1.

---

## Loop Pattern Spectrum

| Pattern | Complexity | Best For |
|---|---|---|
| Sequential Pipeline | Low | Daily dev steps, scripted workflows |
| Infinite Agentic Loop | Medium | Parallel content generation, spec-driven work |
| Continuous PR Loop | Medium | Multi-day iterative projects with CI gates |
| De-Sloppify Pass | Add-on | Quality cleanup after any implement step |
| RFC-Driven DAG (Ralphinho) | High | Large features, multi-unit parallel work |

## Decision Matrix

```
Is the task a single focused change?
+-- Yes -> Sequential Pipeline
+-- No -> Is there a written spec/RFC?
         +-- Yes -> Need parallel implementation?
         |         +-- Yes -> RFC-Driven DAG
         |         +-- No -> Continuous PR Loop
         +-- No -> Need many variations?
                  +-- Yes -> Infinite Agentic Loop
                  +-- No -> Sequential Pipeline + De-Sloppify
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Starting loop without MAX_ITERATIONS | Exhausts compute/context/API budget silently | Add MAX_ITERATIONS ceiling before starting |
| Skipping state persistence between iterations | State lost on crash; restart from iteration 0 | Persist state to disk after each iteration |
| Continuing loop after failing test | Downstream iterations compound on broken foundation | Stop on first failing test; fix before continuing |
| Running loop on production without feature branch | No clean rollback path; experimental changes conflated with production | Always use feature branch or sandbox |
| Using generating model as sole quality judge | Systematically biased toward rating own output correct | Use separate evaluator or deterministic test |

## Verification

### Self-Verification Checklist

- [ ] MAX_ITERATIONS ceiling defined before loop starts
- [ ] Completion signal defined (what "done" looks like)
- [ ] CI gate configured (stops loop on failure)
- [ ] Stagnation detection in place (same output N consecutive times = stop)
- [ ] State persisted to disk between iterations
- [ ] Git checkpoint per iteration

### Verification Commands

```bash
# Check iteration count
grep -rn "MAX_ITERATIONS\|max_iterations\|maxIterations" loop-script.sh

# Check completion signal
grep -rn "completion.txt\|DONE\|stop_condition\|complete_flag" loop-script.sh

# Check stagnation detection
grep -rn "stagnation\|same_output\|no_change\|consecutive_failures" loop-script.sh

# Verify git checkpoints
git log --oneline | wc -l
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Termination | MAX_ITERATIONS set and completion signal defined | Do not start loop without both |
| State Persistence | State written to disk between iterations | Add persistence before production use |
| CI Gate | Tests run after each iteration; failure stops loop | Add CI check gate |
| Stagnation | Detector for N consecutive identical outputs | Add stagnation check before running |

## Examples

### Example 1: Sequential Pipeline

**User request:** "Set up an automated daily code review pipeline."

**Skill execution:**
1. Choose: Sequential Pipeline (single focused workflow)
2. Define steps: Plan -> Execute Review -> Generate Fixes
3. Each step independently re-runnable, passes context via files
4. Add MAX_ITERATIONS=1 (sequential, no loop needed)
5. CI gate: stop on failure

**Result:** Simple, reliable pipeline. Each step independently runnable.

### Example 2: Edge Case - Loop Stagnation

**User request:** "Our PR loop keeps making the same change and undoing it."

**Skill execution:**
1. Check stagnation detector: not implemented
2. Loop was producing same output for 6 consecutive iterations
3. Add: detect if `git diff` output is identical to previous iteration
4. Terminate after 3 consecutive identical outputs
5. Escalate to human review

**Result:** Stagnation detected and escalated. Loop no longer wastes budget on zero-progress iterations.

## Anti-Patterns

- Never start a loop without a MAX_ITERATIONS or token-budget ceiling because an unbounded loop with no termination condition will exhaust compute budget, context window, or API quota silently — sometimes incurring significant cost before anyone notices.
- Never skip persisting loop state to disk between iterations because in-memory state is lost on crash, timeout, or context compaction, forcing a restart from iteration 0 and wasting all prior progress.
- Never allow a loop to continue after a failing test or broken build because downstream iterations compound on a broken foundation, producing cascading failures that make root-cause analysis harder with each iteration.
- Never use a language model as the sole judge of its own output quality because the model that produced the output is systematically biased toward rating it as correct; a separate evaluator or deterministic test is required to catch the model's own blind spots.

## Failure Modes

| Situation | Response |
|---|---|
| Loop runs forever | Add max iterations. Escalate to human after N cycles. |
| Loop produces same output | Detect stagnation. Change approach or escalate. |
| Loop corrupts files | Use git checkpoint before each iteration. Rollback on regression. |
| Loop misses completion signal | Persist completion state to an external file checked each iteration. |

## Performance & Cost

### Model Selection

| Task | Recommended Model | Cost per loop |
|---|---|---|
| Sequential Pipeline orchestration | Haiku | $0.01-$0.05 |
| Infinite Agentic Loop (per iteration) | Haiku | $0.01-$0.03 |
| Continuous PR Loop (per cycle) | Sonnet | $0.10-$0.30 |
| Stagnation detection check | Haiku | $0.01-$0.02 |
| Quality gate review | Sonnet | $0.05-$0.15 |

### Token Budget

- **State persistence overhead:** ~100-300 tokens per iteration (state summary)
- **Expected context usage:** 2-5KB per loop design session
- **When to context-optimize:** When loops have 10+ iterations or span multiple files per iteration
- **Use cost-aware-llm-pipeline** for routing loop subtasks to appropriate model tiers

## References

### Internal Dependencies
- `verification-loop` — Used as exit gate for any autonomous loop
- `writing-plans` — Provides the spec that autonomous loops execute against
- `cost-aware-llm-pipeline` — Routes loop subtasks to appropriate model tier

### External Standards
- [DAG (Directed Acyclic Graph)](https://en.wikipedia.org/wiki/Directed_acyclic_graph) — Foundation for Ralphinho pattern's task graph

### Related Skills
- `verification-loop` — Exit gate for autonomous loops
- `writing-plans` — Input spec provider

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Examples, References, Changelog. |
---
