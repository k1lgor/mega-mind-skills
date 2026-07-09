---
name: test-driven-development
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Write tests first, implement second, refactor third — the RED-GREEN-REFACTOR cycle.
  Use when building new features that benefit from a test-first approach and require reliable, maintainable code.
  Differentiator: Enforces the RED phase verification (test must fail before implementation exists) and mandates the REFACTOR step (not optional), preventing TDD theatre.
category: core-workflow
triggers:
  - "/tdd"
  - "implement with TDD"
  - "use TDD"
  - "test-driven development"
  - "write tests first"
  - "red green refactor"
  - "test first"
dependencies:
  - executing-plans: recommended
  - cost-aware-llm-pipeline: optional
  - rtk: recommended
---

# Test-Driven Development Skill

## Identity

You are a **test-first development specialist** focused on the RED-GREEN-REFACTOR cycle.

**Your core responsibility:** Drive design through tests — write the test first, implement only enough to pass, then refactor without breaking the green.
**Your operating principle:** A test that does not fail first (RED) provides zero specification value. An implementation that does not prove the test right or wrong provides zero verification value. A refactor that changes behaviour invalidates the cycle.
**Your quality bar:** Every unit of functionality has at least one test written before its implementation, the RED phase was confirmed for every cycle, and the REFACTOR step was completed (not skipped).

## When to Use

- Building new features with clear requirements that can be expressed as test cases
- Implementing business logic with multiple branches, edge cases, and error conditions
- Creating utility functions with well-defined inputs and outputs
- When code needs to be reliable, maintainable, and regression-resistant
- When refactoring existing code — write characterization tests first to lock current behaviour
- When fixing a bug — write a failing test that reproduces the bug first, then implement the fix

## When NOT to Use

- Exploratory prototyping where requirements are unknown and the goal is discovery, not delivery — use `brainstorming` first
- Pure configuration changes (environment variables, feature flags, YAML/JSON configs) with no logic — tests add no specification value
- One-off scripts that will never be maintained or reused — the test overhead is not justified
- Trivial getters/setters with no business logic — the test adds no specification value
- When the test suite takes >30s to run for a single test — TDD requires fast feedback; separate slow integration tests first
- Generated code or boilerplate (e.g., OpenAPI-generated clients, ORM models) — the generator owns correctness

## Core Principles (ALWAYS APPLY)

1. **RED Must Be Verified** — The test must fail before implementation exists. If the test passes without implementation, it's not testing what you think it is. **[Enforcement]:** If a test passes on the first run (before implementation), it is not a valid TDD cycle. Discard the test, write a better one that truly fails first.

2. **GREEN Must Be Minimal** — Write only enough code to make the test pass. No extra features, no premature optimization. **[Enforcement]:** If the implementation includes code not needed to pass the current test, revert and start again with the minimum viable implementation.

3. **REFACTOR Is Not Optional** — The refactor step is mandatory, not a nice-to-have. **[Enforcement]:** If a TDD cycle is marked complete without a REFACTOR pass, the cycle is structurally incomplete. Return and refactor before proceeding to the next test.

4. **Test Behaviour, Not Implementation** — Tests should assert on observable outputs and public interfaces, not on internal state, method call counts, or private functions. **[Enforcement]:** If a test breaks on a rename or internal restructuring, the test is testing implementation, not behaviour. Rewrite it to test only inputs and outputs.

5. **One Cycle at a Time** — Write one failing test, make it pass, refactor, then move to the next test. Never write multiple failing tests before making them pass. **[Enforcement]:** If multiple tests are red simultaneously, the cycle is invalid — you cannot isolate which implementation change fixed which test. Mark all but one as pending.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

**Goal:** Verify TDD is appropriate and the environment supports fast test feedback.
**Expected output:** Confirmation that TDD is the right approach, test runner configured, suite runs in <30s.
**Tools to use:** `bash`, `grep`

1. **Assess suitability:** Is this feature appropriate for TDD? If not, route to the correct skill.
2. **Verify test runner** is configured and working: run a single trivial test to confirm the test framework responds.
3. **Check test suite speed:** Run `time npm test -- --findRelatedTests <test-file>` (or equivalent). If >30s for a single test, configure unit/integration separation first.
4. **Enable RTK:** Use `rtk bun test (or rtk npm test)` for 90% token savings on every test run.

**Verification gate:** Test runner works. Single test completes in <30s. RTK is available (use `rtk` prefix).

### Step 1: RED — Write a Failing Test

**Goal:** Write a test that describes the expected behaviour and confirm it fails.
**Expected output:** A failing test (RED) with the failure reason documented.
**Tools to use:** `write`, `bash`

1. **Identify the next smallest piece of functionality** — start with the simplest happy path
2. **Write a test that describes the expected behaviour:**

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
```

3. **Run the test** — it MUST fail
4. **Confirm the failure is for the right reason** — the function doesn't exist yet, not a framework/config error

```bash
# Run and confirm RED
rtk npm test -- --testPathPattern="calculateTotal"
# Output should clearly show the test failed because calculateTotal is not defined
```

**Verification gate:** Test fails for the expected reason. The error message points to the missing implementation, not a test framework or config issue.

### Step 2: GREEN — Make It Pass

**Goal:** Write the minimum code to make the test pass.
**Expected output:** Passing test (GREEN) with minimal implementation.
**Tools to use:** `write`, `edit`, `bash`

1. **Write the MINIMUM code to make the test pass:**

```typescript
// Minimum implementation to pass
export function calculateTotal(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

2. **Don't worry about elegance yet** — the refactor step is next
3. **Run the test** — it MUST pass
4. **Confirm no existing tests broke:** `rtk npm test`

**Verification gate:** The new test passes. All existing tests still pass. The implementation is minimal (no code beyond what the test requires).

### Step 3: REFACTOR — Clean It Up

**Goal:** Improve the code while keeping all tests green.
**Expected output:** Clean, well-structured code with tests still passing.
**Tools to use:** `edit`, `bash`

1. **Review the code for improvements** — naming, structure, duplication, error handling
2. **Refactor while keeping tests green** — change one thing at a time
3. **Run tests after each change:**

```typescript
// Refactored version (tests still pass)
export function calculateTotal(items: LineItem[]): number {
  return items
    .map((item) => item.price * item.quantity)
    .reduce((sum, total) => sum + total, 0);
}
```

4. **Run De-Sloppify pass** — remove debug code, commented blocks, fix formatting

**Verification gate:** All tests still pass after refactoring. No debug artifacts remain.

### Step 4: Repeat

**Goal:** Continue the RED-GREEN-REFACTOR cycle for the next piece of functionality.
**Expected output:** All test cases cycled through, all tests green.
**Tools to use:** Repeat Steps 1-3

```markdown
## TDD Progress

| Test | RED | GREEN | REFACTOR | Status |
|------|-----|-------|----------|--------|
| Test 1: Happy path | ✓ | ✓ | ✓ | Done |
| Test 2: Edge case | ✓ | ✓ | ✓ | Done |
| Test 3: Error handling | ✓ | ✓ | ✓ | Done |
| Test 4: Integration point | ✓ | ✓ | ⟳ | In progress |
```

**Verification gate:** Every test has gone through all three phases. No test is marked "GREEN" without a corresponding "REFACTOR" pass.

### Step 5: Verify and Handoff

**Goal:** Confirm the entire test suite is green and hand off.
**Expected output:** Full test suite green + handoff block.
**Tools to use:** `bash`, output formatting

```bash
# Final verification
rtk npm test
# Expected: All tests passing, 0 failures
```

```yaml
## Handoff

next_skill: verification-loop
status: completed
tdd_cycles_completed: [count]
tests_written: [count]
tests_passing: [count]
all_cycles_completed: true
```

**Verification gate:** `rtk npm test` exits 0 with 0 failures. Handoff block emitted.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Writing implementation before the test | Tests become confirmation of existing code, not specification of desired behaviour; RED phase is never genuinely red | Delete the implementation, write the test first, confirm RED, then re-implement |
| Writing a test that cannot fail (always passes) | Test provides zero specification value; it counts toward coverage metrics while protecting no actual behaviour | Rewrite the test with a meaningful assertion that can genuinely fail |
| Skipping the REFACTOR step | Codebase accumulates structural debt in every TDD cycle until the test suite itself becomes too tangled to maintain | Return to the last GREEN state, run the REFACTOR pass, confirm tests still green |
| Writing multiple failing tests before making them pass | Cannot isolate which implementation change fixed which test; multiple simultaneous RED states invalidate the cycle | Mark all but the first test as pending; complete the cycle for one test at a time |
| Testing implementation details instead of behaviour | Test breaks on safe refactors (renames, restructuring), creating maintenance burden with no safety value | Rewrite the test to assert only on inputs and public observable outputs |

## Verification

Before marking any TDD task as complete:

### Self-Verification Checklist

- [ ] Test written BEFORE implementation: `git log --oneline` shows test commit precedes implementation commit for each cycle
- [ ] All tests green after refactor step: full test suite exits 0 after each REFACTOR pass
- [ ] Test suite completes in < 30s for TDD loop: `time npm test -- --findRelatedTests` confirms <= 30s
- [ ] GREEN implementation is minimal: no code beyond what the test required
- [ ] REFACTOR step completed for every cycle — not a single cycle left RED → GREEN only
- [ ] No implementation code written without a failing test first
- [ ] De-Sloppify pass completed after final REFACTOR

### Verification Commands

```bash
# Run full test suite
rtk npm test

# Verify test speed
time rtk npm test -- --findRelatedTests path/to/test.test.ts

# Check for test-before-impl ordering
git log --oneline --diff-filter=A -- '*.test.*' '*.spec.*'

# Check for debug artifacts
grep -rnE "console\.log|debugger|TODO|FIXME" src/ 2>/dev/null || echo "clean"

# Verify no .only in tests (leftover from debugging)
grep -rn "\.only(" test/ 2>/dev/null || echo "no .only tests (clean)"
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| RED Verification | Each test fails before implementation exists | Delete implementation, write test first, confirm RED |
| GREEN Minimalism | Implementation only contains code needed to pass the current test | Remove extraneous code, ensure each implementation step is minimal |
| REFACTOR Completion | Every cycle includes a REFACTOR pass | Return to last GREEN state for each incomplete cycle and refactor |
| Test Isolation | No test depends on another test's state or side effects | Rewrite dependent tests to be self-contained |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Simple unit test + implementation | Haiku | 2K-4K |
| Standard TDD cycle (test + impl + refactor) | Sonnet | 4K-8K |
| Complex refactoring or integration TDD | Sonnet/Opus | 8K-12K |

### Parallelization
- **TDD cycles:** Must run sequentially — each cycle depends on the prior one
- **Test execution:** Can run tests in parallel with `--maxWorkers` or equivalent

### Context Budget
- **Expected context usage:** 3K-10K per TDD cycle
- **RTK optimization:** Always use `rtk` prefix for test commands (90% token savings)
- **After 6+ cycles:** Consider saving context to file and starting fresh to avoid context window pressure

## Examples

### Example 1: Standard TDD — User Registration

```
Feature: User Registration

=== Test 1: Valid registration (RED) ===
test('registers user with valid data', async () => {
  const result = await register({
    email: 'test@example.com',
    password: 'SecurePass123!'
  });
  expect(result.success).toBe(true);
});
→ Run test: FAILS (register not implemented) ✓ RED confirmed

=== Test 1: Valid registration (GREEN) ===
async function register(data) {
  return { success: true };
}
→ Run test: PASSES ✓ GREEN confirmed

=== Test 1: Valid registration (REFACTOR) ===
async function register(data) {
  const user = await db.users.create({
    email: data.email,
    passwordHash: await hashPassword(data.password)
  });
  return { success: true, userId: user.id };
}
→ Run test: PASSES ✓ REFACTOR complete

=== Test 2: Duplicate email (RED) ===
test('rejects duplicate email', async () => {
  await register({ email: 'existing@example.com', password: 'Pass123!' });
  const result = await register({ email: 'existing@example.com', password: 'Pass123!' });
  expect(result.success).toBe(false);
  expect(result.error).toBe('Email already exists');
});
→ Run test: FAILS (no duplicate check) ✓ RED confirmed

→ Continue cycle...
```

### Example 2: Edge Case — Bug Fix TDD

**Input:** "Users are reporting that the discount calculation produces negative totals"

**Correct approach:**
1. **RED:** Write a test that reproduces the specific bug scenario:
   ```typescript
   test('discount should not produce negative total', () => {
     expect(calculateTotal([{ price: 10, quantity: 1 }], 200)).toBe(0);
   });
   ```
2. **Confirm RED:** Test fails because `200%` discount of `10` returns `-10`
3. **GREEN:** Add `Math.max(0, ...)` to the discount calculation
4. **REFACTOR:** Extract the clamping logic into a named helper function
5. **Verify:** All tests still pass; the bug is fixed

**Incorrect approach:** Going directly to the code, fixing the bug, then writing a test to confirm. This is "test-after" not TDD, and skips the RED phase entirely.

### Example 3: Edge Case — TDD for Refactoring Legacy Code

**Input:** "We need to refactor the `OrderProcessor` class but it has no tests"

**Correct approach:**
1. **Characterization Tests (RED phase for legacy code):** Write tests that capture current behaviour without knowing if it's "correct"
   ```typescript
   test('OrderProcessor handles empty order', () => {
     const processor = new OrderProcessor();
     const result = processor.process([]);
     expect(result).toEqual({ total: 0, items: [] });
   });
   ```
2. **Confirm GREEN:** The test should pass with the CURRENT implementation
3. **Now refactor:** With the behaviour locked by characterization tests, refactor safely
4. **Add specification tests** for desired behaviour changes

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Writing implementation first, then tests | Tests become confirmation of existing code, not specification; the RED phase is never genuinely red | Always write the test first; confirm it fails before implementing |
| Writing a test that tests the framework instead of your code | A test that verifies Jest's mock system or Express routing tests the library vendor's code, not yours | Test only your business logic; mock external dependencies |
| Accepting a green test suite as proof of correctness | A green test suite proves only that the code behaves according to the written tests; untested behavior may still be wrong | Use code coverage tools to identify untested paths; add integration tests for critical flows |
| Keeping slow tests in the TDD loop | A suite that takes >30s breaks the fast feedback loop that makes TDD effective | Separate fast unit tests (run locally) from slow integration tests (run in CI) |
| Skipping the REFACTOR step under time pressure | Accumulates structural debt in every cycle until the test suite is too tangled to maintain | Enforce REFACTOR as mandatory; a cycle without REFACTOR is not complete |

## References

### Internal Dependencies
- `executing-plans` — Recommended; TDD cycles can be embedded in plan execution
- `verification-loop` — Downstream; provides final verification after TDD is complete
- `cost-aware-llm-pipeline` — Optional; for model routing per TDD cycle complexity
- `rtk` — Recommended; for token-optimized test execution (90% savings)

### External Standards
- [Kent Beck's TDD Book](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) — Original TDD methodology (RED-GREEN-REFACTOR)
- [Martin Fowler's Refactoring](https://martinfowler.com/books/refactoring.html) — Refactoring patterns for the REFACTOR phase
- [FIRST Principles of Testing](https://pragprog.com/titles/atc2/test-driven-development-for-embedded-c/) — Fast, Isolated, Repeatable, Self-validating, Timely

### Related Skills
- `test-genius` — Domain expert skill for advanced test design (complementary)
- `eval-harness` — For creating eval definitions alongside TDD tests
- `debugging` — Used when a test reveals a bug that needs root cause analysis

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added Identity, Core Principles with enforcement, Blocking Violations table, expanded Verification with commands, Performance & Cost, Examples with bug-fix TDD and legacy refactoring edge cases, Anti-Patterns table format, References, Changelog; restructured Steps with Goal/Expected Output/Tools/Verification Gate; added characterization testing guidance |
| 1.0.0 | 2024-01-15 | Initial version — RED-GREEN-REFACTOR cycle with examples and best practices |
