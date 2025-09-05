#
# streams.py
#
"""
Stream and output management for Foundation Telemetry.
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


def configure_file_logging(log_file_path: str | None) -> None:
    """
    Configure file logging if a path is provided.
    
    Args:
        log_file_path: Path to log file, or None to disable file logging
    """
    global _PROVIDE_LOG_STREAM, _LOG_FILE_HANDLE
    
    with _STREAM_LOCK:
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
                print(
                    f"Failed to open log file {log_file_path}: {e}",
                    file=sys.stderr
                )
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
                print(f"Failed to flush log file handle: {e}", file=sys.stderr)


def close_log_streams() -> None:
    """Close file log streams and reset to stderr."""
    global _PROVIDE_LOG_STREAM, _LOG_FILE_HANDLE
    
    with _STREAM_LOCK:
        if _LOG_FILE_HANDLE:
            try:
                _LOG_FILE_HANDLE.close()
            except Exception:
                pass
            _LOG_FILE_HANDLE = None
        _PROVIDE_LOG_STREAM = sys.stderr


def reset_streams() -> None:
    """Reset all stream state (for testing)."""
    close_log_streams()