---
name: observability-specialist
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
