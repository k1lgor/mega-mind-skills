---
name: security-reviewer
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
npm audit

# Fix automatically
npm audit fix

# Check before installing
npm audit package-name
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
