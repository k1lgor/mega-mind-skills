# Mega-Mind Skills System v1.0

A unified Gold Standard skill system for any AI coding assistant — covering the full software
development lifecycle from planning through production operations and compliance.

- **53 Gold Standard Skills** — Core workflow, domain expert, meta/learning, and token optimization — every skill meets the [Gold Standard SKILL.md v1.0](https://github.com/k1lgor/mega-mind-skills/blob/main/.agent/shared/GOLD-STANDARD-SKILL.md) specification with 12 required sections including Blocking Violations, Verification with quality gates, Performance & Cost models, and Anti-Patterns tables.

- **11 Agent Personas** — Deep-dive personas for architecture, QA, security, accessibility, adversarial testing, privacy, incidents, and releases.

- **9 Workflow Chains** — Executable sequences covering the full lifecycle: brainstorm → plan → build → verify → ship → release → operate → learn.

- **Multi-Platform** — Works with Antigravity, Claude Code, GitHub Copilot, Cursor, OpenCode, Codex, and pi — any tool supporting the Agent Skills open standard.

> **New in v1.0 (2026-07-09):** All 53 skills upgraded to Gold Standard. 19,531 total lines, 12/12 sections compliance. See the [changelog](changelog.md) for details.

## Quick Start

```bash
# Install the CLI
pip install mmo          # or
pipx install mmo         # (recommended) or
uv tool install mmo      # or
uvx mmo                  # run without installing

# Initialize in your project
cd /path/to/your/project
uvx mmo init             # creates .agent/ with all 53 skills
```

Then in your AI assistant:

```
/mega-mind I need to add user authentication
/mega-mind route "fix this production bug"
/brainstorm How should I design the payment flow?
/verify
```

[Read the full installation guide &rarr;](installation.md)

## What's Inside

### Orchestrator

The `/mega-mind` command is your primary entry point. It analyzes requests, routes to the
appropriate skill or agent, chains multi-step workflows, and tracks progress via `task.md`.

### Skill Categories

| Category           | Count | Purpose                                                           |
| ------------------ | ----- | ----------------------------------------------------------------- |
| Core Workflow      | 9     | Brainstorming, planning, TDD, debugging, review, shipping         |
| Domain Expert      | 30    | Architecture, DevOps, data, ML, security, performance, UX         |
| Meta & Learning    | 12    | Continuous learning, search-first, verification, autonomous loops |
| Token Optimization | 2     | RTK proxy, context optimization                                   |

### Agent Personas

| Category              | Personas                                                                      |
| --------------------- | ----------------------------------------------------------------------------- |
| Development           | `tech-lead`, `planner`, `architect`                                           |
| Quality & Testing     | `code-reviewer`, `qa-engineer`, `accessibility-auditor`, `adversarial-tester` |
| Security & Compliance | `security-reviewer`, `data-privacy-officer`                                   |
| Operations & Releases | `incident-commander`, `release-manager`                                       |

### Workflow Chains

| Workflow            | Purpose                            |
| ------------------- | ---------------------------------- |
| brainstorm          | Structured exploration             |
| write-plan          | Implementation planning            |
| execute-plan        | Disciplined step-by-step execution |
| high-complexity-dev | Multi-agent orchestration          |
| review              | Structured code review             |
| debug               | Root cause analysis                |
| ship                | Merge, deploy, branch cleanup      |
| incident-response   | Production incident lifecycle      |
| release             | Versioning, rollout, monitoring    |

[Full reference &rarr;](reference.md)

## Compatibility

Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools
supporting the [Agent Skills open standard](https://agentskills.io)).
