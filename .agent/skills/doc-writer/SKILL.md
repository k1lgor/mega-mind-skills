---
name: doc-writer
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Generating docs, READMEs, and inline comments. Use for all documentation needs.
triggers:
  - "write documentation"
  - "document this"
  - "create a README"
  - "add comments"
---

# Doc Writer Skill

## Identity

You are a technical writer specializing in clear, comprehensive documentation for software projects.

## When to Use

- Creating README files
- Writing API documentation
- Adding inline code comments
- Creating user guides
- Documenting architecture

## When NOT to Use

- The code being documented is not finalized and likely to change significantly — doc written on unstable code becomes stale immediately
- API endpoints are not yet implemented or are in active redesign — use `api-designer` to finalize the contract first
- You need to add tests or fix behavior — documentation does not substitute for tests or correct behavior
- Internal implementation comments that would be better served by cleaner, self-documenting code — refactor first

## Documentation Types

### 1. README.md

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2

## Quick Start

\`\`\`bash
bun install (or npm install) my-project
\`\`\`

## Installation

\`\`\`bash
git clone https://github.com/user/project.git
cd project
bun install (or npm install)
\`\`\`

## Usage

\`\`\`javascript
import { something } from 'my-project';

something.doThing();
\`\`\`

## API Reference

### `functionName(param1, param2)`

Description of what the function does.

**Parameters:**

- `param1` (Type): Description
- `param2` (Type): Description

**Returns:** Type - Description

**Example:**
\`\`\`javascript
const result = functionName('value', 123);
\`\`\`

## Configuration

| Option  | Type   | Default   | Description |
| ------- | ------ | --------- | ----------- |
| option1 | string | 'default' | Description |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

### 2. API Documentation

```markdown
# API Documentation

## Authentication

All API requests require authentication via Bearer token.

\`\`\`
Authorization: Bearer <token>
\`\`\`

## Endpoints

### GET /api/users

Retrieve all users.

**Parameters:**
| Name | Type | In | Required | Description |
|------|------|-----|----------|-------------|
| page | integer | query | No | Page number (default: 1) |
| limit | integer | query | No | Items per page (default: 20) |

**Response:**
\`\`\`json
{
"data": [
{
"id": 1,
"name": "John Doe",
"email": "john@example.com"
}
],
"meta": {
"total": 100,
"page": 1,
"limit": 20
}
}
\`\`\`

**Status Codes:**
| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 500 | Server Error |

### POST /api/users

Create a new user.

**Request Body:**
\`\`\`json
{
"name": "John Doe",
"email": "john@example.com",
"password": "securepassword"
}
\`\`\`

**Response:**
\`\`\`json
{
"id": 1,
"name": "John Doe",
"email": "john@example.com",
"createdAt": "2024-01-15T10:00:00Z"
}
\`\`\`
```

### 3. Inline Comments

```typescript
/**
 * Calculates the total price for an order including taxes and discounts.
 *
 * @param items - Array of order items with price and quantity
 * @param options - Optional configuration for tax rate and discount
 * @returns The total price rounded to 2 decimal places
 *
 * @example
 * const total = calculateTotal(
 *   [{ price: 10, quantity: 2 }],
 *   { taxRate: 0.1, discount: 5 }
 * );
 * // Returns: 17.00 (20 + 2 tax - 5 discount)
 */
export function calculateTotal(
  items: OrderItem[],
  options?: CalculationOptions,
): number {
  // Calculate subtotal from items
  const subtotal = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  // Apply tax if rate is provided
  const tax = options?.taxRate ? subtotal * options.taxRate : 0;

  // Apply discount if provided
  const discount = options?.discount ?? 0;

  // Calculate final total and round to 2 decimal places
  return Math.round((subtotal + tax - discount) * 100) / 100;
}
```

### 4. Architecture Documentation

```markdown
# System Architecture

## Overview

This document describes the high-level architecture of our system.

## Components

### Frontend (Next.js)

- **Purpose**: User interface and client-side logic
- **Technology**: Next.js 14, React, TypeScript
- **Deployment**: Vercel

### Backend API (Node.js)

- **Purpose**: Business logic and data access
- **Technology**: Node.js, Express, TypeScript
- **Deployment**: AWS ECS

### Database (PostgreSQL)

- **Purpose**: Primary data store
- **Technology**: PostgreSQL 15
- **Deployment**: AWS RDS

## Data Flow

1. User interacts with Frontend
2. Frontend makes API requests to Backend
3. Backend processes requests and queries Database
4. Response flows back to Frontend

## Diagrams

[Architecture diagram here]
```

## Documentation Principles

1. **Clear and Concise** - Get to the point quickly
2. **Example-Driven** - Show, don't just tell
3. **Up-to-Date** - Keep docs synchronized with code
4. **Audience-Aware** - Write for the reader's level
5. **Searchable** - Use clear headings and keywords

## Tips

- Write documentation as you code
- Update docs when changing behavior
- Use consistent formatting
- Include practical examples
- Test your code examples

## Anti-Patterns

- Never document a function without a runnable code example because developers copy-paste signatures and discover missing context only at runtime.
- Never publish docs generated from a stale snapshot because parameter names diverge from the live API and callers pass wrong arguments.
- Never mark a parameter as optional in docs when the implementation requires it because callers omit it and receive cryptic runtime errors.
- Never skip linking to related functions because developers miss the canonical usage pattern and implement workarounds that duplicate existing functionality.
- Never omit error return documentation because callers do not handle errors they do not know exist, causing silent data corruption or unhandled exceptions in production.
- Never write docs for the implementer's mental model instead of the caller's mental model because the caller does not have the implementation context and cannot infer usage from internals.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Code example in docs doesn't compile against current API version | Example was written for an older API version and not updated when the API changed | Run all code examples through the actual compiler/interpreter; fix any that exit non-zero; add a CI step to run doc examples on every API change |
| Parameter names in docs don't match function signatures | Docs were copied from a draft signature that was later renamed during implementation | Run `grep` to diff documented param names against actual function signatures; update docs to match source of truth |
| Docs generated from stale snapshot, diverged from live code | Generated docs (TypeDoc, Sphinx, etc.) last ran against a commit that predates recent refactors | Re-run the doc generator against the current HEAD; commit the regenerated output; add doc generation to the CI pipeline |
| Missing required parameter documented as optional | Parameter was made required during a refactor but the docs still show `(optional)` | Audit all `@param` annotations for required fields; cross-reference with function signatures; update optionality markers |
| Changelog entry references wrong PR number | Entry copy-pasted from a previous release and the PR number not updated | Verify each changelog PR link resolves to the correct PR; run a link-check script that exits non-zero on broken GitHub PR URLs |

## Self-Verification Checklist

- [ ] All code examples compile/run without error: execute each example in isolation and confirm exit code 0
- [ ] All parameter names match live function signatures: `grep` documented param names against source and confirm 0 mismatches
- [ ] No broken internal links: link checker (e.g., `markdown-link-check`) exits 0 with 0 broken links reported
- [ ] All public functions/methods have JSDoc or equivalent docstrings with `@param`, `@returns`, and at least one `@example`
- [ ] README Quick Start instructions are tested by following them literally in a clean environment and produce the expected result
- [ ] API documentation matches the actual implemented endpoint signatures (no documented fields that don't exist)
- [ ] No documentation references internal implementation details that users or API consumers don't need to know

## Success Criteria

This task is complete when:
1. A developer unfamiliar with the codebase can follow the documentation to accomplish the primary use case without asking questions
2. All public API surface area has documented parameters, return values, and at least one usage example
3. Documentation is co-located with or linked from the code it describes (no orphaned docs)
