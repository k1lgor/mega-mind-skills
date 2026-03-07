---
name: rtk
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

- **Before running verbose commands**: `git log`, `cargo test`, `npm install`
- **When context window is limited**: Large projects with many files
- **For cost optimization**: Reduce token usage per session
- **For build/test output**: Only show failures, not full output

## Quick Check: Is RTK Installed?

```bash
rtk --version    # Should show version like "rtk 0.27.1"
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
rtk npm test          # Generic npm test
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
rtk pnpm install

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

| Original           | RTK-Optimized      | Savings |
| ------------------ | ------------------ | ------- |
| `git status`       | `rtk git status`   | 70%     |
| `git log -10`      | `rtk git log -10`  | 85%     |
| `git diff`         | `rtk git diff`     | 80%     |
| `cargo test`       | `rtk cargo test`   | 90%     |
| `cargo build`      | `rtk cargo build`  | 80%     |
| `cargo clippy`     | `rtk cargo clippy` | 85%     |
| `npm test`         | `rtk npm test`     | 90%     |
| `npm run lint`     | `rtk lint`         | 84%     |
| `npx tsc --noEmit` | `rtk tsc`          | 83%     |
| `pytest`           | `rtk pytest`       | 90%     |
| `go test ./...`    | `rtk go test`      | 90%     |
| `pnpm list`        | `rtk pnpm list`    | 70-90%  |
| `ls -la`           | `rtk ls`           | 60%     |
| `cat <file>`       | `rtk read <file>`  | 50-70%  |

## Integration with Mega-Mind

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
- `test-driven-development` - Use `rtk cargo test` / `rtk npm test`
- `systematic-debugging` - Use `rtk git diff` for changes
- `verification-before-completion` - Use RTK for verification commands
