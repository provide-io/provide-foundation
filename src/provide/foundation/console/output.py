"""
Core console output functions for standardized CLI output.

Provides pout() and perr() for consistent output handling with support
for JSON mode, colors, and proper stream separation.
"""

import json
import os
import sys
from typing import Any

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.context import CLIContext
from provide.foundation.errors.decorators import with_error_handling
from provide.foundation.logger import get_logger

log = get_logger(__name__)


def _get_context() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def _should_use_json(ctx: CLIContext | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is None:
        ctx = _get_context()
    return ctx.json_output if ctx else False


def _should_use_color(ctx: CLIContext | None = None, stream=None) -> bool:
    """Determine if color output should be used."""
    if ctx is None:
        ctx = _get_context()

    # Check FORCE_COLOR first (enables color even for non-TTY)
    force_color = os.environ.get('FORCE_COLOR', '').lower()
    if force_color in ('1', 'true', 'yes'):
        return True

    # Check NO_COLOR (disables color even for TTY)
    if os.environ.get('NO_COLOR'):
        return False

    # Check context no_color setting
    if ctx and ctx.no_color:
        return False

    # Check if stream is a TTY
    if stream:
        return getattr(stream, "isatty", lambda: False)()

    return sys.stdout.isatty() or sys.stderr.isatty()


@with_error_handling(fallback=None, suppress=(TypeError, ValueError, AttributeError))
def _output_json(data: Any, stream=sys.stdout) -> None:
    """Output data as JSON."""
    json_str = json.dumps(data, indent=2, default=str)
    if _HAS_CLICK:
        click.echo(json_str, file=stream)
    else:
        print(json_str, file=stream)


@with_error_handling(
    fallback=None,
    suppress=(OSError, IOError, UnicodeEncodeError),
    context_provider=lambda: {"function": "pout"}
)
def pout(message: Any, **kwargs: Any) -> None:
    """
    Output message to stdout.

    Args:
        message: Content to output (any type - will be stringified or JSON-encoded)
        **kwargs: Optional formatting arguments:
            color: Color name (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold text
            dim: Dim text
            nl/newline: Add newline (default: True)
            json_key: Key for JSON output mode
            prefix: Optional prefix string
            ctx: Override context

    Examples:
        pout("Hello world")
        pout({"data": "value"})  # Auto-JSON if dict/list
        pout("Success", color="green", bold=True)
        pout(results, json_key="results")
    """
    ctx = kwargs.get("ctx") or _get_context()

    # Handle newline option (support both nl and newline)
    nl = kwargs.get("nl", kwargs.get("newline", True))

    if _should_use_json(ctx):
        # JSON mode
        if kwargs.get("json_key"):
            _output_json({kwargs["json_key"]: message}, sys.stdout)
        else:
            _output_json(message, sys.stdout)
    else:
        # Regular output mode
        # Add optional prefix
        output = str(message)
        if prefix := kwargs.get("prefix"):
            output = f"{prefix} {output}"

        # Apply color/formatting if requested and supported
        color = kwargs.get("color")
        bold = kwargs.get("bold", False)
        dim = kwargs.get("dim", False)

        if _HAS_CLICK:
            if (color or bold or dim) and _should_use_color(ctx, sys.stdout):
                click.secho(output, fg=color, bold=bold, dim=dim, nl=nl)
            else:
                click.echo(output, nl=nl)
        else:
            # Fallback to standard Python print
            if nl:
                print(output, file=sys.stdout)
            else:
                print(output, file=sys.stdout, end="")


@with_error_handling(
    fallback=None,
    suppress=(OSError, IOError, UnicodeEncodeError),
    context_provider=lambda: {"function": "perr"}
)
def perr(message: Any, **kwargs: Any) -> None:
    """
    Output message to stderr.

    Args:
        message: Content to output (any type - will be stringified or JSON-encoded)
        **kwargs: Optional formatting arguments:
            color: Color name (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold text
            dim: Dim text
            nl/newline: Add newline (default: True)
            json_key: Key for JSON output mode
            prefix: Optional prefix string
            ctx: Override context

    Examples:
        perr("Error occurred")
        perr("Warning", color="yellow")
        perr({"error": details}, json_key="error")
    """
    ctx = kwargs.get("ctx") or _get_context()

    # Handle newline option (support both nl and newline)
    nl = kwargs.get("nl", kwargs.get("newline", True))

    if _should_use_json(ctx):
        # JSON mode
        if kwargs.get("json_key"):
            _output_json({kwargs["json_key"]: message}, sys.stderr)
        else:
            _output_json(message, sys.stderr)
    else:
        # Regular output mode
        # Add optional prefix
        output = str(message)
        if prefix := kwargs.get("prefix"):
            output = f"{prefix} {output}"

        # Apply color/formatting if requested and supported
        color = kwargs.get("color")
        bold = kwargs.get("bold", False)
        dim = kwargs.get("dim", False)

        if _HAS_CLICK:
            if (color or bold or dim) and _should_use_color(ctx, sys.stderr):
                click.secho(output, fg=color, bold=bold, dim=dim, err=True, nl=nl)
            else:
                click.echo(output, err=True, nl=nl)
        else:
            # Fallback to standard Python print
            if nl:
                print(output, file=sys.stderr)
            else:
                print(output, file=sys.stderr, end="")
