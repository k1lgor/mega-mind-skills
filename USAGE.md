# Installing Mega-Mind Skills

This guide covers how to install the Mega-Mind skill set into your project so it is available to your AI coding assistant (Antigravity, Cursor, etc.).

---

## Step 1 — Install the CLI tool

Choose the method that fits your workflow:

### pip (standard)

```bash
pip install mega-mind
```

### pipx (recommended — isolated install, globally available)

```bash
pipx install mega-mind
```

### uv

```bash
uv tool install mega-mind
```

---

## Step 2 — Initialize skills in your project

Navigate to your project root and run:

```bash
mega-mind init
```

This copies the full `.agent/` directory — containing all 42 skills, workflows, and agent definitions — into your project.

### Target a specific directory

```bash
mega-mind init /path/to/your/project
```

### Overwrite an existing installation

```bash
mega-mind init --force
# or
mega-mind init -f
```

> ⚠️ `--force` overwrites the existing `.agent/` directory completely.

---

## What gets installed

After `mega-mind init`, your project will contain:

```
your-project/
└── .agent/
    ├── AGENTS.md          # Master rules loaded at session start
    ├── skills/            # 42 skills (mega-mind, brainstorming, tech-lead, ...)
    ├── workflows/         # Pre-defined workflow sequences
    ├── agents/            # Persistent agent personas
    └── tests/
        └── run-tests.sh   # Validates the installation
```

---

## Step 3 — Verify the installation

```bash
bash .agent/tests/run-tests.sh
```

A successful run confirms all skills, workflows, and agents are in place.

---

## Usage

Once installed, use the `/mega-mind` command in your AI assistant chat to start orchestrating:

```
/mega-mind help
/mega-mind route I need to add OAuth authentication
/mega-mind route fix the login bug
```

See the full [README](./README.md) for the complete command reference and skill routing matrix.
