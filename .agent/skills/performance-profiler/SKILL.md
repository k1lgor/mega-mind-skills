---
name: performance-profiler
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
