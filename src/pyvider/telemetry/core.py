#
# core.py
#
"""
Pyvider Telemetry Core Initialization and Configuration.

This module is the heart of the `pyvider-telemetry` library's setup process.
It is responsible for initializing and configuring the `structlog`-based
logging system according to the provided `TelemetryConfig`.

Key functionalities include:
- `setup_telemetry()`: The primary function for users to explicitly configure
  the telemetry system. It takes a `TelemetryConfig` object (or loads one
  from environment variables) and applies it. This involves:
    - Resetting any existing `structlog` configuration.
    - Building the appropriate chain of `structlog` processors based on the
      configuration (e.g., formatters, emoji handlers, timestamp options).
    - Configuring `structlog` with these processors and the chosen output stream.
- Global State Management: Manages global state related to logging, such as
  the output stream (`_PYVIDER_LOG_STREAM`, defaulting to `sys.stderr`) and
  flags indicating whether explicit setup has been performed (`_EXPLICIT_SETUP_DONE`).
  It also interacts with the lazy initialization state in `logger.base`.
- Processor Chain Assembly: Contains helper functions (e.g.,
  `_build_complete_processor_chain`, `_configure_structlog_output`) that
  construct the list of `structlog` processors by combining core processors
  (like level filtering, context merging) with formatter-specific processors
  (JSON or key-value).
- Default Stream Handling: Ensures that logging output defaults to `sys.stderr`
  and provides utilities for testing with custom streams.
- Shutdown Capabilities: Provides `shutdown_pyvider_telemetry()` for performing
  any necessary cleanup or finalization tasks (currently logs a shutdown message).
- Internal Setup Logger: Uses a standard library logger (`_core_setup_logger`)
  to log messages specifically related to the telemetry setup process itself,
  aiding in debugging configuration issues.

This module orchestrates the configuration details defined in `config.py` and
applies them to the `structlog` system, making it ready for use by the
application via the `pyvider.telemetry.logger` instance.
"""

import logging as stdlib_logging
import os
import sys
import threading
from typing import Any, TextIO, cast

import structlog
from structlog.types import BindableLogger

from pyvider.telemetry.config import (
    TelemetryConfig,
    _build_core_processors_list,
    _build_formatter_processors_list,
)
from pyvider.telemetry.logger import (
    base as logger_base_module,
)

# Enhanced global state management
_PYVIDER_SETUP_LOCK = threading.Lock() # Lock for thread-safe setup operations
_PYVIDER_LOG_STREAM: TextIO = sys.stderr  # Always default to stderr
_CORE_SETUP_LOGGER_NAME = "pyvider.telemetry.core_setup"
_EXPLICIT_SETUP_DONE = False


def _get_safe_stderr() -> TextIO:
    """
    Returns a safe fallback TextIO stream (defaults to `sys.stderr` or `io.StringIO`).

    This function attempts to return `sys.stderr`. If `sys.stderr` is `None` or
    unavailable, it returns an `io.StringIO` instance as a memory-based fallback,
    ensuring that logging components attempting to write to stderr can always
    obtain a valid stream object.

    Returns:
        TextIO: A writable text stream, preferring `sys.stderr` if available.
    """
    if hasattr(sys, 'stderr') and sys.stderr is not None:
        return sys.stderr
    else:
        # Fallback: create a no-op stream if stderr is not available
        import io
        return io.StringIO()


def _set_log_stream_for_testing(stream: TextIO | None) -> None:
    """
    Sets the global log output stream, primarily for testing purposes.

    This allows tests to redirect log output to a custom stream (e.g., `io.StringIO`)
    for capturing and asserting log messages. Setting the stream to `None` resets
    it to the default (`sys.stderr`).

    Warning:
        This is a global setting and should generally only be used in controlled
        testing environments to avoid unintended side effects.

    Args:
        stream (TextIO | None): The TextIO stream to use for logging output.
            If `None`, resets the stream to `sys.stderr`.
    """
    global _PYVIDER_LOG_STREAM
    _PYVIDER_LOG_STREAM = stream if stream is not None else sys.stderr


def _ensure_stderr_default() -> None:
    """
    Ensures the global log output stream (`_PYVIDER_LOG_STREAM`) is `sys.stderr`.

    If `_PYVIDER_LOG_STREAM` is found to be `sys.stdout`, this function corrects
    it to `sys.stderr`. This is a safeguard to prevent accidental logging to
    standard output when standard error is the intended default for logs.
    It does not affect custom streams set for testing.
    """
    global _PYVIDER_LOG_STREAM
    if _PYVIDER_LOG_STREAM is sys.stdout:
        _PYVIDER_LOG_STREAM = sys.stderr


def _create_failsafe_handler() -> stdlib_logging.Handler:
    """
    Creates a standard library logging `StreamHandler` for failsafe logging.

    This handler is configured to output to `sys.stderr` with a basic format,
    prefixed by "[Pyvider Failsafe]". It serves as a last resort if more complex
    `structlog` configurations fail, ensuring that critical errors during setup
    can still be reported.

    Returns:
        stdlib_logging.Handler: A configured `StreamHandler` instance.
    """
    handler = stdlib_logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        stdlib_logging.Formatter("[Pyvider Failsafe] %(levelname)s: %(message)s")
    )
    return handler


def _create_core_setup_logger(globally_disabled: bool = False) -> stdlib_logging.Logger:
    """
    Creates or retrieves and configures the internal logger for setup diagnostics.

    This logger (`pyvider.telemetry.core_setup`) is used by the telemetry system
    itself to log messages about its own configuration and setup process (e.g.,
    which formatter is chosen, if setup is disabled). It uses the standard
    library `logging` to avoid circular dependencies with `structlog` during
    initialization.

    Handlers are reconfigured to point to the current `sys.stderr`.

    Args:
        globally_disabled (bool): If True, a `NullHandler` is added, effectively
            suppressing setup log output. Defaults to False.

    Returns:
        stdlib_logging.Logger: The configured logger instance for setup messages.
    """
    logger = stdlib_logging.getLogger(_CORE_SETUP_LOGGER_NAME)

    # Ensure handlers are (re)configured to use the current stderr
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            # Ensure 'h' is a StreamHandler and has a 'stream' attribute before accessing it.
            if isinstance(h, stdlib_logging.StreamHandler) and \
               h.stream not in (sys.stdout, sys.stderr, _PYVIDER_LOG_STREAM):
                h.close()
        except Exception: # nosec B110 # Broad exception catch for robustness in cleanup
            pass # Continue cleanup even if one handler fails

    # Configure new handler
    handler: stdlib_logging.Handler
    if globally_disabled:
        handler = stdlib_logging.NullHandler()
    else:
        # Always use stderr for this stdlib logger
        handler = stdlib_logging.StreamHandler(sys.stderr)
        formatter = stdlib_logging.Formatter(
            "[Pyvider Setup] %(levelname)s (%(name)s): %(message)s"
        )
        handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Set log level from environment with fallback
    level_str = os.getenv("PYVIDER_CORE_SETUP_LOG_LEVEL", "INFO").upper()
    level = getattr(stdlib_logging, level_str, stdlib_logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    return logger


# Global setup logger
_core_setup_logger = _create_core_setup_logger()


def _build_complete_processor_chain(config: TelemetryConfig) -> list[Any]:
    """
    Constructs the full list of `structlog` processors based on the configuration.

    This function combines core processors (for context, level filtering,
    timestamps, service name, emojis) with formatter-specific processors
    (JSON or key-value console renderer). The order of processors is critical
    for correct log event processing.

    Args:
        config (TelemetryConfig): The active telemetry configuration object.

    Returns:
        list[Any]: A list of `structlog` processor instances, ordered for execution.
            The `Any` type reflects that `ConsoleRenderer` might not strictly
            conform to `StructlogProcessor` protocol in all type systems.
    """
    # Get core processors from config.py
    core_processors = _build_core_processors_list(config)

    output_stream = _PYVIDER_LOG_STREAM

    # Get formatter processors from config.py
    formatter_processors = _build_formatter_processors_list(config.logging, output_stream)

    # Log the choice of formatter
    if config.logging.console_formatter == "json":
        _core_setup_logger.info("📝➡️🎨 Configured JSON renderer.")
    elif config.logging.console_formatter == "key_value":
        _core_setup_logger.info("📝➡️🎨 Configured Key-Value (ConsoleRenderer).")
    else:
        _core_setup_logger.warning(
            f"Unknown formatter '{config.logging.console_formatter}' was processed. "
            "Defaulted to key-value. This indicates a potential issue in config validation."
        )

    # Combine core and formatter processors
    # The return type of _build_formatter_processors_list can be list[Any] due to ConsoleRenderer.
    # Concatenating list[StructlogProcessor] with list[Any] results in list[Any].
    return cast(list[Any], core_processors + formatter_processors) # Added cast for no-any-return


def _apply_structlog_configuration(processors: list[Any]) -> None:
    """
    Applies the generated processor chain and other settings to `structlog`.

    This configures `structlog` globally with the specified processors,
    output stream (via `PrintLoggerFactory`), and wrapper class.

    Args:
        processors (list[Any]): The complete, ordered list of `structlog`
            processors to be used.
    """
    output_stream = _PYVIDER_LOG_STREAM

    # Configure structlog with our processor chain
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=output_stream),
        wrapper_class=cast(type[BindableLogger], structlog.BoundLogger),
        cache_logger_on_first_use=True,
    )

    stream_name = 'sys.stderr' if output_stream == sys.stderr else 'custom stream (testing)'
    _core_setup_logger.info(
        f"📝➡️✅ structlog configured. Wrapper: BoundLogger. Output: {stream_name}."
    )


def _configure_structlog_output(config: TelemetryConfig) -> None:
    """
    Orchestrates the configuration of `structlog` output.

    This involves building the complete processor chain based on the provided
    `TelemetryConfig` and then applying this configuration to `structlog`.

    Args:
        config (TelemetryConfig): The telemetry configuration to apply.
    """
    processors = _build_complete_processor_chain(config)
    _apply_structlog_configuration(processors)


def _handle_globally_disabled_setup() -> None:
    """
    Configures `structlog` for a globally disabled state.

    When telemetry is globally disabled (via `TelemetryConfig.globally_disabled`),
    this function configures `structlog` with an empty processor list and
    `ReturnLoggerFactory`. This effectively makes all logging calls no-ops,
    minimizing performance overhead. It also logs a message via the internal
    setup logger indicating that telemetry is disabled.
    """
    # Create temporary logger for disabled message
    temp_logger_name = f"{_CORE_SETUP_LOGGER_NAME}_temp_disabled_msg"
    temp_logger = stdlib_logging.getLogger(temp_logger_name)

    # Check if we need to configure this temporary logger
    needs_configuration = (
        not temp_logger.handlers or
        not any(
            isinstance(h, stdlib_logging.StreamHandler) and h.stream == sys.stderr
            for h in temp_logger.handlers
        )
    )

    if needs_configuration:
        # Clear and reconfigure
        for h in list(temp_logger.handlers):
            temp_logger.removeHandler(h)

        temp_handler = stdlib_logging.StreamHandler(sys.stderr)
        temp_formatter = stdlib_logging.Formatter(
            "[Pyvider Setup] %(levelname)s (%(name)s): %(message)s"
        )
        temp_handler.setFormatter(temp_formatter)
        temp_logger.addHandler(temp_handler)
        temp_logger.setLevel(stdlib_logging.INFO)
        temp_logger.propagate = False

    temp_logger.info("⚙️➡️🚫 Pyvider telemetry globally disabled.")

    # Configure minimal structlog setup to avoid errors
    structlog.configure(
        processors=[],
        logger_factory=structlog.ReturnLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def reset_pyvider_setup_for_testing() -> None:
    """
    Resets `structlog` defaults and Pyvider Telemetry's internal logger state.

    This utility function is crucial for ensuring that tests run in isolation.
    It clears any existing `structlog` configuration, resets the lazy
    initialization state flags used by `PyviderLogger`, sets the global log
    stream back to `sys.stderr`, and re-initializes the internal setup logger.

    Warning:
        This should only be used in testing environments.
    """
    global _PYVIDER_LOG_STREAM, _core_setup_logger, _EXPLICIT_SETUP_DONE

    with _PYVIDER_SETUP_LOCK:
        # Reset structlog
        structlog.reset_defaults()

        # Reset logger state
        logger_base_module.logger._is_configured_by_setup = False
        logger_base_module.logger._active_config = None

        # Reset lazy setup state
        logger_base_module._LAZY_SETUP_STATE["done"] = False
        logger_base_module._LAZY_SETUP_STATE["error"] = None
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = False

        # Reset stream and setup flags
        _PYVIDER_LOG_STREAM = sys.stderr
        _EXPLICIT_SETUP_DONE = False
        _core_setup_logger = _create_core_setup_logger()


def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Initializes or reconfigures the Pyvider Telemetry (and `structlog`) system.

    This is the primary entry point for explicitly configuring logging. It handles
    both initial setup and reconfiguration if called again. The configuration
    is derived from the provided `TelemetryConfig` object or by parsing
    environment variables if `config` is `None`.

    The setup process involves:
    1. Ensuring the default log stream is `sys.stderr`.
    2. Resetting any existing `structlog` and internal Pyvider Telemetry states
       to ensure a clean configuration, coordinating with the lazy initialization
       mechanism in `PyviderLogger`.
    3. Loading the `TelemetryConfig` (from argument or environment).
    4. Configuring the internal setup logger used for diagnostics during this process.
    5. Applying the main `structlog` configuration based on whether telemetry
       is globally disabled or not. This includes setting up the processor chain.
    6. Updating global state flags to indicate that explicit setup has completed,
       which also influences the behavior of subsequent lazy initialization attempts.

    Args:
        config (TelemetryConfig | None, optional): A `TelemetryConfig` instance
            containing the desired settings. If `None` (the default), configuration
            will be loaded from environment variables via `TelemetryConfig.from_env()`.
    """
    global _PYVIDER_LOG_STREAM, _core_setup_logger, _EXPLICIT_SETUP_DONE

    with _PYVIDER_SETUP_LOCK:
        # Ensure stderr default
        _ensure_stderr_default()

        # Reset state for clean initialization
        structlog.reset_defaults()
        logger_base_module.logger._is_configured_by_setup = False
        logger_base_module.logger._active_config = None

        # Reset lazy setup state since we're doing explicit setup
        logger_base_module._LAZY_SETUP_STATE["done"] = False
        logger_base_module._LAZY_SETUP_STATE["error"] = None
        logger_base_module._LAZY_SETUP_STATE["in_progress"] = False

        # Load configuration
        current_config = config if config is not None else TelemetryConfig.from_env()

        # Create core setup logger
        _core_setup_logger = _create_core_setup_logger(
            globally_disabled=current_config.globally_disabled
        )

        # Log setup start (unless globally disabled)
        if not current_config.globally_disabled:
            _core_setup_logger.info("⚙️➡️🚀 Starting Pyvider (structlog) explicit setup...")

        # Configure based on disabled state
        if current_config.globally_disabled:
            _handle_globally_disabled_setup()
        else:
            _configure_structlog_output(current_config)

        # Mark as properly configured - FIXED: Set both explicit and lazy flags
        logger_base_module.logger._is_configured_by_setup = True
        logger_base_module.logger._active_config = current_config
        _EXPLICIT_SETUP_DONE = True

        # Also mark lazy setup as done to prevent future lazy initialization
        logger_base_module._LAZY_SETUP_STATE["done"] = True # Explicit setup implies lazy setup is also "done"

        if not current_config.globally_disabled:
            _core_setup_logger.info("⚙️➡️✅ Pyvider (structlog) explicit setup completed.")


async def shutdown_pyvider_telemetry(timeout_millis: int = 5000) -> None:
    """
    Performs graceful shutdown procedures for the Pyvider Telemetry system.

    Currently, this function logs a shutdown message. In the future, it could be
    extended to include flushing buffered log entries, closing remote connections
    for telemetry export, or other cleanup tasks required for specific processors
    or configurations.

    Args:
        timeout_millis (int): The timeout in milliseconds to wait for shutdown
            operations to complete. (Currently unused but reserved for future use,
            e.g., with asynchronous processors that require flushing).
    """
    _core_setup_logger.info("🔌➡️🏁 Pyvider telemetry shutdown called.")

# 🐍🛠️
