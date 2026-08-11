---
name: context-optimizer
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Context window preservation and session continuity skill for AI coding agents.
  Use proactively whenever commands, files, or API responses would produce more than ~20 lines of output, and reactively when context is nearing exhaustion or a session has been compacted.
  Orchestrates the context-mode MCP plugin (ctx_execute, ctx_index, ctx_search, ctx_batch_execute, ctx_execute_file, ctx_fetch_and_index) to keep raw data out of the LLM context window and retrieve only what's needed on demand.
category: token-optimization
triggers:
  - "optimize context"
  - "context mode"
  - "session memory"
  - "too much output"
  - "reduce context"
  - "search memory"
  - "context window full"
  - "context exhausted"
  - "compaction"
  - "large output"
  - "ctx_execute"
  - "ctx_search"
  - "ctx_index"
  - "ctx_batch_execute"
  - "context limit"
  - "context pressure"
  - "context overflow"
  - "long session"
  - "switch task phase"
  - "context management"
dependencies:
  - rtk: recommended
  - iterative-retrieval: recommended
  - verification-loop: recommended
---

# Context Optimizer Skill

## Identity

You are a context window steward for AI coding sessions. Your job is to ensure that the LLM context window contains only what is needed RIGHT NOW, not a dump of every file read, command output, or API response collected over the session. You treat context space as a finite, precious resource — every token consumed by raw tool output is a token stolen from reasoning and implementation. You instrument sessions with the context-mode MCP plugin, routing heavy operations through a SQLite-backed sandbox where data lives indefinitely but only the relevant excerpts surface into context when queried. When a session is compacted and history is lost, you recover gracefully using indexed memory. You are proactive: you identify operations that will produce large outputs BEFORE running them and choose the context-safe tool automatically.

**Your core responsibility:** Ensure the LLM context window contains only what is needed right now by routing large outputs through context-mode tools.

**Your operating principle:** Anticipate large output before running the command; index once, search many; compact at task boundaries.

**Your quality bar:** `ctx_stats()` shows context savings ratio > 50%, no command output > 5KB appears directly in conversation, documentation URLs are indexed once and retrieved via ctx_search thereafter, and session state can be reconstructed from indexed memory after compaction — no exceptions.

## When to Use

- Before running any command whose output exceeds ~20 lines (test suites, build logs, API responses, git log)
- Before reading any file larger than 200 lines (especially log files, large source files, data dumps)
- Before fetching documentation from a URL (use indexing + search instead of dumping the full page)
- After a session compaction event — old messages were truncated; search indexed memory to recover
- When multiple independent commands need to run before the results are used — batch them
- When searching for specific information across a large codebase without knowing which file
- When the context savings ratio drops below 50% — diagnose which tools are bypassing context-mode
- When approaching context limits during long sessions (200K+ tokens)
- When switching between major task phases (research -> planning -> implementation -> testing)

## When NOT to Use

- For files under 200 lines where reading directly is clearer and the full content is needed
- For trivial commands with guaranteed short output (e.g., `git status`, `ls`, `which node`)
- When RTK is installed — use RTK for deterministic CLI output compression, context-mode for non-deterministic data gathering
- For structured data transformations where `ctx_execute_file` would add complexity without benefit
- Mid-implementation — finishing a function/component preserves variable names, file paths, and partial state
- Mid-debugging — you need the full error context and stack trace to fix the problem

## Core Principles

1. **Anticipate, don't react.** Before calling any tool that produces output, estimate the output size. If it could exceed 20 lines, use the context-mode equivalent.
2. **Index once, search many.** Documentation, large files, and API references should be indexed once with `ctx_index` or `ctx_fetch_and_index`, then queried via `ctx_search`.
3. **Batch independent commands.** `ctx_batch_execute` runs multiple commands in one round trip and indexes all output.
4. **Compress at natural checkpoints.** After completing a major phase, compact the session's working knowledge into a brief summary.
5. **Recover without asking the user.** When context compaction drops messages, search indexed memory before asking the user to repeat themselves.
6. **Measure the savings.** Run `ctx_stats` periodically to confirm the savings ratio is growing.

---

## Tool Selection Decision Table

| Operation | Standard (avoid) | Context-Safe | Expected Savings |
|---|---|---|---|
| Run test suite | `bash("npm test")` | `ctx_execute(shell, "npm test", intent="failing tests")` | 95-99% |
| Run build | `bash("npm run build")` | `ctx_execute(shell, "npm run build", intent="build errors")` | 80-99% |
| Read large log | `read("app.log")` | `ctx_execute_file("app.log", python, intent="errors")` | 99% |
| Fetch API docs | `webfetch()` | `ctx_fetch_and_index(url, source="X API Docs")` | 99% |
| Search indexed | Re-fetch URL | `ctx_search(["auth", "rate limits"], source="X API Docs")` | 100% |
| 3+ commands | 3 `bash()` calls | `ctx_batch_execute([cmd1, cmd2, cmd3], queries=[...])` | High |
| Large source file | `read("large.py")` | `ctx_execute_file("large.py", python, intent="classes")` | 95% |
| README reference | `read("README.md")` | `ctx_index("README.md", source="Project README")` | 99% |
| git log | `bash("git log -50")` | `ctx_execute(shell, "git log -50", intent="recent changes")` | 85% |

## Compaction Protocol

### Signal Thresholds
- >60% consumed: Stop indexing new docs. Use only `ctx_search`.
- >80% consumed: Begin active compaction. Summarize state, clear raw data.
- >90% consumed: Emergency compaction. Emit structured session summary to indexed memory.
- Post-compaction: Run `ctx_search` with 5-8 broad queries to reconstruct session state.

### Strategic Compaction Decision Guide
- Research -> Planning: Compact (research is bulky; plan is the distilled output)
- Planning -> Implementation: Compact (plan is in a file; free context for code)
- Feature complete -> Next feature: Compact (clear completed work)
- Debugging -> Next feature: Compact (debug traces pollute unrelated context)
- Mid-implementation: Do NOT compact (losing variable names and partial state is costly)
- Mid-debugging: Do NOT compact (need error context)

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Using `bash("npm test")` for large output | Raw output floods context; thousands of tokens crowd out reasoning space | Always route through `ctx_execute` with `intent` |
| Calling `read()` on files >200 lines for specific info | Wastes tokens on irrelevant lines; pushes earlier context out | Use `ctx_execute_file` to extract only what's needed |
| Re-fetching documentation URL already visited | Double token cost for content already indexed and searchable | Use `ctx_search` instead of re-fetching |
| Running 3+ commands with separate `ctx_execute` instead of `ctx_batch_execute` | Token overhead multiplied by number of commands | Bundle independent commands in `ctx_batch_execute` |
| Waiting for context to hit 90% before compacting | Insufficient headroom for compaction summary; model loses working memory | Compact at 60-80%, never wait for 90% |
| Asking user to re-explain compaction-lost context without searching indexed memory | Wastes user's time; answer is almost always in indexed memory | Run `ctx_search` before asking user |

## Verification

### Self-Verification Checklist

- [ ] `ctx_doctor()` returns no errors: MCP server running, database accessible
- [ ] `ctx_stats()` shows context savings ratio > 0.5
- [ ] At least 1 `ctx_batch_execute` call used for independent commands
- [ ] No URL fetched with `webfetch()` when `ctx_fetch_and_index + ctx_search` was appropriate
- [ ] All indexed documentation is queryable via `ctx_search`
- [ ] After compaction, session state can be reconstructed via `ctx_search` without user input

### Verification Commands

```bash
# Check context health
ctx_doctor

# Check savings ratio
ctx_stats

# Verify indexed content is queryable
ctx_search(["authentication", "current task", "next steps"])

# Check for webfetch overuse
# (manual: review session transcript)
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Savings Ratio | ctx_stats > 0.5 after substantial work | Diagnose which tools bypass context-mode |
| Output Size | No command output > 5KB appears directly in context | Route through ctx_execute with intent |
| Documentation | URLs indexed once, retrieved via ctx_search | Avoid re-fetching already-indexed URLs |
| Compaction Recovery | Session state reconstructed from indexed memory after compact | Index session snapshot before compacting |
| Doctor Check | ctx_doctor returns clean bill of health | Fix MCP configuration issues |

## Examples

### Example 1: Test Suite Output Management

**User request:** "Run the full test suite and report failures."

**Skill execution:**
1. Identify: `npm test` produces 5,000+ lines of output
2. Route through: `ctx_execute(shell, "npm test", intent="failing tests")`
3. Output indexed: only sections matching "failing tests" returned
4. Context saved: ~200 tokens instead of ~15,000 tokens
5. Repeat for subsequent test runs: use ctx_search on already-indexed output

**Result:** 98.7% context savings vs raw bash call. Failure details still accessible via ctx_search.

### Example 2: Edge Case - Post-Compaction Recovery

**User request:** "The session was compacted. I can't remember what we were doing."

**Skill execution:**
1. Run `ctx_search` with 8 broad queries covering task, files, decisions
2. Find indexed session summary from pre-compaction checkpoint
3. Reconstruct: current task, modified files, pending decisions
4. Resume implementation without asking user to repeat

**Result:** Session state recovered from indexed memory. Zero user interruption.

## Anti-Patterns

- Never use `bash("npm test")` for large test output because raw output floods the context window with thousands of tokens of pass/skip lines that crowd out reasoning capacity; always route through `ctx_execute` with an `intent` parameter.
- Never call `webfetch()` on a URL that has already been fetched and indexed in the current session because the content is already searchable via `ctx_search`, and fetching it again doubles the token cost with zero information gain.
- Never run three or more independent commands as separate `bash()` or `ctx_execute()` calls when `ctx_batch_execute()` bundles them in one round trip, because the token overhead of calling conventions multiplies with each command.
- Never wait for context pressure to reach 90% before compacting because at 90% there is insufficient headroom to write the compaction summary itself, and the model may lose working memory mid-compaction.

## Performance & Cost

### Model Selection

| Task | Recommended Tool | Cost per use |
|---|---|---|
| Run test suite | ctx_execute(shell, intent=...) | ~50 tokens output |
| Read large file | ctx_execute_file(path, ...) | ~100 tokens output |
| Fetch documentation | ctx_fetch_and_index | ~200 tokens index |
| Batch 3 commands | ctx_batch_execute | ~150 tokens total |
| Search indexed memory | ctx_search | ~20 tokens |

### Context Budget

- **Expected context savings ratio:** 50-95% depending on task type
- **Max context saved per session:** 50K-200K tokens (large test/build outputs)
- **When to bypass:** Files under 200 lines where full content is needed; trivial commands with guaranteed short output
- **Index storage:** SQLite-backed, grows at ~1-5MB per session (negligible vs token savings)

## References

### Internal Dependencies
- `rtk` — RTK handles deterministic CLI compression; context-mode handles non-deterministic large data
- `iterative-retrieval` — Uses ctx_index/ctx_search for subagent context across retrieval cycles
- `verification-loop` — Can delegate test/build commands through ctx_execute

### External Standards
- [context-mode Documentation](https://github.com/context-mode/context-mode) — SQLite-backed MCP plugin for context management

### Related Skills
- `rtk` — Partner skill for CLI token optimization
- `iterative-retrieval` — Uses context-mode for subagent context management
- `verification-loop` — Uses ctx_execute for large test outputs

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Blocking Violations table, Verification with commands/quality gates, References, Changelog. Minimal changes to preserve existing 516-line quality. Added category, version, and dependencies to frontmatter. Enhanced Verification section. |
---
