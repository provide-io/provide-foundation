#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def _should_use_color(ctx: CLIContext | None = None) -> bool:
    """Determine if color output should be used."""
    if ctx is None:
        ctx = _get_context()

    # Check if stdin is a TTY
    return sys.stdin.isatty()


def _handle_json_input(prompt: str, kwargs: dict[str, Any]) -> str | dict[str, Any] | None:
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


def _build_click_prompt_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
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


def _apply_prompt_styling(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> str:
    """Apply color/formatting to prompt if requested and supported."""
    if not _HAS_CLICK or not _should_use_color(ctx):
        return prompt

    color = kwargs.get("color")
    bold = kwargs.get("bold", False)
    if color or bold:
        return click.style(prompt, fg=color, bold=bold)
    return prompt


def _handle_click_input(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input using click.prompt."""
    prompt_kwargs = _build_click_prompt_kwargs(kwargs)
    styled_prompt = _apply_prompt_styling(prompt, kwargs, ctx)
    return click.prompt(styled_prompt, **prompt_kwargs)


def _build_fallback_prompt(prompt: str, kwargs: dict[str, Any]) -> str:
    """Build prompt for fallback input when click is not available."""
    if kwargs.get("default") and kwargs.get("show_default", True):
        return f"{prompt} [{kwargs['default']}]: "
    elif prompt and not prompt.endswith(": "):
        return f"{prompt}: "
    return prompt


def _get_fallback_input(display_prompt: str, kwargs: dict[str, Any]) -> str:
    """Get input using fallback methods when click is not available."""
    if kwargs.get("password") or kwargs.get("hide_input"):
        import getpass

        return getpass.getpass(display_prompt)
    else:
        return input(display_prompt)


def _apply_type_conversion(user_input: str, kwargs: dict[str, Any]) -> Any:
    """Apply type conversion to user input."""
    if type_func := kwargs.get("type"):
        try:
            return type_func(user_input)
        except (TypeError, ValueError):
            return user_input
    return user_input


def _handle_fallback_input(prompt: str, kwargs: dict[str, Any]) -> Any:
    """Handle input using fallback methods."""
    display_prompt = _build_fallback_prompt(prompt, kwargs)
    user_input = _get_fallback_input(display_prompt, kwargs)

    # Handle default value
    if not user_input and "default" in kwargs:
        user_input = str(kwargs["default"])

    return _apply_type_conversion(user_input, kwargs)


def _handle_interactive_input(prompt: str, kwargs: dict[str, Any], ctx: CLIContext | None) -> Any:
    """Handle input in interactive mode."""
    if _HAS_CLICK:
        return _handle_click_input(prompt, kwargs, ctx)
    else:
        return _handle_fallback_input(prompt, kwargs)


def pin(prompt: str = "", **kwargs: Any) -> str | Any:
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


def pin_stream() -> Iterator[str]:
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


async def apin(prompt: str = "", **kwargs: Any) -> str | Any:
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


async def apin_stream() -> AsyncIterator[str]:
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


def pin_lines(count: int | None = None) -> list[str]:
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


async def apin_lines(count: int | None = None) -> list[str]:
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


# 🧱🏗️🔚
