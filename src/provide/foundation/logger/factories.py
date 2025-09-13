#
# factories.py
#
"""
Logger factory functions and simple setup utilities.
"""

from typing import Any


def get_logger(
    name: str | None = None,
    emoji: str | None = None,
    emoji_hierarchy: dict[str, str] | None = None,
) -> Any:
    """
    Get a logger instance through Hub.

    This function now uses Hub-based logger access instead of a global singleton.
    Auto-initializes Foundation if not already done.

    Args:
        name: Logger name (e.g., __name__ from a module)
        emoji: Override emoji for this specific logger instance (deprecated)
        emoji_hierarchy: Define emoji mapping for module hierarchy patterns (deprecated)

    Returns:
        Configured structlog logger instance
    """
    # Emoji hierarchy removed - using event sets now
    # emoji and emoji_hierarchy parameters are deprecated

    from provide.foundation.hub.manager import get_hub

    hub = get_hub()
    return hub.get_foundation_logger(name)


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
    import warnings
    from pathlib import Path

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
