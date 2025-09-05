#
# core.py
#
"""
Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

import io
import sys
import threading
from pathlib import Path
from typing import TextIO

from provide.foundation.utils.streams import get_safe_stderr

_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_STREAM_LOCK = threading.Lock()


def get_log_stream() -> TextIO:
    """Get the current log stream."""
    return _PROVIDE_LOG_STREAM


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr