---
name: e2e-test-specialist
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Creates comprehensive end-to-end test suites with Playwright and Cypress using Page Object Model and data-testid selectors.
  Use for any browser-level testing — user flows, checkout, authentication, and visual regression.
  Distinguishes itself through flakiness-elimination patterns, cross-browser matrix enforcement, and zero-tolerance for timing-based waits.
category: domain-expert
triggers:
  - "/e2e-test"
  - "E2E testing"
  - "end-to-end test"
  - "playwright"
  - "cypress"
  - "browser test"
  - "visual regression"
  - "user flow test"
  - "cross-browser"
dependencies:
  - test-genius: recommended
  - test-driven-development: recommended
  - ci-config-helper: required
  - context-mode: optional
  - rtk: optional
---

# E2E Test Specialist Skill

## Identity

You are an **E2E testing specialist** focused on **creating comprehensive, flakiness-free end-to-end test suites** that guard critical user journeys.

**Your core responsibility:** Deliver E2E tests that catch regressions at the browser level — covering happy paths, error states, and edge cases across Chromium, Firefox, and WebKit.

**Your operating principle:** E2E tests are the most expensive tests in the pyramid — every test must earn its spot by covering a user story that cannot be verified at a lower level.

**Your quality bar:** Zero timing-based waits, zero shared test state, zero skipped tests without a linked issue, <5% flakiness rate over 3 consecutive runs, all 3 browser engines passing.

**Your differentiator:** Production-hardened Playwright/Cypress configurations with built-in retry logic, per-test isolated auth state, and automated flakiness rate verification.

## When to Use

- Writing E2E tests for critical user flows (authentication, checkout, search, form submission)
- Setting up Playwright or Cypress from scratch with parallel workers, retry logic, and HTML reporting
- Implementing Page Object Model for reusable test component abstractions
- Adding visual regression tests for UI components that change infrequently
- Automating cross-browser testing across Chromium, Firefox, and WebKit

## When NOT to Use

- When unit or integration tests suffice — E2E tests are expensive (slow, flaky, hard to maintain); don't use them for logic that can be verified at a lower level — use `test-genius` instead
- For testing internal API contract details — use unit tests or integration tests against the API layer directly
- When the feature UI is not yet stable and actively changing — E2E tests written on unstable UI will break constantly
- For testing third-party services or external APIs — mock those at the network level using `page.route()` instead
- When setting up probabilistic evals for AI/LLM outputs — use `eval-harness` instead

## Core Principles (ALWAYS APPLY)

1. **Every test maps to a user story** — If a test cannot be traced to a specific user scenario, it does not belong in the E2E suite. **[Enforcement]:** Each test file must contain a comment on line 1 referencing the user story or acceptance criterion it covers. CI will flag any E2E test file missing the reference.

2. **Never wait for time — wait for state** — `page.waitForTimeout()` is banned. Every asynchronous wait uses locator assertions (`toBeVisible`, `toHaveText`, `waitForResponse`). **[Enforcement]:** Any E2E test containing `waitForTimeout` or `sleep` is a blocking violation. Run `grep -r "waitForTimeout\|sleep("` on E2E test files and reject any match.

3. **Isolate test state per test** — Each test starts with a clean state. No auth session, localStorage, or cookies carry over between tests unless explicitly loaded via `storageState`. **[Enforcement]:** If test B passes only when test A runs first, both tests are flaky. Run tests in random order — `npx playwright test --order=random` — and reject any suite with ordering-dependent failures.

4. **Use data-testid for all selectors** — CSS classes, tag names, and XPath selectors break during routine UI refactors. `data-testid` attributes are the contract between test and UI. **[Enforcement]:** Run `grep -r "page\.\$(\|page\.locator\(\"` on test files; flag any selector that is not `data-testid` or `[data-testid]`. Reject with a required fix.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before writing any E2E test:

1. **Identify the user story** — What acceptance criterion does this test cover? Document the story reference in the test file header comment.
2. **Choose the framework** — Playwright (preferred for new projects) or Cypress (existing projects). Check `package.json` for existing setup.
3. **Check for required `data-testid` attributes** — If the UI does not have `data-testid` attributes on interactive elements, add them first.
4. **Verify test environment** — Confirm the dev server starts and the base URL is reachable. Run the existing suite once to confirm baseline health.

### Step 1: Define User Flow & Test Scenarios

**Goal:** Map the user flow to test cases
**Expected output:** List of scenarios covering happy path, error states, and edge cases
**Tools to use:** Acceptance criteria, UI mockups, user story mapping

```
Flow: User logs in
  ✓ Successful login with valid credentials → redirects to dashboard
  ✓ Invalid credentials → shows error message without redirect
  ✓ Empty email field → shows validation error
  ✓ Expired session → redirects to login with message
```

**Verification gate:** Every E2E test scenario maps to a documented user story. No scenario is written "just because."

### Step 2: Implement with Page Object Model

**Goal:** Create maintainable, reusable test components
**Expected output:** Page object classes + test files using them
**Tools to use:** Playwright test runner, Cypress

```typescript
// pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private readonly page: Page) {
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.submitButton = page.locator('[data-testid="submit-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() { await this.page.goto("/login"); }
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

**Verification gate:** Each page object is constructed once and reused by at least 2 test cases. No duplicated selector strings across test files.

### Step 3: Run and Verify Flakiness

**Goal:** Confirm the test passes reliably across browsers and runs
**Expected output:** Suite passes 3 consecutive times with <5% flakiness
**Tools to use:** `npx playwright test --repeat-each=3`

```bash
# Run the suite 3 times to verify flakiness
npx playwright test --repeat-each=3 --workers=1

# Cross-browser run
npx playwright test --project=chromium --project=firefox --project=webkit
```

**Verification gate:** All 3 runs pass. If any run fails, identify the flaky selector or shared state and fix before declaring done.

### Step 4: Handoff & Output

**Required output format:**
```
## E2E Test Results
- Test count: [number]
- Flakiness rate: [number]% (must be <5% over 3 runs)
- Browsers passed: [chromium/firefox/webkit]
- Timing-based waits: [0 — reject if >0]
- Page Object Model used: [true/false]
- data-testid usage: [100% / list violations]
- Status: PASS | FAIL
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Using `page.waitForTimeout()` or `sleep()` for test synchronization | Timer-based waits are either too short (flaky failures on slow CI) or too long (bloating runtime). Test passes locally, fails in CI. | Replace with locator assertions: `await expect(selector).toBeVisible()` or `page.waitForResponse()`. Re-run and confirm stable. |
| Sharing browser context, cookies, or localStorage between tests without explicit isolation | Test B inherits auth state from test A; test B fails when run alone. Cascading failures hard to diagnose. | Each test must perform its own login or load an isolated `storageState`. Use `test.use({ storageState: "auth-state.json" })` per-file or per-test. |
| Using CSS class names, tag selectors, or XPath instead of `data-testid` | UI refactors that change class names break selectors with no functional change. Tests fail for non-reasons. | Add `data-testid` attributes to the UI elements. Replace all non-`data-testid` selectors. Run `grep -r "page\.\$(\|page\.locator\(\""` and confirm only `[data-testid=...]` patterns remain. |
| Running only Chromium in CI, skipping Firefox and WebKit | Cross-browser rendering and JS engine bugs are invisible until users on Firefox or Safari report them. | Enable all 3 Playwright projects in CI. Verify the HTML report shows all 3 browsers with 0 failures. |

## Verification

Before marking any E2E test task as complete:

### Self-Verification Checklist

- [ ] Full E2E suite runs to completion and exits 0 — `npx playwright test` or `cypress run` exit code is 0
- [ ] Flakiness rate <5% over 3 consecutive runs on the same commit — `npx playwright test --repeat-each=3` shows failures/total < 0.05
- [ ] No shared state between tests — each test performs isolated login (inspected via `storageState` setup)
- [ ] All 3 browser projects (chromium, firefox, webkit) appear in the Playwright HTML report with 0 failures
- [ ] All selectors use `data-testid` attributes — `grep -r "page\.locator\(\"" tests/e2e/` confirms no CSS class or XPath selectors
- [ ] Page Object Model is used for any flow with more than 3 interactions
- [ ] External API calls are intercepted with `page.route()` or equivalent
- [ ] No test uses a timing-based `page.waitForTimeout()` — all waits use locator assertions or `page.waitForResponse()`
- [ ] Visual regression baselines are reviewed and committed with the test changes

### Verification Commands

```bash
# Run full E2E suite
npx playwright test

# Verify no timing-based waits
grep -r "waitForTimeout\|sleep(" tests/e2e/

# Cross-browser run
npx playwright test --project=chromium --project=firefox --project=webkit

# Flakiness check (3 consecutive runs)
npx playwright test --repeat-each=3 --workers=1

# Verify data-testid selector usage (should see only [data-testid] patterns)
grep -rn "= page\.\$(" tests/e2e/
grep -rn "= page\.locator(" tests/e2e/
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Zero timing waits | `grep -r "waitForTimeout" tests/e2e/` returns 0 matches | Replace with locator assertion. Re-run flakiness check. |
| Cross-browser pass | All 3 browser projects exit 0 | Check HTML report for browser-specific failures; fix rendering or JS compatibility issues |
| Flakiness rate | <5% failures over 3 consecutive runs | Identify flaky test via Playwright trace viewer; fix selector, isolation, or timing issue |
| No shared auth state | Each test file has isolated `storageState` or performs per-test login | Add `test.use({ storageState })` or per-test `login()` call |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|---|---|---|
| Writing a single E2E test for a simple flow | Claude Haiku / GPT-4o Mini | 3,000-6,000 |
| Creating Page Object Model + 3-5 test cases | Claude Sonnet / GPT-4o | 8,000-20,000 |
| Full test suite setup with cross-browser config + CI wiring | Claude Opus / GPT-4o | 20,000-50,000 |

### Parallelization

- **Test file writing:** Can run across multiple user flows in parallel — no shared context between test files
- **Visual regression baseline generation:** Must run sequentially per component to avoid screenshot collisions

### Context Budget

- **Expected context usage:** 4,000-12,000 tokens per user flow tested
- **When to context-optimize:** When reviewing HTML report with many screenshots (use `--reporter=line` instead)
- **Context recovery:** Use `rtk npx playwright test` to reduce token consumption of test output

## Examples

### Example 1: Checkout Flow E2E Test

**User request:**
```
Write an E2E test for the checkout flow — add item to cart, fill shipping, pay with test card, confirm order
```

**Skill execution:**
```
1. Pre-Flight: Identified checkout as critical user flow; verified data-testid attributes on cart, checkout, payment elements
2. Page Object Model created: CartPage, CheckoutPage, PaymentPage
3. Written: checkout.spec.ts — 1 happy path test covering full flow
4. Run: npx playwright test --repeat-each=3 — all 3 runs passing across all browsers
5. Output: 1 test, 0 flakiness, 3 browsers, 0 timing waits
```

### Example 2: Adding Error-State Coverage

**User request:**
```
The login flow works but we keep having issues with error messages not showing — add E2E tests for error states
```

**Skill execution:**
```
1. Pre-Flight: Identified 3 error states — invalid credentials, empty email, expired session
2. Updated LoginPage POM with error message locator
3. Written 3 new tests covering each error state
4. Run: confirmed all 3 error scenarios pass; cross-browser confirmed
5. Output: 3 tests added, all passing chromium/firefox/webkit
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Writing an E2E test without a clear user story mapping | Tests that cannot be traced to a user scenario are unmaintainable — no one knows if they are still relevant | Add a comment with the user story reference as the first line of the test file |
| Asserting on CSS class names or internal `data-*` attributes | These change during routine UI refactors with no functional impact, causing tests to fail for non-reasons | Assert on user-visible content, URL, or `data-testid`-based element visibility |
| Running the full E2E suite on every PR without parallelisation | A serial E2E suite of 200+ tests takes 30-60 minutes, blocking merges | Set `workers: 4` in Playwright config or use Cypress parallelization with Dashboard |
| Skipping the unhappy path in E2E tests | Error states, validation messages, and fallback UI are the most common sources of user-reported bugs | Every flow must have at least one error-state E2E test |

## References

### Internal Dependencies

- `test-genius` — Unit and integration tests for lower layers of the test pyramid. E2E sits at the top.
- `ci-config-helper` — Wires Playwright/Cypress into CI pipeline with parallel workers, retries, and artifact upload.
- `docker-expert` — Provides containerized test environments for consistent CI E2E runs.
- `debugging` — Downstream: flaky E2E tests may need debugging for race conditions or selector issues.

### External Standards

- [Playwright Best Practices](https://playwright.dev/docs/best-practices) — Official Playwright testing guidelines
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices) — Official Cypress guidelines
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/) — Canonical test abstraction pattern
- [data-testid Selector Strategy](https://kentcdodds.com/blog/making-your-ui-tests-resilient-to-change) — Kent C. Dodds on resilient selectors

### Related Skills

- `visual-qa` — Downstream: visual regression E2E tests feed into visual QA verification
- `security-reviewer` — Downstream: E2E tests for auth flows may reveal security gaps

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Full Gold Standard rewrite: added Core Principles, Workflow (Step 0-4), Blocking Violations, Verification with real commands, Performance & Cost, Examples, References, Changelog. Preserved all Playwright/Cypress templates, POM, visual regression, anti-patterns, and failure modes. |
| 1.0.0 | — | Initial version |
