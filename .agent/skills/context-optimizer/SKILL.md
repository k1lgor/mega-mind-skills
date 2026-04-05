---
name: context-optimizer
compatibility: Antigravity, Claude Code, GitHub Copilot, OpenCode, Cursor
description: Context window preservation and session continuity skill for AI coding agents. Orchestrates the context-mode MCP plugin — ctx_execute, ctx_index, ctx_search, ctx_batch_execute, ctx_execute_file, ctx_fetch_and_index — to keep raw data out of the LLM context window and retrieve only what's needed on demand. Use this skill proactively whenever commands, files, or API responses would produce more than ~20 lines of output, and reactively when context is nearing exhaustion or a session has been compacted.
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
---

# Context Optimizer Skill

## Identity

You are a context window steward for AI coding sessions. Your job is to ensure that the LLM context window contains only what is needed RIGHT NOW, not a dump of every file read, command output, or API response collected over the session. You treat context space as a finite, precious resource — every token consumed by raw tool output is a token stolen from reasoning and implementation. You instrument sessions with the context-mode MCP plugin, routing heavy operations through a SQLite-backed sandbox where data lives indefinitely but only the relevant excerpts surface into context when queried. When a session is compacted and history is lost, you recover gracefully using indexed memory. You are proactive: you identify operations that will produce large outputs BEFORE running them and choose the context-safe tool automatically.

## When to Activate

- Before running any command whose output exceeds ~20 lines (test suites, build logs, API responses, git log)
- Before reading any file larger than 200 lines (especially log files, large source files, data dumps)
- Before fetching documentation from a URL (use indexing + search instead of dumping the full page)
- After a session compaction event — old messages were truncated; search indexed memory to recover
- When multiple independent commands need to run before the results are used — batch them
- When searching for specific information across a large codebase without knowing which file
- When the context savings ratio drops below 50% — diagnose which tools are bypassing context-mode
- When approaching context limits during long sessions (200K+ tokens)
- When switching between major task phases (research → planning → implementation → testing)

## When NOT to Use

- For files under 200 lines where reading directly is clearer and the full content is needed
- For trivial commands with guaranteed short output (e.g., `git status`, `ls`, `which node`)
- When RTK is installed — use RTK for deterministic CLI output compression, context-mode for non-deterministic data gathering
- For structured data transformations where `ctx_execute_file` would add complexity without benefit
- Mid-implementation — finishing a function/component preserves variable names, file paths, and partial state
- Mid-debugging — you need the full error context and stack trace to fix the problem

---

## Core Principles

1. **Anticipate, don't react.** Before calling any tool that produces output, estimate the output size. If it could exceed 20 lines, use the context-mode equivalent. Do not wait to see the flood before redirecting it.
2. **Index once, search many.** Documentation, large files, and API references should be indexed once with `ctx_index` or `ctx_fetch_and_index`, then queried via `ctx_search` for the rest of the session. Never re-read the same large file twice.
3. **Batch independent commands.** If three commands need to run before you act on their results, `ctx_batch_execute` runs them in one round trip and indexes all output. Three sequential `ctx_execute` calls are worse — they cost context on each return.
4. **Compress at natural checkpoints.** After completing a major phase (e.g., "explored the codebase", "diagnosed the bug"), compact the session's working knowledge into a brief summary comment or indexed note. Do not carry raw exploration output forward.
5. **Recover without asking the user.** When context compaction drops messages, search the indexed session memory before asking the user to repeat themselves. The answer is almost always there.
6. **Measure the savings.** Run `ctx_stats` periodically to confirm the savings ratio is growing. If it is flat, context-mode tools are not being used. If it is negative, there is a configuration problem.

---

## Tool Selection Decision Table

| Operation                                    | Standard Approach (avoid)        | Context-Safe Approach          | Expected Savings |
| -------------------------------------------- | -------------------------------- | ------------------------------ | ---------------- |
| Run test suite                               | `bash("npm test")`               | `ctx_execute(shell, "npm test", intent="failing tests")` | 95-99% |
| Run build command                            | `bash("npm run build")`          | `ctx_execute(shell, "npm run build", intent="build errors")` | 80-99% |
| Read a large log file                        | `read("app.log")`                | `ctx_execute_file("app.log", python, intent="errors after 14:00")` | 99% |
| Fetch API documentation                      | `webfetch("https://docs.x.com")` | `ctx_fetch_and_index("https://docs.x.com", source="X API Docs")` | 99% |
| Search indexed docs for specific info        | Re-fetch the URL                 | `ctx_search(["authentication endpoint", "rate limits"])` | 100% |
| Run 3+ independent commands                  | 3 separate `bash()` calls        | `ctx_batch_execute([cmd1, cmd2, cmd3], queries=[...])` | High |
| Analyze a large source file for patterns     | `read("large_file.py")`          | `ctx_execute_file("large_file.py", python, intent="class definitions")` | 95% |
| Load README into memory for reference        | `read("README.md")`              | `ctx_index("README.md", source="Project README")` | 99% |
| Run git log to find recent changes           | `bash("git log --oneline -50")`  | `ctx_execute(shell, "git log --oneline -50", intent="recent changes")` | 85% |
| Check context savings for the session        | N/A                              | `ctx_stats()`                  | N/A |

---

## ctx_execute — When and How

Use `ctx_execute` for any command or code that might produce large output. The `intent` parameter is critical — it tells the context-mode engine what information to extract and surface.

```typescript
// Pattern 1: Run a test suite and surface only failures
ctx_execute({
  language: "shell",
  code: "npm test -- --reporter=verbose",
  intent: "failing tests and error messages"
})
// Returns: summary of failing tests + top matching sections
// Full output stays in SQLite sandbox

// Pattern 2: Run a Python analysis that produces a large result set
ctx_execute({
  language: "python",
  code: `
import json, subprocess
result = subprocess.run(['python', 'scripts/analyze.py'], capture_output=True, text=True)
# Print only the summary — full data stays in sandbox
data = json.loads(result.stdout)
print(f"Total records: {data['total']}")
print(f"Anomalies: {data['anomalies'][:5]}")  # First 5 only
  `,
  intent: "anomalies and summary statistics"
})

// Pattern 3: Check build errors without flooding context
ctx_execute({
  language: "shell",
  code: "tsc --noEmit 2>&1",
  intent: "TypeScript compilation errors"
})
```

### When intent is provided and output is large (>5KB):
The engine indexes the output and returns section titles + previews. Use `ctx_search` to drill into specific sections.

```typescript
// After ctx_execute returns "Searchable terms: TS2304, TS2345, cannot find name"
ctx_search({
  queries: ["TS2304 cannot find name", "implicit any type error"],
  source: "TypeScript build output"
})
```

---

## ctx_execute_file — When and How

Use `ctx_execute_file` when you need to analyze a file without reading it entirely into context. The file content is loaded into the `FILE_CONTENT` variable in the sandbox.

```typescript
// Pattern 1: Extract specific information from a large log file
ctx_execute_file({
  path: "/var/log/app/api.log",
  language: "python",
  code: `
import re
errors = []
for line in FILE_CONTENT.split('\\n'):
    if 'ERROR' in line or 'FATAL' in line:
        errors.append(line.strip())

print(f"Total errors: {len(errors)}")
for err in errors[-10:]:  # Last 10 errors
    print(err)
  `,
  intent: "recent errors and their patterns"
})

// Pattern 2: Summarize a large source file's structure
ctx_execute_file({
  path: "src/services/payment.service.ts",
  language: "python",
  code: `
import re
# Extract class and method names
classes = re.findall(r'^class\\s+(\\w+)', FILE_CONTENT, re.MULTILINE)
methods = re.findall(r'^\\s+(?:async\\s+)?(?:public|private|protected)?\\s*(\\w+)\\s*\\(', FILE_CONTENT, re.MULTILINE)
print(f"Classes: {classes}")
print(f"Methods ({len(methods)}): {methods[:20]}")
  `,
  intent: "class structure and method names"
})
```

---

## ctx_index and ctx_search — When and How

Index content that will be queried multiple times during the session. Search it on demand instead of re-loading.

```typescript
// Index a large README for the session
ctx_index({
  path: "README.md",
  source: "Project README"
})

// Index API documentation from a URL
ctx_fetch_and_index({
  url: "https://docs.stripe.com/api",
  source: "Stripe API Docs"
})

// Search indexed content — batch all questions in ONE call
ctx_search({
  queries: [
    "webhook signature verification",
    "charge create endpoint parameters",
    "idempotency key usage"
  ],
  source: "Stripe API Docs",
  limit: 3  // Top 3 results per query
})

// Search without source filter (searches all indexed content)
ctx_search({
  queries: ["authentication flow", "JWT token refresh"],
  contentType: "code"  // Only return code blocks
})
```

---

## ctx_batch_execute — When and How

Use `ctx_batch_execute` whenever you need to run multiple independent commands AND query the results. It is the single most impactful context-saving tool.

```typescript
// Pattern: Project state assessment — run everything in one shot
ctx_batch_execute({
  commands: [
    { label: "Package JSON",   command: "cat package.json" },
    { label: "TypeScript Config", command: "cat tsconfig.json" },
    { label: "Source Tree",    command: "find src -name '*.ts' | head -30" },
    { label: "Recent Commits", command: "git log --oneline -10" },
    { label: "Test Status",    command: "npm test -- --passWithNoTests 2>&1 | tail -20" },
    { label: "Lint Status",    command: "npm run lint 2>&1 | tail -20" }
  ],
  queries: [
    "main entry point and framework",
    "failing tests",
    "lint errors",
    "recent changes to auth or payment code"
  ]
})
// All 6 commands run, all output indexed, all 4 queries answered — 1 context token round trip
```

---

## Compaction Protocol

When context is nearing exhaustion or after a compaction event:

### Signal Thresholds

| Context Usage    | Action Required                                                  |
| ---------------- | ---------------------------------------------------------------- |
| >60% consumed    | Stop indexing new documentation. Use only `ctx_search`.          |
| >80% consumed    | Begin active compaction: summarize current state, clear raw data.|
| >90% consumed    | Emergency compaction. Emit a structured session summary to indexed memory. |
| Post-compaction  | Run `ctx_search` with 5-8 broad queries to reconstruct session state. |

### Emergency Compaction Procedure

```markdown
## Session State Snapshot — [timestamp]

### Task in Progress
[1-2 sentences: what we are building/fixing]

### Files Modified
- [file path]: [what changed and why]

### Key Decisions Made
- [decision]: [rationale]

### Current Blockers
- [blocker]: [attempted approaches]

### Next Steps
1. [next action]
2. [following action]
```

Index this summary immediately:
```typescript
ctx_index({
  content: "<the snapshot markdown above>",
  source: "Session Snapshot " + new Date().toISOString()
})
```

### Post-Compaction Recovery

```typescript
// Recover session state after compaction
ctx_search({
  queries: [
    "task in progress current work",
    "files modified changes made",
    "blockers and decisions",
    "next steps todo",
    "errors encountered"
  ]
})
```

---

## Strategic Compaction Protocol

Strategic compaction preserves critical state by compacting at **logical task boundaries** rather than waiting for auto-compaction at arbitrary points.

### Compaction Decision Guide

| Phase Transition                | Compact? | Why                                                            |
| ------------------------------- | -------- | -------------------------------------------------------------- |
| Research → Planning             | ✅ Yes   | Research context is bulky; plan is the distilled output        |
| Planning → Implementation       | ✅ Yes   | Plan is in a file; free up context for code                    |
| Feature complete → Next feature | ✅ Yes   | Clear completed work before starting new                       |
| Debugging → Next feature        | ✅ Yes   | Debug traces pollute context for unrelated work                |
| After a failed approach         | ✅ Yes   | Clear dead-end reasoning before trying differently             |
| Mid-implementation              | ❌ No    | Losing variable names, file paths, partial state is costly     |
| Mid-debugging                   | ❌ No    | You need the error context to fix the error                    |
| Implementation → Testing        | ⚠️ Maybe | Keep if tests reference recent code; compact if fully separate |

### What Survives Compaction

| Persists After Compact                 | Lost After Compact                  |
| -------------------------------------- | ----------------------------------- |
| `AGENTS.md` / `CLAUDE.md` instructions | Intermediate reasoning and analysis |
| Task tracker (`docs/plans/task.md`)    | File contents you previously read   |
| Memory files (if using claude memory)  | Multi-step conversation context     |
| Git state (commits, branches, files)   | Tool call history and counts        |
| All files on disk                      | Nuanced preferences stated verbally |

### Protocol: Compact with Intention

**Before Compacting:**
1. Save decisions, file paths, and next steps to `docs/plans/session-notes.md` — anything not on disk is lost
2. Update `docs/plans/task.md` — task tracker must be current
3. Commit work in progress if at a stable point (optional but recommended)

**Compacting:**
```
/compact Focus on implementing [next phase]. Context: [key facts to carry forward]
```
The custom message is your bridge — be specific about what to focus on next.

**After Compacting:**
1. Read `docs/plans/task.md` and `docs/plans/session-notes.md` to restore state
2. Continue from exactly where the notes say to continue

### Token Optimization Patterns

**Trigger-Table Lazy Loading** — skills load only when triggered (this is why SKILL.md frontmatter triggers matter):

| Trigger                   | Skill                   |
| ------------------------- | ----------------------- |
| "test", "tdd", "coverage" | test-driven-development |
| "security", "auth", "xss" | security-reviewer       |
| "deploy", "ci/cd"         | deployment-patterns     |
| "migrate", "schema"       | database-migrations     |

**Context Composition Awareness** — monitor what consumes context: `AGENTS.md` (always loaded), loaded skills (1–5K each), conversation history (grows each exchange), tool results (file reads, search results, terminal output). Keep `AGENTS.md` lean and use RTK-wrapped commands (`rtk npm test`, `rtk git diff`) for 60-90% smaller output.

### Context Compaction Signals

Watch for these 5 warning signs that context pressure is building:
- Responses become repetitive or miss earlier context
- You're re-reading files you already read earlier in the session
- The session has run >100 tool calls
- You've finished a major phase (research, planning, a full feature)
- You're about to start something completely different

### Example: Research → Implementation Transition

```
Situation: Just finished researching 3 auth library options.
           About to start implementing chosen option.

Step 1: Write decision to disk
  docs/decisions/auth-library-choice.md:
    "Chose better-auth over next-auth because:
     - TypeScript-first
     - Built-in rate limiting
     - No database adapter needed for our setup"

Step 2: Update task tracker
  docs/plans/task.md → mark "Research auth options" as complete

Step 3: Compact
  /compact Starting auth implementation with better-auth.
           Install: `npm install better-auth`
           Config goes in: lib/auth/config.ts
           Key docs: https://better-auth.com/docs/setup

Step 4: After compaction
  AI reads task.md and auth-library-choice.md → resumes cleanly
```

---

## Session Continuity Patterns

### Beginning of a New Session (picking up previous work)

```typescript
// 1. Check if previous session data exists
ctx_stats()

// 2. If indexed content exists, search for context
ctx_search({
  queries: [
    "task status and progress",
    "last known errors",
    "files being worked on"
  ]
})

// 3. Quickly re-orient with current project state
ctx_batch_execute({
  commands: [
    { label: "Git Status",     command: "git status" },
    { label: "Recent Changes", command: "git diff --stat HEAD~3" },
    { label: "Test Status",    command: "npm test -- --passWithNoTests 2>&1 | tail -10" }
  ],
  queries: ["what changed", "test failures", "uncommitted work"]
})
```

---

## Self-Verification Checklist

Before concluding that context-mode is properly in use for a session:

- [ ] `ctx_doctor()` returns no errors: MCP server is running, SQLite FTS5 database is accessible, and all hooks are registered — output contains 0 lines matching "ERROR\|FAIL\|not found"
- [ ] `ctx_stats()` shows context savings ratio > 0.5: output line matching `context_savings_ratio` contains a value >= 0.50 — ratio < 0.5 after substantial work means context-mode is not being used correctly
- [ ] At least 1 `ctx_batch_execute` call used: session transcript contains `ctx_batch_execute` — `grep -c "ctx_batch_execute" <session_log>` returns >= 1; multiple sequential `ctx_execute` calls for independent commands are absent
- [ ] No large file read with standard `read()` when `ctx_execute_file` was appropriate: `grep -rn "read(.*\.(log\|json\|csv\|md))" <session_log>` returns 0 matches for files > 200 lines — confirmed by checking file sizes
- [ ] No URL fetched with `webfetch()` when `ctx_fetch_and_index + ctx_search` was appropriate: `grep -c "webfetch" <session_log>` returns 0 for documentation or reference URLs — allowed only for one-off quick lookups
- [ ] All indexed documentation is queryable: `ctx_search(["<topic>"])` returns at least 1 result for each major topic indexed in the session — 0 results for a recently indexed topic is a failure
- [ ] Session state recoverable after compaction without asking user: `grep -c "ctx_search\|ctx_index" <post_compaction_log>` returns >= 1 — state was restored via search, not by asking the user to re-provide context
- [ ] Compact output contains every decision made in the original context (count "decided", "chose", "selected", "will use" in original vs compact — must match)
- [ ] Every decision in the compact has a "because Y" rationale preserved (count decisions without rationale = 0)
- [ ] Compact triggers only at a task boundary (last action before compaction was a completed step, not a mid-operation tool call)

## Success Criteria

Task is complete when:

1. `ctx_stats()` reports context savings ratio >50% for sessions with substantial tool usage
2. No command output longer than 5KB appears directly in the conversation context (all routed through ctx_* tools)
3. Documentation URLs are indexed exactly once per session and retrieved via `ctx_search` thereafter
4. After a simulated compaction, session state can be reconstructed via `ctx_search` in one call without user input
5. `ctx_doctor()` returns a clean bill of health with all systems operational
6. All important context (decisions, file locations, next steps) is persisted to disk before compaction
7. The compact message provides enough specificity for the post-compact session to resume without re-discovery

---

## Anti-Patterns

- Never use `bash("npm test")` or `bash("tsc --noEmit")` for commands that produce large output because the raw output floods the context window directly, consuming thousands of tokens that crowd out reasoning space and cannot be searched or filtered after the fact — always route through `ctx_execute` with an `intent`.
- Never call `read()` on files over 200 lines when the goal is to extract specific information because loading the entire file into context wastes tokens on irrelevant lines and pushes earlier context out of the active window, forcing re-reads in later turns — use `ctx_execute_file` instead.
- Never re-fetch a documentation URL you already visited because a second `webfetch()` call on the same URL re-ingests the full HTML into context, doubling the token cost for content that is already indexed and searchable via `ctx_search`.
- Never run 3+ independent commands with separate `ctx_execute` calls when `ctx_batch_execute` would bundle them because sequential calls each return a summary to context, multiplying token overhead by the number of commands when a single batched call would index all output and answer queries in one round trip.
- Never wait for context to hit 90% before compacting because emergency compaction at 90% leaves insufficient headroom for the compaction summary itself, causing the model to lose working memory before it can write a recovery snapshot.
- Never ask the user to re-explain context that was lost to compaction without first running `ctx_search` on indexed session memory because the indexed content almost always contains the answer, and asking the user to repeat themselves wastes their time and signals that the session state was not managed correctly.
- Never ignore the `ctx_stats()` savings ratio because a ratio below 50% after substantial work means context-mode tools are not being invoked on large outputs, which will cause context exhaustion within the same session and force an unplanned compaction that loses working memory.
- Never compact active working memory because discarding in-progress state mid-task leaves the agent unable to resume without full re-derivation.
- Never write a compact without preserving the "because Y" for every decision because a decision without rationale is unverifiable and will be re-litigated in every subsequent phase.
- Never trigger compaction mid-operation because the agent's state machine has no checkpoint at that point and the partial state cannot be safely reconstructed.
- Never skip validating the compact against the original because compaction errors are silent and a missing constraint propagates through all downstream phases undetected.
- Never use a single compaction granularity for all tasks because a high-level compact is insufficient for detail-heavy phases and a low-level compact wastes context budget on trivial tasks.
- Never compact without recording what was removed because the removed content may be needed for rollback or audit and its absence becomes invisible once overwritten.

---

## Failure Modes

| Situation                                          | Response                                                                                     |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ctx_execute` hangs or times out                   | Stuck sandboxed process. Kill via `ctx_doctor`. Check if the command hangs interactively. Add a timeout parameter. |
| Index is corrupted or returns empty results        | Re-index with `ctx_index` (overwrite). Run `ctx_doctor` to check FTS5 database health. |
| Context savings ratio is 0% or negative            | Context-mode tools not being invoked. Check hooks via `ctx_doctor`. Verify calls use `ctx_*` prefix. |
| Session compacted, memory lost                     | Run `ctx_search` with broad queries (task, files, errors). Check if index was cleared between sessions. |
| `ctx_search` returns irrelevant results            | Query too broad. Use 2-4 specific technical terms. Filter by `source` if multiple docs are indexed. |
| `ctx_batch_execute` output is too large            | Output auto-indexed when >5KB. Use the `queries` parameter to extract relevant sections. |
| Compaction loses decision rationale                | Summary too high-level ("decided X" without "because Y"). Always preserve rationale — it's more valuable than the decision. |
| Compaction hits wrong context window               | Agent compacted working memory instead of history. Separate active memory from completed history before compacting. |
| Summary at wrong granularity                       | Too high-level causes re-derivation in next phase. Calibrate detail to the next phase's needs. |
| Compact triggered mid-task                         | Partial state discarded. Only compact at task boundaries — never mid-operation. |
| Compacted output not validated                     | Missing constraints propagate silently. Diff compact against original on all decision points after compacting. |

---

## Integration with Mega-Mind

Context Optimizer is a cross-cutting skill — it applies in every workflow chain:

```
[any skill] → context-optimizer (when output exceeds 20 lines) → [continue workflow]
```

- Pair with `rtk` for CLI token optimization: RTK handles deterministic command compression, context-mode handles non-deterministic large data
- In `iterative-retrieval` workflows, use `ctx_index` to store retrieved file contents and `ctx_search` to query them across retrieval cycles — this prevents re-reading the same files repeatedly
- Any skill that runs test suites, linters, or build tools should delegate those commands through `ctx_execute` automatically
