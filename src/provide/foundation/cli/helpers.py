#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import functools
import sys
from typing import Any, ParamSpec, TypeVar

from provide.foundation.cli.deps import _HAS_CLICK, click
from provide.foundation.errors import ValidationError
from provide.foundation.formatting import format_duration as _format_duration
from provide.foundation.parsers import parse_dict, parse_typed_value
from provide.foundation.serialization import json_loads

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

    return wrapper


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


def _infer_and_parse_value(value: str) -> Any:
    """Infer type from string value and parse using parsers module.

    Tries to detect the type in order: bool, int, float, str.
    Uses the parsers module for consistent parsing behavior.

    Note: Negative numbers are treated as strings to maintain
    compatibility with existing behavior.

    Args:
        value: String value to parse

    Returns:
        Parsed value with inferred type

    """
    # Try bool (handles "true", "false", "yes", "no", "1", "0")
    if value.lower() in ("true", "false", "yes", "no", "1", "0"):
        try:
            return parse_typed_value(value, bool)
        except (ValueError, TypeError):
            pass

    # Try int (positive numbers only, negative numbers treated as strings)
    if value.isdigit():
        try:
            return parse_typed_value(value, int)
        except (ValueError, TypeError):
            pass

    # Try float (handles decimal numbers)
    if "." in value:
        try:
            return parse_typed_value(value, float)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def build_attributes_from_args(
    json_attrs: str | None,
    attr: tuple[str, ...],
) -> tuple[dict[str, Any], int]:
    """Build attributes dictionary from JSON and key=value arguments.

    Uses the parsers module for consistent type inference and parsing.

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
            json_dict = json_loads(json_attrs)
            if not isinstance(json_dict, dict):
                click.echo("Error: JSON attributes must be an object.", err=True)
                return {}, 1
            attributes.update(json_dict)
        except (ValueError, TypeError, ValidationError) as e:
            click.echo(f"Error: Invalid JSON attributes: {e}", err=True)
            return {}, 1

    # Add key=value attributes with automatic type inference
    for kv_pair in attr:
        try:
            key, value = kv_pair.split("=", 1)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def parse_filter_string(filter_str: str) -> dict[str, str]:
    """Parse filter string into key-value dictionary.

    Uses the parsers module for consistent parsing behavior.

    Args:
        filter_str: Filter string in format 'key1=value1,key2=value2'

    Returns:
        Dictionary of filter key-value pairs

    """
    if not filter_str:
        return {}

    try:
        return parse_dict(filter_str, item_separator=",", key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Delegates to formatting.numbers.format_duration() with short format
    and adds spaces between components for CLI readability.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1h 23m 45s", "45s", "1.5s")

    """
    # Handle sub-minute durations with decimal precision
    if seconds < 60:
        return f"{seconds:.1f}s"

    # Use formatting module for consistency, with short format
    # The formatting module produces "1h23m45s", we want "1h 23m 45s"
    formatted = _format_duration(seconds, short=True)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


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

# 🧱🏗️🔚
