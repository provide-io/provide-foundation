#
# base.py
#
"""
Pyvider Telemetry Base Logger Implementation.

This module defines the `PyviderLogger` class, which is the central component
providing the logging interface for the `pyvider-telemetry` library. It is
built on top of `structlog` and offers a consistent logging experience.

Key features of `PyviderLogger`:
- Lazy Initialization: The logging system (including `structlog` configuration)
  is initialized automatically on the first logging call if explicit setup
  via `pyvider.telemetry.core.setup_telemetry()` has not already occurred.
  This ensures that logging works "out-of-the-box" with sensible defaults.
- Thread Safety: The lazy initialization process is thread-safe to prevent
  race conditions in multi-threaded applications.
- Standard Logging Methods: Provides familiar logging methods such as `info()`,
  `debug()`, `warning()`, `error()`, `exception()`, `critical()`, and a custom
  `trace()` method for highly verbose output.
- Argument Formatting: Supports printf-style argument formatting for log messages,
  with robust fallback behavior for incorrect format strings or argument counts.
- Configuration Awareness: Internally manages its configuration state, respecting
  both explicit setup and lazy-initialized default configurations.
- Emergency Fallback: Includes mechanisms to fall back to a basic, failsafe
  logging configuration if the primary setup process encounters critical errors,
  ensuring that logging calls do not crash the application.

A global instance of `PyviderLogger` is instantiated as `logger` at the end
of this module, which is then typically re-exported by
`pyvider.telemetry.logger` and `pyvider.telemetry` for easy application-wide access.
"""

import contextlib  # For suppress
import sys
import threading
from typing import TYPE_CHECKING, Any, TextIO, cast

import structlog
from structlog.types import BindableLogger

from pyvider.telemetry.types import TRACE_LEVEL_NAME

if TYPE_CHECKING:
    from pyvider.telemetry.config import TelemetryConfig

# Global state for lazy initialization
_LAZY_SETUP_LOCK = threading.Lock()
_LAZY_SETUP_STATE: dict[str, Any] = { # Explicitly type the dict
    "done": False,
    "error": None,  # Can store Exception instance or None
    "in_progress": False, # Track setup in progress to prevent recursion
}


def _get_safe_stderr() -> TextIO:
    """
    Returns a safe fallback TextIO stream, defaulting to `sys.stderr`.

    If `sys.stderr` is `None` or unavailable, an `io.StringIO` instance is
    returned as a memory-based fallback. This ensures that logging components
    attempting to write to an error stream always have a valid stream object.

    Returns:
        TextIO: A writable text stream.
    """
    if hasattr(sys, 'stderr') and sys.stderr is not None:
        return sys.stderr
    else:
        # Fallback: create a no-op stream if stderr is not available
        import io
        return io.StringIO()


class PyviderLogger:
    """
    A `structlog`-based logger providing a standardized logging interface.

    This class offers automatic lazy initialization of the logging system if it
    hasn't been explicitly configured via `setup_telemetry()`. It ensures
    thread-safe configuration and provides familiar logging methods (`info`,
    `debug`, `error`, etc.), including a custom `trace` level.

    Key Features:
        - Lazy initialization: Logging works immediately with default settings.
        - Thread-safe: Safe for use in multi-threaded applications.
        - Standard logging methods: `debug()`, `info()`, `warning()`, `error()`,
          `exception()`, `critical()`, and custom `trace()`.
        - Printf-style formatting: Supports `msg % args` style formatting for messages.
        - Structured logging: Allows passing arbitrary `**kwargs` for structured data.
        - `get_logger()`: Method to obtain named logger instances.

    An instance of this class is typically available as `pyvider.telemetry.logger`.
    """

    def __init__(self) -> None:
        """
        Initializes the PyviderLogger.

        The actual `structlog` configuration is deferred until the first logging
        call or an explicit `setup_telemetry()` call, enabling lazy initialization.
        Binds the initial internal logger to the class's module and name.
        """
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None

    def _check_structlog_already_disabled(self) -> bool:
        """
        Checks if `structlog` is already configured with `ReturnLoggerFactory`.

        This state indicates that logging is effectively disabled (all logging
        calls become no-ops). If detected, updates the lazy setup state to
        reflect that setup is "done" to prevent further lazy initialization attempts.

        Returns:
            bool: True if `structlog` is configured with `ReturnLoggerFactory`,
                  False otherwise or if an error occurs checking the configuration.
        """
        global _LAZY_SETUP_STATE
        try:
            current_config = structlog.get_config()
            logger_factory = current_config.get('logger_factory')
            is_return_logger_factory = isinstance(logger_factory, structlog.ReturnLoggerFactory)

            if current_config and is_return_logger_factory:
                with _LAZY_SETUP_LOCK: # Still need lock for state modification
                    _LAZY_SETUP_STATE["done"] = True
                    _LAZY_SETUP_STATE["error"] = None
                return True  # Structlog is already configured as disabled
        except Exception:  # nosec B110 # Broad exception if get_config fails for any reason
            pass # Allow to proceed to full lazy setup
        return False

    def _locked_lazy_setup(self) -> None:
        """
        Performs the core lazy setup logic, protected by `_LAZY_SETUP_LOCK`.

        This method re-verifies the setup state after acquiring the lock to handle
        concurrent calls correctly. It then marks setup as "in_progress", calls
        `_perform_lazy_setup()`, and updates the state based on success or failure.
        If setup fails, it invokes `_setup_emergency_fallback()`.
        """
        global _LAZY_SETUP_STATE
        # Double-check states after acquiring lock
        if self._is_configured_by_setup:
            return
        if _LAZY_SETUP_STATE["done"] and _LAZY_SETUP_STATE["error"] is None:
            return
        if _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"] is not None:
            self._setup_emergency_fallback()
            return

        _LAZY_SETUP_STATE["in_progress"] = True
        try:
            self._perform_lazy_setup()
            _LAZY_SETUP_STATE["done"] = True
            _LAZY_SETUP_STATE["error"] = None
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            _LAZY_SETUP_STATE["done"] = False
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def _ensure_configured(self) -> None:
        """
        Ensures the logging system is configured before any log operation.

        This method implements the core lazy initialization logic. It first checks
        for several fast-path exit conditions (already configured, setup in progress,
        previous error, or structlog already disabled). If none apply, it acquires
        a lock and performs the lazy setup via `_locked_lazy_setup()`.
        This method is thread-safe and idempotent.

        Raises:
            Exception: Propagates exceptions from `_perform_lazy_setup()` if lazy
                       setup fails and no explicit setup was done, though typically
                       `_locked_lazy_setup` handles this by calling `_setup_emergency_fallback`.
        """
        global _LAZY_SETUP_STATE

        # Pre-lock checks for early exit
        if self._is_configured_by_setup:
            return
        if _LAZY_SETUP_STATE["done"] and _LAZY_SETUP_STATE["error"] is None:
            return
        # If setup is already in progress or previously failed, use emergency fallback
        if _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"] is not None:
            self._setup_emergency_fallback()
            return

        # Check if structlog is already effectively disabled
        if self._check_structlog_already_disabled():
            return

        # Slow path: need to perform lazy setup under lock
        with _LAZY_SETUP_LOCK:
            self._locked_lazy_setup()

    def _perform_lazy_setup(self) -> None:
        """
        Executes the actual lazy setup of `structlog` using default or environment-based config.

        This method is called by `_ensure_configured` (under lock) when no prior
        explicit `setup_telemetry()` call has been made. It loads configuration
        via `TelemetryConfig.from_env()` and then applies it using helper functions
        from `pyvider.telemetry.core`. If `TelemetryConfig.from_env()` fails, it
        falls back to a minimal, safe default configuration.

        Raises:
            Exception: Can propagate exceptions from `TelemetryConfig.from_env()` or
                       `_configure_structlog_output()` if they occur, which are then
                       handled by `_locked_lazy_setup()`.
        """
        # Import here to avoid circular imports
        from pyvider.telemetry.config import (
            TelemetryConfig,
        )
        from pyvider.telemetry.core import (
            _configure_structlog_output,
        )

        # NOTE: Do NOT reset stream here - preserve any custom stream set for testing
        # The _ensure_stderr_default() call in core setup will handle stderr enforcement

        # Create default config from environment with fallbacks
        try:
            default_config = TelemetryConfig.from_env()
        except Exception:
            # If environment config fails, use minimal safe defaults
            from pyvider.telemetry.config import (
                LoggingConfig,
            )
            default_config = TelemetryConfig(
                service_name=None,
                logging=LoggingConfig(
                    default_level="DEBUG",  # Match test expectations
                    console_formatter="key_value",
                    logger_name_emoji_prefix_enabled=True,
                    das_emoji_prefix_enabled=True,
                    omit_timestamp=False,
                ),
                globally_disabled=False,
            )

        # Configure structlog if not globally disabled
        if not default_config.globally_disabled:
            _configure_structlog_output(default_config)
        else:
            self._handle_globally_disabled_lazy_setup()

        # Store config but don't mark as setup_telemetry configured
        self._active_config = default_config

    def _handle_globally_disabled_lazy_setup(self) -> None:
        """
        Configures `structlog` for a globally disabled state during lazy setup.

        This sets up `structlog` with minimal processors and `ReturnLoggerFactory`
        to ensure logging calls are inexpensive no-ops when telemetry is disabled.
        """
        structlog.configure(
            processors=[],
            logger_factory=structlog.ReturnLoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def _setup_emergency_fallback(self) -> None:
        """
        Sets up an emergency, failsafe logging configuration for `structlog`.

        This method is invoked if the primary lazy initialization process fails
        or if re-entrant logging calls occur during setup. It configures `structlog`
        with a basic `ConsoleRenderer` to `sys.stderr` or, as a last resort,
        `ReturnLoggerFactory` to prevent crashes. This ensures that subsequent
        logging attempts do not raise further errors.
        """
        try:
            # Configure minimal structlog setup that always works
            structlog.configure(
                processors=[
                    # Use minimal processors that are guaranteed to exist
                    structlog.dev.ConsoleRenderer(colors=False),
                ],
                logger_factory=structlog.PrintLoggerFactory(file=_get_safe_stderr()),
                wrapper_class=cast(type[BindableLogger], structlog.BoundLogger),
                cache_logger_on_first_use=True,
            )
        except Exception:
            # If even minimal structlog config fails, fall back to ReturnLogger
            with contextlib.suppress(Exception): # SIM105 applied
                structlog.configure(
                    processors=[],
                    logger_factory=structlog.ReturnLoggerFactory(),
                    cache_logger_on_first_use=True,
                )
                # If this also fails, logging calls will fail silently (original behavior)

    def get_logger(self, name: str | None = None) -> Any:
        """
        Retrieves a `structlog` bound logger, ensuring configuration first.

        If `name` is provided, the logger will be bound with `logger_name=name`.
        If `name` is `None`, it defaults to "pyvider.default". This method
        ensures that the logging system is initialized (either explicitly or
        lazily) before returning a logger.

        Args:
            name (str | None, optional): The desired name for the logger.
                Defaults to "pyvider.default".

        Returns:
            Any: A `structlog.BoundLogger` instance (typed as `Any` due to
                 `structlog`'s dynamic nature, but functionally a BoundLogger).
        """
        self._ensure_configured()
        effective_name: str = name if name is not None else "pyvider.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def _log_with_level(self, level_method_name: str, event: str, **kwargs: Any) -> None:
        """
        Internal helper to dispatch a log call after ensuring configuration.

        It retrieves a dynamically named logger ("pyvider.dynamic_call") and
        calls the specified logging method (e.g., "info", "debug") on it.

        Args:
            level_method_name (str): The name of the `structlog` logging method
                to call (e.g., "info", "error").
            event (str): The primary log message.
            **kwargs (Any): Additional key-value pairs for structured logging.
        """
        self._ensure_configured()
        log = self.get_logger("pyvider.dynamic_call")
        method_to_call = getattr(log, level_method_name)
        method_to_call(event, **kwargs)

    def _format_message_with_args(self, event: str | Any, args: tuple[Any, ...]) -> str:
        """
        Safely formats a log message with printf-style arguments if provided.

        If `args` are present, it attempts to format `event` using the `%` operator.
        If formatting fails (e.g., due to incorrect format string or argument
        mismatch), it falls back to concatenating the string representation of
        `event` and all `args`. If `event` is not a string, it's first converted
        to one.

        Args:
            event (str | Any): The log event, typically a format string.
            args (tuple[Any, ...]): Arguments for printf-style formatting.

        Returns:
            str: The formatted log message, or a fallback representation.
        """
        # FIXED: Handle non-string events gracefully
        event_str = str(event) if event is not None else ""

        if not args:
            return event_str

        try:
            return event_str % args
        except (TypeError, ValueError, KeyError):
            # Fallback: append args as space-separated values
            args_str = ' '.join(str(arg) for arg in args)
            return f"{event_str} {args_str}"

    def trace(self, event: str, *args: Any, _pyvider_logger_name: str | None = None, **kwargs: Any) -> None:
        """
        Logs a message with TRACE level (the most verbose).

        This is a custom log level, typically used for extremely detailed
        diagnostic information.

        Args:
            event (str): The log message. Can be a printf-style format string if
                `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            _pyvider_logger_name (str | None, optional): Internal parameter to override
                the logger name for this specific call. Defaults to
                "pyvider.dynamic_call_trace".
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        self._ensure_configured()
        formatted_event = self._format_message_with_args(event, args)

        logger_name_for_call = _pyvider_logger_name if _pyvider_logger_name is not None else "pyvider.dynamic_call_trace"
        log = structlog.get_logger().bind(logger_name=logger_name_for_call)

        event_kwargs = kwargs.copy()
        event_kwargs["_pyvider_level_hint"] = TRACE_LEVEL_NAME.lower()
        log.msg(formatted_event, **event_kwargs)

    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with DEBUG level.

        Used for detailed information, typically of interest only when
        diagnosing problems.

        Args:
            event (str): The log message. Can be a printf-style format string if
                `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with INFO level.

        Used for general operational information, confirming that things are
        working as expected.

        Args:
            event (str): The log message. Can be a printf-style format string if
                `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with WARNING level.

        Used for an indication that something unexpected happened, or that some
        problem might occur in the near future (e.g., `disk space low`).
        The software is still working as expected.

        Args:
            event (str): The log message. Can be a printf-style format string if
                `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    warn = warning  # Alias for warning, common in some logging frameworks.

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with ERROR level.

        Used due to a more serious problem, the software has not been able
        to perform some function.

        Args:
            event (str): The log message. Can be a printf-style format string if
                `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with ERROR level and automatically includes exception information.

        This method should be called from an exception handler. It behaves like
        `error()` but adds exception details (traceback) to the log output.

        Args:
            event (str): The log message describing the context of the error.
                Can be a printf-style format string if `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
                `exc_info=True` is automatically added if not provided.
        """
        formatted_event = self._format_message_with_args(event, args)
        kwargs.setdefault('exc_info', True)
        self._log_with_level("error", formatted_event, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Logs a message with CRITICAL level.

        Used for a very serious error, indicating that the program itself may be
        unable to continue running.

        Args:
            event (str): The log message describing the critical failure.
                Can be a printf-style format string if `args` are provided.
            *args (Any): Arguments for printf-style formatting of `event`.
            **kwargs (Any): Additional key-value data to include in the structured log.
        """
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Custom attribute setter to protect internal state if needed.

        Currently, this allows setting any attribute but could be used to
        make certain attributes read-only or trigger actions on change.

        Args:
            name (str): The attribute name being set.
            value (Any): The value to assign to the attribute.
        """
        if name in ("_internal_logger", "_is_configured_by_setup", "_active_config"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


# Global singleton instance
logger: PyviderLogger = PyviderLogger()

# 🐍📖
