---
name: python-patterns
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Production-grade Python design patterns, modern tooling, and idiomatic code standards for Python 3.10+. Covers dataclasses, context managers, decorators, async/await, exception hierarchies, Pydantic validation, pytest patterns, and packaging with pyproject.toml/uv. Use for any Python-specific development where quality, type safety, and performance matter.
triggers:
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
---

# Python Development Patterns

## Identity

You are a senior Python engineer with deep expertise in modern Python (3.10+) idioms, type safety, and production-grade patterns. You write code that is explicit, testable, and maintainable — not clever or magical. You enforce strict tooling discipline: ruff for linting/formatting, pyright for type checking, uv for package management, and pytest for testing. You know when to reach for dataclasses vs Pydantic, when async is appropriate vs threads vs processes, and how to design exception hierarchies that communicate intent clearly. You treat the Python type system as a first-class design tool, not an afterthought.

## When to Activate

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

---

## Core Principles

1. **Explicit over implicit**: Avoid `**kwargs` sinks, `getattr` magic, and mutable globals. Every input and output should be named and typed.
2. **Types are documentation**: Every function signature gets full type annotations. Use `pyright` in strict mode — if it complains, fix the code, not the config.
3. **Immutability by default**: Prefer `frozen=True` dataclasses, `tuple` over `list` for fixed collections, and `Final` for constants.
4. **EAFP with specificity**: Catch only the exceptions you can handle. Never `except Exception:` — always name the specific exception class.
5. **Tooling is non-negotiable**: Every project uses `uv`, `ruff`, and `pyright`. No exceptions. `pip install` directly is forbidden on any managed project.
6. **Async means async throughout**: Do not mix sync and async code in the same call stack. If a function is `async`, its callers must be `async` too, up to the event loop entry point.
7. **Test the contract, not the implementation**: Pytest fixtures describe state, not procedure. Use `parametrize` for combinatorial coverage, not copy-paste tests.

---

## Modern Type Hints (3.10+)

Use built-in generics and union syntax. The `typing` module equivalents are deprecated.

```python
# Modern (Python 3.10+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Union types with | operator (3.10+)
def parse_id(value: str | int) -> int:
    return int(value)

# TypeAlias for complex types (3.10+)
type UserId = int  # Python 3.12+ syntax
# or for 3.10/3.11:
from typing import TypeAlias
UserId: TypeAlias = int

# Protocol-Based Duck Typing — prefer over ABCs for structural subtyping
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: list[Renderable]) -> str:
    return "\n".join(item.render() for item in items)

# ParamSpec for decorator type safety
from typing import ParamSpec, TypeVar, Callable
P = ParamSpec("P")
T = TypeVar("T")

def logged(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

---

## Dataclass Patterns

Dataclasses are the default choice for data containers. Use `frozen=True` unless mutation is required.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Event:
    """Immutable event record. Use frozen=True to enable hashing."""
    id: str
    name: str
    timestamp: datetime
    tags: tuple[str, ...] = field(default_factory=tuple)

    def with_tag(self, tag: str) -> "Event":
        """Return a new Event with an added tag (immutable update pattern)."""
        return Event(
            id=self.id,
            name=self.name,
            timestamp=self.timestamp,
            tags=(*self.tags, tag),
        )

# For mutable containers with validation, use Pydantic (see below)
# For simple accumulators that need mutation, use slots=True without frozen
@dataclass(slots=True)
class Counter:
    name: str
    value: int = 0

    def increment(self, by: int = 1) -> None:
        self.value += by
```

### Dataclass vs Pydantic vs TypedDict Decision Matrix

| Use Case | Tool | Why |
| --- | --- | --- |
| Internal data containers | `@dataclass(frozen=True)` | Zero overhead, no validation |
| API request/response bodies | Pydantic `BaseModel` | Runtime validation + JSON schema |
| External config (env, YAML) | Pydantic `BaseSettings` | Type coercion + env var support |
| Dict-shaped typed data | `TypedDict` | Structural typing without class |
| Simple immutable tuples | `NamedTuple` | Tuple semantics with names |

---

## Pydantic for Validation

Use Pydantic v2 for all external data boundaries (API inputs, config files, environment variables).

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)

    @field_validator("name")
    @classmethod
    def name_must_not_be_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be only whitespace")
        return v.strip()

    @model_validator(mode="after")
    def check_adult_email_domain(self) -> "UserCreate":
        if self.age < 18 and "kids" not in self.email:
            raise ValueError("Under-18 users must use a kids domain")
        return self

class AppSettings(BaseSettings):
    """Reads from environment variables automatically."""
    database_url: str
    api_key: str
    debug: bool = False
    max_workers: int = Field(default=4, ge=1, le=32)

    model_config = {"env_prefix": "APP_", "env_file": ".env"}

# Usage: AppSettings() reads APP_DATABASE_URL, APP_API_KEY, etc.
```

---

## Context Managers

Use context managers for any resource that requires cleanup, not just files.

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator

# Class-based context manager for stateful resources
class DatabaseTransaction:
    def __init__(self, conn):
        self.conn = conn
        self._transaction = None

    def __enter__(self) -> "DatabaseTransaction":
        self._transaction = self.conn.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            self._transaction.commit()
        else:
            self._transaction.rollback()
        return False  # Do not suppress exceptions

# Generator-based context manager for simpler cases
@contextmanager
def temp_directory() -> Generator[Path, None, None]:
    import tempfile, shutil
    tmpdir = Path(tempfile.mkdtemp())
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

# Async context manager
@asynccontextmanager
async def managed_http_client() -> AsyncGenerator["httpx.AsyncClient", None]:
    import httpx
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client

# Usage
with temp_directory() as d:
    (d / "output.txt").write_text("hello")

async def fetch_data(url: str) -> dict:
    async with managed_http_client() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

---

## Decorator Patterns

```python
import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

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
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    wait = backoff_seconds * (2 ** attempt)
                    time.sleep(wait)
            raise RuntimeError("unreachable")  # for type checker
        return wrapper
    return decorator

# Cache decorator (use functools.cache for simple cases)
from functools import cache, cached_property

@cache  # LRU cache with unlimited size (use lru_cache(maxsize=N) for bounded)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# cached_property for expensive computed attributes
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @cached_property
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
```

---

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
import asyncio
import httpx

async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()

async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        # All requests run concurrently, results maintain order
        results = await asyncio.gather(
            *[fetch_one(client, url) for url in urls],
            return_exceptions=True,  # Don't let one failure cancel all
        )
    # Separate successes from failures
    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    if failures:
        print(f"{len(failures)} requests failed: {failures}")
    return successes

# Timeout + cancellation
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict | None:
    try:
        async with asyncio.timeout(timeout):  # Python 3.11+
            async with httpx.AsyncClient() as client:
                return (await client.get(url)).json()
    except TimeoutError:
        return None

# Running CPU-bound work without blocking the event loop
async def process_image(path: Path) -> bytes:
    loop = asyncio.get_running_loop()
    # Run blocking function in thread pool to avoid blocking event loop
    return await loop.run_in_executor(None, _sync_compress_image, path)

def _sync_compress_image(path: Path) -> bytes:
    # Synchronous PIL/Pillow operation
    from PIL import Image
    import io
    img = Image.open(path)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()
```

### asyncio Pitfalls

```python
# WRONG: Never use time.sleep() in async code — it blocks the event loop
async def bad_wait():
    time.sleep(1)  # Blocks ALL coroutines

# CORRECT: Use asyncio.sleep()
async def good_wait():
    await asyncio.sleep(1)  # Yields control to event loop

# WRONG: asyncio.gather with unrelated error handling
async def fragile():
    # If any task raises, all others are cancelled
    results = await asyncio.gather(task1(), task2(), task3())

# CORRECT: Use return_exceptions=True for resilient pipelines
async def resilient():
    results = await asyncio.gather(task1(), task2(), task3(), return_exceptions=True)
    return [r for r in results if not isinstance(r, BaseException)]
```

---

## Exception Hierarchy Design

Design exception hierarchies that express business intent, not implementation details.

```python
# Define a base exception for your library/service
class AppError(Exception):
    """Base class for all application errors."""
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code

# Organize by domain, not by HTTP status
class AuthenticationError(AppError):
    """User is not authenticated."""

class AuthorizationError(AppError):
    """User is authenticated but lacks permission."""

class ResourceNotFoundError(AppError):
    """Requested resource does not exist."""
    def __init__(self, resource_type: str, resource_id: str | int) -> None:
        super().__init__(f"{resource_type} '{resource_id}' not found")
        self.resource_type = resource_type
        self.resource_id = resource_id

class ValidationError(AppError):
    """Input data is invalid."""
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"Validation failed for '{field}': {message}")
        self.field = field

# Usage: catch at the right level
try:
    user = get_user(user_id)
except ResourceNotFoundError as e:
    return http_404(str(e))
except AuthenticationError:
    return http_401()
except AppError as e:
    logger.error("App error: %s (code=%s)", e, e.code)
    return http_500()
```

---

## Pathlib Usage

Never use `os.path` — always use `pathlib.Path`.

```python
from pathlib import Path

# Reading and writing
config_path = Path("config") / "settings.toml"
content = config_path.read_text(encoding="utf-8")
config_path.write_text(updated_content, encoding="utf-8")

# Iterating a directory
def find_python_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))

# Safe path construction (no string concatenation)
def build_output_path(base: Path, name: str, suffix: str = ".json") -> Path:
    return (base / "output" / name).with_suffix(suffix)

# Check existence and create directories
output_dir = Path("dist") / "reports"
output_dir.mkdir(parents=True, exist_ok=True)

# Temporary files
import tempfile
with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
    tmp_path = Path(f.name)
# Process tmp_path, then:
tmp_path.unlink(missing_ok=True)
```

---

## Memory and Performance

### `__slots__` for High-Volume Objects

Reduces memory usage by 30-50% for classes instantiated in high volume.

```python
@dataclass(slots=True)   # dataclass with slots — the modern way
class Point:
    x: float
    y: float

# For regular classes:
class Connection:
    __slots__ = ("host", "port", "_socket")
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._socket = None
```

### Generators for Large Data

```python
from collections.abc import Iterator, Generator

def read_large_file(path: Path) -> Iterator[str]:
    """Read file line-by-line without loading into memory."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()

def batched(iterable, n: int) -> Generator[list, None, None]:
    """Yield successive n-sized batches."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch

# Process a 10GB file in 1000-line batches:
for batch in batched(read_large_file(Path("big.csv")), 1000):
    process_batch(batch)
```

### String Building

```python
# WRONG: O(n^2) string concatenation in a loop
result = ""
for item in items:
    result += item + ", "  # Creates a new string object every iteration

# CORRECT: join()
result = ", ".join(items)

# For complex string building with logic:
import io
buf = io.StringIO()
for item in items:
    buf.write(item)
    if item.endswith("."):
        buf.write("\n")
result = buf.getvalue()
```

---

## Testing Patterns with pytest

### Fixture Design

```python
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Scope: function (default), class, module, session
@pytest.fixture(scope="module")
def db_connection():
    """Module-scoped: one connection per test module."""
    conn = create_test_db_connection()
    yield conn
    conn.close()

@pytest.fixture
def user(db_connection) -> User:
    """Function-scoped: fresh user per test."""
    u = User(name="test", email="test@example.com")
    db_connection.insert(u)
    yield u
    db_connection.delete(u)

# Async fixtures
@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

### Parametrize for Combinatorial Coverage

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("  spaces  ", 8),
    ("unicode: ñ", 10),
])
def test_string_length(input: str, expected: int) -> None:
    assert len(input) == expected

# Parametrize with IDs for clarity
@pytest.mark.parametrize("status_code,should_raise", [
    pytest.param(200, False, id="success"),
    pytest.param(404, True, id="not_found"),
    pytest.param(500, True, id="server_error"),
])
def test_response_handling(status_code: int, should_raise: bool) -> None:
    if should_raise:
        with pytest.raises(HTTPError):
            handle_response(MockResponse(status_code))
    else:
        handle_response(MockResponse(status_code))  # Should not raise

# Exception testing
def test_invalid_user_raises_validation_error() -> None:
    with pytest.raises(ValidationError, match="email"):
        UserCreate(name="Bob", email="not-an-email", age=25)
```

### Mocking

```python
from unittest.mock import AsyncMock, MagicMock, patch

def test_fetch_user_calls_http(monkeypatch):
    mock_get = MagicMock(return_value=MagicMock(json=lambda: {"id": 1, "name": "Alice"}))
    monkeypatch.setattr("myapp.client.get", mock_get)
    result = fetch_user(1)
    mock_get.assert_called_once_with("/users/1")
    assert result.name == "Alice"

@pytest.mark.asyncio
async def test_async_fetch(monkeypatch):
    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value={"id": 1})
    mock_response.raise_for_status = MagicMock()
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await fetch_user_async(1)
    assert result["id"] == 1
```

---

## Packaging with pyproject.toml and uv

### pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "0.1.0"
description = "Short description"
requires-python = ">=3.10"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.4",
    "pyright>=1.1",
]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM", "ANN"]
ignore = ["ANN101", "ANN102"]

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "strict"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### uv Commands (Use Instead of pip)

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install project with dev dependencies
uv sync --extra dev

# Add a new dependency
uv add httpx

# Add a dev dependency
uv add --dev pytest-asyncio

# Run a command inside the project env
uv run pytest
uv run pyright
uv run ruff check .

# Run without installing (like npx)
uvx ruff check .
uvx mypy .
```

---

## Tooling Integration Summary

| Tool | Purpose | Command |
| --- | --- | --- |
| `ruff check` | Linting (replaces flake8, isort, pylint) | `uv run ruff check .` |
| `ruff format` | Formatting (replaces black) | `uv run ruff format .` |
| `pyright` | Type checking (strict mode) | `uv run pyright` |
| `pytest` | Testing | `uv run pytest --cov=src` |
| `uv` | Package management (replaces pip, venv) | `uv sync`, `uv add` |

---

## Self-Verification Checklist

Before declaring a Python task complete, verify:

- [ ] `uv run ruff check .` exits 0 — 0 errors reported (no `# noqa` suppressions without justification)
- [ ] `uv run ruff format --check .` exits 0 — 0 formatting differences
- [ ] `uv run pyright` exits 0 — 0 errors in strict mode (or the agreed mode for this project)
- [ ] All new functions have complete type annotations on parameters and return types
- [ ] No `pip install` was used: `grep -rn "pip install" Makefile scripts/ *.sh` returns = 0 matches
- [ ] Exception handling catches specific types: `grep -rn "except Exception\|except BaseException" src/` returns = 0 matches
- [ ] No `os.path` usage: `grep -rn "os\.path\." src/` returns = 0 matches (replaced by `pathlib.Path`)
- [ ] Mutable default arguments not present: `grep -rn "def .*=\s*\[\|def .*=\s*{" src/` returns = 0 matches
- [ ] `uv run pytest` exits 0 with coverage >= existing baseline %

---

## Success Criteria

A task using this skill is complete when:

1. `uv run ruff check . && uv run ruff format --check . && uv run pyright` all exit with code 0.
2. All new public functions, classes, and methods have type annotations accepted by pyright.
3. `uv run pytest` passes with zero failures and coverage does not regress from the pre-task baseline.
4. No new `# type: ignore` or `# noqa` comments were added without a documented justification comment on the same line.
5. The `pyproject.toml` reflects all new dependencies (no manual `pip install` was used).

---

## Anti-Patterns

- Never use a mutable default argument (e.g., `def f(x=[])`) because Python creates the default object once at function definition time; all callers that omit the argument share the same mutable object, causing state to accumulate across calls.
- Never silence a broad exception with `except Exception: pass` because suppressing all exceptions hides bugs, swallows keyboard interrupts, and makes debugging production failures impossible without additional logging.
- Never import from a module's private namespace (e.g., `from module._internal import X`) because private symbols have no stability guarantee and can be renamed or removed in any minor version without a deprecation notice.
- Never use `is` to compare values (e.g., `x is 1`, `x is "hello"`) because `is` checks object identity, not equality; CPython interns small integers and some strings, making identity comparison coincidentally correct in tests but incorrect in production with different interpreter implementations or string origins.
- Never perform file I/O in a `__init__` method because object construction should not have side effects that require error handling or cleanup; I/O in `__init__` makes the class untestable without touching the filesystem and prevents use of the object in memory-only contexts.
- Never use `time.sleep` in production code to wait for an asynchronous event because sleep-based polling is unpredictable under load — too short causes a busy loop, too long introduces unnecessary latency — and cannot be cancelled cleanly on shutdown.

---

## Failure Modes

| Situation | Response |
| --- | --- |
| pyright reports errors after refactor | Fix the root type error — do not add `# type: ignore`. Narrow the type or add a proper guard. |
| `ruff check` reports import order issues | Run `uv run ruff check --fix .` to auto-fix; review the changes. |
| Async code deadlocks | Audit for `time.sleep()`, blocking DB drivers, or sync code called directly from coroutines. Run in executor. |
| Memory leak in long-running service | Audit for circular references, un-closed file handles, and large objects stored in module globals. Use `tracemalloc`. |
| Test is flaky due to timing | Replace `time.sleep()` assertions with proper async awaits or `pytest-anyio` time controls. |
| uv.lock conflicts in merge | Run `uv sync` after resolving `pyproject.toml` conflict. Commit the regenerated `uv.lock`. |
| Package version conflict | Use `uv add "package>=X,<Y"` to bound the range. Check `uv tree` to see the full dependency graph. |
| Pydantic validation error in production | Add a `try/except ValidationError` at the API boundary and return a structured 422 response with `e.errors()`. |

---

## Integration with Mega-Mind

`python-patterns` is invoked by:

- `backend-architect` when implementing Python services
- `test-genius` when writing pytest suites
- `code-polisher` when refactoring Python code to modern standards
- `migration-upgrader` when upgrading Python version or migrating from Python 2

Hand off to:
- `eval-harness` after writing new logic, to define pass/fail criteria
- `security-reviewer` after implementing auth, crypto, or external API integrations
- `performance-profiler` when async patterns or data processing need benchmarking
