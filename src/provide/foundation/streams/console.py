#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# console.py
#
import sys
from typing import TextIO

from provide.foundation.streams.config import get_stream_config
from provide.foundation.streams.core import get_log_stream

"""Console stream utilities for Foundation.
Handles console-specific stream operations and formatting.
"""


def get_console_stream() -> TextIO:
    """Get the appropriate console stream for output."""
    return get_log_stream()


def is_tty() -> bool:
    """Check if the current stream is a TTY (terminal)."""
    stream = get_log_stream()
    return hasattr(stream, "isatty") and stream.isatty()


def supports_color() -> bool:
    """Check if the current stream supports color output."""
    config = get_stream_config()

    if config.no_color:
        return False

    if config.force_color:
        return True

    # Check if we're in a TTY
    return is_tty()


def write_to_console(message: str, stream: TextIO | None = None, log_fallback: bool = True) -> None:
    """Write a message to the console stream.

    Args:
        message: Message to write
        stream: Optional specific stream to write to, defaults to current console stream
        log_fallback: Whether to log when falling back to stderr

    """
    target_stream = stream or get_console_stream()
    try:
        target_stream.write(message)
        target_stream.flush()
    except Exception as e:
        # Log the fallback for debugging if requested
        if log_fallback:
            try:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().debug(
                    "Console write failed, falling back to stderr",
                    error=str(e),
                    error_type=type(e).__name__,
                    stream_type=type(target_stream).__name__,
                )
            except Exception as log_error:
                # Foundation logger failed, fall back to direct stderr logging
                try:
                    sys.stderr.write(
                        f"[DEBUG] Console write failed (logging also failed): "
                        f"{e.__class__.__name__}: {e} (log_error: {log_error.__class__.__name__})\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    # Even stderr failed - this is a critical system failure, we cannot continue
                    raise RuntimeError(
                        "Critical system failure: unable to write debug information to any stream"
                    ) from e

        # Fallback to stderr - if this fails, let it propagate
        sys.stderr.write(message)
        sys.stderr.flush()


# 🧱🏗️🔚
