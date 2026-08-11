"""Installer behavior tests: layouts, verification, frontmatter, hooks."""

import json
from pathlib import Path

from mega_mind.installer import _copy_skills, install_skills, verify_install

SKILL_COUNT = 53
AGENT_COUNT = 11


def test_agent_install_layout(tmp_path: Path):
    install_skills(str(tmp_path), force=True)
    assert (tmp_path / ".agent" / "AGENTS.md").exists()
    assert len(list((tmp_path / ".agent" / "skills").glob("*/SKILL.md"))) == SKILL_COUNT
    assert (tmp_path / ".agent" / "shared" / "skills-manifest.json").exists()
    assert (tmp_path / ".agent" / "shared" / "routing.json").exists()
    assert (tmp_path / ".agent" / "hooks" / "hooks.json").exists()
    assert verify_install(str(tmp_path), "agent") == []


def test_agent_install_refuses_without_force(tmp_path: Path):
    import pytest

    install_skills(str(tmp_path), force=True)
    with pytest.raises(Exception):
        install_skills(str(tmp_path), force=False)


def test_all_platform_installs(tmp_path: Path):
    install_skills(
        str(tmp_path),
        force=True,
        copilot=True,
        claude=True,
        opencode=True,
        codex=True,
        pi=True,
    )
    # platform flags must NOT create .agent/
    assert not (tmp_path / ".agent").exists()

    for rel in (
        ".github/skills",
        ".claude/skills",
        ".opencode/skills",
        ".codex/skills",
        ".pi/skills",
        ".agents/skills",
    ):
        assert len(list((tmp_path / rel).glob("*/SKILL.md"))) == SKILL_COUNT, rel

    # copilot agents: renamed to .agent.md with injected frontmatter
    copilot_agents = list((tmp_path / ".github" / "agents").glob("*.agent.md"))
    assert len(copilot_agents) == AGENT_COUNT
    assert all(a.read_text(encoding="utf-8").startswith("---") for a in copilot_agents)

    # hooks.json written and parseable for every platform
    for rel in (".github", ".claude", ".opencode", ".codex", ".pi"):
        hooks = json.loads((tmp_path / rel / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        assert "PreToolUse" in hooks["hooks"]

    # every platform verifies against its shipped manifest
    for platform in ("copilot", "claude", "opencode", "codex", "pi"):
        assert verify_install(str(tmp_path), platform) == [], platform


def test_verify_install_detects_corruption(tmp_path: Path):
    install_skills(str(tmp_path), force=True)
    target = tmp_path / ".agent" / "skills" / "debugging" / "SKILL.md"
    target.write_text("# tampered", encoding="utf-8")
    problems = verify_install(str(tmp_path), "agent")
    assert any("debugging" in p for p in problems)


def test_copy_skills_copies_full_directory(tmp_path: Path):
    src = tmp_path / "src-skills"
    (src / "skills" / "demo").mkdir(parents=True)
    (src / "skills" / "demo" / "SKILL.md").write_text("# demo skill", encoding="utf-8")
    (src / "skills" / "demo" / "references.md").write_text("supporting file", encoding="utf-8")
    dst = tmp_path / "dst-skills"
    _copy_skills(src, dst, force=False)
    assert (dst / "demo" / "references.md").read_text(encoding="utf-8") == "supporting file"
