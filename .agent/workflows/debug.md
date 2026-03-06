---
description:
---

# Debug Workflow

## Trigger

Use when encountering bugs or errors.

**Quick Start:** `/mega-mind route "bug description"` or `/debug`

## Steps

### 1. Reproduce the Bug

- Document exact steps to trigger
- Identify expected vs actual behavior
- Note environmental factors

### 2. Gather Evidence

- Check logs
- Check recent changes
- Check dependencies
- Check environment

### 3. Form Hypothesis

Based on evidence:

- Create specific hypothesis
- Design experiment to test
- Run experiment

### 4. Fix and Verify

- Implement fix
- Add regression test
- Verify fix works
- Check for side effects

## Next Steps After Debugging

After completing this workflow, typically continue with:

```
/tdd → Write regression tests
/verify → Verify the fix works
/ship → Deploy the fix
```

Or use:

```
/mega-mind execute ship
```

## Output

- Root cause analysis
- Fix implementation
- Regression test
- Updated documentation if needed

## Related Skills

- `systematic-debugging` - The core debugging skill
- `bug-hunter` - Finding root causes
- `test-driven-development` - Writing regression tests
- `verification-before-completion` - Verify before done
