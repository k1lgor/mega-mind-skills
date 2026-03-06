---
name: workflow-orchestrator
description: Complex task scheduling and orchestration. Use for workflow automation tasks.
triggers:
  - "workflow automation"
  - "task orchestration"
  - "scheduling"
  - "workflow engine"
---

# Workflow Orchestrator Skill

## Identity

You are a workflow orchestration specialist focused on automating complex task sequences.

## When to Use

- Building workflow automation
- Task scheduling
- Process orchestration
- Event-driven systems

## Workflow Patterns

### Sequential Workflow

```
Task A → Task B → Task C → Task D
```

### Parallel Workflow

```
       ┌── Task B ──┐
Task A ├── Task C ──┼── Task E
       └── Task D ──┘
```

### Conditional Workflow

```
Task A → Decision → Task B (if condition)
                 → Task C (else)
```

## Implementation

### Temporal Workflow

```typescript
// workflows/order-workflow.ts
import { proxyActivities } from "@temporalio/workflow";
import type * as activities from "../activities";

const {
  validateOrder,
  reserveInventory,
  processPayment,
  shipOrder,
  notifyCustomer,
} = proxyActivities<typeof activities>({
  startToCloseTimeout: "1 minute",
});

export async function processOrder(orderId: string): Promise<OrderResult> {
  // Step 1: Validate
  const order = await validateOrder(orderId);
  if (!order.valid) {
    throw new Error("Invalid order");
  }

  // Step 2: Reserve inventory
  const reservation = await reserveInventory(order.items);
  if (!reservation.success) {
    throw new Error("Inventory not available");
  }

  try {
    // Step 3: Process payment
    const payment = await processPayment(order.paymentInfo);
    if (!payment.success) {
      throw new Error("Payment failed");
    }

    // Step 4: Ship order
    const shipment = await shipOrder(orderId, reservation.id);

    // Step 5: Notify customer
    await notifyCustomer(order.customerId, {
      type: "order_confirmed",
      orderId,
      trackingNumber: shipment.trackingNumber,
    });

    return { success: true, orderId, trackingNumber: shipment.trackingNumber };
  } catch (error) {
    // Compensating transaction: release inventory
    await releaseInventory(reservation.id);
    throw error;
  }
}
```

### Workflow with Saga Pattern

```typescript
// workflows/saga-workflow.ts
export async function processOrderWithCompensation(orderId: string) {
  const compensations: (() => Promise<void>)[] = [];

  try {
    // Step 1: Create order
    const order = await createOrder(orderId);
    compensations.push(async () => cancelOrder(orderId));

    // Step 2: Reserve inventory
    const reservation = await reserveInventory(order.items);
    compensations.push(async () => releaseInventory(reservation.id));

    // Step 3: Process payment
    const payment = await processPayment(order.payment);
    compensations.push(async () => refundPayment(payment.id));

    // Step 4: Create shipment
    const shipment = await createShipment(orderId);
    compensations.push(async () => cancelShipment(shipment.id));

    return { success: true };
  } catch (error) {
    // Execute compensations in reverse order
    for (const compensate of compensations.reverse()) {
      try {
        await compensate();
      } catch (compensationError) {
        console.error("Compensation failed:", compensationError);
      }
    }
    throw error;
  }
}
```

## Task Scheduling

### Cron-based Scheduling

```typescript
// scheduler.ts
import { CronJob } from "cron";

const jobs = {
  // Daily report at midnight
  dailyReport: new CronJob(
    "0 0 * * *",
    async () => {
      await generateDailyReport();
    },
    null,
    true,
    "America/New_York",
  ),

  // Every hour
  hourlySync: new CronJob("0 * * * *", async () => {
    await syncData();
  }),

  // Every Monday at 9 AM
  weeklyCleanup: new CronJob("0 9 * * 1", async () => {
    await cleanupOldData();
  }),
};

// Start all jobs
Object.values(jobs).forEach((job) => job.start());
```

### Event-Driven Orchestration

```typescript
// event-orchestrator.ts
import { EventEmitter } from "events";

class WorkflowOrchestrator extends EventEmitter {
  async executeWorkflow(workflowId: string, input: any) {
    const workflow = await this.loadWorkflow(workflowId);
    const context = { input, state: {}, events: [] };

    for (const step of workflow.steps) {
      this.emit("step:start", { workflowId, step: step.name });

      try {
        const result = await this.executeStep(step, context);
        context.state[step.name] = result;

        this.emit("step:complete", { workflowId, step: step.name, result });

        // Check for conditional branching
        if (step.branch) {
          const nextStep = step.branch[result.status];
          if (nextStep) {
            workflow.steps = this.insertSteps(workflow.steps, nextStep);
          }
        }
      } catch (error) {
        this.emit("step:error", { workflowId, step: step.name, error });

        if (step.retry && step.retry.count < step.retry.maxRetries) {
          await this.delay(step.retry.delay);
          step.retry.count++;
          continue;
        }

        if (step.compensate) {
          await this.executeCompensation(step.compensate, context);
        }

        throw error;
      }
    }

    return context.state;
  }
}

// Usage
const orchestrator = new WorkflowOrchestrator();

orchestrator.on("step:start", ({ workflowId, step }) => {
  console.log(`Starting ${step} in ${workflowId}`);
});

orchestrator.on("step:error", ({ workflowId, step, error }) => {
  console.error(`Error in ${step}: ${error.message}`);
});

await orchestrator.executeWorkflow("order-processing", { orderId: "123" });
```

## Retry Strategies

```typescript
// retry.ts
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries: number;
    delay: number;
    backoff?: "linear" | "exponential";
    maxDelay?: number;
  },
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= options.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < options.maxRetries) {
        const delay =
          options.backoff === "exponential"
            ? Math.min(
                options.delay * Math.pow(2, attempt),
                options.maxDelay || Infinity,
              )
            : options.delay;

        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// Usage
const result = await withRetry(() => fetchFromExternalAPI(), {
  maxRetries: 3,
  delay: 1000,
  backoff: "exponential",
  maxDelay: 30000,
});
```

## Tips

- Use idempotent operations for reliability
- Implement proper compensation logic
- Handle long-running workflows with state persistence
- Monitor workflow execution
- Set appropriate timeouts
