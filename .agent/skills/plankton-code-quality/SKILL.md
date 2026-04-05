---
name: plankton-code-quality
compatibility: Antigravity, Claude Code, GitHub Copilot, OpenCode, Cursor
description: Write-time code quality enforcement using the Plankton methodology — a three-phase PostToolUse hook pipeline that auto-formats, collects lint violations, and autonomously delegates fixes to a subagent. Enforces a zero-tolerance policy on linter rule suppression and config weakening, replacing ad-hoc cleanup with systematic, measurable quality gates. Use this skill whenever setting up or operating automated code quality enforcement on a project.
triggers:
  - "plankton"
  - "code quality enforcement"
  - "multi-linter"
  - "auto-format"
  - "config protection"
  - "rule gaming"
  - "hook architecture"
  - "linting hooks"
  - "violation budget"
  - "pre-commit quality"
---

# Plankton Code Quality Skill

## Identity

You are a code quality systems architect specializing in proactive, write-time enforcement. You implement the "Plankton" methodology: a PostToolUse hook that runs immediately after every file write or edit, catching and fixing quality violations before they accumulate into technical debt. You treat linter configurations as immutable contracts — no agent, human or AI, may weaken them without explicit human approval. You measure success by the violation count trending toward zero over a session, not by CI passing after the fact. You understand that AI agents will attempt to game quality rules (adding `# noqa`, editing config files, disabling rules inline) and you close every one of those escape hatches. You are the last line of defense before bad code enters the codebase.

## When to Activate

- Configuring per-project code quality hooks for a new or existing project
- Setting up automated formatting and linting pipelines that run on every file save
- Detecting that an agent has disabled, weakened, or worked around linter rules
- Building multi-linter workflows that span TypeScript, Python, Shell, Go, or other languages in a monorepo
- Enforcing package manager consistency (blocking `npm`/`pip` in favor of `bun`/`uv`)
- Integrating Plankton output into CI pipelines (GitHub Actions, GitLab CI)
- Auditing whether quality enforcement is actually running (`/plankton status`)
- Establishing a "violation budget" baseline and tracking improvement over time

## When NOT to Use

- On projects with no linter configuration at all — set up linters first (biome.json, ruff.toml, .shellcheckrc) before activating Plankton; running it on an unconfigured project produces noise without signal
- For one-off exploratory scripts or throwaway prototypes where quality overhead exceeds value
- When the task is specifically to migrate FROM one linter to another — disable Plankton during the migration, re-enable afterward
- For generated code files (protobuf outputs, OpenAPI clients, build artifacts) — add these to `.planktonignore`
- Do not use this skill to evaluate whether a project needs linting — use `code-polisher` for that audit first

---

## Core Principles

1. **Shift left, not right.** Violations caught at write time cost 1x to fix. Violations caught in CI cost 10x. Violations in production cost 100x. Plankton enforces at the earliest possible moment.
2. **Silent success, loud failure.** Phase 1 (formatting) runs silently. The main agent's context is not polluted with "fixed a semicolon" messages. Only unfixable violations surface.
3. **Never suppress, always fix.** `# noqa`, `// eslint-disable`, `# type: ignore` — all are forbidden without a pre-approved exception comment. The correct response to a violation is to fix the underlying issue.
4. **Config files are sacred.** Linter configuration files are protected by PreToolUse hooks. Agents cannot weaken rules to make violations disappear. Any attempted config edit triggers an immediate denial.
5. **Delegate cheaply.** Phase 3 fixes use the cheapest viable model (Haiku for style, Sonnet for complexity). Never route lint fixes through Opus.
6. **Measure the violation budget.** Track violations per session. A well-functioning project has a declining violation count. A flat or rising count means the hooks are being bypassed.
7. **Fail on exit code, not silence.** Hooks that exit 2 block the agent from proceeding. Hooks that exit 0 with a warning are advisory only. The distinction must be explicit in the hook config.

---

## Three-Phase Enforcement Architecture

Plankton runs as a `PostToolUse` hook after any `Edit` or `Write` operation:

```
┌─────────────────────────────────────────────────────────────┐
│              PostToolUse: Edit / Write                      │
│                                                             │
│  Phase 1: AUTO-FORMAT (silent)                              │
│    biome format --write / ruff format / shfmt -w            │
│    → Fixes ~50% of violations silently. No context output.  │
│                                                             │
│  Phase 2: COLLECT VIOLATIONS                                │
│    biome lint / ruff check / shellcheck / tsc --noEmit      │
│    → Outputs structured JSON: { file, line, rule, message } │
│                                                             │
│  Phase 3: DELEGATE + VERIFY                                 │
│    Spawn subagent with violation JSON payload               │
│    → Haiku: style / imports / simple rules                  │
│    → Sonnet: complexity / refactoring / type errors         │
│    Re-run Phase 1+2 to verify. Exit 0 if clean.             │
│    Exit 2 if violations remain after fix attempt.           │
└─────────────────────────────────────────────────────────────┘
```

---

## Language Gate Table

Every file extension routes to a specific linter/formatter pair. If a tool is not installed, the gate is skipped with a warning (exit 0 advisory), never a hard failure.

| Extension          | Formatter          | Linter              | Installed Check                 |
| ------------------ | ------------------ | ------------------- | ------------------------------- |
| `.ts`, `.tsx`      | `biome format`     | `biome lint`        | `which biome`                   |
| `.js`, `.jsx`      | `biome format`     | `biome lint`        | `which biome`                   |
| `.py`              | `ruff format`      | `ruff check`        | `which ruff`                    |
| `.sh`, `.bash`     | `shfmt -w`         | `shellcheck`        | `which shfmt && which shellcheck` |
| `.go`              | `gofmt -w`         | `go vet ./...`      | `which gofmt`                   |
| `.rs`              | `rustfmt`          | `cargo clippy`      | `which rustfmt`                 |
| `.sql`             | `sqlfluff format`  | `sqlfluff lint`     | `which sqlfluff`                |
| `.yaml`, `.yml`    | `prettier --write` | `yamllint`          | `which yamllint`                |
| `.json`            | `biome format`     | `biome lint`        | `which biome`                   |
| `.md`              | `prettier --write` | `markdownlint`      | `which markdownlint`            |

**Decision logic (pseudocode):**

```javascript
// multi-linter.js — Phase 1 + Phase 2 entrypoint
const changedFile = process.env.TOOL_OUTPUT_FILE; // injected by hook runtime

const ext = path.extname(changedFile);
const gate = LANGUAGE_GATE[ext];

if (!gate) {
  process.exit(0); // unknown extension — skip silently
}

const toolInstalled = await checkInstalled(gate.formatterCheck);
if (!toolInstalled) {
  console.error(`[plankton:advisory] ${gate.formatter} not installed, skipping ${ext}`);
  process.exit(0); // advisory only — do not block
}

// Phase 1: format silently
await exec(gate.formatCmd, changedFile);

// Phase 2: collect violations
const violations = await collectViolations(gate.lintCmd, changedFile);

if (violations.length === 0) {
  process.exit(0); // clean
}

// Phase 3: serialize and delegate
const payload = JSON.stringify({ file: changedFile, violations });
await delegateToSubagent(payload);
```

---

## Hook Configuration Examples

### OpenCode / Claude Code (`hooks.json`)

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
  ],
  "PreToolUse": [
    {
      "matcher": "Edit",
      "hooks": [
        {
          "type": "command",
          "command": "node scripts/plankton/prevent_config_edits.js"
        }
      ]
    }
  ]
}
```

### GitHub Copilot (`.github/copilot-config.json` — custom hooks)

```json
{
  "on_file_save": {
    "command": "node scripts/plankton/multi-linter.js",
    "fail_on_exit_code": [2]
  }
}
```

### Claude Code Standalone (`.claude/settings.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "node scripts/plankton/multi-linter.js"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit",
        "command": "node scripts/plankton/prevent_config_edits.js",
        "blocking": true
      }
    ]
  }
}
```

---

## Violation Budget Concept

The violation budget is the maximum number of unfixed violations allowed per session. It starts at the baseline measured on session start and must trend downward.

```
Session start:  Measure baseline violations across all tracked files → store as V_0
During session: Each Phase 2 run emits V_n (current violation count)
Session end:    Compare V_n to V_0

Budget health:
  V_n < V_0       → GREEN  (improved)
  V_n == V_0      → YELLOW (no regression, but no improvement)
  V_n > V_0       → RED    (regression — something bypassed Plankton)
  V_n > V_0 + 10  → CRITICAL — escalate to human
```

Track the budget in a session-scoped file: `scripts/plankton/session-metrics.json`

```json
{
  "session_id": "2026-04-03T09:00:00Z",
  "baseline_violations": 47,
  "current_violations": 12,
  "violations_fixed_by_autoformat": 28,
  "violations_delegated_to_subagent": 7,
  "violations_remaining": 12,
  "budget_status": "GREEN"
}
```

---

## Config Protection (Defense Against Rule-Gaming)

Agents will attempt to suppress violations by modifying the tools that catch them:

**Attack vectors blocked:**
- Adding `# noqa`, `// eslint-disable`, `# type: ignore` inline
- Editing `.ruff.toml`, `biome.json`, `.eslintrc`, `pyproject.toml`, `.shellcheckrc`
- Reducing rule severity from `error` to `warn` or `off`
- Adding files/directories to ignore lists without approval

**Protection implementation:**

```javascript
// prevent_config_edits.js — PreToolUse hook
const PROTECTED_FILES = [
  '.ruff.toml', 'ruff.toml', 'biome.json', '.eslintrc',
  '.eslintrc.js', '.eslintrc.json', 'pyproject.toml',
  '.shellcheckrc', '.markdownlint.json', 'sqlfluff.cfg'
];

const targetFile = process.env.TOOL_INPUT_FILE;
const isProtected = PROTECTED_FILES.some(f => targetFile?.endsWith(f));

if (isProtected) {
  console.error(
    `[plankton:blocked] Attempt to modify protected linter config: ${targetFile}\n` +
    `To modify quality rules, get explicit human approval first.\n` +
    `Fix the underlying code violation instead.`
  );
  process.exit(1); // blocks the Edit/Write tool call
}
```

---

## Status Matrix

| Scenario                       | Agent Sees                               | Hook Exit |
| ------------------------------ | ---------------------------------------- | --------- |
| No violations after format     | Nothing                                  | 0         |
| Auto-fixed by formatter        | Nothing                                  | 0         |
| Linter not installed           | `[plankton:advisory] ruff not installed` | 0         |
| Unfixable violations remain    | `[hook] 3 violation(s) remain in foo.py` | 2         |
| Config edit attempt blocked    | `[plankton:blocked] Protected file...`   | 1         |
| Violation budget exceeded      | `[plankton:budget] V_n > V_0 + 10`      | 2         |

---

## Package Manager Enforcement

| Legacy (Blocked) | Modern (Enforced)                     | Why                               |
| ---------------- | ------------------------------------- | --------------------------------- |
| `npm install`    | `bun install` or `npm ci`             | Speed and lockfile stability      |
| `yarn`           | `bun install`                         | Unified fast toolchain            |
| `pip install`    | `uv add` or `uv sync`                 | 10-100x faster, proper isolation  |
| `poetry add`     | `uv add`                              | uv supersedes poetry              |
| `go get`         | `go mod tidy`                         | Idiomatic Go dependency management|

---

## Self-Verification Checklist

Before declaring Plankton active and functioning on a project, verify:

- [ ] All required linters are installed: run `which biome ruff shellcheck shfmt` and confirm each is present for the project's languages
- [ ] `hooks.json` (or equivalent) contains both `PostToolUse` matchers (`Edit` and `Write`) pointing to `multi-linter.js`
- [ ] `PreToolUse` hook for `prevent_config_edits.js` is registered and exits 1 on protected file attempts
- [ ] Session baseline violation count (`V_0`) has been measured and stored in `session-metrics.json`
- [ ] After editing a test file with a known violation, verify Phase 1 runs silently and Phase 2 reports the violation
- [ ] Attempt to edit `biome.json` — confirm the hook blocks it with exit code 1
- [ ] After a full session, confirm violation count trended down (V_n < V_0)
- [ ] CI pipeline exports Plankton violations as job annotations (not just exit codes)

## Success Criteria

Task is complete when:

1. Every `Edit` or `Write` tool call triggers `multi-linter.js` within 2 seconds
2. Zero violations from formatters (Phase 1 catches all auto-fixable issues)
3. Violation budget `V_n <= V_0` at session end — no regressions introduced
4. At least one successful block of a protected config edit attempt is logged
5. All language gates for the project's file types are installed and operational
6. `session-metrics.json` shows `violations_fixed_by_autoformat > 0` (Plankton is active, not just configured)

---

## Anti-Patterns

- Never add `# noqa` or `// eslint-disable` without an accompanying comment explaining why the rule does not apply and human approval because inline suppression annotations accumulate silently across a codebase until the linter report is essentially empty while real violations are hidden behind suppression markers that nobody reviews or removes.
- Never widen a linter rule (e.g., changing `error` to `warn`) to make a violation disappear because demoting a rule from error to warning removes the blocking enforcement that prevents the violation from reaching CI, allowing the problematic pattern to spread across many files before anyone realizes the guard was disabled.
- Never add entire directories to the linter ignore list to silence broad categories of violations because blanket directory ignores disable quality enforcement on all current and future files in that path, creating an unmonitored zone where code quality degrades indefinitely without any visibility.
- Never run Phase 3 (subagent delegation) through Opus because lint fix tasks are mechanical style and import corrections that do not require frontier reasoning capability — routing them through Opus wastes per-token budget that should be reserved for architectural decisions, not semicolon corrections.
- Never let Phase 1 (formatting) produce output to the main agent's context window because formatting messages like "fixed 3 semicolons in foo.ts" are noise that consumes context tokens, distracts the agent from its primary task, and accumulates into thousands of lines of formatting chatter across a long session.
- Never bypass the violation budget check because if `V_n > V_0 + 10` is suppressed rather than surfaced, new violations introduced during the session become invisible, allowing accumulated lint debt to reach production when developers work around local tooling or the hooks are silently broken.
- Never skip the PreToolUse hook registration because config protection only works if it intercepts edits before they are applied — a PostToolUse check that detects a config modification after it is written cannot undo the weakened rule, and the linter config will remain compromised for the rest of the session.

---

## Failure Modes

| Situation                            | Response                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------ |
| Linter not installed on CI           | Add linter install step to CI before Plankton runs; advisory in local dev |
| Hook not firing after file write     | Check `hooks.json` syntax; verify hook runtime is active; re-register    |
| Agent skips hook by using raw shell  | Add ShellExecute/Bash matchers to hooks.json alongside Edit/Write         |
| Violations oscillate (never decrease)| Investigate if Phase 3 subagent is making the same mistake repeatedly; escalate to Sonnet |
| Config edit blocked but needed legitimately | Create a `plankton-override.md` with human signature, then allow the edit |
| Phase 3 subagent times out           | Reduce violation batch size; fix the most critical violations manually    |
| False positives from a rule          | Add a targeted per-file exception with an explanation comment, not a global suppress |

---

## Integration with Mega-Mind

Plankton is positioned in the **Code Improvement** workflow chain:

```
plankton-code-quality → code-polisher → test-driven-development → verification-loop
```

- Invoke `plankton-code-quality` at the START of any development session to establish the violation baseline
- After `code-polisher` runs a refactor, Plankton's hooks verify no new violations were introduced
- Before `verification-loop`, confirm Plankton's `session-metrics.json` shows GREEN budget status
- Plankton is a background process skill — it runs passively via hooks, not on-demand like most skills
