import rich_click as click


@click.group(
    invoke_without_command=True,
    help="Minimal CLI entrypoint for the project.",
)
@click.pass_context
def main(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


if __name__ == "__main__":
    main()
