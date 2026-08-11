# Changelog

All notable changes to this project will be documented in this file.

## [1.0.3] — 2026-08-11

### 🔧 Fix: PyPI Metadata Summary Over Limit

- The `pyproject.toml` `description` (561 chars) exceeded PyPI's 512-character summary limit, so every upload since v1.0.0 was rejected with `400 'summary' field must be 512 characters or less`. Shortened to a compliant one-line summary; the full feature description lives in the README (the long description). The Publish to PyPI workflow should now succeed end-to-end.

---

## [1.0.2] — 2026-08-11

### 🔧 Hotfix: Platform-Independent Content Hashes

- Content hashes in `skills-manifest.json` are now computed over **line-ending-normalized** bytes (CRLF ≡ LF), so `mmo check`, `mmo doctor`, and the `validate.yml` CI gate produce identical results on Windows and Linux checkouts. The `v1.0.1` tag shipped hashes derived from Windows CRLF working-tree bytes, which made the manifest-freshness check fail on Linux CI; this release corrects that before any distribution.

---

## [1.0.1] — 2026-08-11

### 🔧 Routing & Validation Hardening

- **Single source of truth:** Added `scripts/build-manifest.py`, which generates `.agent/shared/skills-manifest.json` — a machine-readable inventory of all 53 skills (name, category, version, triggers, description, SHA-256 content hash, and 12-section gold-standard compliance). The validator, renderer, installer, and docs all consume it; counts and membership can no longer drift.
- **Machine-checkable routing:** Added `.agent/shared/routing.json` — the curated routing matrix (54 routes, 11 chains) as data. `scripts/render-skills.py` renders the ASCII matrix and `/mega-mind skills` listing into `mega-mind/SKILL.md` inside `<!-- GENERATED -->` fences; any hand-edit or drift fails CI.
- **Manifest-driven validator:** Rewrote `scripts/validate-skill-system.py`. The old validator demanded headings skills don't have (51/53 false failures); the new one checks manifest freshness (hash equality), frontmatter rules, 12/12 gold-standard sections (with the "Instructions / Workflow" tolerance), routing coverage + target validity, chain integrity, trigger collisions, and version attestation (pyproject.toml == `__init__.py`).
- **Hash-verified sync:** `scripts/sync-assets.py` now regenerates the manifest and rendered docs *before* copying, then verifies `.agent/` and `src/mega_mind/assets/` byte-for-byte (content hashes, not counts). `--check` mode added.
- **`mmo doctor` + `mmo check`:** The CLI now diagnoses the environment (`context-mode` presence) and verifies any installed tree against the manifest's content hashes; `mmo check` is the repository gate (manifest → rendered docs → validator → sync → sandboxed install of all 6 platform layouts).
- **Verified installs:** `installer.py` copies full skill directories (supporting files no longer dropped), verifies every copied file byte-for-byte, and structurally checks agent personas (frontmatter injection). A corrupt install fails at the dock, not at runtime.
- **Tests + CI:** Added `tests/` (12 tests: manifest, renderer, installer layouts/verification, validator) and `.github/workflows/validate.yml` (ubuntu + windows: manifest → render → validate → sync → `mmo check` → pytest).
- **Version & spec alignment:** pyproject.toml 1.0.0 → 1.0.1 with `__init__.py` deriving from package metadata (fallback kept in sync); Gold Standard spec references unified to **v2.0** everywhere; **skill frontmatter versions corrected to 2.0.0** (they were upgraded to Gold Standard v2.0 in 1.0.0 but the frontmatter was never bumped) — a new validator check (`skill_versions`) now enforces frontmatter == latest changelog row; category counts corrected to frontmatter ground truth (12 core-workflow / 29 domain-expert / 8 meta-learning / 4 token-optimization) across README, USAGE, AGENTS.md, docs-site, and the mega-mind skill; stale routing names fixed (`perf-profiler`, `tdd`, `docker`, `k8s`); README documents the three version dimensions (package 1.0.1 / spec 2.0 / skills 2.0.0).
- **Docs generated where possible:** README's skill catalog, docs-site `reference.md` skill/chains tables, and `index.md` category table are generated regions — updating a skill's frontmatter updates every table via `render-skills.py`.

---

## [1.0.0] — 2026-07-09

### 🏆 Gold Standard v1.0 — All 53 Skills Upgraded

Every skill in the Mega-Mind system has been upgraded to the **Gold Standard SKILL.md v1.0** specification — 12 required sections covering identity, principles, blocking violations, verification, performance/cost, examples, anti-patterns, references, and changelog. This is the largest quality upgrade in the project's history.

#### ✨ Gold Standard Template

- Created `.agent/shared/GOLD-STANDARD-SKILL.md` — the universal 12-section template with scoring rubric (8.5/10 minimum)
- All 53 skills now have: `version: "2.0.0"`, `category`, `dependencies`, Blocking Violations table, Verification with commands + quality gates, Performance & Cost, structured Examples, Anti-Patterns table, References, and Changelog

#### 🔧 Critical Bug Fixes

- **RTK skill**: Replaced Redux anti-patterns (copy-paste error — "createSlice", "Redux state", "useSelector") with correct RTK-CLI anti-patterns (destructive operations, compact output, interactive commands, error pattern filtering)
- **Broken syntax**: Fixed `rtk bun test (or npm test)` pattern across all skills — replaced with proper shell-compatible alternatives

#### 🏗️ Skill Upgrades (53/53)

- **mega-mind orchestrator**: Upgraded to 671 lines — added Blocking Violations (7 entries), Performance & Cost (model selection table), References, Changelog, autonomous development chain, workflow chain selection guide
- **9 core workflow skills**: All upgraded with Core Principles enforcement, structured workflow steps (Goal/Output/Tools/Gate), quality gates, and expanded examples
- **9 architecture + dev skills**: ADR templates added to architecture skills, before/after code examples enhanced, all sections added
- **8 testing + devops skills**: Framework-specific verification commands, hypothesis-driven debugging loop formalized, IaC patterns with dry-run validation
- **26 domain + meta skills**: Security-reviewer enhanced with OWASP Top 10 (2025), CWE mappings, STRIDE threat modeling, supply chain security checklist

#### 📊 Quality Metrics

- **19,531 total lines** across all 53 skills (avg 369/skill)
- **12/12 sections** in all 53 skills (100% compliance)
- **0 skills** below 12 gold standard sections
- **Line distribution**: 4 under 200, 13 at 200-300, 28 at 300-500, 8 above 500

#### 📖 Documentation

- Updated `AGENTS.md` with v1.0 branding, gold standard reference, and quality section
- Updated `README.md` and `USAGE.md` with v1.0 information
- Updated `pyproject.toml` to version 2.0.0

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
