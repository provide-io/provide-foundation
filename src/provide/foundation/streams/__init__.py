#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.streams.console import (
    get_console_stream,
    is_tty,
    supports_color,
    write_to_console,
)
from provide.foundation.streams.core import (
    ensure_stderr_default,
    get_log_stream,
    set_log_stream_for_testing,
)
from provide.foundation.streams.file import (
    close_log_streams,
    configure_file_logging,
    flush_log_streams,
    reset_streams,
)

"""Foundation Streams Module.

Provides stream management functionality including console, file,
and core stream operations.
"""

__all__ = [
    "close_log_streams",
    # File stream functions
    "configure_file_logging",
    "ensure_stderr_default",
    "flush_log_streams",
    # Console stream functions
    "get_console_stream",
    # Core stream functions
    "get_log_stream",
    "is_tty",
    "reset_streams",
    "set_log_stream_for_testing",
    "supports_color",
    "write_to_console",
]

# 🧱🏗️🔚
