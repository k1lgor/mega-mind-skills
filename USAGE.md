# Installing Mega-Mind Skills

This guide covers how to install the Mega-Mind skill set into your project so it is available to your AI coding assistant (Antigravity, GitHub Copilot, etc.).

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

## Step 2 — Initialize skills in your project

Navigate to your project root and run:

```bash
mmo init
```

This copies the full `.agent/` directory — containing all 42 skills, workflows, and agent definitions — into your project.

### For Claude Code (CLI)

To also install in the format Claude Code expects, add the `--claude` flag:

```bash
mmo init --claude
```

### For GitHub Copilot (VS Code)

To also install in the format GitHub Copilot expects, add the `--copilot` flag:

```bash
mmo init --copilot
```

### For OpenCode

To also install in the format OpenCode expects, add the `--opencode` flag:

```bash
mmo init --opencode
```

### For Codex

To also install in the format Codex expects, add the `--codex` flag:

```bash
mmo init --codex
```

This installs:

- `.agent/` — Core skill system for all tools
- `CLAUDE.md` and `.claude/` — Specialized for Claude Code
- `.github/` — Specialized for GitHub Copilot in VS Code
- `.opencode/` — Specialized for OpenCode
- `.codex/` — Specialized for Codex

### Target a specific directory

```bash
mmo init /path/to/your/project
mmo init /path/to/your/project --claude
mmo init /path/to/your/project --copilot
```

### Overwrite an existing installation

```bash
mmo init --force
mmo init --claude --force
mmo init --copilot --force
mmo init --opencode --force
mmo init --codex --force
mmo init --copilot --claude --opencode --codex --force
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
├── .agent/          # Standard AI tool format
├── CLAUDE.md        # Specialized project rules for Claude
└── .claude/
    ├── hooks/
    │   └── hooks.json # Context-mode hooks registry for Claude Code
    └── skills/      # 42 skills as Agent Skills
```

### With Copilot (`mmo init --copilot`)

```
your-project/
├── .agent/                            # Standard AI tool format
└── .github/
    ├── copilot-instructions.md        # Global Copilot instructions
    ├── hooks/
    │   └── hooks.json                 # Context-mode hooks registry for GitHub Copilot
    ├── skills/                        # 42 skills as Agent Skills (open standard)
    │   ├── mega-mind/SKILL.md
    │   ├── brainstorming/SKILL.md
    │   ├── tech-lead/SKILL.md
    │   └── ... (39 more)
    └── agents/                        # Custom agent personas
        ├── code-reviewer.agent.md
        ├── tech-lead.agent.md
        └── qa-engineer.agent.md
```

---

## Step 3 — Verify the installation

Once initialized, use the `/verify` command within your AI assistant (e.g. Antigravity or GitHub Copilot) to run the **verification-before-completion** protocol. This ensures that the skill system is correctly loaded and ready for use.

---

## Step 4 — Use in GitHub Copilot (VS Code)

After `mmo init --copilot`, open VS Code with GitHub Copilot enabled.

In the Copilot Chat:

1. **Use skills as slash commands** — type `/` to see all 42 skills listed
2. **Invoke mega-mind** — type `/mega-mind` to start the orchestrator
3. **Direct skill commands** — type `/brainstorming`, `/tech-lead`, `/debug`, etc.

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
