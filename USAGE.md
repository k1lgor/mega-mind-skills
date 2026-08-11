# Installing Mega-Mind Skills v1.0.1

This guide covers how to install the Mega-Mind Gold Standard v2.0 skill set into your project so it is available to your AI coding assistant (Antigravity, GitHub Copilot, Claude Code, OpenCode, Codex, etc.).

> **v2.0 Update:** All 53 skills conform to the [Gold Standard SKILL.md v2.0](./.agent/shared/GOLD-STANDARD-SKILL.md) specification — 12 required sections per skill including Blocking Violations, Verification with quality gates, Performance & Cost models, structured Examples, and Anti-Patterns tables. Compliance is machine-verified: every install is checked byte-for-byte against `skills-manifest.json`, and `mmo doctor` confirms hook dependencies and tree integrity.

---

## Step 1 — Install the CLI tool

Choose the method that fits your workflow:

### pip (standard)

```bash
pip install mmo
```

### pipx (recommended — isolated install, globally available)

```bash
pipx install mmo
```

### uv

```bash
# Install as a tool (recommended for frequent use)
uv tool install mmo

# Or run directly without installation
uvx mmo
```

---

## Step 2 — Install the hook prerequisite: `context-mode`

`mmo init` writes `hooks.json` files for supported environments. Those hooks call the `context-mode` CLI, so hook integration will not work unless `context-mode` is installed first.

**Prerequisites:** Node.js 18+

```bash
npm install -g context-mode
context-mode doctor
```

The generated hook entries use commands like:

```json
{
  "command": "context-mode hook claude-code pretooluse"
}
```

If `context-mode doctor` fails, fix that before relying on the generated hooks.

---

## Step 3 — Initialize skills in your project

Navigate to your project root and run:

```bash
uvx mmo init
```

This copies the full `.agent/` directory — containing all 53 active skills, 11 agent personas, 9 executable workflows, shared snippets, and agent definitions — into your project.

When you pass one or more platform flags, `mmo init` installs only those platform-specific files and does **not** also create `.agent/`.

### For Claude Code (CLI)

To also install in the format Claude Code expects, add the `--claude` flag:

```bash
uvx mmo init --claude
```

This installs `CLAUDE.md`, `.claude/skills/` (53 skills), `.claude/commands/` (9 workflows), `.claude/agents/` (11 agent personas), `.claude/shared/`, and `.claude/hooks/hooks.json`.

### For GitHub Copilot (VS Code)

To also install in the format GitHub Copilot expects, add the `--copilot` flag:

```bash
uvx mmo init --copilot
```

This installs `.github/copilot-instructions.md`, `.github/skills/` (53 skills), `.github/agents/` (11 agent personas), `.github/shared/`, and `.github/hooks/hooks.json`.

### For OpenCode

To also install in the format OpenCode expects, add the `--opencode` flag:

```bash
uvx mmo init --opencode
```

This installs `AGENTS.md`, `CLAUDE.md`, `.opencode/skills/`, `.opencode/commands/`, `.opencode/agents/`, `.opencode/shared/`, and `.opencode/hooks/hooks.json`.

### For Codex

To also install in the format Codex expects, add the `--codex` flag:

```bash
uvx mmo init --codex
```

This installs `AGENTS.md`, `.codex/skills/`, `.codex/agents/`, `.codex/shared/`, and `.codex/hooks/hooks.json`.

### For pi-coding-agent

To also install in the format pi expects, add the `--pi` flag:

```bash
uvx mmo init --pi
```

This installs `AGENTS.md`, `CLAUDE.md`, `.pi/skills/`, `.pi/prompts/`, `.pi/agents/`, `.pi/shared/`, `.pi/hooks/hooks.json`, and `.agents/skills/` (cross-tool standard path).

This installs:

- `.agent/` — Core skill system for the default install (`mmo init` with no platform flags)
- `CLAUDE.md` and `.claude/` — Specialized for Claude Code
- `.github/` — Specialized for GitHub Copilot in VS Code
- `.opencode/` — Specialized for OpenCode
- `.codex/` — Specialized for Codex
- `.pi/` — Specialized for pi-coding-agent

### Target a specific directory

```bash
uvx mmo init /path/to/your/project
uvx mmo init /path/to/your/project --claude
uvx mmo init /path/to/your/project --copilot
```

### Overwrite an existing installation

```bash
uvx mmo init --force
uvx mmo init --claude --force
uvx mmo init --copilot --force
uvx mmo init --opencode --force
uvx mmo init --codex --force
uvx mmo init --pi --force
uvx mmo init --copilot --claude --opencode --codex --pi --force
```

> ⚠️ `--force` overwrites the existing directories completely.

---

## What gets installed

### Standard install (`mmo init`)

```
your-project/
└── .agent/
    ├── AGENTS.md          # Master rules loaded at session start
    ├── hooks/
    │   └── hooks.json     # Context-mode hooks registry
    ├── skills/            # 53 skills (mega-mind, brainstorming, tech-lead, ...)
    ├── workflows/         # Pre-defined workflow sequences
    ├── agents/            # Persistent agent personas
    └── instincts/         # Learned patterns
```

### With Claude Code (`mmo init --claude`)

```
your-project/
├── CLAUDE.md        # Specialized project rules for Claude
└── .claude/
    ├── hooks/
    │   └── hooks.json # Context-mode hooks registry for Claude Code
    ├── skills/      # 53 skills as Agent Skills
    ├── commands/    # Workflow files exposed as Claude slash commands
    ├── shared/      # Shared snippet files referenced by skills
    └── agents/      # Agent personas (code-reviewer, tech-lead, ...)
```

### With Copilot (`mmo init --copilot`)

```
your-project/
└── .github/
    ├── copilot-instructions.md        # Global Copilot instructions
    ├── hooks/
    │   └── hooks.json                 # Context-mode hooks registry for GitHub Copilot
    ├── skills/                        # 53 skills as Agent Skills (open standard)
    │   ├── mega-mind/SKILL.md
    │   ├── brainstorming/SKILL.md
    │   ├── tech-lead/SKILL.md
    │   └── ... (50 more)
    ├── shared/                        # Shared snippet files referenced by skills
    └── agents/                        # Custom agent personas
        ├── code-reviewer.agent.md
        ├── tech-lead.agent.md
        └── qa-engineer.agent.md
```

### With OpenCode (`mmo init --opencode`)

```
your-project/
├── AGENTS.md
├── CLAUDE.md
└── .opencode/
    ├── hooks/
    │   └── hooks.json # Context-mode hooks registry for OpenCode
    ├── skills/        # 53 skills
    ├── commands/      # Workflow files exposed as OpenCode slash commands
    ├── shared/        # Shared snippet files referenced by skills
    └── agents/        # Agent personas
```

### With Codex (`mmo init --codex`)

```
your-project/
├── AGENTS.md
└── .codex/
    ├── hooks/
    │   └── hooks.json # Context-mode hooks registry for Codex
    ├── skills/        # 53 skills
    ├── shared/        # Shared snippet files referenced by skills
    └── agents/        # Agent personas
```

### With pi (`mmo init --pi`)

```
your-project/
├── AGENTS.md
├── CLAUDE.md
├── .pi/
│   ├── hooks/
│   │   └── hooks.json  # Context-mode hooks registry for pi
│   ├── skills/         # 53 skills (pi project skill dir)
│   ├── prompts/        # Workflow files as pi prompt templates
│   ├── shared/         # Shared snippet files referenced by skills
│   └── agents/         # Agent personas as prompt templates
└── .agents/
    └── skills/         # Cross-tool Agent Skills standard (pi scans this)
```

---

## Step 4 — Verify the installation

Once initialized:

```bash
# 1. Environment + install-tree integrity (checks context-mode and every
#    installed SKILL.md against the shipped manifest's content hashes)
mmo doctor
```

2. Use the `/verify` command within your AI assistant (e.g. Antigravity or GitHub Copilot) to run the **verification-loop** protocol

`mmo doctor` exits non-zero if `context-mode` is missing from PATH (the generated hooks depend on it) or if any installed skill's content no longer matches the manifest. Re-run it after an `mmo init --force` to confirm a clean install.

---

## Step 5 — Using Mega-Mind Skills

Once installed, the skills integrate automatically with your AI coding assistant. How you invoke them depends on the tool:

### All Tools — The `/mega-mind` Orchestrator

The primary entry point across all platforms:

```
/mega-mind help
/mega-mind route I need to add OAuth authentication
/mega-mind route fix the login bug
/mega-mind status
/mega-mind skills
```

### Direct Skill Invocation

Most platforms support invoking skills directly as slash commands:

| Command       | Skill                          | Purpose                            |
| ------------- | ------------------------------ | ---------------------------------- |
| `/brainstorm` | brainstorming                  | Explore approaches before deciding |
| `/plan`       | writing-plans                  | Create implementation plan         |
| `/execute`    | executing-plans                | Execute plan with tracking         |
| `/debug`      | debugging                      | Debug systematically               |
| `/review`     | requesting-code-review         | Request code review                |
| `/ship`       | finishing-a-development-branch | Deploy to production               |
| `/tdd`        | test-driven-development        | Test-first development             |
| `/verify`     | verification-loop              | Verify before marking done         |

### Platform-Specific Notes

**GitHub Copilot (VS Code):** After `mmo init --copilot`, type `/` in Copilot Chat to see all 53 skills listed. Copilot uses progressive disclosure — full instructions load only when a skill is relevant. Workflow files are not exposed as slash commands (use `/mega-mind execute <workflow>` instead).

**Claude Code:** After `mmo init --claude`, skills load from `.claude/skills/` and workflow commands from `.claude/commands/`. Use `/command-name` for workflow shortcuts.

**OpenCode:** After `mmo init --opencode`, skills load from `.opencode/skills/` and commands from `.opencode/commands/`.

**Codex:** After `mmo init --codex`, skills load from `.codex/skills/`. Use `/mega-mind` for orchestration.

**pi:** After `mmo init --pi`, skills auto-load from `.pi/skills/` and `.agents/skills/`. Workflow prompt templates are available in `.pi/prompts/`.

See the full [README](./README.md) for the complete command reference and skill routing matrix.
