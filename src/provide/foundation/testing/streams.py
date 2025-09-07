#
# streams.py
#
"""
Stream Testing Utilities for Foundation.

Provides utilities for redirecting and managing streams during testing,
allowing tests to capture and control Foundation's output streams.
"""

from typing import TextIO

# Import the actual stream management variables
from provide.foundation.streams.core import get_log_stream


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """
    Set the log stream for testing purposes.

    This allows tests to redirect Foundation's log output to a custom stream
    (like StringIO) for capturing and verifying log messages.

    Args:
        stream: Stream to redirect to, or None to reset to stderr
    """
    # Import the actual implementation from streams.core
    from provide.foundation.streams.core import (
        set_log_stream_for_testing as _set_stream,
    )

    _set_stream(stream)


def get_current_log_stream() -> TextIO:
    """
    Get the currently active log stream.

    Returns:
        The current log stream being used by Foundation
    """
    return get_log_stream()


def reset_log_stream() -> None:
    """Reset log stream back to stderr."""
    set_log_stream_for_testing(None)


__all__ = [
    "get_current_log_stream",
    "reset_log_stream",
    "set_log_stream_for_testing",
]
