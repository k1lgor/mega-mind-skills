---
name: doc-writer
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
npm install my-project
\`\`\`

## Installation

\`\`\`bash
git clone https://github.com/user/project.git
cd project
npm install
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
