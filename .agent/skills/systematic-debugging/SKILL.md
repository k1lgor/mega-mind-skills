---
name: systematic-debugging
description: Root cause tracing with supporting techniques for systematic bug diagnosis and fixing.
triggers:
  - "debug this"
  - "fix this bug"
  - "something is wrong"
  - "investigate this error"
  - "why is this not working"
---

# Systematic Debugging Skill

## When to Use

- Encountering unexpected behavior
- Investigating errors or crashes
- Diagnosing performance issues
- Tracking down race conditions

## Instructions

### Step 1: Reproduce the Bug

Before debugging, ensure you can reproduce the issue:

1. **Document the exact steps** to trigger the bug
2. **Identify the expected behavior**
3. **Identify the actual behavior**
4. **Note any environmental factors** (browser, OS, environment)

```markdown
## Bug Report

**Steps to Reproduce:**

1. Open the application
2. Navigate to /dashboard
3. Click "Export" button
4. Select "PDF" format

**Expected:** PDF downloads successfully
**Actual:** Error "Network timeout" after 30 seconds
**Environment:** Production, Chrome 120, macOS
```

### Step 2: Narrow the Scope

Binary search to isolate the problem:

1. **Check recent changes** - What changed recently?
2. **Check logs** - What errors appear?
3. **Check dependencies** - Any version changes?
4. **Check environment** - Does it happen locally?

### Step 3: Form a Hypothesis

Based on evidence, form a hypothesis:

```
IF [condition] THEN [bug would occur]
```

Example: "IF the PDF generation takes > 30s THEN the load balancer timeout triggers"

### Step 4: Test the Hypothesis

Design an experiment to prove/disprove:

```markdown
## Experiment

**Hypothesis:** PDF generation timeout causes the error

**Test:**

1. Generate a smaller PDF (1 page vs 100 pages)
2. Check if error still occurs

**Result:**

- Small PDF works ✓
- Large PDF fails with same error ✓

**Conclusion:** Hypothesis CONFIRMED - timeout is the issue
```

### Step 5: Fix and Verify

1. **Implement the fix**
2. **Verify the fix resolves the issue**
3. **Check for side effects**
4. **Add a regression test**

## Debugging Techniques

### 1. Log Analysis

```bash
# Search for errors (compact grouped output)
rtk grep "ERROR\|Exception\|Failed" logs/

# Check recent changes (85% savings)
rtk git log --oneline --since="2 days ago"

# Trace specific request
rtk grep "request-id-123" logs/app.log
```

### 2. Interactive Debugging

```javascript
// Add strategic logging
console.log("[DEBUG] Variable state:", variable);
console.log("[DEBUG] Function called with:", arguments);

// Use debugger statements
debugger; // Code will pause here in dev tools
```

### 3. Binary Search

```
Large dataset causing issue?
→ Split in half
→ Test each half
→ Repeat with failing half
→ Until you find the problematic element
```

### 4. Rubber Duck Debugging

Explain the code line-by-line to an inanimate object. Often reveals assumptions.

## Debugging Checklist

```markdown
## Debugging Checklist

### Reproduction

- [ ] Can reproduce consistently
- [ ] Have minimal reproduction case
- [ ] Documented steps

### Investigation

- [ ] Checked logs
- [ ] Checked recent changes
- [ ] Checked environment differences
- [ ] Checked dependencies

### Hypothesis

- [ ] Formed specific hypothesis
- [ ] Designed experiment
- [ ] Ran experiment
- [ ] Documented results

### Fix

- [ ] Implemented fix
- [ ] Verified fix works
- [ ] No side effects
- [ ] Added regression test
- [ ] Updated documentation
```

## Example Debugging Session

```
Bug: User profile page shows "undefined" for name

=== Step 1: Reproduce ===
✓ Can reproduce on staging
✓ Steps documented

=== Step 2: Narrow Scope ===
→ Check logs: TypeError: Cannot read property 'name' of undefined
→ Check code: profile.component.ts line 45
→ Recent changes: User API response format changed

=== Step 3: Form Hypothesis ===
Hypothesis: API now returns 'fullName' instead of 'name'

=== Step 4: Test ===
→ Check API response: { fullName: "John Doe", email: "..." }
→ Component expects: user.name
✓ Hypothesis CONFIRMED

=== Step 5: Fix ===
→ Update component to use user.fullName
→ Add fallback: user.fullName || user.name
→ Add test for both formats
→ Verify fix works
✓ Bug fixed

=== Prevention ===
→ Add API contract test
→ Update TypeScript interface
→ Document API changes in changelog
```

## Tips

- Don't assume - verify everything
- Start with the most likely causes
- Keep a debugging log for complex issues
- Take breaks if stuck - fresh eyes help
- Ask for help if stuck for > 30 minutes
- Always add a regression test after fixing

## Token Optimization (RTK)

Debugging often involves searching logs and checking git history. Use **RTK** to keep the output concise and save tokens:

- Use `rtk git status` or `rtk git diff` to see what changed
- Use `rtk git log -10` to check recent commits
- Use `rtk grep` for grouped search results
- Use `rtk read <file>` for filtered file inspection

This maintains a focused context window while you're investigating root causes.
