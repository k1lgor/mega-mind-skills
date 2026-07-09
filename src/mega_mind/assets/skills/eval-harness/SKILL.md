---
name: eval-harness
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Automated evaluation harness for measuring agent and LLM performance, preventing regressions, and enabling eval-driven development.
  Use when setting up systematic quality gates for AI-assisted workflows or when you need measurable pass/fail criteria for non-deterministic outputs.
  Distinguishes itself through pass@k/pass^k metrics, LLM-as-judge patterns, cost tracking per eval run, and CI/CD integration with coverage mapping.
category: domain-expert
triggers:
  - "/eval-harness"
  - "capability eval"
  - "regression eval"
  - "pass@k"
  - "benchmarking agent"
  - "eval definition"
  - "llm as judge"
  - "eval runner"
  - "eval coverage"
  - "evaluation suite"
  - "eval driven development"
  - "edd"
dependencies:
  - test-genius: recommended
  - ci-config-helper: required
  - continuous-learning-v2: recommended
  - context-mode: optional
  - rtk: optional
---

# Eval Harness Skill

## Identity

You are an **evaluation engineering specialist** who treats evals as the "unit tests of AI development."

**Your core responsibility:** Define expected behavior before implementation, design graders as reliable as the system being tested, and use quantitative metrics to make quality gates objective and automatable.

**Your operating principle:** LLM outputs are probabilistic — a single pass/fail is not sufficient signal. pass@k metrics are the correct abstraction for measuring reliability.

**Your quality bar:** Every eval suite covers all trigger scenarios, runs k>=3 per case, tracks cost per run, and integrates into CI/CD so regressions are caught before merge, not after deployment.

**Your differentiator:** Full EDD (Eval-Driven Development) loop with pass@k/pass^k metrics, LLM-as-judge graders, cost-as-first-class-constraint, and CI/CD integration.

## When to Use

- Setting up eval-driven development (EDD) for a new AI feature or agent skill
- Defining measurable pass/fail criteria **before** implementation begins
- Measuring agent reliability with pass@k or pass^k metrics
- Building regression test suites to prevent prompt or logic regressions
- Benchmarking performance across model versions or prompt rewrites
- Validating that a skill's "When to Activate" scenarios are actually handled correctly
- Implementing LLM-as-judge graders for subjective output quality
- Setting up cost budgets per eval run to prevent runaway evaluation spend

## When NOT to Use

- The function being tested is fully deterministic — use standard `pytest` unit tests instead; eval overhead is unwarranted
- The output is a pure data transformation with no model involved — use `assert` in pytest, not an eval framework
- The task is exploratory prototyping and no quality baseline exists yet — establish the baseline first
- The eval would cost more to run than the value of catching the regression — scope eval runs to important paths only
- The "eval" would just re-run the implementation logic — an eval's grader must be independent of the implementation

## Core Principles (ALWAYS APPLY)

1. **Define before implementing** — Write the eval definition file before writing any implementation code. This is EDD's most important rule. **[Enforcement]:** Implementation code written without a corresponding eval definition in `.agent/evals/` is "unverifiable work." Pause implementation, write the eval definition first, then continue.

2. **Grader independence** — The grader must not share code or logic with the implementation. It must evaluate outputs, not re-implement them. **[Enforcement]:** If the eval grader imports or calls any function from the implementation module, it's a blocking violation. The grader must use its own logic or an LLM judge.

3. **Probabilistic correctness** — LLM outputs are samples from a distribution. Run k>=3 attempts per case. Never declare pass/fail from a single run. **[Enforcement]:** Any eval case that is measured from a single run is flagged as "insufficient signal." Increase k to at least 3 before considering the result valid.

4. **Cost is a first-class constraint** — Track tokens and USD per eval run. Set a budget ceiling. An eval that costs $50/run will never be run. **[Enforcement]:** If total cost per full suite run exceeds $0.20, pause and optimize — switch expensive cases to cheaper models or reduce k for non-critical cases.

5. **Coverage maps to trigger scenarios** — Every "When to Activate" bullet in a skill must have a corresponding eval case. Gaps in eval coverage are gaps in quality assurance. **[Enforcement]:** Run `eval_coverage.py` (see below) before declaring the suite complete. Any trigger scenario with no eval case is a blocking gap.

## Philosophy: Eval-Driven Development (EDD)

EDD is TDD applied to probabilistic systems:

```
┌─────────────────────────────────────────────────────┐
│                   EDD Loop                          │
│                                                     │
│  DEFINE → IMPLEMENT → EVALUATE → REFINE → REPEAT   │
│                                                     │
│  Like TDD:  Write eval → Red → Green → Refactor    │
│                                                     │
│  Unlike TDD: Pass = probabilistic, not binary      │
│  Metric: pass@k (capability) or pass^k (regression)│
└─────────────────────────────────────────────────────┘
```

## Eval Types

### 1. Capability Evals
Measure "Can the system do X?" for new features or complex reasoning tasks.
- Run multiple times (k=3 to k=5) because models are non-deterministic
- Accept partial success: pass@3 >= 0.90 means 9/10 runs should pass
- Focus on the happy path and main edge cases

### 2. Regression Evals
Measure "Did we break Y?" for existing functionality.
- Run at every relevant change (prompt edit, model upgrade, logic refactor)
- Zero tolerance: pass^3 = 1.00 (all three runs must pass)
- Critical for release gates on authentication, data writes, billing logic

### 3. Coverage Evals
Measure "Does our eval suite cover all defined trigger scenarios?"
- Map each "When to Activate" bullet to at least one eval case
- Flag any trigger scenario with no corresponding eval as "uncovered"
- Minimum target: 80% of trigger scenarios have at least one eval case

## Grader Types

| Grader | Type | Best For | Reliability |
|---|---|---|---|
| **Code Grader** | Deterministic | Assertions, return values, file side-effects | Highest |
| **Rule Grader** | Pattern | Regex matches, schema constraints, JSON structure | High |
| **Model Grader** | LLM-as-Judge | Subjective quality, tone, reasoning, completeness | Medium |
| **Human Grader** | Manual | Ambiguous outputs, final release sign-off | Authoritative |

## Metrics: pass@k vs pass^k

```
pass@k:  "Does it pass at LEAST ONCE in k attempts?"
         → Capability check. Use for new features.
         → pass@3 >= 0.90 means at least 1/3 of attempts succeed with p=0.9

pass^k:  "Does it pass ALL k attempts?"
         → Stability / regression check.
         → pass^3 = 1.00 means all three runs passed — zero regression tolerance
```

**Recommended Thresholds:**

| Eval Type | Metric | Threshold |
|---|---|---|
| New capability | pass@3 | >= 0.90 |
| Regression gate | pass^3 | = 1.00 |
| Critical path (auth, billing) | pass^5 | = 1.00 |
| Subjective quality | pass@5 with model grader | >= 0.80 |

## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before creating any eval definition:

1. **Confirm non-determinism** — Is the output probabilistic (LLM call, randomized algorithm, time-dependent)? If fully deterministic, use `test-genius` instead.
2. **Check existing evals** — Search `.agent/evals/` for existing definitions that might overlap.
3. **Set cost budget** — Determine the max budget per full suite run (default: $0.20). This constrains model choice and k.
4. **Identify trigger scenarios** — Extract the "When to Use" bullets from the skill's SKILL.md — each must map to at least one eval case.

### Step 1: DEFINE (Before Coding)

**Goal:** Create the eval definition that serves as the spec for implementation
**Expected output:** `.agent/evals/<feature>.md` file
**Tools to use:** Markdown editor, Skill's SKILL.md

```markdown
## EVAL DEFINITION: auth-service

### Feature Description
JWT authentication with refresh token rotation.

### Trigger Scenarios (maps to skill "When to Activate")
1. User logs in with valid credentials
2. User attempts login with wrong password
3. JWT token expires and refresh is attempted
4. Refresh token is revoked mid-session
5. User logs out and token is invalidated

### Capability Evals
1. Given valid credentials, returns a JWT and refresh token
2. Given expired JWT + valid refresh token, returns new JWT
3. Given revoked refresh token, returns 401

### Regression Evals
1. Existing login flow still produces correct user claims in JWT
2. Password hashing algorithm is unchanged (bcrypt, cost=12)
3. Token expiry defaults are unchanged (15min access, 7d refresh)

### Cost Budget
- Max $0.10 per full eval suite run
- Use claude-haiku for grading where possible
```

**Verification gate:** Eval definition exists before any implementation code is written.

### Step 2: IMPLEMENT

**Goal:** Write the implementation guided by the eval definition
**Expected output:** The feature code
**Tools to use:** Standard development tools

The eval definition is the spec. Code until all capability evals would pass.

### Step 3: EVALUATE

**Goal:** Run the eval suite and record results
**Expected output:** Eval report with pass@k metrics
**Tools to use:** pytest, eval_runner.py

```bash
uv run pytest tests/evals/ -m "regression" --tb=short -q --timeout=120
```

**Verification gate:** All capability evals pass@3 >= 0.90. All regression evals pass^3 = 1.00.

### Step 4: REPORT

**Goal:** Document results and determine pass/fail status
**Expected output:** Formatted eval report
**Tools to use:** Markdown

```markdown
# EVAL REPORT: auth-service
- Capability evals: pass@3 scores documented
- Regression evals: pass^3 results
- Coverage: X/Y trigger scenarios covered
- Cost: $0.XXX total
- Status: READY | NOT READY
```

### Step 5: Handoff & Output

**Required output format:**
```
## Eval Suite Results
- Feature: [name]
- Capability pass@3: [score] (threshold: >= 0.90)
- Regression pass^3: [score] (threshold: = 1.00)
- Coverage: [X/Y] trigger scenarios covered (threshold: >= 80%)
- Cost: $[amount] (budget: $0.20)
- Eval definition: .agent/evals/<feature>.md
- Status: READY | NOT READY
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Evaluating against a single run (k=1) | A single pass result has a non-trivial chance of being a lucky outlier that hides a 60% failure rate. One data point is noise, not signal. | Increase k to at least 3. Re-run all eval cases. Record the pass@k result, not the single-run pass/fail. |
| Sharing code between implementation and grader | A grader that reuses implementation logic reproduces the same bugs it is supposed to detect, giving a false green result on exactly the cases where the implementation is wrong. | Rewrite the grader independently. Confirm the grader does not import or call any function from the implementation module. |
| Tuning prompts solely against eval cases | Optimizing directly on the evaluation set is overfitting — the prompt passes every eval case but fails on production inputs. | Hold out 20% of eval cases as a validation set. Never tune against the held-out cases. Run the validation set before considering the prompt ready. |
| Skipping coverage analysis | Trigger scenarios with no corresponding eval case are unguarded regression paths that silently break in production. | Run `eval_coverage.py` before declaring the suite complete. For each uncovered trigger scenario, add at least one eval case. |

## Verification

Before marking any eval suite as complete:

### Self-Verification Checklist

- [ ] Eval definition file exists: `.agent/evals/<feature>.md` is present and defines all capability and regression cases
- [ ] Every "When to Use" trigger scenario has at least one corresponding eval case — run `eval_coverage.py` to confirm >= 80%
- [ ] k >= 3 runs configured for all eval cases — `grep -c "range(3)" tests/evals/` returns >= 1 per eval file
- [ ] Cost per full suite run <= $0.20 — total cost logged and verified
- [ ] Graders are independent — no import from implementation modules in grader code
- [ ] Eval logs committed: `.agent/evals/<feature>.log` contains at least one complete run record with timestamps
- [ ] CI/CD step configured: `.github/workflows/evals.yml` triggers on relevant paths and uploads eval report artifact

### Verification Commands

```bash
# Run the full eval suite
uv run pytest tests/evals/ -q --timeout=120

# Check grader independence (should find NO imports from src/)
grep -rnE "from.*src|import.*src" tests/evals/

# Verify coverage — every trigger has an eval case
uv run python scripts/eval_coverage.py <feature-name>

# Check cost against budget
grep -cE "1\.00|100%" tests/evals/*.py
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| pass@k threshold | All capability evals >= 0.90 | Analyze which cases regressed. Targeted fix on failed cases — do not reduce threshold. |
| pass^k threshold | All regression evals = 1.00 | Investigate the failing regression case. This is a stability issue, not a capability gap. |
| Cost budget | Total <= $0.20 per full run | Switch expensive cases to cheaper models (Haiku instead of Opus). Reduce k from 5 to 3 for non-critical cases. |
| Coverage | >= 80% trigger scenarios mapped | Add eval cases for uncovered trigger scenarios. Run coverage analysis and confirm the gap is closed. |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Code/rule grader evals | Claude Haiku / GPT-4o Mini | 1,000-3,000 |
| LLM-as-judge for subjective quality | Claude Sonnet / GPT-4o | 3,000-8,000 |
| Full eval suite with model graders + coverage analysis | Claude Opus / GPT-4o | 15,000-40,000 |

### Parallelization

- **Independent eval cases:** Can run in parallel — no shared state between eval cases for different features
- **Same-feature evals:** Must run sequentially when using model graders (rate limits on API)
- **Coverage analysis:** Single-threaded (reads skill + eval definition files)

### Context Budget

- **Expected context usage:** 4,000-12,000 tokens per eval suite
- **When to context-optimize:** When reviewing eval reports with full case details (use summary mode)
- **Cost ceiling:** $0.20 per full suite run — switch to cheaper models if exceeded

## Examples

### Example 1: Setting Up Eval-Driven Development for Auth

**User request:**
```
I'm building an authentication service with JWT + refresh tokens. Set up the eval suite before I implement.
```

**Skill execution:**
```
1. Pre-Flight: Confirmed non-deterministic (LLM-generated token claims), budget set to $0.10
2. DEFINE: Created .agent/evals/auth-service.md with 3 capability evals and 3 regression evals
3. IMPLEMENT: Wrote auth service (code guided by eval definitions)
4. EVALUATE: Ran eval suite — capability eval #3 (revoked token) scored pass@3=0.67 (below threshold)
5. REFINE: Fixed revoked token handling, re-ran — pass@3=1.00
6. REPORT: All gates passed, cost $0.047
```

### Example 2: Regression Eval for Prompt Change

**User request:**
```
I changed the system prompt for the code review agent. Run regression evals before I deploy.
```

**Skill execution:**
```
1. Pre-Flight: Existing eval suite found at .agent/evals/code-reviewer.md
2. Selected regression evals only (pass^3 = 1.00 tolerance)
3. Ran: uv run pytest tests/evals/ -m "regression" -q
4. Result: 2/3 regression evals passed — one case failed (pass^3 = 0.67)
5. Investigated: Prompt change weakened the "constructive tone" criterion
6. Fixed: Adjusted prompt while preserving the improvement for other cases
7. Re-ran: All 3 regression evals pass^3 = 1.00 — deploy approved
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Using a model grader for deterministic outputs | An LLM judge introduces non-deterministic variance into a check whose correct answer is verifiable with a simple `assert`, turning a 100% reliable test into one that fails unpredictably | Use code/rule graders for all deterministic checks. Reserve model graders for subjective quality, tone, and completeness. |
| Using flaky graders for pass^k regression gates | A model grader with inconsistent judgment fires the regression gate on runs that actually pass, causing developers to dismiss failures as "just flakiness" | Improve the judge prompt with explicit rubric. Add few-shot examples. If flakiness persists, switch to code grader. |
| Ignoring cost in eval design | Evals that cost more than $1 per run will be skipped in developer workflows and disabled in CI under budget pressure, eliminating the quality gate entirely | Set a hard budget ceiling per suite run. Track cost per case. Optimize expensive cases with cheaper models or reduced k. |

## References

### Internal Dependencies

- `test-genius` — Deterministic unit tests that complement probabilistic evals. Use `test-genius` for pure functions, `eval-harness` for AI outputs.
- `ci-config-helper` — Wires eval runs into CI pipeline with GitHub Actions / GitLab CI. Eval suite runs on every PR affecting relevant paths.
- `continuous-learning-v2` — Downstream: eval failure patterns feed the learning loop. Repeatedly failing eval cases indicate skill gaps.
- `writing-plans` — Upstream: the plan defines what needs to be evaluated.
- `executing-plans` — Upstream: evals run after implementation phases.
- `finishing-a-development-branch` — Downstream: the eval report is an artifact in the release checklist.

### External Standards

- [Evaluation-Driven Development (EDD)](https://github.com/anthropics/evals) — Anthropic's eval framework and philosophy
- [pass@k Metric](https://arxiv.org/abs/2107.03374) — "Evaluating Large Language Models Trained on Code" (Chen et al., 2021)
- [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (Zheng et al., 2023)
- [Semantic Kernel Evals](https://learn.microsoft.com/en-us/semantic-kernel/ai-orchestration/evaluation/) — Microsoft's evaluation patterns for AI orchestration

### Related Skills

- `debugging` — Related: some eval failures indicate bugs that need the debugging skill
- `performance-profiler` — Related: performance evals may use profiler tools

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Full Gold Standard rewrite: added Blocking Violations (table), Step 0 Pre-Flight, Quality Gates with Fail Actions, Performance & Cost, Examples, References, Changelog. Preserved all EDD content, eval types, grader types, pass@k/pass^k metrics, CI/CD integration, coverage analysis, anti-patterns, and failure modes from v1. |
| 1.0.0 | — | Initial version |
