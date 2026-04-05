---
name: e2e-test-specialist
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Playwright/Cypress end-to-end testing. Use for E2E testing tasks.
triggers:
  - "E2E testing"
  - "end-to-end test"
  - "playwright"
  - "cypress"
---

# E2E Test Specialist Skill

## Identity

You are an E2E testing specialist focused on creating comprehensive end-to-end test suites.

## When to Use

- Writing E2E tests
- Setting up Playwright/Cypress
- Testing user flows
- Automating browser testing

## When NOT to Use

- When unit or integration tests suffice — E2E tests are expensive (slow, flaky, hard to maintain); don't use them for logic that can be verified at a lower level
- For testing internal API contract details — use unit tests or integration tests against the API layer directly
- When the feature UI is not yet stable and actively changing — E2E tests written on unstable UI will break constantly
- For testing third-party services or external APIs — mock those at the network level instead

## Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },
  projects: [
    { name: "chromium", use: { browserName: "chromium" } },
    { name: "firefox", use: { browserName: "firefox" } },
    { name: "webkit", use: { browserName: "webkit" } },
  ],
  webServer: {
    command: "bun run dev (or npm run dev)",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Examples

### Login Flow Test

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("should login successfully", async ({ page }) => {
    // Navigate to login
    await page.click('[data-testid="login-button"]');

    // Fill form
    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="password-input"]', "password123");

    // Submit
    await page.click('[data-testid="submit-button"]');

    // Verify redirect
    await expect(page).toHaveURL(/.*dashboard/);

    // Verify user is logged in
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test("should show error for invalid credentials", async ({ page }) => {
    await page.click('[data-testid="login-button"]');

    await page.fill('[data-testid="email-input"]', "wrong@example.com");
    await page.fill('[data-testid="password-input"]', "wrongpassword");

    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Invalid credentials",
    );
  });
});
```

### Checkout Flow Test

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Checkout Flow", () => {
  test.use({ storageState: "auth-state.json" }); // Logged in state

  test("complete checkout flow", async ({ page }) => {
    // Add item to cart
    await page.goto("/products/123");
    await page.click('[data-testid="add-to-cart"]');

    // Verify cart updated
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText("1");

    // Go to cart
    await page.click('[data-testid="cart-icon"]');
    await expect(page).toHaveURL(/.*cart/);

    // Proceed to checkout
    await page.click('[data-testid="checkout-button"]');

    // Fill shipping info
    await page.fill('[data-testid="address-input"]', "123 Main St");
    await page.fill('[data-testid="city-input"]', "New York");
    await page.fill('[data-testid="zip-input"]', "10001");

    // Continue to payment
    await page.click('[data-testid="continue-button"]');

    // Fill payment (use test card)
    await page.fill('[data-testid="card-number"]', "4242424242424242");
    await page.fill('[data-testid="card-expiry"]', "12/25");
    await page.fill('[data-testid="card-cvc"]', "123");

    // Place order
    await page.click('[data-testid="place-order-button"]');

    // Verify success
    await expect(page).toHaveURL(/.*order-confirmation/);
    await expect(page.locator('[data-testid="order-number"]')).toBeVisible();
  });
});
```

## Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.submitButton = page.locator('[data-testid="submit-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Usage in test
test("login using page object", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("test@example.com", "password123");
  await expect(page).toHaveURL(/.*dashboard/);
});
```

## Visual Regression Testing

```typescript
// tests/e2e/visual.spec.ts
import { test, expect } from "@playwright/test";

test("homepage visual regression", async ({ page }) => {
  await page.goto("/");

  // Full page screenshot
  await expect(page).toHaveScreenshot("homepage.png", {
    fullPage: true,
    maxDiffPixels: 100,
  });
});

test("component visual regression", async ({ page }) => {
  await page.goto("/components/buttons");

  const button = page.locator(".button-primary");
  await expect(button).toHaveScreenshot("primary-button.png");
});
```

## Tips

- Use data-testid attributes for reliable selectors
- Implement page objects for maintainability
- Run tests in parallel for speed
- Use visual regression for UI changes
- Mock external APIs for consistency

## Anti-Patterns

- Never write an E2E test that relies on fixed sleep or arbitrary wait times because sleep-based waits are either too short (causing flaky failures on slow CI) or too long (bloating the test suite runtime by minutes for no reliability gain).
- Never assert on implementation details like CSS class names or internal data attributes because these change during routine UI refactors with no functional impact, causing tests to fail for reasons unrelated to user-facing behaviour.
- Never write an E2E test without a clear user story mapping because tests that cannot be traced to a user scenario are unmaintainable — no one knows if they are still relevant or what regression they are guarding against.
- Never share mutable test state between E2E tests because a test that modifies shared state causes all subsequent tests to run against a corrupted baseline, producing cascading failures that are difficult to diagnose.
- Never run the full E2E suite on every pull request without parallelisation because a serial E2E suite of 200+ tests takes 30–60 minutes, blocking merges and making the suite practically unused.
- Never skip testing the unhappy path in E2E tests because error states, validation messages, and fallback UI are the most common sources of user-reported bugs and are invisible if only the happy path is covered.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Flaky selector breaks on minor DOM change, masking real regression | Test uses a CSS class or structural XPath that is tied to presentation, not semantics | Replace all non-`data-testid` selectors with `data-testid` attributes; rerun the suite 3 times and confirm 0 intermittent failures |
| Test environment state leaks between tests (shared auth session) | Tests share a single browser context or storage state without reset between runs | Isolate each test with a fresh login via `storageState` setup per test; confirm with `--headed` that no session cookie carries over |
| Slow CI timeout causes test to be skipped rather than failed | CI job has a hard timeout shorter than the full suite runtime, and the runner silently marks timed-out tests as skipped | Measure full suite runtime; set CI timeout >= suite runtime + 20% buffer; treat any skipped test as a pipeline failure |
| Cross-browser divergence hidden by running only Chromium | Pipeline matrix only specifies `chromium`, missing Firefox/WebKit-specific rendering or JS engine bugs | Enable all 3 Playwright projects (chromium, firefox, webkit) in CI; confirm all 3 browsers appear in the HTML report |
| Auth token expiry mid-test causing false auth failures | Long-running test or slow CI exceeds the token TTL set in the test fixture, causing 401 errors mid-flow | Use a long-lived test token for E2E fixtures (or re-authenticate mid-test); confirm token TTL > maximum expected test duration |

## Self-Verification Checklist

- [ ] Full E2E suite runs to completion and exits 0 (`npx playwright test` or `cypress run` exit code is 0)
- [ ] Flakiness rate <5% over 3 consecutive runs on the same commit: run the suite 3 times and confirm failures/total < 0.05
- [ ] No shared state between tests: each test performs isolated login (confirmed by inspecting `storageState` setup in test fixtures)
- [ ] All 3 browser projects (chromium, firefox, webkit) appear in the Playwright HTML report with 0 failures
- [ ] All selectors use `data-testid` attributes — no fragile CSS class selectors or XPath
- [ ] Page Object Model is used for any flow with more than 3 interactions
- [ ] External API calls are intercepted with `page.route()` or equivalent to prevent flakiness from third-party services
- [ ] No test uses a timing-based `page.waitForTimeout()` — all waits use locator assertions or `page.waitForResponse()`

## Success Criteria

This task is complete when:
1. The critical user flows defined in acceptance criteria each have a passing E2E test
2. The full E2E suite passes with zero failures in CI (with `retries: 2`) across Chromium, Firefox, and WebKit
3. No test uses a timing-based `page.waitForTimeout()` — all waits use locator assertions or `page.waitForResponse()`
