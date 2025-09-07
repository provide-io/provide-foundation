#
# factories.py
#
"""
Logger factory functions and simple setup utilities.
"""

from typing import Any

from provide.foundation.logger.core import logger


def get_logger(
    name: str | None = None,
    emoji: str | None = None,
    emoji_hierarchy: dict[str, str] | None = None
) -> Any:
    """
    Get a logger instance with the given name and optional emoji customization.

    This is a convenience function that uses the global FoundationLogger.

    Args:
        name: Logger name (e.g., __name__ from a module)
        emoji: Override emoji for this specific logger instance
        emoji_hierarchy: Define emoji mapping for module hierarchy patterns

    Returns:
        Configured structlog logger instance
    """
    # Register emoji hierarchy if provided
    if emoji_hierarchy and name:
        from provide.foundation.logger.emoji.hierarchy import register_emoji_hierarchy
        # Extract base module from name for hierarchy registration
        base_module = name.split('.')[0]
        register_emoji_hierarchy(base_module, emoji_hierarchy)
    
    # Register single emoji if provided
    if emoji and name:
        from provide.foundation.logger.emoji.hierarchy import register_single_emoji
        register_single_emoji(name, emoji)
    
    return logger.get_logger(name)


def setup_logging(
    level: str | int = "INFO",
    json_logs: bool = False,
    log_file: str | None = None,
    **kwargs: Any,
) -> None:
    """
    Simple logging setup for basic use cases.

    Args:
        level: Log level (string or int)
        json_logs: Whether to output logs as JSON
        log_file: Optional file path to write logs
        **kwargs: Additional configuration options
    """
    from pathlib import Path

    from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
    from provide.foundation.setup import setup_telemetry

    # Convert simple parameters to full config
    logging_config = LoggingConfig(
        default_level=str(level).upper(),
        console_formatter="json" if json_logs else "key_value",
        log_file=Path(log_file) if log_file else None,
    )

    telemetry_config = TelemetryConfig(logging=logging_config, **kwargs)
    setup_telemetry(telemetry_config)
