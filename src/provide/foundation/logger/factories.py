#
# factories.py
#
"""
Logger factory functions and simple setup utilities.
"""

import threading
from typing import Any

# Thread-local storage to track initialization state
_is_initializing = threading.local()


def get_logger(
    name: str | None = None,
    emoji: str | None = None,
    emoji_hierarchy: dict[str, str] | None = None,
) -> Any:
    """
    Get a logger instance through Hub with circular import protection.

    This function uses Hub-based logger access with initialization detection
    to prevent circular imports during Foundation setup.

    Args:
        name: Logger name (e.g., __name__ from a module)
        emoji: Override emoji for this specific logger instance (deprecated)
        emoji_hierarchy: Define emoji mapping for module hierarchy patterns (deprecated)

    Returns:
        Configured structlog logger instance
    """
    # Emoji hierarchy removed - using event sets now
    # emoji and emoji_hierarchy parameters are deprecated

    # Check if we're already in the middle of initialization to prevent circular import
    if getattr(_is_initializing, 'value', False):
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


def setup_logging(
    level: str | int = "INFO",
    json_logs: bool = False,
    log_file: str | None = None,
    **kwargs: Any,
) -> None:
    """
    Simple logging setup for basic use cases.

    Now uses Hub-based initialization instead of legacy setup functions.

    Args:
        level: Log level (string or int)
        json_logs: Whether to output logs as JSON
        log_file: Optional file path to write logs
        **kwargs: Additional configuration options
    """
    from pathlib import Path
    import warnings

    warnings.warn(
        "setup_logging() is deprecated. Foundation now auto-initializes on first use. "
        "For explicit configuration, use Hub.initialize_foundation(config).",
        DeprecationWarning,
        stacklevel=2,
    )

    from provide.foundation.hub.manager import get_hub
    from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

    # Convert simple parameters to full config
    logging_config = LoggingConfig(
        default_level=str(level).upper(),
        console_formatter="json" if json_logs else "key_value",
        log_file=Path(log_file) if log_file else None,
    )

    telemetry_config = TelemetryConfig(logging=logging_config, **kwargs)

    # Initialize through Hub instead of legacy setup
    hub = get_hub()
    hub.initialize_foundation(telemetry_config)
