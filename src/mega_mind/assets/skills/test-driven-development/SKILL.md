---
name: test-driven-development
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
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

## When NOT to Use

- Exploratory prototyping where requirements are unknown and the goal is discovery, not delivery
- Pure configuration changes (environment variables, feature flags, YAML/JSON configs) with no logic
- One-off scripts that will never be maintained or reused
- Trivial getters/setters with no business logic — the test adds no specification value

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

## Anti-Patterns

- Never write the implementation before the test because writing implementation first biases every test you then write toward confirming what the code already does, not toward specifying what it should do, and the RED phase is never genuinely red.
- Never write a test that cannot fail because a test that always passes regardless of the implementation provides zero specification value; it counts toward coverage metrics while protecting no actual behaviour.
- Never skip the refactor step of red-green-refactor because a codebase that only receives RED and GREEN passes accumulates structural debt in every TDD cycle until the test suite itself becomes too tangled to maintain.
- Never write multiple failing tests before making them pass because multiple simultaneous failing tests make it impossible to confirm that each GREEN implementation is minimal; you cannot isolate which implementation change fixed which test.
- Never write a test that tests the framework instead of your code because a test that verifies Jest's mock system works, or that Express routes requests, is a test of the library vendor's code, not yours, and adds no safety net for your logic.
- Never accept a green test suite as proof of correctness because a green test suite proves only that the code behaves according to the tests written; it says nothing about untested behaviour, integration points, or requirements that were never translated into tests.

## Success Criteria

This skill is complete when: 1) Every new unit of functionality has at least one test written before its implementation. 2) Each RED → GREEN → REFACTOR cycle is documented and the test suite stays green throughout. 3) No implementation code was written without a failing test first — the RED phase was confirmed for every cycle.

## Failure Modes

| Failure                                                                    | Cause                                                                                                      | Recovery                                                                                                                                     |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Testing implementation details not behaviour, test breaks on safe refactor | Test asserts on internal variable names, method call counts, or private state instead of observable output | Rewrite the test to assert only on inputs and public outputs; if the test breaks on a rename, the test is testing the wrong thing            |
| Test passes but logic is wrong (false green from mocked dependency)        | Mock returns a hardcoded value that never matches production; actual integration never exercised           | Add at least one integration test (no mocks) for each critical path; use contract tests to verify mock behaviour matches the real dependency |
| Refactor step skipped under time pressure, accumulating technical debt     | Team treats RED → GREEN as done; refactor is deferred indefinitely under sprint pressure                   | Enforce the refactor step as a mandatory phase; a story is not done until the REFACTOR pass is completed and the test suite is still green   |
| Test suite too slow (>30s) for TDD red-green-refactor loop to be practical | Full integration suite runs on every `npm test`; unit tests mixed with database-hitting tests              | Separate fast unit tests from slow integration tests; ensure `npm test` runs only fast tests (<10s); run integration tests in CI only        |
| Test written after implementation, not driving design (TDD theatre)        | Developer writes implementation first, then writes a test to confirm the code they already wrote           | Verify the RED phase via `git log --oneline` — test commit must precede implementation commit; if not, rewrite using TDD retroactively       |

## Self-Verification Checklist

- [ ] Test written BEFORE implementation: `git log --oneline` shows test commit precedes implementation commit for each cycle
- [ ] All tests green after refactor step: full test suite exits 0 after each REFACTOR pass
- [ ] Test suite completes in < 30s for TDD loop: `time npm test` (or equivalent) confirms duration <= 30s
      grep -cE "FAIL|failing|red"
- [ ] GREEN implementation is minimal: `git diff --stat HEAD~1 HEAD` shows = 0 files changed beyond what the test required
- [ ] No implementation code written without a failing test: `git log --oneline` count of test commits >= count of implementation commits

## Token Optimization (RTK)

When running test commands in the RED and GREEN phases, always prefer using **RTK** to reduce token consumption:

- Use `rtk cargo test` instead of `cargo test`
- Use `rtk bun test (or rtk npm test)` instead of `bun test (or npm test)`
- Use `rtk pytest` instead of `pytest`

This keeps the session context window clean and reduces costs.
