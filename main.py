import rich_click as click

from config import configure_logging
from loggers import CustomLogger, EvalLogger, get_logger

config = configure_logging()
logger = get_logger(CustomLogger, name=__name__)
eval_logger = get_logger(EvalLogger, config=config, name=__name__)


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
    eval_logger.metric("example_metric", 0.5234)
    logger.success("This is a success message.")
    exit(main())
