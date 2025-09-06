#
# coordinator.py
#
"""
Main setup coordination for Foundation Telemetry.
Handles the core setup logic, state management, and setup logger creation.
"""

import logging as stdlib_logging
import threading
from typing import Any

import structlog

from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
from provide.foundation.logger.core import (
    _LAZY_SETUP_STATE,
    logger as foundation_logger,
)
from provide.foundation.logger.emoji.sets import BUILTIN_EMOJI_SETS
from provide.foundation.logger.setup.emoji_resolver import resolve_active_emoji_config
from provide.foundation.logger.setup.processors import (
    configure_structlog_output,
    handle_globally_disabled_setup,
)
from provide.foundation.streams import get_log_stream
from provide.foundation.utils.streams import get_foundation_log_stream, get_safe_stderr

_PROVIDE_SETUP_LOCK = threading.Lock()
_CORE_SETUP_LOGGER_NAME = "provide.foundation.core_setup"
_EXPLICIT_SETUP_DONE = False
_FOUNDATION_LOG_LEVEL: int | None = None


def get_foundation_log_level() -> int:
    """Get the Foundation log level from LoggingConfig, checking only once."""
    global _FOUNDATION_LOG_LEVEL
    if _FOUNDATION_LOG_LEVEL is None:
        # Use the proper config system to get the Foundation setup log level
        logging_config = LoggingConfig.from_env(strict=False)
        level_str = logging_config.foundation_setup_log_level.upper()
        _FOUNDATION_LOG_LEVEL = getattr(
            stdlib_logging,
            level_str,
            stdlib_logging.INFO,  # Default fallback
        )
    return _FOUNDATION_LOG_LEVEL


def create_core_setup_logger(globally_disabled: bool = False) -> Any:
    """Create a structlog logger for core setup messages."""
    if globally_disabled:
        # Configure structlog to be a no-op for core setup logger
        structlog.configure(
            processors=[],
            logger_factory=structlog.ReturnLoggerFactory(),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )
        return structlog.get_logger(_CORE_SETUP_LOGGER_NAME)
    else:
        # Get the foundation log output stream
        try:
            logging_config = LoggingConfig.from_env(strict=False)
            foundation_stream = get_foundation_log_stream(
                logging_config.foundation_log_output
            )
        except Exception:
            # Fallback to stderr if config loading fails
            foundation_stream = get_safe_stderr()

        # Configure structlog for core setup logger
        structlog.configure(
            processors=[
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.dev.ConsoleRenderer(),
            ],
            logger_factory=structlog.PrintLoggerFactory(file=foundation_stream),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(_CORE_SETUP_LOGGER_NAME)


def internal_setup(
    config: TelemetryConfig | None = None, is_explicit_call: bool = False
) -> None:
    """
    The single, internal setup function that both explicit and lazy setup call.
    It is protected by the _PROVIDE_SETUP_LOCK in its callers.
    """
    # This function assumes the lock is already held.
    structlog.reset_defaults()
    foundation_logger._is_configured_by_setup = False
    foundation_logger._active_config = None
    foundation_logger._active_resolved_emoji_config = None
    _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})

    current_config = config if config is not None else TelemetryConfig.from_env()
    core_setup_logger = create_core_setup_logger(
        globally_disabled=current_config.globally_disabled
    )

    if not current_config.globally_disabled:
        core_setup_logger.debug(
            "⚙️➡️🚀 Starting Foundation (structlog) setup",
            service_name=current_config.service_name,
            log_level=current_config.logging.default_level,
            formatter=current_config.logging.console_formatter,
        )

    resolved_emoji_config = resolve_active_emoji_config(
        current_config.logging, BUILTIN_EMOJI_SETS
    )

    if current_config.globally_disabled:
        handle_globally_disabled_setup()
    else:
        configure_structlog_output(
            current_config, resolved_emoji_config, get_log_stream()
        )

    foundation_logger._is_configured_by_setup = is_explicit_call
    foundation_logger._active_config = current_config
    foundation_logger._active_resolved_emoji_config = resolved_emoji_config
    _LAZY_SETUP_STATE["done"] = True

    if not current_config.globally_disabled:
        field_definitions, emoji_sets = resolved_emoji_config
        core_setup_logger.debug(
            "⚙️➡️✅ Foundation (structlog) setup completed",
            emoji_sets_enabled=len(field_definitions) > 0,
            emoji_sets_count=len(emoji_sets),
            processors_configured=True,
            log_file_enabled=current_config.logging.log_file is not None,
        )
