#!/bin/bash

# Mega-Mind Skills Installation Script for Antigravity IDE
# Usage: ./install.sh [project-path]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🧠 MEGA-MIND SKILLS INSTALLER                              ║"
echo "║   Unified Superpowers + Virtual Company for Antigravity IDE  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Determine target directory
if [ -z "$1" ]; then
  TARGET_DIR="$(pwd)"
else
  TARGET_DIR="$1"
fi

# Resolve to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
  echo -e "${RED}Error: Directory does not exist: $TARGET_DIR${NC}"
  exit 1
}

echo -e "${BLUE}Target directory: ${TARGET_DIR}${NC}"
echo ""

# Check if target is a project directory
if [ ! -f "$TARGET_DIR/package.json" ] && [ ! -f "$TARGET_DIR/go.mod" ] && [ ! -f "$TARGET_DIR/Cargo.toml" ] && [ ! -f "$TARGET_DIR/pyproject.toml" ]; then
  echo -e "${YELLOW}⚠️  Warning: Target doesn't appear to be a standard project directory.${NC}"
  echo -e "${YELLOW}   Installation will continue anyway.${NC}"
  echo ""
fi

# Find script directory (where mega-mind-skills is located)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"

# Check if source exists
if [ ! -d "$SOURCE_DIR/.agent" ]; then
  echo -e "${RED}Error: Cannot find .agent directory in $SOURCE_DIR${NC}"
  exit 1
fi

# Check for existing installation
if [ -d "$TARGET_DIR/.agent" ]; then
  echo -e "${YELLOW}⚠️  Existing .agent directory found at target.${NC}"
  echo ""
  echo -e "  Options:"
  echo -e "  ${CYAN}[b]${NC}ackup existing and install fresh"
  echo -e "  ${CYAN}[m]${NC}erge (keep existing, add missing files)"
  echo -e "  ${CYAN}[o]${NC}verwrite completely"
  echo -e "  ${CYAN}[c]${NC}ancel installation"
  echo ""
  read -p "  Choose option [b/m/o/c]: " choice

  case $choice in
    b|B)
      BACKUP_DIR="$TARGET_DIR/.agent.backup.$(date +%Y%m%d%H%M%S)"
      echo -e "${BLUE}Backing up existing .agent to $BACKUP_DIR${NC}"
      mv "$TARGET_DIR/.agent" "$BACKUP_DIR"
      ;;
    m|M)
      echo -e "${BLUE}Merging with existing installation...${NC}"
      MERGE=true
      ;;
    o|O)
      echo -e "${BLUE}Removing existing installation...${NC}"
      rm -rf "$TARGET_DIR/.agent"
      ;;
    c|C|*)
      echo -e "${YELLOW}Installation cancelled.${NC}"
      exit 0
      ;;
  esac
fi

# Installation
echo ""
echo -e "${GREEN}📦 Installing Mega-Mind Skills...${NC}"
echo ""

# Create directories
mkdir -p "$TARGET_DIR/.agent/skills"
mkdir -p "$TARGET_DIR/.agent/workflows"
mkdir -p "$TARGET_DIR/.agent/agents"
mkdir -p "$TARGET_DIR/.agent/tests"

# Copy AGENTS.md (master contract)
echo -e "${CYAN}  → Copying AGENTS.md (master contract)${NC}"
cp "$SOURCE_DIR/.agent/AGENTS.md" "$TARGET_DIR/.agent/"

# Copy all skills
echo -e "${CYAN}  → Copying skills (40 skills)${NC}"
for skill_dir in "$SOURCE_DIR/.agent/skills"/*/; do
  if [ -d "$skill_dir" ]; then
    skill_name=$(basename "$skill_dir")
    mkdir -p "$TARGET_DIR/.agent/skills/$skill_name"
    cp "$skill_dir"/* "$TARGET_DIR/.agent/skills/$skill_name/" 2>/dev/null || true
  fi
done

# Copy workflows
echo -e "${CYAN}  → Copying workflows${NC}"
cp "$SOURCE_DIR/.agent/workflows"/*.md "$TARGET_DIR/.agent/workflows/" 2>/dev/null || true

# Copy agents
echo -e "${CYAN}  → Copying agent profiles${NC}"
cp "$SOURCE_DIR/.agent/agents"/*.md "$TARGET_DIR/.agent/agents/" 2>/dev/null || true

# Copy tests
echo -e "${CYAN}  → Copying test scripts${NC}"
cp "$SOURCE_DIR/.agent/tests"/*.sh "$TARGET_DIR/.agent/tests/" 2>/dev/null || true
chmod +x "$TARGET_DIR/.agent/tests/"*.sh 2>/dev/null || true

# Create plans directory for task tracking
echo -e "${CYAN}  → Creating plans directory${NC}"
mkdir -p "$TARGET_DIR/docs/plans"

# Create initial task.md if it doesn't exist
if [ ! -f "$TARGET_DIR/docs/plans/task.md" ]; then
  cat > "$TARGET_DIR/docs/plans/task.md" << 'EOF'
# Task Tracker

| Task ID | Description | Status | Priority | Dependencies |
|---------|-------------|--------|----------|--------------|
| - | No tasks yet | - | - | - |

## Status Values
- `pending` - Not started
- `in_progress` - Currently working
- `completed` - Finished
- `blocked` - Waiting on something

## Priority Values
- `high` - Must complete soon
- `medium` - Normal priority
- `low` - Nice to have
EOF
  echo -e "${CYAN}  → Created initial task.md${NC}"
fi

# Make scripts executable
chmod +x "$TARGET_DIR/.agent/tests/run-tests.sh" 2>/dev/null || true

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run tests
echo -e "${BLUE}🧪 Running validation tests...${NC}"
echo ""
cd "$TARGET_DIR"
bash .agent/tests/run-tests.sh

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}📚 Quick Start Guide:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  1. Open your project in ${GREEN}Antigravity IDE${NC}"
echo -e "  2. The skills will be automatically loaded"
echo -e "  3. Use commands like:"
echo ""
echo -e "     ${YELLOW}/mega-mind${NC}         - Main orchestrator"
echo -e "     ${YELLOW}/brainstorm${NC}        - Explore approaches"
echo -e "     ${YELLOW}/plan${NC}              - Create implementation plan"
echo -e "     ${YELLOW}/execute${NC}           - Execute with tracking"
echo -e "     ${YELLOW}/debug${NC}             - Debug systematically"
echo -e "     ${YELLOW}/review${NC}            - Request code review"
echo -e "     ${YELLOW}/ship${NC}              - Deploy to production"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}📖 Documentation:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  • ${BLUE}README.md${NC}          - Full documentation"
echo -e "  • ${BLUE}.agent/AGENTS.md${NC}   - Master contract & rules"
echo -e "  • ${BLUE}.agent/skills/${NC}     - Individual skill files"
echo -e "  • ${BLUE}.agent/workflows/${NC}  - Workflow definitions"
echo ""
echo -e "${GREEN}🎉 Happy coding with Mega-Mind!${NC}"
