#!/usr/bin/env python
"""Fix grep patterns for POSIX portability across all SKILL.md files.
Changes:
  grep -FLAGS "a\\|b"  ->  grep -FLAGSE "a|b"  (add -E, replace \\| with |)
  grep -FLAGSE "a|b"   ->  grep -FLAGSE "a|b"  (already fixed)
  \\s  ->  [[:space:]]  (in grep patterns only)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".agent" / "skills"


def fix_file(path):
    content = open(path, encoding="utf-8").read()
    original = content
    lines = content.split("\n")
    new_lines = []
    changes = 0

    for line in lines:
        new_line = line
        # Match: grep -FLAGS "pattern1\\|pattern2"
        # We need to find grep commands with alternation \|
        if "grep" in line:
            # Pattern for grep with \| inside quotes
            # Handle: grep -rn "a\|b"  ->  grep -rnE "a|b"
            m = re.search(r'(grep\s+)(-[a-zA-Z]+)(\s+)"([^"]*\\\|[^"]*)"', line)
            if m:
                prefix = m.group(1)
                flags = m.group(2)
                pattern = m.group(4)
                new_pattern = pattern.replace("\\|", "|")
                if "E" not in flags:
                    new_flags = flags + "E"
                else:
                    new_flags = flags
                new_line = prefix + new_flags + ' "' + new_pattern + '"'
                changes += 1

            # Fix \s -> [[:space:]] inside grep commands
            if "grep" in new_line and "\\s" in new_line:
                new_line = new_line.replace("\\s", "[[:space:]]")

            # Fix \b -> (remove, only in grep context)
            if "grep" in new_line and "\\b" in new_line:
                new_line = new_line.replace("\\b", "")

        new_lines.append(new_line)

    new_content = "\n".join(new_lines)
    if new_content != original:
        open(path, "w", encoding="utf-8").write(new_content)
    return changes


def main():
    total = 0
    fixed_files = 0
    for f in sorted(SKILLS_DIR.rglob("SKILL.md")):
        c = fix_file(f)
        if c > 0:
            print(f"  Fixed {c} patterns in {f.parent.name}")
            fixed_files += 1
        total += c
    print(f"\nTotal: {total} patterns fixed across {fixed_files} files")
    return 0 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
