import hashlib
import json
import shutil
from pathlib import Path


def _verify_copied(src_root: Path, dst_root: Path, label: str) -> None:
    """Receiving inspection: fail loudly if any copied file differs from source."""
    mismatches = []
    for item in sorted(src_root.rglob("*")):
        if item.is_dir() or "__pycache__" in item.parts:
            continue
        rel = item.relative_to(src_root)
        dest = dst_root / rel
        if not dest.exists():
            mismatches.append(f"missing: {label}/{rel}")
        elif hashlib.sha256(item.read_bytes()).hexdigest() != hashlib.sha256(
            dest.read_bytes()
        ).hexdigest():
            mismatches.append(f"corrupt: {label}/{rel}")
    if mismatches:
        raise RuntimeError(
            f"Install verification failed for {label}:\n  " + "\n  ".join(mismatches[:10])
        )


def verify_install(target_dir: str, platform: str = "agent") -> list[str]:
    """Verify an installed tree against the shipped skills-manifest.json.

    Returns a list of problems (empty = healthy). `platform` selects the skills
    directory layout: agent, copilot, claude, opencode, codex, or pi.
    """
    target_path = Path(target_dir).resolve()
    # platform name -> platform root dir (copilot installs under .github)
    platform_root = {
        "agent": target_path / ".agent",
        "copilot": target_path / ".github",
        "claude": target_path / ".claude",
        "opencode": target_path / ".opencode",
        "codex": target_path / ".codex",
        "pi": target_path / ".pi",
    }.get(platform)
    skills_dir = platform_root / "skills" if platform_root else None

    if skills_dir is None:
        return [f"unknown platform '{platform}'"]
    if not skills_dir.exists():
        return [f"{skills_dir} not found — nothing installed for platform '{platform}'"]

    manifest_path = platform_root / "shared" / "skills-manifest.json"
    problems: list[str] = []
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        by_name = {s["name"]: s["sha256"] for s in manifest["skills"]}
        installed = {
            p.parent.name for p in skills_dir.glob("*/SKILL.md")
        }
        for name in sorted(by_name):
            path = skills_dir / name / "SKILL.md"
            if not path.exists():
                problems.append(f"missing skill: {name}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != by_name[name]:
                problems.append(f"content mismatch: {name}")
        for name in sorted(installed - set(by_name)):
            problems.append(f"unexpected skill: {name}")
    else:
        problems.append(
            f"no skills-manifest.json found under {manifest_path.parent} — "
            "cannot verify content integrity"
        )
    return problems


def _verify_platform(assets_src: Path, target_path: Path, pairs: list[tuple[str, str]]) -> None:
    """Verify each (source_subdir, dest_subdir) subtree copied byte-identically."""
    for rel_src, rel_dst in pairs:
        src = assets_src / rel_src
        if not src.exists():
            continue
        _verify_copied(src, target_path / rel_dst, rel_dst)


def _verify_agents(assets_src: Path, agents_dst: Path, agent_ext: bool = False) -> None:
    """Structural check for agent personas.

    Agents are renamed (.agent.md for Copilot) and gain injected YAML
    frontmatter when the source lacks it, so they are verified by presence,
    frontmatter, and preserved title instead of byte equality.
    """
    agents_src = assets_src / "agents"
    if not agents_src.exists():
        return
    for agent_file in sorted(agents_src.glob("*.md")):
        stem = agent_file.stem + (".agent.md" if agent_ext else ".md")
        dest = agents_dst / stem
        if not dest.exists():
            raise RuntimeError(f"missing agent: {dest.name}")
        content = dest.read_text(encoding="utf-8")
        if not content.startswith("---"):
            raise RuntimeError(f"agent missing frontmatter: {dest.name}")


def install_skills(
    target_dir: str,
    force: bool = False,
    copilot: bool = False,
    claude: bool = False,
    opencode: bool = False,
    codex: bool = False,
    pi: bool = False,
):
    """Install skills into the target directory.

    Without platform flags, creates .agent/ (the default Antigravity directory).
    With platform flags, creates ONLY the requested platform directories — .agent/
    is NOT created.

    Every copy is verified byte-for-byte against the package assets afterwards;
    a corrupted or truncated install fails here instead of silently at runtime.

    Args:
        target_dir: The root directory of the project to install into.
        force: If True, overwrite existing files.
        copilot: Install into .github/ for GitHub Copilot.
        claude: Install CLAUDE.md and .claude/ for Claude Code.
        opencode: Install into .opencode/ for OpenCode.
        codex: Install into .codex/ for OpenAI Codex.
        pi: Install into .pi/ and .agents/ for pi-coding-agent.
    """
    target_path = Path(target_dir).resolve()
    agent_path = target_path / ".agent"

    # Discovery of assets embedded in the package
    assets_src = Path(__file__).parent / "assets"

    if not assets_src.exists():
        raise FileNotFoundError(f"Source assets not found at {assets_src}")

    # Determine whether any platform-specific flag was passed.
    # When NO flags are passed, `mmo init` installs into .agent/ (the default).
    # When flags ARE passed, ONLY the requested platforms are installed — .agent/ is NOT created.
    any_platform = copilot or claude or opencode or codex or pi

    if not any_platform:
        # Bare `mmo init` — install .agent/ as the canonical directory.
        if agent_path.exists() and not force:
            raise FileExistsError(
                f".agent directory already exists in {target_dir}. Use --force to overwrite."
            )
        shutil.copytree(assets_src, agent_path, dirs_exist_ok=True)
        _verify_copied(assets_src, agent_path, ".agent")

    if copilot:
        _install_github_copilot(assets_src, target_path, force)

    if claude:
        _install_claude_code(assets_src, target_path, force)

    if opencode:
        _install_opencode(assets_src, target_path, force)

    if codex:
        _install_codex(assets_src, target_path, force)

    if pi:
        _install_pi(assets_src, target_path, force)

    _install_hooks(
        target_path,
        force,
        agent=not any_platform,
        copilot=copilot,
        claude=claude,
        opencode=opencode,
        codex=codex,
        pi=pi,
    )


def _install_hooks(
    target_path: Path,
    force: bool,
    agent: bool = True,
    copilot: bool = False,
    claude: bool = False,
    opencode: bool = False,
    codex: bool = False,
    pi: bool = False,
):
    """Install hooks.json for context-mode in the respective environments."""
    import json

    def get_hook_content(target_env: str) -> str:
        return json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {
                            "type": "command",
                            "command": f"context-mode hook {target_env} pretooluse",
                        }
                    ],
                    "PostToolUse": [
                        {
                            "type": "command",
                            "command": f"context-mode hook {target_env} posttooluse",
                        }
                    ],
                    "PreCompact": [
                        {
                            "type": "command",
                            "command": f"context-mode hook {target_env} precompact",
                        }
                    ],
                    "SessionStart": [
                        {
                            "type": "command",
                            "command": f"context-mode hook {target_env} sessionstart",
                        }
                    ],
                }
            },
            indent=2,
        )

    def write_hooks(env_dir: Path, env_name: str):
        env_dir.mkdir(parents=True, exist_ok=True)
        hooks_file = env_dir / "hooks.json"
        if not hooks_file.exists() or force:
            hooks_file.write_text(get_hook_content(env_name), encoding="utf-8")

    if agent:
        write_hooks(target_path / ".agent" / "hooks", "antigravity")

    if copilot:
        write_hooks(target_path / ".github" / "hooks", "vscode-copilot")

    if claude:
        write_hooks(target_path / ".claude" / "hooks", "claude-code")

    if opencode:
        write_hooks(target_path / ".opencode" / "hooks", "opencode")

    if codex:
        write_hooks(target_path / ".codex" / "hooks", "codex")

    if pi:
        write_hooks(target_path / ".pi" / "hooks", "pi-coding-agent")


def _install_github_copilot(assets_src: Path, target_path: Path, force: bool):
    """Install GitHub Copilot-compatible files into .github/ directory.

    Creates:
      .github/copilot-instructions.md  — project Copilot instructions (from AGENTS.md)
      .github/skills/<name>/SKILL.md   — all skills (Agent Skills standard)
      .github/agents/<name>.agent.md   — all agent personas
    """
    github_path = target_path / ".github"

    # 1. Copy copilot-instructions.md from AGENTS.md
    agents_md = assets_src / "AGENTS.md"
    copilot_instructions = github_path / "copilot-instructions.md"
    if agents_md.exists():
        copilot_instructions.parent.mkdir(parents=True, exist_ok=True)
        if not copilot_instructions.exists() or force:
            shutil.copy2(agents_md, copilot_instructions)

    # 2. Copy skills to .github/skills/<name>/SKILL.md
    _copy_skills(assets_src, github_path / "skills", force)

    # 3. Copy shared snippets to .github/shared/
    _copy_shared(assets_src, github_path / "shared", force)

    # 4. Copy agents to .github/agents/<name>.agent.md
    _copy_agents_with_frontmatter(
        assets_src, github_path / "agents", force, agent_ext=True
    )

    _verify_platform(
        assets_src,
        target_path,
        [("skills", ".github/skills"), ("shared", ".github/shared")],
    )
    _verify_agents(assets_src, github_path / "agents", agent_ext=True)


def _install_claude_code(assets_src: Path, target_path: Path, force: bool):
    """Install Claude Code-compatible files.

    Creates:
      CLAUDE.md             — project rules (from AGENTS.md)
      .claude/skills/       — all skills (Agent Skills standard)
      .claude/agents/       — all agent personas
    """
    # 1. Create CLAUDE.md in root (mirror of AGENTS.md)
    agents_md = assets_src / "AGENTS.md"
    claude_md = target_path / "CLAUDE.md"
    if agents_md.exists():
        if not claude_md.exists() or force:
            shutil.copy2(agents_md, claude_md)

    # 2. Copy skills to .claude/skills/<name>/SKILL.md
    _copy_skills(assets_src, target_path / ".claude" / "skills", force)

    # 3. Copy shared snippets to .claude/shared/
    _copy_shared(assets_src, target_path / ".claude" / "shared", force)

    # 4. Copy workflows as commands to .claude/commands/
    _copy_commands(assets_src, target_path / ".claude" / "commands", force)

    # 5. Copy agents to .claude/agents/
    _copy_agents_with_frontmatter(assets_src, target_path / ".claude" / "agents", force)

    _verify_platform(
        assets_src,
        target_path,
        [
            ("skills", ".claude/skills"),
            ("shared", ".claude/shared"),
            ("commands", ".claude/commands"),
        ],
    )
    _verify_agents(assets_src, target_path / ".claude" / "agents")


def _install_opencode(assets_src: Path, target_path: Path, force: bool):
    """Install OpenCode-compatible files.

    Creates:
      AGENTS.md             — project instructions at root (OpenCode primary)
      CLAUDE.md             — fallback instructions (from AGENTS.md)
      .opencode/skills/     — all skills
      .opencode/agents/     — all agent personas
    """
    agents_md = assets_src / "AGENTS.md"

    # 1. AGENTS.md at root — OpenCode primary instructions file.
    root_agents_md = target_path / "AGENTS.md"
    if agents_md.exists() and (not root_agents_md.exists() or force):
        shutil.copy2(agents_md, root_agents_md)

    # 2. CLAUDE.md at root — OpenCode fallback (also used by Claude Code)
    claude_md = target_path / "CLAUDE.md"
    if agents_md.exists() and (not claude_md.exists() or force):
        shutil.copy2(agents_md, claude_md)

    # 3. Skills to .opencode/skills/<name>/SKILL.md
    _copy_skills(assets_src, target_path / ".opencode" / "skills", force)

    # 4. Shared snippets to .opencode/shared/
    _copy_shared(assets_src, target_path / ".opencode" / "shared", force)

    # 5. Workflows as commands to .opencode/commands/
    _copy_commands(assets_src, target_path / ".opencode" / "commands", force)

    # 6. Agent personas to .opencode/agents/
    _copy_agents_with_frontmatter(
        assets_src, target_path / ".opencode" / "agents", force
    )

    _verify_platform(
        assets_src,
        target_path,
        [
            ("skills", ".opencode/skills"),
            ("shared", ".opencode/shared"),
            ("commands", ".opencode/commands"),
        ],
    )
    _verify_agents(assets_src, target_path / ".opencode" / "agents")


def _install_codex(assets_src: Path, target_path: Path, force: bool):
    """Install OpenAI Codex-compatible files.

    Codex reads AGENTS.md at the project root for project-level instructions.
    Skills live in .codex/skills/<name>/SKILL.md.

    Creates:
      AGENTS.md             — project instructions (Codex reads this at root)
      .codex/skills/        — all skills
      .codex/agents/        — all agent personas
    """
    agents_md = assets_src / "AGENTS.md"

    # 1. AGENTS.md at root — Codex primary instructions file.
    root_agents_md = target_path / "AGENTS.md"
    if agents_md.exists() and (not root_agents_md.exists() or force):
        shutil.copy2(agents_md, root_agents_md)

    # 2. Skills to .codex/skills/<name>/SKILL.md
    _copy_skills(assets_src, target_path / ".codex" / "skills", force)

    # 3. Shared snippets to .codex/shared/
    _copy_shared(assets_src, target_path / ".codex" / "shared", force)

    # 4. Agent personas to .codex/agents/
    _copy_agents_with_frontmatter(assets_src, target_path / ".codex" / "agents", force)

    _verify_platform(
        assets_src,
        target_path,
        [("skills", ".codex/skills"), ("shared", ".codex/shared")],
    )
    _verify_agents(assets_src, target_path / ".codex" / "agents")


def _install_pi(assets_src: Path, target_path: Path, force: bool):
    """Install pi-coding-agent-compatible files.

    Pi loads skills from .pi/skills/ and .agents/skills/ (Agent Skills standard).
    Prompt templates (slash commands) live in .pi/prompts/.
    Context files: AGENTS.md and CLAUDE.md at root.

    Creates:
      AGENTS.md             — project context (pi reads root .md files)
      CLAUDE.md             — fallback context (pi reads root .md files)
      .pi/skills/           — all skills (pi project skill dir)
      .pi/prompts/          — workflow prompt templates (pi slash commands)
      .pi/agents/           — agent personas as prompt templates
      .agents/skills/       — all skills (cross-tool Agent Skills standard)
    """
    agents_md = assets_src / "AGENTS.md"

    # 1. AGENTS.md at root — pi reads it as context
    root_agents_md = target_path / "AGENTS.md"
    if agents_md.exists() and (not root_agents_md.exists() or force):
        shutil.copy2(agents_md, root_agents_md)

    # 2. CLAUDE.md at root — pi also reads this as fallback context
    claude_md = target_path / "CLAUDE.md"
    if agents_md.exists() and (not claude_md.exists() or force):
        shutil.copy2(agents_md, claude_md)

    # 3. Skills to .pi/skills/ (pi-specific project skill location)
    _copy_skills(assets_src, target_path / ".pi" / "skills", force)

    # 4. Shared snippets to .pi/shared/
    _copy_shared(assets_src, target_path / ".pi" / "shared", force)

    # 5. Workflows as prompt templates to .pi/prompts/
    _copy_commands(assets_src, target_path / ".pi" / "prompts", force)

    # 6. Agent personas to .pi/agents/ as prompt templates
    _copy_agents_with_frontmatter(assets_src, target_path / ".pi" / "agents", force)

    # 7. Also install to .agents/skills/ for cross-tool compatibility
    #    (pi scans .agents/skills/ in cwd and ancestor directories)
    _copy_skills(assets_src, target_path / ".agents" / "skills", force)

    _verify_platform(
        assets_src,
        target_path,
        [
            ("skills", ".pi/skills"),
            ("shared", ".pi/shared"),
            ("commands", ".pi/prompts"),
            ("skills", ".agents/skills"),
        ],
    )
    _verify_agents(assets_src, target_path / ".pi" / "agents")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _copy_skills(assets_src: Path, skills_dst: Path, force: bool):
    """Copy every skill directory (SKILL.md plus any supporting files) to skills_dst/<name>/.

    The Agent Skills standard allows supporting files beside SKILL.md (references,
    scripts, templates). Copying the whole directory keeps those files from being
    silently dropped during install.
    """
    skills_src = assets_src / "skills"
    if not skills_src.exists():
        return
    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        dest_dir = skills_dst / skill_dir.name
        if dest_dir.exists() and not force:
            continue
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(skill_dir, dest_dir)


def _copy_shared(assets_src: Path, shared_dst: Path, force: bool):
    shared_src = assets_src / "shared"
    if not shared_src.exists():
        return
    shared_dst.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(shared_src.iterdir()):
        if src_file.is_file():
            dest_file = shared_dst / src_file.name
            if not dest_file.exists() or force:
                shutil.copy2(src_file, dest_file)


def _copy_commands(assets_src: Path, commands_dst: Path, force: bool):
    workflows_src = assets_src / "workflows"
    if not workflows_src.exists():
        return
    commands_dst.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(workflows_src.iterdir()):
        if src_file.is_file():
            dest_file = commands_dst / src_file.name
            if not dest_file.exists() or force:
                shutil.copy2(src_file, dest_file)


def _copy_agents_with_frontmatter(
    assets_src: Path, agents_dst: Path, force: bool, agent_ext: bool = False
):
    """Copy agent personas, injecting YAML frontmatter if missing.

    When *agent_ext* is True (GitHub Copilot), produces <name>.agent.md.
    Otherwise keeps the original <name>.md filename.
    """
    agents_src = assets_src / "agents"
    if not agents_src.exists():
        return
    agents_dst.mkdir(parents=True, exist_ok=True)
    for agent_file in sorted(agents_src.iterdir()):
        if agent_file.is_file() and agent_file.suffix == ".md":
            new_name = (agent_file.stem + ".agent.md") if agent_ext else agent_file.name
            dest_file = agents_dst / new_name
            if not dest_file.exists() or force:
                content = agent_file.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    title = next(
                        (
                            line.lstrip("#").strip()
                            for line in content.split("\n")
                            if line.startswith("#")
                        ),
                        agent_file.stem,
                    )
                    frontmatter = (
                        f"---\n"
                        f"description: {title} - specialized Mega-Mind agent\n"
                        f'tools: ["editFiles", "runCommands", "search", "fetch"]\n'
                        f"---\n\n"
                    )
                    content = frontmatter + content
                dest_file.write_text(content, encoding="utf-8")
