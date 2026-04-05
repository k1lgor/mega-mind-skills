# Installing Mega-Mind Skills

This guide covers how to install the Mega-Mind skill set into your project so it is available to your AI coding assistant (Antigravity, GitHub Copilot, Claude Code, OpenCode, Codex, etc.).

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

This copies the full `.agent/` directory — containing all 53 active skills, workflows, shared snippets, and agent definitions — into your project.

When you pass one or more platform flags, `mmo init` installs only those platform-specific files and does **not** also create `.agent/`.

### For Claude Code (CLI)

To also install in the format Claude Code expects, add the `--claude` flag:

```bash
uvx mmo init --claude
```

This installs `CLAUDE.md`, `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, `.claude/shared/`, and `.claude/hooks/hooks.json`.

### For GitHub Copilot (VS Code)

To also install in the format GitHub Copilot expects, add the `--copilot` flag:

```bash
uvx mmo init --copilot
```

This installs `.github/copilot-instructions.md`, `.github/skills/`, `.github/agents/`, `.github/shared/`, and `.github/hooks/hooks.json`.

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

This installs:

- `.agent/` — Core skill system for the default install (`mmo init` with no platform flags)
- `CLAUDE.md` and `.claude/` — Specialized for Claude Code
- `.github/` — Specialized for GitHub Copilot in VS Code
- `.opencode/` — Specialized for OpenCode
- `.codex/` — Specialized for Codex

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
uvx mmo init --copilot --claude --opencode --codex --force
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
    ├── skills/            # 60+ skills (mega-mind, brainstorming, tech-lead, ...)
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

---

## Step 4 — Verify the installation

Once initialized:

1. Run `context-mode doctor` to verify the hook dependency is installed and healthy
2. Use the `/verify` command within your AI assistant (e.g. Antigravity or GitHub Copilot) to run the **verification-before-completion** protocol

This ensures both the hook integration and the skill system are correctly loaded and ready for use.

---

## Step 5 — Use in GitHub Copilot (VS Code)

After `mmo init --copilot`, open VS Code with GitHub Copilot enabled.

In the Copilot Chat:

1. **Use skills as slash commands** — type `/` to see all 60 skills listed
2. **Invoke mega-mind** — type `/mega-mind` to start the orchestrator
3. **Direct skill commands** — type `/brainstorming`, `/tech-lead`, `/debug`, etc.

Copilot does not have a commands/workflows directory equivalent, so Mega-Mind workflow files are only exposed as slash commands for Claude Code and OpenCode.

Skills use Copilot's **progressive disclosure** system:

- Copilot reads `name` + `description` upfront (lightweight)
- Full instructions load only when the skill is relevant to your request
- You can force-invoke any skill with its `/` slash command

---

## Usage (all tools)

Once installed, use the `/mega-mind` command in your AI assistant chat to start orchestrating:

```
/mega-mind help
/mega-mind route I need to add OAuth authentication
/mega-mind route fix the login bug
```

See the full [README](./README.md) for the complete command reference and skill routing matrix.
