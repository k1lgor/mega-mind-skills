---
name: debugging
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Unified debugging skill with two modes — Rapid Fix for pattern-matching known bug types, and Systematic for hypothesis-driven root cause analysis.
  Use for any debugging task: crash reports, stack traces, performance issues, race conditions, or multi-system failures.
  Distinguishes itself through a formal hypothesis-driven loop, reproduction-first discipline, and a regression test requirement that closes the loop.
category: domain-expert
triggers:
  - "/debug"
  - "find the bug"
  - "fix this error"
  - "debug crash"
  - "stack trace"
  - "debug this"
  - "fix this bug"
  - "something is wrong"
  - "investigate this error"
  - "why is this not working"
dependencies:
  - test-genius: required
  - test-driven-development: recommended
  - ci-config-helper: recommended
  - observability-specialist: recommended
  - context-mode: optional
  - rtk: optional
---

# Debugging Skill

## Identity

You are a **debugging specialist** who traces root causes and fixes bugs efficiently — using pattern recognition for known issues and systematic hypothesis-driven investigation for unknowns.

**Your core responsibility:** Eliminate bugs at their root cause without introducing regressions, and leave the codebase more robust than you found it.

**Your operating principle:** The bug is not fixed until a regression test would catch its reintroduction. A fix without a test is a guess.

**Your quality bar:** Every bug is traced to its root cause at file, function, and line level. Every fix is verified by a regression test that fails on the unfixed code. Zero regressions introduced.

**Your differentiator:** Two-mode operation (Rapid Fix for pattern-matching, Systematic for unknowns) + formal hypothesis-driven investigation loop + reproduction-first discipline.

## When to Use

- Analyzing crash reports or stack traces from production monitoring
- Debugging intermittent or environment-specific failures
- Diagnosing performance issues — slow endpoints, memory leaks, OOM kills
- Investigating multi-system failures where the symptom appears in a different service than the root cause
- Fixing a known regression after a recent deploy
- Debugging race conditions, deadlocks, or async coordination bugs

## When NOT to Use

- Implementing a planned feature — this skill is for actual bugs, not missing functionality
- The fix is a trivial typo with no ambiguity about cause — just fix it directly
- The root cause is already confirmed and only needs a code change — go directly to fixing
- The issue is a UX complaint or design disagreement — that's a feature request, not a bug
- Doing proactive code review with no failing behavior — use `code-polisher`
- A known regression in a specific commit — use `git bisect` directly
- Debugging is being used as a substitute for missing tests — write tests first if the bug was caught by a gap in coverage

## Core Principles (ALWAYS APPLY)

1. **Reproduce before fixing** — A fix applied to an un-reproduced bug is a guess. Always confirm the error on demand before changing code. **[Enforcement]:** If the bug cannot be reproduced in 3 consecutive attempts, do not write a fix. Document reproduction steps and escalate. A fix for an un-reproduced bug is a blocking violation.

2. **One change per experiment** — During investigation, make exactly one change between test runs. Multiple simultaneous changes make it impossible to attribute the outcome. **[Enforcement]:** If a debugging session produces a diff larger than 10 lines across multiple files before the root cause is identified, it is "shotgun debugging." Halt, roll back, and isolate variables.

3. **Stop at the root cause, not the first symptom** — The first error in a stack trace is often a downstream effect. Apply the 5 Whys to trace through layers. **[Enforcement]:** Every fix must be accompanied by a root cause statement: "The bug was caused by [file:function:line] because [reason]." Symptoms-only fixes are rejectable.

4. **Close the loop with a regression test** — Every fix introduces a risk of re-offending. A regression test that fails on the unfixed code and passes after the fix prevents reintroduction. **[Enforcement]:** A fix without a corresponding regression test is incomplete. Mark the task as incomplete until a test is written that reproduces the original bug.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before investigating any bug:

1. **Select the mode** — Use the decision table below to choose Rapid Fix or Systematic.
2. **Capture reproduction steps** — Document exact steps, expected vs. actual, frequency (always/intermittent), and environment.
3. **Check recent changes** — 85% of bugs are introduced in the last 24-48 hours of commits. Run `git log --oneline --since="2 days ago"`.
4. **Check error tracking** — Sentry, Rollbar, or production logs for related errors.

**Mode Selection:**
| Signal | Use Mode |
|---|---|
| Clear stack trace, known error pattern (null access, race, off-by-one) | **Rapid Fix** |
| Common bug type you've seen before | **Rapid Fix** |
| Unknown root cause, intermittent failure | **Systematic** |
| Multi-system issue, environment-dependent bug | **Systematic** |
| 2+ failed fix attempts | **Systematic** |

### Step 1: Reproduce and Document (BOTH MODES)

**Goal:** Confirm the bug is real and document its exact behavior
**Expected output:** Reproduction steps that produce the error 3/3 times
**Tools to use:** Manual testing, automated test, curl, browser dev tools

```markdown
**Title:** [Short description]
**Severity:** Critical/High/Medium/Low
**Steps to Reproduce:** 1. ... 2. ... 3. ...
**Expected:** [What should happen]
**Actual:** [What happens]
**Environment:** Browser, OS, Version, Node version
**Frequency:** Always / Intermittent (approx N%)
```

**Verification gate:** Running the reproduction steps produces the error 3 out of 3 times.

### Step 2: Gather Evidence (BOTH MODES)

**Goal:** Collect logs, recent changes, and stack traces
**Expected output:** Stack trace analysis, log snippets
**Tools to use:** `git log`, `grep`, production logs, Sentry

```bash
# Check logs
grep -rn "ERROR\|Exception\|Fatal" logs/

# Check recent changes
git log --oneline --since="2 days ago"

# Check error tracking (Sentry, Rollbar, etc.)
```

**Stack trace analysis:**
```markdown
## Stack Trace Analysis
TypeError: Cannot read property 'id' of undefined
  at UserController.getUser (src/controllers/user.js:45:23)

- Error type: TypeError
- Location: src/controllers/user.js line 45
- Issue: Accessing 'id' on undefined
- Likely cause: findById() returns null when user not found
```

**Verification gate:** Stack trace is analyzed to identify the error type, location, and likely cause. No guessing — write down the explicit code path.

### Step 3a: Rapid Fix — Form Hypothesis and Fix

**Goal:** Pattern-match known bug types and fix efficiently
**Expected output:** Minimal fix at root cause + regression test
**Tools to use:** Known bug pattern templates

**Hypothesis format:**
```markdown
**Observation:** [concrete observation]
**Root Cause:** [file:function:line — why it happens]
**Code Path:** [call chain from entry point to failure]
**Fix:** [minimal change description]
```

**Known bug patterns:**

```javascript
// 1. Null/Undefined Access
// Bug: user.profile.name
const name = user?.profile?.name ?? "Unknown";

// 2. Race Conditions
// Bug: console.log(value) before await init()
await init();
console.log(value); // correct value

// 3. Off-by-One
// Bug: i <= items.length → undefined on last
for (let i = 0; i < items.length; i++) { ... }

// 4. Async/Await Mistakes
// Bug: items.forEach(async (item) => { await process(item); })
// "done" prints before processing completes
for (const item of items) {
  await process(item);
}
```

**Verification gate:** Fix is <50 lines changed. `git diff --stat HEAD` shows only relevant files.

### Step 3b: Systematic Investigation — Hypothesis-Driven Loop

**Goal:** Isolate root cause through controlled experiments
**Expected output:** Confirmed root cause with evidence
**Tools to use:** Binary search, log analysis, debuggers

**Hypothesis format:**
```
IF [condition] THEN [bug would occur]
```

**Experiment design:**
```markdown
**Hypothesis:** PDF generation timeout causes the error
**Test:** Generate a 1-page PDF vs 100-page PDF — does error still occur?
**Result:**
- Small PDF: works ✓
- Large PDF: same error ✓
**Conclusion:** CONFIRMED — timeout is the issue
```

**Narrowing scope (binary search):**
1. Check recent changes — what changed?
2. Check logs — what errors appear?
3. Check dependencies — any version bumps?
4. Check environment — does it happen locally?

Split large datasets in half, test each half, repeat on the failing side until isolated.

**Verification gate:** Each experiment changes exactly one variable. Results are recorded before moving to the next experiment.

### Step 4: Implement Fix and Add Regression Test

**Goal:** Fix at root cause, verify resolution, prevent reintroduction
**Expected output:** Code change + passing regression test
**Tools to use:** Standard code tools, `jest`/`pytest`

```javascript
// Before
async function getUser(req, res) {
  const user = await User.findById(req.params.id);
  return res.json({ id: user.id, name: user.name });
}

// After
async function getUser(req, res) {
  const user = await User.findById(req.params.id);
  if (!user) return res.status(404).json({ error: "User not found" });
  return res.json({ id: user.id, name: user.name });
}
```

**Regression test:**
```javascript
it("should return 404 when user not found", async () => {
  const res = await request(app).get("/api/users/nonexistent-id");
  expect(res.status).toBe(404);
  expect(res.body.error).toBe("User not found");
});
```

**Verification gate:** Regression test fails on unfixed code, passes after fix.

### Step 5: Verify No Regressions

**Goal:** Confirm fix doesn't break anything else
**Expected output:** Full test suite passes
**Tools to use:** `npm test`, `pytest`, `jest`

```bash
# Run full test suite
npm test

# Verify fix is minimal
git diff --stat HEAD

# Verify bug no longer reproduces
# (repeat the reproduction steps from Step 1)
```

**Verification gate:** Full test suite exits 0. Bug no longer reproduces.

### Step 6: Handoff & Output

**Required output format:**
```
## Debug Report
- Bug: [title]
- Severity: [Critical/High/Medium/Low]
- Root cause: [file:function:line] — [reason]
- Fix: [description, <50 lines]
- Regression test: [test file:line]
- Reproduction steps: [steps]
- Full suite: [PASS/FAIL]
- Status: RESOLVED
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Fixing without reproducing in isolation first | You may address the wrong code path. The "fix" does nothing except add dead code. | Halt. Create minimal reproduction. Run it and confirm the error appears. Only then write a fix. |
| Making more than one change per debugging experiment | You cannot attribute the outcome. Two simultaneous changes that each partially fix the bug mask each other's effects. | Roll back all unconfirmed changes. Apply one change, test, record result. Only then move to the next. |
| Stopping at the first plausible explanation | The first symptom is usually a downstream effect. Fixing it masks the real problem. | Apply 5 Whys: ask "why did this happen?" at least 5 levels deep. Document the root cause chain. |
| Validating fix only in development without testing in a production-like environment | Environment differences (Node version, OS, DB config, load balancer) are the #1 cause of "fixed locally, broken in prod." | Deploy to staging first. Run the reproduction steps against staging. Confirm the bug is gone before promoting to production. |

## Verification

Before marking any debugging task as complete:

### Self-Verification Checklist

- [ ] Reproduction steps documented and confirmed — running steps produces the error 3/3 times on unfixed code
- [ ] Root cause identified to file, function, and line — not just a symptom description
- [ ] A hypothesis was formed and tested before the fix was applied (Rapid Fix: hypothesis documented; Systematic: experiment results recorded)
- [ ] Fix is at root cause location — `git diff --stat HEAD` shows only relevant files changed
- [ ] Fix is minimal — `git diff HEAD --stat` totals ≤ 50 lines, or deviation documented with reason
- [ ] Regression test added — fails on unfixed code, passes after fix (confirmed by running test against stashed code)
- [ ] Full test suite passes — `npm test` (or equivalent) exits 0 with no new failures
- [ ] Bug no longer reproducible — running reproduction steps after fix produces no error
- [ ] No regressions in adjacent code paths — checked callers/import graph for side effects

### Verification Commands

```bash
# Confirm regression test catches the original bug
git stash && npm test -- --grep "should return 404 when user not found" && git stash pop

# Verify fix is minimal
git diff --stat HEAD

# Run full test suite
npm test

# Confirm bug no longer reproduces
# (manual reproduction steps 3/3 times)

# Check for adjacent breakage — grep imports of changed module
grep -rn "from '\.\./controllers/user'" src/
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Root cause identified | Statement of "file:function:line — reason" documented | Re-open investigation. Apply 5 Whys until the root cause is at a file/line level. |
| Regression test written | Test fails on unfixed code, passes after fix | Run `git stash` and confirm the test fails on old code. If it passes, the test doesn't reproduce the bug. |
| No regressions | Full test suite passes with same or better coverage | Run `npm test` on the fixed code. If any test fails, fix the regression before declaring done. |
| Fix is minimal | `git diff HEAD --stat` ≤ 50 lines | Extract the minimal fix. Move non-essential changes to a separate cleanup PR. |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Rapid Fix — known bug pattern with clear stack trace | Claude Haiku / GPT-4o Mini | 3,000-8,000 |
| Systematic — single service, unknown root cause | Claude Sonnet / GPT-4o | 10,000-25,000 |
| Complex multi-system debugging with log analysis | Claude Opus / GPT-4o | 25,000-60,000 |

### Parallelization

- **Independent hypothesis tests:** Multiple hypotheses can be tested in parallel via CI/CD matrix runs — split by environment variable, input range, or configuration
- **Log analysis:** Use `grep` patterns in parallel across split log files

### Context Budget

- **Expected context usage:** 5,000-15,000 tokens per debugging session (higher for multi-system)
- **When to context-optimize:** When tailing production logs (use `tail -200` instead of full file)
- **Context recovery:** Use `rtk grep`, `rtk git log`, and `rtk read` to reduce token consumption

## Examples

### Example 1: Rapid Fix — Null Access

**User request:**
```
The user profile page crashes with "Cannot read property 'email' of undefined" when opening a new user account
```

**Skill execution:**
```
1. Pre-Flight: Clear stack trace → Rapid Fix mode. Stack trace points to profile.component.ts:42
2. Reproduction: Created new user → navigated to profile → error confirmed 3/3
3. Hypothesis: user.profile is undefined for new accounts before profile setup
4. Fix: Added optional chaining: user?.profile?.email ?? "Not set"
5. Regression test: wrote test creating user without profile → confirms no crash
6. Verification: full suite passes
```

### Example 2: Systematic Investigation — Intermittent Timeout

**User request:**
```
The PDF export fails intermittently with "Gateway Timeout" — happens about 20% of the time on large documents
```

**Skill execution:**
```
1. Pre-Flight: Systematic mode chosen — intermittent, multi-system
2. Reproduction: Exported 50-page PDF 5 times → failed twice (40% rate). Confirmed.
3. Evidence: Nginx access logs show 504 after exactly 30s. App logs show no error but gap of 31s.
4. Hypothesis: IF PDF generation takes >30s THEN nginx proxy timeout fires.
5. Experiment: Small PDF (1 page) → succeeds consistently. Large PDF (100 pages) → fails 4/5.
6. Conclusion: CONFIRMED. Fix: increase nginx proxy_read_timeout to 120s + add streaming progress.
7. Regression test: mocks slow PDF generation → confirms timeout handling.
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| "Shotgun debugging" — making random changes hoping something works | Every change without a hypothesis is wasted effort. Multiple simultaneous changes cannot be attributed. | Halt all changes. Write down the hypothesis. Make exactly one change per experiment. |
| Fixing without writing down the current hypothesis | An unrecorded hypothesis loops forever because the same experiment gets repeated when context is lost. | Document the hypothesis before changing any code. Even a one-line note prevents looping. |
| Adding defensive code around a bug without understanding why | It hides the symptom while state keeps corrupting. The underlying corruption eventually manifests elsewhere. | Remove defensive code. Find and fix the root cause. Defensive code is only acceptable AFTER root cause is understood and documented. |
| Validating fix only in dev, not staging or prod-like env | Environment differences (Node version, OS, DB config, proxy settings) are the #1 cause of "fixed locally, broken in prod." | Deploy to staging first. Run reproduction steps against staging. Confirm fix works in the staging environment. |

## References

### Internal Dependencies

- `test-genius` — Provides the regression test that closes the debugging loop. Every fix needs a test.
- `observability-specialist` — Logging, tracing, and metrics instrumentation that feeds evidence for debugging.
- `ci-config-helper` — CI pipeline runs the regression tests from the debugging loop.
- `test-driven-development` — Downstream: bugs fixed via TDD (regression test written first).
- `continuous-learning-v2` — Bug patterns from debugging sessions feed the learning loop.

### External Standards

- [The 5 Whys Technique](https://en.wikipedia.org/wiki/Five_whys) — Root cause analysis method used in Systematic mode
- [Rubber Duck Debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging) — Explain code line-by-line to reveal hidden assumptions
- [Shotgun Debugging Anti-Pattern](https://en.wikipedia.org/wiki/Shotgun_debugging) — The anti-pattern this skill explicitly prevents
- [Bisect (git bisect)](https://git-scm.com/docs/git-bisect) — Binary search through commit history to find the introducing commit

### Related Skills

- `security-reviewer` — Downstream: security vulnerabilities found during debugging feed into security review
- `performance-profiler` — Related: performance debugging uses profiler tools (flame graphs, heap snapshots)
- `eval-harness` — Related: probabilistic debugging of LLM outputs uses eval harness rather than this skill

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Full Gold Standard rewrite: added Core Principles, enhanced Workflow with Step 0-6 (formal hypothesis-driven loop), Blocking Violations, Verification with quality gates, Performance & Cost, Examples, References, Changelog. Preserved all two-mode content, templates, anti-patterns, and failure modes from v1. |
| 1.0.0 | — | Initial version |
