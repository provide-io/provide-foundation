# provide/foundation/console/input.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator
import contextlib
import sys
from typing import TYPE_CHECKING, Any, TypeVar

from provide.foundation.context import CLIContext
from provide.foundation.errors import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.serialization import json_dumps, json_loads

try:
    import click

    _HAS_CLICK = True
except ImportError:
    if TYPE_CHECKING:
        import click
    else:
        click: Any = None
    _HAS_CLICK = False

"""Core console input functions for standardized CLI input.

Provides pin() and async variants for consistent input handling with support
for JSON mode, streaming, and proper integration with the foundation's patterns.
"""

log = get_logger(__name__)

T = TypeVar("T")
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


def x__get_context__mutmut_orig() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_1() -> CLIContext | None:
    """Get current context from Click or environment."""
    if _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_2() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = None
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_3() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=None)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_4() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=False)
    if ctx and hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_5() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "obj") or isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_6() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx or hasattr(ctx, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_7() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(None, "obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_8() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, None) and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_9() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr("obj") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_10() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if (
        ctx
        and hasattr(
            ctx,
        )
        and isinstance(ctx.obj, CLIContext)
    ):
        return ctx.obj
    return None


def x__get_context__mutmut_11() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "XXobjXX") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


def x__get_context__mutmut_12() -> CLIContext | None:
    """Get current context from Click or environment."""
    if not _HAS_CLICK:
        return None
    ctx = click.get_current_context(silent=True)
    if ctx and hasattr(ctx, "OBJ") and isinstance(ctx.obj, CLIContext):
        return ctx.obj
    return None


x__get_context__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_context__mutmut_1": x__get_context__mutmut_1,
    "x__get_context__mutmut_2": x__get_context__mutmut_2,
    "x__get_context__mutmut_3": x__get_context__mutmut_3,
    "x__get_context__mutmut_4": x__get_context__mutmut_4,
    "x__get_context__mutmut_5": x__get_context__mutmut_5,
    "x__get_context__mutmut_6": x__get_context__mutmut_6,
    "x__get_context__mutmut_7": x__get_context__mutmut_7,
    "x__get_context__mutmut_8": x__get_context__mutmut_8,
    "x__get_context__mutmut_9": x__get_context__mutmut_9,
    "x__get_context__mutmut_10": x__get_context__mutmut_10,
    "x__get_context__mutmut_11": x__get_context__mutmut_11,
    "x__get_context__mutmut_12": x__get_context__mutmut_12,
}


def _get_context(*args, **kwargs):
    result = _mutmut_trampoline(x__get_context__mutmut_orig, x__get_context__mutmut_mutants, args, kwargs)
    return result


_get_context.__signature__ = _mutmut_signature(x__get_context__mutmut_orig)
x__get_context__mutmut_orig.__name__ = "x__get_context"


def x__should_use_json__mutmut_orig(ctx: CLIContext | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is None:
        ctx = _get_context()
    return ctx.json_output if ctx else False


def x__should_use_json__mutmut_1(ctx: CLIContext | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is not None:
        ctx = _get_context()
    return ctx.json_output if ctx else False


def x__should_use_json__mutmut_2(ctx: CLIContext | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is None:
        ctx = None
    return ctx.json_output if ctx else False


def x__should_use_json__mutmut_3(ctx: CLIContext | None = None) -> bool:
    """Determine if JSON output should be used."""
    if ctx is None:
        ctx = _get_context()
    return ctx.json_output if ctx else True


x__should_use_json__mutmut_mutants: ClassVar[MutantDict] = {
    "x__should_use_json__mutmut_1": x__should_use_json__mutmut_1,
    "x__should_use_json__mutmut_2": x__should_use_json__mutmut_2,
    "x__should_use_json__mutmut_3": x__should_use_json__mutmut_3,
}


def _should_use_json(*args, **kwargs):
    result = _mutmut_trampoline(
        x__should_use_json__mutmut_orig, x__should_use_json__mutmut_mutants, args, kwargs
    )
    return result


_should_use_json.__signature__ = _mutmut_signature(x__should_use_json__mutmut_orig)
x__should_use_json__mutmut_orig.__name__ = "x__should_use_json"


def x__should_use_color__mutmut_orig(ctx: CLIContext | None = None) -> bool:
    """Determine if color output should be used."""
    if ctx is None:
        ctx = _get_context()

    # Check if stdin is a TTY
    return sys.stdin.isatty()


def x__should_use_color__mutmut_1(ctx: CLIContext | None = None) -> bool:
    """Determine if color output should be used."""
    if ctx is not None:
        ctx = _get_context()

    # Check if stdin is a TTY
    return sys.stdin.isatty()


def x__should_use_color__mutmut_2(ctx: CLIContext | None = None) -> bool:
    """Determine if color output should be used."""
    if ctx is None:
        ctx = None

    # Check if stdin is a TTY
    return sys.stdin.isatty()


x__should_use_color__mutmut_mutants: ClassVar[MutantDict] = {
    "x__should_use_color__mutmut_1": x__should_use_color__mutmut_1,
    "x__should_use_color__mutmut_2": x__should_use_color__mutmut_2,
}


def _should_use_color(*args, **kwargs):
    result = _mutmut_trampoline(
        x__should_use_color__mutmut_orig, x__should_use_color__mutmut_mutants, args, kwargs
    )
    return result


_should_use_color.__signature__ = _mutmut_signature(x__should_use_color__mutmut_orig)
x__should_use_color__mutmut_orig.__name__ = "x__should_use_color"


def x__handle_json_input__mutmut_orig(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_1(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() or prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_2(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(None, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_3(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=None, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_4(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=None)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_5(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_6(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_7(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(
                    prompt,
                    err=True,
                )
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_8(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=False, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_9(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=True)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_10(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(None, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_11(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=None, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_12(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end=None)

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_13(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_14(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_15(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(
                    prompt,
                    file=sys.stderr,
                )

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_16(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="XXXX")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_17(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = None

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_18(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = None
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_19(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(None)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_20(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = None

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_21(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get(None):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_22(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("XXtypeXX"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_23(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("TYPE"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_24(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(None, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_25(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, None):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_26(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_27(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(
                TypeError,
            ):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_28(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = None

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_29(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(None)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_30(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get(None):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_31(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("XXjson_keyXX"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_32(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("JSON_KEY"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_33(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error(None, error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_34(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=None)
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_35(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error(error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_36(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error(
            "Failed to read JSON input",
        )
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_37(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("XXFailed to read JSON inputXX", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_38(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("failed to read json input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_39(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("FAILED TO READ JSON INPUT", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_40(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(None))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_41(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get(None):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_42(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("XXjson_keyXX"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_43(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("JSON_KEY"):
            return {json_key: None, "error": str(e)}
        return None


def x__handle_json_input__mutmut_44(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "XXerrorXX": str(e)}
        return None


def x__handle_json_input__mutmut_45(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "ERROR": str(e)}
        return None


def x__handle_json_input__mutmut_46(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
    """Handle input in JSON mode."""
    try:
        if sys.stdin.isatty() and prompt:
            # Interactive mode, still show prompt to stderr
            if _HAS_CLICK:
                click.echo(prompt, err=True, nl=False)
            else:
                print(prompt, file=sys.stderr, end="")

        line = sys.stdin.readline().strip()

        # Try to parse as JSON first
        try:
            data: Any = json_loads(line)
        except ValidationError:
            # Treat as plain string
            data = line

        # Apply type conversion if specified
        if type_func := kwargs.get("type"):
            with contextlib.suppress(TypeError, ValueError):
                data = type_func(data)

        if json_key := kwargs.get("json_key"):
            return {json_key: data}
        return data

    except Exception as e:
        log.error("Failed to read JSON input", error=str(e))
        if json_key := kwargs.get("json_key"):
            return {json_key: None, "error": str(None)}
        return None


x__handle_json_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_json_input__mutmut_1": x__handle_json_input__mutmut_1,
    "x__handle_json_input__mutmut_2": x__handle_json_input__mutmut_2,
    "x__handle_json_input__mutmut_3": x__handle_json_input__mutmut_3,
    "x__handle_json_input__mutmut_4": x__handle_json_input__mutmut_4,
    "x__handle_json_input__mutmut_5": x__handle_json_input__mutmut_5,
    "x__handle_json_input__mutmut_6": x__handle_json_input__mutmut_6,
    "x__handle_json_input__mutmut_7": x__handle_json_input__mutmut_7,
    "x__handle_json_input__mutmut_8": x__handle_json_input__mutmut_8,
    "x__handle_json_input__mutmut_9": x__handle_json_input__mutmut_9,
    "x__handle_json_input__mutmut_10": x__handle_json_input__mutmut_10,
    "x__handle_json_input__mutmut_11": x__handle_json_input__mutmut_11,
    "x__handle_json_input__mutmut_12": x__handle_json_input__mutmut_12,
    "x__handle_json_input__mutmut_13": x__handle_json_input__mutmut_13,
    "x__handle_json_input__mutmut_14": x__handle_json_input__mutmut_14,
    "x__handle_json_input__mutmut_15": x__handle_json_input__mutmut_15,
    "x__handle_json_input__mutmut_16": x__handle_json_input__mutmut_16,
    "x__handle_json_input__mutmut_17": x__handle_json_input__mutmut_17,
    "x__handle_json_input__mutmut_18": x__handle_json_input__mutmut_18,
    "x__handle_json_input__mutmut_19": x__handle_json_input__mutmut_19,
    "x__handle_json_input__mutmut_20": x__handle_json_input__mutmut_20,
    "x__handle_json_input__mutmut_21": x__handle_json_input__mutmut_21,
    "x__handle_json_input__mutmut_22": x__handle_json_input__mutmut_22,
    "x__handle_json_input__mutmut_23": x__handle_json_input__mutmut_23,
    "x__handle_json_input__mutmut_24": x__handle_json_input__mutmut_24,
    "x__handle_json_input__mutmut_25": x__handle_json_input__mutmut_25,
    "x__handle_json_input__mutmut_26": x__handle_json_input__mutmut_26,
    "x__handle_json_input__mutmut_27": x__handle_json_input__mutmut_27,
    "x__handle_json_input__mutmut_28": x__handle_json_input__mutmut_28,
    "x__handle_json_input__mutmut_29": x__handle_json_input__mutmut_29,
    "x__handle_json_input__mutmut_30": x__handle_json_input__mutmut_30,
    "x__handle_json_input__mutmut_31": x__handle_json_input__mutmut_31,
    "x__handle_json_input__mutmut_32": x__handle_json_input__mutmut_32,
    "x__handle_json_input__mutmut_33": x__handle_json_input__mutmut_33,
    "x__handle_json_input__mutmut_34": x__handle_json_input__mutmut_34,
    "x__handle_json_input__mutmut_35": x__handle_json_input__mutmut_35,
    "x__handle_json_input__mutmut_36": x__handle_json_input__mutmut_36,
    "x__handle_json_input__mutmut_37": x__handle_json_input__mutmut_37,
    "x__handle_json_input__mutmut_38": x__handle_json_input__mutmut_38,
    "x__handle_json_input__mutmut_39": x__handle_json_input__mutmut_39,
    "x__handle_json_input__mutmut_40": x__handle_json_input__mutmut_40,
    "x__handle_json_input__mutmut_41": x__handle_json_input__mutmut_41,
    "x__handle_json_input__mutmut_42": x__handle_json_input__mutmut_42,
    "x__handle_json_input__mutmut_43": x__handle_json_input__mutmut_43,
    "x__handle_json_input__mutmut_44": x__handle_json_input__mutmut_44,
    "x__handle_json_input__mutmut_45": x__handle_json_input__mutmut_45,
    "x__handle_json_input__mutmut_46": x__handle_json_input__mutmut_46,
}


def _handle_json_input(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_json_input__mutmut_orig, x__handle_json_input__mutmut_mutants, args, kwargs
    )
    return result


_handle_json_input.__signature__ = _mutmut_signature(x__handle_json_input__mutmut_orig)
x__handle_json_input__mutmut_orig.__name__ = "x__handle_json_input"


def x__build_click_prompt_kwargs__mutmut_orig(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_1(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = None

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_2(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "XXtypeXX" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_3(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "TYPE" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_4(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" not in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_5(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = None
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_6(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["XXtypeXX"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_7(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["TYPE"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_8(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["XXtypeXX"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_9(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["TYPE"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_10(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "XXdefaultXX" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_11(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "DEFAULT" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_12(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" not in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_13(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = None
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_14(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["XXdefaultXX"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_15(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["DEFAULT"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_16(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["XXdefaultXX"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_17(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["DEFAULT"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_18(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") and kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_19(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get(None) or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_20(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("XXpasswordXX") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_21(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("PASSWORD") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_22(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get(None):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_23(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("XXhide_inputXX"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_24(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("HIDE_INPUT"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_25(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = None
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_26(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["XXhide_inputXX"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_27(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["HIDE_INPUT"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_28(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = False
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_29(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "XXconfirmation_promptXX" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_30(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "CONFIRMATION_PROMPT" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_31(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" not in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_32(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = None
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_33(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["XXconfirmation_promptXX"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_34(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["CONFIRMATION_PROMPT"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_35(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["XXconfirmation_promptXX"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_36(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["CONFIRMATION_PROMPT"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_37(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "XXshow_defaultXX" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_38(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "SHOW_DEFAULT" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_39(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" not in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_40(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = None
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_41(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["XXshow_defaultXX"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_42(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["SHOW_DEFAULT"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_43(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["XXshow_defaultXX"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_44(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["SHOW_DEFAULT"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_45(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "XXvalue_procXX" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_46(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "VALUE_PROC" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_47(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" not in kwargs:
        prompt_kwargs["value_proc"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_48(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = None

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_49(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["XXvalue_procXX"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_50(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["VALUE_PROC"] = kwargs["value_proc"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_51(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["XXvalue_procXX"]

    return prompt_kwargs


def x__build_click_prompt_kwargs__mutmut_52(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for click.prompt from our kwargs."""
    prompt_kwargs = {}

    # Map our kwargs to click.prompt kwargs
    if "type" in kwargs:
        prompt_kwargs["type"] = kwargs["type"]
    if "default" in kwargs:
        prompt_kwargs["default"] = kwargs["default"]
    if kwargs.get("password") or kwargs.get("hide_input"):
        prompt_kwargs["hide_input"] = True
    if "confirmation_prompt" in kwargs:
        prompt_kwargs["confirmation_prompt"] = kwargs["confirmation_prompt"]
    if "show_default" in kwargs:
        prompt_kwargs["show_default"] = kwargs["show_default"]
    if "value_proc" in kwargs:
        prompt_kwargs["value_proc"] = kwargs["VALUE_PROC"]

    return prompt_kwargs


x__build_click_prompt_kwargs__mutmut_mutants: ClassVar[MutantDict] = {
    "x__build_click_prompt_kwargs__mutmut_1": x__build_click_prompt_kwargs__mutmut_1,
    "x__build_click_prompt_kwargs__mutmut_2": x__build_click_prompt_kwargs__mutmut_2,
    "x__build_click_prompt_kwargs__mutmut_3": x__build_click_prompt_kwargs__mutmut_3,
    "x__build_click_prompt_kwargs__mutmut_4": x__build_click_prompt_kwargs__mutmut_4,
    "x__build_click_prompt_kwargs__mutmut_5": x__build_click_prompt_kwargs__mutmut_5,
    "x__build_click_prompt_kwargs__mutmut_6": x__build_click_prompt_kwargs__mutmut_6,
    "x__build_click_prompt_kwargs__mutmut_7": x__build_click_prompt_kwargs__mutmut_7,
    "x__build_click_prompt_kwargs__mutmut_8": x__build_click_prompt_kwargs__mutmut_8,
    "x__build_click_prompt_kwargs__mutmut_9": x__build_click_prompt_kwargs__mutmut_9,
    "x__build_click_prompt_kwargs__mutmut_10": x__build_click_prompt_kwargs__mutmut_10,
    "x__build_click_prompt_kwargs__mutmut_11": x__build_click_prompt_kwargs__mutmut_11,
    "x__build_click_prompt_kwargs__mutmut_12": x__build_click_prompt_kwargs__mutmut_12,
    "x__build_click_prompt_kwargs__mutmut_13": x__build_click_prompt_kwargs__mutmut_13,
    "x__build_click_prompt_kwargs__mutmut_14": x__build_click_prompt_kwargs__mutmut_14,
    "x__build_click_prompt_kwargs__mutmut_15": x__build_click_prompt_kwargs__mutmut_15,
    "x__build_click_prompt_kwargs__mutmut_16": x__build_click_prompt_kwargs__mutmut_16,
    "x__build_click_prompt_kwargs__mutmut_17": x__build_click_prompt_kwargs__mutmut_17,
    "x__build_click_prompt_kwargs__mutmut_18": x__build_click_prompt_kwargs__mutmut_18,
    "x__build_click_prompt_kwargs__mutmut_19": x__build_click_prompt_kwargs__mutmut_19,
    "x__build_click_prompt_kwargs__mutmut_20": x__build_click_prompt_kwargs__mutmut_20,
    "x__build_click_prompt_kwargs__mutmut_21": x__build_click_prompt_kwargs__mutmut_21,
    "x__build_click_prompt_kwargs__mutmut_22": x__build_click_prompt_kwargs__mutmut_22,
    "x__build_click_prompt_kwargs__mutmut_23": x__build_click_prompt_kwargs__mutmut_23,
    "x__build_click_prompt_kwargs__mutmut_24": x__build_click_prompt_kwargs__mutmut_24,
    "x__build_click_prompt_kwargs__mutmut_25": x__build_click_prompt_kwargs__mutmut_25,
    "x__build_click_prompt_kwargs__mutmut_26": x__build_click_prompt_kwargs__mutmut_26,
    "x__build_click_prompt_kwargs__mutmut_27": x__build_click_prompt_kwargs__mutmut_27,
    "x__build_click_prompt_kwargs__mutmut_28": x__build_click_prompt_kwargs__mutmut_28,
    "x__build_click_prompt_kwargs__mutmut_29": x__build_click_prompt_kwargs__mutmut_29,
    "x__build_click_prompt_kwargs__mutmut_30": x__build_click_prompt_kwargs__mutmut_30,
    "x__build_click_prompt_kwargs__mutmut_31": x__build_click_prompt_kwargs__mutmut_31,
    "x__build_click_prompt_kwargs__mutmut_32": x__build_click_prompt_kwargs__mutmut_32,
    "x__build_click_prompt_kwargs__mutmut_33": x__build_click_prompt_kwargs__mutmut_33,
    "x__build_click_prompt_kwargs__mutmut_34": x__build_click_prompt_kwargs__mutmut_34,
    "x__build_click_prompt_kwargs__mutmut_35": x__build_click_prompt_kwargs__mutmut_35,
    "x__build_click_prompt_kwargs__mutmut_36": x__build_click_prompt_kwargs__mutmut_36,
    "x__build_click_prompt_kwargs__mutmut_37": x__build_click_prompt_kwargs__mutmut_37,
    "x__build_click_prompt_kwargs__mutmut_38": x__build_click_prompt_kwargs__mutmut_38,
    "x__build_click_prompt_kwargs__mutmut_39": x__build_click_prompt_kwargs__mutmut_39,
    "x__build_click_prompt_kwargs__mutmut_40": x__build_click_prompt_kwargs__mutmut_40,
    "x__build_click_prompt_kwargs__mutmut_41": x__build_click_prompt_kwargs__mutmut_41,
    "x__build_click_prompt_kwargs__mutmut_42": x__build_click_prompt_kwargs__mutmut_42,
    "x__build_click_prompt_kwargs__mutmut_43": x__build_click_prompt_kwargs__mutmut_43,
    "x__build_click_prompt_kwargs__mutmut_44": x__build_click_prompt_kwargs__mutmut_44,
    "x__build_click_prompt_kwargs__mutmut_45": x__build_click_prompt_kwargs__mutmut_45,
    "x__build_click_prompt_kwargs__mutmut_46": x__build_click_prompt_kwargs__mutmut_46,
    "x__build_click_prompt_kwargs__mutmut_47": x__build_click_prompt_kwargs__mutmut_47,
    "x__build_click_prompt_kwargs__mutmut_48": x__build_click_prompt_kwargs__mutmut_48,
    "x__build_click_prompt_kwargs__mutmut_49": x__build_click_prompt_kwargs__mutmut_49,
    "x__build_click_prompt_kwargs__mutmut_50": x__build_click_prompt_kwargs__mutmut_50,
    "x__build_click_prompt_kwargs__mutmut_51": x__build_click_prompt_kwargs__mutmut_51,
    "x__build_click_prompt_kwargs__mutmut_52": x__build_click_prompt_kwargs__mutmut_52,
}


def _build_click_prompt_kwargs(*args, **kwargs):
    result = _mutmut_trampoline(
        x__build_click_prompt_kwargs__mutmut_orig, x__build_click_prompt_kwargs__mutmut_mutants, args, kwargs
    )
    return result


_build_click_prompt_kwargs.__signature__ = _mutmut_signature(x__build_click_prompt_kwargs__mutmut_orig)
x__build_click_prompt_kwargs__mutmut_orig.__name__ = "x__build_click_prompt_kwargs"


def x__apply_prompt_styling__mutmut_orig(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_1(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK and not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_2(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_3(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_4(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(None):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_5(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = None
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_6(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get(None)
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_7(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("XXcolorXX")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_8(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("COLOR")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_9(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = None
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_10(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get(None, False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_11(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", None)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_12(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get(False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_13(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get(
        "bold",
    )
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_14(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("XXboldXX", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_15(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("BOLD", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_16(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", True)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_17(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color and bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_18(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(None, fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_19(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=None, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_20(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=None)
    return prompt


def x__apply_prompt_styling__mutmut_21(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(fg=color, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_22(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, bold=bold)
    return prompt


def x__apply_prompt_styling__mutmut_23(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(
            prompt,
            fg=color,
        )
    return prompt


x__apply_prompt_styling__mutmut_mutants: ClassVar[MutantDict] = {
    "x__apply_prompt_styling__mutmut_1": x__apply_prompt_styling__mutmut_1,
    "x__apply_prompt_styling__mutmut_2": x__apply_prompt_styling__mutmut_2,
    "x__apply_prompt_styling__mutmut_3": x__apply_prompt_styling__mutmut_3,
    "x__apply_prompt_styling__mutmut_4": x__apply_prompt_styling__mutmut_4,
    "x__apply_prompt_styling__mutmut_5": x__apply_prompt_styling__mutmut_5,
    "x__apply_prompt_styling__mutmut_6": x__apply_prompt_styling__mutmut_6,
    "x__apply_prompt_styling__mutmut_7": x__apply_prompt_styling__mutmut_7,
    "x__apply_prompt_styling__mutmut_8": x__apply_prompt_styling__mutmut_8,
    "x__apply_prompt_styling__mutmut_9": x__apply_prompt_styling__mutmut_9,
    "x__apply_prompt_styling__mutmut_10": x__apply_prompt_styling__mutmut_10,
    "x__apply_prompt_styling__mutmut_11": x__apply_prompt_styling__mutmut_11,
    "x__apply_prompt_styling__mutmut_12": x__apply_prompt_styling__mutmut_12,
    "x__apply_prompt_styling__mutmut_13": x__apply_prompt_styling__mutmut_13,
    "x__apply_prompt_styling__mutmut_14": x__apply_prompt_styling__mutmut_14,
    "x__apply_prompt_styling__mutmut_15": x__apply_prompt_styling__mutmut_15,
    "x__apply_prompt_styling__mutmut_16": x__apply_prompt_styling__mutmut_16,
    "x__apply_prompt_styling__mutmut_17": x__apply_prompt_styling__mutmut_17,
    "x__apply_prompt_styling__mutmut_18": x__apply_prompt_styling__mutmut_18,
    "x__apply_prompt_styling__mutmut_19": x__apply_prompt_styling__mutmut_19,
    "x__apply_prompt_styling__mutmut_20": x__apply_prompt_styling__mutmut_20,
    "x__apply_prompt_styling__mutmut_21": x__apply_prompt_styling__mutmut_21,
    "x__apply_prompt_styling__mutmut_22": x__apply_prompt_styling__mutmut_22,
    "x__apply_prompt_styling__mutmut_23": x__apply_prompt_styling__mutmut_23,
}


def _apply_prompt_styling(*args, **kwargs):
    result = _mutmut_trampoline(
        x__apply_prompt_styling__mutmut_orig, x__apply_prompt_styling__mutmut_mutants, args, kwargs
    )
    return result


_apply_prompt_styling.__signature__ = _mutmut_signature(x__apply_prompt_styling__mutmut_orig)
x__apply_prompt_styling__mutmut_orig.__name__ = "x__apply_prompt_styling"


def x__handle_click_input__mutmut_orig(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_1(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = None
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_2(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(None)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_3(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = None
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_4(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(None, kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_5(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, None, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_6(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, None)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_7(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_8(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_9(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(
        prompt,
        kwargs,
    )
    return click.prompt(styled_prompt, **prompt_kwargs)


def x__handle_click_input__mutmut_10(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(None, **prompt_kwargs)


def x__handle_click_input__mutmut_11(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(**prompt_kwargs)


def x__handle_click_input__mutmut_12(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(
        styled_prompt,
    )


x__handle_click_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_click_input__mutmut_1": x__handle_click_input__mutmut_1,
    "x__handle_click_input__mutmut_2": x__handle_click_input__mutmut_2,
    "x__handle_click_input__mutmut_3": x__handle_click_input__mutmut_3,
    "x__handle_click_input__mutmut_4": x__handle_click_input__mutmut_4,
    "x__handle_click_input__mutmut_5": x__handle_click_input__mutmut_5,
    "x__handle_click_input__mutmut_6": x__handle_click_input__mutmut_6,
    "x__handle_click_input__mutmut_7": x__handle_click_input__mutmut_7,
    "x__handle_click_input__mutmut_8": x__handle_click_input__mutmut_8,
    "x__handle_click_input__mutmut_9": x__handle_click_input__mutmut_9,
    "x__handle_click_input__mutmut_10": x__handle_click_input__mutmut_10,
    "x__handle_click_input__mutmut_11": x__handle_click_input__mutmut_11,
    "x__handle_click_input__mutmut_12": x__handle_click_input__mutmut_12,
}


def _handle_click_input(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_click_input__mutmut_orig, x__handle_click_input__mutmut_mutants, args, kwargs
    )
    return result


_handle_click_input.__signature__ = _mutmut_signature(x__handle_click_input__mutmut_orig)
x__handle_click_input__mutmut_orig.__name__ = "x__handle_click_input"


def x__build_fallback_prompt__mutmut_orig(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_1(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") or kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_2(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get(None) and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_3(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("XXdefaultXX") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_4(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("DEFAULT") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_5(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get(None, True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_6(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", None):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_7(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get(True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_8(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get(
        "show_default",
    ):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_9(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("XXshow_defaultXX", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_10(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("SHOW_DEFAULT", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_11(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", False):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_12(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['XXdefaultXX']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_13(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['DEFAULT']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_14(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt or not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_15(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_16(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(None):
        return f"{prompt}: "
    return prompt


def x__build_fallback_prompt__mutmut_17(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith("XX: XX"):
        return f"{prompt}: "
    return prompt


x__build_fallback_prompt__mutmut_mutants: ClassVar[MutantDict] = {
    "x__build_fallback_prompt__mutmut_1": x__build_fallback_prompt__mutmut_1,
    "x__build_fallback_prompt__mutmut_2": x__build_fallback_prompt__mutmut_2,
    "x__build_fallback_prompt__mutmut_3": x__build_fallback_prompt__mutmut_3,
    "x__build_fallback_prompt__mutmut_4": x__build_fallback_prompt__mutmut_4,
    "x__build_fallback_prompt__mutmut_5": x__build_fallback_prompt__mutmut_5,
    "x__build_fallback_prompt__mutmut_6": x__build_fallback_prompt__mutmut_6,
    "x__build_fallback_prompt__mutmut_7": x__build_fallback_prompt__mutmut_7,
    "x__build_fallback_prompt__mutmut_8": x__build_fallback_prompt__mutmut_8,
    "x__build_fallback_prompt__mutmut_9": x__build_fallback_prompt__mutmut_9,
    "x__build_fallback_prompt__mutmut_10": x__build_fallback_prompt__mutmut_10,
    "x__build_fallback_prompt__mutmut_11": x__build_fallback_prompt__mutmut_11,
    "x__build_fallback_prompt__mutmut_12": x__build_fallback_prompt__mutmut_12,
    "x__build_fallback_prompt__mutmut_13": x__build_fallback_prompt__mutmut_13,
    "x__build_fallback_prompt__mutmut_14": x__build_fallback_prompt__mutmut_14,
    "x__build_fallback_prompt__mutmut_15": x__build_fallback_prompt__mutmut_15,
    "x__build_fallback_prompt__mutmut_16": x__build_fallback_prompt__mutmut_16,
    "x__build_fallback_prompt__mutmut_17": x__build_fallback_prompt__mutmut_17,
}


def _build_fallback_prompt(*args, **kwargs):
    result = _mutmut_trampoline(
        x__build_fallback_prompt__mutmut_orig, x__build_fallback_prompt__mutmut_mutants, args, kwargs
    )
    return result


_build_fallback_prompt.__signature__ = _mutmut_signature(x__build_fallback_prompt__mutmut_orig)
x__build_fallback_prompt__mutmut_orig.__name__ = "x__build_fallback_prompt"


def x__get_fallback_input__mutmut_orig(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_1(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") and kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_2(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get(None) or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_3(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("XXpasswordXX") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_4(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("PASSWORD") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_5(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get(None):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_6(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("XXhide_inputXX"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_7(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("HIDE_INPUT"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_8(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(None)
    else:
        return input(display_prompt)


def x__get_fallback_input__mutmut_9(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(None)


x__get_fallback_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_fallback_input__mutmut_1": x__get_fallback_input__mutmut_1,
    "x__get_fallback_input__mutmut_2": x__get_fallback_input__mutmut_2,
    "x__get_fallback_input__mutmut_3": x__get_fallback_input__mutmut_3,
    "x__get_fallback_input__mutmut_4": x__get_fallback_input__mutmut_4,
    "x__get_fallback_input__mutmut_5": x__get_fallback_input__mutmut_5,
    "x__get_fallback_input__mutmut_6": x__get_fallback_input__mutmut_6,
    "x__get_fallback_input__mutmut_7": x__get_fallback_input__mutmut_7,
    "x__get_fallback_input__mutmut_8": x__get_fallback_input__mutmut_8,
    "x__get_fallback_input__mutmut_9": x__get_fallback_input__mutmut_9,
}


def _get_fallback_input(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_fallback_input__mutmut_orig, x__get_fallback_input__mutmut_mutants, args, kwargs
    )
    return result


_get_fallback_input.__signature__ = _mutmut_signature(x__get_fallback_input__mutmut_orig)
x__get_fallback_input__mutmut_orig.__name__ = "x__get_fallback_input"


def x__apply_type_conversion__mutmut_orig(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get("type"):
        try:
            return type_func(user_input)
        except (TypeError, ValueError):
            return user_input
    return user_input


def x__apply_type_conversion__mutmut_1(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get(None):
        try:
            return type_func(user_input)
        except (TypeError, ValueError):
            return user_input
    return user_input


def x__apply_type_conversion__mutmut_2(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get("XXtypeXX"):
        try:
            return type_func(user_input)
        except (TypeError, ValueError):
            return user_input
    return user_input


def x__apply_type_conversion__mutmut_3(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get("TYPE"):
        try:
            return type_func(user_input)
        except (TypeError, ValueError):
            return user_input
    return user_input


def x__apply_type_conversion__mutmut_4(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get("type"):
        try:
            return type_func(None)
        except (TypeError, ValueError):
            return user_input
    return user_input


x__apply_type_conversion__mutmut_mutants: ClassVar[MutantDict] = {
    "x__apply_type_conversion__mutmut_1": x__apply_type_conversion__mutmut_1,
    "x__apply_type_conversion__mutmut_2": x__apply_type_conversion__mutmut_2,
    "x__apply_type_conversion__mutmut_3": x__apply_type_conversion__mutmut_3,
    "x__apply_type_conversion__mutmut_4": x__apply_type_conversion__mutmut_4,
}


def _apply_type_conversion(*args, **kwargs):
    result = _mutmut_trampoline(
        x__apply_type_conversion__mutmut_orig, x__apply_type_conversion__mutmut_mutants, args, kwargs
    )
    return result


_apply_type_conversion.__signature__ = _mutmut_signature(x__apply_type_conversion__mutmut_orig)
x__apply_type_conversion__mutmut_orig.__name__ = "x__apply_type_conversion"


def x__handle_fallback_input__mutmut_orig(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_1(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = None
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_2(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(None, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_3(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, None)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_4(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_5(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(
        prompt,
    )
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_6(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = None

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_7(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(None, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_8(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, None)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_9(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_10(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(
        display_prompt,
    )

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_11(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input or "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_12(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_13(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "XXdefaultXX" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_14(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "DEFAULT" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_15(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" not in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_16(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = None

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_17(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(None)

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_18(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["XXdefaultXX"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_19(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["DEFAULT"])

    return _apply_type_conversion(user_input, kwargs)


def x__handle_fallback_input__mutmut_20(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(None, kwargs)


def x__handle_fallback_input__mutmut_21(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, None)


def x__handle_fallback_input__mutmut_22(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(kwargs)


def x__handle_fallback_input__mutmut_23(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(
        user_input,
    )


x__handle_fallback_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_fallback_input__mutmut_1": x__handle_fallback_input__mutmut_1,
    "x__handle_fallback_input__mutmut_2": x__handle_fallback_input__mutmut_2,
    "x__handle_fallback_input__mutmut_3": x__handle_fallback_input__mutmut_3,
    "x__handle_fallback_input__mutmut_4": x__handle_fallback_input__mutmut_4,
    "x__handle_fallback_input__mutmut_5": x__handle_fallback_input__mutmut_5,
    "x__handle_fallback_input__mutmut_6": x__handle_fallback_input__mutmut_6,
    "x__handle_fallback_input__mutmut_7": x__handle_fallback_input__mutmut_7,
    "x__handle_fallback_input__mutmut_8": x__handle_fallback_input__mutmut_8,
    "x__handle_fallback_input__mutmut_9": x__handle_fallback_input__mutmut_9,
    "x__handle_fallback_input__mutmut_10": x__handle_fallback_input__mutmut_10,
    "x__handle_fallback_input__mutmut_11": x__handle_fallback_input__mutmut_11,
    "x__handle_fallback_input__mutmut_12": x__handle_fallback_input__mutmut_12,
    "x__handle_fallback_input__mutmut_13": x__handle_fallback_input__mutmut_13,
    "x__handle_fallback_input__mutmut_14": x__handle_fallback_input__mutmut_14,
    "x__handle_fallback_input__mutmut_15": x__handle_fallback_input__mutmut_15,
    "x__handle_fallback_input__mutmut_16": x__handle_fallback_input__mutmut_16,
    "x__handle_fallback_input__mutmut_17": x__handle_fallback_input__mutmut_17,
    "x__handle_fallback_input__mutmut_18": x__handle_fallback_input__mutmut_18,
    "x__handle_fallback_input__mutmut_19": x__handle_fallback_input__mutmut_19,
    "x__handle_fallback_input__mutmut_20": x__handle_fallback_input__mutmut_20,
    "x__handle_fallback_input__mutmut_21": x__handle_fallback_input__mutmut_21,
    "x__handle_fallback_input__mutmut_22": x__handle_fallback_input__mutmut_22,
    "x__handle_fallback_input__mutmut_23": x__handle_fallback_input__mutmut_23,
}


def _handle_fallback_input(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_fallback_input__mutmut_orig, x__handle_fallback_input__mutmut_mutants, args, kwargs
    )
    return result


_handle_fallback_input.__signature__ = _mutmut_signature(x__handle_fallback_input__mutmut_orig)
x__handle_fallback_input__mutmut_orig.__name__ = "x__handle_fallback_input"


def x__handle_interactive_input__mutmut_orig(
    prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None
) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_1(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(None, kwargs, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_2(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, None, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_3(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, None)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_4(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(kwargs, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_5(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_6(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(
            prompt,
            kwargs,
        )
    else:
        return _handle_fallback_input(prompt, kwargs)


def x__handle_interactive_input__mutmut_7(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(None, kwargs)


def x__handle_interactive_input__mutmut_8(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(prompt, None)


def x__handle_interactive_input__mutmut_9(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(kwargs)


def x__handle_interactive_input__mutmut_10(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(
            prompt,
        )


x__handle_interactive_input__mutmut_mutants: ClassVar[MutantDict] = {
    "x__handle_interactive_input__mutmut_1": x__handle_interactive_input__mutmut_1,
    "x__handle_interactive_input__mutmut_2": x__handle_interactive_input__mutmut_2,
    "x__handle_interactive_input__mutmut_3": x__handle_interactive_input__mutmut_3,
    "x__handle_interactive_input__mutmut_4": x__handle_interactive_input__mutmut_4,
    "x__handle_interactive_input__mutmut_5": x__handle_interactive_input__mutmut_5,
    "x__handle_interactive_input__mutmut_6": x__handle_interactive_input__mutmut_6,
    "x__handle_interactive_input__mutmut_7": x__handle_interactive_input__mutmut_7,
    "x__handle_interactive_input__mutmut_8": x__handle_interactive_input__mutmut_8,
    "x__handle_interactive_input__mutmut_9": x__handle_interactive_input__mutmut_9,
    "x__handle_interactive_input__mutmut_10": x__handle_interactive_input__mutmut_10,
}


def _handle_interactive_input(*args, **kwargs):
    result = _mutmut_trampoline(
        x__handle_interactive_input__mutmut_orig, x__handle_interactive_input__mutmut_mutants, args, kwargs
    )
    return result


_handle_interactive_input.__signature__ = _mutmut_signature(x__handle_interactive_input__mutmut_orig)
x__handle_interactive_input__mutmut_orig.__name__ = "x__handle_interactive_input"


def x_pin__mutmut_orig(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_1(prompt: str = "XXXX", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_2(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = None

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_3(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") and _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_4(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get(None) or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_5(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("XXctxXX") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_6(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("CTX") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_7(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(None):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_8(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(None, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_9(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, None)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_10(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_11(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(
            prompt,
        )
    else:
        return _handle_interactive_input(prompt, kwargs, ctx)


def x_pin__mutmut_12(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(None, kwargs, ctx)


def x_pin__mutmut_13(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, None, ctx)


def x_pin__mutmut_14(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, kwargs, None)


def x_pin__mutmut_15(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(kwargs, ctx)


def x_pin__mutmut_16(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(prompt, ctx)


def x_pin__mutmut_17(prompt: str = "", **kwargs: Any) -> str | Any:
    """Input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Optional formatting arguments:
            type: Type to convert input to (int, float, bool, etc.)
            default: Default value if no input provided
            password: Hide input for passwords (default: False)
            confirmation_prompt: Ask for confirmation (for passwords)
            hide_input: Hide the input (same as password)
            show_default: Show default value in prompt
            value_proc: Callable to process the value
            json_key: Key for JSON output mode
            ctx: Override context
            color: Color for prompt (red, green, yellow, blue, cyan, magenta, white)
            bold: Bold prompt text

    Returns:
        User input as string or converted type

    Examples:
        name = pin("Enter name: ")
        age = pin("Age: ", type=int, default=0)
        password = pin("Password: ", password=True)

    In JSON mode, returns structured input data.

    """
    ctx = kwargs.get("ctx") or _get_context()

    if _should_use_json(ctx):
        return _handle_json_input(prompt, kwargs)
    else:
        return _handle_interactive_input(
            prompt,
            kwargs,
        )


x_pin__mutmut_mutants: ClassVar[MutantDict] = {
    "x_pin__mutmut_1": x_pin__mutmut_1,
    "x_pin__mutmut_2": x_pin__mutmut_2,
    "x_pin__mutmut_3": x_pin__mutmut_3,
    "x_pin__mutmut_4": x_pin__mutmut_4,
    "x_pin__mutmut_5": x_pin__mutmut_5,
    "x_pin__mutmut_6": x_pin__mutmut_6,
    "x_pin__mutmut_7": x_pin__mutmut_7,
    "x_pin__mutmut_8": x_pin__mutmut_8,
    "x_pin__mutmut_9": x_pin__mutmut_9,
    "x_pin__mutmut_10": x_pin__mutmut_10,
    "x_pin__mutmut_11": x_pin__mutmut_11,
    "x_pin__mutmut_12": x_pin__mutmut_12,
    "x_pin__mutmut_13": x_pin__mutmut_13,
    "x_pin__mutmut_14": x_pin__mutmut_14,
    "x_pin__mutmut_15": x_pin__mutmut_15,
    "x_pin__mutmut_16": x_pin__mutmut_16,
    "x_pin__mutmut_17": x_pin__mutmut_17,
}


def pin(*args, **kwargs):
    result = _mutmut_trampoline(x_pin__mutmut_orig, x_pin__mutmut_mutants, args, kwargs)
    return result


pin.__signature__ = _mutmut_signature(x_pin__mutmut_orig)
x_pin__mutmut_orig.__name__ = "x_pin"


def x_pin_stream__mutmut_orig() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_1() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = None

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_2() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(None):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_3() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = None
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_4() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = None
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_5() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(None)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_6() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(None) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_7() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_8() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(None)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_9() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug(None)
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_10() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("XX📥 Starting input streamXX")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_11() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_12() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 STARTING INPUT STREAM")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_13() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = None
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_14() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 1
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_15() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = None
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_16() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip(None)
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_17() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.lstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_18() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("XX\n\rXX")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_19() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count = 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_20() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count -= 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_21() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 2
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_22() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace(None, line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_23() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=None, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_24() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=None)
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_25() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace(line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_26() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_27() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace(
                    "📥 Stream line",
                    line_num=line_count,
                )
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_28() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("XX📥 Stream lineXX", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_29() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_30() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 STREAM LINE", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=line_count)


def x_pin_stream__mutmut_31() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug(None, lines=line_count)


def x_pin_stream__mutmut_32() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 Input stream ended", lines=None)


def x_pin_stream__mutmut_33() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug(lines=line_count)


def x_pin_stream__mutmut_34() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug(
                "📥 Input stream ended",
            )


def x_pin_stream__mutmut_35() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("XX📥 Input stream endedXX", lines=line_count)


def x_pin_stream__mutmut_36() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 input stream ended", lines=line_count)


def x_pin_stream__mutmut_37() -> Iterator[str]:
    """Stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        for line in pin_stream():
            process(line)

    Note: This blocks on each line. For non-blocking, use apin_stream().

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, try to read as JSON first
        stdin_content = sys.stdin.read()
        try:
            # Try to parse as JSON array/object
            data = json_loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json_dumps(item) if not isinstance(item, str) else item
            else:
                yield json_dumps(data)
        except ValidationError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        log.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                log.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            log.debug("📥 INPUT STREAM ENDED", lines=line_count)


x_pin_stream__mutmut_mutants: ClassVar[MutantDict] = {
    "x_pin_stream__mutmut_1": x_pin_stream__mutmut_1,
    "x_pin_stream__mutmut_2": x_pin_stream__mutmut_2,
    "x_pin_stream__mutmut_3": x_pin_stream__mutmut_3,
    "x_pin_stream__mutmut_4": x_pin_stream__mutmut_4,
    "x_pin_stream__mutmut_5": x_pin_stream__mutmut_5,
    "x_pin_stream__mutmut_6": x_pin_stream__mutmut_6,
    "x_pin_stream__mutmut_7": x_pin_stream__mutmut_7,
    "x_pin_stream__mutmut_8": x_pin_stream__mutmut_8,
    "x_pin_stream__mutmut_9": x_pin_stream__mutmut_9,
    "x_pin_stream__mutmut_10": x_pin_stream__mutmut_10,
    "x_pin_stream__mutmut_11": x_pin_stream__mutmut_11,
    "x_pin_stream__mutmut_12": x_pin_stream__mutmut_12,
    "x_pin_stream__mutmut_13": x_pin_stream__mutmut_13,
    "x_pin_stream__mutmut_14": x_pin_stream__mutmut_14,
    "x_pin_stream__mutmut_15": x_pin_stream__mutmut_15,
    "x_pin_stream__mutmut_16": x_pin_stream__mutmut_16,
    "x_pin_stream__mutmut_17": x_pin_stream__mutmut_17,
    "x_pin_stream__mutmut_18": x_pin_stream__mutmut_18,
    "x_pin_stream__mutmut_19": x_pin_stream__mutmut_19,
    "x_pin_stream__mutmut_20": x_pin_stream__mutmut_20,
    "x_pin_stream__mutmut_21": x_pin_stream__mutmut_21,
    "x_pin_stream__mutmut_22": x_pin_stream__mutmut_22,
    "x_pin_stream__mutmut_23": x_pin_stream__mutmut_23,
    "x_pin_stream__mutmut_24": x_pin_stream__mutmut_24,
    "x_pin_stream__mutmut_25": x_pin_stream__mutmut_25,
    "x_pin_stream__mutmut_26": x_pin_stream__mutmut_26,
    "x_pin_stream__mutmut_27": x_pin_stream__mutmut_27,
    "x_pin_stream__mutmut_28": x_pin_stream__mutmut_28,
    "x_pin_stream__mutmut_29": x_pin_stream__mutmut_29,
    "x_pin_stream__mutmut_30": x_pin_stream__mutmut_30,
    "x_pin_stream__mutmut_31": x_pin_stream__mutmut_31,
    "x_pin_stream__mutmut_32": x_pin_stream__mutmut_32,
    "x_pin_stream__mutmut_33": x_pin_stream__mutmut_33,
    "x_pin_stream__mutmut_34": x_pin_stream__mutmut_34,
    "x_pin_stream__mutmut_35": x_pin_stream__mutmut_35,
    "x_pin_stream__mutmut_36": x_pin_stream__mutmut_36,
    "x_pin_stream__mutmut_37": x_pin_stream__mutmut_37,
}


def pin_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_pin_stream__mutmut_orig, x_pin_stream__mutmut_mutants, args, kwargs)
    return result


pin_stream.__signature__ = _mutmut_signature(x_pin_stream__mutmut_orig)
x_pin_stream__mutmut_orig.__name__ = "x_pin_stream"


async def x_apin__mutmut_orig(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_1(prompt: str = "XXXX", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_2(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = None
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_3(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = None
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_4(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(None, prompt, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_5(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, None, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_6(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(prompt, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_7(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, **kwargs)
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_8(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(
        pin,
        prompt,
    )
    return await loop.run_in_executor(None, func)


async def x_apin__mutmut_9(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(None, None)


async def x_apin__mutmut_10(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(func)


async def x_apin__mutmut_11(prompt: str = "", **kwargs: Any) -> str | Any:
    """Async input from stdin with optional prompt.

    Args:
        prompt: Prompt to display before input
        **kwargs: Same as pin()

    Returns:
        User input as string or converted type

    Examples:
        name = await apin("Enter name: ")
        age = await apin("Age: ", type=int)

    Note: This runs the blocking input in a thread pool to avoid blocking the event loop.

    """
    import functools

    loop = asyncio.get_event_loop()
    func = functools.partial(pin, prompt, **kwargs)
    return await loop.run_in_executor(
        None,
    )


x_apin__mutmut_mutants: ClassVar[MutantDict] = {
    "x_apin__mutmut_1": x_apin__mutmut_1,
    "x_apin__mutmut_2": x_apin__mutmut_2,
    "x_apin__mutmut_3": x_apin__mutmut_3,
    "x_apin__mutmut_4": x_apin__mutmut_4,
    "x_apin__mutmut_5": x_apin__mutmut_5,
    "x_apin__mutmut_6": x_apin__mutmut_6,
    "x_apin__mutmut_7": x_apin__mutmut_7,
    "x_apin__mutmut_8": x_apin__mutmut_8,
    "x_apin__mutmut_9": x_apin__mutmut_9,
    "x_apin__mutmut_10": x_apin__mutmut_10,
    "x_apin__mutmut_11": x_apin__mutmut_11,
}


def apin(*args, **kwargs):
    result = _mutmut_trampoline(x_apin__mutmut_orig, x_apin__mutmut_mutants, args, kwargs)
    return result


apin.__signature__ = _mutmut_signature(x_apin__mutmut_orig)
x_apin__mutmut_orig.__name__ = "x_apin"


async def x_apin_stream__mutmut_orig() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_1() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = None

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_2() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(None):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_3() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = None

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_4() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = None
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_5() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = None
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_6() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(None)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_7() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(None) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_8() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_9() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(None)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_10() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip(None) for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_11() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.lstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_12() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("XX\n\rXX") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_13() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = None
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_14() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, None)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_15() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_16() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(
            None,
        )
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_17() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug(None)
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_18() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("XX📥 Starting async input streamXX")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_19() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_20() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 STARTING ASYNC INPUT STREAM")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_21() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = None

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_22() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 1

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_23() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = None
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_24() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = None
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_25() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = None

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_26() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(None)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_27() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(None, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_28() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, None)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_29() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_30() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(
            lambda: protocol,
        )

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_31() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: None, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_32() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while False:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_33() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = None
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_34() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_35() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        return

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_36() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = None
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_37() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip(None)
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_38() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").lstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_39() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode(None).rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_40() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("XXutf-8XX").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_41() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("UTF-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_42() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("XX\n\rXX")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_43() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count = 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_44() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count -= 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_45() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 2
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_46() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace(None, line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_47() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=None, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_48() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=None)
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_49() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace(line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_50() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_51() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace(
                        "📥 Async stream line",
                        line_num=line_count,
                    )
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_52() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("XX📥 Async stream lineXX", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_53() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_54() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 ASYNC STREAM LINE", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_55() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug(None, lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_56() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=None)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_57() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug(lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_58() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug(
                        "📥 Async stream cancelled",
                    )
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_59() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("XX📥 Async stream cancelledXX", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_60() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_61() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 ASYNC STREAM CANCELLED", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_62() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    return
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_63() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error(None, error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_64() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=None, lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_65() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=None)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_66() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error(error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_67() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_68() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error(
                        "📥 Async stream error",
                        error=str(e),
                    )
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_69() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("XX📥 Async stream errorXX", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_70() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_71() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 ASYNC STREAM ERROR", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_72() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(None), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_73() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    return
        finally:
            log.debug("📥 Async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_74() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug(None, lines=line_count)


async def x_apin_stream__mutmut_75() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 Async input stream ended", lines=None)


async def x_apin_stream__mutmut_76() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug(lines=line_count)


async def x_apin_stream__mutmut_77() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug(
                "📥 Async input stream ended",
            )


async def x_apin_stream__mutmut_78() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("XX📥 Async input stream endedXX", lines=line_count)


async def x_apin_stream__mutmut_79() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 async input stream ended", lines=line_count)


async def x_apin_stream__mutmut_80() -> AsyncIterator[str]:
    """Async stream input line by line from stdin.

    Yields:
        Lines from stdin (without trailing newline)

    Examples:
        async for line in apin_stream():
            await process(line)

    This provides non-blocking line-by-line input streaming.

    """
    ctx = _get_context()

    if _should_use_json(ctx):
        # In JSON mode, read all input and yield parsed lines
        loop = asyncio.get_event_loop()

        def read_json() -> list[str]:
            try:
                stdin_content = sys.stdin.read()
                data = json_loads(stdin_content)
                if isinstance(data, list):
                    return [json_dumps(item) if not isinstance(item, str) else item for item in data]
                return [json_dumps(data)]
            except ValidationError:
                # Fall back to line-by-line reading - content already read
                return [line.rstrip("\n\r") for line in stdin_content.splitlines() if line]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        log.debug("📥 Starting async input stream")
        line_count = 0

        # Create async reader for stdin
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)

        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        try:
            while True:
                try:
                    line_bytes = await reader.readline()
                    if not line_bytes:
                        break

                    line = line_bytes.decode("utf-8").rstrip("\n\r")
                    line_count += 1
                    log.trace("📥 Async stream line", line_num=line_count, length=len(line))
                    yield line

                except asyncio.CancelledError:
                    log.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    log.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            log.debug("📥 ASYNC INPUT STREAM ENDED", lines=line_count)


x_apin_stream__mutmut_mutants: ClassVar[MutantDict] = {
    "x_apin_stream__mutmut_1": x_apin_stream__mutmut_1,
    "x_apin_stream__mutmut_2": x_apin_stream__mutmut_2,
    "x_apin_stream__mutmut_3": x_apin_stream__mutmut_3,
    "x_apin_stream__mutmut_4": x_apin_stream__mutmut_4,
    "x_apin_stream__mutmut_5": x_apin_stream__mutmut_5,
    "x_apin_stream__mutmut_6": x_apin_stream__mutmut_6,
    "x_apin_stream__mutmut_7": x_apin_stream__mutmut_7,
    "x_apin_stream__mutmut_8": x_apin_stream__mutmut_8,
    "x_apin_stream__mutmut_9": x_apin_stream__mutmut_9,
    "x_apin_stream__mutmut_10": x_apin_stream__mutmut_10,
    "x_apin_stream__mutmut_11": x_apin_stream__mutmut_11,
    "x_apin_stream__mutmut_12": x_apin_stream__mutmut_12,
    "x_apin_stream__mutmut_13": x_apin_stream__mutmut_13,
    "x_apin_stream__mutmut_14": x_apin_stream__mutmut_14,
    "x_apin_stream__mutmut_15": x_apin_stream__mutmut_15,
    "x_apin_stream__mutmut_16": x_apin_stream__mutmut_16,
    "x_apin_stream__mutmut_17": x_apin_stream__mutmut_17,
    "x_apin_stream__mutmut_18": x_apin_stream__mutmut_18,
    "x_apin_stream__mutmut_19": x_apin_stream__mutmut_19,
    "x_apin_stream__mutmut_20": x_apin_stream__mutmut_20,
    "x_apin_stream__mutmut_21": x_apin_stream__mutmut_21,
    "x_apin_stream__mutmut_22": x_apin_stream__mutmut_22,
    "x_apin_stream__mutmut_23": x_apin_stream__mutmut_23,
    "x_apin_stream__mutmut_24": x_apin_stream__mutmut_24,
    "x_apin_stream__mutmut_25": x_apin_stream__mutmut_25,
    "x_apin_stream__mutmut_26": x_apin_stream__mutmut_26,
    "x_apin_stream__mutmut_27": x_apin_stream__mutmut_27,
    "x_apin_stream__mutmut_28": x_apin_stream__mutmut_28,
    "x_apin_stream__mutmut_29": x_apin_stream__mutmut_29,
    "x_apin_stream__mutmut_30": x_apin_stream__mutmut_30,
    "x_apin_stream__mutmut_31": x_apin_stream__mutmut_31,
    "x_apin_stream__mutmut_32": x_apin_stream__mutmut_32,
    "x_apin_stream__mutmut_33": x_apin_stream__mutmut_33,
    "x_apin_stream__mutmut_34": x_apin_stream__mutmut_34,
    "x_apin_stream__mutmut_35": x_apin_stream__mutmut_35,
    "x_apin_stream__mutmut_36": x_apin_stream__mutmut_36,
    "x_apin_stream__mutmut_37": x_apin_stream__mutmut_37,
    "x_apin_stream__mutmut_38": x_apin_stream__mutmut_38,
    "x_apin_stream__mutmut_39": x_apin_stream__mutmut_39,
    "x_apin_stream__mutmut_40": x_apin_stream__mutmut_40,
    "x_apin_stream__mutmut_41": x_apin_stream__mutmut_41,
    "x_apin_stream__mutmut_42": x_apin_stream__mutmut_42,
    "x_apin_stream__mutmut_43": x_apin_stream__mutmut_43,
    "x_apin_stream__mutmut_44": x_apin_stream__mutmut_44,
    "x_apin_stream__mutmut_45": x_apin_stream__mutmut_45,
    "x_apin_stream__mutmut_46": x_apin_stream__mutmut_46,
    "x_apin_stream__mutmut_47": x_apin_stream__mutmut_47,
    "x_apin_stream__mutmut_48": x_apin_stream__mutmut_48,
    "x_apin_stream__mutmut_49": x_apin_stream__mutmut_49,
    "x_apin_stream__mutmut_50": x_apin_stream__mutmut_50,
    "x_apin_stream__mutmut_51": x_apin_stream__mutmut_51,
    "x_apin_stream__mutmut_52": x_apin_stream__mutmut_52,
    "x_apin_stream__mutmut_53": x_apin_stream__mutmut_53,
    "x_apin_stream__mutmut_54": x_apin_stream__mutmut_54,
    "x_apin_stream__mutmut_55": x_apin_stream__mutmut_55,
    "x_apin_stream__mutmut_56": x_apin_stream__mutmut_56,
    "x_apin_stream__mutmut_57": x_apin_stream__mutmut_57,
    "x_apin_stream__mutmut_58": x_apin_stream__mutmut_58,
    "x_apin_stream__mutmut_59": x_apin_stream__mutmut_59,
    "x_apin_stream__mutmut_60": x_apin_stream__mutmut_60,
    "x_apin_stream__mutmut_61": x_apin_stream__mutmut_61,
    "x_apin_stream__mutmut_62": x_apin_stream__mutmut_62,
    "x_apin_stream__mutmut_63": x_apin_stream__mutmut_63,
    "x_apin_stream__mutmut_64": x_apin_stream__mutmut_64,
    "x_apin_stream__mutmut_65": x_apin_stream__mutmut_65,
    "x_apin_stream__mutmut_66": x_apin_stream__mutmut_66,
    "x_apin_stream__mutmut_67": x_apin_stream__mutmut_67,
    "x_apin_stream__mutmut_68": x_apin_stream__mutmut_68,
    "x_apin_stream__mutmut_69": x_apin_stream__mutmut_69,
    "x_apin_stream__mutmut_70": x_apin_stream__mutmut_70,
    "x_apin_stream__mutmut_71": x_apin_stream__mutmut_71,
    "x_apin_stream__mutmut_72": x_apin_stream__mutmut_72,
    "x_apin_stream__mutmut_73": x_apin_stream__mutmut_73,
    "x_apin_stream__mutmut_74": x_apin_stream__mutmut_74,
    "x_apin_stream__mutmut_75": x_apin_stream__mutmut_75,
    "x_apin_stream__mutmut_76": x_apin_stream__mutmut_76,
    "x_apin_stream__mutmut_77": x_apin_stream__mutmut_77,
    "x_apin_stream__mutmut_78": x_apin_stream__mutmut_78,
    "x_apin_stream__mutmut_79": x_apin_stream__mutmut_79,
    "x_apin_stream__mutmut_80": x_apin_stream__mutmut_80,
}


def apin_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_apin_stream__mutmut_orig, x_apin_stream__mutmut_mutants, args, kwargs)
    return result


apin_stream.__signature__ = _mutmut_signature(x_apin_stream__mutmut_orig)
x_apin_stream__mutmut_orig.__name__ = "x_apin_stream"


def x_pin_lines__mutmut_orig(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_1(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = None
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_2(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(None):
        lines.append(line)
        if count is not None and i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_3(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(None)
        if count is not None and i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_4(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None or i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_5(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is None and i + 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_6(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i - 1 >= count:
            break
    return lines


def x_pin_lines__mutmut_7(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i + 2 >= count:
            break
    return lines


def x_pin_lines__mutmut_8(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i + 1 > count:
            break
    return lines


def x_pin_lines__mutmut_9(count: int | None = None) -> list[str]:
    """Read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = pin_lines(3)  # Read exactly 3 lines
        all_lines = pin_lines()  # Read until EOF

    """
    lines = []
    for i, line in enumerate(pin_stream()):
        lines.append(line)
        if count is not None and i + 1 >= count:
            return
    return lines


x_pin_lines__mutmut_mutants: ClassVar[MutantDict] = {
    "x_pin_lines__mutmut_1": x_pin_lines__mutmut_1,
    "x_pin_lines__mutmut_2": x_pin_lines__mutmut_2,
    "x_pin_lines__mutmut_3": x_pin_lines__mutmut_3,
    "x_pin_lines__mutmut_4": x_pin_lines__mutmut_4,
    "x_pin_lines__mutmut_5": x_pin_lines__mutmut_5,
    "x_pin_lines__mutmut_6": x_pin_lines__mutmut_6,
    "x_pin_lines__mutmut_7": x_pin_lines__mutmut_7,
    "x_pin_lines__mutmut_8": x_pin_lines__mutmut_8,
    "x_pin_lines__mutmut_9": x_pin_lines__mutmut_9,
}


def pin_lines(*args, **kwargs):
    result = _mutmut_trampoline(x_pin_lines__mutmut_orig, x_pin_lines__mutmut_mutants, args, kwargs)
    return result


pin_lines.__signature__ = _mutmut_signature(x_pin_lines__mutmut_orig)
x_pin_lines__mutmut_orig.__name__ = "x_pin_lines"


async def x_apin_lines__mutmut_orig(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_1(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = None
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_2(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = None
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_3(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 1
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_4(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(None)
        i += 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_5(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i = 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_6(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i -= 1
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_7(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 2
        if count is not None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_8(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None or i >= count:
            break
    return lines


async def x_apin_lines__mutmut_9(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is None and i >= count:
            break
    return lines


async def x_apin_lines__mutmut_10(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i > count:
            break
    return lines


async def x_apin_lines__mutmut_11(count: int | None = None) -> list[str]:
    """Async read multiple lines from stdin.

    Args:
        count: Number of lines to read (None for all until EOF)

    Returns:
        List of input lines

    Examples:
        lines = await apin_lines(3)  # Read exactly 3 lines
        all_lines = await apin_lines()  # Read until EOF

    """
    lines = []
    i = 0
    async for line in apin_stream():
        lines.append(line)
        i += 1
        if count is not None and i >= count:
            return
    return lines


x_apin_lines__mutmut_mutants: ClassVar[MutantDict] = {
    "x_apin_lines__mutmut_1": x_apin_lines__mutmut_1,
    "x_apin_lines__mutmut_2": x_apin_lines__mutmut_2,
    "x_apin_lines__mutmut_3": x_apin_lines__mutmut_3,
    "x_apin_lines__mutmut_4": x_apin_lines__mutmut_4,
    "x_apin_lines__mutmut_5": x_apin_lines__mutmut_5,
    "x_apin_lines__mutmut_6": x_apin_lines__mutmut_6,
    "x_apin_lines__mutmut_7": x_apin_lines__mutmut_7,
    "x_apin_lines__mutmut_8": x_apin_lines__mutmut_8,
    "x_apin_lines__mutmut_9": x_apin_lines__mutmut_9,
    "x_apin_lines__mutmut_10": x_apin_lines__mutmut_10,
    "x_apin_lines__mutmut_11": x_apin_lines__mutmut_11,
}


def apin_lines(*args, **kwargs):
    result = _mutmut_trampoline(x_apin_lines__mutmut_orig, x_apin_lines__mutmut_mutants, args, kwargs)
    return result


apin_lines.__signature__ = _mutmut_signature(x_apin_lines__mutmut_orig)
x_apin_lines__mutmut_orig.__name__ = "x_apin_lines"


# <3 🧱🤝🖥️🪄
