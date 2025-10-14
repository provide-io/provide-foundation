# provide/foundation/logger/setup/coordinator.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging as stdlib_logging
from typing import Any

import structlog

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.core import (
    _LAZY_SETUP_STATE,
    logger as foundation_logger,
)
from provide.foundation.logger.setup.processors import (
    configure_structlog_output,
    handle_globally_disabled_setup,
)
from provide.foundation.streams import get_log_stream
from provide.foundation.utils.streams import get_safe_stderr

"""Main setup coordination for Foundation Telemetry.
Handles the core setup logic, state management, and setup logger creation.
"""

_CORE_SETUP_LOGGER_NAME = "provide.foundation.core_setup"
_EXPLICIT_SETUP_DONE = False
_FOUNDATION_LOG_LEVEL: int | None = None
_CACHED_SETUP_LOGGER: Any | None = None


def get_foundation_log_level(config: TelemetryConfig | None = None) -> int:
    """Get Foundation log level for setup phase, safely.

    Args:
        config: Optional TelemetryConfig to use. If provided, uses config value.
               If None, loads from environment and caches.

    Returns:
        Numeric log level from stdlib logging module

    """
    global _FOUNDATION_LOG_LEVEL

    # If config provided, use it directly (no caching)
    if config is not None:
        level_str = config.logging.foundation_setup_log_level.upper()
        valid_levels = {
            "CRITICAL": stdlib_logging.CRITICAL,
            "ERROR": stdlib_logging.ERROR,
            "WARNING": stdlib_logging.WARNING,
            "INFO": stdlib_logging.INFO,
            "DEBUG": stdlib_logging.DEBUG,
            "NOTSET": stdlib_logging.NOTSET,
        }
        return valid_levels.get(level_str, stdlib_logging.INFO)

    # Otherwise use cached value or load from config
    if _FOUNDATION_LOG_LEVEL is None:
        # Load config to get foundation_setup_log_level
        temp_config = TelemetryConfig.from_env()
        level_str = temp_config.logging.foundation_setup_log_level.upper()

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
    """Create Foundation's internal setup logger (structlog).

    This is used internally by Foundation during its own initialization.
    Components should use get_system_logger() instead.

    Returns the same logger instance when called multiple times (singleton pattern).
    """
    global _CACHED_SETUP_LOGGER

    # Return cached logger if already created
    if _CACHED_SETUP_LOGGER is not None:
        return _CACHED_SETUP_LOGGER
    if globally_disabled:
        # Configure structlog to be a no-op for core setup logger
        structlog.configure(
            processors=[],
            logger_factory=structlog.ReturnLoggerFactory(),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )
        _CACHED_SETUP_LOGGER = structlog.get_logger(_CORE_SETUP_LOGGER_NAME)
        return _CACHED_SETUP_LOGGER
    # Get the foundation log output stream, respecting test stream redirection
    try:
        # Use get_log_stream() which respects test stream redirection
        foundation_stream = get_log_stream()
    except Exception:
        # Fallback to stderr if stream access fails
        foundation_stream = get_safe_stderr()

    # Get the log level threshold
    log_level_threshold = get_foundation_log_level()

    # Create a filtering processor that respects FOUNDATION_LOG_LEVEL
    def filter_by_foundation_level(logger: Any, method_name: str, event_dict: Any) -> Any:
        """Filter log entries by Foundation log level threshold."""
        # Get numeric level for the current log method
        level_map = {
            "debug": stdlib_logging.DEBUG,
            "info": stdlib_logging.INFO,
            "warning": stdlib_logging.WARNING,
            "error": stdlib_logging.ERROR,
            "critical": stdlib_logging.CRITICAL,
            "trace": 5,  # TRACE level
        }
        current_level = level_map.get(method_name, stdlib_logging.INFO)

        # Drop the event if it's below the threshold
        if current_level < log_level_threshold:
            raise structlog.DropEvent

        return event_dict

    # Check if output stream is a TTY for color support
    is_tty = hasattr(foundation_stream, "isatty") and foundation_stream.isatty()

    # Configure structlog for core setup logger with same formatting as application logger
    structlog.configure(
        processors=[
            filter_by_foundation_level,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
            structlog.dev.ConsoleRenderer(colors=is_tty, exception_formatter=structlog.dev.plain_traceback),
        ],
        logger_factory=structlog.PrintLoggerFactory(file=foundation_stream),
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

    _CACHED_SETUP_LOGGER = structlog.get_logger(_CORE_SETUP_LOGGER_NAME)
    return _CACHED_SETUP_LOGGER


def reset_setup_logger_cache() -> None:
    """Reset the cached setup logger for testing."""
    global _CACHED_SETUP_LOGGER
    _CACHED_SETUP_LOGGER = None


def reset_foundation_log_level_cache() -> None:
    """Reset the cached Foundation log level for testing."""
    global _FOUNDATION_LOG_LEVEL
    _FOUNDATION_LOG_LEVEL = None


def reset_coordinator_state() -> None:
    """Reset all coordinator state for testing."""
    reset_setup_logger_cache()
    reset_foundation_log_level_cache()


def _configure_stdlib_module_logging(module_levels: dict[str, str] | dict[str, Any]) -> None:
    """Configure Python stdlib logging for module-level suppression.

    This suppresses DEBUG messages from third-party modules like asyncio.

    Args:
        module_levels: Dictionary mapping module names to log levels

    """
    for module_name, level_str in module_levels.items():
        module_logger = stdlib_logging.getLogger(module_name)
        numeric_level = stdlib_logging.getLevelName(str(level_str).upper())
        if isinstance(numeric_level, int):
            module_logger.setLevel(numeric_level)


def get_system_logger(name: str, config: TelemetryConfig | None = None) -> object:
    """Get a vanilla Python logger without Foundation enhancements.

    This provides a plain Python logger that respects FOUNDATION_LOG_LEVEL
    but doesn't trigger Foundation's initialization. Use this for logging
    during Foundation's setup phase or when you need to avoid circular
    dependencies.

    Args:
        name: Logger name (e.g., "provide.foundation.otel.setup")
        config: Optional TelemetryConfig to use for log level and output

    Returns:
        A standard Python logging.Logger instance

    Note:
        "Vanilla" means plain/unmodified Python logging, without
        Foundation's features like emoji prefixes or structured logging.

    """
    import logging
    import sys

    slog = logging.getLogger(name)

    # Configure only once per logger
    if not slog.handlers:
        log_level = get_foundation_log_level(config)
        slog.setLevel(log_level)

        # Respect FOUNDATION_LOG_OUTPUT setting from config or env
        if config is not None:
            output = config.logging.foundation_log_output.lower()
        else:
            # Load config to get foundation_log_output
            temp_config = TelemetryConfig.from_env()
            output = temp_config.logging.foundation_log_output.lower()

        stream = sys.stderr if output != "stdout" else sys.stdout

        handler = logging.StreamHandler(stream)
        handler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)-5s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        handler.setFormatter(formatter)
        slog.addHandler(handler)

        # Don't propagate to avoid duplicate messages
        slog.propagate = False

    return slog


def internal_setup(config: TelemetryConfig | None = None, is_explicit_call: bool = False) -> None:
    """The single, internal setup function that both explicit and lazy setup call.
    It is protected by the _PROVIDE_SETUP_LOCK in its callers.
    """
    # This function assumes the lock is already held.
    structlog.reset_defaults()

    # Reset OTLP provider to ensure new LoggerProvider with updated config
    # This is critical when service_name changes, as OpenTelemetry's Resource is immutable
    try:
        from provide.foundation.logger.processors.otlp import reset_otlp_provider

        reset_otlp_provider()
    except ImportError:
        # OTLP not available (missing opentelemetry packages), skip reset
        pass

    # Use __dict__ access to avoid triggering proxy initialization
    foundation_logger.__dict__["_is_configured_by_setup"] = False
    foundation_logger.__dict__["_active_config"] = None
    _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})

    current_config = config if config is not None else TelemetryConfig.from_env()
    core_setup_logger = create_foundation_internal_logger(globally_disabled=current_config.globally_disabled)

    if not current_config.globally_disabled:
        core_setup_logger.debug(
            "⚙️➡️🚀 Starting Foundation (structlog) setup",
            service_name=current_config.service_name,
            log_level=current_config.logging.default_level,
            formatter=current_config.logging.console_formatter,
        )

        # Log OpenTelemetry/OTLP configuration
        if current_config.otlp_endpoint:
            try:
                from provide.foundation.integrations.openobserve.config import OpenObserveConfig

                oo_config = OpenObserveConfig.from_env()
                if oo_config.is_configured():
                    # OpenObserve auto-configured OTLP
                    core_setup_logger.debug(
                        "📡 OpenObserve integration enabled - OTLP log export active",
                        otlp_endpoint=current_config.otlp_endpoint,
                        openobserve_org=oo_config.org,
                        openobserve_stream=oo_config.stream,
                    )
                else:
                    # Manually configured OTLP
                    core_setup_logger.debug(
                        "📡 OpenTelemetry OTLP log export active",
                        otlp_endpoint=current_config.otlp_endpoint,
                        otlp_traces_endpoint=current_config.otlp_traces_endpoint,
                    )
            except ImportError:
                # OpenObserve not available, just log basic OTLP config
                core_setup_logger.debug(
                    "📡 OpenTelemetry OTLP log export active",
                    otlp_endpoint=current_config.otlp_endpoint,
                    otlp_traces_endpoint=current_config.otlp_traces_endpoint,
                )

    if current_config.globally_disabled:
        core_setup_logger.trace("Setting up globally disabled telemetry")
        handle_globally_disabled_setup()
    else:
        # Configure log file if specified
        if current_config.logging.log_file is not None:
            from provide.foundation.streams.file import configure_file_logging

            configure_file_logging(log_file_path=str(current_config.logging.log_file))

        core_setup_logger.trace("Configuring structlog output processors")
        configure_structlog_output(current_config, get_log_stream())

    # Use __dict__ access to avoid triggering proxy initialization
    foundation_logger.__dict__["_is_configured_by_setup"] = is_explicit_call
    foundation_logger.__dict__["_active_config"] = current_config
    _LAZY_SETUP_STATE["done"] = True

    # Configure Python stdlib logging for module-level suppression
    if not current_config.globally_disabled and current_config.logging.module_levels:
        _configure_stdlib_module_logging(current_config.logging.module_levels)

    if not current_config.globally_disabled:
        core_setup_logger.debug(
            "⚙️➡️✅ Foundation (structlog) setup completed",
            processors_configured=True,
            log_file_enabled=current_config.logging.log_file is not None,
        )


# <3 🧱🤝📝🪄
