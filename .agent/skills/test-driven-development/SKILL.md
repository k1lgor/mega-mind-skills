---
name: test-driven-development
description: Write tests first, implement second. Use when building new features that benefit from a test-first approach.
triggers:
  - "implement with TDD"
  - "use TDD"
  - "test-driven development"
  - "write tests first"
---

# Test-Driven Development Skill

## When to Use

- Building new features with clear requirements
- Implementing business logic
- Creating utility functions
- When code needs to be reliable and maintainable

## Instructions

### The TDD Cycle

```
┌─────────────────────────────────────────┐
│                                         │
│  RED → GREEN → REFACTOR → (repeat)      │
│                                         │
└─────────────────────────────────────────┘
```

### Step 1: RED - Write a Failing Test

1. **Identify the next smallest piece of functionality**
2. **Write a test that describes the expected behavior**
3. **Run the test - it should FAIL**
4. **Confirm the failure is for the right reason**

```typescript
// Example: Testing a new function
describe("calculateTotal", () => {
  it("should sum line items correctly", () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 },
    ];
    expect(calculateTotal(items)).toBe(35);
  });
});
// This test FAILS because calculateTotal doesn't exist yet
```

### Step 2: GREEN - Make It Pass

1. **Write the MINIMUM code to make the test pass**
2. **Don't worry about elegance yet**
3. **Run the test - it should PASS**

```typescript
// Minimum implementation to pass
export function calculateTotal(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

### Step 3: REFACTOR - Clean It Up

1. **Review the code for improvements**
2. **Refactor while keeping tests green**
3. **Run tests after each change**

```typescript
// Refactored version (tests still pass)
export function calculateTotal(items: LineItem[]): number {
  return items
    .map((item) => item.price * item.quantity)
    .reduce((sum, total) => sum + total, 0);
}
```

### Step 4: Repeat

Continue the cycle for the next piece of functionality.

## TDD Workflow

```markdown
## Feature: [Name]

### Test Cases (Write in Order)

1. [ ] Test case 1: Basic happy path
2. [ ] Test case 2: Edge case
3. [ ] Test case 3: Error handling
4. [ ] Test case 4: Integration point

### Progress

| Test   | Status     | Implementation |
| ------ | ---------- | -------------- |
| Test 1 | RED        | -              |
| Test 1 | GREEN      | Done           |
| Test 1 | REFACTORED | Done           |
| Test 2 | RED        | -              |

...
```

## Example TDD Session

```
Feature: User Registration

=== Test 1: Valid registration ===

[RED] Writing test for valid registration...
test('registers user with valid data', async () => {
  const result = await register({
    email: 'test@example.com',
    password: 'SecurePass123!'
  });
  expect(result.success).toBe(true);
});
→ Run test: FAILS (register not implemented)

[GREEN] Implementing minimum code...
async function register(data) {
  return { success: true };
}
→ Run test: PASSES

[REFACTOR] Improving implementation...
async function register(data) {
  const user = await db.users.create({
    email: data.email,
    passwordHash: await hashPassword(data.password)
  });
  return { success: true, userId: user.id };
}
→ Run test: PASSES

=== Test 2: Duplicate email ===

[RED] Writing test for duplicate email...
test('rejects duplicate email', async () => {
  await register({ email: 'existing@example.com', password: 'Pass123!' });
  const result = await register({ email: 'existing@example.com', password: 'Pass123!' });
  expect(result.success).toBe(false);
  expect(result.error).toBe('Email already exists');
});
→ Run test: FAILS

[GREEN] Implementing duplicate check...
async function register(data) {
  const existing = await db.users.findByEmail(data.email);
  if (existing) {
    return { success: false, error: 'Email already exists' };
  }
  const user = await db.users.create({...});
  return { success: true, userId: user.id };
}
→ Run test: PASSES

=== All tests green! Feature complete. ===
```

## Best Practices

- **Write the test first, always** - No exceptions
- **Test behavior, not implementation** - Focus on inputs/outputs
- **Keep tests independent** - Each test should run in isolation
- **One assertion per test** (mostly) - Keep tests focused
- **Use descriptive test names** - Should read like documentation
- **Don't skip RED** - A test that passes immediately is suspicious

## Anti-Patterns to Avoid

- ❌ Writing tests after implementation
- ❌ Writing multiple tests before any implementation
- ❌ Skipping refactoring step
- ❌ Over-engineering in the GREEN phase
- ❌ Testing implementation details instead of behavior

## Token Optimization (RTK)

When running test commands in the RED and GREEN phases, always prefer using **RTK** to reduce token consumption:

- Use `rtk cargo test` instead of `cargo test`
- Use `rtk npm test` instead of `npm test`
- Use `rtk pytest` instead of `pytest`

This keeps the session context window clean and reduces costs.
