from __future__ import annotations

#
# factories.py
#
import threading
from typing import Any

"""Logger factory functions and simple setup utilities."""

_is_initializing = threading.local()


def get_logger(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function uses Hub-based logger access with initialization detection
    to prevent circular imports during Foundation setup.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    """

    # Check if we're already in the middle of initialization to prevent circular import
    if getattr(_is_initializing, "value", False):
        import structlog

        return structlog.get_logger(name)

    try:
        # Set initialization flag
        _is_initializing.value = True

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always clear the initialization flag
        _is_initializing.value = False
