from __future__ import annotations

from collections.abc import Callable
import functools
import json
import sys
from typing import Any, ParamSpec, TypeVar

from provide.foundation.cli.deps import _HAS_CLICK, click
from provide.foundation.parsers import parse_dict, parse_typed_value

"""Shared utilities for CLI commands.

Provides common helper functions to reduce code duplication across
CLI command implementations.
"""

# Type variables for decorators
P = ParamSpec("P")
R = TypeVar("R")


def requires_click(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to ensure Click is available for CLI commands.

    Replaces the boilerplate if _HAS_CLICK / else ImportError stub pattern.

    Example:
        @requires_click
        def my_command(*args, **kwargs):
            # Command implementation
            pass

    Args:
        func: CLI command function to wrap

    Returns:
        Wrapped function that raises ImportError if Click is not available

    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not _HAS_CLICK:
            raise ImportError(
                "CLI commands require optional dependencies. "
                "Install with: pip install 'provide-foundation[cli]'"
            )
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def get_message_from_stdin() -> tuple[str | None, int]:
    """Get message from stdin if available.

    Returns:
        Tuple of (message, error_code). If successful, error_code is 0.
        If stdin is a TTY (no piped input), returns (None, 1).

    """
    if sys.stdin.isatty():
        return None, 1

    try:
        message = sys.stdin.read().strip()
        if not message:
            click.echo("Error: Empty input from stdin.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def build_attributes_from_args(
    json_attrs: str | None,
    attr: tuple[str, ...],
) -> tuple[dict[str, Any], int]:
    """Build attributes dictionary from JSON and key=value arguments.

    Args:
        json_attrs: JSON string of attributes
        attr: Tuple of key=value attribute strings

    Returns:
        Tuple of (attributes dict, error_code). Error code is 0 on success.

    """
    attributes: dict[str, Any] = {}

    # Parse JSON attributes first
    if json_attrs:
        try:
            json_dict = json.loads(json_attrs)
            if not isinstance(json_dict, dict):
                click.echo("Error: JSON attributes must be an object.", err=True)
                return {}, 1
            attributes.update(json_dict)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON attributes: {e}", err=True)
            return {}, 1

    # Add key=value attributes
    for kv_pair in attr:
        try:
            key, value = kv_pair.split("=", 1)
            # Try to parse as number, boolean, or keep as string
            if value.lower() in ("true", "false"):
                attributes[key] = value.lower() == "true"
            elif value.isdigit():
                attributes[key] = int(value)
            elif "." in value and value.replace(".", "").replace("-", "").isdigit():
                attributes[key] = float(value)
            else:
                attributes[key] = value
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def parse_filter_string(filter_str: str) -> dict[str, str]:
    """Parse filter string into key-value dictionary.

    Args:
        filter_str: Filter string in format 'key1=value1,key2=value2'

    Returns:
        Dictionary of filter key-value pairs

    """
    filters = {}
    if not filter_str:
        return filters

    for pair in filter_str.split(","):
        try:
            key, value = pair.split("=", 1)
            filters[key.strip()] = value.strip()
        except ValueError:
            click.echo(f"Warning: Invalid filter pair '{pair}', skipping.", err=True)

    return filters


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1h 23m 45s", "45s", "1.5s")

    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m {remaining_seconds}s"


def get_client_from_context(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


__all__ = [
    "build_attributes_from_args",
    "format_duration",
    "get_client_from_context",
    "get_message_from_stdin",
    "parse_filter_string",
    "requires_click",
]
