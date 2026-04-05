---
name: rtk
compatibility: Antigravity, Claude Code, GitHub Copilot
description: |
  RTK (Rust Token Killer) is a CLI proxy that reduces LLM token consumption by 60-90%
  on common development commands. Use this skill to optimize CLI operations and track
  token savings. Always prefer RTK-wrapped commands when RTK is installed.
triggers:
  - "rtk"
  - "token optimization"
  - "save tokens"
  - "optimize output"
  - "reduce tokens"
  - "compact output"
  - "cli optimization"
---

# RTK (Rust Token Killer) Skill

## Overview

RTK is a high-performance CLI proxy that minimizes LLM token consumption by filtering and compressing command outputs. It achieves **60-90% token savings** on common development operations.

## When to Use

- **Before running verbose commands**: `git log`, `cargo test`, `bun install (or npm install)`
- **When context window is limited**: Large projects with many files
- **For cost optimization**: Reduce token usage per session
- **For build/test output**: Only show failures, not full output

## When NOT to Use

- When RTK is not installed — fall back gracefully to raw commands; do not fail or stall waiting for RTK
- When verbose output is explicitly needed for debugging (e.g., investigating a specific build warning) — use the raw command directly
- For commands where RTK's output compression would hide information needed for the current task
- For `git commit`, `git push`, or other write commands where you need to confirm the exact output

## Quick Check: Is RTK Installed?

```bash
rtk --version    # Should show version like "rtk 0.27.2"
rtk gain         # Should show token savings stats
```

If these fail, RTK is not installed. Use standard commands instead.

## Command Reference

### Git Operations

```bash
# Status (70% savings)
rtk git status
rtk git status --short

# Log (85% savings)
rtk git log -10
rtk git log --oneline -20
rtk git log --graph --oneline --all

# Diff (80% savings)
rtk git diff
rtk git diff --cached
rtk git diff main..feature

# Branch (60% savings)
rtk git branch
rtk git branch -a
```

### Rust / Cargo

```bash
# Test (90% savings - failures only)
rtk cargo test
rtk cargo test --lib
rtk cargo test <test_name>

# Build (80% savings - errors/warnings only)
rtk cargo build
rtk cargo build --release

# Check (compact output)
rtk cargo check
rtk cargo check --all-targets

# Clippy (85% savings - grouped by severity)
rtk cargo clippy
rtk cargo clippy --all-targets
```

### Node.js / JavaScript / TypeScript

```bash
# Test runners
rtk bun test (or rtk npm test)          # Generic bun test (or npm test)
rtk vitest            # Vitest (99.5% savings)

# Linting (84% savings)
rtk lint              # ESLint/Biome
rtk eslint src/

# TypeScript (83% savings)
rtk tsc               # TypeScript compiler
rtk npx tsc --noEmit

# Frameworks
rtk next              # Next.js (87% savings)
rtk playwright        # E2E tests (94% savings)
```

### Python

```bash
# Linting/Formatting
rtk ruff check        # Ruff linter (80% savings)
rtk ruff format       # Ruff formatter

# Type checking (80% savings)
rtk mypy src/

# Testing (90% savings)
rtk pytest
rtk pytest tests/

# Package management
rtk pip list          # pip/uv (70-85% savings)
```

### Go

```bash
# Testing (90% savings)
rtk go test ./...
rtk go test -v ./...

# Build (80% savings)
rtk go build ./...

# Vet (75% savings)
rtk go vet ./...

# Linting (85% savings)
rtk golangci-lint run
```

### Package Managers

```bash
# pnpm (70-90% savings)
rtk pnpm list
rtk pnpm outdated
rtk pnpm install (or rtk npm install)

# npm
rtk npm list
rtk npm outdated

# pip
rtk pip list
rtk pip outdated
```

### Database / ORM

```bash
# Prisma (88% savings)
rtk prisma migrate status
rtk prisma db push
rtk prisma studio
```

### Utilities

```bash
# Directory listing
rtk ls                # Tree format with counts
rtk ls -la            # Detailed listing

# File reading (with filtering)
rtk read <file>       # Smart file reading
rtk read --filter=aggressive <file>

# Search
rtk grep <pattern> <path>    # Grouped by file

# JSON inspection
rtk json <file>       # Structure without values

# Optimization Flags (NEW in v0.27+)
rtk --ultra-compact <cmd>   # Inline format with ASCII icons (Level 2)
rtk --skip-env <cmd>        # Set SKIP_ENV_VALIDATION=1 for child processes
```

## Token Savings Statistics

```bash
# View cumulative savings
rtk gain

# View command history
rtk gain --history

# Example output:
# ╭──────────────────────────────────────────────╮
# │ Total commands: 127                          │
# │ Tokens saved: 89,432                         │
# │ Average savings: 78.3%                       │
# │ Cost saved: $1.79                            │
# ╰──────────────────────────────────────────────╯
```

## Proxy Mode

For commands not specifically supported by RTK, use proxy mode:

```bash
# Still tracks usage, just no filtering
rtk proxy <any-command> <args>

# Examples
rtk proxy docker ps
rtk proxy kubectl get pods
rtk proxy curl https://api.example.com
```

## Tool Translation Table

When RTK is installed, translate commands automatically:

| Original                         | RTK-Optimized                | Savings |
| -------------------------------- | ---------------------------- | ------- |
| `git status`                     | `rtk git status`             | 70%     |
| `git log -10`                    | `rtk git log -10`            | 85%     |
| `git diff`                       | `rtk git diff`               | 80%     |
| `cargo test`                     | `rtk cargo test`             | 90%     |
| `cargo build`                    | `rtk cargo build`            | 80%     |
| `cargo clippy`                   | `rtk cargo clippy`           | 85%     |
| `bun test (or npm test)`         | `rtk bun test (or npm test)` | 90%     |
| `bun run lint (or npm run lint)` | `rtk lint`                   | 84%     |
| `npx tsc --noEmit`               | `rtk tsc`                    | 83%     |
| `pytest`                         | `rtk pytest`                 | 90%     |
| `go test ./...`                  | `rtk go test`                | 90%     |
| `pnpm list`                      | `rtk pnpm list`              | 70-90%  |
| `ls -la`                         | `rtk ls`                     | 60%     |
| `cat <file>`                     | `rtk read <file>`            | 50-70%  |

## Integration with Mega-Mind

## Anti-Patterns

- Never mutate state outside of a createSlice reducer because mutations outside reducers bypass Immer's change tracking, producing state updates that the Redux DevTools cannot record and that time-travel debugging cannot replay.
- Never put non-serializable values in Redux state because non-serializable values (Date objects, class instances, functions) cannot be persisted, replayed, or compared with strict equality, causing silent failures in selectors and middleware.
- Never use useSelector with a new object or array literal in the selector function because a selector that returns a new reference on every call causes the component to re-render on every dispatch, regardless of whether the relevant data changed.
- Never dispatch an action that triggers another dispatch synchronously because synchronous chained dispatches bypass the middleware pipeline for the inner dispatch and create action ordering that is impossible to reproduce in tests.
- Never store derived data in Redux state when it can be computed from existing state because redundant derived state goes out of sync with its source, requiring manual synchronisation logic that is consistently forgotten or incorrectly implemented.
- Never use RTK Query with a baseUrl that differs between environments without configuration because a hardcoded baseUrl causes all API calls to target the wrong environment in staging or production, making the bug invisible until deployment.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Token savings not achieved because context was already small | RTK applied to a command that outputs fewer than 200 tokens; compression overhead exceeds benefit | Skip RTK for small-output commands; use `rtk gain` to identify which command types are actually saving tokens in this project |
| RTK not installed in environment, command fails silently | `rtk` binary not on PATH; CI or remote environment missing the install step | Check `rtk --version` exits 0 before wrapping any command; fall back to raw command if check fails; add RTK install to CI setup step |
| Command output truncated unexpectedly, leaving partial context | RTK's output filter aggressively drops lines that match a suppression rule; needed information removed | Re-run the raw command without RTK to see full output; file an issue or adjust RTK filter config; for debugging sessions use raw commands |
| RTK applied to wrong file, compressing irrelevant content | `rtk read <file>` called on a binary or auto-generated file; output is noise | Verify the target file path with `ls` before reading; only use `rtk read` on human-readable source or config files |

### When to Suggest RTK

1. **User asks to run a command** → Check if RTK version exists
2. **Output seems verbose** → Suggest using RTK next time
3. **Context window is filling** → Remind about RTK savings

### Example Interaction

```
User: Run git log to see recent commits

AI: Running optimized command with RTK:
    $ rtk git log --oneline -10

    a1b2c3d feat: add user authentication
    e4f5g6h fix: resolve session timeout
    ...

    💡 Token savings: 87% (used 234 tokens vs 1,800 raw)
    💰 Run `rtk gain` to see cumulative savings
```

## Fallback Behavior

If RTK is not installed or fails:

```
1. Try RTK command
2. If fails → Execute raw command
3. Log that RTK would have saved tokens
4. Continue normally
```

The system gracefully degrades without breaking functionality.

## Configuration

### RTK Config File

Location: `~/.config/rtk/config.toml`

```toml
[tracking]
# Custom database location (optional)
database_path = "~/.local/share/rtk/tracking.db"

[tee]
# Save full output on failure
enabled = true
directory = "~/.local/share/rtk/tee"
max_files = 20
max_size_mb = 1
```

### Environment Variables

```bash
RTK_DB_PATH=/custom/path/tracking.db
RTK_TEE=true
RTK_TEE_DIR=/custom/tee
```

## Best Practices

1. **Prefer RTK for verbose commands**: Always wrap git, cargo, npm, pytest
2. **Check savings periodically**: `rtk gain` to see impact
3. **Use proxy for unsupported commands**: Still tracks usage
4. **Combine with other skills**: Use RTK within TDD, debugging, and review workflows

## Common Issues

### RTK Not Found

```bash
# Install RTK
cargo install rtk

# Or download binary
curl -sSL https://github.com/rtk-ai/rtk/releases/latest/download/rtk-$(uname -s)-$(uname -m) -o /usr/local/bin/rtk
chmod +x /usr/local/bin/rtk
```

### Wrong Package Installed

There are two "rtk" packages:

- ✅ **rtk-ai/rtk** (Rust Token Killer) - This is what we want
- ❌ **reachingforthejack/rtk** (Rust Type Kit) - Different project

Verify: `rtk gain` should show token savings, not "command not found"

### Command Not Supported

Use proxy mode:

```bash
rtk proxy <unsupported-command>
```

## Related Skills

- `executing-plans` - Use RTK when running plan steps
- `test-driven-development` - Use `rtk cargo test` / `rtk bun test` (or `rtk npm test`)
- `systematic-debugging` - Use `rtk git diff` for changes
- `verification-before-completion` - Use RTK for verification commands

## Self-Verification Checklist

- [ ] RTK installed and `rtk --version` exits 0 — verified before using any RTK-wrapped commands
- [ ] Token count after compression is lower than before — `rtk gain` shows cumulative tokens saved > 0 for this session
- [ ] Compressed output is syntactically valid — key fields (test names, error messages, file paths) are present and parseable in the RTK output
- [ ] All supported CLI operations use RTK-wrapped equivalents (`rtk git status`, `rtk bun test`, etc.)
- [ ] Fallback to raw commands is in place when RTK is unavailable (no hard dependency)
- [ ] Verbose debugging commands use raw CLI (not RTK) when full output is needed

## Success Criteria

This skill is complete when: 1) all supported CLI commands in the current session use RTK-wrapped equivalents, 2) `rtk gain` shows measurable token savings, and 3) there is a documented fallback for environments where RTK is not installed.
