#
# core.py
#
"""Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

import sys
import threading
from typing import TextIO

from provide.foundation.streams.config import get_stream_config

_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_STREAM_LOCK = threading.Lock()




def get_log_stream() -> TextIO:
    """Get the current log stream."""
    return _PROVIDE_LOG_STREAM


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes."""
    from provide.foundation.testmode.detection import is_in_click_testing

    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
