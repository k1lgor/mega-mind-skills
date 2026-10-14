# Routing Regression Fixtures (prompt level)

Manual, prompt-level tests for the Mega-Mind routing layer.

The validator (`scripts/validate-skill-system.py`) covers the **deterministic** half of
routing: phrase uniqueness, target resolution, chain integrity, coverage. These fixtures
cover the half only an agent can judge — picking a route from a real sentence, and
honouring `When NOT to Use` redirects.

## How to run

Give the prompt to a fresh agent that has the routing matrix (either
`.agent/shared/routing.json` or the generated matrix inside
`.agent/skills/mega-mind/SKILL.md`) and **nothing else from this file**. Score three things:
did it reach `expected`, did it honour the redirect, did it avoid the failure mode.

Runs are LLM-judged, so treat results as a regression signal, not a CI gate. The
deterministic checks live in `scripts/validate-skill-system.py` and run in CI.

## Cases

| # | Prompt | Expected route | Also required | Guards against |
| --- | --- | --- | --- | --- |
| 1 | "fix this bug — login fails after password reset, the token seems expired" | `debugging` | `When NOT to Use` does not fire (it is a real defect, not a feature request) | bug vs feature confusion |
| 2 | "write tests: I need unit tests for the config parser before we ship" | `test-genius` | the tie-break is stated explicitly | `write tests` vs `unit tests` tie |
| 3 | "review my code before I open the PR" | `code-reviewer` — an **agent**, not a skill | the layer is stated | skill/agent boundary |
| 4 | "before we build any linting hooks — does this project even need linting?" | `plankton-code-quality` → **redirect** → `code-polisher` | the redirect target does not bounce back | `When NOT to Use` re-routing |
| 5 | "our k8s pods are crashlooping again and I think it is the database connection pool" | `debugging` first (unknown root cause), then `k8s-orchestrator` | the fallback path is stated (`CLASSIFY`, no matrix phrase matches) | ambiguous no-phrase fallback |
| 6 | "design and build a new CSV export feature end-to-end, tests included, then get it ready to ship" | Feature Development chain (Z-Pattern) | step 0 `search-first` gate, and commit gate `finishing-a-development-branch` | chain drift |

## Scoring

- **PASS** — reached `expected` and stated why in one sentence.
- **AMBIGUOUS** — reached a defensible neighbour route and named the competing rule.
- **FAIL** — no route, wrong layer (skill vs agent), or an ignored `When NOT to Use` redirect.

## Known-ambiguous cases

- **Case 2** contains both `write tests` and `unit tests`. Rule since mega-mind **2.1.2**:
  a named test type beats the generic phrase → `test-genius`.
- **Case 5** matches no matrix phrase. Rule since mega-mind **2.1.2**: a failing behaviour
  with an unknown root cause goes to `debugging` first and the platform skill takes over
  once the cause is known. Answering `k8s-orchestrator` is acceptable **only** if the
  agent states the debugging handoff.

## Full-coverage run (all 53 skills)

Method: one realistic prompt per skill (expectation = that skill), routing data supplied inline
(routing matrix + agent routes + frontmatter-trigger hints for the six skills that have no
matrix phrase), prompts split across three batched agents, scored centrally by prompt number.

Result (2026-10-14, mega-mind 2.1.2): **53/53 routed as expected** — including the six
trigger-only skills (`brainstorming`, `writing-plans`, `finishing-a-development-branch`,
`rtk`, `content-hash-cache-pattern`, `mega-mind`).

Caveats, so the number is not over-read: prompts inside one batch share a single context
(anchoring risk), the routing agents are the same model family as this fixture's author, and
the expectations are derived from the routing data itself. This measures internal
consistency of the routing surface, not external ground truth. Deterministic guarantees stay
with `scripts/validate-skill-system.py`.

## Final suite (64 targets x 3 prompts)

Method: every skill (53) and every agent persona (11) tested **individually** with three distinct
phrasings per target (the exact matrix phrase, a natural paraphrase, a real-world sentence) — 192
evaluations, no multi-skill prompts. Routing matrix, agent routes, rosters and trigger hints supplied
inline; prompts split across four batched agents (16 targets each); scored centrally by prompt number.

Result (2026-10-14, mega-mind 2.1.3, 57 routes): **192/192 routed as expected, 64/64 targets at 3/3.**
This includes the agent/skill name collisions, which resolve correctly: `act as tech lead` reaches the
**agent** while `design system` reaches the **skill**; likewise `security reviewer` (agent) vs
`security audit` (skill).

Caveats unchanged from the full-coverage run above: prompts in one block share a context, the routing
agents are the same model family as this fixture's author, and expectations derive from the routing
data itself — a consistency measurement, not external ground truth.

## Recording results

Append one row per release run:

| Date | mega-mind version | Passed | Ambiguous | Failed | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | 2.1.1 | 4 | 2 (cases 2, 5) | 0 | Baseline run; cases 2 and 5 drove the 2.1.2 precedence rules |
| 2026-10-14 | 2.1.2 | 53 | 0 | 0 | Full-coverage run: one prompt per skill, 3 batched agents, every skill routed to its expected owner |
| 2026-10-14 | 2.1.3 | 192 | 0 | 0 | Final suite: all 53 skills + 11 agents, 3 phrasings each, 4 batched agents, every target 3/3 |
