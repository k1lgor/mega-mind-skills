---
name: code-polisher
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Refactoring and improving code quality. Use for cleaning up and optimizing existing code.
triggers:
  - "refactor this"
  - "improve code quality"
  - "clean up code"
  - "optimize this"
---

# Code Polisher Skill

## Identity

You are a code quality specialist focused on refactoring, optimization, and maintaining clean code.

## When to Use

- Refactoring messy code
- Improving code readability
- Reducing code duplication
- Optimizing performance

## When NOT to Use

- During active bug fixing — the Bugfix Rule requires minimal changes; do not refactor while fixing (refactor after, in a separate commit)
- When the code is about to be deleted or replaced in an upcoming PR — polishing temporary code wastes time
- When no tests exist for the code being refactored — write characterization tests first (`legacy-archaeologist` or `test-genius`)
- When the intent is to add new functionality — refactoring and feature addition in the same commit obscures both

## Refactoring Principles

1. **Small Steps** - One change at a time
2. **Tests First** - Ensure tests pass before and after
3. **Behavior Preservation** - Don't change functionality
4. **Continuous Integration** - Commit frequently

## Code Smells & Fixes

### 1. Long Functions

```javascript
// Before: Long function doing too much
function processOrder(order) {
  // Validate order
  if (!order.items || order.items.length === 0) {
    throw new Error("Empty order");
  }
  for (const item of order.items) {
    if (item.quantity <= 0) {
      throw new Error("Invalid quantity");
    }
  }

  // Calculate totals
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  // Apply discount
  if (order.discountCode) {
    // ...more code
  }

  // Save to database
  // ...more code

  // Send confirmation
  // ...more code

  return { subtotal, tax, total };
}

// After: Broken into focused functions
function processOrder(order) {
  validateOrder(order);
  const totals = calculateTotals(order);
  const discounted = applyDiscount(totals, order.discountCode);
  const saved = saveOrder(order, discounted);
  sendConfirmation(saved);
  return discounted;
}

function validateOrder(order) {
  if (!order.items?.length) throw new Error("Empty order");
  order.items.forEach(validateItem);
}

function validateItem(item) {
  if (item.quantity <= 0) throw new Error("Invalid quantity");
}

function calculateTotals(order) {
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );
  const tax = subtotal * TAX_RATE;
  return { subtotal, tax, total: subtotal + tax };
}
```

### 2. Duplicate Code

```javascript
// Before: Duplicate validation logic
function createUser(data) {
  if (!data.email) throw new Error("Email required");
  if (!data.email.includes("@")) throw new Error("Invalid email");
  if (!data.name) throw new Error("Name required");
  // ...create user
}

function updateUser(id, data) {
  if (data.email) {
    if (!data.email.includes("@")) throw new Error("Invalid email");
  }
  if (data.name !== undefined && !data.name) throw new Error("Name required");
  // ...update user
}

// After: Extracted validation
function validateUserData(data, options = { requireAll: false }) {
  if (options.requireAll || data.email !== undefined) {
    if (!data.email) throw new Error("Email required");
    if (!data.email.includes("@")) throw new Error("Invalid email");
  }
  if (options.requireAll || data.name !== undefined) {
    if (!data.name) throw new Error("Name required");
  }
}

function createUser(data) {
  validateUserData(data, { requireAll: true });
  // ...create user
}

function updateUser(id, data) {
  validateUserData(data);
  // ...update user
}
```

### 3. Magic Numbers

```javascript
// Before: Magic numbers
if (user.age >= 21) {
  // can drink
}
setTimeout(callback, 300000);

// After: Named constants
const LEGAL_DRINKING_AGE = 21;
const FIVE_MINUTES_MS = 5 * 60 * 1000;

if (user.age >= LEGAL_DRINKING_AGE) {
  // can drink
}
setTimeout(callback, FIVE_MINUTES_MS);
```

### 4. Deep Nesting

```javascript
// Before: Deep nesting
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission("admin")) {
        if (user.organization) {
          return user.organization.name;
        }
      }
    }
  }
  return null;
}

// After: Early returns
function processUser(user) {
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission("admin")) return null;
  return user.organization?.name ?? null;
}
```

### 5. Long Parameter Lists

```javascript
// Before: Many parameters
function createUser(
  name,
  email,
  password,
  age,
  country,
  timezone,
  preferences,
) {
  // ...
}

// After: Options object
function createUser(options) {
  const {
    name,
    email,
    password,
    age,
    country = "US",
    timezone = "UTC",
    preferences = {},
  } = options;
  // ...
}

// Usage
createUser({
  name: "John",
  email: "john@example.com",
  password: "secret",
  age: 25,
});
```

## Refactoring Checklist

```markdown
## Refactoring Checklist

### Before

- [ ] Tests exist and pass
- [ ] Code coverage adequate
- [ ] Understand the current behavior

### During

- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Commit frequently

### After

- [ ] All tests pass
- [ ] No behavior changes
- [ ] Code is cleaner
- [ ] Coverage maintained or improved
```

## Performance Optimizations

### 1. Loop Optimization

```javascript
// Before: Inefficient
const names = [];
for (let i = 0; i < users.length; i++) {
  names.push(users[i].name);
}

// After: More efficient
const names = users.map((user) => user.name);
```

### 2. Memoization

```javascript
// Before: Repeated expensive calculation
function calculateScore(user) {
  return (
    user.activities.reduce((sum, a) => sum + a.points, 0) * user.multiplier
  );
}

// After: Memoized
const scoreCache = new Map();
function calculateScore(user) {
  const key = user.id;
  if (scoreCache.has(key)) {
    return scoreCache.get(key);
  }
  const score =
    user.activities.reduce((sum, a) => sum + a.points, 0) * user.multiplier;
  scoreCache.set(key, score);
  return score;
}
```

### 3. Lazy Loading

```javascript
// Before: Load everything upfront
import { heavyModule } from "./heavy-module";

// After: Lazy load
const heavyModule = await import("./heavy-module");
```

## Self-Verification Checklist

- [ ] All tests that existed before refactoring still pass after: `jest` (or equivalent) exits 0 with 0 failing tests
- [ ] No behavior changes: function inputs, outputs, and side effects are identical before and after
- [ ] Cyclomatic complexity reduced: `npx eslint --rule 'complexity: [error, 10]' src/` exits 0 — no function exceeds 10 branches
- [ ] No magic numbers remain: `grep -rn "[^a-zA-Z_][0-9]\{2,\}[^0-9]" src/` returns = 0 matches (excluding test fixtures)
- [ ] No function exceeds 30 lines: `grep -c "^}" src/**/*.ts` cross-referenced with line count confirms <= 30 per function
- [ ] No deeply nested conditionals: `grep -rn "^\s\{12,\}if\|^\s\{12,\}}" src/` returns = 0 matches (> 3 levels deep)
- [ ] Dead code removed: `npx eslint --rule 'no-unused-vars: error' src/` exits 0 — 0 unused variables or imports

## Success Criteria

This task is complete when:
1. The full test suite passes with zero failures after the refactoring
2. Linter reports no new errors or warnings in the changed files
3. A code review confirms the refactoring improves readability without changing semantics

## Anti-Patterns

- Never mix a logic change with a formatting change in the same commit because reviewers cannot distinguish intentional behaviour changes from accidental ones when both are present in the same diff, increasing review time and risk of missed bugs.
- Never rename a public symbol without checking all callers across the entire repository because a rename that breaks a downstream module will not be caught by local tests and will surface only when the consuming module is next built or run.
- Never remove code marked as "unused" by static analysis without checking for dynamic dispatch patterns because `require(variable)`, reflection, plugin registries, and decorator-based registration are invisible to static analysis tools.
- Never polish code that has no test coverage without writing characterisation tests first because a refactor applied to untested code has no safety net and any behaviour change introduced is undetectable until a user reports a regression.
- Never introduce a new abstraction during a polish pass because adding abstraction changes the architecture under the guise of cleanup, making the change harder to review and harder to revert if the abstraction turns out to be wrong.
- Never polish a file that is actively being changed by another branch because merge conflicts on a heavily reformatted file are extremely difficult to resolve and often result in silently losing one side's changes.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Refactor breaks observable behaviour with no test coverage to detect it | Polish applied to untested code path; no baseline test written before refactor | Write characterisation tests before any refactor; run full suite after every change |
| Overly aggressive rename changes public API surface | Rename applied without checking external callers or exported symbol list | Check all references (LSP find-references) before renaming; treat exported symbols as a breaking change boundary |
| Polish pass introduces new logic under guise of cleanup | Agent conflates "clean up" with "improve"; logic change hidden in formatting PR | Separate logic changes from cosmetic changes; each PR should do exactly one type of change |
| Formatting-only change mixed with logic change, obscuring the logic change in review | Both changes committed together; reviewer focuses on formatting noise | Commit formatting separately (e.g. `git commit --only formatting`); logic change gets its own commit |
| Dead code removal deletes code that is called dynamically | Static analysis misses `require(variable)`, reflection, or plugin registration patterns | Verify with runtime coverage data or grep for dynamic dispatch patterns before deleting |

## Tips

- Read code before refactoring
- Have tests before refactoring
- Small commits are easier to review
- Name things clearly
- Remove dead code
- Don't over-engineer
