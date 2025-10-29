# provide/foundation/cli/helpers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


def x_get_message_from_stdin__mutmut_orig() -> tuple[str | None, int]:
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


def x_get_message_from_stdin__mutmut_1() -> tuple[str | None, int]:
    """Get message from stdin if available.

    Returns:
        Tuple of (message, error_code). If successful, error_code is 0.
        If stdin is a TTY (no piped input), returns (None, 1).

    """
    if sys.stdin.isatty():
        return None, 2

    try:
        message = sys.stdin.read().strip()
        if not message:
            click.echo("Error: Empty input from stdin.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_2() -> tuple[str | None, int]:
    """Get message from stdin if available.

    Returns:
        Tuple of (message, error_code). If successful, error_code is 0.
        If stdin is a TTY (no piped input), returns (None, 1).

    """
    if sys.stdin.isatty():
        return None, 1

    try:
        message = None
        if not message:
            click.echo("Error: Empty input from stdin.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_3() -> tuple[str | None, int]:
    """Get message from stdin if available.

    Returns:
        Tuple of (message, error_code). If successful, error_code is 0.
        If stdin is a TTY (no piped input), returns (None, 1).

    """
    if sys.stdin.isatty():
        return None, 1

    try:
        message = sys.stdin.read().strip()
        if message:
            click.echo("Error: Empty input from stdin.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_4() -> tuple[str | None, int]:
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
            click.echo(None, err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_5() -> tuple[str | None, int]:
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
            click.echo("Error: Empty input from stdin.", err=None)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_6() -> tuple[str | None, int]:
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
            click.echo(err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_7() -> tuple[str | None, int]:
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
            click.echo(
                "Error: Empty input from stdin.",
            )
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_8() -> tuple[str | None, int]:
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
            click.echo("XXError: Empty input from stdin.XX", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_9() -> tuple[str | None, int]:
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
            click.echo("error: empty input from stdin.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_10() -> tuple[str | None, int]:
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
            click.echo("ERROR: EMPTY INPUT FROM STDIN.", err=True)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_11() -> tuple[str | None, int]:
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
            click.echo("Error: Empty input from stdin.", err=False)
            return None, 1
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_12() -> tuple[str | None, int]:
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
            return None, 2
        return message, 0
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_13() -> tuple[str | None, int]:
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
        return message, 1
    except Exception as e:
        click.echo(f"Error reading from stdin: {e}", err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_14() -> tuple[str | None, int]:
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
        click.echo(None, err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_15() -> tuple[str | None, int]:
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
        click.echo(f"Error reading from stdin: {e}", err=None)
        return None, 1


def x_get_message_from_stdin__mutmut_16() -> tuple[str | None, int]:
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
        click.echo(err=True)
        return None, 1


def x_get_message_from_stdin__mutmut_17() -> tuple[str | None, int]:
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
        click.echo(
            f"Error reading from stdin: {e}",
        )
        return None, 1


def x_get_message_from_stdin__mutmut_18() -> tuple[str | None, int]:
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
        click.echo(f"Error reading from stdin: {e}", err=False)
        return None, 1


def x_get_message_from_stdin__mutmut_19() -> tuple[str | None, int]:
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
        return None, 2


x_get_message_from_stdin__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_message_from_stdin__mutmut_1": x_get_message_from_stdin__mutmut_1,
    "x_get_message_from_stdin__mutmut_2": x_get_message_from_stdin__mutmut_2,
    "x_get_message_from_stdin__mutmut_3": x_get_message_from_stdin__mutmut_3,
    "x_get_message_from_stdin__mutmut_4": x_get_message_from_stdin__mutmut_4,
    "x_get_message_from_stdin__mutmut_5": x_get_message_from_stdin__mutmut_5,
    "x_get_message_from_stdin__mutmut_6": x_get_message_from_stdin__mutmut_6,
    "x_get_message_from_stdin__mutmut_7": x_get_message_from_stdin__mutmut_7,
    "x_get_message_from_stdin__mutmut_8": x_get_message_from_stdin__mutmut_8,
    "x_get_message_from_stdin__mutmut_9": x_get_message_from_stdin__mutmut_9,
    "x_get_message_from_stdin__mutmut_10": x_get_message_from_stdin__mutmut_10,
    "x_get_message_from_stdin__mutmut_11": x_get_message_from_stdin__mutmut_11,
    "x_get_message_from_stdin__mutmut_12": x_get_message_from_stdin__mutmut_12,
    "x_get_message_from_stdin__mutmut_13": x_get_message_from_stdin__mutmut_13,
    "x_get_message_from_stdin__mutmut_14": x_get_message_from_stdin__mutmut_14,
    "x_get_message_from_stdin__mutmut_15": x_get_message_from_stdin__mutmut_15,
    "x_get_message_from_stdin__mutmut_16": x_get_message_from_stdin__mutmut_16,
    "x_get_message_from_stdin__mutmut_17": x_get_message_from_stdin__mutmut_17,
    "x_get_message_from_stdin__mutmut_18": x_get_message_from_stdin__mutmut_18,
    "x_get_message_from_stdin__mutmut_19": x_get_message_from_stdin__mutmut_19,
}


def get_message_from_stdin(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_message_from_stdin__mutmut_orig, x_get_message_from_stdin__mutmut_mutants, args, kwargs
    )
    return result


get_message_from_stdin.__signature__ = _mutmut_signature(x_get_message_from_stdin__mutmut_orig)
x_get_message_from_stdin__mutmut_orig.__name__ = "x_get_message_from_stdin"


def x__infer_and_parse_value__mutmut_orig(value: str) -> Any:
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


def x__infer_and_parse_value__mutmut_1(value: str) -> Any:
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
    if value.upper() in ("true", "false", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_2(value: str) -> Any:
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
    if value.lower() not in ("true", "false", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_3(value: str) -> Any:
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
    if value.lower() in ("XXtrueXX", "false", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_4(value: str) -> Any:
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
    if value.lower() in ("TRUE", "false", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_5(value: str) -> Any:
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
    if value.lower() in ("true", "XXfalseXX", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_6(value: str) -> Any:
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
    if value.lower() in ("true", "FALSE", "yes", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_7(value: str) -> Any:
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
    if value.lower() in ("true", "false", "XXyesXX", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_8(value: str) -> Any:
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
    if value.lower() in ("true", "false", "YES", "no", "1", "0"):
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


def x__infer_and_parse_value__mutmut_9(value: str) -> Any:
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
    if value.lower() in ("true", "false", "yes", "XXnoXX", "1", "0"):
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


def x__infer_and_parse_value__mutmut_10(value: str) -> Any:
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
    if value.lower() in ("true", "false", "yes", "NO", "1", "0"):
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


def x__infer_and_parse_value__mutmut_11(value: str) -> Any:
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
    if value.lower() in ("true", "false", "yes", "no", "XX1XX", "0"):
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


def x__infer_and_parse_value__mutmut_12(value: str) -> Any:
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
    if value.lower() in ("true", "false", "yes", "no", "1", "XX0XX"):
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


def x__infer_and_parse_value__mutmut_13(value: str) -> Any:
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
            return parse_typed_value(None, bool)
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


def x__infer_and_parse_value__mutmut_14(value: str) -> Any:
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
            return parse_typed_value(value, None)
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


def x__infer_and_parse_value__mutmut_15(value: str) -> Any:
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
            return parse_typed_value(bool)
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


def x__infer_and_parse_value__mutmut_16(value: str) -> Any:
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
            return parse_typed_value(
                value,
            )
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


def x__infer_and_parse_value__mutmut_17(value: str) -> Any:
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
            return parse_typed_value(None, int)
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


def x__infer_and_parse_value__mutmut_18(value: str) -> Any:
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
            return parse_typed_value(value, None)
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


def x__infer_and_parse_value__mutmut_19(value: str) -> Any:
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
            return parse_typed_value(int)
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


def x__infer_and_parse_value__mutmut_20(value: str) -> Any:
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
            return parse_typed_value(
                value,
            )
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


def x__infer_and_parse_value__mutmut_21(value: str) -> Any:
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
    if "XX.XX" in value:
        try:
            return parse_typed_value(value, float)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def x__infer_and_parse_value__mutmut_22(value: str) -> Any:
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
    if "." not in value:
        try:
            return parse_typed_value(value, float)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def x__infer_and_parse_value__mutmut_23(value: str) -> Any:
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
            return parse_typed_value(None, float)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def x__infer_and_parse_value__mutmut_24(value: str) -> Any:
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
            return parse_typed_value(value, None)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def x__infer_and_parse_value__mutmut_25(value: str) -> Any:
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
            return parse_typed_value(float)
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


def x__infer_and_parse_value__mutmut_26(value: str) -> Any:
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
            return parse_typed_value(
                value,
            )
        except (ValueError, TypeError):
            pass

    # Default to string (includes negative numbers)
    return value


x__infer_and_parse_value__mutmut_mutants: ClassVar[MutantDict] = {
    "x__infer_and_parse_value__mutmut_1": x__infer_and_parse_value__mutmut_1,
    "x__infer_and_parse_value__mutmut_2": x__infer_and_parse_value__mutmut_2,
    "x__infer_and_parse_value__mutmut_3": x__infer_and_parse_value__mutmut_3,
    "x__infer_and_parse_value__mutmut_4": x__infer_and_parse_value__mutmut_4,
    "x__infer_and_parse_value__mutmut_5": x__infer_and_parse_value__mutmut_5,
    "x__infer_and_parse_value__mutmut_6": x__infer_and_parse_value__mutmut_6,
    "x__infer_and_parse_value__mutmut_7": x__infer_and_parse_value__mutmut_7,
    "x__infer_and_parse_value__mutmut_8": x__infer_and_parse_value__mutmut_8,
    "x__infer_and_parse_value__mutmut_9": x__infer_and_parse_value__mutmut_9,
    "x__infer_and_parse_value__mutmut_10": x__infer_and_parse_value__mutmut_10,
    "x__infer_and_parse_value__mutmut_11": x__infer_and_parse_value__mutmut_11,
    "x__infer_and_parse_value__mutmut_12": x__infer_and_parse_value__mutmut_12,
    "x__infer_and_parse_value__mutmut_13": x__infer_and_parse_value__mutmut_13,
    "x__infer_and_parse_value__mutmut_14": x__infer_and_parse_value__mutmut_14,
    "x__infer_and_parse_value__mutmut_15": x__infer_and_parse_value__mutmut_15,
    "x__infer_and_parse_value__mutmut_16": x__infer_and_parse_value__mutmut_16,
    "x__infer_and_parse_value__mutmut_17": x__infer_and_parse_value__mutmut_17,
    "x__infer_and_parse_value__mutmut_18": x__infer_and_parse_value__mutmut_18,
    "x__infer_and_parse_value__mutmut_19": x__infer_and_parse_value__mutmut_19,
    "x__infer_and_parse_value__mutmut_20": x__infer_and_parse_value__mutmut_20,
    "x__infer_and_parse_value__mutmut_21": x__infer_and_parse_value__mutmut_21,
    "x__infer_and_parse_value__mutmut_22": x__infer_and_parse_value__mutmut_22,
    "x__infer_and_parse_value__mutmut_23": x__infer_and_parse_value__mutmut_23,
    "x__infer_and_parse_value__mutmut_24": x__infer_and_parse_value__mutmut_24,
    "x__infer_and_parse_value__mutmut_25": x__infer_and_parse_value__mutmut_25,
    "x__infer_and_parse_value__mutmut_26": x__infer_and_parse_value__mutmut_26,
}


def _infer_and_parse_value(*args, **kwargs):
    result = _mutmut_trampoline(
        x__infer_and_parse_value__mutmut_orig, x__infer_and_parse_value__mutmut_mutants, args, kwargs
    )
    return result


_infer_and_parse_value.__signature__ = _mutmut_signature(x__infer_and_parse_value__mutmut_orig)
x__infer_and_parse_value__mutmut_orig.__name__ = "x__infer_and_parse_value"


def x_build_attributes_from_args__mutmut_orig(
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


def x_build_attributes_from_args__mutmut_1(
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
    attributes: dict[str, Any] = None

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


def x_build_attributes_from_args__mutmut_2(
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
            json_dict = None
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


def x_build_attributes_from_args__mutmut_3(
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
            json_dict = json_loads(None)
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


def x_build_attributes_from_args__mutmut_4(
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
            if isinstance(json_dict, dict):
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


def x_build_attributes_from_args__mutmut_5(
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
                click.echo(None, err=True)
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


def x_build_attributes_from_args__mutmut_6(
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
                click.echo("Error: JSON attributes must be an object.", err=None)
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


def x_build_attributes_from_args__mutmut_7(
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
                click.echo(err=True)
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


def x_build_attributes_from_args__mutmut_8(
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
                click.echo(
                    "Error: JSON attributes must be an object.",
                )
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


def x_build_attributes_from_args__mutmut_9(
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
                click.echo("XXError: JSON attributes must be an object.XX", err=True)
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


def x_build_attributes_from_args__mutmut_10(
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
                click.echo("error: json attributes must be an object.", err=True)
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


def x_build_attributes_from_args__mutmut_11(
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
                click.echo("ERROR: JSON ATTRIBUTES MUST BE AN OBJECT.", err=True)
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


def x_build_attributes_from_args__mutmut_12(
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
                click.echo("Error: JSON attributes must be an object.", err=False)
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


def x_build_attributes_from_args__mutmut_13(
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
                return {}, 2
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


def x_build_attributes_from_args__mutmut_14(
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
            attributes.update(None)
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


def x_build_attributes_from_args__mutmut_15(
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
            click.echo(None, err=True)
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


def x_build_attributes_from_args__mutmut_16(
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
            click.echo(f"Error: Invalid JSON attributes: {e}", err=None)
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


def x_build_attributes_from_args__mutmut_17(
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
            click.echo(err=True)
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


def x_build_attributes_from_args__mutmut_18(
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
            click.echo(
                f"Error: Invalid JSON attributes: {e}",
            )
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


def x_build_attributes_from_args__mutmut_19(
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
            click.echo(f"Error: Invalid JSON attributes: {e}", err=False)
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


def x_build_attributes_from_args__mutmut_20(
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
            return {}, 2

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


def x_build_attributes_from_args__mutmut_21(
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
            key, value = None
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_22(
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
            key, value = kv_pair.split(None, 1)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_23(
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
            key, value = kv_pair.split("=", None)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_24(
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
            key, value = kv_pair.split(1)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_25(
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
            key, value = kv_pair.split(
                "=",
            )
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_26(
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
            key, value = kv_pair.rsplit("=", 1)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_27(
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
            key, value = kv_pair.split("XX=XX", 1)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_28(
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
            key, value = kv_pair.split("=", 2)
            attributes[key] = _infer_and_parse_value(value)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_29(
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
            attributes[key] = None
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_30(
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
            attributes[key] = _infer_and_parse_value(None)
        except ValueError:
            click.echo(
                f"Error: Invalid attribute format '{kv_pair}'. Use key=value.",
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_31(
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
                None,
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_32(
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
                err=None,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_33(
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
                err=True,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_34(
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
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_35(
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
                err=False,
            )
            return {}, 1

    return attributes, 0


def x_build_attributes_from_args__mutmut_36(
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
            return {}, 2

    return attributes, 0


def x_build_attributes_from_args__mutmut_37(
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

    return attributes, 1


x_build_attributes_from_args__mutmut_mutants: ClassVar[MutantDict] = {
    "x_build_attributes_from_args__mutmut_1": x_build_attributes_from_args__mutmut_1,
    "x_build_attributes_from_args__mutmut_2": x_build_attributes_from_args__mutmut_2,
    "x_build_attributes_from_args__mutmut_3": x_build_attributes_from_args__mutmut_3,
    "x_build_attributes_from_args__mutmut_4": x_build_attributes_from_args__mutmut_4,
    "x_build_attributes_from_args__mutmut_5": x_build_attributes_from_args__mutmut_5,
    "x_build_attributes_from_args__mutmut_6": x_build_attributes_from_args__mutmut_6,
    "x_build_attributes_from_args__mutmut_7": x_build_attributes_from_args__mutmut_7,
    "x_build_attributes_from_args__mutmut_8": x_build_attributes_from_args__mutmut_8,
    "x_build_attributes_from_args__mutmut_9": x_build_attributes_from_args__mutmut_9,
    "x_build_attributes_from_args__mutmut_10": x_build_attributes_from_args__mutmut_10,
    "x_build_attributes_from_args__mutmut_11": x_build_attributes_from_args__mutmut_11,
    "x_build_attributes_from_args__mutmut_12": x_build_attributes_from_args__mutmut_12,
    "x_build_attributes_from_args__mutmut_13": x_build_attributes_from_args__mutmut_13,
    "x_build_attributes_from_args__mutmut_14": x_build_attributes_from_args__mutmut_14,
    "x_build_attributes_from_args__mutmut_15": x_build_attributes_from_args__mutmut_15,
    "x_build_attributes_from_args__mutmut_16": x_build_attributes_from_args__mutmut_16,
    "x_build_attributes_from_args__mutmut_17": x_build_attributes_from_args__mutmut_17,
    "x_build_attributes_from_args__mutmut_18": x_build_attributes_from_args__mutmut_18,
    "x_build_attributes_from_args__mutmut_19": x_build_attributes_from_args__mutmut_19,
    "x_build_attributes_from_args__mutmut_20": x_build_attributes_from_args__mutmut_20,
    "x_build_attributes_from_args__mutmut_21": x_build_attributes_from_args__mutmut_21,
    "x_build_attributes_from_args__mutmut_22": x_build_attributes_from_args__mutmut_22,
    "x_build_attributes_from_args__mutmut_23": x_build_attributes_from_args__mutmut_23,
    "x_build_attributes_from_args__mutmut_24": x_build_attributes_from_args__mutmut_24,
    "x_build_attributes_from_args__mutmut_25": x_build_attributes_from_args__mutmut_25,
    "x_build_attributes_from_args__mutmut_26": x_build_attributes_from_args__mutmut_26,
    "x_build_attributes_from_args__mutmut_27": x_build_attributes_from_args__mutmut_27,
    "x_build_attributes_from_args__mutmut_28": x_build_attributes_from_args__mutmut_28,
    "x_build_attributes_from_args__mutmut_29": x_build_attributes_from_args__mutmut_29,
    "x_build_attributes_from_args__mutmut_30": x_build_attributes_from_args__mutmut_30,
    "x_build_attributes_from_args__mutmut_31": x_build_attributes_from_args__mutmut_31,
    "x_build_attributes_from_args__mutmut_32": x_build_attributes_from_args__mutmut_32,
    "x_build_attributes_from_args__mutmut_33": x_build_attributes_from_args__mutmut_33,
    "x_build_attributes_from_args__mutmut_34": x_build_attributes_from_args__mutmut_34,
    "x_build_attributes_from_args__mutmut_35": x_build_attributes_from_args__mutmut_35,
    "x_build_attributes_from_args__mutmut_36": x_build_attributes_from_args__mutmut_36,
    "x_build_attributes_from_args__mutmut_37": x_build_attributes_from_args__mutmut_37,
}


def build_attributes_from_args(*args, **kwargs):
    result = _mutmut_trampoline(
        x_build_attributes_from_args__mutmut_orig, x_build_attributes_from_args__mutmut_mutants, args, kwargs
    )
    return result


build_attributes_from_args.__signature__ = _mutmut_signature(x_build_attributes_from_args__mutmut_orig)
x_build_attributes_from_args__mutmut_orig.__name__ = "x_build_attributes_from_args"


def x_parse_filter_string__mutmut_orig(filter_str: str) -> dict[str, str]:
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


def x_parse_filter_string__mutmut_1(filter_str: str) -> dict[str, str]:
    """Parse filter string into key-value dictionary.

    Uses the parsers module for consistent parsing behavior.

    Args:
        filter_str: Filter string in format 'key1=value1,key2=value2'

    Returns:
        Dictionary of filter key-value pairs

    """
    if filter_str:
        return {}

    try:
        return parse_dict(filter_str, item_separator=",", key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_2(filter_str: str) -> dict[str, str]:
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
        return parse_dict(None, item_separator=",", key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_3(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=None, key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_4(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=",", key_separator=None, strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_5(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=",", key_separator="=", strip=None)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_6(filter_str: str) -> dict[str, str]:
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
        return parse_dict(item_separator=",", key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_7(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_8(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=",", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_9(filter_str: str) -> dict[str, str]:
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
        return parse_dict(
            filter_str,
            item_separator=",",
            key_separator="=",
        )
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_10(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator="XX,XX", key_separator="=", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_11(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=",", key_separator="XX=XX", strip=True)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_12(filter_str: str) -> dict[str, str]:
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
        return parse_dict(filter_str, item_separator=",", key_separator="=", strip=False)
    except ValueError as e:
        click.echo(f"Warning: Invalid filter format: {e}", err=True)
        return {}


def x_parse_filter_string__mutmut_13(filter_str: str) -> dict[str, str]:
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
        click.echo(None, err=True)
        return {}


def x_parse_filter_string__mutmut_14(filter_str: str) -> dict[str, str]:
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
        click.echo(f"Warning: Invalid filter format: {e}", err=None)
        return {}


def x_parse_filter_string__mutmut_15(filter_str: str) -> dict[str, str]:
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
        click.echo(err=True)
        return {}


def x_parse_filter_string__mutmut_16(filter_str: str) -> dict[str, str]:
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
        click.echo(
            f"Warning: Invalid filter format: {e}",
        )
        return {}


def x_parse_filter_string__mutmut_17(filter_str: str) -> dict[str, str]:
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
        click.echo(f"Warning: Invalid filter format: {e}", err=False)
        return {}


x_parse_filter_string__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_filter_string__mutmut_1": x_parse_filter_string__mutmut_1,
    "x_parse_filter_string__mutmut_2": x_parse_filter_string__mutmut_2,
    "x_parse_filter_string__mutmut_3": x_parse_filter_string__mutmut_3,
    "x_parse_filter_string__mutmut_4": x_parse_filter_string__mutmut_4,
    "x_parse_filter_string__mutmut_5": x_parse_filter_string__mutmut_5,
    "x_parse_filter_string__mutmut_6": x_parse_filter_string__mutmut_6,
    "x_parse_filter_string__mutmut_7": x_parse_filter_string__mutmut_7,
    "x_parse_filter_string__mutmut_8": x_parse_filter_string__mutmut_8,
    "x_parse_filter_string__mutmut_9": x_parse_filter_string__mutmut_9,
    "x_parse_filter_string__mutmut_10": x_parse_filter_string__mutmut_10,
    "x_parse_filter_string__mutmut_11": x_parse_filter_string__mutmut_11,
    "x_parse_filter_string__mutmut_12": x_parse_filter_string__mutmut_12,
    "x_parse_filter_string__mutmut_13": x_parse_filter_string__mutmut_13,
    "x_parse_filter_string__mutmut_14": x_parse_filter_string__mutmut_14,
    "x_parse_filter_string__mutmut_15": x_parse_filter_string__mutmut_15,
    "x_parse_filter_string__mutmut_16": x_parse_filter_string__mutmut_16,
    "x_parse_filter_string__mutmut_17": x_parse_filter_string__mutmut_17,
}


def parse_filter_string(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_filter_string__mutmut_orig, x_parse_filter_string__mutmut_mutants, args, kwargs
    )
    return result


parse_filter_string.__signature__ = _mutmut_signature(x_parse_filter_string__mutmut_orig)
x_parse_filter_string__mutmut_orig.__name__ = "x_parse_filter_string"


def x_format_duration__mutmut_orig(seconds: float) -> str:
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


def x_format_duration__mutmut_1(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Delegates to formatting.numbers.format_duration() with short format
    and adds spaces between components for CLI readability.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1h 23m 45s", "45s", "1.5s")

    """
    # Handle sub-minute durations with decimal precision
    if seconds <= 60:
        return f"{seconds:.1f}s"

    # Use formatting module for consistency, with short format
    # The formatting module produces "1h23m45s", we want "1h 23m 45s"
    formatted = _format_duration(seconds, short=True)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_2(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Delegates to formatting.numbers.format_duration() with short format
    and adds spaces between components for CLI readability.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "1h 23m 45s", "45s", "1.5s")

    """
    # Handle sub-minute durations with decimal precision
    if seconds < 61:
        return f"{seconds:.1f}s"

    # Use formatting module for consistency, with short format
    # The formatting module produces "1h23m45s", we want "1h 23m 45s"
    formatted = _format_duration(seconds, short=True)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_3(seconds: float) -> str:
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
    formatted = None

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_4(seconds: float) -> str:
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
    formatted = _format_duration(None, short=True)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_5(seconds: float) -> str:
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
    formatted = _format_duration(seconds, short=None)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_6(seconds: float) -> str:
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
    formatted = _format_duration(short=True)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_7(seconds: float) -> str:
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
    formatted = _format_duration(
        seconds,
    )

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_8(seconds: float) -> str:
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
    formatted = _format_duration(seconds, short=False)

    # Add spaces between components for better CLI readability
    # Transform "1h23m45s" → "1h 23m 45s"
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_9(seconds: float) -> str:
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
    result = None
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_10(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace(None, "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_11(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", None)
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_12(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_13(seconds: float) -> str:
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
    result = (
        formatted.replace("h", "h ")
        .replace("m", "m ")
        .replace(
            "d",
        )
    )
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_14(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace(None, "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_15(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", None).replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_16(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_17(seconds: float) -> str:
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
    result = (
        formatted.replace("h", "h ")
        .replace(
            "m",
        )
        .replace("d", "d ")
    )
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_18(seconds: float) -> str:
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
    result = formatted.replace(None, "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_19(seconds: float) -> str:
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
    result = formatted.replace("h", None).replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_20(seconds: float) -> str:
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
    result = formatted.replace("h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_21(seconds: float) -> str:
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
    result = (
        formatted.replace(
            "h",
        )
        .replace("m", "m ")
        .replace("d", "d ")
    )
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_22(seconds: float) -> str:
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
    result = formatted.replace("XXhXX", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_23(seconds: float) -> str:
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
    result = formatted.replace("H", "h ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_24(seconds: float) -> str:
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
    result = formatted.replace("h", "XXh XX").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_25(seconds: float) -> str:
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
    result = formatted.replace("h", "H ").replace("m", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_26(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("XXmXX", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_27(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("M", "m ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_28(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "XXm XX").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_29(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "M ").replace("d", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_30(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("XXdXX", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_31(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("D", "d ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_32(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "XXd XX")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_33(seconds: float) -> str:
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
    result = formatted.replace("h", "h ").replace("m", "m ").replace("d", "D ")
    return result.rstrip()  # Remove trailing space


def x_format_duration__mutmut_34(seconds: float) -> str:
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
    return result.lstrip()  # Remove trailing space


x_format_duration__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_duration__mutmut_1": x_format_duration__mutmut_1,
    "x_format_duration__mutmut_2": x_format_duration__mutmut_2,
    "x_format_duration__mutmut_3": x_format_duration__mutmut_3,
    "x_format_duration__mutmut_4": x_format_duration__mutmut_4,
    "x_format_duration__mutmut_5": x_format_duration__mutmut_5,
    "x_format_duration__mutmut_6": x_format_duration__mutmut_6,
    "x_format_duration__mutmut_7": x_format_duration__mutmut_7,
    "x_format_duration__mutmut_8": x_format_duration__mutmut_8,
    "x_format_duration__mutmut_9": x_format_duration__mutmut_9,
    "x_format_duration__mutmut_10": x_format_duration__mutmut_10,
    "x_format_duration__mutmut_11": x_format_duration__mutmut_11,
    "x_format_duration__mutmut_12": x_format_duration__mutmut_12,
    "x_format_duration__mutmut_13": x_format_duration__mutmut_13,
    "x_format_duration__mutmut_14": x_format_duration__mutmut_14,
    "x_format_duration__mutmut_15": x_format_duration__mutmut_15,
    "x_format_duration__mutmut_16": x_format_duration__mutmut_16,
    "x_format_duration__mutmut_17": x_format_duration__mutmut_17,
    "x_format_duration__mutmut_18": x_format_duration__mutmut_18,
    "x_format_duration__mutmut_19": x_format_duration__mutmut_19,
    "x_format_duration__mutmut_20": x_format_duration__mutmut_20,
    "x_format_duration__mutmut_21": x_format_duration__mutmut_21,
    "x_format_duration__mutmut_22": x_format_duration__mutmut_22,
    "x_format_duration__mutmut_23": x_format_duration__mutmut_23,
    "x_format_duration__mutmut_24": x_format_duration__mutmut_24,
    "x_format_duration__mutmut_25": x_format_duration__mutmut_25,
    "x_format_duration__mutmut_26": x_format_duration__mutmut_26,
    "x_format_duration__mutmut_27": x_format_duration__mutmut_27,
    "x_format_duration__mutmut_28": x_format_duration__mutmut_28,
    "x_format_duration__mutmut_29": x_format_duration__mutmut_29,
    "x_format_duration__mutmut_30": x_format_duration__mutmut_30,
    "x_format_duration__mutmut_31": x_format_duration__mutmut_31,
    "x_format_duration__mutmut_32": x_format_duration__mutmut_32,
    "x_format_duration__mutmut_33": x_format_duration__mutmut_33,
    "x_format_duration__mutmut_34": x_format_duration__mutmut_34,
}


def format_duration(*args, **kwargs):
    result = _mutmut_trampoline(
        x_format_duration__mutmut_orig, x_format_duration__mutmut_mutants, args, kwargs
    )
    return result


format_duration.__signature__ = _mutmut_signature(x_format_duration__mutmut_orig)
x_format_duration__mutmut_orig.__name__ = "x_format_duration"


def x_get_client_from_context__mutmut_orig(ctx: Any) -> tuple[Any | None, int]:
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


def x_get_client_from_context__mutmut_1(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_2(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get(None) if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_3(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("XXclientXX") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_4(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("CLIENT") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_5(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_6(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo(None, err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_7(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=None)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_8(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo(err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_9(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo(
            "Error: OpenObserve not configured.",
        )
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_10(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("XXError: OpenObserve not configured.XX", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_11(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("error: openobserve not configured.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_12(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("ERROR: OPENOBSERVE NOT CONFIGURED.", err=True)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_13(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=False)
        return None, 1
    return client, 0


def x_get_client_from_context__mutmut_14(ctx: Any) -> tuple[Any | None, int]:
    """Get OpenObserve client from Click context.

    Args:
        ctx: Click context object

    Returns:
        Tuple of (client, error_code). Error code is 0 on success.

    """
    client = ctx.obj.get("client") if ctx.obj else None
    if not client:
        click.echo("Error: OpenObserve not configured.", err=True)
        return None, 2
    return client, 0


def x_get_client_from_context__mutmut_15(ctx: Any) -> tuple[Any | None, int]:
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
    return client, 1


x_get_client_from_context__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_client_from_context__mutmut_1": x_get_client_from_context__mutmut_1,
    "x_get_client_from_context__mutmut_2": x_get_client_from_context__mutmut_2,
    "x_get_client_from_context__mutmut_3": x_get_client_from_context__mutmut_3,
    "x_get_client_from_context__mutmut_4": x_get_client_from_context__mutmut_4,
    "x_get_client_from_context__mutmut_5": x_get_client_from_context__mutmut_5,
    "x_get_client_from_context__mutmut_6": x_get_client_from_context__mutmut_6,
    "x_get_client_from_context__mutmut_7": x_get_client_from_context__mutmut_7,
    "x_get_client_from_context__mutmut_8": x_get_client_from_context__mutmut_8,
    "x_get_client_from_context__mutmut_9": x_get_client_from_context__mutmut_9,
    "x_get_client_from_context__mutmut_10": x_get_client_from_context__mutmut_10,
    "x_get_client_from_context__mutmut_11": x_get_client_from_context__mutmut_11,
    "x_get_client_from_context__mutmut_12": x_get_client_from_context__mutmut_12,
    "x_get_client_from_context__mutmut_13": x_get_client_from_context__mutmut_13,
    "x_get_client_from_context__mutmut_14": x_get_client_from_context__mutmut_14,
    "x_get_client_from_context__mutmut_15": x_get_client_from_context__mutmut_15,
}


def get_client_from_context(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_client_from_context__mutmut_orig, x_get_client_from_context__mutmut_mutants, args, kwargs
    )
    return result


get_client_from_context.__signature__ = _mutmut_signature(x_get_client_from_context__mutmut_orig)
x_get_client_from_context__mutmut_orig.__name__ = "x_get_client_from_context"


__all__ = [
    "build_attributes_from_args",
    "format_duration",
    "get_client_from_context",
    "get_message_from_stdin",
    "parse_filter_string",
    "requires_click",
]


# <3 🧱🤝💻🪄
