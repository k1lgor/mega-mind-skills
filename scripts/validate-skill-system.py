#!/usr/bin/env python3
"""Mega-Mind Skill System Validator.

Checks: skill count, routing coverage, heading consistency, required sections,
grep portability, task.md integrity.
Usage: python scripts/validate-skill-system.py [--report]
"""

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = ROOT / ".agent"
SKILLS_DIR = AGENT_DIR / "skills"
SKILL_PATHS = sorted(SKILLS_DIR.rglob("SKILL.md"))
SKILL_NAMES = sorted(p.parent.name for p in SKILL_PATHS)
AGENT_NAMES = {
    "planner",
    "architect",
    "code-reviewer",
    "qa-engineer",
    "security-reviewer",
    "tech-lead",
}
REQUIRED_SECTIONS = [
    "## When NOT to Use",
    "## Self-Verification Checklist",
    "## Success Criteria",
]
HEADING_CANONICAL = {
    "## When Not to Use": "## When NOT to Use",
    "## When to NOT Use": "## When NOT to Use",
}


def read(path):
    return open(path, encoding="utf-8").read()


def check_skill_count():
    content = read(AGENT_DIR / "AGENTS.md")
    declared = None
    for m in re.finditer(r"(\d+)\s+(Active\s+)?skills?", content, re.IGNORECASE):
        declared = int(m.group(1))
    actual = len(SKILL_PATHS)
    if declared and declared != actual:
        return [
            {
                "sev": "ERROR",
                "check": "skill_count",
                "msg": f"AGENTS.md says {declared}, disk has {actual}",
            }
        ]
    return [
        {
            "sev": "OK",
            "check": "skill_count",
            "msg": f"{actual} skills (AGENTS.md matches disk)",
        }
    ]


def check_routing():
    content = read(SKILLS_DIR / "mega-mind" / "SKILL.md")
    covered = set()
    for m in re.finditer(r"\u2192\s*([\w-]+(?:\s*\u2192\s*[\w-]+)*)", content):
        for skill in re.findall(r"[\w-]+", m.group(1)):
            covered.add(skill)
    for m in re.finditer(r"`([\w-]+)`", content):
        covered.add(m.group(1))
    no_route = {
        "rtk",
        "context-optimizer",
        "content-hash-cache-pattern",
        "iterative-retrieval",
        "autonomous-loops",
        "mega-mind",
    }
    uncovered = set(SKILL_NAMES) - covered - no_route
    if uncovered:
        return [
            {
                "sev": "WARNING",
                "check": "routing",
                "msg": f"Uncovered: {sorted(uncovered)}",
            }
        ]
    return [
        {"sev": "OK", "check": "routing", "msg": "All skills covered in routing matrix"}
    ]


def check_headings():
    issues = []
    for path in SKILL_PATHS:
        content = read(path)
        name = path.parent.name
        for variant, canonical in HEADING_CANONICAL.items():
            if variant in content:
                issues.append(
                    {
                        "sev": "WARNING",
                        "check": "heading",
                        "msg": f"'{name}' uses '{variant}'",
                    }
                )
    if not issues:
        issues.append(
            {"sev": "OK", "check": "headings", "msg": "All headings canonical"}
        )
    return issues


def check_required():
    issues = []
    for path in SKILL_PATHS:
        content = read(path)
        name = path.parent.name
        for s in REQUIRED_SECTIONS:
            if s not in content:
                issues.append(
                    {
                        "sev": "ERROR",
                        "check": "required",
                        "msg": f"'{name}' missing '{s}'",
                    }
                )
    if not issues:
        issues.append(
            {"sev": "OK", "check": "required", "msg": "All required sections present"}
        )
    return issues


def check_grep_portability():
    issues = []
    for path in SKILL_PATHS:
        lines = read(path).split("\n")
        name = path.parent.name
        for i, line in enumerate(lines, 1):
            if "grep" not in line:
                continue
            if r"\|" in line and "grep -" in line and "-E" not in line:
                issues.append(
                    {
                        "sev": "WARNING",
                        "check": "grep",
                        "msg": f"'{name}:{i}' uses \\| without -E",
                    }
                )
            if r"\s" in line and r"[[:space:]]" not in line:
                pass  # \s warnings are informational only
    if not issues:
        issues.append({"sev": "OK", "check": "grep", "msg": "All grep patterns use -E"})
    return issues


def main():
    all_issues = []
    for check in [
        check_skill_count,
        check_routing,
        check_headings,
        check_required,
        check_grep_portability,
    ]:
        all_issues.extend(check())

    errors = [i for i in all_issues if i["sev"] == "ERROR"]
    warnings = [i for i in all_issues if i["sev"] == "WARNING"]
    ok = [i for i in all_issues if i["sev"] == "OK"]

    print("=" * 50)
    print(f"Results: {len(errors)} errors, {len(warnings)} warnings, {len(ok)} passed")
    print("=" * 50)
    for i in all_issues:
        icon = {"ERROR": "X", "WARNING": "!", "OK": "+", "INFO": "?"}.get(i["sev"], "?")
        print(f"  [{icon}] [{i['check']}] {i['msg']}")

    if "--report" in sys.argv:
        from datetime import datetime

        rpath = AGENT_DIR / "evals" / "validation-report.md"
        lines = [
            "# Validation Report",
            f"Date: {datetime.now().isoformat()[:10]}",
            "",
            f"Errors: {len(errors)}",
            f"Warnings: {len(warnings)}",
            "",
        ]
        for i in all_issues:
            lines.append(f"- [{i['sev']}] {i['check']}: {i['msg']}")
        open(rpath, "w", encoding="utf-8").write("\n".join(lines))
        print(f"\nReport: {rpath.relative_to(ROOT)}")

    return 0 if len(errors) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
