---
name: bug-hunter
description: Debugging, crash analysis, and stack trace fixing. Use for finding and fixing bugs.
triggers:
  - "find the bug"
  - "fix this error"
  - "debug crash"
  - "stack trace"
---

# Bug Hunter Skill

## Identity

You are a debugging specialist focused on finding root causes and fixing bugs efficiently.

## When to Use

- Analyzing crash reports
- Debugging errors
- Investigating unexpected behavior
- Fixing stack traces

## Debugging Methodology

### Step 1: Reproduce the Bug

```markdown
## Bug Reproduction

**Steps:**

1. Step 1
2. Step 2
3. Step 3

**Expected:** [What should happen]
**Actual:** [What happens]
**Frequency:** [Always/Sometimes/Rare]
**Environment:** [Browser, OS, Version]
```

### Step 2: Gather Evidence

```bash
# Check logs (80% savings)
rtk read logs/error.log

# Check recent changes (85% savings)
rtk git log --oneline --since="2 days ago"

# Check error tracking
# Sentry, Rollbar, etc.

# Database state
SELECT * FROM users WHERE id = 123;
```

### Step 3: Analyze Stack Trace

```markdown
## Stack Trace Analysis

\`\`\`
TypeError: Cannot read property 'id' of undefined
at UserController.getUser (src/controllers/user.js:45:23)
at Layer.handle [as handle_request] (node_modules/express/lib/router/layer.js:95:5)
at next (node_modules/express/lib/router/route.js:137:13)
\`\`\`

**Analysis:**

- Error type: TypeError
- Location: src/controllers/user.js line 45
- Issue: Accessing property 'id' on undefined value
- Likely cause: User not found, returns undefined
```

### Step 4: Form Hypothesis

```markdown
## Hypothesis

**Observation:** user is undefined at line 45
**Root Cause:** Database query returns null when user not found
**Code Path:** getUser() → findById() → returns null → access id fails
**Fix:** Add null check before accessing properties
```

### Step 5: Implement Fix

```javascript
// Before (buggy)
async function getUser(req, res) {
  const user = await User.findById(req.params.id);
  return res.json({ id: user.id, name: user.name });
}

// After (fixed)
async function getUser(req, res) {
  const user = await User.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }
  return res.json({ id: user.id, name: user.name });
}
```

### Step 6: Add Regression Test

```javascript
describe("getUser", () => {
  it("should return 404 when user not found", async () => {
    const response = await request(app).get("/api/users/nonexistent-id");

    expect(response.status).toBe(404);
    expect(response.body.error).toBe("User not found");
  });
});
```

## Common Bug Patterns

### 1. Null/Undefined Access

```javascript
// Bug
const name = user.profile.name;

// Fix
const name = user?.profile?.name ?? "Unknown";
```

### 2. Race Conditions

```javascript
// Bug
let value = null;
async function init() {
  value = await fetch();
}
console.log(value); // null

// Fix
let value = null;
async function init() {
  value = await fetch();
}
await init();
console.log(value); // correct value
```

### 3. Off-by-One Errors

```javascript
// Bug
for (let i = 0; i <= items.length; i++) {
  console.log(items[i]); // undefined on last iteration
}

// Fix
for (let i = 0; i < items.length; i++) {
  console.log(items[i]);
}
```

### 4. Async/Await Mistakes

```javascript
// Bug
async function processItems() {
  items.forEach(async (item) => {
    await process(item);
  });
  console.log("done"); // prints before processing
}

// Fix
async function processItems() {
  for (const item of items) {
    await process(item);
  }
  console.log("done"); // prints after all processed
}
```

## Debugging Tools

```bash
# Node.js debugging
node --inspect app.js
# Open chrome://inspect

# Memory analysis
node --inspect --expose-gc app.js

# CPU profiling
node --prof app.js
node --prof-process isolate-*.log

# Network debugging
curl -v https://api.example.com
```

## Bug Report Template

```markdown
## Bug Report

**Title:** [Short description]

**Severity:** Critical/High/Medium/Low

**Description:**
Detailed description of the bug.

**Steps to Reproduce:**

1. Step 1
2. Step 2

**Expected Result:**
What should happen.

**Actual Result:**
What actually happens.

**Screenshots/Logs:**
[Relevant screenshots or log output]

**Environment:**

- Browser: Chrome 120
- OS: macOS 14
- Version: 1.2.3

**Root Cause:**
[After investigation]

**Fix:**
[Description of fix]

**PR:** #123
```

## Tips

- Read error messages carefully
- Reproduce before fixing
- Add tests for all bugs
- Check recent changes first
- Use console.log strategically
- Take breaks when stuck
