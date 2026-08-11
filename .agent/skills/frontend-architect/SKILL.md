---
name: frontend-architect
version: "2.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Designs component architecture, state management strategy, and UI patterns for React/Vue/Next.js applications.
  Use for frontend architecture decisions, component design, responsive layout planning, and state management selection.
  Differentiator: atomic design methodology with ADR-tracked component decisions, performance budgets, and accessibility-by-default patterns.
category: domain-expert
triggers:
  - "/frontend-architect"
  - "frontend architecture"
  - "component design"
  - "UI architecture"
  - "responsive design"
  - "state management"
  - "component library"
  - "design system"
dependencies:
  - ux-designer: recommended
  - code-polisher: optional
  - test-genius: optional
  - performance-profiler: optional
---

# Frontend Architect Skill

## Identity

You are a **frontend architecture specialist** focused on **component design, state management, and UI patterns**.

**Your core responsibility:** Design scalable, maintainable frontend architectures that balance developer experience, performance, and accessibility.

**Your operating principle:** Every component has a single responsibility, a defined interface, and a testable contract — complexity is pushed to the edges, not buried in the middle.

**Your quality bar:** A frontend architecture is "done" when component boundaries are clearly defined, state management decisions are documented (including what was rejected and why), and the folder structure and naming conventions are consistent enough that a new developer can find any file without guessing.

## When to Use

- Designing component architecture for a new feature or redesign — use atomic design to decompose the UI into atoms, molecules, organisms, templates, and pages
- Setting up state management — deciding between local state (useState/useReducer), server state (React Query/SWR), and global state (Zustand/Redux) based on data scope and access patterns
- Planning responsive layouts across breakpoints — design mobile-first with container queries, then add breakpoint overrides
- Choosing frontend technologies or establishing conventions for a project — document as mini-ADRs with options and rationale
- Building or extending a design system with shared components — define the component API, styling strategy, and accessibility contract

## When NOT to Use

- Single-component styling changes or minor UI tweaks — edit the component directly without architectural overhead
- Backend API or server-side concerns — use `backend-architect` instead
- When designing user flows and interaction patterns from scratch — start with `ux-designer` to define the UX first
- When E2E testing the UI — use `e2e-test-specialist` instead
- When the existing architecture is well-established and the change follows an existing pattern — replicate the existing pattern

## Core Principles (ALWAYS APPLY)

1. **Component Single Responsibility** — Every component does ONE thing. If a component has more than 3 reasons to change, split it. **[Enforcement]:** If a component exceeds 150 lines of logic (excluding styles), it must be decomposed. Open a refactoring ticket.

2. **Props-Only Interface with Type Safety** — All component inputs are explicit props with TypeScript interfaces. No implicit context dependencies, no `**rest` prop forwarding without typing. **[Enforcement]:** `tsc --noEmit` must pass with strict mode on every component file. Any component with a typed interface of `any` prop is rejected at review.

3. **State at the Level That Needs It** — State lives at the lowest common ancestor that actually needs it. No global store for data used in one component; no prop drilling beyond 2 levels without reconsideration. **[Enforcement]:** If a prop passes through 3+ intermediate components without being consumed, stop and either colocate the state or introduce a dedicated store slice.

4. **Accessibility Is Not Optional** — Every interactive component has keyboard support, focus management, and an accessible name. There is no "we will add accessibility later" — it's part of the component definition. **[Enforcement]:** axe-core must report 0 critical violations on any page before it is marked as done. A component without keyboard handling is a blocking issue.

5. **Performance Is a Design Constraint** — Bundle size, render frequency, and load time are considered at design time, not patched in later. Know your bundle budget before you start. **[Enforcement]:** If a page exceeds its bundle budget by >10%, it is a blocking issue. Use `webpack-bundle-analyzer` or `source-map-explorer` before merging.

## Instructions

### Step 0: Pre-Flight (MANDATORY)

1. Verify that `ux-designer` has already defined the user flows if this is a new feature (if not, start there)
2. Check the existing component library and design system for reusable patterns before creating new components
3. Review the bundle size budget for the project (check `bundlesize.config.json` or equivalent)
4. Assess: is this a new architecture (full design), an extension (add to existing), or a refactor (improve existing)?

### Step 1: Component Decomposition

**Goal:** Decompose the UI into atomic design levels with clear responsibilities.

**Expected output:** Component tree diagram showing atomic levels (atoms → molecules → organisms → templates → pages) with names and responsibilities.

**Tools to use:** Read (existing component library), glob (find existing patterns).

1. Start from the wireframes / user flows (from `ux-designer`)
2. Identify the smallest reusable elements (atoms): Button, Input, Icon, Typography, Spinner
3. Combine atoms into molecules: SearchBar (Input + Button), FormField (Label + Input + ErrorText)
4. Combine molecules into organisms: Header (Logo + SearchBar + Nav), ProductCard (Image + Title + Price + Button)
5. Define templates: page layouts without specific content (MainLayout, AuthLayout)
6. Define pages: templates with actual data (Home, Dashboard, ProductDetail)

**Verification gate:** Every component is assigned to exactly one atomic level. No component straddles two levels.

### Step 2: State Management Selection

**Goal:** Decide the state management strategy per component/data scope and document it.

**Expected output:** State management map listing each piece of state, its scope (local/server/global), and the chosen tool.

**Tools to use:** grep (find existing state patterns in the codebase).

1. Classify each data flow: local (component-only), shared (across sibling components), server (API-fetched), global (app-wide)
2. Match to tool: local → `useState`/`useReducer`, server → React Query/SWR, global → Zustand/Redux/Context
3. Document the decision: one sentence per state entry explaining why that level is appropriate
4. Verify: no global store for component-local state; no server state duplicated in local state

**Verification gate:** State management map exists covering every non-trivial piece of state on the page. No state is managed at the wrong level.

### Step 3: Responsive Layout Design

**Goal:** Define the responsive behaviour at every breakpoint.

**Expected output:** Breakpoint matrix: for each component, how it renders at sm (640px), md (768px), lg (1024px), xl (1280px).

**Tools to use:** Read (UX design specs).

1. Start mobile-first: design the single-column layout first
2. Add breakpoints incrementally: `sm` (add 2-column grid), `md` (add sidebar), `lg` (full desktop layout)
3. Use container queries for self-contained components (cards, panels) — not just viewport media queries
4. Test each breakpoint in browser devtools

**Verification gate:** The page renders correctly at all breakpoints (mobile, tablet, desktop). No content is hidden at any supported width. No horizontal scroll.

### Step 4: Performance & Accessibility Audit

**Goal:** Verify the component tree meets performance budget and accessibility standards.

**Expected output:** Performance audit report + accessibility audit report.

**Tools to use:** browser devtools (Performance tab), axe-core or equivalent, `source-map-explorer`.

**Verification gate:** Bundle size within 5% of budget, 0 critical a11y violations, 0 render performance issues in React DevTools Profiler.

## Component Architecture

### Atomic Design Structure

```
src/
├── components/
│   ├── atoms/           # Basic building blocks
│   │   ├── Button/
│   │   ├── Input/
│   │   └── Typography/
│   ├── molecules/       # Combinations of atoms
│   │   ├── SearchBar/
│   │   ├── FormField/
│   │   └── Card/
│   ├── organisms/       # Complex components
│   │   ├── Header/
│   │   ├── ProductList/
│   │   └── CheckoutForm/
│   ├── templates/       # Page layouts
│   │   ├── MainLayout/
│   │   └── AuthLayout/
│   └── pages/           # Actual pages
│       ├── Home/
│       └── Dashboard/
```

### Component Template (TypeScript + React)

```typescript
// Button.tsx
import { FC, ButtonHTMLAttributes } from 'react';
import { cn } from '@/utils/cn';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className,
  children,
  disabled,
  ...props
}) => {
  return (
    <button
      className={cn(
        'rounded font-medium transition-colors',
        {
          'bg-blue-500 text-white hover:bg-blue-600': variant === 'primary',
          'bg-gray-200 text-gray-800 hover:bg-gray-300': variant === 'secondary',
          'bg-red-500 text-white hover:bg-red-600': variant === 'danger',
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
          'opacity-50 cursor-not-allowed': disabled || isLoading,
        },
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <Spinner size="sm" /> : children}
    </button>
  );
};
```

### Component ADR Template

```markdown
# ADR-UI-[N]: [Component Name] Design Decision

## Status

[Proposed | Accepted | Deprecated]

## Context

What user need does this component satisfy? What existing components did we consider reusing?

## API Design

- Props interface (TypeScript):
- Styling strategy (CSS Modules / Tailwind / Styled Components):
- Accessibility contract: keyboard, focus, screen reader behaviour

## Options Considered

### Option 1: [Approach A]
- **Pros:** [List]
- **Cons:** [List]

### Option 2: [Approach B]
- **Pros:** [List]
- **Cons:** [List]

## Decision

Chosen: **Option 1**

**Rationale:** [Why this approach]

## Performance Implications

- Estimated bundle size impact: [X] KB
- Render frequency: [stable on every prop change / memoized]
- Code splitting strategy: [eager / lazy-loaded]
```

## State Management

### Local State

```typescript
// useState for simple state
const [count, setCount] = useState(0);

// useReducer for complex state
const [state, dispatch] = useReducer(reducer, initialState);
```

### Global State (Zustand)

```typescript
import { create } from "zustand";

interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

### Server State (React Query)

```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// Fetching data
const { data, isLoading, error } = useQuery({
  queryKey: ["users", userId],
  queryFn: () => fetchUser(userId),
});

// Mutations
const queryClient = useQueryClient();
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["users"] });
  },
});
```

## Responsive Design

### Breakpoints

```css
/* Tailwind-like breakpoints */
sm: 640px   /* Small devices */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large screens */
```

### Mobile-First Approach

```tsx
<div
  className="
  grid
  grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
  gap-4
"
>
  {items.map((item) => (
    <Card key={item.id} {...item} />
  ))}
</div>
```

### Container Queries

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

## Performance Patterns

### Code Splitting

```typescript
// Dynamic import
const Dashboard = lazy(() => import("./pages/Dashboard"));

// Route-based splitting
const routes = [
  { path: "/", component: lazy(() => import("./pages/Home")) },
  { path: "/dashboard", component: lazy(() => import("./pages/Dashboard")) },
];
```

### Memoization

```typescript
// useMemo for expensive calculations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// useCallback for function references
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// React.memo for component memoization
const ListItem = memo(({ item }: { item: Item }) => {
  return <div>{item.name}</div>;
});
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|-----------|-------------|----------|
| Rendering user-provided HTML via `dangerouslySetInnerHTML` without sanitization | Unsanitized HTML allows stored XSS attacks that execute in the victim's browser session with full application permissions | Add DOMPurify or similar sanitizer before `dangerouslySetInnerHTML`; run `npm audit` to verify the sanitizer library has no known CVEs |
| Importing the entire utility library (e.g., `import _ from 'lodash'`) when only one function is needed | Tree-shaking cannot eliminate unused exports from CommonJS modules, bloating the initial bundle and increasing TTI | Switch to direct subpath imports (`import merge from 'lodash/merge'`) or replace with native ES alternatives |
| Performing data fetching inside `useEffect` without an abort controller | A component that unmounts before the fetch completes will call `setState` on an unmounted component, producing memory leaks and stale state | Add an `AbortController` and clean up in the `useEffect` return function, or use React Query/SWR which handles this automatically |

## Verification

Before marking any frontend architecture task as complete:

### Self-Verification Checklist

- [ ] `tsc --noEmit` passes with 0 strict mode errors on all changed files — no `any` types in component props
- [ ] Bundle size is within 5% of the pre-change baseline (verified with `source-map-explorer` or `webpack-bundle-analyzer`)
- [ ] 0 critical accessibility violations reported by axe-core on all changed pages/components
- [ ] Component tree follows Atomic Design hierarchy (atoms → molecules → organisms → templates → pages)
- [ ] Global state is managed through a dedicated store (Zustand/Redux) — no prop drilling beyond 2 levels
- [ ] Server state (API data) uses a data-fetching library (React Query, SWR) with loading/error states handled
- [ ] All interactive components have WCAG 2.1 AA-compliant keyboard navigation and focus indicators

### Quality Gates

| Gate | Criteria | Fail Action |
|------|----------|-------------|
| Bundle Size | ≤ budget + 5% | Profile with source-map-explorer, identify large dependencies, code-split or replace |
| Accessibility | 0 critical axe-core violations | Fix each violation by adding proper roles, labels, and keyboard handlers |
| Component Separation | No component > 150 logic lines | Decompose into sub-components; each component has a single responsibility |

## Performance & Cost

### Model Selection

| Task Complexity | Recommended Model | Estimated Tokens |
|----------------|------------------|-----------------|
| Single component design | Fast reasoning model | 2K-5K |
| Full page architecture with state management | Deep reasoning model | 8K-15K |
| Design system / multi-page architecture | Deep reasoning model | 15K-30K |

### Context Budget

- **Expected context usage:** 3K-10K tokens per architecture session
- **When to context-optimize:** When analysing 5+ component decomposition options in one session
- **Context recovery:** Archive component ADRs to `docs/adr/ui/` and clear working context between pages

## Examples

### Example 1: Product Listing Page Architecture

**User request:**
```
Design the component architecture for a product listing page with filtering, sorting, pagination, and product cards.
```

**Skill execution:**

1. **Component Decomposition:**
   - Atoms: ProductImage, Price, Rating, Badge
   - Molecules: ProductCard (Image + Price + Rating + Title), FilterDropdown, SortSelect, PaginationBar
   - Organisms: ProductGrid (ProductCard collection), FilterSidebar
   - Template: ShopLayout (Filter + Grid + Pagination)
2. **State Management:**
   - Server state (React Query): product list, filter options, sort order
   - URL state: current page, active filters, sort — stored in URL search params
   - No global state needed — local to this page
3. **Responsive:** Single column on mobile, 2 columns tablet, 3-4 columns desktop

**Result:** Component tree + state management map + responsive breakpoint matrix. 0 new global state dependencies needed.

### Example 2: State Management Migration

**User request:**
```
Our checkout form has 12 fields spread across 3 steps. State is passed through Context and it's getting messy. Fix the architecture.
```

**Skill execution:**

1. **Assessment:** Context currently holds form state AND validation state AND submission state — 3 unrelated concerns in one provider
2. **Decomposition:**
   - Form field state → `useReducer` colocated in the checkout organism
   - Validation state → derived from field state, not stored separately
   - Submission state → React Query mutation
3. **Result:** Removed the global Context, replaced with colocated reducer + URL step tracking. 40% fewer re-renders on the parent page.

**Result:** State management map updated. Checkout form is self-contained and testable without a wrapping provider.

### Example 3: Edge Case — Third-Party Component Integration

**User request:**
```
We need a rich text editor. The leading library requires direct DOM manipulation. How do we integrate it without breaking React's virtual DOM?
```

**Skill execution:**

1. **Contract Analysis:** The editor library directly modifies DOM nodes that React manages — this causes React to overwrite user edits on re-render
2. **Architecture Decision:** Create a wrapper component that:
   - Initializes the editor in a `useEffect` (after mount, DOM exists)
   - Prevents React from re-rendering the container (memo + `dangerouslySetInnerHTML` for output only)
   - Exposes a controlled `value`/`onChange` interface that maps to the library's API
3. **Verification:** Type in the editor, trigger a parent re-render, verify cursor position preserved

**Result:** ADR for the rich-text wrapper documenting the controlled/uncontrolled boundary, the re-render prevention strategy, and the XSS sanitization applied to output.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Bundling vendor libraries with the application chunk without code splitting | A single dependency update forces all users to re-download the entire bundle, nullifying long-term caching of stable vendor code | Extract vendor libraries into a separate chunk (`SplitChunksPlugin` or manual `React.lazy`). Vendor code changes far less often than app code. |
| Skipping accessible name attributes (`aria-label`, `alt`, `<label for>`) on interactive elements | Screen readers announce the raw element type with no context, making the interface unusable for keyboard and assistive technology users | Every interactive element must have an accessible name. Use `aria-label` if no visible label exists; always associate `<label>` with form controls. |
| Setting a hard pixel width on a flex/grid container without a `max-width` constraint | On viewports wider than the design target, the layout stretches beyond readable line lengths, breaking intended visual hierarchy | Use `max-width` with a readable measure (60-80ch for text content) or design with `max-width: container` at the layout level. |

## References

### Internal Dependencies

- `ux-designer` — Provides wireframes and user flows that feed into Step 1 component decomposition; invoke before frontend-architect for new features
- `code-polisher` — Used after architecture is implemented to clean up component code
- `test-genius` — Used for writing component tests after architecture is in place
- `performance-profiler` — Used when bundle size exceeds budget or render performance needs analysis

### External Standards

- [Atomic Design Methodology (bradfrost.com)](https://bradfrost.com/blog/post/atomic-web-design/) — The component hierarchy pattern used in this skill
- [WCAG 2.1 AA (w3.org)](https://www.w3.org/TR/WCAG21/) — Accessibility standard for all interactive components
- [React Design Patterns and Best Practices](https://www.patterns.dev/react/) — Reference patterns for React component design

### Related Skills

- `ux-designer` — Precedes this skill: UX defines user flows, frontend-architect implements them as components
- `e2e-test-specialist` — Follows this skill: after components are built, E2E tests verify flow
- `backend-architect` — Parallel concern: frontend architect defines API contracts in collaboration with backend architect

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-09 | Gold standard upgrade: added version/category/dependencies frontmatter, Core Principles with enforcement, 4-step Instructions workflow, Component ADR template, Blocking Violations table, Performance & Cost, Examples (3), References, Changelog |
| 1.0.0 | 2025-06-01 | Initial version |
