#!/usr/bin/env python3
"""Generate .agent/shared/skills-manifest.json — the single source of truth for
the skill inventory.

Walks .agent/skills/*/SKILL.md, parses YAML frontmatter and the heading tree,
and emits a machine-readable manifest with per-skill metadata, content hashes,
and gold-standard section compliance. The validator, renderer, installer, and
docs all consume this file; docs can never disagree with it again.

Usage:
    python scripts/build-manifest.py            # regenerate manifest
    python scripts/build-manifest.py --check    # fail if manifest is stale
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = ROOT / ".agent"
SKILLS_DIR = AGENT_DIR / "skills"
MANIFEST_PATH = AGENT_DIR / "shared" / "skills-manifest.json"

SCHEMA_VERSION = "2.0"

# Ordered — also determines the manifest's category key order (a set would
# randomize iteration order across processes via hash randomization and make
# --check flaky).
VALID_CATEGORIES = [
    "core-workflow",
    "domain-expert",
    "meta-learning",
    "token-optimization",
]

# The 12 canonical sections of the Gold Standard SKILL.md v2.0 spec
# (.agent/shared/GOLD-STANDARD-SKILL.md). Heading variants are tolerated:
# "Core Principles (ALWAYS APPLY)" counts as "Core Principles".
CANONICAL_SECTIONS = [
    "Identity",
    "When to Use",
    "When NOT to Use",
    "Core Principles",
    "Instructions",
    "Blocking Violations (NEVER)",
    "Verification",
    "Performance & Cost",
    "Examples",
    "Anti-Patterns",
    "References",
    "Changelog",
]

SECTION_ALIASES = {
    "Core Principles (ALWAYS APPLY)": "Core Principles",
}

# Skills that are invoked by other skills rather than routed by the matrix.
# A skill may be listed here only if it also appears in another skill's
# `dependencies` frontmatter.
ROUTING_EXEMPT = ["rtk", "content-hash-cache-pattern", "mega-mind"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_of(path: Path) -> str:
    """Content hash with line endings normalized (CRLF == LF).

    Git may check the tree out with different line endings per platform, so a
    hash over raw bytes would differ between Windows and Linux checkouts.
    """
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split frontmatter (---\n...\n---) from body; parse keys crudely.

    Returns (dict of key -> raw value, body). Values are kept as strings or
    lists of strings — enough for the manifest, and dependency-free.
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text, body = parts[1], parts[2]
    fm: dict = {}
    key = None
    for line in fm_text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if key is not None and isinstance(fm.get(key), list):
                fm[key].append(line.strip().lstrip("-").strip().strip('"'))
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key, raw = m.group(1), m.group(2).strip()
            if raw == "|":
                fm[key] = []
            elif raw:
                fm[key] = raw.strip('"')
            else:
                fm[key] = []
    return fm, body


def section_compliance(body: str) -> dict[str, bool]:
    """Map each canonical section name to whether the skill defines it.

    Section 5 of the spec is "Instructions / Workflow": the how-to content may
    live under a domain-specific heading (e.g. "The Protocol", "Phase 1: ...",
    "The 6-Phase Verification Loop") instead of the literal "Instructions", so
    any operational (non-canonical) ## heading satisfies it.
    """
    headings = set()
    for m in re.finditer(r"^##\s+(.+)$", body, re.M):
        h = m.group(1).strip()
        headings.add(SECTION_ALIASES.get(h, h))
    canonical = set(CANONICAL_SECTIONS)
    compliance = {s: s in headings for s in CANONICAL_SECTIONS}
    compliance["Instructions"] = compliance["Instructions"] or any(
        h not in canonical for h in headings
    )
    return compliance


def build_skill_entry(path: Path) -> dict:
    text = read(path)
    fm, body = parse_frontmatter(text)
    name = path.parent.name
    title_m = re.search(r"^#\s+(.+)$", body, re.M)
    sections = section_compliance(body)
    return {
        "name": name,
        "title": title_m.group(1).strip() if title_m else name,
        "category": fm.get("category", ""),
        "version": fm.get("version", ""),
        "description": " ".join(fm.get("description", [])).strip()
        if isinstance(fm.get("description"), list)
        else str(fm.get("description", "")),
        "triggers": fm.get("triggers", []) or [],
        "dependencies": fm.get("dependencies", []) or [],
        "sha256": sha256_of(path),
        "line_count": text.count("\n") + 1,
        "sections": sections,
        "missing_sections": [s for s, ok in sections.items() if not ok],
    }


def build_manifest() -> dict:
    skills = []
    for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        skills.append(build_skill_entry(path))

    categories: dict[str, list[str]] = {c: [] for c in VALID_CATEGORIES}
    for entry in skills:
        categories.setdefault(entry["category"], []).append(entry["name"])
    for names in categories.values():
        names.sort()

    return {
        "schema_version": SCHEMA_VERSION,
        "spec": "Gold Standard SKILL.md v2.0",
        "canonical_sections": CANONICAL_SECTIONS,
        "routing_exempt": sorted(ROUTING_EXEMPT),
        "categories": categories,
        "skill_count": len(skills),
        "skills": skills,
    }


def main() -> int:
    manifest = build_manifest()
    payload = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    if "--check" in sys.argv:
        if MANIFEST_PATH.exists() and MANIFEST_PATH.read_text(encoding="utf-8") == payload:
            print(f"[OK] skills-manifest.json is fresh ({manifest['skill_count']} skills)")
            return 0
        print(
            f"[STALE] {MANIFEST_PATH.relative_to(ROOT)} is out of date — "
            "run `python scripts/build-manifest.py` to regenerate.",
            file=sys.stderr,
        )
        return 1

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(payload, encoding="utf-8")
    print(
        f"[OK] wrote {MANIFEST_PATH.relative_to(ROOT)} "
        f"({manifest['skill_count']} skills, schema {SCHEMA_VERSION})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
