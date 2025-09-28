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
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        # Only validate real streams, not mock objects
        # Check if this is a real stream that can be closed
        if (
            hasattr(_PROVIDE_LOG_STREAM, "closed")
            and not hasattr(_PROVIDE_LOG_STREAM, "_mock_name")  # Skip mock objects
            and _PROVIDE_LOG_STREAM.closed
        ):
            # Stream is closed, reset to stderr
            try:
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                        _PROVIDE_LOG_STREAM = sys.stderr
                    else:
                        # Even sys.stderr is closed, use a safe fallback
                        try:
                            import io

                            _PROVIDE_LOG_STREAM = io.StringIO()  # Safe fallback for parallel tests
                        except ImportError:
                            # Last resort - raise exception
                            raise ValueError("All available streams are closed") from None
                else:
                    # Create a safe fallback stream
                    try:
                        import io

                        _PROVIDE_LOG_STREAM = io.StringIO()
                    except ImportError:
                        raise ValueError("No stderr available") from None
            except (OSError, AttributeError) as e:
                # Handle specific stream-related errors with logging
                try:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        "Stream operation failed, falling back to stderr",
                        error=str(e),
                        error_type=type(e).__name__,
                    )
                except Exception:
                    # Can't log, proceed with fallback anyway
                    pass

                # Try stderr one more time before giving up
                if hasattr(sys, "stderr") and sys.stderr is not None:
                    try:
                        if not (hasattr(sys.stderr, "closed") and sys.stderr.closed):
                            _PROVIDE_LOG_STREAM = sys.stderr
                        else:
                            # Even stderr is closed - this is a critical error
                            raise ValueError("All available streams are closed (including stderr)") from e
                    except (OSError, AttributeError):
                        # stderr is also problematic - this is a critical error
                        raise ValueError("Stream validation failed - stderr unavailable") from e
                else:
                    # No stderr available - this is a critical error
                    raise ValueError("Stream validation failed - no stderr available") from e

        return _PROVIDE_LOG_STREAM


def _reconfigure_structlog_stream() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
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

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    with _STREAM_LOCK:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = sys.stderr
