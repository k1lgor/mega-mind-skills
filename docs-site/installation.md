# Installation

## Step 1 — Install the CLI (v1.0.0)

```bash
# pip (standard)
pip install mmo

# pipx (recommended — isolated install, globally available)
pipx install mmo

# uv (fast Python package manager)
uv tool install mmo

# Run directly without installation
uvx mmo
```

## Step 2 — Initialize in your project

```bash
cd /path/to/your/project

# Standard install (creates .agent/)
uvx mmo init
```

## Platform-Specific Installs

Pass one or more platform flags to install for specific AI coding assistants.

### Claude Code

```bash
uvx mmo init --claude
```

Creates: `CLAUDE.md`, `.claude/skills/` (53 skills), `.claude/commands/` (9 workflows),
`.claude/agents/` (11 persona), `.claude/shared/`, `.claude/hooks/hooks.json`.

### GitHub Copilot

```bash
uvx mmo init --copilot
```

Creates: `.github/copilot-instructions.md`, `.github/skills/`, `.github/agents/`,
`.github/shared/`, `.github/hooks/hooks.json`.

### OpenCode

```bash
uvx mmo init --opencode
```

Creates: `AGENTS.md`, `CLAUDE.md`, `.opencode/skills/`, `.opencode/commands/`,
`.opencode/agents/`, `.opencode/shared/`, `.opencode/hooks/hooks.json`.

### Codex

```bash
uvx mmo init --codex
```

Creates: `AGENTS.md`, `.codex/skills/`, `.codex/agents/`, `.codex/shared/`,
`.codex/hooks/hooks.json`.

### pi-coding-agent

```bash
uvx mmo init --pi
```

Creates: `AGENTS.md`, `CLAUDE.md`, `.pi/skills/`, `.pi/prompts/`, `.pi/agents/`,
`.pi/shared/`, `.pi/hooks/hooks.json`, `.agents/skills/`.

### Multiple platforms

```bash
uvx mmo init --copilot --claude --force
```

When flags are passed, only the requested platforms are installed — `.agent/` is **not** created.

## Overwriting

```bash
uvx mmo init --force
uvx mmo init --copilot --claude --force
```

## Verify Installation

```bash
mmo --version
# Should output: mmo, version 1.0.0
```

Then in your AI assistant, run `/verify` to confirm all skills are correctly installed.

## CLI Reference

```bash
# Install into a specific directory
uvx mmo init /path/to/project
uvx mmo init /path/to/project --copilot

# Show version
uvx mmo --version
# or
mmo --version
```
