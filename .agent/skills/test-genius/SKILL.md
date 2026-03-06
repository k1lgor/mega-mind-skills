---
name: test-genius
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
