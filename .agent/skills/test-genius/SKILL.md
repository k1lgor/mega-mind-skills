---
name: test-genius
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Writing unit tests and increasing coverage. Use for all testing-related tasks.
triggers:
  - "write tests"
  - "add test coverage"
  - "unit tests"
  - "test this code"
---

# Test Genius Skill

## Identity

You are a testing specialist focused on writing comprehensive, maintainable tests.

## When to Use

- Writing unit tests
- Increasing code coverage
- Writing integration tests
- Test-driven development

## When NOT to Use

- You are practicing TDD and need to write tests BEFORE implementation — use `test-driven-development` skill instead (this skill assumes code already exists)
- You are writing E2E browser tests — use `e2e-test-specialist` instead
- The code being tested is not yet finalized and likely to change significantly (tests written now will be thrown away)
- You are auditing test quality on a large codebase without a specific coverage gap — use `skill-stocktake` for that

## Testing Philosophy

```
Good tests are:
1. Fast - Run in milliseconds
2. Isolated - No external dependencies
3. Repeatable - Same result every time
4. Self-validating - Pass or fail clearly
5. Timely - Written close to the code
```

## Test Structure

### AAA Pattern

```javascript
describe("calculateTotal", () => {
  it("should calculate total with tax", () => {
    // Arrange
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 },
    ];
    const taxRate = 0.1;

    // Act
    const result = calculateTotal(items, { taxRate });

    // Assert
    expect(result).toBe(38.5);
  });
});
```

## Unit Test Templates

### Testing Functions

```javascript
describe("functionName", () => {
  // Happy path
  it("should [expected behavior] when [condition]", () => {
    const input = createValidInput();
    const result = functionName(input);
    expect(result).toEqual(expectedOutput);
  });

  // Edge cases
  it("should handle empty input", () => {
    const result = functionName([]);
    expect(result).toEqual([]);
  });

  // Error cases
  it("should throw error when input is invalid", () => {
    expect(() => functionName(null)).toThrow("Input is required");
  });
});
```

### Testing Classes

```javascript
describe("UserService", () => {
  let service;
  let mockRepository;

  beforeEach(() => {
    mockRepository = {
      findById: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };
    service = new UserService(mockRepository);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("getUser", () => {
    it("should return user when found", async () => {
      mockRepository.findById.mockResolvedValue({ id: 1, name: "John" });

      const result = await service.getUser(1);

      expect(result).toEqual({ id: 1, name: "John" });
      expect(mockRepository.findById).toHaveBeenCalledWith(1);
    });

    it("should throw NotFoundError when user not found", async () => {
      mockRepository.findById.mockResolvedValue(null);

      await expect(service.getUser(999)).rejects.toThrow(NotFoundError);
    });
  });
});
```

### Testing Async Code

```javascript
describe("async operations", () => {
  it("should handle successful promise", async () => {
    const result = await fetchData();
    expect(result).toBeDefined();
  });

  it("should handle rejected promise", async () => {
    await expect(fetchFailingData()).rejects.toThrow("Network error");
  });

  it("should handle timeouts", async () => {
    await expect(slowOperation()).rejects.toThrow("Timeout");
  }, 5000); // Set timeout to 5 seconds
});
```

### Testing API Endpoints

```javascript
describe("POST /api/users", () => {
  it("should create user with valid data", async () => {
    const response = await request(app).post("/api/users").send({
      name: "John Doe",
      email: "john@example.com",
    });

    expect(response.status).toBe(201);
    expect(response.body).toMatchObject({
      name: "John Doe",
      email: "john@example.com",
    });
  });

  it("should return 400 for invalid email", async () => {
    const response = await request(app).post("/api/users").send({
      name: "John Doe",
      email: "invalid-email",
    });

    expect(response.status).toBe(400);
    expect(response.body.error).toContain("email");
  });
});
```

## Mocking Strategies

### Mocking Functions

```javascript
// Using Jest
jest.mock("../utils/logger");
const logger = require("../utils/logger");

it("should log on error", () => {
  processError(new Error("test"));
  expect(logger.error).toHaveBeenCalledWith("Error: test");
});
```

### Mocking Modules

```javascript
jest.mock("axios");
const axios = require("axios");

it("should fetch data", async () => {
  axios.get.mockResolvedValue({ data: { id: 1 } });

  const result = await fetchUser(1);

  expect(result).toEqual({ id: 1 });
});
```

### Mocking Time

```javascript
jest.useFakeTimers();

it("should call callback after delay", () => {
  const callback = jest.fn();
  scheduleCallback(callback, 1000);

  expect(callback).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});
```

## Coverage Guidelines

| Type       | Target | Notes                |
| ---------- | ------ | -------------------- |
| Lines      | 80%    | Minimum acceptable   |
| Branches   | 75%    | All decision paths   |
| Functions  | 90%    | All public functions |
| Statements | 80%    | All executable code  |

## Test File Organization

```
src/
├── services/
│   └── user.service.ts
└── __tests__/
    └── services/
        └── user.service.test.ts
```

## Tips

- One concept per test
- Use descriptive test names
- Don't test implementation details
- Test behavior, not code
- Keep tests simple and readable
- Use test data builders for complex objects

## Anti-Patterns

- Never write a test that doesn't assert anything because a test with no assertion always passes regardless of whether the feature works, creating false confidence in the test suite.
- Never mock the system under test because mocking the code being tested means the test exercises the mock, not the implementation; the test will pass even when the real code is completely broken.
- Never delete a failing test to fix CI because deleting a test removes the only evidence that a bug exists; the underlying problem remains and will manifest in production.
- Never write tests after implementation as a formality because tests written after the fact are biased toward confirming what the code does, not specifying what it should do; they miss the failure cases the implementation never considered.
- Never couple a test to implementation details because a test that asserts on internal variable names, private methods, or call counts breaks on safe refactors and forces the developer to update tests whenever the internals change.
- Never write a test that passes when the feature is not implemented because a test that passes on an empty implementation is not testing anything; the RED phase must be confirmed before any implementation is written.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Test suite passes at 100% coverage but misses integration failure between units | Unit tests mock all collaborators; no test exercises the real wiring between components | Add integration tests for critical component boundaries without mocks; verify the real dependency contract is exercised |
| Mocked dependency diverges from real implementation, hiding contract breakage | Mock was written once and never updated when the real API changed; tests pass but production breaks | Add contract tests (e.g., Pact) or in-process integration tests that call the real dependency; run them in CI |
| Flaky test marked `skip` instead of fixed, masking real intermittent failure | Developer adds `.skip` or `xit` to stop CI failing; underlying non-determinism never resolved | Require every skipped test to have an issue tracker reference in the skip comment; ban `skip` without a linked ticket in CI |
| Test data factory produces invalid state that real users can't reach | Factory shortcuts validation; creates objects that bypass domain invariants | Review test factory output against the domain model; ensure factories go through the same validation path as production code |
| Snapshot test updated blindly without reviewing diff, approving regression | Developer runs `jest --updateSnapshot` to clear failing snapshots without reading the diff | Require snapshot diffs to be reviewed before committing; treat snapshot updates as code changes, not CI noise |

## Self-Verification Checklist

- [ ] Coverage ≥80% — `jest --coverage` (or `vitest --coverage`) exits 0 and reports line coverage ≥80% for changed modules
- [ ] No tests marked `skip` without an issue tracker reference — `grep -r "\.skip\|xit\|xdescribe" tests/` shows 0 results without a linked issue comment
- [ ] All mocked dependencies have contract tests — each mock has a corresponding integration or contract test verifying the mock matches reality
- [ ] All edge cases are covered: empty inputs, null/undefined, boundary values, and error paths each have a dedicated test
- [ ] Tests are isolated: no test depends on another test's state or shared mutable variables
- [ ] Async tests properly await results and assert on resolved/rejected values, not promises

## Success Criteria

This task is complete when:
1. All new or changed functions have at least one passing test covering the happy path and one covering the primary error path
2. `jest --coverage` (or project-equivalent) reports no decrease in line/branch coverage from the baseline
3. The full test suite runs to completion with zero failures
