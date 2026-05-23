---
description: Full release coordination lifecycle — versioning, changelog generation, build verification, rollout strategy selection, phased deployment, monitoring, and rollback planning. Use when preparing a release for any environment.
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
---

# Release Workflow

## Trigger

Use when preparing a release for staging or production.

**Quick Start:** `/mega-mind execute release` or `/release`

## Prerequisites

- Feature development complete and merged to main
- All `verification-loop` phases passed
- Code review completed and approved
- The `release-manager` agent persona loaded

## Steps

### 1. Scope the Release

- Identify all commits since the last release tag: `git log --oneline <last_tag>..HEAD`
- Categorize by conventional commit type: `feat:`, `fix:`, `chore:`, `docs:`, `BREAKING CHANGE:`
- Check for any commits that should not be in this release
- Determine the version bump (semver): PATCH, MINOR, or MAJOR

### 2. Generate Changelog

- Compile changes into categories: Added, Changed, Fixed, Deprecated, Removed, Security
- Flag migration notes for breaking changes
- Write user-facing release notes
- Update `CHANGELOG.md`

### 3. Create Release Candidate

- Bump version in package manifest
- Create release commit: `git commit -m "chore: bump version to v<version>"`
- Tag: `git tag v<version>`
- Push: `git push origin v<version>`

### 4. Verify Build and Tests

- CI builds the release tag
- All quality gates pass (see `verification-loop`)
- If build fails → fix and retag
- Do NOT proceed to rollout if any gate is red

### 5. Select Rollout Strategy

| Risk Level                    | Strategy                            | Example                               |
| ----------------------------- | ----------------------------------- | ------------------------------------- |
| Low (patch, small fix)        | Full deploy to 100%                 | Bug fix, dependency update            |
| Medium (minor feat, refactor) | Phased: 10% → 50% → 100%            | New feature, performance improvement  |
| High (major feat, migration)  | Feature-flag gated + phased         | Database migration, new auth flow     |
| Critical (breaking change)    | Dark launch + feature flag + phased | API version bump, architecture change |

### 6. Document Rollback Plan

- For every release, document:
  - Rollback command: `git revert <tag>` or `kubectl rollout undo`
  - Estimated rollback time
  - Data migration rollback (if applicable)
  - Feature flag kill switch location

### 7. Execute Rollout

- Deploy per the selected strategy
- Monitor error rates, latency, and throughput for the defined monitoring window
- If error rate exceeds threshold → halt and rollback
- If monitoring window passes → declare release healthy

### 8. Post-Release Health Check

- Verify all metrics are at or below baseline
- Confirm no alerts have fired
- Write a post-release health report: `docs/releases/v<version>-health.md`
- Declare the release complete

## Next Steps After Release

After completing this workflow, typically continue with:

```
/observability (if monitoring gaps were identified)
/continuous-learning (extract patterns from the release)
```

Or use:

```
/mega-mind execute continuous-learning-v2
```

## Output

- Version tag
- Changelog updated
- Release notes published
- Rollback plan documented
- Post-release health report

## Related Skills

- `release-manager` — The release management agent persona
- `verification-loop` — Quality gate before release
- `ci-config-helper` — CI/CD pipeline configuration
- `observability-specialist` — Post-release monitoring
- `finishing-a-development-branch` — Base shipping workflow
