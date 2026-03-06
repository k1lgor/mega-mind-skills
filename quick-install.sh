#!/bin/bash

# Quick Install Script for Antigravity IDE
# Run this from your project directory

set -e

echo "🧠 Mega-Mind Quick Install"
echo "=========================="
echo ""

# Check if we're being run with a target directory
TARGET="${1:-$(pwd)}"

# Get the source directory
SOURCE="$(cd "$(dirname "$0")" && pwd)"

echo "Target: $TARGET"
echo "Source: $SOURCE"
echo ""

# Check if mega-mind-skills exists
if [ ! -d "$SOURCE/.agent" ]; then
  echo "❌ Error: Cannot find .agent directory"
  echo "   Make sure you're running from mega-mind-skills directory"
  exit 1
fi

# Create target .agent directory
mkdir -p "$TARGET/.agent"

# Copy everything
echo "📦 Copying files..."
cp -r "$SOURCE/.agent/"* "$TARGET/.agent/"

# Make scripts executable
chmod +x "$TARGET/.agent/tests/run-tests.sh" 2>/dev/null || true

echo ""
echo "✅ Done! Mega-Mind skills installed to $TARGET/.agent/"
echo ""
echo "Quick commands:"
echo "  /mega-mind  - Main orchestrator"
echo "  /brainstorm - Explore ideas"
echo "  /plan       - Create plan"
echo "  /execute    - Execute plan"
echo "  /debug      - Fix bugs"
echo "  /ship       - Deploy"
