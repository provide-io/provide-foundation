#
# file.py
#
"""
File stream management for Foundation.
Handles file-based logging streams and file operations.
"""

import io
from pathlib import Path
import sys

from provide.foundation.streams.core import (
    _LOG_FILE_HANDLE,
    _PROVIDE_LOG_STREAM,
    _STREAM_LOCK,
)
from provide.foundation.utils.streams import get_safe_stderr


def _safe_error_output(message: str) -> None:
    """
    Output error message to stderr using basic print to avoid circular dependencies.
    
    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(message, file=sys.stderr)


def configure_file_logging(log_file_path: str | None) -> None:
    """
    Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging
    """
    global _PROVIDE_LOG_STREAM, _LOG_FILE_HANDLE

    # Import here to avoid circular dependency
    from provide.foundation.streams.core import _is_in_click_testing

    with _STREAM_LOCK:
        # Don't modify streams if we're in Click testing context
        if _is_in_click_testing():
            return
        # Close existing file handle if it exists
        if _LOG_FILE_HANDLE and _LOG_FILE_HANDLE is not _PROVIDE_LOG_STREAM:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = _PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            _PROVIDE_LOG_STREAM, io.TextIOWrapper
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                _LOG_FILE_HANDLE = open(
                    log_file_path, "a", encoding="utf-8", buffering=1
                )
                _PROVIDE_LOG_STREAM = _LOG_FILE_HANDLE
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                _PROVIDE_LOG_STREAM = get_safe_stderr()
        elif not is_test_stream:
            _PROVIDE_LOG_STREAM = get_safe_stderr()


def flush_log_streams() -> None:
    """Flush all log streams."""
    global _LOG_FILE_HANDLE

    with _STREAM_LOCK:
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.flush()
            except Exception as e:
                _safe_error_output(f"Failed to flush log file handle: {e}")


def close_log_streams() -> None:
    """Close file log streams and reset to stderr."""
    global _PROVIDE_LOG_STREAM, _LOG_FILE_HANDLE

    # Import here to avoid circular dependency
    from provide.foundation.streams.core import _is_in_click_testing

    with _STREAM_LOCK:
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if not _is_in_click_testing():
            _PROVIDE_LOG_STREAM = sys.stderr


def reset_streams() -> None:
    """Reset all stream state (for testing)."""
    # Import here to avoid circular dependency
    from provide.foundation.streams.core import _is_in_click_testing

    # Don't reset streams if we're in Click testing context
    if not _is_in_click_testing():
        close_log_streams()
