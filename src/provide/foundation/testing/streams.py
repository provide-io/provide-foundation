#
# streams.py
#
"""
Stream Testing Utilities for Foundation.

Provides utilities for redirecting and managing streams during testing,
allowing tests to capture and control Foundation's output streams.
"""

import sys
import threading
from typing import TextIO

# Import the actual stream management functions
from provide.foundation.streams.core import _PROVIDE_LOG_STREAM, _STREAM_LOCK


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """
    Set the log stream for testing purposes.
    
    This allows tests to redirect Foundation's log output to a custom stream
    (like StringIO) for capturing and verifying log messages.
    
    Args:
        stream: Stream to redirect to, or None to reset to stderr
    """
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr


def get_current_log_stream() -> TextIO:
    """
    Get the currently active log stream.
    
    Returns:
        The current log stream being used by Foundation
    """
    return _PROVIDE_LOG_STREAM


def reset_log_stream() -> None:
    """Reset log stream back to stderr."""
    set_log_stream_for_testing(None)


__all__ = [
    "set_log_stream_for_testing",
    "get_current_log_stream", 
    "reset_log_stream",
]