#!/bin/bash

# Mega-Mind Skills Test Runner
# Run this to validate the skill setup

echo "🧪 Running Mega-Mind Skills Tests..."
echo ""

PASS=0
FAIL=0

# Define directories first
SKILLS_DIR="$(dirname "$0")/../skills"
WORKFLOWS_DIR="$(dirname "$0")/../workflows"
AGENTS_DIR="$(dirname "$0")/../agents"
AGENTS_MD="$(dirname "$0")/../AGENTS.md"

# Test 0: Check Mega-Mind Orchestrator
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 0: Checking Mega-Mind Orchestrator..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$SKILLS_DIR/mega-mind/SKILL.md" ]; then
  echo "  ✅ mega-mind (Orchestrator)"
  ((PASS++))
else
  echo "  ❌ mega-mind (MISSING - Critical!)"
  ((FAIL++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Checking core workflow skills..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

CORE_SKILLS=(
  "brainstorming"
  "writing-plans"
  "executing-plans"
  "single-flow-task-execution"
  "test-driven-development"
  "systematic-debugging"
  "requesting-code-review"
  "receiving-code-review"
  "verification-before-completion"
  "finishing-a-development-branch"
  "using-git-worktrees"
  "using-mega-mind"
  "writing-skills"
)

for skill in "${CORE_SKILLS[@]}"; do
  if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
    echo "  ✅ $skill"
    ((PASS++))
  else
    echo "  ❌ $skill (MISSING)"
    ((FAIL++))
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Checking domain expert skills..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DOMAIN_SKILLS=(
  "tech-lead"
  "doc-writer"
  "bug-hunter"
  "test-genius"
  "code-polisher"
  "security-reviewer"
  "performance-profiler"
  "migration-upgrader"
  "ci-config-helper"
  "infra-architect"
  "api-designer"
  "data-engineer"
  "frontend-architect"
  "backend-architect"
  "docker-expert"
  "k8s-orchestrator"
  "data-analyst"
  "mobile-architect"
  "ml-engineer"
  "observability-specialist"
  "ux-designer"
  "product-manager"
  "e2e-test-specialist"
  "search-vector-architect"
  "workflow-orchestrator"
  "legacy-archaeologist"
  "skill-generator"
  "rtk"
)

for skill in "${DOMAIN_SKILLS[@]}"; do
  if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
    echo "  ✅ $skill"
    ((PASS++))
  else
    echo "  ❌ $skill (MISSING)"
    ((FAIL++))
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Checking workflows..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

WORKFLOWS=(
  "brainstorm.md"
  "execute-plan.md"
  "write-plan.md"
  "debug.md"
  "review.md"
  "ship.md"
)

for workflow in "${WORKFLOWS[@]}"; do
  if [ -f "$WORKFLOWS_DIR/$workflow" ]; then
    echo "  ✅ $workflow"
    ((PASS++))
  else
    echo "  ❌ $workflow (MISSING)"
    ((FAIL++))
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Checking agents..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AGENTS=(
  "code-reviewer.md"
  "tech-lead.md"
  "qa-engineer.md"
)

for agent in "${AGENTS[@]}"; do
  if [ -f "$AGENTS_DIR/$agent" ]; then
    echo "  ✅ $agent"
    ((PASS++))
  else
    echo "  ❌ $agent (MISSING)"
    ((FAIL++))
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 5: Checking AGENTS.md..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$AGENTS_MD" ]; then
  echo "  ✅ AGENTS.md exists"
  ((PASS++))

  # Check for key sections
  if grep -q "Session Rules" "$AGENTS_MD"; then
    echo "  ✅ AGENTS.md has Session Rules"
    ((PASS++))
  else
    echo "  ❌ AGENTS.md missing Session Rules"
    ((FAIL++))
  fi

  if grep -q "Skill Routing" "$AGENTS_MD"; then
    echo "  ✅ AGENTS.md has Skill Routing"
    ((PASS++))
  else
    echo "  ❌ AGENTS.md missing Skill Routing"
    ((FAIL++))
  fi
else
  echo "  ❌ AGENTS.md (MISSING)"
  ((FAIL++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 6: Checking skill frontmatter..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check a sample of skills for proper frontmatter (including mega-mind)
SAMPLE_SKILLS=("mega-mind" "brainstorming" "tech-lead" "bug-hunter" "docker-expert")

for skill in "${SAMPLE_SKILLS[@]}"; do
  SKILL_FILE="$SKILLS_DIR/$skill/SKILL.md"
  if [ -f "$SKILL_FILE" ]; then
    if head -10 "$SKILL_FILE" | grep -q "^name:"; then
      echo "  ✅ $skill has valid frontmatter"
      ((PASS++))
    else
      echo "  ❌ $skill missing valid frontmatter"
      ((FAIL++))
    fi
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 TEST RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  ✅ Passed: $PASS"
echo "  ❌ Failed: $FAIL"
echo "  📋 Total:  $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
  echo "🎉 All tests passed! Mega-Mind is ready to use."
  exit 0
else
  echo "⚠️  Some tests failed. Please check the missing components."
  exit 1
fi
