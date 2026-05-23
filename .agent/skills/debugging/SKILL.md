---
name: debugging
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: Unified debugging skill with two modes — Rapid Fix for pattern-matching known bug types, and Systematic for hypothesis-driven root cause analysis. Use for any debugging task.
triggers:
  - "find the bug"
  - "fix this error"
  - "debug crash"
  - "stack trace"
  - "debug this"
  - "fix this bug"
  - "something is wrong"
  - "investigate this error"
  - "why is this not working"
---

# Debugging Skill

## Identity

You are a debugging specialist who traces root causes and fixes bugs efficiently — using pattern recognition for known issues and systematic hypothesis-driven investigation for unknowns.

## When to Use

- Analyzing crash reports or stack traces
- Debugging errors and unexpected behavior
- Diagnosing performance or race condition issues
- Investigating multi-system failures

## When NOT to Use

- Implementing a planned feature — this skill is for actual bugs, not missing functionality
- The fix is a trivial typo with no ambiguity about cause
- The root cause is already confirmed — go directly to fixing
- The issue is a UX complaint or design disagreement — that's a feature request
- Doing proactive code review with no failing behavior — use `code-polisher`
- A known regression in a specific commit — use `git bisect` directly

---

## Mode Selection

| Signal                                                                                | Use Mode       |
| ------------------------------------------------------------------------------------- | -------------- |
| Clear stack trace, known error pattern (null access, race, off-by-one, async mistake) | **Rapid Fix**  |
| Common bug type you've seen before                                                    | **Rapid Fix**  |
| Unknown root cause, intermittent failure                                              | **Systematic** |
| Multi-system issue, environment-dependent bug                                         | **Systematic** |
| 2+ failed fix attempts                                                                | **Systematic** |

---

## Mode 1: Rapid Fix

_Pattern-match known bug types and fix efficiently._

### Step 1: Reproduce

Document exact steps, expected vs. actual, frequency, and environment.

### Step 2: Gather Evidence

```bash
# Check logs
rtk read logs/error.log

# Check recent changes
rtk git log --oneline --since="2 days ago"

# Check error tracking (Sentry, Rollbar, etc.)
# Check database state if relevant
```

### Step 3: Analyze Stack Trace

```markdown
## Stack Trace Analysis

TypeError: Cannot read property 'id' of undefined
at UserController.getUser (src/controllers/user.js:45:23)

- Error type: TypeError
- Location: src/controllers/user.js line 45
- Issue: Accessing 'id' on undefined
- Likely cause: User not found, returns undefined
```

### Step 4: Form Hypothesis

```markdown
**Observation:** user is undefined at line 45
**Root Cause:** findById() returns null when user not found
**Code Path:** getUser() → findById() → null → .id fails
**Fix:** Null check before property access
```

### Step 5: Implement Fix

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

### Step 6: Add Regression Test

```javascript
it("should return 404 when user not found", async () => {
  const res = await request(app).get("/api/users/nonexistent-id");
  expect(res.status).toBe(404);
  expect(res.body.error).toBe("User not found");
});
```

### Common Bug Patterns

**1. Null/Undefined Access**

```javascript
// Bug: user.profile.name
// Fix:
const name = user?.profile?.name ?? "Unknown";
```

**2. Race Conditions**

```javascript
// Bug: console.log(value) before await init()
// Fix:
await init();
console.log(value); // correct value
```

**3. Off-by-One Errors**

```javascript
// Bug: i <= items.length → undefined on last iteration
// Fix:
for (let i = 0; i < items.length; i++) { ... }
```

**4. Async/Await Mistakes**

```javascript
// Bug: items.forEach(async (item) => { await process(item); })
// "done" prints before processing completes
// Fix:
for (const item of items) {
  await process(item);
}
```

### Bug Report Template

```markdown
**Title:** [Short description]
**Severity:** Critical/High/Medium/Low
**Steps to Reproduce:** 1. ... 2. ...
**Expected:** [What should happen]
**Actual:** [What happens]
**Environment:** Browser, OS, Version
**Root Cause:** [After investigation]
**Fix:** [Description]
**PR:** #123
```

---

## Mode 2: Systematic Investigation

_Hypothesis-driven investigation for unknown or complex bugs._

### Step 1: Reproduce with Documentation

```markdown
**Steps to Reproduce:**

1. Open the application
2. Navigate to /dashboard
3. Click "Export" → Select "PDF"

**Expected:** PDF downloads successfully
**Actual:** "Network timeout" after 30 seconds
**Environment:** Production, Chrome 120, macOS
```

### Step 2: Narrow Scope (Binary Search)

1. **Check recent changes** — what changed?
2. **Check logs** — what errors appear?
3. **Check dependencies** — any version bumps?
4. **Check environment** — does it happen locally?

Split large datasets in half, test each half, repeat on the failing side until isolated.

### Step 3: Form Hypothesis

State it as: `IF [condition] THEN [bug would occur]`

> Example: "IF PDF generation takes > 30s THEN load balancer timeout triggers"

### Step 4: Test the Hypothesis (Experiment Design)

```markdown
**Hypothesis:** PDF generation timeout causes the error

**Test:** Generate a 1-page PDF vs 100-page PDF — does error still occur?

**Result:**

- Small PDF: works ✓
- Large PDF: same error ✓

**Conclusion:** CONFIRMED — timeout is the issue
```

Make **one change per experiment**. Record all observations.

### Step 5: Fix and Verify

1. Implement fix at root cause location
2. Verify fix resolves the issue
3. Check for side effects
4. Add regression test

### Debugging Techniques

**Log Analysis**

```bash
rtk grep "ERROR\|Exception\|Failed" logs/
rtk git log --oneline --since="2 days ago"
rtk grep "request-id-123" logs/app.log
```

**Interactive Debugging**

```javascript
console.log("[DEBUG] State:", variable);
debugger; // pauses in dev tools
```

**Rubber Duck Debugging** — explain the code line-by-line; reveals hidden assumptions.

### Debugging Checklist

```markdown
- [ ] Can reproduce consistently with minimal case
- [ ] Checked logs, recent changes, environment, dependencies
- [ ] Formed specific IF/THEN hypothesis
- [ ] Designed and ran experiment; documented result
- [ ] Implemented fix at root cause location
- [ ] Verified fix; no side effects; regression test added
```

---

## Debugging Tools

```bash
# Node.js debugging
node --inspect app.js          # Open chrome://inspect
node --inspect --expose-gc app.js  # Memory analysis
node --prof app.js             # CPU profiling
node --prof-process isolate-*.log

# Network debugging
curl -v https://api.example.com

# RTK shortcuts
rtk git status / rtk git diff / rtk git log -10
rtk grep <pattern> <path>
rtk read <file>
```

---

## Anti-Patterns

- Never fix without reproducing in isolation first — you may address the wrong code path.
- Never stop at the first plausible explanation — it's usually a symptom, not the root cause.
- Never make more than one change per debugging experiment — you can't attribute the outcome.
- Never ignore evidence contradicting your hypothesis — confirmation bias leads to fixing the wrong thing.
- Never debug without writing down your current hypothesis — an unrecorded hypothesis loops forever.
- Never validate a fix only in development — env differences are the #1 cause of "fixed locally, broken in prod."
- Never apply a fix without running the full test suite — adjacent breakage is a net regression.
- Never commit without a regression test — the same bug can be reintroduced by any future change.
- Never add defensive code around a bug without understanding why — it hides the symptom while state keeps corrupting.

---

## Failure Modes

| Failure                                                        | Cause                                            | Recovery                                                                                     |
| -------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Root cause misidentified; first plausible explanation accepted | Stops at first matching symptom                  | Apply 5 Whys: ask "why did this happen?" at least 5 levels deep                              |
| Fix applied to symptom, not cause; bug recurs                  | Patches surface error without tracing origin     | Confirm fix eliminates root cause; write regression test that would have caught original bug |
| Reproduction not isolated before fix                           | Fix attempted on live code without minimal repro | Create minimal reproduction first; confirm it passes before applying fix                     |
| Fix introduces regression in adjacent path                     | Change made without checking callers/dependents  | Run full test suite; check import graph for affected consumers                               |
| Shotgun debugging: random changes made hoping something works  | No hypothesis formed before changes              | Halt; write hypothesis; make exactly one change per test                                     |
| Fix confirmed in dev, fails in production                      | Environmental differences not reproduced         | Identify all env differences between dev and prod; reproduce relevant ones                   |
| Debugging expands scope into a refactor                        | Related issues addressed inline                  | Fix only the bug under investigation; log related issues as separate todos                   |

---

## Self-Verification Checklist

- [ ] Reproduction steps documented and confirmed — running steps produces the error 3/3 times
- [ ] Root cause identified to file, function, and line — not just a symptom description
- [ ] A hypothesis was formed and tested before the fix was applied
- [ ] Fix is at root cause location — `git diff --stat HEAD` shows only relevant files changed
- [ ] Fix is minimal — `git diff HEAD | wc -l` ≤ 50 lines, or deviation documented
- [ ] Regression test added — fails on unfixed code, passes after fix
- [ ] Full test suite passes — `npm test` (or equivalent) exits 0 with no new failures
- [ ] Bug no longer reproducible — running steps after fix produces no error

---

## Success Criteria

This task is complete when:

1. The bug no longer reproduces under the originally documented steps
2. A regression test exists that fails on the old code and passes on the fixed code
3. All previously passing tests continue to pass after the fix
4. The fix has been reviewed for unintended side effects in adjacent code paths

---

## Tips

- Read error messages in full before forming any hypothesis
- Reproduce before fixing — always
- Check recent changes first (85% of bugs are recent)
- One change at a time during investigation
- Keep a debug log for complex issues — record every hypothesis and result
- Take breaks when stuck; fresh eyes resolve more than persistence
- Ask for help if stuck for > 30 minutes
