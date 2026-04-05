---
name: workflow-orchestrator
compatibility: Antigravity, Claude Code, GitHub Copilot
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

## When NOT to Use

- Simple single-skill tasks that don't require coordination across multiple steps or services — invoke the relevant skill directly
- When a linear script or cron job suffices — full workflow orchestration is overhead for simple sequential jobs
- Real-time event handling with sub-second latency requirements — Temporal/orchestration adds latency overhead
- When the "workflow" is just 2-3 API calls in sequence — implement it directly in the service layer

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

## Self-Verification Checklist

- [ ] All saga steps have compensation registered: `grep -rn "compensat\|rollback\|undo" <workflow_code>` returns >= number of steps that mutate external state — steps with mutation but no compensation are a blocking failure
- [ ] Dead-letter queue alert configured and tested: DLQ size metric alert exists in monitoring config; `grep -rn "DLQ\|dead.letter\|deadLetter" <monitoring_config>` returns at least 1 match with a numeric threshold
- [ ] Orchestrator replica count >= 2: `grep -n "replicas:" <deployment_manifest>` returns a value >= 2 — single-replica orchestrators fail this check; `kubectl get deployment <name> -o jsonpath='{.spec.replicas}'` returns >= 2
- [ ] All workflow steps are idempotent: `grep -rn "idempotent\|idempotency.key\|dedup" <workflow_code>` returns at least 1 match per step that calls an external API — steps without idempotency keys fail
- [ ] Retry policies specify max attempts and delay strategy: `grep -rn "maxAttempts\|max_retries\|retryable\|backoff" <workflow_config>` returns at least 1 match per step — open-ended retries without limits fail this check
- [ ] Workflow state persisted: `grep -rn "persist\|checkpoint\|saveState\|store" <orchestrator_code>` returns at least 1 match — in-memory-only state fails; process restart test exits 0 and workflow resumes from last checkpoint

This task is complete when:
1. The workflow executes successfully end-to-end in a test environment with all happy-path steps passing
2. Failure injection testing confirms compensation logic runs correctly when any single step fails
3. The workflow is observable: each step emits start/complete/error events that appear in the monitoring dashboard

## Anti-Patterns

- Never start a parallel workflow without defining a join condition because parallel branches that have no explicit join point run to completion independently and the orchestrator has no signal for when the aggregate is done, causing downstream steps to start prematurely or never start.
- Never orchestrate steps that share mutable state without explicit locking because two concurrent steps reading and writing the same state field will produce race conditions whose outcome depends on scheduling order, making failures non-deterministic and hard to reproduce.
- Never treat a timed-out step as failed without checking for partial completion because a step that timed out may have already mutated external state (e.g., charged a card, reserved inventory); retrying without checking for partial completion causes duplicate side effects.
- Never define a workflow without an explicit terminal state because a workflow with no defined end condition can loop, stall, or accumulate running instances indefinitely, exhausting resources and making observability impossible.
- Never retry a non-idempotent step automatically because an automatic retry of a step that is not idempotent (e.g., sends an email, charges a payment) executes the side effect multiple times, causing data corruption or duplicate user-facing actions.
- Never orchestrate without logging each step's start, end, and output because a workflow with no per-step log produces no forensic trail; when a step fails mid-workflow the only way to diagnose it is to re-run the entire workflow from the beginning.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Saga compensation step fails, leaving distributed system in inconsistent state | Compensation function throws an uncaught error; partial rollback leaves inventory released but payment not refunded | Wrap every compensation step in its own retry with exponential backoff; log compensation failures to a dead-letter queue for manual resolution |
| Workflow state corrupted by concurrent update from two orchestrator instances | Two orchestrator pods process the same workflow event simultaneously; no optimistic locking on state updates | Use optimistic locking (version field) or distributed lock (Redis SETNX) on workflow state updates; configure Temporal/equivalent for exclusive execution |
| Dead-letter queue overflows because poison-pill message never acknowledged | One malformed message loops through retry indefinitely; DLQ fills; real failures stop alerting | Set a max-retry limit per message type; add a DLQ size alert at 80% capacity; auto-quarantine messages that exceed retry budget |
| Orchestrator is single point of failure; worker nodes healthy but idle | Orchestrator deployed as a single replica with no health check; workers wait for tasks that never arrive | Run orchestrator with ≥2 replicas behind a load balancer; add a liveness probe that fails if the task queue depth grows beyond threshold |
| Step retry without idempotency key causes duplicate side effects | Step issues an external API call without an idempotency key; retry sends the call twice; payment charged twice | Every step that mutates external state must include an idempotency key derived from the workflow ID and step name; verify by inspecting API call logs |

## Self-Verification Checklist

- [ ] All saga steps have compensation registered: `grep -rn "compensat\|rollback\|undo" <workflow_code>` returns >= number of steps that mutate external state — steps with mutation but no compensation are a blocking failure
- [ ] Dead-letter queue alert configured and tested: DLQ size metric alert exists in monitoring config; `grep -rn "DLQ\|dead.letter\|deadLetter" <monitoring_config>` returns at least 1 match with a numeric threshold
- [ ] Orchestrator replica count >= 2: `grep -n "replicas:" <deployment_manifest>` returns a value >= 2 — single-replica orchestrators fail this check; `kubectl get deployment <name> -o jsonpath='{.spec.replicas}'` returns >= 2
- [ ] All workflow steps are idempotent: `grep -rn "idempotent\|idempotency.key\|dedup" <workflow_code>` returns at least 1 match per step that calls an external API — steps without idempotency keys fail
- [ ] Retry policies specify max attempts and delay strategy: `grep -rn "maxAttempts\|max_retries\|retryable\|backoff" <workflow_config>` returns at least 1 match per step — open-ended retries without limits fail this check
- [ ] Workflow state persisted: `grep -rn "persist\|checkpoint\|saveState\|store" <orchestrator_code>` returns at least 1 match — in-memory-only state fails; process restart test exits 0 and workflow resumes from last checkpoint

## Tips

- Use idempotent operations for reliability
- Implement proper compensation logic
- Handle long-running workflows with state persistence
- Monitor workflow execution
- Set appropriate timeouts
