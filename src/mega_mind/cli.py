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
def init(target_dir, force):
    """Initialize Mega-Mind skills in the target directory"""
    try:
        install_skills(target_dir, force)
        click.echo(
            click.style(
                f" \u2705 Successfully initialized Mega-Mind in {target_dir}",
                fg="green",
            )
        )
    except Exception as e:
        click.echo(click.style(f" \u274c Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
