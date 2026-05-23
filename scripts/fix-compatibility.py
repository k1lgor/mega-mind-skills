#!/usr/bin/env python
"""Normalize compatibility frontmatter across ALL .agent/ files.

Every skill, agent, and workflow must declare the same broad compatibility
line so no coding agent is excluded.

The canonical line (from README.md):
  Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor,
  OpenCode, Codex, pi, and all tools supporting the Agent Skills standard)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = ROOT / ".agent"

CANONICAL = "Any AI coding agent (Antigravity, Claude Code, Copilot, Cursor, OpenCode, Codex, pi, and all tools supporting the Agent Skills open standard)"


def fix_file(path, is_skill=True, is_agent=False, is_workflow=False):
    """Add or replace compatibility field in frontmatter."""
    content = open(path, encoding="utf-8").read()
    original = content

    if not content.startswith("---"):
        return False  # no frontmatter (shared snippets)

    if is_skill or is_agent or is_workflow:
        # Replace existing compatibility line, or add after name/description/tools
        if re.search(r"^compatibility:", content, re.MULTILINE):
            content = re.sub(
                r"^compatibility:.*$",
                f"compatibility: {CANONICAL}",
                content,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            # Add after the first line of frontmatter (after ---)
            # For agents: after tools:
            # For skills: after name: line
            # For workflows: after description: line
            if is_agent:
                content = re.sub(
                    r"^(tools:.+)$",
                    f"\\1\ncompatibility: {CANONICAL}",
                    content,
                    count=1,
                    flags=re.MULTILINE,
                )
            elif is_workflow:
                content = re.sub(
                    r"^(description:.+)$",
                    f"\\1\ncompatibility: {CANONICAL}",
                    content,
                    count=1,
                    flags=re.MULTILINE,
                )
            elif is_skill:
                content = re.sub(
                    r"^(name:.+)$",
                    f"\\1\ncompatibility: {CANONICAL}",
                    content,
                    count=1,
                    flags=re.MULTILINE,
                )

    if content != original:
        open(path, "w", encoding="utf-8").write(content)
        return True
    return False


def main():
    fixed = []

    # Skills (53 files)
    for f in sorted((AGENT_DIR / "skills").rglob("SKILL.md")):
        if fix_file(f, is_skill=True):
            fixed.append(f"s  {f.parent.name}")

    # Agents (6 files)
    for f in sorted((AGENT_DIR / "agents").rglob("*.md")):
        if fix_file(f, is_agent=True):
            fixed.append(f"a  {f.parent.name}/{f.name}")

    # Workflows (7 files)
    for f in sorted((AGENT_DIR / "workflows").rglob("*.md")):
        if fix_file(f, is_workflow=True):
            fixed.append(f"w  {f.stem}")

    print(f"Fixed {len(fixed)} files:")
    for f in fixed:
        print(f"  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
