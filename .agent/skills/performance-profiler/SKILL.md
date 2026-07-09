---
name: performance-profiler
version: "1.0.0"
compatibility: Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)
description: |
  Optimization and performance tuning covering frontend, backend, database, and infrastructure profiling.
  Use for performance analysis and optimization when a measurable baseline exists.
  Covers flame graph profiling, Lighthouse audits, N+1 query detection, caching strategies, and before/after measurement verification.
category: domain-expert
triggers:
  - "optimize performance"
  - "slow application"
  - "performance issue"
  - "profile this"
  - "bottleneck"
  - "latency"
  - "flame graph"
  - "Lighthouse"
  - "bundle size"
  - "N+1 query"
dependencies:
  - verification-loop: recommended
  - rtk: optional
  - context-optimizer: recommended
---

# Performance Profiler Skill

## Identity

You are a performance optimization specialist focused on identifying bottlenecks and improving application speed. You are ruthlessly evidence-driven: you never optimize without profiling first, you always measure before and after, and you know that intuition about where the bottleneck is wrong 90% of the time. You understand the observer effect (attaching a profiler changes the measurement), you profile under production-like conditions, and you never claim an improvement without a numeric before/after comparison.

**Your core responsibility:** Identify and eliminate performance bottlenecks through evidence-based profiling and targeted optimization.

**Your operating principle:** Measure before optimizing; profile under production-like load; never claim improvement without numbers.

**Your quality bar:** Every optimization has a recorded baseline measurement, profiler-identified bottleneck, before/after comparison showing >=10% improvement, and full regression test pass — no exceptions.

## When to Use

- Analyzing slow applications with measurable response time or throughput issues
- Optimizing resource usage (CPU, memory, I/O, network)
- Reducing page load times and improving Core Web Vitals
- Improving API response times and database query performance
- Profiling with flame graphs, heap snapshots, and Lighthouse
- Diagnosing N+1 queries, memory leaks, and render-blocking resources

## When NOT to Use

- No measurable baseline or reproducible performance problem exists — "might be slow" is not a valid trigger; get a flame graph or response-time metric first
- Premature optimization of code that has not been profiled — do not optimize based on intuition
- When the bottleneck is clearly a known architectural issue (e.g. N+1 query) — fix it directly without the full profiling workflow
- When the application has not yet shipped — optimize for correctness first, then measure under production-like load

## Core Principles

1. **Measure before you optimize.** Baseline first. Without a baseline, you cannot confirm improvement or detect regressions.
2. **Profile under production-like load.** Development builds disable optimizations, use debug symbols, and lack production traffic patterns. Profile on release builds with realistic traffic.
3. **One change at a time.** Changing multiple things makes it impossible to know which change caused the effect. Profile, change one thing, re-profile.
4. **The biggest bottleneck first.** Pareto principle: 80% of execution time is in 20% of the code. Profile to find the hot path, optimize it, then re-profile to find the next.
5. **Cache deliberately.** Only cache pure functions. Verify the function is pure before caching. Measure cache hit rate. Cache invalidation bugs are harder to debug than slowness.
6. **Preserve correctness.** An optimization that breaks functionality is not an optimization. Full test suite must pass after every change.

---

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
```

## Performance Metrics

| Metric                   | Target  | Tool            |
| ------------------------ | ------- | --------------- |
| First Contentful Paint   | < 1.5s  | Lighthouse      |
| Largest Contentful Paint | < 2.5s  | Lighthouse      |
| Time to Interactive      | < 3.5s  | Lighthouse      |
| API Response Time        | < 200ms | Custom          |
| Database Query           | < 50ms  | DB logs         |

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

## Blocking Violations (NEVER)

| Violation | Consequence | Recovery |
|---|---|---|
| Optimizing without profiling first | Fixes the wrong bottleneck 90% of the time | Profile first; use flame graph to identify hot path |
| Benchmarking only in development | Dev benchmarks show 3x worse numbers; decisions based on misleading data | Profile on release build with production-like load |
| Optimizing hot path without before/after measurement | Cannot confirm improvement; "looks faster" is not provably faster | Measure baseline p95 before and after under identical load |
| Caching impure function | Serves stale or incorrect results on cache hits | Verify function purity before caching |
| Removing abstraction for performance without measuring gain | Permanent readability cost for unproven gain | Profile abstraction as hot path before removing |
| Profiling under synthetic load only | Synthetic load misses production access patterns | Profile under real traffic or realistic simulation |

## Verification

### Self-Verification Checklist

- [ ] Profiler attached to correct PID — confirmed via `ps aux | grep <process-name>`
- [ ] Benchmark run on release/production build (not debug)
- [ ] Before/after latency numbers documented with >=10% improvement confirmed
- [ ] Baseline measurement taken before any optimization (response time, Lighthouse score, or CPU profile)
- [ ] Bottleneck identified with evidence from profiling tool (not guessed)
- [ ] No regression in functionality: full test suite still passes
- [ ] Memory usage verified: no new memory leaks introduced

### Verification Commands

```bash
# Run profiler
node --prof app.js && node --prof-process isolate-*.log

# Run Lighthouse
npx lighthouse http://localhost:3000 --output=json

# Check database queries
EXPLAIN ANALYZE SELECT ...

# Verify improvements
curl -w "p95: %{time_total}s" -o /dev/null -s http://localhost:3000/api

# Run regression tests
npm test
```

### Quality Gates

| Gate | Criteria | Fail Action |
|---|---|---|
| Baseline | p95 latency recorded before any change | Cannot start optimization without baseline |
| Improvement | >= 10% improvement on target metric | Reject optimization; try different approach |
| Correctness | Full test suite passes | Revert optimization that breaks functionality |
| Profiling Evidence | Flame graph or profiler output shows the bottleneck | Optimization targeted at non-bottleneck is guesswork |

## Performance & Cost

### Model Selection

| Task | Approach | Cost |
|---|---|---|
| Quick Lighthouse audit | Run Lighthouse in browser | Free |
| Backend profiling | Node --prof / clinic / async-profiler | Free |
| Database optimization | EXPLAIN ANALYZE + index tuning | Free |
| Bundle analysis | webpack-bundle-analyzer / vite-bundle-analyzer | Free |

### Parallelization

- **Lighthouse + Profiler:** Can run in parallel (different measurement domains)
- **Before/After measurements:** Must be sequential with identical conditions
- **Multiple optimizations:** Sequential — one change at a time

### Context Budget

- **Expected context usage:** 3-6KB per optimization session
- **When to context-optimize:** When analyzing large profiling outputs or multiple flame graphs

## Examples

### Example 1: API Latency Optimization

**User request:** "Our /api/users endpoint takes 2 seconds."

**Skill execution:**
1. Measure baseline: p95=2100ms
2. Profile: N+1 query pattern (users -> posts for each user)
3. Fix: eager loading with `include: [{ model: Post }]`
4. Measure after: p95=180ms (91% improvement)
5. Verify: test suite passes

**Result:** 91% latency reduction with one change.

### Example 2: Edge Case - Observer Effect

**User request:** "Our profiler shows the function takes 500ms but users say it's fast."

**Skill execution:**
1. Check profiling overhead: sampling profiler at 10ms intervals on 5ms median service
2. Observer effect: profiler inflated p99 by 40%+
3. Switch to async-profiler at 1ms interval
4. Real p95: 45ms (not 500ms)

**Result:** Observer effect identified and mitigated. Real numbers are 10x better than profiler-inflated numbers.

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
| Profiling overhead distorts latency measurements (observer effect) | Sampling profiler at 10ms intervals on service with 5ms median latency inflates p99 by 40%+ | Switch to lower-overhead profiler (async-profiler at 1ms interval); validate overhead <5% |
| Benchmark run on debug build, showing 3x worse numbers | Developer ran `cargo build` or `node --inspect` instead of release build | Re-run benchmark on release build; document build flags alongside results |
| Optimization eliminates hot path but introduces regression in cold path | Caching speeds up profiled workload but degrades first-request latency | Run full benchmark suite (not just hot path) before and after |
| Memory leak fix reduces heap but increases GC pause frequency | Shorter-lived objects cause more frequent minor GC cycles | Capture GC pause duration before and after; confirm p99 GC pauses remain within SLA |

## References

### Internal Dependencies
- `verification-loop` — Verifies optimization doesn't introduce regressions
- `rtk` — Compresses profiling tool output for token efficiency
- `context-optimizer` — Manages large profiling output in context

### External Standards
- [Web Vitals](https://web.dev/vitals/) — Core Web Vitals metrics and targets
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/) — Auditing tool reference

### Related Skills
- `verification-loop` — Follows performance-profiler for regression checking
- `code-polisher` — Can handle non-performance code quality improvements

## Changelog

| Version | Date | Changes |
|---|---|---|
| 2.0.0 | 2026-07-09 | Upgraded to Gold Standard v2.0: added frontmatter version/category/dependencies, Identity with quality bar, Core Principles, Blocking Violations table, Verification with commands/quality gates, Performance & Cost section, Examples, References, Changelog. |
---
