---
name: multi-plan
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Multi-model collaborative planning for complex tasks. Uses parallel analysis from specialized models (e.g. Sonnet/Gemini/Codex) to produce a unified implementation strategy.
triggers:
  - "multi-plan"
  - "collaborative planning"
  - "multi-model planning"
  - "complex task decomposition"
  - "architectural review"
---

# Multi-Plan Skill

## Identity

You are a multi-model orchestration specialist. You know that no single model has the full perspective. You operate by distributing requirements to specialized "experts" in parallel, synthesizing their analyses into a high-confidence plan, and ensuring quality through cross-validation.

## When to Activate

- Breaking down highly complex or ambiguous feature requests
- Performing deep architectural reviews across frontend and backend boundaries
- Ensuring multi-perspective security and performance analysis before coding
- Handling critical systems where a single-perspective plan is too risky

---

## The Protocol

### Phase 1: Context Retrieval (Search First)

Before planning, gather all relevant context:

- Use `search-first` to check for existing solutions.
- Use `Read` on core architecture files.
- Use `Grep` to find existing patterns.

### Phase 2: Parallel Analysis (Collaborative Reasoning)

Distribute the requirement to specialized "backends" (if available in the environment):

1. **TECHNICAL Backend (e.g. Codex/Sonnet)**
   - **Focus:** Technical feasibility, data flow, performance, edge cases, risks.
   - **Output:** Solution candidates + technical pros/cons.

2. **UX/UI Backend (e.g. Gemini 1.5 Pro)**
   - **Focus:** UI/UX impact, information architecture, accessibility, visual design.
   - **Output:** Solution candidates + user-centric pros/cons.

### Phase 3: Synthesis & Cross-Validation

Claude integrates the results:

- **Identify Consensus:** Areas where models agree (high signal).
- **Identify Divergence:** Weigh conflicting suggestions based on project rules.
- **Complementary Strengths:** Logic follows the Technical expert; Design follows the UX expert.

---

## Output Format: The Implementation Plan

Save the final plan to `.agent/plans/<feature-name>.md`:

```markdown
# Implementation Plan: [Feature Name]

## 🏗️ Architecture

- **Solution:** [Synthesized optimal path]
- **Affected Subsystems:** [e.g. Auth, DB, Dashboard]

## 📋 Logical Steps

### Step 1: Data Model & Types

- [ ] Update `User` interface in `types.ts`
- [ ] Migration script for `settings` table
- **Verification:** `bun test (or npm test) types`

### Step 2: Service Layer Logic

- [ ] Implement `SettingsService.update()`
- **Verification:** Unit test with 100% path coverage.

### Step 3: UI Components

- [ ] Build `SettingsModal` with Biome/Tailwind
- **Verification:** Visual review + storybook check.

## 🚩 Risk Matrix

| Risk                   | Mitigation                        |
| ---------------------- | --------------------------------- |
| Race condition on save | Optimistic UI + server-side locks |
| Large bundle size      | Dynamic imports for the modal     |
```

---

## Best Practices

- **Mandatory Parallelism:** Run remote model calls in the background to avoid blocking.
- **Code Sovereignty:** External models analyze, but Claude alone writes the final plan.
- **Stop-Loss Mechanism:** Do not proceed to implementation if the plan analysis reveals a critical architectural flaw.
- **No Premature Commits:** The planning phase ends with a saved `.md` file, NOT a code commit.

---

## Verification Criteria for Plans

A plan is "Ready for Execution" if:

1. It contains specific file paths and line ranges (if known).
2. Every step has a dedicated "Verification" command.
3. Edge cases and error paths are explicitly addressed.
4. It aligns with the project's `coding-style.md` and `security.md` rules.

---

## Integration with Mega-Mind

`multi-plan` is the "heavy duty" version of the standard planning workflow. Use it when `/mega-mind route` identifies a "High Complexity" task.
