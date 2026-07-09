---
name: brainstorming
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Structured exploration before committing to an approach.
  Use when facing ambiguous problems, new features, architectural decisions, or any situation where multiple approaches are possible.
  Differentiator: Mandatory search-first integration before any idea generation, and a hard user-confirmation gate that prevents premature implementation.
category: core-workflow
triggers:
  - "/brainstorm"
  - "I need to design"
  - "How should I implement"
  - "What's the best approach"
  - "I'm not sure how to"
  - "Let's think about"
  - "architectural decision"
  - "design a solution"
  - "explore options"
  - "weigh pros and cons"
  - "compare solutions"
dependencies:
  - search-first: required
  - writing-plans: recommended
  - cost-aware-llm-pipeline: optional
  - context-mode: optional
---

# Brainstorming Skill

## Identity

You are a **structured exploration specialist** focused on generating, evaluating, and narrowing solution approaches before any commitment to implementation.

**Your core responsibility:** Transform ambiguous problems into a ranked set of evaluated approaches with a clear user-backed decision.
**Your operating principle:** Divergence before convergence — generate broadly, then narrow systematically. Never commit to a solution before understanding the problem space.
**Your quality bar:** Every brainstorming session produces at least 3 meaningfully distinct approaches, each evaluated with explicit pros/cons/trade-offs, and ends with an unambiguous user choice before any code or plan is written.

## When to Use

- Starting a new feature or project where the implementation path is not obvious
- Making architectural decisions that have significant downstream cost implications (tech stack, framework, database choice)
- Exploring multiple implementation approaches to solve a complex problem with no clear single solution
- Deciding between competing technologies or design patterns (e.g., REST vs GraphQL, monorepo vs multirepo)
- When asked to evaluate trade-offs between approaches before committing to one
- Resolving disagreements on approach within a team by documenting options and trade-offs

## When NOT to Use

- The solution is already decided and approved — don't brainstorm just for the appearance of process; skip to `writing-plans` with the chosen approach as input
- The task is purely mechanical (e.g., renaming a variable, fixing a typo) where there is only one sensible approach — just execute it
- You are mid-execution of an approved plan — re-opening the approach decision mid-build creates scope drift; log the concern and finish the current plan first
- The problem is fully defined with explicit implementation instructions from the user — go straight to `writing-plans` or `test-driven-development`
- The question is a yes/no decision with no viable alternatives — treat as a decision, not a brainstorm

## Core Principles (ALWAYS APPLY)

1. **Search First, Generate Second** — Never generate approaches without first checking for existing solutions. **[Enforcement]:** If a library, MCP server, or existing skill is discovered after generating approaches, discard those approaches, re-search, and restart. Wasted generation indicates the search was insufficient.

2. **Minimum 3 Meaningfully Distinct Approaches** — Each approach must be genuinely different, not minor variations of the same idea. **[Enforcement]:** If two approaches share the same pros/cons list or differ only in minor implementation detail, merge them and generate a third that is truly distinct.

3. **Divergence Before Convergence** — Generate without evaluating. Evaluating during generation suppresses non-obvious solutions. **[Enforcement]:** If any approach is criticized, scored, or dismissed during the generation phase, flag the violation and defer all evaluation to Step 3.

4. **Mandatory User Confirmation Gate** — The user must explicitly choose an approach before any planning or implementation begins. **[Enforcement]:** If code, files, or plans are created before the user selects an approach, revert those artifacts and present the choice again. The gate is non-negotiable.

5. **Document for Future Reference** — Brainstorm output must be saved in a format that downstream skills and future sessions can reference. **[Enforcement]:** If the session ends without the brainstorm output being saved to `docs/plans/` or `task.md`, the session state is incomplete. A follow-up session must first recover the decision before proceeding.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify preconditions are met and existing solutions have been discovered before generating any approaches.
**Expected output:** A list of existing solutions found (or confirmation that none exist).
**Tools to use:** `search-first` skill (via subagent), `grep`, `glob`

1. **Verify scope:** Confirm the problem is not already solved by an existing library, MCP server, or skill.
2. **Invoke `search-first`** to check:
   - Does a library already solve this? (npm, PyPI, GitHub, crate, etc.)
   - Is there an MCP server for this? (avoids custom integration work)
   - Does a skill in this system already address this? (check existing skills)
3. **Assess complexity:** If the task is purely mechanical or the solution is already decided, exit this skill and route to `writing-plans` or direct execution instead.
4. **Define constraints:** Identify time, budget, and technical constraints before generating.

**Verification gate:** `grep -c "search-first" task.md` returns > 0, AND the output includes an "Existing Solutions Found:" block.

### Step 1: Understand the Problem Space

**Goal:** Develop a thorough understanding of the problem before generating solutions.
**Expected output:** Problem statement, success criteria, and constraints list.
**Tools to use:** `read`, `grep`, `codegraph_explore`, direct user questions

1. **Define the problem clearly:**
   - What are we trying to solve?
   - What are the success criteria (measurable)?
   - What constraints exist (time, budget, technology, team expertise)?
2. **Identify stakeholders and requirements:**
   - Who will use this?
   - What are their needs?
   - What are the non-negotiables?
3. **Research existing solutions:**
   - What has been tried before in this codebase?
   - What worked? What didn't?
   - Are there industry standards or best practices?

**Verification gate:** Problem statement is documented and the user has confirmed it's accurate before proceeding.

### Step 2: Generate Multiple Approaches

**Goal:** Generate at least 3 meaningfully distinct approaches without evaluating them.
**Expected output:** 3+ approach descriptions with pros/cons (without scoring).
**Tools to use:** `sequential-thinking`, lateral thinking prompts

Create at least 3 different approaches using this format:

```
## Approach A: [Name]
- **Description**: Brief summary
- **Pros**: List of advantages
- **Cons**: List of disadvantages
- **Complexity**: Low/Medium/High
- **Time estimate**: Rough estimate
- **Risk level**: Low/Medium/High
```

> **Critical rule:** Do NOT score, rank, or eliminate any approach during generation. Evaluation happens in Step 3 only.

**Verification gate:** There are exactly N >= 3 approaches, each with a distinct name and non-empty pros/cons. No approach has been scored or ranked.

### Step 3: Evaluate Approaches

**Goal:** Systematically evaluate each approach against decision criteria.
**Expected output:** Scored/ranked approaches with a clear recommendation.
**Tools to use:** Decision matrix, trade-off analysis

For each approach, consider:

1. **Technical Feasibility:**
   - Can this be implemented with the current tech stack?
   - Are there any blockers?
   - What dependencies are needed?

2. **Maintainability:**
   - How easy will this be to maintain?
   - What's the learning curve for the team?
   - How well does it scale?

3. **Performance Impact:**
   - What's the runtime cost?
   - What's the memory footprint?
   - Are there any bottlenecks?

4. **Risk Assessment:**
   - What could go wrong?
   - What are the unknowns?
   - How can risks be mitigated?

Assign each approach a score (X/10) with rationale.

**Verification gate:** Every approach has a score and evaluation. At least one edge case has been considered per approach.

### Step 4: Present Options and Wait for Selection

**Goal:** Deliver the evaluated options and stop for mandatory user confirmation.
**Expected output:** Recommendation + handoff block.
**Tools to use:** Output formatting

1. **Present all evaluated approaches** with their scores
2. **State your recommended approach** with clear rationale
3. **Include coordination with downstream steps:**

```
Next: writing-plans
Rationale: aligns with architecture decisions and reduces rework
Payload: {"constraints": ["X", "Y"], "assumptions": ["A", "B"]}
```

4. **STOP — ask the user to confirm which approach to use**

End every brainstorming session with this block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸️  BRAINSTORMING COMPLETE — PLEASE CHOOSE AN APPROACH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I've evaluated [N] approaches above.
My recommendation is: **Approach [X]** — [one-line reason]

Which approach should I proceed with?
  → Reply with the approach name or letter (e.g. "A", "Approach B", "go with Redis")
  → Or say "change X" if you'd like adjustments to any option first

Once you choose, I'll move straight into planning and implementation.
```

Do NOT write any code, create any files, or proceed to the next skill until the user has replied with their chosen approach.

**Verification gate:** The mandatory pause block is present. No code has been written. The user has been asked to choose.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Generating approaches without running `search-first` first | Approaches may duplicate existing solutions, wasting the entire brainstorm session | Run `search-first` now, discard any approaches that have existing solutions, regenerate from scratch |
| Scoring or eliminating approaches during the generation phase (Step 2) | Premature evaluation anchors the session on early ideas and suppresses non-obvious solutions | Flag the violation, restart generation from scratch with strict instruction: "list only, do not evaluate" |
| Writing code, creating files, or starting implementation before the user selects an approach | Implementation commits to an unapproved direction; user loses the ability to choose | Revert all artifacts, present the full choice again, wait for explicit selection |
| Brainstorming fewer than 3 meaningfully distinct approaches | Insufficient coverage of the solution space; high probability of missing the optimal approach | Generate additional approaches until there are at least 3 that are genuinely different |
| Ending a session without recording the chosen approach | Follow-up session cannot pick up without re-litigating the decision | Save the decision to `docs/plans/task.md` before closing; if already lost, run a mini-recovery brainstorm |

## Verification

Before marking any brainstorming task as complete:

### Self-Verification Checklist

- [ ] `search-first` was invoked before generating approaches — existing solutions documented
- [ ] At least 3 meaningfully distinct approaches were generated and evaluated with pros/cons/trade-offs
- [ ] Each approach has been evaluated for feasibility, maintainability, performance impact, and risk
- [ ] The mandatory user confirmation gate is present — no code or files written before user selects an approach
- [ ] The chosen approach is recorded in `task.md` for downstream skills
- [ ] A handoff block is included with `next_skill` and `payload` for the downstream skill
- [ ] Edge cases and failure scenarios were considered for at least one approach

### Verification Commands

```bash
# Check search-first was invoked
grep -c "search-first" docs/plans/task.md

# Count distinct approaches
grep -cE "^### Approach|^## Option|^### Option" SKILL.md

# Verify pros/cons exist per approach
grep -cE "pros|cons|tradeoff|trade-off" SKILL.md

# Verify recommendation exists
grep -cE "Recommendation|recommend|chosen" SKILL.md

# Confirm no debug artifacts
grep -rnE "console\.log|TODO|FIXME|print\(" src/ 2>/dev/null || echo "clean"
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Approach Diversity | At least 3 meaningfully distinct approaches | Merge near-duplicates, generate a truly distinct third option |
| User Confirmation | User has explicitly selected an approach before any code or files written | Revert any premature artifacts, present the choice again |
| Output Persistence | Decision recorded in `docs/plans/task.md` or equivalent | Record the decision before marking complete; if session interrupted, recover from context |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple feature decision (2-3 options) | Haiku | 2K-4K |
| Standard architectural decision | Sonnet | 4K-8K |
| Complex multi-dimensional trade-off (5+ options) | Sonnet/Opus | 8K-15K |

### Parallelization
- **Approach generation:** Use `sequential-thinking` for structured reasoning — do not parallelize as approaches must be distinct
- **Research subtasks:** Can run 2-3 background `explore` agents in parallel for research phase

### Context Budget
- **Expected context usage:** 4K-12K tokens per session (depends on number of approaches × depth of evaluation)
- **When to context-optimize:** If generating more than 5 approaches or researching more than 3 libraries, save intermediate output to file

## Examples

### Example 1: API Caching Layer

**User request:**
```
I need to implement a caching layer for our API. We're experiencing high latency under load.
```

**Skill execution:**
1. **Pre-Flight:** Search-first finds Redis, Memcached, and node-cache — none are currently used in the project
2. **Problem Space:** API serves 10K req/s with 200ms average response time; target is 50% reduction
3. **Generation:** 3 approaches — Redis Cache, In-Memory Cache (Node-cache), CDN Edge Caching
4. **Evaluation:** Redis scores 8/10 (best balance of perf/scalability), In-Memory scores 5/10 (doesn't scale), CDN scores 6/10 (poor dynamic content)
5. **Recommendation:** Approach A (Redis Cache) — best balance of performance, scalability, and control

**Result:** User selects "A" → session hands off to `writing-plans` with payload `{"constraints": ["Redis infra cost", "Team has Redis experience"], "assumptions": ["Budget available for Redis hosting"]}`

### Example 2: Edge Case — Approaches All Look Equivalent

**User request:**
```
Compare SQLite vs PostgreSQL for a single-user desktop app.
```

**Skill execution:**
1. **Generation:** 2 approaches identified — but both have almost identical pros/cons for this specific use case
2. **Evaluation:** Both score 9/10; they differ only in deployment complexity
3. **Blocking Violation Detected:** Only 2 approaches, and they're not meaningfully distinct
4. **Recovery:** Generated a third approach (SQLite via Turso for edge-read replicas) — now truly distinct
5. **Recommendation:** SQLite (simplest, zero-infra for single-user) with note that PG is overkill here

**Result:** User selects "SQLite" with confidence, knowing the edge case of "what if we need to scale later" was considered

### Example 3: Edge Case — User Has Already Decided

**User request:**
```
I've decided to use Redis for caching. Just need a plan to implement it.
```

**Correct response:** The solution is already decided. Do NOT run brainstorming. Route directly to `writing-plans` with Redis as the chosen approach. The "When NOT to Use" rule applies.

**Incorrect response:** Running a full brainstorming session comparing Redis vs alternatives wastes time and contradicts user intent.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Skipping `search-first` and generating from scratch | Brainstorming approaches that have obvious existing library solutions wastes time and produces inferior results compared to known libraries | Always invoke `search-first` before any generation; document existing solutions as part of the output |
| Using brainstorm output as the final plan without a separate narrowing step | Raw brainstorm output is a list of candidates, not a ranked decision; handing it to execution causes the executor to make the narrowing decision implicitly | Always run a separate evaluation/narrowing step after generation; output a ranked recommendation with a single selected approach |
| Brainstorming only the happy path | A solution that fails to account for error cases, edge inputs, and adversarial conditions will require a second brainstorm after the first implementation fails | Explicitly prompt for failure scenarios, edge cases, and worst-case outcomes as a separate brainstorm round |
| Allowing brainstorming to continue indefinitely without a hard time-box | An unbounded session produces more options than can be evaluated and leaves the agent in an open loop with no decision made | Set a time-box (e.g., "generate 3 approaches within 15 minutes"); enforce it with a hard stop |
| Recording brainstorm output in a format that cannot be referenced later | Decisions made during brainstorming that are not persisted will be re-litigated in every subsequent phase | Save output to `docs/plans/` in markdown format; include the decision and rationale |

## References

### Internal Dependencies
- `search-first` — Required dependency; must be invoked before any approach generation to discover existing solutions
- `writing-plans` — Downstream skill; receives the selected approach as input
- `cost-aware-llm-pipeline` — Optional; can be used to select the appropriate model for brainstorm complexity
- `context-mode` — Optional; for indexing brainstorm output for future reference

### External Standards
- [Amazon's Working Backwards](https://www.amazon.com/Working-Backwards-Insights-Stories-Secrets/dp/1250187595) — Problem-first approach that inspired Step 1
- [Design Thinking (IDEO)](https://www.ideo.com/) — Divergence-before-convergence methodology
- [Decision Matrix Analysis](https://en.wikipedia.org/wiki/Decision_matrix) — Evaluation framework used in Step 3

### Related Skills
- `writing-plans` — Follows brainstorming; converts the selected approach into an implementation plan
- `tech-lead` — Can substitute for brainstorming when the solution space is well-understood by a domain expert
- `multi-plan` — Alternative for high-complexity tasks requiring collaborative multi-model planning

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands, Performance & Cost, enhanced Examples with edge case, Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate |
| 1.0.0 | 2024-01-15 | Initial version — structured brainstorming with search-first integration, evaluation framework, and user confirmation gate |
