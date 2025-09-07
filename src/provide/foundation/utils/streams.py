"""Stream utilities for foundation library."""

import io
import sys
from typing import TextIO


def get_safe_stderr() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()
    """
    return (
        sys.stderr
        if hasattr(sys, "stderr") and sys.stderr is not None
        else io.StringIO()
    )


def get_foundation_log_stream(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning
    """
    if output_setting == "stdout":
        return sys.stdout
    elif output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config import _get_config_logger

            _get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()
