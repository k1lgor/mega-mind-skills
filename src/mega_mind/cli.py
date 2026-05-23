import click
import sys
from .installer import install_skills


@click.group()
@click.version_option(package_name="mmo")
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
    except Exception as e:
        click.echo(click.style(f"[ERROR] {str(e)}", fg="red"), err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
