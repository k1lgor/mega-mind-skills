---
name: frontend-architect
compatibility: Antigravity, Claude Code, GitHub Copilot
description: UI, Components, and Responsive Design. Use for frontend architecture decisions.
triggers:
  - "frontend architecture"
  - "component design"
  - "UI architecture"
  - "responsive design"
---

# Frontend Architect Skill

## Identity

You are a frontend architecture specialist focused on component design, state management, and UI patterns.

## When to Use

- Designing component architecture
- Setting up state management
- Planning responsive layouts
- Choosing frontend technologies

## When NOT to Use

- Single-component styling changes or minor UI tweaks — edit the component directly without architectural overhead
- Backend API or server-side concerns — use `backend-architect` instead
- When designing user flows and interaction patterns from scratch — start with `ux-designer` to define the UX first
- When E2E testing the UI — use `e2e-test-specialist` instead

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

### Component Template

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

## Folder Structure

```
src/
├── components/       # Reusable components
├── hooks/            # Custom hooks
├── lib/              # Third-party integrations
├── services/         # API services
├── stores/           # State stores
├── types/            # TypeScript types
├── utils/            # Utility functions
├── styles/           # Global styles
└── pages/            # Page components
```

## Tips

- Keep components small and focused
- Use composition over inheritance
- Implement proper error boundaries
- Optimize for performance
- Maintain consistent naming
- Write tests for critical paths

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Component re-renders on every parent update due to missing memoization | Child component is defined inline or props include new object/array literals on every render | Wrap component with `React.memo`; memoize object/array props with `useMemo`; confirm with React DevTools Profiler that render count drops |
| CSS specificity conflict causing style to silently override | Two rules target the same element with equal or unpredictable specificity; one silently wins | Use browser devtools to identify which rule wins; refactor to BEM, CSS Modules, or scoped utility classes to eliminate the conflict |
| Bundle size regression from unintentional import of full library | `import { one } from 'big-library'` pulls in the entire library because the package lacks tree-shaking | Run `npm run build -- --analyze` (or `source-map-explorer`); identify the offending import; switch to a direct subpath import or a lighter alternative; confirm bundle size is within 5% of baseline |
| Hydration mismatch between SSR and client rendering | Component renders different HTML on server vs client (e.g., reads `window`, `Date.now()`, or random values at render time) | Move non-deterministic reads behind `useEffect` or `typeof window !== 'undefined'` guards; fix all React hydration warnings (0 warnings in console) |
| Accessibility violation: interactive element missing keyboard focus handling | Button or link implemented as `<div onClick>` with no `tabIndex`, `role`, or keyboard event handler | Replace `<div onClick>` with semantic `<button>` or `<a>`; run axe-core and confirm 0 critical violations |

## Anti-Patterns

- Never render user-provided HTML via `dangerouslySetInnerHTML` without sanitization because unsanitized HTML allows stored XSS attacks that execute in the victim's browser session with full application permissions.
- Never import the entire utility library (e.g., `import _ from 'lodash'`) when only one function is needed because tree-shaking cannot eliminate unused exports from CommonJS modules, bloating the initial bundle and increasing Time-to-Interactive.
- Never inline critical-path CSS as large `<style>` blocks generated at runtime via CSS-in-JS without extraction because runtime style injection blocks the main thread during hydration, increasing Cumulative Layout Shift and First Contentful Paint.
- Never skip accessible name attributes (`aria-label`, `alt`, `<label for>`) on interactive elements because screen readers announce the raw element type with no context, making the interface unusable for keyboard and assistive technology users.
- Never perform data fetching inside a `useEffect` without an abort controller or cancellation mechanism because a component that unmounts before the fetch completes will attempt to call `setState` on an unmounted component, producing memory leaks and stale state bugs.
- Never set a hard pixel width on a flex or grid container without a `max-width` constraint because on viewports wider than the design target the layout stretches beyond readable line lengths, breaking the intended visual hierarchy.
- Never bundle vendor libraries with the application chunk without code splitting because a single dependency update forces all users to re-download the entire bundle, nullifying long-term caching of stable vendor code.

## Self-Verification Checklist

- [ ] `lsp_diagnostics` returns 0 errors on all changed files; TypeScript strict mode passes with 0 `any` types in component props
- [ ] Bundle size is within 5% of the pre-change baseline (verified with `source-map-explorer` or `webpack-bundle-analyzer`)
- [ ] 0 critical accessibility violations reported by axe-core (or equivalent) on all changed pages/components
- [ ] Component tree follows Atomic Design hierarchy (atoms → molecules → organisms → templates → pages)
- [ ] Global state is managed through a dedicated store (Zustand/Redux) — no prop drilling beyond 2 levels
- [ ] Server state (API data) uses a data-fetching library (React Query, SWR) with loading/error states handled
- [ ] All interactive components have WCAG 2.1 AA-compliant keyboard navigation and focus indicators

## Success Criteria

This task is complete when:
1. Component architecture is documented with the folder structure and responsibility boundaries defined
2. State management strategy is selected and implemented with no duplicate state across local and global stores
3. Responsive layout renders correctly at sm (640px), md (768px), and lg (1024px) breakpoints
