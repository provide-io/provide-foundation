#
# core.py
#
"""
Core FoundationLogger implementation.
Contains the main logging class with all logging methods.
"""

import contextlib
import threading
from typing import TYPE_CHECKING, Any

import structlog

from provide.foundation.types import TRACE_LEVEL_NAME

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig

_LAZY_SETUP_LOCK = threading.Lock()
_LAZY_SETUP_STATE: dict[str, Any] = {"done": False, "error": None, "in_progress": False}


class FoundationLogger:
    """A `structlog`-based logger providing a standardized logging interface."""

    def __init__(self) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None

    def _check_structlog_already_disabled(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"), structlog.ReturnLoggerFactory
            ):
                with _LAZY_SETUP_LOCK:
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            pass
        return False

    def _ensure_configured(self) -> None:
        """
        Ensures the logger is configured, performing lazy setup if necessary.
        This method is thread-safe and handles setup failures gracefully.
        """
        # Fast path for already configured loggers.
        if self._is_configured_by_setup or (
            _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]
        ):
            return

        # If setup is in progress by another thread, or failed previously, use fallback.
        if _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If structlog is already configured to be a no-op, we're done.
        if self._check_structlog_already_disabled():
            return

        # Acquire lock to perform setup.
        with _LAZY_SETUP_LOCK:
            # Double-check state after acquiring lock, as another thread might have finished.
            if self._is_configured_by_setup or (
                _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]
            ):
                return

            # If error was set while waiting for lock, use fallback.
            if _LAZY_SETUP_STATE["error"]:
                self._setup_emergency_fallback()
                return

            # If still needs setup, perform lazy setup.
            if not _LAZY_SETUP_STATE["done"]:
                self._perform_lazy_setup()

    def _perform_lazy_setup(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def _setup_emergency_fallback(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def get_logger(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "pyvider.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def _log_with_level(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "pyvider.dynamic_call")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def _format_message_with_args(self, event: str | Any, args: tuple[Any, ...]) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(event) % args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(event)

    def trace(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    warn = warning  # Alias for compatibility

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def bind(self, **kwargs: Any) -> Any:
        """
        Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context
        """
        self._ensure_configured()
        log = self.get_logger("pyvider.context_bind")
        return log.bind(**kwargs)

    def unbind(self, *keys: str) -> Any:
        """
        Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys
        """
        self._ensure_configured()
        log = self.get_logger("pyvider.context_unbind")
        return log.unbind(*keys)

    def try_unbind(self, *keys: str) -> Any:
        """
        Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys
        """
        self._ensure_configured()
        log = self.get_logger("pyvider.context_try_unbind")
        return log.try_unbind(*keys)

    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to prevent accidental modification of logger state."""
        if hasattr(self, name) and name.startswith("_"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


# Global logger instance
logger: FoundationLogger = FoundationLogger()
