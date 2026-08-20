#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Core stream management for Foundation.
Handles log streams, file handles, and output configuration.
"""

from __future__ import annotations

import sys
import threading
from typing import TextIO

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.errors.base import FoundationError
from provide.foundation.utils.streams import ensure_utf8_stream

_PROVIDE_LOG_STREAM: TextIO = ensure_utf8_stream(sys.stderr)
_LOG_FILE_HANDLE: TextIO | None = None

# How long any of the stream operations below will wait for the stream lock.
_STREAM_LOCK_TIMEOUT_SECONDS = 5.0


def _get_stream_lock() -> threading.RLock:
    """Get the stream lock from LockManager.

    Returns managed lock to prevent deadlocks and enable monitoring.
    """
    # Lock is registered during Foundation initialization via register_foundation_locks()
    return get_lock_manager().get_lock("foundation.stream")


def get_log_stream() -> TextIO:
    """Get the current log stream.

    Note: High complexity is intentional for robust stream handling across test/prod.
    """
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, return stderr as fallback
        return ensure_utf8_stream(sys.stderr)
    try:
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
                # Handle specific stream-related errors
                # NOTE: Cannot use Foundation logger here as it depends on these same streams (circular dependency)
                # Using perr() which is safe as it doesn't depend on Foundation logger
                try:
                    from provide.foundation.console.output import perr

                    perr(
                        f"[STREAM ERROR] Stream operation failed, falling back to stderr: "
                        f"{e.__class__.__name__}: {e}"
                    )
                except Exception:
                    # Generic catch intentional: perr() import/call failed.
                    # Try direct stderr write as absolute last resort.
                    try:
                        sys.stderr.write(
                            f"[STREAM ERROR] Stream operation failed: {e.__class__.__name__}: {e}\n"
                        )
                        sys.stderr.flush()
                    except Exception:
                        # Generic catch intentional: Even stderr.write() failed.
                        # Suppress all errors - this is low-level stream infrastructure.
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
    finally:
        _get_stream_lock().release()


def _reconfigure_structlog_stream() -> None:
    """Reconfigure structlog to use the current log stream.

    This helper function updates structlog's logger factory to use the current
    _PROVIDE_LOG_STREAM value, preserving all other configuration.
    """
    try:
        import structlog

        current_config = structlog.get_config()
        if current_config and "logger_factory" in current_config:
            # Check if force stream redirect is enabled
            from provide.foundation.streams.config import get_stream_config

            stream_config = get_stream_config()
            cache_loggers = not stream_config.force_stream_redirect

            # Reconfigure with the new stream while preserving other config
            new_config = {**current_config}
            new_config["logger_factory"] = structlog.PrintLoggerFactory(file=_PROVIDE_LOG_STREAM)
            new_config["cache_logger_on_first_use"] = cache_loggers
            structlog.configure(**new_config)
    except Exception:
        # Generic catch intentional: structlog might not be configured yet,
        # might not be installed, or reconfiguration may fail.
        # All cases are acceptable - just proceed without reconfiguration.
        pass


class StreamRedirectRefusedError(FoundationError):
    """A test-stream redirect was asked for and not performed.

    Both refusals below used to return quietly. A caller that had asked to
    capture logs then held a buffer nothing was writing to, and found out via
    whatever it asserted about the contents -- typically `len(lines) == 1`
    failing with 0, in a test that had nothing to do with streams. The reason
    is known at the point of refusal and is worth raising there.
    """

    def _default_code(self) -> str:
        return "STREAM_REDIRECT_REFUSED"


def set_log_stream_for_testing(stream: TextIO | None) -> None:
    """Set the log stream for testing purposes.

    This function not only sets the stream but also reconfigures structlog
    if it's already configured to ensure logs actually go to the test stream.

    Raises:
        StreamRedirectRefusedError: If the redirect could not be performed.
            Never returns without having installed `stream`.
    """
    from provide.foundation.testmode.detection import should_allow_stream_redirect

    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=_STREAM_LOCK_TIMEOUT_SECONDS):
        raise StreamRedirectRefusedError(
            f"Timed out after {_STREAM_LOCK_TIMEOUT_SECONDS}s waiting for the "
            f"foundation.stream lock; the log stream was left unchanged.",
            reason="lock_timeout",
        )
    try:
        # The Click guard exists to stop Click's own output capture being
        # hijacked. Restoring the default stream hijacks nothing, so a reset is
        # always honoured -- refusing one would strand a caller on whatever
        # buffer it was tearing down.
        if stream is not None and not should_allow_stream_redirect():
            raise StreamRedirectRefusedError(
                "Stream redirection is blocked inside Click's testing context, so "
                "Click's own output capture is not disturbed. Set "
                "FOUNDATION_FORCE_STREAM_REDIRECT=true to redirect anyway.",
                reason="click_testing",
            )

        _PROVIDE_LOG_STREAM = (
            ensure_utf8_stream(stream) if stream is not None else ensure_utf8_stream(sys.stderr)
        )

        # Reconfigure structlog to use the new stream
        _reconfigure_structlog_stream()
    finally:
        _get_stream_lock().release()


def ensure_stderr_default() -> None:
    """Ensure the log stream defaults to stderr if it's stdout."""
    global _PROVIDE_LOG_STREAM
    if not _get_stream_lock().acquire(timeout=5.0):
        # If we can't acquire the lock within 5 seconds, skip the operation
        return
    try:
        if _PROVIDE_LOG_STREAM is sys.stdout:
            _PROVIDE_LOG_STREAM = ensure_utf8_stream(sys.stderr)
    finally:
        _get_stream_lock().release()


# 🧱🏗️🔚
