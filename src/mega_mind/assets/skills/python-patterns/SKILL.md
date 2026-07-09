---
name: python-patterns
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Production-grade Python design patterns, modern tooling, and idiomatic code standards for Python 3.10+.
  Use for any Python-specific development where quality, type safety, and performance matter.
  Differentiator: strict tooling discipline (uv + ruff + pyright + pytest), decision matrix for dataclass/Pydantic/TypedDict selection, async/await deep-dive with concurrency model decision guide, and exception hierarchy design patterns.
category: domain-expert
triggers:
  - "/python"
  - "python patterns"
  - "idiomatic python"
  - "python threading"
  - "python async"
  - "type hints"
  - "__slots__"
  - "pydantic"
  - "pytest fixtures"
  - "pyproject.toml"
  - "uv package manager"
  - "dataclass"
  - "context manager"
  - "python decorator"
  - "asyncio"
  - "ruff"
dependencies:
  - code-polisher: optional
  - test-genius: optional
  - migration-upgrader: optional
  - performance-profiler: optional
  - security-reviewer: optional
---

# Python Development Patterns

## Identity

You are a **senior Python engineer** with deep expertise in **modern Python (3.10+) idioms, type safety, and production-grade patterns**.

**Your core responsibility:** Write Python code that is explicit, testable, and maintainable — not clever or magical. Apply strict tooling discipline: ruff for linting/formatting, pyright for type checking, uv for package management, and pytest for testing.

**Your operating principle:** The Python type system is a first-class design tool, not an afterthought. Every function signature is fully annotated, every public API is documented via types, and pyright strict mode enforcement means if the type checker complains, you fix the code, not the config.

**Your quality bar:** A Python task is "done" when `uv run ruff check . && uv run ruff format --check . && uv run pyright && uv run pytest` all exit 0, every public function has complete type annotations, and no `# type: ignore` or `# noqa` comments were added without a documented justification.

## When to Use

- Writing new Python services, libraries, utilities, or CLI tools
- Refactoring legacy Python 2.x or early 3.x code to modern standards
- Implementing concurrency (asyncio, threading, multiprocessing) and needing to choose the right model
- Designing data models and needing to choose between dataclasses, Pydantic, TypedDict, or NamedTuple
- Setting up a new Python project with pyproject.toml, uv, ruff, and pyright
- Writing pytest test suites with fixtures, parametrize, and coverage gates
- Packaging a library for distribution via PyPI or private registries
- Implementing context managers or decorators for cross-cutting concerns

## When NOT to Use

- The project is not Python — do not apply Python patterns to TypeScript, Go, or other languages
- The task is a trivial one-liner or script with no reuse — skip the full infrastructure
- The codebase is frozen legacy code that cannot be touched (read-only archaeology) — use `legacy-archaeologist` instead
- The ask is purely about SQL, infrastructure, or Docker with no Python logic involved
- The user explicitly wants a "quick and dirty" prototype and has accepted lower quality

## Core Principles (ALWAYS APPLY)

1. **Explicit Over Implicit** — Avoid `**kwargs` sinks, `getattr` magic, and mutable globals. Every input and output should be named and typed. **[Enforcement]:** Any function signature using `**kwargs` without a defined TypedDict for the keyword arguments is rejected at review. Any mutation of a module-level global from inside a function is a blocking issue.

2. **Types Are Documentation** — Every function signature gets full type annotations. Use `pyright` in strict mode — if it complains, fix the code, not the config. **[Enforcement]:** `pyright` must exit 0 in strict mode. If a suppression (`# type: ignore`) is added, it must be accompanied by a same-line comment explaining why. More than 5 suppressions in a single PR triggers a mandatory review.

3. **Immutability by Default** — Prefer `frozen=True` dataclasses, `tuple` over `list` for fixed collections, and `Final` for constants. **[Enforcement]:** A mutable default argument (`def f(x=[])`) is an automatic review failure. A list defined at module level that is never mutated should be a tuple.

4. **EAFP With Specificity** — Catch only the exceptions you can handle. Never `except Exception:` — always name the specific exception class. **[Enforcement]:** A bare `except Exception` (without re-raise) in a production code path is a blocking violation. `except Exception as e: logger.error(...); raise` is acceptable for logging wrappers only.

5. **Tooling Is Non-Negotiable** — Every project uses `uv`, `ruff`, and `pyright`. No exceptions. `pip install` directly is forbidden on any managed project. **[Enforcement]:** If `pip install` is detected in a Makefile, script, or documentation, it must be replaced with `uv add`. Any commit that adds a dependency via `pip install` is automatically rejected.

6. **Async Means Async Throughout** — Do not mix sync and async code in the same call stack. If a function is `async`, its callers must be `async` too, up to the event loop entry point. **[Enforcement]:** A sync function calling an async function with `.run()` or `create_task()` outside an explicit async boundary is a design flaw and must be restructured.

7. **Test the Contract, Not the Implementation** — Pytest fixtures describe state, not procedure. Use `parametrize` for combinatorial coverage, not copy-paste tests. **[Enforcement]:** Any test module with 3+ similar test functions that differ only in input/output values must be refactored to use `@pytest.mark.parametrize`.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

Before writing any Python code:
1. Verify toolchain: `uv --version`, `ruff --version`, `pyright --version` all return without errors
2. Check that `pyproject.toml` exists and has the correct tool configuration (ruff, pyright, pytest)
3. If working on existing code, run the baseline checks: `uv run ruff check . && uv run ruff format --check . && uv run pyright && uv run pytest`
4. Identify the Python version target: `requires-python = ">=3.10"` in pyproject.toml
5. Check whether this is new code, refactoring, or a fix — this determines tooling strictness

### Step 1: Type Design

**Goal:** Choose the correct data modelling tool for each data structure.

**Expected output:** Data model definitions using the appropriate tool (dataclass, Pydantic, TypedDict, NamedTuple).

**Tools to use:** Write (model files), pyright (verify type correctness).

**Decision Matrix:**

| Use Case                    | Tool                      | Why                              |
|----------------------------|---------------------------|----------------------------------|
| Internal data containers   | `@dataclass(frozen=True)` | Zero overhead, no validation     |
| API request/response bodies | Pydantic `BaseModel`     | Runtime validation + JSON schema |
| External config (env/YAML) | Pydantic `BaseSettings`  | Type coercion + env var support  |
| Dict-shaped typed data     | `TypedDict`              | Structural typing without class  |
| Simple immutable tuples    | `NamedTuple`             | Tuple semantics with names       |

```python
# Internal data — dataclass
@dataclass(frozen=True, slots=True)
class Event:
    id: str
    name: str
    timestamp: datetime

# API boundary — Pydantic
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
```

**Verification gate:** `pyright` reports 0 type errors. The data model choice matches the decision matrix above.

### Step 2: Function & Logic Implementation

**Goal:** Write fully-typed functions with proper error handling and documentation.

**Expected output:** One or more Python modules with complete type annotations, exception hierarchy, and docstrings.

**Tools to use:** Write (code files), ruff (linting during write).

**Modern Type Hints (3.10+):**
```python
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def parse_id(value: str | int) -> int:
    return int(value)

from typing import Protocol
class Renderable(Protocol):
    def render(self) -> str: ...
```

**Exception Hierarchy:**
```python
class AppError(Exception):
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code

class ResourceNotFoundError(AppError): ...
class ValidationError(AppError): ...
```

**Verification gate:** `uv run pyright` exits 0. `uv run ruff check .` exits 0. Every function has parameter and return type annotations.

### Step 3: Async/Concurrency Design

**Goal:** Choose the correct concurrency model and implement it correctly.

**Expected output:** Async or concurrent code following the decision matrix below.

**Tools to use:** Write (async code), pyright (type-check async patterns).

**Concurrency Decision Matrix:**
```
Task requires shared state with threads?          → asyncio (Task + Lock)
Task is I/O-bound, uses async-native libraries?   → asyncio
Task calls blocking C extensions / sync libs?     → ThreadPoolExecutor
Task is CPU-intensive (image processing, ML)?     → ProcessPoolExecutor
```

```python
# Correct async pattern
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict | None:
    try:
        async with asyncio.timeout(timeout):  # Python 3.11+
            async with httpx.AsyncClient() as client:
                return (await client.get(url)).json()
    except TimeoutError:
        return None
```

**Verification gate:** No `time.sleep()` in async code. No blocking library calls in the event loop without `run_in_executor`. All callers of async functions are themselves async.

### Step 4: Test Writing

**Goal:** Write pytest tests that cover the contract, not the implementation.

**Expected output:** Test files with fixtures, parametrize, and coverage meeting the project baseline.

**Tools to use:** Write (test files), bash (`uv run pytest`).

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5), ("", 0), ("  spaces  ", 8),
])
def test_string_length(input: str, expected: int) -> None:
    assert len(input) == expected

@pytest.fixture(scope="module")
def db_connection():
    conn = create_test_db_connection()
    yield conn
    conn.close()
```

**Verification gate:** `uv run pytest` exits 0 with coverage >= existing baseline %. No test uses `time.sleep()` for synchronisation.

### Step 5: Final Verification

**Goal:** Run the full toolchain and confirm all gates pass.

**Expected output:** All four tools (ruff check, ruff format, pyright, pytest) exit 0.

**Tools to use:** bash (toolchain commands).

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

**Verification gate:** All four commands exit 0. No warnings in ruff check. No errors in pyright strict mode.

## Modern Type Hints (3.10+)

Use built-in generics and union syntax. The `typing` module equivalents are deprecated.

```python
# Modern (Python 3.10+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Union types with | operator (3.10+)
def parse_id(value: str | int) -> int:
    return int(value)

# Protocol-Based Duck Typing — prefer over ABCs for structural subtyping
from typing import Protocol, runtime_checkable
@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...
```

## Dataclass Patterns

```python
@dataclass(frozen=True, slots=True)
class Event:
    id: str
    name: str
    timestamp: datetime
    tags: tuple[str, ...] = field(default_factory=tuple)
```

## Pydantic for Validation

Use Pydantic v2 for all external data boundaries (API inputs, config files, environment variables).

```python
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)

class AppSettings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False
    max_workers: int = Field(default=4, ge=1, le=32)
    model_config = {"env_prefix": "APP_", "env_file": ".env"}
```

## Context Managers

Use context managers for any resource that requires cleanup, not just files.

```python
@contextmanager
def temp_directory() -> Generator[Path, None, None]:
    import tempfile, shutil
    tmpdir = Path(tempfile.mkdtemp())
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
```

## Decorator Patterns

```python
# Retry decorator with exponential backoff
def retry(
    max_attempts: int = 3,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    backoff_seconds: float = 1.0,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(backoff_seconds * (2 ** attempt))
            raise RuntimeError("unreachable")
        return wrapper
    return decorator
```

## Async/Await Deep Dive

### Choosing the Right Concurrency Model

```
Task requires shared state with threads?          → asyncio
Task is I/O-bound, uses async-native libraries?   → asyncio
Task calls blocking C extensions / sync libs?     → ThreadPoolExecutor
Task is CPU-intensive (image processing, ML)?     → ProcessPoolExecutor
```

### asyncio.gather for Concurrent I/O

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        results = await asyncio.gather(
            *[fetch_one(client, url) for url in urls],
            return_exceptions=True,
        )
    successes = [r for r in results if not isinstance(r, Exception)]
    return successes
```

### asyncio Pitfalls

```python
# WRONG: time.sleep() in async code
async def bad_wait():
    time.sleep(1)  # Blocks ALL coroutines

# CORRECT: asyncio.sleep()
async def good_wait():
    await asyncio.sleep(1)  # Yields to event loop
```

## Exception Hierarchy Design

```python
class AppError(Exception):
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code

class AuthenticationError(AppError): ...
class AuthorizationError(AppError): ...
class ResourceNotFoundError(AppError): ...
class ValidationError(AppError): ...
```

## Pathlib Usage

Never use `os.path` — always use `pathlib.Path`.

```python
config_path = Path("config") / "settings.toml"
content = config_path.read_text(encoding="utf-8")
```

## Memory and Performance

### `__slots__` for High-Volume Objects

```python
@dataclass(slots=True)  # 30-50% memory savings
class Point:
    x: float
    y: float
```

### Generators for Large Data

```python
def read_large_file(path: Path) -> Iterator[str]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()
```

### String Building

```python
# CORRECT: join()
result = ", ".join(items)
# For complex building:
buf = io.StringIO()
for item in items:
    buf.write(item)
result = buf.getvalue()
```

## Testing Patterns with pytest

### Fixture Design

```python
@pytest.fixture(scope="module")
def db_connection():
    conn = create_test_db_connection()
    yield conn
    conn.close()
```

### Parametrize for Combinatorial Coverage

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5), ("", 0), ("  spaces  ", 8),
])
def test_string_length(input: str, expected: int) -> None:
    assert len(input) == expected
```

## Packaging with pyproject.toml and uv

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pydantic>=2.0", "httpx>=0.27"]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "strict"
```

### uv Commands (Use Instead of pip)

```bash
uv venv && source .venv/bin/activate
uv sync --extra dev
uv add httpx
uv add --dev pytest-asyncio
uv run pytest
uv run pyright
uv run ruff check .
```

## Tooling Integration Summary

| Tool          | Purpose                                  | Command                   |
|---------------|------------------------------------------|---------------------------|
| `ruff check`  | Linting (replaces flake8, isort, pylint) | `uv run ruff check .`     |
| `ruff format` | Formatting (replaces black)              | `uv run ruff format .`    |
| `pyright`     | Type checking (strict mode)              | `uv run pyright`          |
| `pytest`      | Testing                                  | `uv run pytest --cov=src` |
| `uv`          | Package management (replaces pip/venv)   | `uv sync`, `uv add`       |

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|-----------|-------------|----------|
| Using a mutable default argument (e.g., `def f(x=[])`) | Python creates the default object once at function definition time; all callers that omit the argument share the same mutable object, causing state to accumulate across calls | Change default to `None` and add an `if x is None: x = []` guard inside the function body. pyright will flag this if configured correctly. |
| Silencing a broad exception with `except Exception: pass` | Suppressing all exceptions hides bugs, swallows keyboard interrupts, and makes debugging production failures impossible without additional logging | Either catch specific exception types, or log the exception before `pass`. A bare `except: pass` is always wrong. |
| Using `is` to compare values (e.g., `x is 1`, `x is "hello"`) | `is` checks object identity, not equality; CPython interns small integers and some strings, making identity comparison coincidentally correct in tests but incorrect in production with different interpreter implementations | Use `==` for value comparison. Reserve `is` for `None` comparison (`x is None`) and singleton checks only. |

## Verification

Before declaring any Python task complete:

### Self-Verification Checklist

- [ ] `uv run ruff check .` exits 0 — 0 errors reported (no `# noqa` suppressions without justification)
- [ ] `uv run ruff format --check .` exits 0 — 0 formatting differences
- [ ] `uv run pyright` exits 0 — 0 errors in strict mode
- [ ] All new functions have complete type annotations on parameters and return types
- [ ] No `pip install` used: `grep -rn "pip install" Makefile scripts/` returns 0 matches
- [ ] No `os.path` usage: `grep -rn "os\.path\." src/` returns 0 matches (replaced by `pathlib.Path`)
- [ ] `uv run pytest` exits 0 with coverage >= existing baseline %

### Quality Gates

| Gate | Criteria | Fail Action |
|------|----------|-------------|
| Type Safety | `pyright` strict mode exits 0 with 0 errors | Fix type errors; do not add `# type: ignore`. If genuinely impossible to type, add ignore with justification comment. |
| Code Quality | `ruff check` exits 0 with 0 warnings | Auto-fix with `ruff check --fix .`. Review changes. Suppress only with justification. |
| Test Coverage | `pytest` exits 0 with no regression in pass count | Investigate failures. If pre-existing, document in task.md. Do not disable tests. |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|----------------|------------------|-----------------|
| Single function/module with straightforward types | Fast reasoning model | 2K-5K |
| New service with async, Pydantic, pytest | Deep reasoning model | 5K-15K |
| Large refactor across multiple modules + async migration | Deep reasoning model | 15K-30K |

### Context Budget

- **Expected context usage:** 3K-10K tokens per Python task
- **When to context-optimize:** When reviewing 10+ module outputs from ruff/pyright — pipe through `rtk` to reduce noise
- **Context recovery:** Commit after each logical module is passing all toolchain checks

## Examples

### Example 1: API Data Model Design

**User request:**
```
Design the data models for a user registration API — validate email, enforce age limits, and support configurable settings.
```

**Skill execution:**

1. **Choice:** Pydantic `BaseModel` for API boundary (needs validation), `BaseSettings` for configuration (env var support)
2. **Implementation:**
   - `UserCreate(BaseModel)` with `Field(min_length=1, max_length=100)` for name, `Field(pattern=r"...")` for email, `Field(ge=0, le=150)` for age
   - `@field_validator("name")` to strip whitespace
   - `AppSettings(BaseSettings)` with `env_prefix: "APP_"` for env-var-driven config
3. **Verification:** `pyright` strict mode exits 0. `ruff check` exits 0. `pytest` passes with edge cases (empty name, invalid email format, age = 0, age = 150, age = 151).

**Result:** `user_model.py` with 2 Pydantic models, 2 validators, 0 type errors. 8 pytest test cases covering all field constraints.

### Example 2: Async API Client

**User request:**
```
Write an async function that fetches data from 5 external APIs concurrently and aggregates the results. Handle timeouts and partial failures gracefully.
```

**Skill execution:**

1. **Choice:** `asyncio.gather` with `return_exceptions=True` — all requests fire concurrently, one failure doesn't cancel others
2. **Implementation:**
   - `async with httpx.AsyncClient(timeout=30.0)` as shared client
   - `asyncio.gather(*[fetch_one(client, url) for url in urls], return_exceptions=True)`
   - Separate successes from failures after gather
   - `asyncio.timeout(5.0)` per individual request for fine-grained timeout
3. **Result:** 5 concurrent requests. If 2 fail, 3 succeed — partial results returned with error count logged.

**Result:** `aggregator.py` with 2 functions, complete type annotations, 100% test coverage (success, partial failure, full failure, timeout).

### Example 3: Edge Case — Debugging a Memory Leak

**User request:**
```
Our long-running service leaks memory. After 24 hours it's using 2GB and needs restarting.
```

**Skill execution:**

1. **Investigation:** Use `tracemalloc` to find top allocations
2. **Finding:** A cache implemented as a module-level `dict` that grows without bound — keys are unique request IDs that are never evicted
3. **Fix:** Replace unbounded dict with `lru_cache(maxsize=1000)` or a custom `OrderedDict`-based LRU cache
4. **Verification:** Run the service under load for 1 hour, confirm heap stabilises under 200MB

**Result:** 2-line fix (`cache: dict = {}` → `@lru_cache(maxsize=1000)`). 24-hour stability test passes with heap under 200MB.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Performing file I/O in a `__init__` method | Object construction should not have side effects that require error handling or cleanup; I/O in `__init__` makes the class untestable without touching the filesystem | Move I/O to a factory function or class method. The constructor should only assign values. |
| Using `time.sleep` in production code to wait for an asynchronous event | Sleep-based polling is unpredictable under load — too short causes a busy loop, too long introduces unnecessary latency — and cannot be cancelled cleanly on shutdown | Use `asyncio.Event` or a proper synchronisation primitive. If polling is unavoidable, use exponential backoff with a configurable timeout. |
| Importing from a module's private namespace (`from module._internal import X`) | Private symbols have no stability guarantee and can be renamed or removed in any minor version without a deprecation notice | Use only the public API. If the needed symbol is not public, open a feature request or implement the functionality yourself. |

## References

### Internal Dependencies

- `code-polisher` — Applies structural refactoring patterns to Python code after initial implementation
- `test-genius` — Complements testing patterns; test-genius focuses on test strategy, python-patterns covers tool-specific pytest usage
- `migration-upgrader` — Uses Python-specific patterns when upgrading Python version or migrating from Python 2
- `performance-profiler` — Used when async patterns, memory usage, or data processing needs benchmarking
- `security-reviewer` — Audits Python code for security vulnerabilities after implementation

### External Standards

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/) — Base style guide; ruff enforces this automatically
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) — Type annotation standard used throughout
- [PEP 585 — Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/) — Enables `list[str]` instead of `List[str]`
- [PEP 604 — Allow writing union types as X | Y](https://peps.python.org/pep-0604/) — Enables `str | int` instead of `Union[str, int]`
- [Pydantic v2 Official Documentation](https://docs.pydantic.dev/latest/) — Reference for Pydantic model design and validation
- [pytest Documentation](https://docs.pytest.org/en/stable/) — Test framework patterns and fixture design

### Related Skills

- `code-polisher` — Follows this skill: after Python implementation, code-polisher can optimise structure
- `migration-upgrader` — Invokes this skill when Python version migration requires modern idiom updates
- `backend-architect` — Invokes this skill when implementing Python backend services

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-09 | Gold standard upgrade: added version/category/dependencies frontmatter, Core Principles with enforcement, 5-step Instructions workflow (Type Design → Logic Implementation → Async Design → Tests → Verification), Blocking Violations table, Performance & Cost, Examples (3), Anti-Patterns table, References, Changelog |
| 1.0.0 | 2025-06-01 | Initial version |
