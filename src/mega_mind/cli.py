import json
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from . import __version__
from .installer import install_skills, verify_install

# Platform name -> relative skills dir used by doctor/check.
PLATFORM_SKILLS = [
    ("agent", ".agent/skills"),
    ("copilot", ".github/skills"),
    ("claude", ".claude/skills"),
    ("opencode", ".opencode/skills"),
    ("codex", ".codex/skills"),
    ("pi", ".pi/skills"),
]


@click.group()
@click.version_option(version=__version__)
def cli():
    """Mega-Mind Orchestrator CLI"""
    pass


@cli.command()
@click.argument("target_dir", type=click.Path(), default=".")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
@click.option(
    "--copilot",
    is_flag=True,
    help="Install GitHub Copilot-compatible files into .github/",
)
@click.option(
    "--claude",
    is_flag=True,
    help="Install Claude Code-compatible files (CLAUDE.md, .claude/)",
)
@click.option(
    "--opencode",
    is_flag=True,
    help="Install OpenCode-compatible files (.opencode/)",
)
@click.option(
    "--codex",
    is_flag=True,
    help="Install Codex-compatible files (.codex/)",
)
@click.option(
    "--pi",
    is_flag=True,
    help="Install pi-coding-agent-compatible files (.pi/, .agents/)",
)
def init(target_dir, force, copilot, claude, opencode, codex, pi):
    """Initialize Mega-Mind skills in the target directory.

    Without flags, installs to .agent/ (Antigravity / standard agent tools).
    With platform flags, installs ONLY into the requested platform directories.
    Every copied file is verified byte-for-byte; a failed copy aborts the install.
    """
    try:
        install_skills(target_dir, force, copilot, claude, opencode, codex, pi)
        click.echo(
            click.style(
                f"[OK] Successfully initialized Mega-Mind in {target_dir}",
                fg="green",
            )
        )
        if copilot:
            click.echo(
                click.style(
                    "    🤖 GitHub Copilot files installed in .github/",
                    fg="cyan",
                )
            )
            click.echo(
                click.style(
                    "    📂 Skills available as slash commands in VS Code Copilot chat",
                    fg="cyan",
                )
            )
        if claude:
            click.echo(
                click.style(
                    "    🧠 Claude Code files installed in CLAUDE.md and .claude/",
                    fg="magenta",
                )
            )
            click.echo(
                click.style(
                    "    📂 Skills available for Claude Code CLI",
                    fg="magenta",
                )
            )
        if opencode:
            click.echo(
                click.style(
                    "    📂 OpenCode files installed in .opencode/",
                    fg="yellow",
                )
            )
        if codex:
            click.echo(
                click.style(
                    "    📂 Codex files installed in .codex/",
                    fg="blue",
                )
            )
        if pi:
            click.echo(
                click.style(
                    "    🧩 pi-coding-agent files installed in .pi/ and .agents/",
                    fg="bright_cyan",
                )
            )
            click.echo(
                click.style(
                    "    📂 Skills loaded automatically by pi on session start",
                    fg="bright_cyan",
                )
            )
        click.echo(
            click.style(
                "    🔎 Run `mmo doctor` to verify the install and hook dependency.",
                fg="white",
            )
        )
    except Exception as e:
        click.echo(click.style(f"[ERROR] {str(e)}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument("request")
@click.option("--json", "as_json", is_flag=True, help="Machine-readable output")
@click.option(
    "--shared-dir",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="Directory holding routing.json + skills-manifest.json",
)
def route(request, as_json, shared_dir):
    """Route a natural-language request to the skill or agent that owns it.

    Applies the documented precedence rules: explicit persona invocation,
    named test type over generic "write tests", debugging-first for failures
    with an unknown root cause, then longest routing phrase, then unambiguous
    frontmatter triggers. Exits 1 when nothing matches.
    """
    from .router import find_shared_dir, load_routing, route as resolve

    shared = Path(shared_dir) if shared_dir else find_shared_dir()
    if shared is None:
        click.echo(
            click.style(
                "[ERROR] no routing.json found — run `mmo init` first",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)

    decision = resolve(request, load_routing(shared))
    if decision is None:
        if as_json:
            click.echo(json.dumps({"request": request, "target": None}))
        else:
            click.echo(
                click.style(f"[UNROUTED] {request}", fg="yellow")
                + "\n  No routing phrase matched. Classify manually per the "
                "orchestrator Request Analysis step 4."
            )
        sys.exit(1)

    if as_json:
        click.echo(json.dumps({"request": request, **decision.to_dict()}, indent=2))
        return

    label = "agent" if decision.kind == "agent" else "skill"
    # ASCII only: this string must survive a legacy console code page.
    click.echo(
        click.style(f"-> {decision.target} ", fg="green", bold=True)
        + click.style(f"({label})", fg="cyan")
    )
    click.echo(f"  layer:  {decision.layer}  [matched: '{decision.matched}']")
    if decision.chain:
        click.echo(f"  chain:  {decision.chain}")
    if decision.deferred_to:
        click.echo(f"  next:   {', '.join(decision.deferred_to)} after diagnosis")
    click.echo(f"  reason: {decision.reason}")


@cli.command()
@click.argument("target_dir", type=click.Path(), default=".")
def doctor(target_dir):
    """Diagnose the environment and verify an installed Mega-Mind tree.

    Checks: (1) the context-mode CLI that generated hooks depend on, and
    (2) every installed platform's skills against skills-manifest.json hashes.
    Exits non-zero if any check fails.
    """
    problems = 0

    ctx = _which("context-mode")
    if ctx:
        click.echo(click.style(f"[OK]   context-mode found at {ctx}", fg="green"))
    else:
        click.echo(
            click.style(
                "[FAIL] context-mode not found on PATH — generated hooks will fail. "
                "Install it with: npm install -g context-mode",
                fg="red",
            )
        )
        problems += 1

    target = Path(target_dir).resolve()
    found_any = False
    for platform, rel in PLATFORM_SKILLS:
        if not (target / rel).exists():
            continue
        found_any = True
        issues = verify_install(str(target), platform)
        if issues:
            problems += len(issues)
            for msg in issues:
                click.echo(click.style(f"[FAIL] {platform}: {msg}", fg="red"))
        else:
            click.echo(click.style(f"[OK]   {platform}: install tree matches manifest", fg="green"))

    if not found_any:
        click.echo(
            click.style(
                f"[WARN] no Mega-Mind install found under {target} "
                "(looked for .agent, .github, .claude, .opencode, .codex, .pi)",
                fg="yellow",
            )
        )

    if problems:
        click.echo(click.style(f"\n[FAIL] {problems} issue(s) found", fg="red"))
        sys.exit(1)
    click.echo(click.style("\n[OK] environment healthy", fg="green"))


@cli.command()
def check():
    """Maintainer gate: validate manifest, generated docs, sync state, and a
    sandboxed install of every platform layout. Run from the repo root."""
    repo = _find_repo_root()
    if repo is None:
        click.echo(
            click.style(
                "[ERROR] not inside a mega-mind-skills repository — run from the repo root",
                fg="red",
            )
        )
        sys.exit(1)

    failed = False
    steps = [
        (["scripts/build-manifest.py", "--check"], "skills manifest fresh"),
        (["scripts/render-skills.py", "--check"], "generated docs fresh"),
        (["scripts/validate-skill-system.py"], "skill system validation"),
        (["scripts/sync-assets.py", "--check"], ".agent/ == assets/ sync"),
    ]
    for cmd, label in steps:
        result = subprocess.run(
            [sys.executable, *cmd], cwd=repo, capture_output=True, text=True
        )
        if result.returncode == 0:
            click.echo(click.style(f"[OK]   {label}", fg="green"))
        else:
            failed = True
            click.echo(click.style(f"[FAIL] {label}", fg="red"))
            if result.stdout.strip():
                for line in result.stdout.strip().splitlines()[-8:]:
                    click.echo(f"       {line}")
            if result.stderr.strip():
                for line in result.stderr.strip().splitlines()[-8:]:
                    click.echo(f"       {line}", err=True)

    # Sandboxed install of all platform layouts against the packaged assets.
    with tempfile.TemporaryDirectory(prefix="mmo-check-") as tmp:
        target = Path(tmp) / "proj"
        try:
            install_skills(
                str(target),
                force=True,
                copilot=True,
                claude=True,
                opencode=True,
                codex=True,
                pi=True,
            )
            for platform, _ in PLATFORM_SKILLS[1:]:
                issues = verify_install(str(target), platform)
                if issues:
                    failed = True
                    click.echo(
                        click.style(f"[FAIL] sandbox install: {platform}", fg="red")
                    )
                    for msg in issues:
                        click.echo(f"       {msg}")
        except Exception as e:
            failed = True
            click.echo(click.style(f"[FAIL] sandbox install raised: {e}", fg="red"))

        if not failed:
            click.echo(
                click.style("[OK]   sandboxed install of all 6 platform layouts", fg="green")
            )

    if failed:
        click.echo(click.style("\n[FAIL] mmo check found problems", fg="red"))
        sys.exit(1)
    click.echo(click.style("\n[OK] all checks passed", fg="green"))


def _which(name: str) -> str | None:
    import shutil

    return shutil.which(name)


def _find_repo_root() -> Path | None:
    """Walk up from cwd looking for the repo marker (.agent + scripts + manifest)."""
    current = Path.cwd().resolve()
    for directory in [current, *current.parents]:
        if (
            (directory / ".agent" / "shared" / "skills-manifest.json").exists()
            and (directory / "scripts" / "validate-skill-system.py").exists()
        ):
            return directory
    return None


def _ensure_utf8_streams() -> None:
    """Make stdout/stderr safe on consoles whose default encoding is not UTF-8.

    Windows consoles often default to a legacy code page (cp1251, cp437, cp932...).
    Writing a non-ASCII glyph such as the route arrow or an init emoji then raises
    UnicodeEncodeError and the command dies after doing its work. Reconfiguring once at
    startup keeps the readable glyphs on capable terminals and degrades to replacement
    characters instead of a traceback elsewhere.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:  # click's test runner replaces the streams
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def main():
    _ensure_utf8_streams()
    cli()


if __name__ == "__main__":
    main()
