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
    """Get Foundation log level for setup phase, safely."""
    global _FOUNDATION_LOG_LEVEL
    if _FOUNDATION_LOG_LEVEL is None:
        import os
        
        # Direct env read - avoid config imports that cause circular deps
        level_str = os.environ.get("FOUNDATION_LOG_LEVEL", "INFO").upper()
        
        # Validate and map to numeric level
        valid_levels = {
            "CRITICAL": stdlib_logging.CRITICAL,
            "ERROR": stdlib_logging.ERROR,
            "WARNING": stdlib_logging.WARNING,
            "INFO": stdlib_logging.INFO,
            "DEBUG": stdlib_logging.DEBUG,
            "NOTSET": stdlib_logging.NOTSET,
        }
        
        _FOUNDATION_LOG_LEVEL = valid_levels.get(level_str, stdlib_logging.INFO)
    return _FOUNDATION_LOG_LEVEL


def create_foundation_internal_logger(globally_disabled: bool = False) -> Any:
    """
    Create Foundation's internal setup logger (structlog).
    
    This is used internally by Foundation during its own initialization.
    Components should use get_vanilla_logger() instead.
    """
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
            logging_config = LoggingConfig.from_env()
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


def get_vanilla_logger(name: str):
    """
    Get a vanilla Python logger without Foundation enhancements.
    
    This provides a plain Python logger that respects FOUNDATION_LOG_LEVEL
    but doesn't trigger Foundation's initialization. Use this for logging
    during Foundation's setup phase or when you need to avoid circular
    dependencies.
    
    Args:
        name: Logger name (e.g., "provide.foundation.otel.setup")
    
    Returns:
        A standard Python logging.Logger instance
        
    Note:
        "Vanilla" means plain/unmodified Python logging, without
        Foundation's features like emoji prefixes or structured logging.
    """
    import logging
    import sys
    import os
    
    slog = logging.getLogger(name)
    
    # Configure only once per logger
    if not slog.handlers:
        log_level = get_foundation_log_level()
        slog.setLevel(log_level)
        
        # Respect FOUNDATION_LOG_OUTPUT setting
        output = os.environ.get("FOUNDATION_LOG_OUTPUT", "stderr").lower()
        stream = sys.stderr if output != "stdout" else sys.stdout
        
        handler = logging.StreamHandler(stream)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)-5s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        handler.setFormatter(formatter)
        slog.addHandler(handler)
        
        # Don't propagate to avoid duplicate messages
        slog.propagate = False
    
    return slog


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
    _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})

    current_config = config if config is not None else TelemetryConfig.from_env()
    core_setup_logger = create_foundation_internal_logger(
        globally_disabled=current_config.globally_disabled
    )

    if not current_config.globally_disabled:
        core_setup_logger.debug(
            "⚙️➡️🚀 Starting Foundation (structlog) setup",
            service_name=current_config.service_name,
            log_level=current_config.logging.default_level,
            formatter=current_config.logging.console_formatter,
        )


    if current_config.globally_disabled:
        handle_globally_disabled_setup()
    else:
        configure_structlog_output(
            current_config, get_log_stream()
        )

    foundation_logger._is_configured_by_setup = is_explicit_call
    foundation_logger._active_config = current_config
    _LAZY_SETUP_STATE["done"] = True

    if not current_config.globally_disabled:
        core_setup_logger.debug(
            "⚙️➡️✅ Foundation (structlog) setup completed",
            processors_configured=True,
            log_file_enabled=current_config.logging.log_file is not None,
        )
