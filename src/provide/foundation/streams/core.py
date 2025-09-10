#
# core.py
#
"""
Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

import sys
import threading
from typing import TextIO

from provide.foundation.streams.config import get_stream_config

_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_STREAM_LOCK = threading.Lock()


def _is_in_click_testing() -> bool:
    """Check if we're running inside Click's testing framework."""
    import inspect
    
    config = get_stream_config()
    
    # Check environment variables for Click testing
    if config.click_testing:
        return True

    # Check the call stack for Click's testing module or CLI integration tests
    for frame_info in inspect.stack():
        module = frame_info.frame.f_globals.get("__name__", "")
        filename = frame_info.filename or ""

        if "click.testing" in module or "test_cli_integration" in filename:
            return True

        # Also check for common Click testing patterns
        locals_self = frame_info.frame.f_locals.get("self")
        if hasattr(locals_self, "runner"):
            runner = locals_self.runner
            if hasattr(runner, "invoke") and "CliRunner" in str(type(runner)):
                return True

    return False


def get_log_stream() -> TextIO:
    """Get the current log stream."""
    return _PROVIDE_LOG_STREAM


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        # Don't modify streams if we're in Click testing context
        if _is_in_click_testing():
            return
        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
