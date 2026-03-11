import click
import sys
from .installer import install_skills


@click.group()
@click.version_option(package_name="mega-mind-orchestrator")
def cli():
    """Mega-Mind Orchestrator CLI"""
    pass


@cli.command()
@click.argument("target_dir", type=click.Path(), default=".")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
@click.option(
    "--copilot",
    is_flag=True,
    help="Also install GitHub Copilot-compatible files into .github/",
)
@click.option(
    "--claude",
    is_flag=True,
    help="Also install Claude Code-compatible files (CLAUDE.md, .claude/)",
)
def init(target_dir, force, copilot, claude):
    """Initialize Mega-Mind skills in the target directory.

    By default, installs to .agent/ for Antigravity / standard agent tools.

    Use --copilot to also install into .github/ for GitHub Copilot (VS Code).
    Use --claude to also install CLAUDE.md and .claude/ for Claude Code.
    """
    try:
        install_skills(target_dir, force, copilot, claude)
        click.echo(
            click.style(
                f" ✅ Successfully initialized Mega-Mind in {target_dir}",
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
    except Exception as e:
        click.echo(click.style(f" ❌ Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
