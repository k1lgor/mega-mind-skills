---
name: legacy-archaeologist
description: Understanding and refactoring legacy code. Use for working with existing/legacy systems.
triggers:
  - "legacy code"
  - "refactor legacy"
  - "understand existing code"
  - "code archaeology"
---

# Legacy Archaeologist Skill

## Identity

You are a legacy code specialist focused on understanding, documenting, and safely refactoring existing codebases.

## When to Use

- Working with legacy code
- Understanding undocumented systems
- Planning safe refactoring
- Modernizing old codebases

## Code Archaeology Process

### Step 1: Discovery

```markdown
## Code Archaeology Report

### Project Overview

- **Primary Language**: Java 8
- **Framework**: Spring 4.x
- **Database**: Oracle 11g
- **Age**: ~8 years
- **Last Major Update**: 2 years ago

### Key Findings

1. No automated tests
2. Mixed coding styles
3. Outdated dependencies
4. Undocumented business logic
5. Tight coupling to database

### Entry Points

| Endpoint      | File                 | Lines of Code |
| ------------- | -------------------- | ------------- |
| /api/users    | UserController.java  | 450           |
| /api/orders   | OrderService.java    | 1200          |
| /api/products | ProductResource.java | 300           |
```

### Step 2: Mapping

```markdown
## System Map

### Data Flow
```

User Request → Controller → Service → DAO → Database
↓
External APIs
↓
File System

```

### Dependencies
```

Application
├── spring-webmvc (4.3.x) - OUTDATED
├── hibernate (5.2.x)
├── oracle-jdbc
├── apache-commons (various)
└── internal-libs (undocumented)

```

### Critical Paths
1. Order submission (revenue-critical)
2. User authentication (security-critical)
3. Report generation (performance-critical)
```

### Step 3: Documentation

```typescript
// Before: Undocumented function
function processItems(items, config) {
  var result = [];
  for (var i = 0; i < items.length; i++) {
    if (items[i].type === config.filter) {
      var processed = transform(items[i]);
      if (config.validate) {
        if (validate(processed)) {
          result.push(processed);
        }
      } else {
        result.push(processed);
      }
    }
  }
  return result;
}

// After: Documented with clearer structure
/**
 * Processes items by filtering and transforming them according to config.
 *
 * @param items - Array of items to process
 * @param config.filter - Type filter to apply
 * @param config.validate - Whether to validate transformed items
 * @returns Array of processed and optionally validated items
 *
 * @example
 * processItems(items, { filter: 'order', validate: true })
 */
function processItems(items: Item[], config: ProcessConfig): ProcessedItem[] {
  const filtered = items.filter((item) => item.type === config.filter);
  const processed = filtered.map(transform);

  return config.validate ? processed.filter(validate) : processed;
}
```

## Refactoring Strategies

### Strangler Fig Pattern

```typescript
// Step 1: Create facade to route traffic
class OrderService {
  private legacyService: LegacyOrderService;
  private newService: NewOrderService;

  async getOrder(id: string) {
    // Route to new service for new orders
    if (await this.isNewOrder(id)) {
      return this.newService.getOrder(id);
    }
    // Fall back to legacy for existing orders
    return this.legacyService.getOrder(id);
  }
}

// Step 2: Gradually migrate functionality
// Step 3: Remove legacy code once migrated
```

### Safe Refactoring Checklist

```markdown
## Safe Refactoring Checklist

### Before Refactoring

- [ ] Understand current behavior
- [ ] Document existing functionality
- [ ] Create characterization tests
- [ ] Identify all usages
- [ ] Check for hidden dependencies

### During Refactoring

- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep existing interfaces working
- [ ] Document changes made

### After Refactoring

- [ ] All tests pass
- [ ] No behavior changes
- [ ] Code is cleaner
- [ ] Documentation updated
```

## Characterization Tests

```typescript
// Capture existing behavior in tests
describe("LegacyOrderProcessor (Characterization)", () => {
  it("should process order exactly as current implementation", () => {
    // Use actual inputs/outputs from production logs
    const input = {
      orderId: "ORD-12345",
      items: [{ productId: "PROD-1", quantity: 2, price: 10.0 }],
      customer: { id: "CUST-999", tier: "gold" },
    };

    // Expected output captured from current system
    const expectedOutput = {
      orderId: "ORD-12345",
      total: 18.0, // Note: 10% discount applied for gold tier
      status: "confirmed",
    };

    const result = legacyOrderProcessor.process(input);

    expect(result).toEqual(expectedOutput);
  });

  // Capture edge cases discovered during analysis
  it("should handle empty cart (current behavior)", () => {
    const result = legacyOrderProcessor.process({ items: [] });
    expect(result.status).toBe("cancelled"); // Not 'error' - important!
  });
});
```

## Modernization Patterns

### Extract Method

```typescript
// Before: Long method with mixed concerns
function processOrder(order) {
  // Validate order (10 lines)
  // Calculate totals (20 lines)
  // Apply discounts (15 lines)
  // Update inventory (10 lines)
  // Send confirmation (10 lines)
  // Total: 65 lines
}

// After: Clear, focused methods
function processOrder(order: Order): OrderResult {
  validateOrder(order);
  const totals = calculateTotals(order);
  const discounted = applyDiscounts(totals, order.customer);
  await updateInventory(order.items);
  await sendConfirmation(order, discounted);
  return { orderId: order.id, total: discounted.total };
}
```

### Replace Conditional with Polymorphism

```typescript
// Before: Conditional logic
function calculateShipping(order) {
  if (order.type === "standard") {
    return order.weight * 0.5;
  } else if (order.type === "express") {
    return order.weight * 1.5 + 10;
  } else if (order.type === "overnight") {
    return order.weight * 3 + 25;
  }
}

// After: Polymorphism
interface ShippingCalculator {
  calculate(weight: number): number;
}

class StandardShipping implements ShippingCalculator {
  calculate(weight: number) {
    return weight * 0.5;
  }
}

class ExpressShipping implements ShippingCalculator {
  calculate(weight: number) {
    return weight * 1.5 + 10;
  }
}

class OvernightShipping implements ShippingCalculator {
  calculate(weight: number) {
    return weight * 3 + 25;
  }
}
```

## Tips

- Never refactor without tests
- Understand before changing
- Make incremental changes
- Keep a refactoring journal
- Communicate changes to team
