#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import functools
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from provide.foundation.cli.deps import click
from provide.foundation.context import CLIContext
from provide.foundation.process import exit_error, exit_interrupted
from provide.foundation.serialization import json_dumps

"""Standard CLI decorators for consistent option handling."""

if TYPE_CHECKING:
    import click as click_types

F = TypeVar("F", bound=Callable[..., Any])

# Standard log level choices (including custom TRACE level)
LOG_LEVELS = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def logging_options(f: F) -> F:
    """Add standard logging options to a Click command.

    Adds:
    - --log-level/-l: Set logging verbosity (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
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
    """Add configuration file options to a Click command.

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
    """Add output formatting options to a Click command.

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
    """Apply flexible CLI options that can be used at any command level.

    Combines logging_options and config_options for consistent
    control at both group and command levels.
    """
    f = logging_options(f)
    f = config_options(f)
    return f


def standard_options(f: F) -> F:
    """Apply all standard CLI options.

    Combines logging_options, config_options, and output_options.
    """
    f = logging_options(f)
    f = config_options(f)
    f = output_options(f)
    return f


def error_handler(f: F) -> F:
    """Decorator to handle errors consistently in CLI commands.

    Catches exceptions and formats them appropriately based on
    debug mode and output format.
    """

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
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
                error_data = {
                    "error": str(e),
                    "type": type(e).__name__,
                }
                click.echo(json_dumps(error_data), err=True)
            else:
                click.secho(f"Error: {e}", fg="red", err=True)

            exit_error(f"Command failed: {e!s}")

    return wrapper  # type: ignore[return-value]


def _ensure_cli_context(ctx: click_types.Context) -> None:
    """Ensure the Click context has a CLIContext object."""
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


def _update_context_from_kwargs(cli_context: CLIContext, kwargs: dict[str, Any]) -> None:
    """Update CLIContext from command kwargs."""
    if kwargs.get("log_level"):
        cli_context.log_level = kwargs["log_level"]
    if kwargs.get("log_file"):
        # Ensure log_file is a Path object, as expected by Context
        cli_context.log_file = Path(kwargs["log_file"])
    if "log_format" in kwargs and kwargs["log_format"] is not None:
        cli_context.log_format = kwargs["log_format"]
    if "json_output" in kwargs and kwargs["json_output"] is not None:
        cli_context.json_output = kwargs["json_output"]
    if "no_color" in kwargs and kwargs["no_color"] is not None:
        cli_context.no_color = kwargs["no_color"]
    if "no_emoji" in kwargs and kwargs["no_emoji"] is not None:
        cli_context.no_emoji = kwargs["no_emoji"]
    if kwargs.get("profile"):
        cli_context.profile = kwargs["profile"]
    if kwargs.get("config"):
        cli_context.load_config(kwargs["config"])


def _remove_cli_options_from_kwargs(kwargs: dict[str, Any]) -> None:
    """Remove CLI options from kwargs to avoid duplicate arguments."""
    cli_option_keys = [
        "log_level",
        "log_file",
        "log_format",
        "json_output",
        "no_color",
        "no_emoji",
        "profile",
        "config",
    ]
    for key in cli_option_keys:
        kwargs.pop(key, None)


def pass_context(f: F) -> F:
    """Decorator to pass the foundation CLIContext to a command.

    Creates or retrieves a CLIContext from Click's context object
    and passes it as the first argument to the decorated function.
    """

    @functools.wraps(f)
    @click.pass_context
    def wrapper(ctx: click_types.Context, *args: Any, **kwargs: Any) -> Any:
        # Get or create foundation context
        _ensure_cli_context(ctx)

        # Update context from command options
        _update_context_from_kwargs(ctx.obj, kwargs)

        # Remove CLI options from kwargs to avoid duplicate arguments
        _remove_cli_options_from_kwargs(kwargs)

        return f(ctx.obj, *args, **kwargs)

    return wrapper  # type: ignore[return-value]


def version_option(version: str | None = None, prog_name: str | None = None) -> Callable[[F], F]:
    """Add a --version option to display version information.

    Args:
        version: Version string to display
        prog_name: Program name to display

    """

    def decorator(f: F) -> F:
        return click.version_option(
            version=version,
            prog_name=prog_name,
            message="%(prog)s version %(version)s",
        )(f)

    return decorator


# 🧱🏗️🔚
