import rich_click as click

from config import configure_logging
from loggers import CustomLogger, get_logger

config = configure_logging()
logger = get_logger(CustomLogger, __name__)


@click.group(
    invoke_without_command=True,
    help="Minimal CLI entrypoint for the project.",
)
@click.pass_context
def main(ctx: click.Context) -> int:
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    return 0


if __name__ == "__main__":
    logger.success("Application started successfully!")
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    exit(main())
