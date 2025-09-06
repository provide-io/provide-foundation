#
# __init__.py
#
"""
Foundation Streams Module.

Provides stream management functionality including console, file,
and core stream operations.
"""

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

__all__ = [
    # Core stream functions
    "get_log_stream",
    "set_log_stream_for_testing",
    "ensure_stderr_default",
    # File stream functions
    "configure_file_logging",
    "flush_log_streams",
    "close_log_streams",
    "reset_streams",
    # Console stream functions
    "get_console_stream",
    "is_tty",
    "supports_color",
    "write_to_console",
]
