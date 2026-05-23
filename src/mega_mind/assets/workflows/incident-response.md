---
description: Full incident response lifecycle — detection, severity classification, triage, mitigation, rollback coordination, root cause analysis, and blameless postmortem. Use when production is degraded, down, or exhibiting anomalous behavior.
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
---

# Incident Response Workflow

## Trigger

Use when production is degraded, down, or exhibiting anomalous behavior.

**Quick Start:** `/mega-mind execute incident-response` or `/incident`

## Prerequisites

- Access to production logs, metrics, and deployment history
- The `incident-commander` agent persona loaded
- Communication channel established (Slack, PagerDuty, or equivalent)

## Steps

### 1. Acknowledge and Classify

- Confirm the alert or report
- Classify severity: SEV1 (outage/data corruption) / SEV2 (major degradation) / SEV3 (minor) / SEV4 (cosmetic)
- Default to SEV1 if unsure — severity can always be downgraded
- Notify stakeholders per severity SLA

### 2. Assess Recent Changes

- Review deploys, config changes, dependency updates, and infrastructure changes in the last 24 hours
- If a recent deploy is found → move to Rollback step
- If no deploy → move to Triage step

### 3. Mitigate or Rollback

- **Rollback preferred**: revert the deploy to the last known-good version. Always faster than forward-fix.
- **Feature-flag disable**: if a feature flag exists, disable the feature. Instant effect, no deploy.
- **Traffic drain**: if the issue is limited to a specific region or instance, drain traffic.
- **Forward-fix**: only when rollback is not possible (e.g., irreversible data migration). Fast-track the fix.

### 4. Verify Mitigation

- Confirm error rates returning to baseline
- Confirm affected users can complete their flows
- Document the mitigation action in the incident timeline

### 5. Root Cause Analysis

Use the `debug` workflow if the root cause is unknown:

- Reproduce in staging
- Gather evidence (logs, metrics, traces)
- Form and test hypotheses
- Identify root cause

If the root cause is known (e.g., specific commit), skip to documentation.

### 6. Write Postmortem

Create a blameless postmortem in `docs/postmortems/<date>-<summary>.md`:

- Timeline with all actions and timestamps
- Root cause
- Action items with owners and tracking issues
- Lessons learned (what went well, what went wrong, what to improve)
- Blameless statement

See `incident-commander` agent for the postmortem template.

### 7. Track Action Items

- Create tracking issues for every action item
- Assign owners
- Set deadlines

## Next Steps After Incident Response

After completing this workflow, typically continue with:

```
/debug (if root cause needs deeper investigation)
/review (if code changes resulted)
/ship (if a fix needs to be deployed)
```

Or use:

```
/mega-mind execute review
/mega-mind execute ship
```

## Output

- Incident timeline with timestamps
- Postmortem document
- Action items with owners and tracking issues
- Runbook updates (if applicable)

## Related Skills

- `incident-commander` — The incident management agent persona
- `debugging` — Root cause analysis for unknown issues
- `finishing-a-development-branch` — Shipping the fix
- `security-reviewer` — If the incident has security implications
