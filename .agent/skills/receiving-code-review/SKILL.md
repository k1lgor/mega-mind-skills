---
name: receiving-code-review
description: Handling feedback systematically. Use when you receive code review feedback.
triggers:
  - "got review feedback"
  - "addressing review comments"
  - "responding to review"
---

# Receiving Code Review Skill

## When to Use

- After receiving code review feedback
- When addressing review comments
- When responding to requested changes

## Instructions

### Step 1: Read and Understand

1. **Read all comments** before responding
2. **Understand the intent** behind each comment
3. **Categorize feedback** by type:
   - Must fix (blocking issues)
   - Should fix (important improvements)
   - Consider (suggestions)
   - Questions (need clarification)

### Step 2: Respond Professionally

For each comment:

```markdown
**Status:** [Addressed / Discussing / Won't Fix]

**Response:**
[Your explanation or the fix applied]

**Change:** (if applicable)
[Link to the commit or describe the change]
```

### Step 3: Make Changes

1. **Create a checklist** of items to address
2. **Fix issues** in logical groups
3. **Add new tests** if needed
4. **Self-review** again before pushing

### Step 4: Follow Up

1. **Mark conversations resolved**
2. **Request re-review** if significant changes
3. **Thank reviewers** for their time

## Feedback Categories and Responses

### Must Fix (Blocking)

```markdown
**Comment:** "This has a security vulnerability - user input isn't validated"

**Response:**
✅ **Addressed**
Added input validation using the validateInput middleware. All user-provided strings are now sanitized.

**Change:** Commit abc123
```

### Should Fix (Important)

```markdown
**Comment:** "This function is doing too much - consider breaking it up"

**Response:**
✅ **Addressed**
Split into three smaller functions: parseInput, validateData, and saveRecord. Each has a single responsibility.

**Change:** Commit def456
```

### Consider (Suggestion)

```markdown
**Comment:** "Could use a more descriptive variable name"

**Response:**
✅ **Addressed**
Renamed `x` to `processedItemCount` for clarity.

**Alternative:** Kept as is because this is a loop iterator and `i` is conventional. Open to changing if you feel strongly.
```

### Questions

```markdown
**Comment:** "Why did you choose this approach?"

**Response:**
🤔 **Discussing**
I chose this approach because:

1. It's consistent with the existing pattern
2. It's more performant for our use case
3. It's easier to test

Happy to discuss alternatives if you have concerns.
```

## Response Templates

### Agreeing and Fixing

```
Good catch! Fixed in [commit]. The [change] now [improvement].
```

### Explaining the Choice

```
I chose this approach because [reason]. The main benefit is [benefit]. I considered [alternative] but went with this because [why this is better].
```

### Requesting Clarification

```
Could you elaborate on [aspect]? I want to make sure I understand the concern correctly before making changes.
```

### Politely Disagreeing

```
I appreciate the feedback. I considered this but decided against it because [reason]. If you feel strongly about this, I'm happy to discuss further and potentially revise.
```

## Checklist for Addressing Feedback

```markdown
## Review Response Checklist

### Critical Issues

- [ ] Issue 1: [Description] - Fixed in commit X
- [ ] Issue 2: [Description] - Fixed in commit Y

### Suggestions

- [ ] Suggestion 1: Implemented
- [ ] Suggestion 2: Discussed and agreed to defer

### Questions

- [ ] Question 1: Answered
- [ ] Question 2: Clarified

### Self-Review After Changes

- [ ] All tests still pass
- [ ] New code follows style guide
- [ ] No new issues introduced
```

## Example Response Session

```markdown
## Review Response for PR #456

### Must Fix Items

**Comment 1:** SQL injection risk on line 45
✅ **Addressed** - Added parameterized query. Commit: a1b2c3

**Comment 2:** Missing error handling
✅ **Addressed** - Added try/catch with proper error logging. Commit: d4e5f6

### Suggestions

**Comment 3:** Consider using async/await
✅ **Addressed** - Refactored to async/await for better readability. Commit: g7h8i9

**Comment 4:** Add more descriptive names
🤔 **Discussing** - I kept the short names because they're local loop variables. Open to changing if you prefer longer names.

### Follow-up

- [ ] All critical items addressed
- [ ] Tests pass
- [ ] Ready for re-review

Thanks for the thorough review! Please let me know if you have any other concerns.
```

## Tips

- Don't take feedback personally
- Assume positive intent from reviewers
- Address all comments - don't skip any
- Ask for clarification if you don't understand
- Thank reviewers for catching issues
- Learn from patterns in feedback
