from __future__ import annotations

#
# console.py
#
import sys
from typing import TextIO

from provide.foundation.streams.config import get_stream_config
from provide.foundation.streams.core import get_log_stream

"""Console stream utilities for Foundation.
Handles console-specific stream operations and formatting.
"""


def get_console_stream() -> TextIO:
    """Get the appropriate console stream for output."""
    return get_log_stream()


def is_tty() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "isatty") and stream.isatty()


def supports_color() -> bool:
    """Check if the current stream supports color output."""
    config = get_stream_config()

    if config.no_color:
        return False

    if config.force_color:
        return True

    # Check if we're in a TTY
    return is_tty()


def write_to_console(message: str, stream: TextIO | None = None, log_fallback: bool = True) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested, but avoid recursion by not using Foundation logger
        if log_fallback:
            # Use print to stderr directly to avoid circular dependencies
            import traceback
            try:
                print(f"[DEBUG] Console write failed, falling back to stderr: {e.__class__.__name__}: {e}", file=sys.stderr)
            except Exception:
                # Can't even log to stderr, proceed silently
                pass

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()
