#
# console.py
#
"""
Console stream utilities for Foundation.
Handles console-specific stream operations and formatting.
"""

import sys
from typing import TextIO

from provide.foundation.streams.config import get_stream_config
from provide.foundation.streams.core import get_log_stream


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


def write_to_console(message: str, stream: TextIO | None = None) -> None:
    """
    Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception:
        # Fallback to stderr
        sys.stderr.write(message)
        sys.stderr.flush()
