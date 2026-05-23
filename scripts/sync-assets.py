#!/usr/bin/env python
"""Sync .agent/ (development source) -> src/mega_mind/assets/ (distribution source).

Copies all updated files while preserving:
  - hooks/hooks.json (only in assets, not in .agent/)
  - __pycache__ (local build artifacts)
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = ROOT / ".agent"
ASSETS_DIR = ROOT / "src" / "mega_mind" / "assets"


def sync_dir(src, dst, label):
    """Copy all files from src to dst, creating dirs as needed."""
    if not src.exists():
        print(f"  SKIP {label}: {src} does not exist")
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        dest = dst / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)
        count += 1
    print(f"  {label}: {count} files synced")
    return count


def main():
    print("Syncing .agent/ -> src/mega_mind/assets/")
    print("=" * 50)

    total = 0

    # Sync AGENTS.md
    shutil.copy2(AGENT_DIR / "AGENTS.md", ASSETS_DIR / "AGENTS.md")
    print("  AGENTS.md: 1 file synced")
    total += 1

    # Sync agents
    total += sync_dir(AGENT_DIR / "agents", ASSETS_DIR / "agents", "agents")

    # Sync shared
    total += sync_dir(AGENT_DIR / "shared", ASSETS_DIR / "shared", "shared")

    # Sync skills
    total += sync_dir(AGENT_DIR / "skills", ASSETS_DIR / "skills", "skills")

    # Sync workflows
    total += sync_dir(AGENT_DIR / "workflows", ASSETS_DIR / "workflows", "workflows")

    # Preserve hooks (only in assets, not in .agent/)
    hooks_src = ASSETS_DIR / "hooks" / "hooks.json"
    if hooks_src.exists():
        print("  hooks: preserved (1 file, not in .agent/)")

    print(f"\nTotal: {total} files synced")

    # Verify counts match
    agent_agents = len(list((AGENT_DIR / "agents").rglob("*.md")))
    asset_agents = len(list((ASSETS_DIR / "agents").rglob("*.md")))
    agent_skills = len(list((AGENT_DIR / "skills").rglob("SKILL.md")))
    asset_skills = len(list((ASSETS_DIR / "skills").rglob("SKILL.md")))
    agent_workflows = len(list((AGENT_DIR / "workflows").rglob("*.md")))
    asset_workflows = len(list((ASSETS_DIR / "workflows").rglob("*.md")))

    print("\nVerification:")
    print(
        f"  agents:    .agent/ = {agent_agents},  assets/ = {asset_agents}  {'OK' if agent_agents == asset_agents else 'MISMATCH'}"
    )
    print(
        f"  skills:    .agent/ = {agent_skills},  assets/ = {asset_skills}  {'OK' if agent_skills == asset_skills else 'MISMATCH'}"
    )
    print(
        f"  workflows: .agent/ = {agent_workflows},  assets/ = {asset_workflows}  {'OK' if agent_workflows == asset_workflows else 'MISMATCH'}"
    )

    all_match = (
        agent_agents == asset_agents
        and agent_skills == asset_skills
        and agent_workflows == asset_workflows
    )
    return 0 if all_match else 1


if __name__ == "__main__":
    sys.exit(main())
