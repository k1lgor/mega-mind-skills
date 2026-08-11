---
name: content-hash-cache-pattern
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  SHA-256 content hash caching for file processing to avoid redundant work and reduce LLM costs.
  Use when processing files (extraction, transformation) to avoid redundant work and reduce costs.
  Covers content-hash-based cache key design, frozen dataclass entries, file-based cache storage with O(1) lookup, and service layer wrapper pattern.
category: token-optimization
triggers:
  - "content-hash"
  - "file cache"
  - "sha256 cache"
  - "cache key"
  - "cached extraction"
  - "redundant processing"
  - "deduplicate processing"
  - "cache invalidation"
dependencies:
  - context-optimizer: recommended
---

# Content-Hash File Cache Pattern

## Identity

You are a performance and efficiency specialist. You know that file paths are unstable but content is truth. You implement O(1) file-based caching using SHA-256 content hashes, ensuring that file moves/renames never cause a cache miss and content changes never cause a stale hit.

**Your core responsibility:** Eliminate redundant file processing by caching results keyed by SHA-256 content hash, not file path or timestamp.

**Your operating principle:** Content is truth; file paths are unstable; SHA-256 is the key.

**Your quality bar:** Every cache entry uses SHA-256 content hash as key, stores source path for debugging, writes via atomic rename, and handles corruption gracefully by falling back to processing — no exceptions.

## When to Use

- Designing file processing pipelines (PDF/text extraction, image processing)
- Implementing caching for expensive LLM operations (summarization, analysis)
- Reducing redundant compute in data transformation scripts
- Optimizing CLI tools that process many local files

## When NOT to Use

- **Small volatility:** If files change every few seconds and processing is cheap (e.g. reading a small JSON)
- **Extremely large files (>2GB):** Hashing may take longer than processing itself
- **Limited Disk Space:** Cache directories can grow indefinitely; implement TTL or LRU cleanup

## Core Principles

1. **Content is truth, not path.** File paths are unstable — renaming a file should preserve its cache entry. Only content changes invalidate cache.
2. **SHA-256 for uniqueness.** MD5 has known collisions; SHA-1 has practical collision attacks. Use SHA-256 as the minimum.
3. **Atomic writes prevent corruption.** Write to `.tmp` file, then rename to final path. A partial write on crash must not produce a valid-looking cache entry.
4. **Graceful degradation.** Cache corruption or I/O errors must not crash the application. Fall back to processing.
5. **`--force` overrides cache.** Always provide an explicit cache-busting flag for recovery from poisoned cache entries.

---

## Core Pattern

### Content-Hash Based Cache Key

```python
import hashlib
from pathlib import Path

_HASH_CHUNK_SIZE = 65536  # 64KB chunks for memory-efficient hashing

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

### Service Layer Wrapper

```python
def process_with_cache(file_path: Path, *, cache_enabled: bool = True, cache_dir: Path = Path(".cache")) -> dict:
    """Service layer: cache check -> processing -> cache write."""
    if not cache_enabled:
        return process_pure(file_path)
    file_hash = compute_file_hash(file_path)
    cached = read_cache(cache_dir, file_hash)
    if cached is not None:
        return cached["data"]
    result = process_pure(file_path)
    entry = CacheEntry(file_hash=file_hash, source_path=str(file_path), document=result)
    write_cache(cache_dir, entry)
    return result
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Using mtime as sole cache key | File renames/permission changes/network copies update mtime without content change; unnecessary reprocessing | Always hash file content (SHA-256); never rely on mtime alone |
| Using file paths as cache keys | Renaming/moving file causes cache miss; identical content re-processed | Use content hash, not path, as cache key |
| Storing cache directory in Git | Large binary/derived blobs bloat repo history; slows clones | Add `.cache/` to `.gitignore` |
| Writing cache entries directly without atomic rename | Process kill mid-write leaves partial file; loaded as valid on next run | Write to .tmp file, then fs.rename atomically |
| Using MD5/SHA-1 for hash | Known collision vulnerabilities; two different inputs can produce same key, serving wrong cached result | Use SHA-256 minimum |
| Skipping `--force` bypass flag | Cannot recover from poisoned cache without manually deleting files | Add `--force` flag to bypass cache and re-process |

## Verification

### Self-Verification Checklist

- [ ] Source file path stored in cache entry for debugging
- [ ] `.cache/` in `.gitignore`
- [ ] `--force` bypass flag implemented
- [ ] Atomic writes: write to tmp, then rename
- [ ] Graceful fallback on cache corruption/IO errors
- [ ] SHA-256 (minimum) used for hash

### Verification Commands

```bash
# Check gitignore
grep -c "\.cache" .gitignore

# Verify atomic writes
grep -rn "tmp\|tempfile\|rename\|os.replace\|mv " src/cache.py

# Check fallback handling
grep -rn "cache_miss\|fallback\|except\|catch" src/cache.py

# Verify hash algorithm
grep -rn "sha256" src/cache.py
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Hash Algorithm | SHA-256 minimum used | Replace MD5/SHA-1 with SHA-256 |
| Atomic Writes | Write to temp, then rename | Add atomic write pattern |
| Cache Bypass | `--force` flag implemented | Add flag for recovery |
| Git Safety | `.cache/` in `.gitignore` | Add gitignore entry |

## Examples

### Example 1: PDF Text Extraction Caching

**User request:** "We extract text from 10,000 PDF invoices every day. Most haven't changed since yesterday."

**Skill execution:**
1. Compute SHA-256 hash for each PDF
2. Check cache: 9,200 of 10,000 files unchanged from yesterday
3. Only process the 800 new/modified files
4. Write cache entries for the 800 newly processed results
5. Serve 9,200 cached results instantly

**Result:** 92% cache hit rate. Processing time drops from 4 hours to 20 minutes.

### Example 2: Edge Case - Cache Poisoning Recovery

**User request:** "Our cache returned bad results for 50 files. We need to bust it."

**Skill execution:**
1. Identify the poisoned hash values
2. Run `process_with_cache(file_path, --force)` for those 50 files
3. New results written to cache with atomic rename
4. Verify: `--force` flag bypasses cache and processes fresh

**Result:** Poisoned entries replaced. `--force` flag verified as working recovery mechanism.

## Anti-Patterns

- Never use file modification time (mtime) as the sole cache key because file renames, permission changes, and network copies update mtime without changing content, causing unnecessary reprocessing of every file whose metadata changed.
- Never store the cache directory in version control because large binary or derived blobs bloat repository history and slow down every clone; always add `.cache/` to `.gitignore`.
- Never use MD5 or SHA-1 for content hashing because both have known collision attacks, meaning two different inputs can produce the same hash and serve the wrong cached result.
- Never write cache entries directly without an atomic rename because a process kill mid-write leaves a partial file that the next invocation loads as a valid complete result.

## Performance & Cost

### Parallelization

- **Hashing phase:** Parallelizable across files (I/O-bound, limited by disk speed)
- **Processing phase:** Parallelizable for independent files, but beware of memory pressure
- **Cache writes:** Must be sequential per file (atomic rename); parallel writes to different files are safe

### Storage Budget

- **Cache entry size:** Varies by result type (text: ~1KB, structured JSON: ~2-5KB, embeddings: ~10-100KB)
- **TTL recommendation:** Implement LRU eviction when cache exceeds 1GB or 100K entries
- **Expected context usage:** 1-2KB per cache pattern design session

## References

### Internal Dependencies
- `context-optimizer` — Manages context for large cache operations

### External Standards
- [NIST SHA-256](https://csrc.nist.gov/publications/detail/fips/180/4/final) — Secure Hash Standard

### Related Skills
- `context-optimizer` — Companion skill for managing cached data in context

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Examples (see below), References, Changelog. |
---
