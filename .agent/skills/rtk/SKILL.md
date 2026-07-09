---
name: rtk
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  RTK (Rust Token Killer) CLI proxy that reduces LLM token consumption by 60-90% on common development commands.
  Use to optimize CLI operations and track token savings — always prefer RTK-wrapped commands when RTK is installed.
  Covers git, cargo, npm/pnpm/bun, pytest, go, and common utilities with measured savings statistics per command.
category: token-optimization
triggers:
  - "rtk"
  - "token optimization"
  - "save tokens"
  - "optimize output"
  - "reduce tokens"
  - "compact output"
  - "cli optimization"
  - "rtk gain"
dependencies:
  - verification-loop: recommended
  - executing-plans: recommended
  - context-optimizer: recommended
---

# RTK (Rust Token Killer) Skill

## Identity

You are a token optimization specialist. RTK is a high-performance CLI proxy that minimizes LLM token consumption by filtering and compressing command outputs. You always prefer RTK-wrapped commands when RTK is installed, and fall back gracefully when it is not.

**Your core responsibility:** Minimize LLM token consumption by routing CLI commands through RTK for 60-90% output compression.

**Your operating principle:** Always prefer RTK when installed; fall back gracefully when unavailable; never fail or stall waiting for RTK.

**Your quality bar:** All supported CLI operations use RTK-wrapped equivalents, `rtk gain` shows measurable token savings for the session, and fallback to raw commands is seamless when RTK is unavailable — no exceptions.

## When to Use

- **Before running verbose commands:** `git log`, `cargo test`, `npm install`
- **When context window is limited:** Large projects with many files
- **For cost optimization:** Reduce token usage per session
- **For build/test output:** Only show failures, not full output

## When NOT to Use

- When RTK is not installed — fall back gracefully to raw commands; do not fail or stall waiting for RTK
- When verbose output is explicitly needed for debugging — use the raw command directly
- For commands where RTK's output compression would hide information needed for the current task
- For `git commit`, `git push`, or other write commands where you need to confirm the exact output

## Core Principles

1. **Prefer RTK for verbose commands.** Always wrap git, cargo, npm, pytest in RTK when installed.
2. **Fall back gracefully.** If RTK is not installed, use raw commands. Never block on RTK being unavailable.
3. **Check savings periodically.** Use `rtk gain` to see cumulative impact and verify RTK is active.
4. **Use proxy for unsupported commands.** `rtk proxy <cmd>` still tracks usage even without filtering.

---

## Command Reference

### Git Operations (70-85% savings)
```bash
rtk git status
rtk git log -10
rtk git diff
```

### Rust/Cargo (80-90% savings)
```bash
rtk cargo test
rtk cargo build
rtk cargo clippy
```

### Node.js/TypeScript (80-99% savings)
```bash
rtk npm test
rtk tsc
rtk lint
```

### Python (80-90% savings)
```bash
rtk pytest
rtk ruff check
rtk mypy src/
```

### Go (75-90% savings)
```bash
rtk go test ./...
rtk go build ./...
rtk golangci-lint run
```

### Utilities (50-70% savings)
```bash
rtk ls -la
rtk read <file>
rtk grep <pattern> <path>
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Calling raw command when RTK-wrapped equivalent exists | Missed token savings of 60-90%; unnecessary context pressure | Check RTK availability first, then use RTK wrapper |
| Failing or stalling when RTK not installed | Blocks workflow for missing optional tool | Check `rtk --version` first; fall back to raw command |
| Using RTK on command with <200 token output | Compression overhead exceeds benefit | Skip RTK for tiny outputs; use raw command |
| Not checking `rtk gain` to verify savings | Cannot measure impact; RTK may not be filtering effectively | Periodically run `rtk gain` to verify savings |

## Verification

### Self-Verification Checklist

- [ ] RTK installed and `rtk --version` exits 0
- [ ] Token count after compression is lower than before (verified via `rtk gain`)
- [ ] Compressed output is syntactically valid (key fields present)
- [ ] All supported CLI operations use RTK-wrapped equivalents
- [ ] Fallback to raw commands in place when RTK unavailable
- [ ] Verbose debugging commands use raw CLI (not RTK)

### Verification Commands

```bash
# Check installation
rtk --version

# Check cumulative savings
rtk gain
rtk gain --history

# Verify compression quality
rtk git log --oneline -5
# Confirm output is readable and complete for the task
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Installation | `rtk --version` exits 0 | Fall back to raw commands |
| Savings | `rtk gain` shows tokens saved > 0 | Verify RTK is being invoked correctly |
| Fallback | Raw commands work when RTK unavailable | Ensure no hard dependency on RTK |
| Output Quality | Compressed output contains needed fields | Use raw command for missing details |

## Examples

### Example 1: Git Log Optimization

**User request:** "Show me the last 50 commits."

**Skill execution:**
1. Without RTK: `git log -50` produces ~3,500 tokens of full commit messages
2. With RTK: `rtk git log -50` produces ~500 tokens (summary format)
3. Key fields preserved: commit hash, author, date, subject
4. Verification: `rtk gain` shows 85% token savings

**Result:** 85% token reduction. All needed information (hashes, authors, dates) preserved.

### Example 2: Edge Case - RTK Not Installed

**User request:** "Run tests and show results."

**Skill execution:**
1. Check `rtk --version`: exits non-zero (not installed)
2. Fall back to `npm test` directly
3. Output is full-verbosity (no compression)
4. Proceed without blocking — RTK is an optimization, not a requirement

**Result:** Workflow continues seamlessly. No delay from missing optional tool.

## Anti-Patterns

- Never call a raw command when an RTK-wrapped equivalent exists because you miss 60-90% token savings and put unnecessary pressure on the context window with verbose output that RTK would have compressed.
- Never fail or stall when RTK is not installed because RTK is an optional optimization, not a hard dependency; check availability with `rtk --version` and fall back gracefully to raw commands.
- Never use RTK on commands producing less than ~200 tokens of output because the RTK wrapper overhead exceeds the savings, and the raw output fits trivially in context.
- Never skip running `rtk gain` periodically to verify savings because without measurement you cannot confirm RTK is active, correctly configured, and actually filtering output.

## Performance & Cost

### Savings by Command Type

| Command | Raw Tokens | RTK Tokens | Savings |
|---|---|---|---|
| `git log -50` | ~3,500 | ~500 | 85% |
| `cargo test` | ~8,000 | ~800 | 90% |
| `npm test` | ~5,000 | ~500 | 90% |
| `pytest` | ~6,000 | ~600 | 90% |
| `go test ./...` | ~4,000 | ~600 | 85% |
| `ls -la` (large dir) | ~500 | ~150 | 70% |

### Installation Cost

- **Binary size:** ~5MB on disk
- **Install time:** <10 seconds via cargo install or prebuilt binary
- **CPU overhead:** <2ms per wrapped command
- **Expected context usage:** negligible (~200 bytes for `rtk gain` check)

## References

### Internal Dependencies
- `verification-loop` — Uses RTK for all verification commands
- `executing-plans` — Uses RTK when running plan steps
- `context-optimizer` — Pair with RTK for full token optimization strategy

### External Standards
- [RTK Repository](https://github.com/rtk-ai/rtk) — Official RTK project

### Related Skills
- `context-optimizer` — RTK handles deterministic CLI compression; context-mode handles non-deterministic large data
- `verification-loop` — RTK used throughout verification phases

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, References, Changelog. |
---
