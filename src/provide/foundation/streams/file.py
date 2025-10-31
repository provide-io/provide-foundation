#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# file.py
#
import contextlib
import io
from pathlib import Path
import sys

from provide.foundation.streams.core import (
    _get_stream_lock,
    _reconfigure_structlog_stream,
)
from provide.foundation.utils.streams import get_safe_stderr

"""File stream management for Foundation.
Handles file-based logging streams and file operations.
"""


def _safe_error_output(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(message, file=sys.stderr)


def configure_file_logging(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def flush_log_streams() -> None:
    """Flush all log streams."""
    import provide.foundation.streams.core as core_module

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            try:
                core_module._LOG_FILE_HANDLE.flush()
            except Exception as e:
                _safe_error_output(f"Failed to flush log file handle: {e}")


def close_log_streams() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if not is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = sys.stderr
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def reset_streams() -> None:
    """Reset all stream state (for testing)."""
    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    # Don't reset streams if we're in Click testing context
    if not is_in_click_testing():
        close_log_streams()


# 🧱🏗️🔚
