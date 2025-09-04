#
# base.py
#
"""
Foundation Telemetry Base Logger Implementation.
Defines FoundationLogger with lazy initialization, thread safety, and standard logging methods.
"""

import contextlib
import io
import logging
import sys
import threading
from typing import TYPE_CHECKING, Any, TextIO, cast

import structlog
from structlog.types import BindableLogger

from provide.foundation.types import TRACE_LEVEL_NAME

if TYPE_CHECKING:
    from provide.foundation.core import ResolvedEmojiConfig
    from provide.foundation.logger.config import TelemetryConfig

_LAZY_SETUP_LOCK = threading.Lock()
_LAZY_SETUP_STATE: dict[str, Any] = {"done": False, "error": None, "in_progress": False}


def _get_safe_stderr() -> TextIO:
    return (
        sys.stderr
        if hasattr(sys, "stderr") and sys.stderr is not None
        else io.StringIO()
    )


class FoundationLogger:
    """A `structlog`-based logger providing a standardized logging interface."""

    def __init__(self) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._active_resolved_emoji_config: ResolvedEmojiConfig | None = None

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
                return  # pragma: no cover - TODO: Requires complex threading test to simulate race condition

            # If setup failed while waiting for the lock, use fallback.
            if _LAZY_SETUP_STATE["error"]:
                self._setup_emergency_fallback()
                return

            # Mark as in progress and perform setup.
            _LAZY_SETUP_STATE["in_progress"] = True
            try:
                self._perform_lazy_setup()
            except Exception as e:
                _LAZY_SETUP_STATE["error"] = e
                _LAZY_SETUP_STATE["done"] = False
                self._setup_emergency_fallback()
            finally:
                _LAZY_SETUP_STATE["in_progress"] = False

    def _perform_lazy_setup(self) -> None:
        """
        Executes lazy setup by calling the main internal setup function.
        """
        from provide.foundation.core import _internal_setup

        # Calling _internal_setup with no config will make it use from_env()
        # and is_explicit_call=False will be used.
        _internal_setup(config=None, is_explicit_call=False)

    def _setup_emergency_fallback(self) -> None:
        try:
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer(colors=False)],
                logger_factory=structlog.PrintLoggerFactory(file=_get_safe_stderr()),
                wrapper_class=cast(type[BindableLogger], structlog.BoundLogger),
                cache_logger_on_first_use=True,
            )
        except Exception:
            with contextlib.suppress(Exception):
                structlog.configure(
                    processors=[],
                    logger_factory=structlog.ReturnLoggerFactory(),
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
        log = self.get_logger("pyvider.dynamic_call")
        getattr(log, level_method_name)(event, **kwargs)

    def _format_message_with_args(self, event: str | Any, args: tuple[Any, ...]) -> str:
        event_str = str(event) if event is not None else ""
        if not args:
            return event_str
        try:
            return event_str % args
        except (TypeError, ValueError, KeyError):
            return f"{event_str} {' '.join(str(arg) for arg in args)}"

    def trace(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._ensure_configured()
        formatted_event = self._format_message_with_args(event, args)
        logger_name = _foundation_logger_name or "pyvider.dynamic_call_trace"
        log = self.get_logger(logger_name)
        kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
        log.msg(formatted_event, **kwargs)

    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        self._log_with_level(
            "debug", self._format_message_with_args(event, args), **kwargs
        )

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        self._log_with_level(
            "info", self._format_message_with_args(event, args), **kwargs
        )

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        self._log_with_level(
            "warning", self._format_message_with_args(event, args), **kwargs
        )

    warn = warning

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        self._log_with_level(
            "error", self._format_message_with_args(event, args), **kwargs
        )

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("exc_info", True)
        self._log_with_level(
            "error", self._format_message_with_args(event, args), **kwargs
        )

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        self._log_with_level(
            "critical", self._format_message_with_args(event, args), **kwargs
        )

    def bind(self, **kwargs: Any) -> Any:
        """
        Create a new logger with additional context.
        
        This is a pass-through to structlog's bind() method,
        providing a consistent API with get_logger().
        
        Args:
            **kwargs: Key-value pairs to bind to the logger context
            
        Returns:
            A new logger instance with the bound context
        """
        self._ensure_configured()
        return self.get_logger().bind(**kwargs)
    
    def unbind(self, *keys: str) -> Any:
        """
        Remove keys from the logger context.
        
        This is a pass-through to structlog's unbind() method.
        
        Args:
            *keys: Keys to remove from the context
            
        Returns:
            A new logger instance with the keys removed
        """
        self._ensure_configured()
        return self.get_logger().unbind(*keys)
    
    def try_unbind(self, *keys: str) -> Any:
        """
        Try to remove keys from the logger context (won't fail if key doesn't exist).
        
        This is a pass-through to structlog's try_unbind() method.
        
        Args:
            *keys: Keys to try to remove from the context
            
        Returns:
            A new logger instance with the keys removed (if they existed)
        """
        self._ensure_configured()
        return self.get_logger().try_unbind(*keys)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)


logger: FoundationLogger = FoundationLogger()


def get_logger(name: str | None = None) -> Any:
    """
    Get a logger instance with the given name.

    This is a convenience function that uses the global FoundationLogger.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance
    """
    return logger.get_logger(name)


def setup_logging(
    level: str | int = "INFO",
    json_logs: bool = False,
    log_file: str | None = None,
    **kwargs,
) -> None:
    """
    Setup logging configuration.

    This is a convenience function for basic logging setup.
    For more control, use setup_telemetry() from foundation.core.

    Args:
        level: Log level (string or int)
        json_logs: Whether to output logs as JSON
        log_file: Optional file path to write logs
        **kwargs: Additional configuration options
    """
    from provide.foundation.core import setup_telemetry
    from provide.foundation.logger.config import LoggingConfig, TelemetryConfig
    from provide.foundation.types import LogLevelStr

    logging_config = LoggingConfig(
        default_level=cast(LogLevelStr, level if isinstance(level, str) else logging.getLevelName(level)),
        console_formatter="json" if json_logs else "key_value",
    )
    config = TelemetryConfig(logging=logging_config)

    setup_telemetry(config)
