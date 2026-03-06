---
name: verification-before-completion
description: Prove it works before claiming it's done. Use before marking any task complete.
triggers:
  - "mark as done"
  - "complete this task"
  - "is this done"
  - "verify this works"
---

# Verification Before Completion Skill

## When to Use

- Before marking any task as complete
- Before closing a PR
- Before saying "I'm done"
- Before merging to main

## Verification Protocol

### Step 1: Run Tests

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests (if applicable)
npm run test:e2e

# Check coverage
npm run test:coverage
```

**All tests must pass.** If any test fails, the task is not complete.

### Step 2: Run Linters and Type Checks

```bash
# Lint
npm run lint

# Type check (TypeScript)
npm run type-check

# Format check
npm run format:check
```

**No errors allowed.** Warnings should be addressed or documented.

### Step 3: Build Check

```bash
# Build
npm run build

# Production build
npm run build:prod
```

**Build must succeed without errors.**

### Step 4: Manual Verification

Actually use the feature:

```markdown
## Manual Verification Checklist

- [ ] Feature works as expected
- [ ] Edge cases handled
- [ ] Error states are graceful
- [ ] Loading states are appropriate
- [ ] Mobile/responsive (if applicable)
- [ ] Accessibility (if applicable)
- [ ] No console errors
- [ ] No unexpected warnings
```

### Step 5: Integration Check

Verify the change doesn't break other parts:

- [ ] Related features still work
- [ ] Navigation still works
- [ ] API integrations still work
- [ ] Database operations still work

## Verification Template

```markdown
# Verification Report: [Task Name]

## Date: [Date]

## Verifier: [Name]

### Automated Checks

| Check             | Status  | Notes                 |
| ----------------- | ------- | --------------------- |
| Unit tests        | ✅ PASS | 145 tests, 0 failures |
| Integration tests | ✅ PASS | 23 tests, 0 failures  |
| Lint              | ✅ PASS | No errors             |
| Type check        | ✅ PASS | No errors             |
| Build             | ✅ PASS | Build succeeded       |
| Coverage          | ✅ PASS | 87% (target: 80%)     |

### Manual Verification

- [x] Feature works correctly
- [x] Edge cases handled
- [x] No console errors
- [x] Responsive design works

### Integration Check

- [x] Related feature A works
- [x] Related feature B works
- [x] Navigation works
- [x] API calls work

### Issues Found

- None

### Conclusion

✅ **VERIFIED** - Task is complete and ready for merge.
```

## Common Verification Failures

### Tests Failing

```markdown
**Issue:** 2 tests failing in user.service.test.ts

**Root Cause:** New field added to User model not reflected in test fixtures

**Fix:** Updated test fixtures to include new field

**Verification:** Re-ran tests - all pass
```

### Build Failing

```markdown
**Issue:** TypeScript build error - Type 'string | undefined' is not assignable to type 'string'

**Root Cause:** Optional field not handled in new code

**Fix:** Added null check with default value

**Verification:** Build succeeds
```

### Manual Verification Failure

```markdown
**Issue:** Feature works but shows console error

**Root Cause:** Missing error boundary

**Fix:** Added error boundary component

**Verification:** No console errors
```

## Decision Matrix

| Tests Pass | Lint Clean | Build OK | Manual OK | Result       |
| ---------- | ---------- | -------- | --------- | ------------ |
| ❌         | -          | -        | -         | **NOT DONE** |
| ✅         | ❌         | -        | -         | **NOT DONE** |
| ✅         | ✅         | ❌       | -         | **NOT DONE** |
| ✅         | ✅         | ✅       | ❌        | **NOT DONE** |
| ✅         | ✅         | ✅       | ✅        | **DONE**     |

## Tips

- Run verification multiple times during development
- Don't skip manual testing - automated tests don't catch everything
- Check in different environments if possible
- Have someone else test if possible
- Document any known issues for future work
