---
name: code-polisher
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

## Tips

- Read code before refactoring
- Have tests before refactoring
- Small commits are easier to review
- Name things clearly
- Remove dead code
- Don't over-engineer
