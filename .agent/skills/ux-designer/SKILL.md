---
name: ux-designer
compatibility: Antigravity, Claude Code, GitHub Copilot
description: UI/UX flows and design systems. Use for user experience design tasks.
triggers:
  - "UX design"
  - "user experience"
  - "design system"
  - "user flow"
---

# UX Designer Skill

## Identity

You are a UX design specialist focused on creating intuitive user experiences and design systems.

## When to Use

- Designing user flows
- Creating design systems
- Improving user experience
- Accessibility improvements

## When NOT to Use

- Backend/API work with no user-facing component — ux-designer operates exclusively on user-facing surfaces
- Minor styling tweaks to a single component that are already specified — use `frontend-architect` or edit directly
- When the feature requirements and user stories are not yet defined — use `product-manager` to define them first
- Performance optimization of backend services — use `performance-profiler` instead

## User Research Framework

```markdown
## User Research

### User Personas

| Persona     | Goals                 | Pain Points              |
| ----------- | --------------------- | ------------------------ |
| Power User  | Efficiency, shortcuts | Too many clicks          |
| New User    | Guidance, simplicity  | Complex interface        |
| Mobile User | Quick access          | Small screen limitations |

### User Journey Map

1. Discovery → 2. Onboarding → 3. Core Task → 4. Completion → 5. Return
```

## Design System Components

### Design Tokens

```css
/* tokens.css */
:root {
  /* Colors */
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  --color-neutral-50: #fafafa;
  --color-neutral-500: #737373;
  --color-neutral-900: #171717;

  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Typography */
  --font-family: system-ui, -apple-system, sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Borders */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}
```

### Component Patterns

```markdown
## Button Component

### Variants

| Variant   | Usage               | Style                |
| --------- | ------------------- | -------------------- |
| Primary   | Main actions        | Solid, accent color  |
| Secondary | Alternative actions | Outline, neutral     |
| Ghost     | Tertiary actions    | No border, text only |
| Danger    | Destructive actions | Red accent           |

### States

- Default: Normal appearance
- Hover: Slight color change
- Focus: Focus ring for accessibility
- Active: Pressed appearance
- Disabled: Reduced opacity, no interaction

### Sizes

| Size   | Padding   | Font Size |
| ------ | --------- | --------- |
| Small  | 8px 16px  | 14px      |
| Medium | 12px 24px | 16px      |
| Large  | 16px 32px | 18px      |
```

## User Flow Templates

### Onboarding Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Welcome   │───▶│   Sign Up   │───▶│   Profile   │
│   Screen    │    │   Form      │    │   Setup     │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Login     │    │   Tutorial  │
                   │   Screen    │    │   Optional  │
                   └─────────────┘    └─────────────┘
```

### Checkout Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Cart    │──▶│ Shipping │──▶│ Payment  │──▶│  Confirm │
│ Review   │   │  Info    │   │  Info    │   │ Success  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │
     ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Continue │   │ Back to  │   │ Edit     │
│ Shopping │   │  Cart    │   │ Payment  │
└──────────┘   └──────────┘   └──────────┘
```

## Accessibility Guidelines

```markdown
## WCAG 2.1 Compliance

### Perceivable

- [ ] Text alternatives for images
- [ ] Captions for videos
- [ ] Color contrast ratio 4.5:1 minimum
- [ ] Resizable text up to 200%

### Operable

- [ ] Keyboard navigation support
- [ ] Focus indicators visible
- [ ] Skip navigation links
- [ ] No keyboard traps

### Understandable

- [ ] Clear and consistent navigation
- [ ] Form labels and instructions
- [ ] Error messages are helpful
- [ ] Language attribute set

### Robust

- [ ] Valid HTML
- [ ] ARIA landmarks used
- [ ] Screen reader tested
- [ ] Works without JavaScript (progressive enhancement)
```

## Tips

- Design for accessibility from the start
- Use consistent patterns across the app
- Test with real users
- Consider edge cases
- Document design decisions

## Anti-Patterns

- Never design a UI without testing it with real users because designers systematically over-estimate how intuitive their own designs are; assumptions that feel obvious to the designer are consistently confusing to first-time users.
- Never use colour alone to convey information because approximately 8% of users have colour vision deficiency and will receive no information from a colour-only signal; WCAG 2.1 SC 1.4.1 requires a secondary indicator.
- Never add a feature without considering the impact on the existing information architecture because each new feature adds a navigation node and cognitive load; an unchecked IA grows until users cannot find anything.
- Never skip loading and error states in a design because a shipped UI without designed loading and error states defaults to raw browser spinners and unstyled error text, producing a broken experience on every slow or failed network call.
- Never design for the happy path only because users who hit an empty state, a permission error, or a partial data load see the gaps left by happy-path-only design; these states are the ones that drive user churn.
- Never use placeholder text in a final design because placeholder text disappears when the user starts typing, removing the only label they had; production components based on placeholder-as-label designs fail WCAG 2.1 SC 3.3.2.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Design system token used inconsistently, causing visual regression on mobile | Developer hardcodes a hex colour instead of using the token variable; token update doesn't propagate | Audit computed styles with browser DevTools on mobile viewport (320px); replace all hardcoded values with design tokens before shipping |
| Accessibility review skipped, component ships with 0 ARIA labels | Deadline pressure causes the accessibility checklist to be deferred; no automated check in CI | Run axe-core (or equivalent) in CI as a blocking step; any component with 0 ARIA roles on interactive elements must not merge |
| User flow designed without edge case (empty state, error state) coverage | Happy-path flow designed first and only; edge states added as afterthoughts or not at all | For every flow, explicitly design the empty state, error state, and loading state before the flow is considered complete |
| Font loaded synchronously blocking render, causing FOUT | Font `<link>` added in `<head>` without `rel="preload"` or `font-display: swap`; blocks paint until font loads | Add `font-display: swap` to the `@font-face` declaration; use `rel="preload"` for critical fonts; verify with Lighthouse |
| Interactive affordance missing on mobile touch target (<44px) | Component designed at desktop scale; touch target too small to tap reliably on mobile | Measure all interactive elements at 320px viewport width; any target smaller than 44×44px must be expanded before shipping |

## Self-Verification Checklist

- [ ] 0 critical accessibility violations: axe-core scan exits 0 — critical violation count = 0
- [ ] All interactive elements have touch target >= 44x44px — verified at 320px viewport width
- [ ] Design reviewed on mobile viewport (320px): `grep -c "320px\|mobile\|responsive" design_review.md` returns > 0
- [ ] User personas defined: `grep -c "persona\|Persona" ux_doc.md` returns >= 1
- [ ] All interactive states covered: `grep -c "hover\|focus\|active\|disabled\|loading\|error\|empty" src/components/` returns > 0
- [ ] Color contrast ratio meets WCAG 2.1 AA: normal text contrast >= 4.5:1, large text >= 3:1 — verified with a contrast checker

## Success Criteria

This task is complete when:
1. User flows are fully documented from entry point to completion, including all branching paths and error states
2. WCAG 2.1 AA compliance is confirmed for all color combinations and interactive elements
3. The design system components used are documented with their variants, states, and usage guidelines
