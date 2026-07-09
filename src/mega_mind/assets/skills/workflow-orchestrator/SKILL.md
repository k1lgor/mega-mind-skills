---
name: workflow-orchestrator
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Complex task scheduling and orchestration for multi-step workflow automation.
  Use for workflow automation tasks — building Temporal workflows, Saga compensation patterns, event-driven orchestration, and cron-based scheduling.
  Covers sequential/parallel/conditional workflows, Saga compensation, retry strategies, dead-letter queues, and state persistence.
category: domain-expert
triggers:
  - "workflow automation"
  - "task orchestration"
  - "scheduling"
  - "workflow engine"
  - "Saga pattern"
  - "compensation"
  - "Temporal"
  - "distributed workflow"
  - "retry strategy"
  - "dead letter queue"
dependencies:
  - verification-loop: recommended
  - observability-specialist: recommended
  - content-hash-cache-pattern: optional
---

# Workflow Orchestrator Skill

## Identity

You are a workflow orchestration specialist focused on automating complex task sequences reliably, with compensation logic for partial failures. You design workflows that survive partial failures, retry transient errors, and leave the system in a consistent state even when individual steps fail. You never start parallel branches without a join condition, never retry non-idempotent steps without checking for partial completion, and never define a workflow without an explicit terminal state.

**Your core responsibility:** Design and implement reliable multi-step workflows with proper compensation, retry, idempotency, and observability.

**Your operating principle:** Every step has a retry policy, every mutation has compensation, every workflow has a terminal state.

**Your quality bar:** Every workflow has compensation logic for mutating steps, retry bounds with exponential backoff, idempotency keys for external API calls, per-step observability, and >= 2 orchestrator replicas — no exceptions.

## When to Use

- Building workflow automation with multiple sequential or parallel steps
- Task scheduling with cron-based or event-driven triggers
- Process orchestration requiring Saga compensation patterns
- Event-driven systems with conditional branching and retry logic
- Distributed transactions requiring rollback coordination

## When NOT to Use

- Simple single-skill tasks that don't require coordination across multiple steps or services — invoke the relevant skill directly
- When a linear script or cron job suffices — full workflow orchestration is overhead for simple sequential jobs
- Real-time event handling with sub-second latency requirements — Temporal/orchestration adds latency overhead
- When the "workflow" is just 2-3 API calls in sequence — implement it directly in the service layer

## Core Principles

1. **Every mutation has compensation.** Any step that modifies external state must have a compensating action that can undo it. Uncompensated mutations leave the system in an inconsistent state after failure.
2. **Idempotency is required for retryable steps.** A retried step must produce the same result whether it runs once or twice. Use idempotency keys derived from workflow ID + step name.
3. **State must persist between steps.** If the orchestrator crashes mid-workflow, it must resume from the last persisted checkpoint, not start from scratch.
4. **Observability is not optional.** Every step must emit start/complete/error events. A workflow without per-step logs produces no forensic trail for debugging failures.
5. **Parallel branches need explicit join conditions.** Unjoined parallel branches have no signal for when the aggregate is complete, causing downstream steps to start prematurely or never start.
6. **Dead-letter queues prevent infinite retries.** Poison-pill messages that cannot be processed must be quarantined, not retried indefinitely.

---

## Workflow Patterns

### Sequential Workflow
```
Task A -> Task B -> Task C -> Task D
```

### Parallel Workflow
```
       +-- Task B --+
Task A +-- Task C --+-- Task E
       +-- Task D --+
```

### Conditional Workflow
```
Task A -> Decision -> Task B (if condition)
                  -> Task C (else)
```

---

## Implementation

### Temporal Workflow

```typescript
export async function processOrder(orderId: string): Promise<OrderResult> {
  const order = await validateOrder(orderId);
  if (!order.valid) throw new Error("Invalid order");

  const reservation = await reserveInventory(order.items);
  if (!reservation.success) throw new Error("Inventory not available");

  try {
    const payment = await processPayment(order.paymentInfo);
    const shipment = await shipOrder(orderId, reservation.id);
    await notifyCustomer(order.customerId, { type: "order_confirmed", orderId });
    return { success: true, orderId, trackingNumber: shipment.trackingNumber };
  } catch (error) {
    await releaseInventory(reservation.id);
    throw error;
  }
}
```

### Saga Compensation Pattern

```typescript
async function processOrderWithCompensation(orderId: string) {
  const compensations: (() => Promise<void>)[] = [];

  try {
    const order = await createOrder(orderId);
    compensations.push(async () => cancelOrder(orderId));

    const reservation = await reserveInventory(order.items);
    compensations.push(async () => releaseInventory(reservation.id));

    const payment = await processPayment(order.payment);
    compensations.push(async () => refundPayment(payment.id));
  } catch (error) {
    for (const compensate of compensations.reverse()) {
      try { await compensate(); } catch (e) { console.error("Compensation failed:", e); }
    }
    throw error;
  }
}
```

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Starting parallel workflow without join condition | Branches run independently; no signal for aggregate completion | Add explicit join point before downstream steps |
| Orchestrating steps sharing mutable state without locking | Race conditions; non-deterministic failures | Add optimistic locking or distributed lock on state updates |
| Retrying non-idempotent step automatically | Duplicate side effects (double charge, double email) | Use idempotency key derived from workflow ID + step name |
| Defining workflow without explicit terminal state | Workflow loops/stalls indefinitely, exhausting resources | Define end condition for every workflow |
| Single orchestrator replica without health check | Orchestrator is single point of failure; workers idle | Run >= 2 replicas behind load balancer with liveness probe |

## Verification

### Self-Verification Checklist

- [ ] Compensation logic exists for every step with side effects
- [ ] Dead-letter queue configured for all workflows
- [ ] Orchestrator replica count >= 2
- [ ] Idempotency keys present on mutating steps
- [ ] Retry bounds defined (max attempts, backoff)
- [ ] State persisted between steps
- [ ] Per-step observability: start/complete/error events emitted

### Verification Commands

```bash
# Check compensation coverage
grep -rn "compensat\|rollback\|undo" src/orchestrator/

# Check DLQ config
grep -rn "DLQ\|dead.letter\|deadLetter" src/orchestrator/

# Check idempotency keys
grep -rn "idempotent\|idempotency.key\|dedup" src/orchestrator/

# Check retry bounds
grep -rn "maxAttempts\|max_retries\|retryable\|backoff" src/orchestrator/

# Verify orchestrator replicas
kubectl get deployment <name> -o jsonpath='{.spec.replicas}'
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Compensation | Every mutating step has rollback | Add compensation before deploying |
| Idempotency | Every external API call has idempotency key | Add key before enabling retry |
| Retry Bounds | max retries defined, backoff configured | Add bounds to prevent retry storms |
| State Persistence | Checkpoint between each step | Add state persistence before production |
| High Availability | Replica count >= 2 | Add replicas and liveness probe |

## Performance & Cost

### Model Selection

| Task | Approach | Cost |
|---|---|---|
| Simple sequential | Direct function calls | Minimal |
| Temporal workflow | Temporal server + workers | Server cost + worker compute |
| Saga coordination | Compensation stack in code | Free |

### Parallelization

- **Independent branches:** Run in parallel with explicit join
- **Sequential steps:** Must run in order
- **Compensation:** Runs in reverse order on failure

### Context Budget

- **Expected context usage:** 4-8KB per workflow design session
- **When to context-optimize:** When reviewing multi-branch workflows or complex compensation chains

## Examples

### Example 1: Order Processing Workflow

**User request:** "Build a reliable order processing workflow."

**Skill execution:**
1. Design sequential flow: Validate -> Reserve Inventory -> Process Payment -> Ship -> Notify
2. Add compensation for each step: release inventory if payment fails, refund if shipping fails
3. Add idempotency keys on payment and shipping API calls
4. Add retry with exponential backoff (3 attempts)
5. Add state persistence between steps
6. Configure DLQ for unprocessable orders

**Result:** Reliable order processing with complete compensation, retry, and observability.

### Example 2: Edge Case - Partial Failure

**User request:** "Payment succeeded but shipping failed. The customer was charged but not shipped."

**Skill execution:**
1. Compensation for shipping failure: do NOT retry payment (already succeeded)
2. Run compensation: refund payment via refundPayment()
3. Log the failure with full context
4. Send to DLQ for manual resolution
5. Report: compensation completed successfully, order cancelled

**Result:** Customer refunded. System in consistent state.

## Anti-Patterns

- Never start a parallel workflow without defining a join condition because parallel branches that have no explicit join point run to completion independently and the orchestrator has no signal for when the aggregate is done, causing downstream steps to start prematurely or never start.
- Never orchestrate steps that share mutable state without explicit locking because two concurrent steps reading and writing the same state field will produce race conditions whose outcome depends on scheduling order, making failures non-deterministic and hard to reproduce.
- Never treat a timed-out step as failed without checking for partial completion because a step that timed out may have already mutated external state (e.g., charged a card, reserved inventory); retrying without checking for partial completion causes duplicate side effects.
- Never define a workflow without an explicit terminal state because a workflow with no defined end condition can loop, stall, or accumulate running instances indefinitely, exhausting resources and making observability impossible.
- Never retry a non-idempotent step automatically because an automatic retry of a step that is not idempotent (e.g., sends an email, charges a payment) executes the side effect multiple times, causing data corruption or duplicate user-facing actions.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Saga compensation step fails, leaving distributed system in inconsistent state | Compensation function throws uncaught error; partial rollback | Wrap every compensation in retry with exponential backoff; log compensation failures to DLQ |
| Workflow state corrupted by concurrent update from two orchestrator instances | Two pods process same workflow event simultaneously; no optimistic locking | Use optimistic locking (version field) or distributed lock on workflow state updates |
| Dead-letter queue overflows because poison-pill message never acknowledged | One malformed message loops through retry indefinitely | Set max-retry limit per message type; add DLQ size alert at 80% capacity |
| Orchestrator is single point of failure; worker nodes healthy but idle | Single replica with no health check | Run >= 2 replicas; add liveness probe; task queue depth alert |
| Step retry without idempotency key causes duplicate side effects | Step issues external API call without idempotency key; retry sends call twice | Every mutating step must include idempotency key from workflow ID + step name |

## References

### Internal Dependencies
- `verification-loop` — Verifies all workflow phases pass
- `observability-specialist` — Monitors workflow execution health
- `content-hash-cache-pattern` — Caches workflow state snapshots

### External Standards
- [Temporal Documentation](https://docs.temporal.io/) — Workflow orchestration engine
- [Saga Pattern](https://microservices.io/patterns/data/saga.html) — Distributed transaction pattern

### Related Skills
- `verification-loop` — Follows workflow-orchestrator for verification
- `observability-specialist` — Partner skill for workflow monitoring

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Performance & Cost section, Examples, References, Changelog. |
---
