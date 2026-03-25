---
name: strategic-compact
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Context window management via strategic compaction at logical task boundaries. Use when approaching context limits during long sessions, or when switching between major task phases.
triggers:
  - "context limit"
  - "compact"
  - "compaction"
  - "context pressure"
  - "context overflow"
  - "long session"
  - "switch task phase"
  - "context management"
---

# Strategic Compact Skill

## Identity

You are a context management specialist. You know that auto-compaction at arbitrary points loses critical state. Strategic compaction at logical phase boundaries — with intention — preserves what matters and clears what doesn't.

## When to Activate

- Running long sessions that approach context limits (200K+ tokens)
- Switching between major task phases (research → planning → implementation → testing)
- After completing a major milestone before starting new work
- When your responses start feeling less focused or coherent (context pressure signal)
- After a failed approach — clear the dead-end reasoning before retrying

---

## Why Strategic Compaction?

**Auto-compaction fires at arbitrary points:**

- Often mid-task, losing important variable names and file paths
- No awareness of logical task boundaries
- Can interrupt complex multi-step operations

**Strategic compaction at logical boundaries:**

- After exploration → Compact research, keep the plan
- After a milestone → Fresh start for next phase
- After a failed approach → Clear dead-end reasoning before new try

---

## Compaction Decision Guide

Use this table to decide WHEN to compact:

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

---

## What Survives Compaction

Understanding what persists helps you compact with confidence:

| Persists After Compact                 | Lost After Compact                  |
| -------------------------------------- | ----------------------------------- |
| `AGENTS.md` / `CLAUDE.md` instructions | Intermediate reasoning and analysis |
| Task tracker (`docs/plans/task.md`)    | File contents you previously read   |
| Memory files (if using claude memory)  | Multi-step conversation context     |
| Git state (commits, branches, files)   | Tool call history and counts        |
| All files on disk                      | Nuanced preferences stated verbally |

---

## Protocol: Compact with Intention

### Before Compacting

1. **Save important context to files** — anything you'll need after compaction:

   ```bash
   # Write a session summary to disk
   cat > docs/plans/session-notes.md << 'EOF'
   ## Session Notes — [date]

   ### What was done
   - [key decisions made]
   - [files changed]

   ### What's next
   - [immediate next step]
   - [dependencies to check]

   ### Important discoveries
   - [codebase uses "throttle" not "rate-limit"]
   - [auth module is in lib/auth/, not src/]
   EOF
   ```

2. **Update task tracker** — `docs/plans/task.md` must be current before compacting

3. **Commit work in progress** if at a stable point (optional but recommended)

### Compacting

```
/compact Focus on implementing [next phase]. Context: [key facts to carry forward]
```

The custom message is critical — it tells the AI what matters after compaction.

### After Compacting

1. Read `docs/plans/task.md` to restore session state
2. Read `docs/plans/session-notes.md` if you wrote one
3. Continue from exactly where the notes say to continue

---

## Token Optimization Patterns

### Trigger-Table Lazy Loading

Instead of loading all skills at session start, skills should load only when triggered:

| Trigger                   | Skill                   | Load When          |
| ------------------------- | ----------------------- | ------------------ |
| "test", "tdd", "coverage" | test-driven-development | Testing context    |
| "security", "auth", "xss" | security-reviewer       | Security work      |
| "deploy", "ci/cd"         | deployment-patterns     | Deployment context |
| "migrate", "schema"       | database-migrations     | DB work            |

This is why skill triggers in SKILL.md frontmatter are important — they enable lazy loading.

### Context Composition Awareness

Monitor what consumes context:

- **AGENTS.md / CLAUDE.md** — always loaded; keep them lean and focused
- **Loaded skills** — each skill adds 1–5K tokens
- **Conversation history** — grows with every exchange
- **Tool results** — file reads, search results, terminal output all add bulk

### Reduce Bulk Before It Grows

```bash
# Prefer RTK-wrapped commands (60-90% smaller output)
rtk git diff       # vs `git diff` (full output)
rtk bun test (or npm test)       # vs `bun test (or npm test)` (concise summary)
rtk ls src/        # vs `ls -la src/` (trimmed listing)
```

---

## Context Compaction Signals

Watch for these signs that context pressure is building:

- Responses become repetitive or miss earlier context
- You're re-reading files you already read earlier in the session
- The session has run >100 tool calls
- You've finished a major phase (research, planning, a full feature)
- You're about to start something completely different

---

## Example: Research → Implementation Transition

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
           Install: `bun install (or npm install) better-auth`
           Config goes in: lib/auth/config.ts
           Key docs: https://better-auth.com/docs/setup

Step 4: After compaction
  AI reads task.md and auth-library-choice.md → resumes cleanly
```

---

## Tips

- **Write before compacting** — anything not on disk is lost
- **The compact message is your bridge** — be specific about what to focus on next
- **Don't compact mid-implementation** — finish the current function/component first
- **Compact after debugging resolved** — clear error context before continuing with features
- **Use `/compact` not auto-compact** — strategic > automatic; you know the logical boundaries
