"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Wolt Summer Eng Assignment."""


if __name__ == "__main__":
    main(prog_name="wolt-summer-eng-assignment")  # pragma: no cover
