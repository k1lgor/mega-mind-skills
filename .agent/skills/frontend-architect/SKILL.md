---
name: frontend-architect
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
