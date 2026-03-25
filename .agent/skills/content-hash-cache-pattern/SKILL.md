---
name: content-hash-cache-pattern
compatibility: Antigravity, Claude Code, GitHub Copilot
description: SHA-256 content hash caching for file processing. Use when processing files (extraction, transformation) to avoid redundant work and reduce LLM costs.
triggers:
  - "content-hash"
  - "file cache"
  - "sha256 cache"
  - "cache key"
  - "cached extraction"
  - "redundant processing"
---

# Content-Hash File Cache Pattern

## Identity

You are a performance and efficiency specialist. You know that file paths are unstable but content is truth. You implement O(1) file-based caching using SHA-256 content hashes, ensuring that file moves/renames never cause a cache miss and content changes never cause a stale hit.

## When to Activate

- Designing file processing pipelines (PDF/text extraction, image processing)
- Implementing caching for expensive LLM operations (summarization, analysis)
- Reducing redundant compute in data transformation scripts
- Optimizing CLI tools that process many local files

---

## Core Pattern

### 1. Content-Hash Based Cache Key

Use file content (not path or timestamp) as the cache key.

```python
import hashlib
from pathlib import Path

_HASH_CHUNK_SIZE = 65536  # 64KB chunks for memory-efficient hashing of large files

def compute_file_hash(path: Path) -> str:
    """SHA-256 of file contents (chunked for large files)."""
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(_HASH_CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()
```

**Why content hash?**

- **Stability:** File rename/move = 100% cache hit.
- **Accuracy:** Any content change = automatic cache invalidation.
- **Simplicity:** No central index file needed; the hash _is_ the pointer.

---

### 2. Frozen Dataclass for Cache Entry

Store metadata along with the cached result to help with debugging and traceability.

```python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class CacheEntry:
    file_hash: str     # SHA-256 key
    source_path: str   # For debugging only
    document: Any      # The cached result (e.g. JSON, extracted text)
```

---

### 3. File-Based Cache Storage

Store each entry as `{hash}.json`. This allows O(1) lookup without loading a massive main index file.

```python
import json

def write_cache(cache_dir: Path, entry: CacheEntry) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{entry.file_hash}.json"

    # Serialize entry (logic omitted for brevity)
    data = {"hash": entry.file_hash, "path": entry.source_path, "data": entry.document}

    cache_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def read_cache(cache_dir: Path, file_hash: str) -> dict | None:
    cache_file = cache_dir / f"{file_hash}.json"
    if not cache_file.is_file():
        return None
    try:
        raw = cache_file.read_text(encoding="utf-8")
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return None  # Treat corruption as a miss
```

---

### 4. Service Layer Wrapper (SRP)

Keep the processing function pure. Wrap it in a service layer that handles the cache logic.

```python
def process_with_cache(
    file_path: Path,
    *,
    cache_enabled: bool = True,
    cache_dir: Path = Path(".cache"),
) -> dict:
    """Service layer: cache check -> processing -> cache write."""
    if not cache_enabled:
        return process_pure(file_path)

    file_hash = compute_file_hash(file_path)

    # 1. Check cache
    cached = read_cache(cache_dir, file_hash)
    if cached is not None:
        return cached["data"]

    # 2. Cache miss -> process
    result = process_pure(file_path)

    # 3. Write cache
    entry = CacheEntry(file_hash=file_hash, source_path=str(file_path), document=result)
    write_cache(cache_dir, entry)

    return result
```

---

## Key Design Decisions

- **SHA-256 over MD5:** Avoid collisions; security is rarely the goal, but uniqueness is.
- **Separate Files over Index:** Avoid global lock contention and memory bloat on large datasets.
- **Frozen Slots:** Minimize memory overhead for large processing batches.
- **Fail Gracefully:** Corruption or IO errors in cache reading should fallback to processing, not crash the app.

---

## Best Practices

- **Use subdirectories** (e.g., `.cache/ab/abcdef...json`) if storing >10,000 files to avoid OS directory performance degradation.
- **Explicit Invalidation:** Add a `--force` flag to bypass cache and re-process.
- **Metadata Storage:** Always store the source path in the cache entry so you can trace where data came from.
- **Atomic Writes:** Write to a temp file and rename it to `{hash}.json` to avoid reading partially written cache entries.

---

## When NOT to Use

- **Small volatility:** If files change every few seconds and processing is cheap (e.g. reading a small JSON).
- **Extremely large files (>2GB):** Hashing may take longer than the processing itself if the processing is simple line-counting.
- **Limited Disk Space:** Cache directories can grow indefinitely; implement a TTL or LRU cleanup if space is tight.

---

## Anti-Patterns

- **Using timestamps only:** `mtime` changes on renames or permission edits without content changes.
- **Using paths as keys:** Moving a file shouldn't invalidate its expensive previous analysis.
- **Storing cache in Git:** Unless results are very small and critical for build stability, keep `.cache/` in `.gitignore`.
