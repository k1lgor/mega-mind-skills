---
name: eval-harness
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Automated evaluation harness for measuring agent and LLM performance, preventing regressions, and enabling eval-driven development. Covers capability evals, regression evals, pass@k metrics, LLM-as-judge patterns, cost tracking per eval run, and CI/CD integration. Use when setting up systematic quality gates for AI-assisted workflows or when you need measurable pass/fail criteria for non-deterministic outputs.
triggers:
  - "eval-harness"
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
---

# Eval Harness Skill

## Identity

You are an evaluation engineering specialist who treats evals as the "unit tests of AI development." You define expected behavior before implementation, design graders that are as reliable as the system being tested, and use quantitative metrics to make quality gates objective and automatable. You understand that LLM outputs are probabilistic — a single pass/fail is not sufficient signal, and pass@k metrics are the correct abstraction for measuring reliability. You build eval suites that cover not just the happy path but all trigger scenarios defined in the skill or feature being evaluated. You integrate evals into CI/CD so regressions are caught before merge, not after deployment.

## When to Activate

- Setting up eval-driven development (EDD) for a new AI feature or agent skill
- Defining measurable pass/fail criteria before implementation begins
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

---

## Core Principles

1. **Define before implementing**: Write the eval definition file before writing any implementation code. This is EDD's most important rule.
2. **Grader independence**: The grader must not share code or logic with the implementation. It must evaluate outputs, not re-implement them.
3. **Probabilistic correctness**: LLM outputs are samples from a distribution. Run k>=3 attempts per case. Never declare pass/fail from a single run.
4. **Cost is a first-class constraint**: Track tokens and USD per eval run. Set a budget ceiling. An eval that costs $50/run will never be run.
5. **Coverage maps to trigger scenarios**: Every "When to Activate" bullet in a skill must have a corresponding eval case. Gaps in eval coverage are gaps in quality assurance.
6. **Fail fast on regressions**: pass^k (all k attempts must pass) is the correct metric for regression evals. One failure in k means the regression gate fires.
7. **Eval results are artifacts**: Store results in `.agent/evals/<feature>.log` with timestamps. Use them to track trends, not just current state.

---

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

---

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

- Map each "When to Activate" bullet in the skill/feature to at least one eval case
- Flag any trigger scenario with no corresponding eval as "uncovered"
- Minimum target: 80% of trigger scenarios have at least one eval case

---

## Grader Types

| Grader           | Type          | Best For                                          | Reliability   |
| ---------------- | ------------- | ------------------------------------------------- | ------------- |
| **Code Grader**  | Deterministic | Assertions, return values, file side-effects      | Highest       |
| **Rule Grader**  | Pattern       | Regex matches, schema constraints, JSON structure | High          |
| **Model Grader** | LLM-as-Judge  | Subjective quality, tone, reasoning, completeness | Medium        |
| **Human Grader** | Manual        | Ambiguous outputs, final release sign-off         | Authoritative |

---

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

| Eval Type                     | Metric                   | Threshold |
| ----------------------------- | ------------------------ | --------- |
| New capability                | pass@3                   | >= 0.90   |
| Regression gate               | pass^3                   | = 1.00    |
| Critical path (auth, billing) | pass^5                   | = 1.00    |
| Subjective quality            | pass@5 with model grader | >= 0.80   |

---

## Eval Workflow

### Phase 1: DEFINE (Before Coding)

Create an eval definition at `.agent/evals/<feature>.md`:

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

### Grader Types

- Capability 1-3: Code grader (assert response shape + status code)
- Regression 1: Model grader (validate claims content semantically)
- Regression 2-3: Code grader (deterministic)

### Success Metrics

- Capability evals: pass@3 >= 0.90
- Regression evals: pass^3 = 1.00

### Cost Budget

- Max $0.10 per full eval suite run
- Use claude-haiku for grading where possible
```

### Phase 2: IMPLEMENT

Write the implementation. The eval definition is the spec.

### Phase 3: EVALUATE

Run the eval suite and record results. See pytest runner below.

### Phase 4: REPORT

```markdown
# EVAL REPORT: auth-service

Date: 2025-04-03
Model: claude-sonnet-4-5
Runs: k=3

## Capability Evals

1. Valid login returns JWT → PASS (3/3) pass@3=1.00
2. Expired JWT + refresh → PASS (3/3) pass@3=1.00
3. Revoked token returns 401 → PASS (2/3) pass@3=0.67 ← BELOW THRESHOLD

## Regression Evals

1. JWT claims correct → PASS (3/3) pass^3=1.00
2. Bcrypt cost unchanged → PASS (3/3) pass^3=1.00
3. Expiry defaults unchanged → PASS (3/3) pass^3=1.00

## Coverage

Trigger scenarios covered: 5/5 (100%)

## Cost

Total tokens: 12,450 input / 3,200 output
Total cost: $0.047

## Status: NOT READY — Capability eval #3 below threshold

Action: Investigate revoked token handling
```

---

## Pytest-Based Eval Runner

```python
# tests/evals/test_auth_eval.py
import pytest
import time
from anthropic import Anthropic
from myapp.auth import AuthService, TokenError

client = Anthropic()

# ─── Code Grader ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("run_id", range(3))  # k=3 runs
def test_valid_login_returns_jwt(run_id: int, auth_service: AuthService) -> None:
    """Capability eval: valid credentials → JWT + refresh token."""
    result = auth_service.login("alice@example.com", "correct-password")
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.expires_in == 900  # 15 minutes

@pytest.mark.parametrize("run_id", range(3))
def test_revoked_refresh_raises(run_id: int, auth_service: AuthService) -> None:
    """Capability eval: revoked refresh token → TokenError."""
    auth_service.revoke("refresh-abc-123")
    with pytest.raises(TokenError, match="revoked"):
        auth_service.refresh("refresh-abc-123")

# ─── Model Grader (LLM-as-Judge) ────────────────────────────────────────────────

JUDGE_SYSTEM_PROMPT = """
You are an evaluator for JWT token content. You will receive a decoded JWT payload
and a set of criteria. Respond with JSON: {"pass": true/false, "reason": "..."}
Do not invent criteria not listed. Be strict.
""".strip()

def llm_judge(output: str, criteria: str, model: str = "claude-haiku-3-5-20251001") -> dict:
    """LLM-as-judge grader. Returns {"pass": bool, "reason": str}."""
    response = client.messages.create(
        model=model,
        max_tokens=256,
        system=JUDGE_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Output:\n{output}\n\nCriteria:\n{criteria}"
        }]
    )
    import json
    return json.loads(response.content[0].text)

@pytest.mark.parametrize("run_id", range(3))
def test_jwt_claims_correct(run_id: int, auth_service: AuthService) -> None:
    """Regression eval: JWT contains expected claims (model grader)."""
    result = auth_service.login("alice@example.com", "correct-password")
    decoded = auth_service.decode_token(result.access_token)

    verdict = llm_judge(
        output=str(decoded),
        criteria=(
            "1. Contains 'sub' field with user email\n"
            "2. Contains 'exp' field as a Unix timestamp\n"
            "3. Contains 'iat' field as a Unix timestamp\n"
            "4. 'exp' is approximately 900 seconds after 'iat'\n"
        )
    )
    assert verdict["pass"], f"JWT claims failed: {verdict['reason']}"
```

### Fixtures

```python
# conftest.py
import pytest
from myapp.auth import AuthService
from myapp.db import create_test_db

@pytest.fixture(scope="module")
def auth_service():
    db = create_test_db()
    db.seed_user(email="alice@example.com", password="correct-password")
    svc = AuthService(db=db, secret="test-secret-key")
    yield svc
    db.teardown()
```

### Running Evals with Cost Tracking

```python
# eval_runner.py — standalone runner with cost tracking
import json
import time
from dataclasses import dataclass, field
from anthropic import Anthropic

@dataclass
class EvalResult:
    case_id: str
    run: int
    passed: bool
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    notes: str = ""

@dataclass
class EvalSuite:
    name: str
    results: list[EvalResult] = field(default_factory=list)

    def pass_at_k(self, case_id: str) -> float:
        """Fraction of runs that passed for a given case."""
        case_runs = [r for r in self.results if r.case_id == case_id]
        if not case_runs:
            return 0.0
        return sum(1 for r in case_runs if r.passed) / len(case_runs)

    def pass_all_k(self, case_id: str) -> bool:
        """True iff ALL runs for a case passed (regression gate)."""
        case_runs = [r for r in self.results if r.case_id == case_id]
        return all(r.passed for r in case_runs) if case_runs else False

    @property
    def total_cost(self) -> float:
        return sum(r.cost_usd for r in self.results)

    def report(self) -> str:
        lines = [f"# Eval Suite: {self.name}", f"Total cost: ${self.total_cost:.4f}", ""]
        for case_id in {r.case_id for r in self.results}:
            p = self.pass_at_k(case_id)
            all_pass = self.pass_all_k(case_id)
            status = "PASS" if p >= 0.9 else "FAIL"
            lines.append(f"  {case_id}: pass@k={p:.2f} pass^k={all_pass} [{status}]")
        return "\n".join(lines)
```

---

## CI/CD Integration

### GitHub Actions Step

```yaml
# .github/workflows/evals.yml
name: Eval Suite

on:
  pull_request:
    paths:
      - "src/**"
      - ".agent/skills/**"
      - "prompts/**"

jobs:
  evals:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync --extra dev
      - name: Run regression evals
        run: |
          uv run pytest tests/evals/ \
            -m "regression" \
            --tb=short \
            -q \
            --timeout=120
        env:
          EVAL_K_RUNS: "3"
          EVAL_BUDGET_USD: "0.20"
      - name: Upload eval report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: eval-report
          path: .agent/evals/*.log
```

---

## Eval Coverage Analysis

Eval coverage tracks whether all defined trigger scenarios have at least one eval case.

```python
# scripts/eval_coverage.py
import re
from pathlib import Path

def extract_trigger_scenarios(skill_path: Path) -> list[str]:
    """Extract 'When to Activate' bullets from a SKILL.md."""
    content = skill_path.read_text()
    section = re.search(r"## When to Activate\n(.*?)(?=\n##)", content, re.DOTALL)
    if not section:
        return []
    bullets = re.findall(r"^- (.+)$", section.group(1), re.MULTILINE)
    return bullets

def extract_eval_cases(eval_def_path: Path) -> list[str]:
    """Extract eval case descriptions from eval definition."""
    content = eval_def_path.read_text()
    cases = re.findall(r"^\d+\. (.+)$", content, re.MULTILINE)
    return cases

def coverage_report(skill: str) -> None:
    skill_path = Path(f".agent/skills/{skill}/SKILL.md")
    eval_path = Path(f".agent/evals/{skill}.md")

    triggers = extract_trigger_scenarios(skill_path)
    cases = extract_eval_cases(eval_path)

    print(f"Skill: {skill}")
    print(f"Trigger scenarios: {len(triggers)}")
    print(f"Eval cases: {len(cases)}")
    print(f"Coverage estimate: {min(len(cases)/len(triggers), 1.0):.0%}" if triggers else "N/A")
```

---

## Eval Artifact Layout

```
.agent/evals/
├── auth-service.md         # Definition (written before implementation)
├── auth-service.log        # Run history (appended per run, never overwritten)
└── auth-service.report.md  # Latest formatted report

docs/releases/<version>/
└── eval-summary.md         # Aggregated eval summary for release sign-off
```

---

## Self-Verification Checklist

Before declaring an eval suite complete:

- [ ] Eval definition file exists: `grep -c "## Success Criteria" .agent/evals/*.md` returns >= 1 per feature
- [ ] Every "When to Activate" trigger scenario has at least one corresponding eval case: `grep -c "^- \[ \]" .agent/evals/<feature>.md` returns >= 3
- [ ] Graders are independent of implementation: `grep -rn "from.*src\|import.*src" .agent/evals/` returns = 0 matches
- [ ] k >= 3 runs configured for all eval cases
- [ ] Regression evals use pass^k with threshold = 1.00: `grep -c "1\.00\|100%" .agent/evals/<feature>.md` returns > 0
- [ ] Cost per full suite run <= $0.20: estimated cost logged and total cost = 0 budget overruns
- [ ] CI/CD job configured: `grep -c "evals\|eval-harness" .github/workflows/*.yml` returns > 0
- [ ] Eval logs committed: `grep -c "\.log" .agent/evals/` returns >= 1 after a run

---

## Success Criteria

An eval harness task is complete when:

1. All capability evals achieve pass@3 >= 0.90 across three independent runs.
2. All regression evals achieve pass^3 = 1.00 across three independent runs.
3. Eval coverage >= 80% of trigger scenarios defined in the skill/feature spec.
4. Total cost per full eval suite run is documented and <= $0.20.
5. The GitHub Actions CI step runs and exits successfully on a passing branch.
6. `.agent/evals/<feature>.log` contains at least one complete run record with timestamps.

---

## Anti-Patterns

- Never eval against a single run because LLM outputs are samples from a probability distribution, and a single pass result has a non-trivial chance of being a lucky outlier that hides a 60% failure rate — one data point is noise, not signal for a pass/fail quality gate.
- Never share code between implementation and grader because a grader that reuses implementation logic will reproduce the same bugs it is supposed to detect, giving a false green result on exactly the cases where the implementation is wrong.
- Never tune prompts solely against eval cases because optimizing directly on the evaluation set is overfitting — the prompt will pass every eval case while failing on the production inputs that were not included, giving false confidence that the system is ready to ship.
- Never skip coverage analysis because trigger scenarios with no corresponding eval case are unguarded regression paths — a prompt or logic change can silently break a whole category of inputs that the suite never exercises, and the regression will only surface in production.
- Never use a model grader for deterministic outputs because an LLM judge introduces non-deterministic variance into a check whose correct answer is verifiable with a simple `assert`, turning a 100% reliable test into one that fails unpredictably due to grader inconsistency rather than actual regressions.
- Never ignore cost because evals that cost more than $1 per run will be skipped in developer workflows and disabled in CI under budget pressure, eliminating the quality gate entirely at the exact moments when it matters most — after a high-risk change.
- Never use flaky graders for pass^k regression gates because a model grader with inconsistent judgment fires the regression gate on runs that actually pass, causing developers to lose trust in the CI signal and start dismissing failures as "just flakiness" rather than investigating real regressions.

---

## Failure Modes

| Situation                                           | Response                                                                                                    |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| pass@k drops below threshold after prompt edit      | Do not roll back blindly. Analyze which cases regressed. Targeted fix, not revert.                          |
| Model grader gives inconsistent verdicts            | Improve the judge prompt with explicit rubric. Add few-shot examples. Move to code grader if possible.      |
| Eval suite costs exceed budget ceiling              | Switch expensive cases from Sonnet/Opus to Haiku for grading. Reduce k from 5 to 3 for non-critical cases.  |
| CI eval step fails due to API rate limit            | Add exponential backoff in the eval runner. Reduce parallelism. Cache grader calls where safe.              |
| Eval definition exists but no cases are implemented | Treat as blocking. Eval definition without runner is just documentation, not a quality gate.                |
| New feature ships with no eval definition           | File as a tech debt item immediately. Create eval definition within the same sprint.                        |
| Eval results contradict each other across runs      | Check for non-determinism in the system under test (random seeds, timestamps). Control for those variables. |

---

## Integration with Mega-Mind

`eval-harness` is invoked by:

- `verification-before-completion` as the final quality gate before marking a task complete
- `continuous-learning-v2` to extract lessons from which eval cases repeatedly fail
- `test-genius` when the task involves AI/LLM outputs that require probabilistic testing
- `skill-generator` to verify a new skill's trigger scenarios are handled correctly

`eval-harness` is upstream of:

- `continuous-learning-v2` — eval failure patterns feed the learning loop
- `finishing-a-development-branch` — the eval report is an artifact in the release checklist

`eval-harness` is downstream of:

- `writing-plans` — the plan defines what needs to be evaluated
- `executing-plans` — evals run after implementation phases
