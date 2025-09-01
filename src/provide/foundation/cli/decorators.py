"""Standard CLI decorators for consistent option handling."""

import functools
import logging
import sys
from typing import Any, Callable, TypeVar

import click
import structlog

from provide.foundation.context import Context

F = TypeVar("F", bound=Callable[..., Any])

# Standard log level choices
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def logging_options(f: F) -> F:
    """
    Add standard logging options to a Click command.
    
    Adds:
    - --log-level/-l: Set logging verbosity
    - --log-file: Write logs to file
    - --debug: Enable debug mode
    """
    f = click.option(
        "--log-level", "-l",
        type=click.Choice(LOG_LEVELS, case_sensitive=False),
        default=None,
        envvar="PROVIDE_LOG_LEVEL",
        help="Set the logging level",
    )(f)
    f = click.option(
        "--log-file",
        type=click.Path(dir_okay=False, writable=True, resolve_path=True),
        default=None,
        envvar="PROVIDE_LOG_FILE",
        help="Write logs to file",
    )(f)
    f = click.option(
        "--debug",
        is_flag=True,
        default=None,
        envvar="PROVIDE_DEBUG",
        help="Enable debug mode",
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
        "--config", "-c",
        type=click.Path(exists=True, dir_okay=False, resolve_path=True),
        default=None,
        envvar="PROVIDE_CONFIG_FILE",
        help="Path to configuration file",
    )(f)
    f = click.option(
        "--profile", "-p",
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
    - --quiet/-q: Suppress non-error output
    - --verbose/-v: Increase output verbosity
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
        "--quiet", "-q",
        is_flag=True,
        default=False,
        help="Suppress non-error output",
    )(f)
    f = click.option(
        "--verbose", "-v",
        count=True,
        default=0,
        help="Increase output verbosity (-vvv for max)",
    )(f)
    return f


def standard_options(f: F) -> F:
    """
    Apply all standard CLI options.
    
    Combines logging_options, config_options, and output_options.
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
        ctx = click.get_current_context()
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
            sys.exit(130)  # Standard exit code for SIGINT
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
            
            sys.exit(1)
    
    return wrapper


def pass_context(f: F) -> F:
    """
    Decorator to pass the foundation Context to a command.
    
    Creates or retrieves a Context from Click's context object
    and passes it as the first argument to the decorated function.
    """
    @functools.wraps(f)
    @click.pass_context
    def wrapper(ctx: click.Context, *args, **kwargs):
        # Get or create foundation context
        if not hasattr(ctx, "obj") or ctx.obj is None:
            ctx.obj = Context()
        elif not isinstance(ctx.obj, Context):
            # If obj exists but isn't a Context, wrap it
            if isinstance(ctx.obj, dict):
                ctx.obj = Context.from_dict(ctx.obj)
            else:
                # Store existing obj and create new Context
                old_obj = ctx.obj
                ctx.obj = Context()
                ctx.obj._cli_data = old_obj
        
        # Update context from command options
        if "log_level" in kwargs and kwargs["log_level"]:
            ctx.obj.log_level = kwargs["log_level"]
        if "log_file" in kwargs and kwargs["log_file"]:
            ctx.obj.log_file = kwargs["log_file"]
        if "debug" in kwargs and kwargs["debug"] is not None:
            ctx.obj.debug = kwargs["debug"]
        if "json_output" in kwargs and kwargs["json_output"] is not None:
            ctx.obj.json_output = kwargs["json_output"]
        if "profile" in kwargs and kwargs["profile"]:
            ctx.obj.profile = kwargs["profile"]
        if "config" in kwargs and kwargs["config"]:
            ctx.obj.load_config(kwargs["config"])
        
        # Remove these from kwargs to avoid duplicate arguments
        for key in ["log_level", "log_file", "debug", "json_output", "profile", "config"]:
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
            version=version,
            prog_name=prog_name,
            message="%(prog)s version %(version)s"
        )(f)
    
    return decorator