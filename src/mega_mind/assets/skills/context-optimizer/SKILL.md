---
name: context-optimizer
compatibility: Antigravity, Claude Code, GitHub Copilot
description: |
  Context Mode optimization skill for preventing context window exhaustion and
  maintaining session continuity. Use this skill to query the FTS5 document
  index, execute data-heavy commands safely in the sandbox, and process files
  without flooding the context window.
triggers:
  - "optimize context"
  - "context mode"
  - "session memory"
  - "too much output"
  - "reduce context"
  - "search memory"
---

# Context Optimizer Skill

## Overview

The Context Optimizer skill leverages the `context-mode` MCP server to dramatically reduce LLM context window bloat (by up to 98%). It intercepts heavy tool outputs, keeping raw data in a secure SQLite sandbox and indexing it via FTS5/BM25 for on-demand retrieval.

## When to Use

- **When running commands with massive output**: `curl`ing large JSONs or HTML pages, tailing large log files, running comprehensive test suites.
- **When searching across a large codebase**: Indexing documentation or large legacy files without dumping them into context.
- **When recovering from session truncation**: If older parts of the conversation are forgotten, use this skill to search the session memory.

## Mandatory Tool Usage

When `context-mode` is active, you **MUST** prefer its tools over standard file reads or terminal executions for operations expected to yield >1KB of data.

| Standard Approach                          | Context-Optimized Approach | Context Savings          |
| ------------------------------------------ | -------------------------- | ------------------------ |
| Multiple `execute`                         | `ctx_batch_execute`        | High (Batching)          |
| Running `curl` or `bun test (or npm test)` | `ctx_execute`              | 99% (Stdout filtering)   |
| `cat large_file.log`                       | `ctx_execute_file`         | 99% (Sandbox processing) |
| Loading full API docs                      | `ctx_fetch_and_index`      | 99% (FTS5 indexing)      |
| Repeated searches                          | `ctx_search`               | On-demand retrieval      |

## Command Reference

### Diagnostics & Stats

Always start by checking if Context Mode is installed and functioning:

- `ctx_stats`: View total context savings and session usage statistics.
- `ctx_doctor`: Diagnose hooks, local SQLite DB, and ensure your system is properly configured to route through the sandbox.

### Executing Code & Commands Safely

Use `ctx_execute` for any command that might produce large output:

```json
{
  "language": "shell",
  "code": "npm run test",
  "intent": "failing tests"
}
```

_Why this is better:_ If the output is >5KB, it doesn't flood the context window. The server indexes it and returns a summary. You then use `ctx_search` to find "failing tests".

### Batch Execution

If you need to run multiple commands (e.g., `npm list`, `cat package.json`, `git log`), use `ctx_batch_execute` INSTEAD of running them sequentially. It executes all provided commands and allows querying the results in a single turnaround.

### Indexing and Searching Knowledge

**Indexing Web Docs:**
Instead of `read_url_content`, use `ctx_fetch_and_index`:

```json
{
  "url": "https://docs.example.com",
  "source": "Example API Docs"
}
```

**Indexing Local Files / Code:**
Use `ctx_index` for any large Markdown, README, or logs.

**Retrieving Data:**
Once indexed, use `ctx_search` with multiple queries:

```json
{
  "queries": ["how to authenticate", "rate limits"],
  "source": "Example API Docs"
}
```

## Best Practices

1. **Never use standard `read_file` on files >200 lines.** Use `ctx_execute_file` with a short bash or python script to extract only the information you need, or `ctx_index` if you plan to search it repeatedly.
2. **Combine with RTK.** Use `rtk` tools for deterministic CLI operations (like `git status`) and `context-mode` tools for non-deterministic or heavy data gathering (like `curl` or full test suite runs).
3. **If you forget context, search.** If the conversation compacts and you lose track of recent errors, use `ctx_search` rather than asking the user to repeat the error.

## Integration with Mega-Mind

This skill is automatically invoked when context optimization or memory search is required. As an agent, adopt these tools organically whenever you anticipate large data payloads.
