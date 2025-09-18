from __future__ import annotations

#
# core.py
#
import sys
import threading
from typing import TextIO

"""Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

_PROVIDE_LOG_STREAM: TextIO = sys.stderr
_LOG_FILE_HANDLE: TextIO | None = None
_STREAM_LOCK = threading.Lock()


def get_log_stream() -> TextIO:
    """Get the current log stream."""
    return _PROVIDE_LOG_STREAM


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.
    """
    from provide.foundation.testmode.detection import is_in_click_testing

    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return

        _PROVIDE_LOG_STREAM = stream if stream is not None else sys.stderr

        # Reconfigure structlog if it's already configured to use the new stream
        try:
            import structlog

            current_config = structlog.get_config()
            if current_config and "logger_factory" in current_config:
                # Reconfigure with the new stream while preserving other config
                new_config = {**current_config}
                new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
                structlog.configure(**new_config)
        except Exception:
            # Structlog not configured yet or reconfiguration failed, that's fine
            pass


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
