---
name: performance-profiler
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Optimization and performance tuning. Use for performance analysis and optimization.
triggers:
  - "optimize performance"
  - "slow application"
  - "performance issue"
  - "profile this"
---

# Performance Profiler Skill

## Identity

You are a performance optimization specialist focused on identifying bottlenecks and improving application speed.

## When to Use

- Analyzing slow applications
- Optimizing resource usage
- Reducing load times
- Improving response times

## When NOT to Use

- No measurable baseline or reproducible performance problem exists — "might be slow" is not a valid trigger; get a flame graph or response-time metric first
- Premature optimization of code that has not been profiled — do not optimize based on intuition
- When the bottleneck is clearly a known architectural issue (e.g. N+1 query) — fix it directly without the full profiling workflow
- When the application has not yet shipped — optimize for correctness first, then measure under production-like load

## Performance Analysis Framework

### Step 1: Measure Baseline

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Memory usage
node --expose-gc --inspect app.js

# Response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3000/api
```

### Step 2: Identify Bottlenecks

```markdown
## Performance Analysis

### Frontend

- [ ] Measure page load time
- [ ] Check bundle size
- [ ] Analyze critical rendering path
- [ ] Check network requests

### Backend

- [ ] Measure API response times
- [ ] Check database queries
- [ ] Analyze CPU usage
- [ ] Check memory leaks

### Infrastructure

- [ ] CDN configuration
- [ ] Caching headers
- [ ] Compression enabled
```

### Step 3: Optimize

### Step 4: Verify Improvement

## Common Optimizations

### Frontend

```javascript
// Code splitting
const Component = lazy(() => import("./HeavyComponent"));

// Image optimization
<img src="image.webp" loading="lazy" alt="..." />;

// Bundle analysis
import { BundleAnalyzerPlugin } from "webpack-bundle-analyzer";

// Caching
const cache = new Map();
function cachedFetch(url) {
  if (cache.has(url)) return cache.get(url);
  const promise = fetch(url).then((r) => r.json());
  cache.set(url, promise);
  return promise;
}
```

### Backend

```javascript
// Database query optimization
// Before: N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// After: Eager loading
const users = await User.findAll({
  include: [{ model: Post }],
});

// Caching
const cachedData = await redis.get("key");
if (cachedData) return JSON.parse(cachedData);

const data = await expensiveOperation();
await redis.setex("key", 3600, JSON.stringify(data));
return data;

// Connection pooling
const pool = mysql.createPool({
  connectionLimit: 10,
  host: "localhost",
  user: "root",
  password: "password",
  database: "mydb",
});
```

### Database

```sql
-- Add indexes
CREATE INDEX idx_users_email ON users(email);

-- Analyze query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Optimize joins
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE u.active = true;
```

## Performance Metrics

| Metric                   | Target  | Tool            |
| ------------------------ | ------- | --------------- |
| First Contentful Paint   | < 1.5s  | Lighthouse      |
| Largest Contentful Paint | < 2.5s  | Lighthouse      |
| Time to Interactive      | < 3.5s  | Lighthouse      |
| API Response Time        | < 200ms | Custom          |
| Database Query           | < 50ms  | DB logs         |
| Memory Usage             | < 80%   | Process monitor |

## Profiling Tools

```bash
# Node.js
node --prof app.js
clinic doctor -- node app.js
0x app.js

# Chrome DevTools
# Performance tab for frontend profiling

# Database
EXPLAIN ANALYZE SELECT ...

# Network
curl -w "Time: %{time_total}s\n" -o /dev/null -s URL
```

## Optimization Checklist

```markdown
## Performance Optimization Checklist

### Frontend

- [ ] Minimize bundle size
- [ ] Enable compression (gzip/brotli)
- [ ] Use lazy loading
- [ ] Optimize images
- [ ] Use CDN for static assets
- [ ] Minimize render-blocking resources
- [ ] Implement caching

### Backend

- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Implement caching layer
- [ ] Use connection pooling
- [ ] Enable response compression
- [ ] Implement rate limiting
- [ ] Use async operations

### Infrastructure

- [ ] Configure CDN
- [ ] Enable HTTP/2
- [ ] Set proper cache headers
- [ ] Use load balancing
- [ ] Scale horizontally if needed
```

## Tips

- Always measure before optimizing
- Focus on the biggest bottlenecks first
- Cache aggressively but wisely
- Profile in production-like conditions
- Monitor continuously after deployment

## Anti-Patterns

- Never optimise without profiling first because optimisation based on intuition targets the wrong function 90% of the time; the actual bottleneck is almost never where you expect it to be.
- Never benchmark in development only because development builds disable compiler optimisations, use debug symbols, and lack production traffic patterns; development benchmarks regularly show 3x worse numbers than production and cannot be used to make decisions.
- Never optimise a hot path without a before/after measurement because an optimisation that cannot be measured cannot be confirmed; code that looks faster is not provably faster until the numbers say so.
- Never cache the result of a function without verifying the function is pure because caching an impure function (one with side effects or non-deterministic output) serves stale or incorrect results on every cache hit.
- Never remove an abstraction for performance without measuring the gain because removing an abstraction is a permanent readability cost; if the profiler does not show the abstraction as a significant hot path, the trade-off is not justified.
- Never profile under synthetic load only because synthetic load does not reproduce production access patterns, cache warming, connection pool exhaustion, or concurrent user behaviour; a benchmark that shows green under synthetic load can still fail under real traffic.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| Profiling overhead distorts latency measurements (observer effect) | Attaching a sampling profiler at 10ms intervals on a service with 5ms median latency inflates p99 by 40%+ | Switch to a lower-overhead continuous profiler (e.g., async-profiler at 1ms interval); validate overhead is <5% before treating numbers as representative |
| Benchmark run on debug build, showing 3× worse numbers than production | Developer ran `cargo build` or `node --inspect` instead of `cargo build --release` or production node binary | Re-run benchmark explicitly on the release build; document build flags used alongside every benchmark result |
| Optimization eliminates hot path but introduces regression in cold path | Caching or memoization speeds up the profiled workload but degrades first-request latency or memory under varied input | Run the full benchmark suite (not just the hot path) before and after; add a cold-start latency test to the benchmark suite |
| Memory leak fix reduces heap but increases GC pause frequency | Shorter-lived objects cause more frequent minor GC cycles, increasing p99 latency even as average drops | Capture GC pause duration before and after (use `--expose-gc` or equivalent); confirm p99 GC pauses remain within SLA |
| Profiler attached to wrong process PID, returning unrelated data | PID reuse or multiple instances running; profiler targeting a sidecar or proxy instead of the application | Verify PID with `ps aux | grep <process-name>` before attaching; cross-reference with process start time to confirm correct target |

## Self-Verification Checklist

- [ ] Profiler attached to correct PID — confirmed via `ps aux | grep <process-name>` showing process name matches expected application
- [ ] Benchmark run on release/production build (not debug) — build command and flags documented alongside results
- [ ] Before/after latency numbers documented with ≥10% improvement confirmed: baseline p95 recorded before any change, post-optimization p95 recorded under identical load conditions
- [ ] Baseline measurement was taken before any optimization (response time, Lighthouse score, or CPU profile recorded)
- [ ] The bottleneck is identified with evidence from a profiling tool — not guessed (e.g., flame graph shows function at ≥20% CPU)
- [ ] No regression in functionality: full test suite still passes after optimizations
- [ ] Memory usage verified: no new memory leaks introduced (heap snapshots before/after compared if relevant)

## Success Criteria

This task is complete when:
1. A before/after performance comparison exists with concrete numbers (e.g. "API p95 latency reduced from 850ms to 210ms")
2. The bottleneck identified by profiling is confirmed fixed, not just masked by caching
3. The optimization is deployed and monitoring confirms the improvement holds under real load
