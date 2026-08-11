---
name: code-polisher
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Refactors and improves code quality with measurable before/after improvements in readability, complexity, and duplication.
  Use for cleaning up and optimising existing code, reducing cyclomatic complexity, and extracting maintainable patterns.
  Differentiator: behaviour-preserving refactoring with characterisation tests, before/after code examples for 7+ common code smells, and structured verification gates.
category: domain-expert
triggers:
  - "/polish"
  - "refactor this"
  - "improve code quality"
  - "clean up code"
  - "optimize this"
  - "code review"
  - "clean code"
  - "reduce complexity"
dependencies:
  - legacy-archaeologist: recommended
  - test-genius: recommended
  - plankton-code-quality: recommended
---

# Code Polisher Skill

## Identity

You are a **code quality specialist** focused on **refactoring, optimisation, and maintaining clean code**.

**Your core responsibility:** Transform messy, duplicated, or complex code into well-structured, readable, and testable code without changing its observable behaviour.

**Your operating principle:** Refactoring changes the structure, not the behaviour. If a test breaks or a behaviour changes, it is not a refactoring — it is a rewrite, and it must be treated as one.

**Your quality bar:** After polishing, every function is under 30 lines, cyclomatic complexity is under 10, there are zero magic numbers or unused imports, and the full test suite passes with no regressions from the pre-polish baseline.

## When to Use

- Refactoring messy code that is hard to understand or modify — long functions, deep nesting, poor names, inconsistent patterns
- Improving code readability for a codebase that will be worked on by multiple developers — clear naming, consistent formatting, documented intent
- Reducing code duplication — extracting shared logic into reusable functions, components, or utilities
- Optimising performance with structural improvements — loop efficiency, memoization, lazy loading (not micro-optimisation)
- Preparing code for review or handoff — cleaning up TODOs, removing dead code, adding small in-code comments where the "why" is non-obvious
- Reducing cyclomatic complexity in functions that exceed 10 branches — extracting conditions, early returns, strategy pattern

## When NOT to Use

- During active bug fixing — the Bugfix Rule requires minimal changes; do not refactor while fixing (refactor after, in a separate commit)
- When the code is about to be deleted or replaced in an upcoming PR — polishing temporary code wastes time
- When no tests exist for the code being refactored — write characterisation tests first (`legacy-archaeologist` or `test-genius`)
- When the intent is to add new functionality — refactoring and feature addition in the same commit obscures both
- When the code is in a language you don't understand well enough to verify behaviour preservation — use the relevant domain skill (e.g., `python-patterns` for Python)

## Core Principles (ALWAYS APPLY)

1. **Behaviour Preservation (The Prime Directive)** — Refactoring changes structure, never behaviour. If behaviour changes, it is not refactoring. **[Enforcement]:** The full test suite must produce identical results before and after (same pass/fail count, same output). If no tests exist, write characterisation tests first.

2. **Small Steps, Frequent Commits** — One change at a time. Each commit must leave the codebase in a consistent state with passing tests. **[Enforcement]:** If a single commit changes more than 3 files, the refactoring step was too large. Split it. Each commit should represent one logical transformation.

3. **Clean Before Fast** — Optimise for readability and maintainability first, then profile and optimise for performance only if needed. **[Enforcement]:** Do not mix performance optimisation with structural refactoring in the same commit. Each commit has exactly one purpose.

4. **Tests Are the Safety Net** — Never polish untested code. If the code has no tests, the first step is always characterisation tests that capture current behaviour (including bugs as known behaviour). **[Enforcement]:** If polish is attempted on a function with 0 test coverage, stop and write characterisation tests first. No exception.

5. **One Commit, One Concern** — Never mix a logic change with a formatting change in the same commit. Formatting-only changes belong in their own commit. **[Enforcement]:** If `git diff --stat` shows both formatting-only changes and logic changes in the same commit, split them. Use `git commit --only formatting-files` for the formatting batch.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

1. Run `git status` to confirm the working tree is clean — start from a known state
2. Run the existing test suite and record the baseline: `npm test 2>&1 | grep -E "pass|fail"` — save this output
3. Check test coverage for the files to be refactored: if coverage is < 60%, write characterisation tests first (see `legacy-archaeologist`)
4. Identify the scope: single function, a file, or a module
5. Run `plankton-code-quality` (if available) for a pre-polish quality baseline

### Step 1: Characterisation (If No Tests)

**Goal:** Capture the current behaviour of the code in tests before making any changes.

**Expected output:** Test file(s) that cover the critical paths of the code to be refactored, all passing.

**Tools to use:** test-genius (for test writing), legacy-archaeologist (for legacy code patterns).

1. Identify the inputs and outputs of the code to be refactored
2. Collect 3-5 realistic input examples (use production logs or usage data if available)
3. Run each example through the current code and capture the output
4. Write tests that assert current-output matches captured-output
5. Run tests and confirm they pass

**Verification gate:** All characterisation tests pass. The test count > 0 for each function being refactored.

### Step 2: Identify & Apply Refactorings

**Goal:** Apply one refactoring at a time, verifying behaviour preservation after each.

**Expected output:** Clean, well-structured code with all existing tests still passing.

**Tools to use:** LSP (find-references before renaming), grep (find all usages), ast-grep (structural search/replace).

**Common Code Smells & Fixes:**

**1. Long Functions (>30 lines)**
```javascript
// Before: Long function doing too much
function processOrder(order) {
  if (!order.items || order.items.length === 0) throw new Error("Empty order");
  for (const item of order.items) {
    if (item.quantity <= 0) throw new Error("Invalid quantity");
  }
  let subtotal = 0;
  for (const item of order.items) { subtotal += item.price * item.quantity; }
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
  if (order.discountCode) { /* more code */ }
  /* save to database */ /* send confirmation */
  return { subtotal, tax, total };
}

// After: Extract Method — each function does one thing
function processOrder(order) {
  validateOrder(order);
  const totals = calculateTotals(order);
  const discounted = applyDiscount(totals, order.discountCode);
  const saved = saveOrder(order, discounted);
  sendConfirmation(saved);
  return discounted;
}
function validateOrder(order) { /* ... */ }
function calculateTotals(order) { /* ... */ }
```

**2. Duplicate Code → Extract Function**
```javascript
// Before: Duplicate validation in createUser and updateUser
function createUser(data) {
  if (!data.email) throw new Error("Email required");
  if (!data.email.includes("@")) throw new Error("Invalid email");
  // ...create user
}
function updateUser(id, data) {
  if (data.email && !data.email.includes("@")) throw new Error("Invalid email");
  // ...update user
}

// After: Shared validation
function validateEmail(email) {
  if (!email) throw new Error("Email required");
  if (!email.includes("@")) throw new Error("Invalid email");
}
```

**3. Deep Nesting → Early Returns**
```javascript
// Before: 4 levels of nesting
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission("admin")) {
        return user.organization?.name ?? null;
      }
    }
  }
  return null;
}

// After: Guard clauses
function processUser(user) {
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission("admin")) return null;
  return user.organization?.name ?? null;
}
```

**4. Magic Numbers → Named Constants**
```javascript
// Before
if (user.age >= 21) { /* adult */ }
setTimeout(callback, 300000);

// After
const LEGAL_AGE = 21;
const FIVE_MINUTES_MS = 5 * 60 * 1000;
```

**Verification gate:** After each individual refactoring, run tests and confirm they pass. If they fail, revert the last change.

### Step 3: Deduplication Pass

**Goal:** Extract repeated patterns into shared utilities.

**Expected output:** Deduplicated code with extracted functions/utilities; all tests pass.

**Tools to use:** grep (find similar patterns), LSP (rename symbol).

1. Search for repeated code blocks using grep for common patterns
2. Extract each duplicated block into a named function
3. Replace all instances with calls to the extracted function

**Verification gate:** The same test suite passes. Duplication count (measured by grep for similar blocks) has decreased.

### Step 4: Verification & Cleanup

**Goal:** Confirm behaviour preservation and clean up all artifacts.

**Expected output:** Clean commit(s) with passing tests, no debug code, no TODOs.

**Tools to use:** bash (test runner), plankton-code-quality (final quality check).

1. Run the full test suite — compare pass/fail count to pre-refactoring baseline
2. Run linter — fix any new warnings (but don't reformat the entire file unless intentional)
3. Remove any debug logging, TODOs, or commented-out code added during refactoring
4. Commit each logical refactoring separately with descriptive messages

**Verification gate:** Test suite produces identical results to baseline. Linter exits 0. No commented-out code remains.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|-----------|-------------|----------|
| Mixing a logic change with a formatting change in the same commit | Reviewers cannot distinguish intentional behaviour changes from accidental ones when both are present, increasing review time and missed-bug risk | Separate formatting into its own commit. Reset the mixed commit, commit formatting first, then logic. |
| Removing code marked as "unused" without checking for dynamic dispatch | `require(variable)`, reflection, plugin registries, and decorator-based registration are invisible to static analysis | Search for dynamic dispatch patterns before deleting. If unsure, add a deprecation warning and monitor logs for a release cycle. |
| Polishing code that has no test coverage without writing characterisation tests first | A refactor applied to untested code has no safety net; any behaviour change introduced is undetectable until a user reports a regression | Write characterisation tests that capture current outputs for at least 3 representative inputs before touching any code. |

## Verification

Before marking any code-polish task as complete:

### Self-Verification Checklist

- [ ] All tests that existed before refactoring still pass: `npm test` (or equivalent) exits 0 with 0 failing tests
- [ ] No behaviour changes: function inputs, outputs, and side effects are identical before and after
- [ ] Cyclomatic complexity reduced: `npx eslint --rule 'complexity: [error, 10]' src/` exits 0 — no function exceeds 10 branches
- [ ] No magic numbers remain: `grep -rn "[^a-zA-Z_][0-9]\{2,\}[^0-9]" src/` returns 0 matches (excluding test fixtures)
- [ ] No function exceeds 30 lines (excluding style-only files)
- [ ] Dead code removed: linter reports 0 unused variables or imports
- [ ] De-Sloppify pass completed: no `console.log`, `TODO`, `FIXME`, or commented-out code left

### Quality Gates

| Gate | Criteria | Fail Action |
|------|----------|-------------|
| Test Parity | Test pass/fail count identical to pre-refactoring baseline | Revert the refactoring commit; characterisation tests may have been wrong — verify against original spec |
| Complexity | No function exceeds 10 cyclomatic branches | Extract conditional logic into smaller named functions; apply early-return pattern |
| Function Size | No function exceeds 30 logic lines | Extract method: each sub-operation becomes its own function |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|----------------|------------------|-----------------|
| Simple rename/formatting in a single file | Fast reasoning model | 1K-3K |
| Function extraction / complexity reduction | Fast reasoning model | 3K-8K |
| Multi-file deduplication with structural analysis | Deep reasoning model | 8K-20K |

### Context Budget

- **Expected context usage:** 2K-8K tokens per refactoring session
- **When to context-optimize:** When analyzing 10+ usages of a repeated pattern for deduplication
- **Context recovery:** Commit after each logical transformation to clear working context

## Examples

### Example 1: Long Function Refactoring

**User request:**
```
This 80-line function handles order processing. It's hard to test and harder to modify. Clean it up.
```

**Skill execution:**

1. **Characterisation:** Write 3 tests capturing current behaviour (valid order, empty cart, missing items)
2. **Decomposition:**
   - Extract `validateOrder()` — 15 lines → 5 lines
   - Extract `calculateTotals()` — 20 lines → 8 lines
   - Extract `applyDiscounts()` — 15 lines → 10 lines (with separate discount strategies)
   - Extract `sendOrderConfirmation()` — 10 lines → 5 lines
3. **Result:** 7 functions, each <= 15 lines. All 3 characterisation tests + 5 new unit tests pass.

**Result:** Cyclomatic complexity reduced from 18 to 4. Each function is independently testable.

### Example 2: Conditional → Polymorphism

**User request:**
```
The shipping calculator has 8 if/else branches for different shipping methods. Every time we add a method, we modify this function.
```

**Skill execution:**

1. **Assessment:** The Open/Closed principle is violated — adding a shipping method modifies existing code
2. **Refactoring:** Extract each branch into a strategy class/function implementing a common interface
3. **Registration:** Use a map/dictionary to register strategies by type
4. **Result:** Adding a new shipping method requires a new strategy file and one line in the registration map — no modification of existing code

**Result:** 8 strategies extracted. Adding shipping method now requires only a new file + registration entry. Open for extension, closed for modification.

### Example 3: Edge Case — Dead Code with Dynamic Dispatch

**User request:**
```
Remove all unused functions from the utils module.
```

**Skill execution:**

1. **Static Analysis:** LSP reports 3 exported functions with zero references
2. **Dynamic Check:** Search for `require('./utils')`, `require('./utils).*\(`, and plugin registrations
3. **Finding:** One "unused" function is called via `require('./utils')[dynamicVar]()` in a plugin loader
4. **Action:** Rename the other 2 (confirmed dead), leave the dynamic one with a deprecation comment. Do NOT delete it.

**Result:** 2 functions removed, 1 function marked deprecated with a warning log. Tested in production for 2 release cycles before final removal.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Renaming a public symbol without checking all callers | A rename that breaks a downstream module will not be caught by local tests and surfaces only when the consuming module is next built or run | Check all references with LSP "find references" before renaming. Treat exported symbols as a breaking change boundary. |
| Introducing a new abstraction during a polish pass | Adding abstraction changes the architecture under the guise of cleanup, making the change harder to review and harder to revert if the abstraction is wrong | Polish = improve existing structure. Abstraction = new architecture. These belong in different commits, preferably different PRs. |
| Polishing a file actively being changed by another branch | Merge conflicts on a heavily reformatted file are extremely difficult to resolve and often result in silently losing one side's changes | Coordinate with the other developer. Polish can wait until after their branch is merged, or agree on a shared formatting commit first. |

## References

### Internal Dependencies

- `legacy-archaeologist` — Provides characterisation test patterns and legacy code assessment; invoke when polishing untested legacy code
- `test-genius` — Writes characterisation and unit tests to support refactoring
- `plankton-code-quality` — Provides pre/post polish quality baseline metrics and enforces formatting on write
- `python-patterns` — Language-specific polish patterns for Python code

### External Standards

- [Refactoring: Improving the Design of Existing Code (Martin Fowler)](https://martinfowler.com/books/refactoring.html) — The canonical reference for behaviour-preserving refactoring patterns
- [Code Smells Catalog (refactoring.guru)](https://refactoring.guru/refactoring/smells) — Categorised list of code smells with refactoring recipes
- [Working Effectively with Legacy Code (Michael Feathers)](https://www.goodreads.com/book/show/44919.Working_Effectively_with_Legacy_Code) — Characterisation test patterns and legacy code refactoring strategies

### Related Skills

- `legacy-archaeologist` — Precedes this skill: characterisation tests before refactoring
- `test-genius` — Used alongside: tests provide the safety net for refactoring
- `python-patterns` — Language-specific variant: provides Python idioms and patterns for polishing Python code

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-09 | Gold standard upgrade: added version/category/dependencies frontmatter, Core Principles with enforcement, 4-step Instructions workflow (with characterisation, refactoring, deduplication, verification), Blocking Violations table, Performance & Cost, Examples (3 with code), Anti-Patterns table, References, Changelog |
| 1.0.0 | 2025-06-01 | Initial version |
