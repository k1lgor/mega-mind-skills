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

## Self-Verification Checklist

- [ ] SHA-256 is used: `grep -rn "sha256\|createHash.*sha256\|hashlib.sha256" <cache_implementation>` returns at least 1 match — MD5 or SHA-1 usage returns 0 matches in the same files
- [ ] Atomic write via temp file + rename: `grep -rn "tmp\|tempfile\|rename\|os.replace\|mv " <cache_write_code>` returns at least 1 match per cache write path — direct writes to the final path return 0 matches
- [ ] Cache miss falls back gracefully: `grep -rn "cache_miss\|fallback\|except\|catch" <cache_implementation>` returns at least 1 match; running the pipeline with an empty cache exits 0
- [ ] Corrupted cache entries handled as miss: `grep -rn "json.JSONDecodeError\|SyntaxError\|corrupt\|invalid.*cache\|except.*parse" <cache_implementation>` returns at least 1 match — unhandled parse errors fail this check
- [ ] Source file path stored in cache entry: `grep -rn "\"source\"\|\"file_path\"\|\"path\"" <cache_entry_schema>` returns at least 1 match; sample cache entries contain a non-empty path value
- [ ] `.cache/` in `.gitignore`: `grep -c "\.cache" .gitignore` returns >= 1 — missing entry means cache files can be accidentally committed
- [ ] `--force` bypass implemented: `grep -rn "\-\-force\|force_rebuild\|skip_cache\|bypass" <pipeline_entrypoint>` returns at least 1 match — no bypass mechanism fails this check

## Success Criteria

This skill is complete when: 1) every file processing call checks the SHA-256 content hash before running expensive work, 2) cache hits skip processing and return stored results without re-reading source files, and 3) cache misses and corrupted entries fall back silently to full processing without crashing the pipeline.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Cache hit returned for file whose content changed but mtime did not update | File on network share or copied with preserved mtime; only mtime checked, not content hash | Always hash file content (SHA-256); never rely on mtime alone as a cache key |
| Hash collision causes wrong cached result served | Two different inputs produce identical hash (extremely rare but non-zero with weak hashes) | Use SHA-256 or stronger; add content-length to cache key as secondary discriminator |
| Cache directory grows unbounded, consuming disk | No eviction policy; every unique input accumulates a cache entry | Implement LRU eviction or TTL expiry; add cache size monitoring alert |
| Cache written without atomic rename, leaving corrupt partial file | Process killed mid-write; partial file accepted as valid on next read | Write to a `.tmp` file, then `fs.rename` atomically; on read, validate file is complete (checksum header) |
| Cached result from different config served to incompatible consumer | Config hash not included in cache key; cache shared across environments | Include all config-affecting variables in the cache key; scope cache directories per environment |

## Anti-Patterns

- Never use `mtime` as the sole cache key because file renames, permission changes, and network-share copies update the modification timestamp without altering content, causing unnecessary reprocessing and invalidating valid cache entries that cost real compute time to regenerate.
- Never use file paths as cache keys because renaming or moving a file causes the cache to treat identical content as entirely new work, re-running every downstream step and negating all previously stored computation.
- Never store the cache directory in Git because committing large binary or derived cache blobs bloats repository history permanently, slows every future `git clone`, and conflates reproducible build outputs with version-controlled source artifacts.
- Never write cache entries directly to the final destination file without an atomic rename because a process kill or crash mid-write leaves a partial file on disk that will be loaded as valid on the next run, returning corrupt data silently.
- Never use MD5 or SHA-1 as the hash algorithm because MD5 has known collision vulnerabilities and SHA-1 has practical collision attacks, meaning two different inputs can produce the same key and serve the wrong cached result.
- Never omit the source file path from the cache entry because debugging a wrong cache hit becomes impossible without knowing which source file produced the stored result, turning data provenance into guesswork.
- Never skip implementing a `--force` bypass flag because without an explicit cache-busting mechanism, developers cannot recover from a poisoned cache without manually deleting cache files, making operational recovery unnecessarily fragile.
