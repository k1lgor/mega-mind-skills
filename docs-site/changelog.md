# Changelog

## [0.8.0] — 2026-05-23

### Full Lifecycle Coverage

- **5 new agent personas**: `incident-commander` (production incidents), `release-manager` (versioning/rollouts), `accessibility-auditor` (WCAG compliance), `adversarial-tester` (chaos/fuzz testing), `data-privacy-officer` (GDPR/CCPA/SOC2)
- **2 new workflows**: `incident-response` (full incident lifecycle), `release` (version → changelog → rollout → monitor)
- **5 new workflow chains**: Incident Response, Release, Accessibility Audit, Adversarial Test, Compliance Review
- Agent personas expanded from 6 → 11, workflows from 7 → 9

### Structural Fixes

14 fixes including routing matrix coverage, heading normalization, grep portability,
tiered verification, handoff interface, instinct decay mechanism, search-first ordering,
RTK fallback protocol, and automated skill system validation.

### Universal Compatibility

All skills, agents, and workflows now declare compatibility with any AI coding agent.

### Distribution

- Version bumped to 0.8.0
- Source distribution and wheel built
- GitHub tag v0.8.0 pushed

## [0.7.0] — 2026-04-30

### Orchestration Fixes

- Fixed 23 stale skill references across the entire skill system
- Reconciled skill counts in AGENTS.md — now correctly shows 53
- Fixed phase count inconsistency in workflow chains
- Added missing `autoresearch-loop` and `regex-vs-llm-structured-text` to skill lists

### New Platform: pi-coding-agent

- Added `--pi` flag to CLI and installer
- Cross-tool Agent Skills standard support

### Distribution

- Synced all `.agent/` fixes to `src/mega_mind/assets/`
- Updated README, USAGE, documentation

## [0.6.0] — 2026-04-17

### Skill Library Consolidation

- Merged overlapping skills, removed stale ones
- Enhanced agent definitions with structured frameworks
- Added shared operational guides (DE-SLOPPIFY, RTK_GUIDE, VERIFICATION-GATE)

## [0.5.0] — 2026-04-05

Initial public release. Core skill system with 53 skills, 6 agent personas, and 7 workflows.
