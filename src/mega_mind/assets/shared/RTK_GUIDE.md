# RTK (Rust Token Killer) Usage Guide

> Shared snippet referenced by all skills that run CLI commands.

## Rule

**You MUST use RTK-wrapped commands for all supported CLI operations if RTK is installed.**

Usage: `rtk <command>` (e.g., `rtk bun test`, `rtk npm test`, `rtk git status`, `rtk tsc`).

## Common Mappings

| Original Command                | RTK Command                     | Typical Savings |
| ------------------------------- | ------------------------------- | --------------- |
| `git log`                       | `rtk git log`                   | 85%             |
| `git status`                    | `rtk git status`                | 70%             |
| `git diff`                      | `rtk git diff`                  | 80%             |
| `npm test` / `bun test`         | `rtk npm test` / `rtk bun test` | 90%             |
| `pytest`                        | `rtk pytest`                    | 90%             |
| `cargo test`                    | `rtk cargo test`                | 90%             |
| `tsc --noEmit`                  | `rtk tsc`                       | 83%             |
| `npm run lint` / `bun run lint` | `rtk lint`                      | 84%             |
| `ls`                            | `rtk ls`                        | 60%             |
| `grep`                          | `rtk grep`                      | 70%             |

## RTK Proxy (for compound commands)

For commands that RTK doesn't directly wrap, use `rtk proxy`:

```bash
rtk proxy bun run build
rtk proxy npm run test:integration
```

## Monitoring Savings

Run `rtk gain` periodically to check cumulative token savings for the session.

## When NOT to Use RTK

- When you need the full, unfiltered output for debugging
- When piping output to another tool that needs the raw format
- For interactive commands that require user input

## Fallback Protocol (When RTK is NOT Installed)

If `rtk` is not installed or produces an error, fall back to the bare command:

```bash
# Detect if RTK is available
rtk --version 2>/dev/null || RTK_AVAILABLE=false

# If RTK_AVAILABLE is false, use bare commands directly:
bun test          # Instead of rtk bun test
tsc --noEmit      # Instead of rtk tsc
git status        # Instead of rtk git status
```

**Rule**: Before running any RTK-wrapped command, check availability. If RTK is absent, run the equivalent bare command with the same flags. Document in task.md when RTK was unavailable so the session can install it later.
