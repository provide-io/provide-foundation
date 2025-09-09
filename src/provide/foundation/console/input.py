"""
Core console input functions for standardized CLI input.

Provides pin() and async variants for consistent input handling with support
for JSON mode, streaming, and proper integration with the foundation's patterns.
"""

import asyncio
from collections.abc import AsyncIterator, Iterator
import json
import sys
from typing import Any, TypeVar

try:
    import click

    _HAS_CLICK = True
except ImportError:
    click = None
    _HAS_CLICK = False

from provide.foundation.context import CLIContext
from provide.foundation.logger import get_logger

plog = get_logger(__name__)

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


def pin(prompt: str = "", **kwargs: Any) -> str | Any:
    """
    Input from stdin with optional prompt.

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
        # JSON mode - read from stdin and parse
        try:
            if sys.stdin.isatty():
                # Interactive mode, still show prompt to stderr
                if prompt:
                    if _HAS_CLICK:
                        click.echo(prompt, err=True, nl=False)
                    else:
                        print(prompt, file=sys.stderr, end="")

            line = sys.stdin.readline().strip()

            # Try to parse as JSON first
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Treat as plain string
                data = line

            # Apply type conversion if specified
            if type_func := kwargs.get("type"):
                try:
                    data = type_func(data)
                except (TypeError, ValueError):
                    pass

            if json_key := kwargs.get("json_key"):
                return {json_key: data}
            return data

        except Exception as e:
            plog.error("Failed to read JSON input", error=str(e))
            if json_key := kwargs.get("json_key"):
                return {json_key: None, "error": str(e)}
            return None
    else:
        # Regular interactive mode - use click.prompt
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

        if _HAS_CLICK:
            # Apply color/formatting to prompt if requested and supported
            styled_prompt = prompt
            if _should_use_color(ctx):
                color = kwargs.get("color")
                bold = kwargs.get("bold", False)
                if color or bold:
                    styled_prompt = click.style(prompt, fg=color, bold=bold)

            return click.prompt(styled_prompt, **prompt_kwargs)
        else:
            # Fallback to standard Python input
            display_prompt = prompt
            if kwargs.get("default") and kwargs.get("show_default", True):
                display_prompt = f"{prompt} [{kwargs['default']}]: "
            elif prompt and not prompt.endswith(": "):
                display_prompt = f"{prompt}: "

            if kwargs.get("password") or kwargs.get("hide_input"):
                import getpass

                user_input = getpass.getpass(display_prompt)
            else:
                user_input = input(display_prompt)

            # Handle default value
            if not user_input and "default" in kwargs:
                user_input = str(kwargs["default"])

            # Type conversion
            if type_func := kwargs.get("type"):
                try:
                    return type_func(user_input)
                except (TypeError, ValueError):
                    return user_input

            return user_input


def pin_stream() -> Iterator[str]:
    """
    Stream input line by line from stdin.

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
            data = json.loads(stdin_content)
            if isinstance(data, list):
                for item in data:
                    yield json.dumps(item) if not isinstance(item, str) else item
            else:
                yield json.dumps(data)
        except json.JSONDecodeError:
            # Fall back to line-by-line reading
            for line in stdin_content.splitlines():
                if line:  # Skip empty lines
                    yield line
    else:
        # Regular mode - yield lines as they come
        plog.debug("📥 Starting input stream")
        line_count = 0
        try:
            for line in sys.stdin:
                line = line.rstrip("\n\r")
                line_count += 1
                plog.trace("📥 Stream line", line_num=line_count, length=len(line))
                yield line
        finally:
            plog.debug("📥 Input stream ended", lines=line_count)


async def apin(prompt: str = "", **kwargs: Any) -> str | Any:
    """
    Async input from stdin with optional prompt.

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
    """
    Async stream input line by line from stdin.

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

        def read_json():
            try:
                data = json.load(sys.stdin)
                if isinstance(data, list):
                    return [
                        json.dumps(item) if not isinstance(item, str) else item
                        for item in data
                    ]
                else:
                    return [json.dumps(data)]
            except json.JSONDecodeError:
                # Fall back to line-by-line reading
                return [line.rstrip("\n\r") for line in sys.stdin]

        lines = await loop.run_in_executor(None, read_json)
        for line in lines:
            yield line
    else:
        # Regular mode - async line streaming
        plog.debug("📥 Starting async input stream")
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
                    plog.trace(
                        "📥 Async stream line", line_num=line_count, length=len(line)
                    )
                    yield line

                except asyncio.CancelledError:
                    plog.debug("📥 Async stream cancelled", lines=line_count)
                    break
                except Exception as e:
                    plog.error("📥 Async stream error", error=str(e), lines=line_count)
                    break
        finally:
            plog.debug("📥 Async input stream ended", lines=line_count)


def pin_lines(count: int | None = None) -> list[str]:
    """
    Read multiple lines from stdin.

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
    """
    Async read multiple lines from stdin.

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
