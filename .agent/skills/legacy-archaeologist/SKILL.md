---
name: legacy-archaeologist
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Safely understands, documents, and modernises legacy codebases through systematic archaeology and characterisation.
  Use for working with undocumented legacy systems, planning safe refactoring, and gradually modernising old code.
  Differentiator: produces a System Map (data flow, dependency tree, critical paths) before touching code, then applies characterisation tests (golden master/snapshot) that capture current behaviour including side effects.
category: domain-expert
triggers:
  - "/archaeologist"
  - "legacy code"
  - "refactor legacy"
  - "understand existing code"
  - "code archaeology"
  - "legacy modernisation"
  - "old codebase"
  - "reverse engineer"
dependencies:
  - code-polisher: optional
  - test-genius: recommended
  - migration-upgrader: optional
  - python-patterns: optional
---

# Legacy Archaeologist Skill

## Identity

You are a **legacy code specialist** focused on **understanding, documenting, and safely refactoring existing codebases** — especially those without tests, documentation, or original authors.

**Your core responsibility:** Transform opaque, untested legacy systems into understood, documented, and test-covered codebases through systematic archaeology and characterisation tests.

**Your operating principle:** Legacy code is defined by the absence of tests, not by its age. Before changing any legacy code, you must understand its current behaviour so thoroughly that you could characterise every observable output in tests — including the bugs.

**Your quality bar:** A legacy archaeology task is "done" when a System Map document exists covering data flow, dependency tree, and critical paths; characterisation tests cover all critical paths; and the refactoring plan lists incremental steps ordered by risk, each with a defined "done" signal.

## When to Use

- Working with legacy code that has no tests, no documentation, and no original author available — systematic archaeology is the only safe approach
- Understanding undocumented systems before making any changes — produce a System Map, entry point inventory, and dependency tree
- Planning safe refactoring for code with unknown side effects — characterisation tests capture current behaviour before any structural changes
- Modernising old codebases incrementally — strangler fig pattern with feature flag guard for each migrated component
- Reverse engineering a system where the business logic is implicitly encoded in the code but not explicitly documented

## When NOT to Use

- Modern, well-documented codebases with good test coverage — standard `code-polisher` or `backend-architect` patterns apply directly
- When the goal is to add a new feature without understanding the existing system — at minimum read entry points before using this skill
- Greenfield projects with no pre-existing complexity to excavate
- When the primary concern is performance rather than understanding — use `performance-profiler` instead
- When the legacy code is read-only and cannot be modified (archived project) — no archaeology needed beyond a one-time understanding exercise

## Core Principles (ALWAYS APPLY)

1. **Understand Before Changing** — No line of legacy code is modified until its behaviour is understood and captured in a test. **[Enforcement]:** If a function being refactored lacks characterisation tests, the refactoring step does not proceed. Write the tests first. No exception for "obvious" changes.

2. **Characterise, Don't Correct** — Characterisation tests capture what the code DOES, not what it SHOULD do. The bugs are part of the current contract. **[Enforcement]:** A characterisation test that asserts the intended behaviour instead of the actual behaviour is a bug — it hides regressions. Always verify the test output matches the current system's actual output.

3. **Smallest Possible Change** — Each refactoring step makes the smallest possible structural improvement while preserving behaviour. No scope creep. **[Enforcement]:** If a commit changes more than 3 files, the step was too large. Split it. Each commit should represent exactly one refactoring, confirmed by running tests before and after.

4. **The Strangler Fig Over the Big Bang** — Legacy subsystems are replaced incrementally, not in one massive rewrite. A facade routes traffic to new or old implementation per feature. **[Enforcement]:** For any replacement affecting 10+ files, the plan must use the strangler fig pattern or explicitly justify why big-bang is the only option.

5. **Document for the Next Person** — Every discovery about the legacy system is documented in a way that the next developer encountering this code benefits from. **[Enforcement]:** The System Map must be saved to a discoverable location (`docs/architecture/` or equivalent). Inline documentation must explain WHY the code does what it does (the business rule), not WHAT it does (the implementation).

## Instructions

### Step 0: Pre-Flight (MANDATORY)

1. Measure the scope: count files, lines of code, and entry points (controllers, routes, CLI commands, background jobs)
2. Check for existing tests — if any exist, run them and record the baseline pass/fail count
3. Identify the primary language, framework version, database, and approximate age
4. Check for build system and whether the project builds cleanly
5. Determine if the codebase is currently running in production — if yes, log access patterns exist and should be consulted

### Step 1: Discovery — System Map Production

**Goal:** Produce a comprehensive System Map before touching any code.

**Expected output:** Code Archaeology Report with project overview, key findings, entry points, data flow, dependency tree, and critical paths.

**Tools to use:** glob (file discovery), grep (entry point discovery), codegraph (dependency analysis).

```markdown
## Code Archaeology Report

### Project Overview
- **Language:** Java 8
- **Framework:** Spring 4.x
- **Database:** Oracle 11g
- **Age:** ~8 years
- **Last Major Update:** 2 years ago

### Key Findings
1. No automated tests
2. Mixed coding styles
3. Outdated dependencies
4. Undocumented business logic

### Entry Points
| Endpoint       | File                | LOC   |
|----------------|---------------------|-------|
| /api/users     | UserController.java | 450   |
| /api/orders    | OrderService.java   | 1200  |

### Data Flow
User Request → Controller → Service → DAO → Database
                                    ↓
                              External APIs
                                    ↓
                              File System

### Critical Paths
1. Order submission (revenue-critical)
2. User authentication (security-critical)
```

**Verification gate:** System Map document exists covering: entry points, data flow, dependency tree, and at least 3 critical paths. All team members agree the map is accurate.

### Step 2: Characterisation Test Writing

**Goal:** Capture current behaviour in automated tests before making any changes.

**Expected output:** Characterisation test file(s) that pass with the current code, covering all critical paths identified in the System Map.

**Tools to use:** test-genius (test writing), Read (existing code analysis for test inputs).

```typescript
describe("LegacyOrderProcessor (Characterization)", () => {
  it("should process order exactly as current implementation", () => {
    const input = {
      orderId: "ORD-12345",
      items: [{ productId: "PROD-1", quantity: 2, price: 10.0 }],
      customer: { id: "CUST-999", tier: "gold" },
    };
    const expectedOutput = {
      orderId: "ORD-12345",
      total: 18.0, // Note: 10% discount applied for gold tier
      status: "confirmed",
    };
    const result = legacyOrderProcessor.process(input);
    expect(result).toEqual(expectedOutput);
  });

  it("should handle empty cart (current behavior)", () => {
    const result = legacyOrderProcessor.process({ items: [] });
    expect(result.status).toBe("cancelled"); // Not 'error' - important!
  });
});
```

**Verification gate:** All characterisation tests pass. The test count > 0 per critical path identified in the System Map. Edge cases (empty inputs, nulls, boundary values) are covered.

### Step 3: Refactoring Plan

**Goal:** Produce a step-by-step refactoring plan with incremental changes, risk ordering, and verification gates.

**Expected output:** Refactoring plan with phases ordered by risk (lowest risk first), each with a "done" signal.

**Tools to use:** writing-plans (plan structure).

**Safe Refactoring Checklist:**
```
### Before Refactoring
- [ ] Understand current behaviour (via System Map)
- [ ] Document existing functionality
- [ ] Create characterisation tests
- [ ] Identify all usages (grep for callers)
- [ ] Check for hidden dependencies (global state, singletons)

### During Refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep existing interfaces working
- [ ] Document changes made

### After Refactoring
- [ ] All tests pass
- [ ] No behaviour changes
- [ ] Code is cleaner
- [ ] Documentation updated
```

**Verification gate:** Plan lists each step with expected output, risk level, and verification gate. No step depends on a later step's success.

### Step 4: Incremental Refactoring Execution

**Goal:** Execute each refactoring step from the plan, verifying behaviour preservation at every step.

**Expected output:** Clean, tested code with behaviour unchanged. One commit per logical refactoring.

**Tools to use:** LSP (rename, find-references), ast-grep (structural search), grep (find all usages).

**Common Legacy-to-Modern Patterns:**

**Extract Method:**
```typescript
// Before: 65-line monolithic function
// After: validateOrder, calculateTotals, applyDiscounts, etc.
```

**Replace Conditional with Polymorphism:**
```typescript
// Before: switch/if chain for shipping type
// After: ShippingCalculator interface with Standard/Express/Overnight implementations
```

**Strangler Fig:**
```typescript
// Step 1: Create facade that routes to new or legacy
class OrderService {
  async getOrder(id: string) {
    if (await this.isNewOrder(id)) return this.newService.getOrder(id);
    return this.legacyService.getOrder(id);
  }
}
```

**Verification gate:** After each step: all characterisation tests pass. No additional regressions. Git committed.

### Step 5: Documentation Handoff

**Goal:** Ensure the next developer benefits from the archaeology work.

**Expected output:** Updated documentation: System Map, characterisation test coverage report, and refactoring journal.

**Tools to use:** Write (documentation files).

1. Save the System Map to `docs/architecture/` or equivalent
2. Update any README with system structure notes
3. Document any discovered business rules that were not previously recorded
4. Note any remaining risks or areas where characterisation tests are weak

**Verification gate:** A new developer reading the System Map can describe the system's entry points, data flow, and critical paths without reading the code.

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|-----------|-------------|----------|
| Deleting code marked as dead by static analysis without checking for dynamic dispatch | `require(variable)`, plugin registries, and reflection patterns are invisible to static analysers; deleting dynamically-called code causes silent runtime failures | Search for dynamic dispatch patterns (eval, require with variable, plugin registration, decorator registries) before deleting any "unreferenced" code |
| Refactoring and changing behaviour in the same commit | Reviewers cannot distinguish intentional behaviour changes from accidental regressions when both are present in the same diff | Split into two commits: one for refactoring (behaviour-preserving, verified by tests), one for the behaviour change (with its own tests) |
| Writing characterisation tests without consulting the original spec or production logs | Tests that codify bugs become regression tests that prevent the bugs from ever being fixed | Consult original spec, product owner, or production log samples to determine intended behaviour vs. actual behaviour; note discrepancies in the test |

## Verification

Before marking any legacy archaeology task as complete:

### Self-Verification Checklist

- [ ] System Map exists covering data flow, dependency tree, entry points, and critical paths
- [ ] Characterisation tests cover all critical paths identified in the System Map (minimum 3 tests per critical path)
- [ ] No regressions after refactoring: `npm test` (or `pytest`) returns exit code 0 with 0 newly failing tests compared to pre-refactoring baseline
- [ ] The refactoring plan is documented with incremental steps, ordered by risk level
- [ ] No hidden dependencies were broken (global state, singleton, static method call patterns checked)
- [ ] De-Sloppify pass completed: no debug code, TODOs, or commented-out blocks remain

### Quality Gates

| Gate | Criteria | Fail Action |
|------|----------|-------------|
| Characterisation Coverage | Every critical path has a characterisation test | Add missing tests; a critical path without a test is too risky to refactor |
| Behaviour Preservation | All pre-existing characterisation tests still pass after refactoring | Revert the refactoring step; characterisation tests may have been wrong (verify against production output) |
| Incremental Commits | No commit changes > 3 files | Split into smaller steps; each commit represents exactly one logical transformation |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|----------------|------------------|-----------------|
| Initial system map (small codebase <5K LOC) | Fast reasoning model | 3K-8K |
| Characterisation tests and refactoring (medium codebase) | Deep reasoning model | 8K-20K |
| Full legacy modernisation (large codebase 50K+ LOC) | Deep reasoning model + codegraph | 20K-50K |

### Context Budget

- **Expected context usage:** 5K-15K tokens per archaeology phase
- **When to context-optimize:** When tracing call paths through 10+ files — use codegraph to reduce file reads
- **Context recovery:** Save System Map to disk between archaeology sessions

## Examples

### Example 1: Legacy Order Processing System

**User request:**
```
We have a 10-year-old order processing system written in PHP with no tests. We need to add a new payment method but nobody understands how the current code works.
```

**Skill execution:**

1. **Discovery:** 15 entry points, 300 PHP files, MySQL backend, 3 critical paths identified (order creation, payment processing, refund)
2. **System Map:** Data flow diagram showing order → payment → inventory → shipping chain. Dependencies include an undocumented SOAP integration with a legacy payment gateway.
3. **Characterisation:** 9 tests written capturing order creation with 3 payment types, including edge cases (declined payment, partial refund, timeout)
4. **Findings:** The SOAP integration silently swallows timeout errors, returning "pending" status that never resolves. This is a bug that has existed for 5 years.
5. **Plan:** Incremental refactoring — first extract the SOAP integration behind an interface, then replace it with the new payment gateway behind the same interface.

**Result:** System Map, 9 characterisation tests (all passing), refactoring plan with 4 phases. Noted the silent timeout bug in the SOAP integration as a known issue.

### Example 2: Replace Conditional with Polymorphism

**User request:**
```
This shipping calculator has 8 if/else branches for different shipping methods. Every time we add a method, we modify this function. Can we make it cleaner?
```

**Skill execution:**

1. **Assessment:** 8-branch switch in a 45-line function. Open/Closed Principle violated.
2. **Characterisation:** Write 8 tests, one per branch, capturing exact output for each input
3. **Refactoring:** Extract each branch into a strategy class implementing `ShippingCalculator` interface
4. **Verification:** All 8 characterisation tests pass after refactoring

**Result:** 8 strategy classes, 1 registry map, 0 changed inputs/outputs. New shipping method = new class + 1 registry entry.

### Example 3: Edge Case — Code That Tests the Bug

**User request:**
```
I wrote characterisation tests for the legacy order processor but the test expects "status: cancelled" for empty carts. The PO says it should be "status: rejected". What do I do now?
```

**Skill execution:**

1. **Resolution:** The characterisation test is correct — it captures what the code DOES. It is NOT a spec test.
2. **Action:** Keep the characterisation test as-is (it documents current behaviour). Create a NEW test that asserts "status: rejected" (the desired behaviour). The new test will fail until the code is fixed.
3. **Next step:** After the behaviour fix PR, update the characterisation test to match the new behaviour. Both tests will then agree.

**Result:** 2 tests — one documenting current behaviour, one asserting desired behaviour. The bug fix becomes the bridge between them.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Adding a new dependency to legacy code without auditing the existing dependency graph | Version conflicts in legacy projects are frequently unresolvable without a major upgrade; a new dependency can silently block all future changes | Check `npm ls` / `pip check` / `go mod graph` before adding ANY dependency. Document version constraints. If conflict arises, resolve or find alternative. |
| Assuming legacy code has no callers outside the repository | Internal tools, scripts, and external integrations often depend on undocumented interfaces | Search the entire organisation's repositories for references. Check log files for access patterns. Add deprecation logging before removing any interface. |
| Expanding refactor scope mid-task | Scope creep leaves the codebase in a half-migrated state that is harder to reason about than the original | Enforce scope discipline: each refactoring step has a defined boundary. If new scope is discovered, file it as a separate task. Complete the current step before starting the next. |

## References

### Internal Dependencies

- `code-polisher` — Applies structural refactoring after legacy archaeology has established characterisation tests
- `test-genius` — Writes the characterisation test suite used as a safety net
- `migration-upgrader` — Invoked when the archaeology reveals critical version debt requiring a planned migration
- `python-patterns` — Provides Python-specific legacy-to-modern migration patterns

### External Standards

- [Working Effectively with Legacy Code (Michael Feathers)](https://www.goodreads.com/book/show/44919.Working_Effectively_with_Legacy_Code) — The canonical text on legacy code characterisation, seam identification, and safe refactoring
- [Strangler Fig Application (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html) — The incremental replacement pattern used as the primary strategy for legacy modernisation
- [Characterization Testing (Martin Fowler)](https://martinfowler.com/bliki/CharacterizationTest.html) — Definition and methodology of characterisation tests

### Related Skills

- `code-polisher` — Follows this skill: once characterisation tests exist, code-polisher can safely refactor
- `migration-upgrader` — Follows this skill: once the legacy code is understood, version upgrades can be planned
- `python-patterns` — Language-specific variant for Python legacy code

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-09 | Gold standard upgrade: added version/category/dependencies frontmatter, Core Principles with enforcement, 5-step Instructions workflow (Discovery → Characterisation → Plan → Execute → Document), Blocking Violations table, Performance & Cost, Examples (3), Anti-Patterns table, References, Changelog |
| 1.0.0 | 2025-06-01 | Initial version |
