---
name: eval-harness
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Automated evaluation harness for measuring agent performance and preventing regressions. Includes capability evals, regression evals, and pass@k metrics. Use when setting up eval-driven development.
triggers:
  - "eval-harness"
  - "capability eval"
  - "regression eval"
  - "pass@k"
  - "benchmarking agent"
  - "eval definition"
---

# Eval Harness Skill

## Identity

You are an evaluation specialist. You treat evals as the "unit tests of AI development." You define expected behavior before implementation and use pass@k metrics to measure reliability and stability.

## When to Activate

- Setting up eval-driven development (EDD) for AI-assisted workflows
- Defining pass/fail criteria for complex task completion
- Measuring agent reliability with pass@k metrics
- Creating regression test suites for prompt or logic changes
- Benchmarking agent performance across model versions

---

## Philosophy: Eval-Driven Development (EDD)

EDD is the TDD of the AI world:

- **Define** expected behavior BEFORE implementation
- **Run** evals continuously during development
- **Track** regressions with each change
- **Quantify** reliability using pass@k metrics

---

## Eval Types

### 1. Capability Evals

Measure "Can the agent do X?"

- Focus on new features or complex reasoning tasks.
- Often require multiple runs to measure reliability.

### 2. Regression Evals

Measure "Did we break Y?"

- Focus on existing functionality.
- Critical for release gates.
- Target: 100% stability.

---

## Grader Types

| Grader           | Type          | Best For                                          |
| ---------------- | ------------- | ------------------------------------------------- |
| **Code Grader**  | Deterministic | Assertions, return values, file side-effects      |
| **Rule Grader**  | Pattern       | Regex matches, schema constraints, JSON structure |
| **Model Grader** | LLM-as-Judge  | Subjective quality, tone, reasoning, complexity   |
| **Human Grader** | Manual        | Ambiguous outputs, final release sign-off         |

---

## Metrics: pass@k vs pass^k

- **pass@k**: Practical reliability. "Does it pass at least once in k attempts?"
  - Use for capability evals where variety is expected (e.g. creative writing).
- **pass^k**: Stability test. "Does it pass all k attempts?"
  - Use for release-critical regression paths (e.g. authentication, data writes).

**Recommended Thresholds:**

- Capability evals: pass@3 >= 0.90
- Regression evals: pass^3 = 1.00 (Zero regression tolerance)

---

## Eval Workflow

### 1. Define (Before Coding)

Create an eval definition at `.agent/evals/<feature>.md`:

```markdown
## EVAL DEFINITION: auth-service

### Capability Evals

1. Can generate valid JWT
2. Can refresh expired token
3. Can revoke session

### Regression Evals

1. Existing login flow still works
2. Password hashing unchanged

### Success Metrics

- pass@3 > 90% for capabilities
- pass^3 = 100% for regressions
```

### 2. Implement

Write the implementation code.

### 3. Evaluate

Run the evals and record results.

### 4. Report

Generate a summary report:

```markdown
# EVAL REPORT: auth-service

Capabilites: 3/3 PASS (pass@3)
Regressions: 2/2 PASS (pass^3)
Status: READY FOR PR
```

---

## Integration Patterns

- **Pre-Implementation:** `/eval define <name>` (Creates definition artifact)
- **During Implementation:** `/eval check <name>` (Quick status check)
- **Post-Implementation:** `/eval report <name>` (Final release snapshot)

---

## Minimal Eval Artifact Layout

- `.agent/evals/<feature>.md` — Definition
- `.agent/evals/<feature>.log` — Run history
- `docs/releases/<version>/eval-summary.md` — Release snapshot

---

## Anti-Patterns

- **Overfitting**: Tuning prompts solely for the eval examples.
- **Happy-path only**: Missing edge cases and failure modes in the eval suite.
- **Flaky Graders**: Allowing a model grader to have inconsistent judgment for deterministic tasks.
- **Ignoring Cost**: Chasing a high pass rate with extremely expensive prompts/models.
