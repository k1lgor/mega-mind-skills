---
description: High-stakes development using multi-agent orchestration and collaborative planning.
---

# High-Complexity Development Workflow

## Trigger

Use for features requiring major architectural changes, deep security considerations, or complex multi-model reasoning.

**Quick Start:** `/mega-mind execute high-complexity-dev`

## Prerequisites

- Feature request with high ambiguity or technical risk.
- Project uses the v1.8.0 skill library.

## Steps

### 1. Research & ADR (Architect)

- Invoke `search-first` to check for prior art.
- Use the **`architect`** agent to analyze trade-offs.
- Create an **ADR (Architecture Decision Record)** in `docs/adr/`.

### 2. Multi-Model Planning (multi-plan)

- Invoke the **`multi-plan`** skill.
- Distribute the ADR and requirements to specialized experts (e.g., Tech vs. UX).
- Synthesize a high-confidence plan in `.agent/plans/`.

### 3. User Approval Gate

- **STOP.** Present the synthesized plan and ADR to the user.
- Wait for explicit approval before proceeding.

### 4. Orchestrated Execution (multi-execute)

- Invoke the **`multi-execute`** skill.
- Generate parallel prototypes (Logic + UI).
- Claude as "Code Sovereign" refactors and merges prototypes into production code.

### 5. Continuous Verification (verification-loop)

- Run the **`verification-loop`**.
- Execute all 6 phases: De-Sloppify ➔ Build ➔ Types ➔ Lint ➔ Tests ➔ Security.
- Target coverage: 80%+.

### 6. Security Audit (security-reviewer)

- Invoke the **`security-reviewer`** for a targeted final scan.
- Remediate any flagged vulnerabilities.

### 7. Branch Wrap-up

- Clean up the feature branch and prepare for PR using `finishing-a-development-branch`.

## Related Skills

- `multi-plan` & `multi-execute`
- `architect` & `security-reviewer`
- `verification-loop`
- `search-first`
