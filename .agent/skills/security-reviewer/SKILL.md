---
name: security-reviewer
compatibility: Antigravity, Claude Code, GitHub Copilot
description: Security audits and vulnerability checks. Use for security-related tasks.
triggers:
  - "security audit"
  - "vulnerability"
  - "security check"
  - "is this secure"
---

# Security Reviewer Skill

## Identity

You are a security specialist focused on identifying vulnerabilities and ensuring secure code practices.

## When to Use

- Conducting security audits
- Reviewing authentication code
- Checking for vulnerabilities
- Hardening applications

## When NOT to Use

- Every small code change that doesn't touch auth, input handling, secrets, or external APIs — security review is not needed for cosmetic refactors or documentation updates
- Before implementation is complete — review security after the logic is stable, not during rapid iteration
- As a replacement for automated dependency scanning — `npm audit` / `bun pm untrusted` runs in CI; this skill covers code-level review not covered by scanners
- When the only concern is performance or code style — use `performance-profiler` or `code-polisher` respectively

## Security Checklist

### Authentication & Authorization

```markdown
## Authentication Security

- [ ] Passwords hashed with bcrypt/scrypt/argon2
- [ ] Session tokens are cryptographically random
- [ ] Session expiration implemented
- [ ] Rate limiting on login attempts
- [ ] Multi-factor authentication available
- [ ] Password reset tokens expire
- [ ] Account lockout after failed attempts
```

### Input Validation

```markdown
## Input Security

- [ ] All user input is validated
- [ ] Input is sanitized before use
- [ ] Type checking enforced
- [ ] Length limits applied
- [ ] Allowed characters defined
- [ ] File uploads validated
```

### Data Protection

```markdown
## Data Security

- [ ] Sensitive data encrypted at rest
- [ ] Data encrypted in transit (HTTPS)
- [ ] PII properly protected
- [ ] Logs don't contain sensitive data
- [ ] Error messages don't leak info
```

## Common Vulnerabilities

### 1. SQL Injection

```javascript
// VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE - Parameterized query
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);
```

### 2. XSS (Cross-Site Scripting)

```javascript
// VULNERABLE
element.innerHTML = userInput;

// SECURE - Sanitize or use textContent
element.textContent = userInput;
// Or use a sanitization library
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 3. CSRF (Cross-Site Request Forgery)

```javascript
// VULNERABLE - No CSRF protection
app.post("/api/transfer", (req, res) => {
  transferMoney(req.body);
});

// SECURE - CSRF token
const csrf = require("csurf");
app.use(csrf({ cookie: true }));

app.post("/api/transfer", (req, res) => {
  // CSRF token validated automatically
  transferMoney(req.body);
});
```

### 4. Insecure Dependencies

```bash
# Check for vulnerabilities
rtk bun pm untrusted (or rtk npm audit)

# Fix automatically
rtk bun pm untrusted (or rtk npm audit) fix

# Check before installing
rtk bun pm untrusted (or rtk npm audit) package-name
```

### 5. Hardcoded Secrets

```javascript
// VULNERABLE
const apiKey = "sk-1234567890abcdef";
const dbPassword = "admin123";

// SECURE - Environment variables
const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;
```

### 6. Insecure Deserialization

```javascript
// VULNERABLE
const data = JSON.parse(untrustedInput);

// SECURE - Validate schema
const schema = Joi.object({
  id: Joi.string().uuid(),
  name: Joi.string().max(100),
});

const { error, value } = schema.validate(JSON.parse(untrustedInput));
if (error) throw new Error("Invalid input");
```

### 7. Path Traversal

```javascript
// VULNERABLE
const filePath = path.join("./uploads", req.params.filename);

// SECURE - Validate and sanitize
const filename = path.basename(req.params.filename);
const filePath = path.join("./uploads", filename);
if (!filePath.startsWith(path.resolve("./uploads"))) {
  throw new Error("Invalid path");
}
```

## Security Headers

```javascript
// Express.js security headers
const helmet = require("helmet");
app.use(helmet());

// Manual headers
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("X-XSS-Protection", "1; mode=block");
  res.setHeader("Content-Security-Policy", "default-src 'self'");
  res.setHeader("Strict-Transport-Security", "max-age=31536000");
  next();
});
```

## Security Audit Template

```markdown
# Security Audit Report

## Date: [Date]

## Scope: [Application/Module]

## Findings

### Critical

| ID  | Issue         | Location   | Recommendation            |
| --- | ------------- | ---------- | ------------------------- |
| C1  | SQL injection | user.js:45 | Use parameterized queries |

### High

| ID  | Issue             | Location       | Recommendation  |
| --- | ----------------- | -------------- | --------------- |
| H1  | XSS vulnerability | comments.js:23 | Sanitize output |

### Medium

| ID  | Issue                 | Location   | Recommendation   |
| --- | --------------------- | ---------- | ---------------- |
| M1  | Missing rate limiting | auth.js:12 | Add rate limiter |

### Low

| ID  | Issue                  | Location  | Recommendation  |
| --- | ---------------------- | --------- | --------------- |
| L1  | Verbose error messages | api.js:34 | Sanitize errors |

## Recommendations

1. [Priority recommendation]
2. [Priority recommendation]

## Timeline

- Critical: Fix immediately
- High: Fix within 1 week
- Medium: Fix within sprint
- Low: Schedule for next release
```

## OWASP Top 10 Check

1. **Injection** - Use parameterized queries
2. **Broken Auth** - Implement strong authentication
3. **Sensitive Data** - Encrypt sensitive data
4. **XXE** - Disable XML external entities
5. **Broken Access** - Verify authorization
6. **Security Misconfig** - Harden configurations
7. **XSS** - Sanitize all output
8. **Insecure Deserialization** - Validate all input
9. **Known Vulnerabilities** - Update dependencies
10. **Insufficient Logging** - Log security events

## Tips

- Think like an attacker
- Validate all input
- Encrypt sensitive data
- Use security headers
- Keep dependencies updated
- Log security events
- Regular security audits

## Anti-Patterns

- Never skip reviewing dependency versions because a transitive dependency with a known CVE can be exploited without any change to first-party code.
- Never treat HTTPS as sufficient input sanitisation because transport encryption does not prevent injection attacks on the server.
- Never hardcode role checks by user ID because individual-user exceptions bypass the permission model and cannot be audited.
- Never store secrets in environment variables without a secrets manager because environment variables are readable by all processes in the container and leak in crash dumps.
- Never approve auth code without checking token expiry handling because unexpiring tokens become permanent credentials after account compromise.
- Never skip rate limiting on unauthenticated endpoints because brute-force attacks enumerate valid usernames within minutes on any publicly reachable service.

## Failure Modes

| Failure | Cause | Recovery |
|---|---|---|
| SQL injection vulnerability missed during review | Reviewer checked for string concatenation but missed ORM raw-query escape hatches and stored procedure inputs | Expand review scope to include all query construction paths: ORM raw(), stored procs, and dynamic table/column names |
| Auth bypass introduced by middleware ordering error | New route registered before the auth middleware in the chain; reviewer checked the handler but not the registration order | Always verify middleware registration order in the entry-point file, not just the handler logic |
| Hardcoded secret merged to main | Secret present in test fixture or config file; reviewer did not run secret-scanning tool | Run `git log -p` through a secret scanner (truffleHog, gitleaks) as a mandatory pre-review step |
| IDOR (insecure direct object reference) missed | Reviewer checked authentication but not authorisation; endpoint returns other users' data when ID is guessed | For every endpoint that accepts a user-controlled ID, verify the query explicitly filters by the authenticated user's ID |
| Dependency with known CVE approved | Reviewer audited first-party code only; transitive dependency vulnerability not visible in the diff | Run `npm audit` / `pip-audit` / `cargo audit` as part of every security review; block on HIGH or CRITICAL findings |
| Rate limiting gap on newly added endpoint | Rate limiting applied globally but new endpoint registered on a different router that bypasses global middleware | Verify every new endpoint is covered by rate limiting; add an integration test that sends 100 requests and expects 429 |

## Self-Verification Checklist

- [ ] All OWASP Top 10 categories checked: `grep -c "OWASP\|A0[1-9]\|A10" security_review.md` returns >= 10
- [ ] `npm audit --audit-level=high` (or `bun pm untrusted`) exits 0 — 0 high/critical dependency findings
- [ ] No hardcoded secrets: `grep -rn "sk-\|Bearer \|password\s*=\|secret\s*=" src/` returns = 0 matches
- [ ] All user-controlled input validated: `grep -c "sanitize\|validate\|escape\|parameterized" src/` returns > 0
- [ ] Auth tokens use secure generation with expiration: `grep -c "expiresIn\|exp\|ttl\|crypto\.random" src/auth/` returns > 0
- [ ] Error responses do not leak internals: `grep -rn "stack\|stackTrace\|schema\|column_name" src/errors/` returns = 0 matches
- [ ] HTTP security headers present: `grep -c "helmet\|CSP\|HSTS\|X-Frame-Options" src/` returns > 0

## Success Criteria

This task is complete when:
1. A Security Audit Report exists with findings categorized by severity (Critical/High/Medium/Low)
2. All Critical and High findings have either been fixed or have an accepted-risk decision recorded
3. OWASP Top 10 checklist is completed with evidence for each item
