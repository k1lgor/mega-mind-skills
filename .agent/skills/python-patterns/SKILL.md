---
name: python-patterns
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Python design patterns and best practices. Use for Python-specific development, type hinting, and performance optimization.
triggers:
  - "python patterns"
  - "idiomatic python"
  - "python threading"
  - "python async"
  - "type hints"
  - "__slots__"
---

# Python Development Patterns

## Identity

You are a Python expert focused on readability, performance, and idiomatic code ("The Zen of Python"). You prioritize explicit code over magic, use modern type hints (3.9+), and understand the memory and concurrency trade-offs of the Python interpreted environment.

## When to Activate

- Writing new Python services or utilities
- Refactoring legacy Python code to modern standards
- Optimizing Python performance (memory/CPU)
- Implementing concurrency (Async, Threading, Multiprocessing)

---

## Core Principles

1. **Readability Counts**: Focus on PEP 8 compliance and clear variable names.
2. **Explicit is Better Than Implicit**: Avoid magic **getattr** or global state where possible.
3. **EAFP (Easier to Ask Forgiveness Than Permission)**: Use try-except blocks instead of pre-checking if/exists.

---

## Modern Type Hints (3.9+)

Use the built-in generics instead of the deprecated `typing` equivalents.

```python
# Modern (Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Protocol-Based Duck Typing
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: list[Renderable]) -> str:
    return "\n".join(item.render() for item in items)
```

---

## Memory & Performance

### 1. Using `__slots__`

Reduces memory usage by up to 40% for objects created in high volume.

```python
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y
```

### 2. Generators for Large Data

Avoid loading massive lists into memory.

```python
def read_massive_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

### 3. String Building

Use `"".join()` or `io.StringIO` instead of loop concatenation (which is O(n²)).

---

## Concurrency Decision Matrix

| Type                | Best For                     | Implementation                           |
| ------------------- | ---------------------------- | ---------------------------------------- |
| **AsyncIO**         | Concurrent I/O (APIs, DBs)   | `async def`, `await`                     |
| **Threading**       | I/O-bound with blocking libs | `concurrent.futures.ThreadPoolExecutor`  |
| **Multiprocessing** | CPU-bound (Encoding, Data)   | `concurrent.futures.ProcessPoolExecutor` |

---

## Tooling Integration

- **Formatter:** `ruff format`
- **Linter:** `ruff check`
- **Type Checker:** `pyright` or `mypy`
- **Manager:** `uv` (strongly recommended over pip)

---

## Anti-Patterns to Avoid

- **Mutable Default Arguments:** Never use `def foo(items=[])`. Use `None`.
- **Catching Base Exception:** Never use `except Exception:`. Be specific.
- **Manual Path Concatenation:** Always use `pathlib.Path` over `os.path.join`.
