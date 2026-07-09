# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] — 2026-07-09

### 🏆 Gold Standard v1.0 — All 53 Skills Upgraded

Every skill upgraded to the **Gold Standard SKILL.md v1.0** specification — 12 required sections:
Blocking Violations, Verification with quality gates, Performance & Cost models, structured
Examples, Anti-Patterns tables, and full References/Changelog. This is the largest quality
upgrade in the project's history.

- **Created** `.agent/shared/GOLD-STANDARD-SKILL.md` — universal 12-section template with scoring rubric
- **All 53 skills** now at 12/12 gold standard sections (100% compliance, 19,531 total lines)
- **Fixed** RTK skill Redux anti-patterns (critical copy-paste bug)
- **Fixed** broken `rtk bun test (or npm test)` syntax across all skills
- **Added** Blocking Violations, Performance & Cost, References to every skill
- **Enhanced** mega-mind orchestrator to 671 lines with workflow chain selection guide
- **Enhanced** security-reviewer with OWASP Top 10 (2025), CWE mappings, STRIDE threat modeling
- **Updated** AGENTS.md, README.md, USAGE.md, and pyproject.toml for v1.0

---

## [0.8.0] — 2026-05-23

### 🏗️ Full Lifecycle Coverage

- **5 new agent personas**: `incident-commander` (production incidents), `release-manager` (versioning/rollouts), `accessibility-auditor` (WCAG compliance), `adversarial-tester` (chaos/fuzz testing), `data-privacy-officer` (GDPR/CCPA/SOC2)
- **2 new workflows**: `incident-response` (full incident lifecycle), `release` (version→changelog→rollout→monitor)
- **5 new workflow chains**: Incident Response, Release, Accessibility Audit, Adversarial Test, Compliance Review — all registered in the mega-mind routing matrix
- Agent personas expanded from 6 → 11, workflows from 7 → 9

### 🔧 Structural Fixes (14 items)

| #   | Issue                             | Resolution                                                             |
| --- | --------------------------------- | ---------------------------------------------------------------------- |
| 1   | `task.md` single-point-of-failure | Backup script + stub + workflow reference                              |
| 2   | Routing matrix drift              | Validator enforces coverage; all 53 skills + 11 agents covered         |
| 3   | Skill count inconsistency         | Reconciled to 53 across AGENTS.md, disk, routing matrix                |
| 4   | Cross-skill vocabulary drift      | 18 headings normalized; verification phases unified                    |
| 5   | Z-Pattern rigidity                | 7 decomposition patterns added (API-First, ML, IaC, etc.)              |
| 6   | Grep-fragile checklists           | 115 patterns fixed across 34 skills (`-E` flag, POSIX-compliant)       |
| 7   | Agent/skill boundary blurred      | Routing note + code-reviewer/qa-engineer added to matrix               |
| 8   | No formal handoff interface       | Handoff block template + 3 key skills updated                          |
| 9   | Instinct decay mechanism          | `last_validated`/`review_by` fields + decay table + conflict detection |
| 10  | `search-first` after routing      | Moved to step 2 in Request Analysis                                    |
| 11  | RTK hard dependency               | Fallback protocol with detection + bare commands                       |
| 12  | No skill regression tests         | Validator script + chain integrity eval                                |
| 13  | Flat verification depth           | Tiered verification (Tier 1 Surface / Tier 2 Standard / Tier 3 Deep)   |
| 14  | Claude-specific idioms            | Runtime-agnostic terms + compatibility section in multi-execute        |

### 🌐 Universal Compatibility

- Unified `compatibility:` frontmatter across all 53 skills, 11 agents, and 9 workflows to:
  `Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)`
- Updated AGENTS.md, README.md, USAGE.md, and pyproject.toml descriptions to reflect universal compatibility

### 📦 Distribution

- Synced all `.agent/` changes to `src/mega_mind/assets/` for correct package distribution
- Created `scripts/validate-skill-system.py` — automated validator (skill count, routing, headings, required sections, grep portability)
- Created `scripts/backup-task-state.sh` — timestamped task.md backups
- Created `scripts/sync-assets.py` — one-command sync from `.agent/` to `src/mega_mind/assets/`
- Fixed Unicode encoding error in CLI (`✅`/`❌` → `[OK]`/`[ERROR]`) for Windows console compatibility

## [0.7.0] — 2026-04-30

### 🔧 Orchestration Fixes

- Fixed 23 stale skill references across the entire skill system (`systematic-debugging` → `debugging`, `verification-before-completion` → `verification-loop`, `bug-hunter` → `debugging`, `api-designer` → `backend-architect`, `using-mega-mind` → `mega-mind`)
- Reconciled skill counts in AGENTS.md — now correctly shows 9 Core + 30 Domain Expert + 12 Meta + 2 Token = 53
- Fixed phase count inconsistency in execute-plan and high-complexity-dev workflows (6 → 10 phases matching verification-loop)
- Added missing `autoresearch-loop` to Meta & Learning skills list
- Added missing `regex-vs-llm-structured-text` to Domain Expert skills
- Recategorized `planner` and `architect` as agent personas (not skills) in AGENTS.md routing matrix
- Completed ship workflow chain with `continuous-learning-v2`

### 🧩 New Platform: pi-coding-agent

- Added `--pi` flag to CLI and installer
- Installs to `.pi/skills/`, `.pi/prompts/`, `.pi/agents/`, and `.agents/skills/` (cross-tool Agent Skills standard)
- Full documentation in README.md and USAGE.md with platform-specific notes

### 📦 Distribution

- Synced all `.agent/` fixes to `src/mega_mind/assets/` for correct package distribution
- Updated README.md: fixed skill counts, shared/ directory listing, removed phantom tests/ dir
- Updated USAGE.md: Step 5 is now general usage guide for all platforms with command reference table

## [0.6.0] — 2026-04-17

### 🔄 Skill Library Consolidation

- Consolidated and enhanced the agent skill library — merged overlapping skills, removed stale ones
- Enhanced agent definitions with structured frameworks and protocols
- Synchronized workflow references with consolidated skill library
- Updated skill listings post-consolidation across all documentation

### 📚 New Shared Operational Guides

- Added `DE-SLOPPIFY.md` — code quality cleanup checklist
- Added `RTK_GUIDE.md` — Rust Token Killer usage guide (60-90% token savings)
- Added `VERIFICATION-GATE.md` — structured 6-phase verification checkpoint

### 📖 Documentation

- Updated skill documentation and usage guide post-consolidation
- Added `.agent/evals` to `.gitignore` for evaluation artifacts

## [0.5.0] — 2026-04-05

### 🏷️ Rebrand to `mmo`

- CLI entry point renamed to `mmo` (was `mega-mind-orchestrator`)
- PyPI package name: `mmo`
- Both `mmo` and `mega-mind-orchestrator` console scripts registered

### 🌐 Platform Support

- Expanded platform flags for targeted installation
- Full Claude Code, GitHub Copilot, OpenCode, and Codex compatibility

## [0.4.0] — 2026-04-03

### 🪝 Context-Mode Hook Integration

- Implemented `context-mode` hook system for all supported environments
- Hooks for PreToolUse, PostToolUse, PreCompact, and SessionStart events
- Added `.agent/hooks/hooks.json` generation

### 🛡️ Behavior Guardrails

- Added session rules: no proactive commits, mandatory task tracking, search-first, de-sloppify, security by design
- Added autoresearch rules: continuous-learning-v2 loop, self-eval before done
- Enforced quality gates before any task marked complete

## [0.3.2] — 2026-03-28

### 🔧 Fixes

- Fixed installation commands to use `mega-mind-orchestrator` console script entry point

## [0.3.1] — 2026-03-27

### 🔧 Fixes

- Updated GitHub Actions workflow versions

## [0.3.0] — 2026-03-27

### 🚀 Platform Installer

- Added `--claude` flag for Claude Code-compatible installation
- Added `--copilot` flag for GitHub Copilot-compatible installation
- Skills copied to platform-specific directories with proper file naming

### 🧠 Mega-Mind Orchestration

- Added structured workflow system via `AGENTS.md` with mega-mind orchestrator
- Request routing matrix, skill chains, workflow definitions
- Task tracking via `docs/plans/task.md`

### 🏷️ Metadata

- Added `compatibility` frontmatter field to all skills for AI coding assistant targeting
- Added `--from` option to uv tool install

## [0.2.0] — 2026-03-25

### 🤖 GitHub Copilot Support

- Added GitHub Copilot-compatible file structure to the installer
- Targeted brainstorming gate for structured exploration

## [0.1.1] — 2026-03-24

### 🔧 Fixes

- Added `--version` option to CLI with proper package name

## [0.1.0] — 2026-03-24

### 🎉 Initial Release

- Mega-Mind CLI tool for skill system installation
- 53+ specialized AI coding assistant skills across 4 categories
- `mmo init` CLI command for project initialization
- PyPI package published as `mega-mind-orchestrator`
- CI/CD pipeline for automated PyPI publishing
- RTK token optimization integration
