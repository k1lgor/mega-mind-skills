---
name: observability-specialist
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Logging, tracing, and monitoring setup. Use for observability and monitoring tasks.
triggers:
  - "observability"
  - "monitoring"
  - "logging"
  - "tracing"
  - "alerting"
---

# Observability Specialist Skill

## Identity

You are an observability specialist focused on building comprehensive monitoring, logging, and tracing systems.

## When to Use

- Setting up monitoring
- Implementing logging
- Adding distributed tracing
- Creating dashboards and alerts

## When NOT to Use

- Before the code is stable enough to instrument — adding observability to rapidly changing prototype code creates noise, not signal
- For simple scripts or one-off tools with no ongoing operational use
- When the team has no on-call rotation or alert response process — alerts with no responder are worse than no alerts (alert fatigue)
- As a substitute for fixing bugs — if error rate is high, fix the errors; don't just add a dashboard for them

## Observability Pillars

```
┌─────────────────────────────────────────────────┐
│                   Observability                  │
├─────────────────┬─────────────────┬─────────────┤
│     Metrics     │      Logs       │   Traces    │
│  (Aggregated)   │  (Event-based)  │ (Context)   │
└─────────────────┴─────────────────┴─────────────┘
```

## Logging Implementation

```typescript
// logger.ts
import winston from "winston";

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json(),
  ),
  defaultMeta: {
    service: "my-service",
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple(),
      ),
    }),
    new winston.transports.File({
      filename: "logs/error.log",
      level: "error",
    }),
    new winston.transports.File({
      filename: "logs/combined.log",
    }),
  ],
});

// Structured logging helpers
export const logRequest = (req, res, responseTime) => {
  logger.info("HTTP Request", {
    method: req.method,
    path: req.path,
    status: res.statusCode,
    responseTime: `${responseTime}ms`,
    userAgent: req.get("user-agent"),
    ip: req.ip,
  });
};

export const logError = (error, context = {}) => {
  logger.error("Application Error", {
    error: {
      message: error.message,
      stack: error.stack,
      name: error.name,
    },
    ...context,
  });
};
```

## Metrics Collection

```typescript
// metrics.ts
import {
  collectDefaultMetrics,
  Registry,
  Counter,
  Histogram,
  Gauge,
} from "prom-client";

const register = new Registry();
collectDefaultMetrics({ register });

// Custom metrics
export const httpRequestDuration = new Histogram({
  name: "http_request_duration_seconds",
  help: "Duration of HTTP requests in seconds",
  labelNames: ["method", "path", "status"],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  registers: [register],
});

export const httpRequestTotal = new Counter({
  name: "http_requests_total",
  help: "Total number of HTTP requests",
  labelNames: ["method", "path", "status"],
  registers: [register],
});

export const activeConnections = new Gauge({
  name: "active_connections",
  help: "Number of active connections",
  registers: [register],
});

// Middleware
export const metricsMiddleware = (req, res, next) => {
  const start = Date.now();

  res.on("finish", () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestDuration
      .labels(req.method, req.path, res.statusCode.toString())
      .observe(duration);

    httpRequestTotal
      .labels(req.method, req.path, res.statusCode.toString())
      .inc();
  });

  next();
};
```

## Distributed Tracing

```typescript
// tracing.ts
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { JaegerExporter } from "@opentelemetry/exporter-jaeger";
import { Resource } from "@opentelemetry/resources";
import { trace } from "@opentelemetry/api";

const provider = new NodeTracerProvider({
  resource: new Resource({
    "service.name": "my-service",
    "service.version": "1.0.0",
  }),
  exporters: [
    new JaegerExporter({
      endpoint: "http://jaeger:14268/api/traces",
    }),
  ],
});

provider.register();

export const tracer = trace.getTracer("my-service");

// Usage in code
export async function processOrder(orderId: string) {
  const span = tracer.startSpan("process_order");

  try {
    span.setAttribute("order.id", orderId);

    const order = await fetchOrder(orderId);
    span.addEvent("order_fetched");

    const result = await validateOrder(order);
    span.addEvent("order_validated");

    span.setStatus({ code: 0 }); // OK
    return result;
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: 2, message: error.message }); // ERROR
    throw error;
  } finally {
    span.end();
  }
}
```

## Alerting Rules

```yaml
# alerting-rules.yml
groups:
  - name: application
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value | humanizePercentage }}

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: 95th percentile latency is {{ $value }}s

      - alert: ServiceDown
        expr: up{job="my-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Service is down
          description: Service {{ $labels.instance }} is down
```

## Dashboard Template

```markdown
## Application Dashboard

### Overview

| Metric             | Current   | Alert Threshold |
| ------------------ | --------- | --------------- |
| Request Rate       | 1,234/min | -               |
| Error Rate         | 0.5%      | > 5%            |
| P95 Latency        | 250ms     | > 1s            |
| Active Connections | 456       | > 1000          |

### Error Breakdown

| Error Type       | Count | Rate |
| ---------------- | ----- | ---- |
| 500 Server Error | 23    | 0.2% |
| 404 Not Found    | 45    | 0.3% |
| Timeout          | 12    | 0.1% |

### Resource Usage

| Resource | Usage | Limit |
| -------- | ----- | ----- |
| CPU      | 45%   | 80%   |
| Memory   | 2.1GB | 4GB   |
| Disk     | 45GB  | 100GB |
```

## Tips

- Use structured logging with consistent formats
- Implement correlation IDs for request tracing
- Set meaningful alert thresholds
- Create runbooks for common alerts
- Monitor the monitoring system itself

## Anti-Patterns

- Never add a high-cardinality label (e.g. user_id, request_id) to a Prometheus metric because it creates millions of time series and causes the Prometheus server to OOM under normal traffic.
- Never set trace sampling rate to 100% in production because it floods the collector, increases latency of every instrumented request, and exhausts storage within hours.
- Never ship a log line containing PII without scrubbing because centralized logging systems retain data for months and a single log export violates GDPR/CCPA.
- Never define an alert without a runbook link because on-call engineers cannot remediate an alert they have never seen before, extending MTTR unnecessarily.
- Never monitor only the happy path because errors and latency spikes on failure paths are invisible until a customer reports them, at which point data for diagnosis is already gone.
- Never use wall-clock timestamps for distributed trace correlation because clock skew between nodes causes spans to appear out of order, making traces unreadable.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Alert fires but runbook link is stale, on-call engineer can't find remediation steps | Runbook URL changed after alert was created, never updated | Audit all alert annotations for runbook URLs; validate each link before going on-call |
| High-cardinality label added to metric, causing Prometheus memory OOM | Developer added user ID or request ID as a label without understanding cardinality implications | Remove the high-cardinality label immediately; replace with a lower-cardinality bucketed label; restart Prometheus with `-storage.tsdb.retention.time` to reclaim memory |
| Trace sampling rate set to 100% under load, overwhelming collector | Sampling rate left at 100% from development; not adjusted for production traffic volume | Reduce sampling to 1-10% via head-based sampling config; use tail-based sampling for error traces only |
| Log line contains PII (email, token) shipped to centralized logging system | Logging middleware serializes request body or headers without a PII scrubber | Add a scrubbing transform in the logging pipeline; rotate any leaked tokens immediately; audit retention store for PII exposure |
| Dashboard shows metric but no alert threshold defined, masking SLO breach | Dashboard built for visibility without pairing alerts to SLO targets | For each SLO metric on the dashboard, add a corresponding alert rule with a `for: 5m` guard; link the alert to the dashboard panel |

## Self-Verification Checklist

- [ ] All dashboards load without error in Grafana (or equivalent) — 0 panel errors shown
- [ ] At least one alert fires correctly when a bad signal is injected (e.g., error rate spike test confirms alert triggers within 5 minutes)
- [ ] Log sample grep confirms 0 PII matches: `grep -E '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|Bearer [A-Za-z0-9._-]+)' <log-sample>` exits with no matches
- [ ] Structured JSON logging is configured (not plain-text log lines)
- [ ] Correlation IDs are present on all inbound requests and propagated through downstream calls
- [ ] Dashboards cover the 4 golden signals: latency, traffic, errors, saturation
- [ ] Runbooks exist for all configured alerts — every alert annotation has a valid, reachable runbook URL

## Success Criteria

This skill is complete when: 1) structured logs with correlation IDs are emitted from every service boundary, 2) at least error rate and latency are instrumented with actionable alerts, and 3) a runbook exists for each alert so the on-call engineer knows what to do when it fires.
