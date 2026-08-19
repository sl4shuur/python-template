"""Command-line interface for the application."""

import rich_click as click

from app.main import run

# Configure Rich-Click
click.rich_click.TEXT_MARKUP = "rich"
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.ERRORS_SUGGESTION = (
    "\nTry running the [bold cyan]'--help'[/] flag for more information."
)
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit our documentation."

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "rich_help_config": {
        "text_markup": "rich",
        "show_arguments": True,
        "group_arguments_options": True,
        "style_option": "bold cyan",
        "style_command": "bold cyan",
        "style_usage": "bold yellow",
        "style_errors_panel_border": "red",
    },
}


@click.command(
    context_settings=CONTEXT_SETTINGS,
    help="[bold]Run the application.[/]",
    epilog="[dim]Tip: use [bold cyan]-h[/] as a shortcut for [bold cyan]--help[/].[/]",
)
def main() -> int:
    """Run the application from the command line."""
    return run()


if __name__ == "__main__":
    main()
