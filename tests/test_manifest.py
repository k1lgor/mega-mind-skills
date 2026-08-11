"""End-to-end checks for the manifest + validator + renderer pipeline.

These tests run the repo's own scripts as subprocesses so the real entry
points are exercised (the script files are hyphenated and not importable).
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_script(name: str, *args: str):
    return subprocess.run(
        [sys.executable, f"scripts/{name}", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def load_manifest() -> dict:
    return json.loads(
        (ROOT / ".agent" / "shared" / "skills-manifest.json").read_text(encoding="utf-8")
    )


def test_manifest_is_fresh():
    result = run_script("build-manifest.py", "--check")
    assert result.returncode == 0, result.stderr


def test_manifest_is_internally_consistent():
    m = load_manifest()
    assert m["skill_count"] == len(m["skills"]) == 53
    assert sum(len(v) for v in m["categories"].values()) == m["skill_count"]
    for entry in m["skills"]:
        assert entry["name"] in m["categories"][entry["category"]]
        assert entry["missing_sections"] == [], f"{entry['name']} missing sections"


def test_manifest_hashes_match_disk():
    import hashlib

    m = load_manifest()
    for entry in m["skills"]:
        path = ROOT / ".agent" / "skills" / entry["name"] / "SKILL.md"
        assert path.exists()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]


def test_generated_regions_are_fresh():
    result = run_script("render-skills.py", "--check")
    assert result.returncode == 0, result.stderr


def test_generated_regions_embedded():
    text = (ROOT / ".agent" / "skills" / "mega-mind" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "BEGIN GENERATED: routing-matrix" in text
    assert "END GENERATED: routing-matrix" in text
    assert "BEGIN GENERATED: skills-listing" in text
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "BEGIN GENERATED: skill-inventory" in readme


def test_validator_passes():
    result = run_script("validate-skill-system.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_routing_data_resolves():
    m = load_manifest()
    routing = json.loads(
        (ROOT / ".agent" / "shared" / "routing.json").read_text(encoding="utf-8")
    )
    skill_names = {s["name"] for s in m["skills"]}
    agent_names = {p.stem for p in (ROOT / ".agent" / "agents").glob("*.md")}
    targets = skill_names | agent_names
    for route in routing["routes"]:
        assert route["skill"] in targets, f"route target {route['skill']} unknown"
    for chain in routing["chains"]:
        for step in chain["steps"]:
            assert step in targets, f"chain {chain['name']} step {step} unknown"
