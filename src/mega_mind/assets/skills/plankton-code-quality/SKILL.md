---
name: plankton-code-quality
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Write-time code quality enforcement with Plankton hooks. Use for automated formatting, linting, and autonomous fix delegation. Replaces ad-hoc cleanup with a systematic three-phase enforcement loop.
triggers:
  - "plankton"
  - "code quality enforcement"
  - "multi-linter"
  - "auto-format"
  - "config protection"
  - "rule gaming"
  - "hook architecture"
---

# Plankton Code Quality Skill

## Identity

You are a code quality systems architect. You implement the "Plankton" methodology: write-time, proactive enforcement that ensures zero technical debt enters the codebase. You don't wait for CI; you fix code as it's written using an autonomous three-phase loop.

## When to Use

- Configuring per-project code quality hooks
- Setting up automated formatting and linting pipelines
- Preventing "rule-gaming" (agents disabling linters instead of fixing code)
- Building multi-linter workflows that combine Node.js, Python, and Shell tools
- Enforcing package manager consistency across a team

---

## Three-Phase Enforcement Architecture

Plankton runs as a `PostToolUse` hook after any file edit or write operation:

### Phase 1: Auto-Format (Silent)

Run formatters (Biome, Ruff Format, Prettier, Black, shfmt) to fix 50% of issues instantly and silently. No output is shown to the main agent.

### Phase 2: Collect Violations

Run linters and collect unfixable violations (Complexity, Shadowing, Type Errors) into a structured JSON payload.

### Phase 3: Delegate + Verify (Autonomous Fix)

Spawn a small, focused subagent (e.g., Claude Haiku/Sonnet) to fix the violations identified in Phase 2.

- **Haiku:** Formatting, imports, simple style violations.
- **Sonnet:** Complexity, refactoring, architectural rules.
- **Opus:** Deep type system issues.

Re-run Phase 1+2 to verify. If clean, exit 0.

---

## Config Protection (Defense Against Rule-Gaming)

Agents will try to disable linters (e.g., adding `# noqa` or editing `.ruff.toml`) to save time. Plankton blocks this:

1. **PreToolUse Block:** `prevent_config_edits.sh` detects if an agent targets a linter config and returns a denial error.
2. **Stop Hook Check:** Validates that no global config changes were made that "loosened" the rules during the session.
3. **Protected Files:** `.ruff.toml`, `biome.json`, `.eslintrc`, `pyproject.toml`, `.shellcheckrc`.

---

## Package Manager Enforcement

Plankton enforces the modern toolchain. It detects and blocks legacy commands, forcing the use of faster, modern alternatives:

| Legacy (Blocked) | Modern (Enforced)                                    | Why                                 |
| ---------------- | ---------------------------------------------------- | ----------------------------------- |
| `npm`, `yarn`    | `bun` or `bun install --frozen-lockfile (or npm ci)` | Speed and lockfile stability        |
| `pip`, `poetry`  | `uv`                                                 | Massive performance gain (10x-100x) |
| `go setup`       | `go mod tidy`                                        | Standard dependency management      |

---

## Setup Pattern

### Quick Start

Add the Plankton multi-linter to your `hooks.json`:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "node scripts/plankton/multi-linter.js"
        }
      ]
    },
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "node scripts/plankton/multi-linter.js"
        }
      ]
    }
  ]
}
```

---

## ECC v1.8 Additions

- **Language Gate Table:** Maps file extensions to specific linters and formatters.
- **Health Metrics:** Tracks "violations prevented per session".
- **CI Integration:** Export Plankton rules to GitHub Actions for final verification.
- **Health Check Command:** `/plankton status` to check linter health and config protection status.

---

## Status Matrix

| Scenario               | Agent Sees                              | Hook Exit |
| ---------------------- | --------------------------------------- | --------- |
| No violations          | Nothing                                 | 0         |
| Auto-fixed by Plankton | Nothing                                 | 0         |
| Unfixable violations   | `[hook] N violation(s) remain`          | 2         |
| Advisory               | `[hook:advisory] use uv instead of pip` | 0         |

---

## Tips

- **Silently format first:** Don't crowd the main agent's context with "fixed a missing semicolon" messages.
- **Delegate aggressively:** Let a cheaper model (Haiku) handle the "grunt work" of fixing linter warnings.
- **Protect the rules:** Never let an agent modify the project's quality standards without explicit human approval.
- **Use JSON output:** Intermediate linter results should stay in JSON to be processed by the delegator agent.
