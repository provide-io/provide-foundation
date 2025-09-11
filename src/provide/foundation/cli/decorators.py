"""Standard CLI decorators for consistent option handling."""

from collections.abc import Callable
import functools
from pathlib import Path
import sys
from typing import Any, TypeVar

try:
    import click
except ImportError:
    click = None

from provide.foundation.context import CLIContext
from provide.foundation.process import exit_error, exit_interrupted

F = TypeVar("F", bound=Callable[..., Any])

# Standard log level choices
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def logging_options(f: F) -> F:
    """
    Add standard logging options to a Click command.

    Adds:
    - --log-level/-l: Set logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - --log-file: Write logs to file
    - --log-format: Choose log output format (json, text, key_value)
    """
    f = click.option(
        "--log-level",
        "-l",
        type=click.Choice(LOG_LEVELS, case_sensitive=False),
        default=None,
        envvar="PROVIDE_LOG_LEVEL",
        help="Set the logging level",
    )(f)
    f = click.option(
        "--log-file",
        type=click.Path(dir_okay=False, writable=True, path_type=Path),
        default=None,
        envvar="PROVIDE_LOG_FILE",
        help="Write logs to file",
    )(f)
    f = click.option(
        "--log-format",
        type=click.Choice(["json", "text", "key_value"], case_sensitive=False),
        default="key_value",
        envvar="PROVIDE_LOG_FORMAT",
        help="Log output format",
    )(f)
    return f


def config_options(f: F) -> F:
    """
    Add configuration file options to a Click command.

    Adds:
    - --config/-c: Path to configuration file
    - --profile/-p: Configuration profile to use
    """
    f = click.option(
        "--config",
        "-c",
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        default=None,
        envvar="PROVIDE_CONFIG_FILE",
        help="Path to configuration file",
    )(f)
    f = click.option(
        "--profile",
        "-p",
        default=None,
        envvar="PROVIDE_PROFILE",
        help="Configuration profile to use",
    )(f)
    return f


def output_options(f: F) -> F:
    """
    Add output formatting options to a Click command.

    Adds:
    - --json: Output in JSON format
    - --no-color: Disable colored output
    - --no-emoji: Disable emoji in output
    """
    f = click.option(
        "--json",
        "json_output",
        is_flag=True,
        default=None,
        envvar="PROVIDE_JSON_OUTPUT",
        help="Output in JSON format",
    )(f)
    f = click.option(
        "--no-color",
        is_flag=True,
        default=False,
        envvar="PROVIDE_NO_COLOR",
        help="Disable colored output",
    )(f)
    f = click.option(
        "--no-emoji",
        is_flag=True,
        default=False,
        envvar="PROVIDE_NO_EMOJI",
        help="Disable emoji in output",
    )(f)
    return f


def flexible_options(f: F) -> F:
    """
    Apply flexible CLI options that can be used at any command level.

    Combines logging_options and config_options for consistent
    control at both group and command levels.
    """
    f = logging_options(f)
    f = config_options(f)
    return f


def standard_options(f: F) -> F:
    """
    Apply all standard CLI options.

    Combines logging_options, config_options, and output_options.

    Note: Consider using flexible_options for better granular control.
    This decorator is maintained for backward compatibility.
    """
    f = logging_options(f)
    f = config_options(f)
    f = output_options(f)
    return f


def error_handler(f: F) -> F:
    """
    Decorator to handle errors consistently in CLI commands.

    Catches exceptions and formats them appropriately based on
    debug mode and output format.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        click.get_current_context()
        debug = kwargs.get("debug", False)
        json_output = kwargs.get("json_output", False)

        try:
            return f(*args, **kwargs)
        except click.ClickException:
            # Let Click handle its own exceptions
            raise
        except KeyboardInterrupt:
            if not json_output:
                click.secho("\nInterrupted by user", fg="yellow", err=True)
            exit_interrupted()
        except Exception as e:
            if debug:
                # In debug mode, show full traceback
                raise

            if json_output:
                import json

                error_data = {
                    "error": str(e),
                    "type": type(e).__name__,
                }
                click.echo(json.dumps(error_data), err=True)
            else:
                click.secho(f"Error: {e}", fg="red", err=True)

            exit_error(f"Command failed: {str(e)}")

    return wrapper


def pass_context(f: F) -> F:
    """
    Decorator to pass the foundation CLIContext to a command.

    Creates or retrieves a CLIContext from Click's context object
    and passes it as the first argument to the decorated function.
    """

    @functools.wraps(f)
    @click.pass_context
    def wrapper(ctx: click.Context, *args, **kwargs):
        # Get or create foundation context
        if not hasattr(ctx, "obj") or ctx.obj is None:
            ctx.obj = CLIContext()
        elif not isinstance(ctx.obj, CLIContext):
            # If obj exists but isn't a Context, wrap it
            if isinstance(ctx.obj, dict):
                ctx.obj = CLIContext.from_dict(ctx.obj)
            else:
                # Store existing obj and create new CLIContext
                old_obj = ctx.obj
                ctx.obj = CLIContext()
                ctx.obj._cli_data = old_obj

        # Update context from command options
        if kwargs.get("log_level"):
            ctx.obj.log_level = kwargs["log_level"]
        if kwargs.get("log_file"):
            # Ensure log_file is a Path object, as expected by Context
            ctx.obj.log_file = Path(kwargs["log_file"])
        if "log_format" in kwargs and kwargs["log_format"] is not None:
            ctx.obj.log_format = kwargs["log_format"]
        if "json_output" in kwargs and kwargs["json_output"] is not None:
            ctx.obj.json_output = kwargs["json_output"]
        if "no_color" in kwargs and kwargs["no_color"] is not None:
            ctx.obj.no_color = kwargs["no_color"]
        if "no_emoji" in kwargs and kwargs["no_emoji"] is not None:
            ctx.obj.no_emoji = kwargs["no_emoji"]
        if kwargs.get("profile"):
            ctx.obj.profile = kwargs["profile"]
        if kwargs.get("config"):
            ctx.obj.load_config(kwargs["config"])

        # Remove these from kwargs to avoid duplicate arguments
        for key in [
            "log_level",
            "log_file",
            "log_format",
            "json_output",
            "no_color",
            "no_emoji",
            "profile",
            "config",
        ]:
            kwargs.pop(key, None)

        return f(ctx.obj, *args, **kwargs)

    return wrapper


def version_option(version: str | None = None, prog_name: str | None = None):
    """
    Add a --version option to display version information.

    Args:
        version: Version string to display
        prog_name: Program name to display
    """

    def decorator(f: F) -> F:
        return click.version_option(
            version=version, prog_name=prog_name, message="%(prog)s version %(version)s"
        )(f)

    return decorator
