#!/usr/bin/env python
"""Normalize headings across all skills:
## When to Activate  ->  ## When to Use
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".agent" / "skills"

REPLACEMENTS = {
    "## When to Activate": "## When to Use",
}


def fix_file(path):
    content = open(path, encoding="utf-8").read()
    original = content
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
    if content != original:
        open(path, "w", encoding="utf-8").write(content)
        return True
    return False


def main():
    fixed = []
    not_fixed = []
    for f in sorted(SKILLS_DIR.rglob("SKILL.md")):
        if fix_file(f):
            fixed.append(f.parent.name)
        else:
            not_fixed.append(f.parent.name)

    print(f"Fixed {len(fixed)} files:")
    for s in fixed:
        print(f"  {s}")
    print(f"\nNo change ({len(not_fixed)} files): all headings already canonical")
    return 0


if __name__ == "__main__":
    sys.exit(main())
