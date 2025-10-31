#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# core.py
#
import contextlib
from typing import TYPE_CHECKING, Any

import structlog

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.logger.types import TRACE_LEVEL_NAME

"""Core FoundationLogger implementation.
Contains the main logging class with all logging methods.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig

_LAZY_SETUP_STATE: dict[str, Any] = {"done": False, "error": None, "in_progress": False}


class FoundationLogger:
    """A `structlog`-based logger providing a standardized logging interface."""

    def __init__(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def setup(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def _check_structlog_already_disabled(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def _try_hub_configuration(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return False

        try:
            # Use the injected hub instance to get config
            config = self._hub.get_foundation_config()
            if config and not self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def _should_use_emergency_fallback(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"]

    def _perform_locked_setup(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def _ensure_configured(self) -> None:
        """Ensures the logger is configured, performing lazy setup if necessary.
        Uses Hub for configuration when available, falls back to lazy setup.
        This method is thread-safe and handles setup failures gracefully.
        """
        # Fast path for already configured loggers.
        if self._is_configured_by_setup:
            return

        # If we have a Hub, try to get configuration from it
        if self._try_hub_configuration():
            return

        # Check if setup is already done
        if _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]:
            return

        # If setup is in progress by another thread, or failed previously, use fallback.
        if self._should_use_emergency_fallback():
            self._setup_emergency_fallback()
            return

        # If structlog is already configured to be a no-op, we're done.
        if self._check_structlog_already_disabled():
            return

        # Acquire lock to perform setup.
        try:
            with get_lock_manager().acquire("foundation.logger.lazy"):
                self._perform_locked_setup()
        except Exception:
            # If lock acquisition fails (e.g., due to ordering violations), use emergency fallback
            self._setup_emergency_fallback()

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
        effective_name = name if name is not None else "foundation.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def _log_with_level(self, level_method_name: str, event: str, **kwargs: Any) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
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
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def unbind(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def try_unbind(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to prevent accidental modification of logger state."""
        if hasattr(self, name) and name.startswith("_"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


# Global logger function - gets logger through Hub
def get_global_logger() -> FoundationLogger:
    """Get the global FoundationLogger instance through Hub.

    This function acts as the Composition Root for the global logger instance,
    maintained for backward compatibility.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to inject a logger instance via a `Container`. This global
    accessor should be avoided in new application code.

    Returns:
        FoundationLogger instance from Hub

    """
    from provide.foundation.hub.manager import get_hub

    hub = get_hub()
    logger_instance = hub._component_registry.get("foundation.logger.instance", "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


class GlobalLoggerProxy:
    """Proxy object that forwards all attribute access to Hub-based logger."""

    def __getattr__(self, name: str) -> Any:
        return getattr(get_global_logger(), name)

    # Forward common logger methods to help mypy
    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(event, *args, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(event, *args, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(event, *args, **kwargs)

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(event, *args, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(event, *args, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(event, *args, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow tests to set internal state on the underlying logger."""
        if name.startswith("_"):
            # For internal attributes, set them on the actual logger instance
            logger = get_global_logger()
            setattr(logger, name, value)
        else:
            super().__setattr__(name, value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return get_global_logger().get_logger(*args, **kwargs)


# Global logger instance (now a proxy)
logger = GlobalLoggerProxy()

# 🧱🏗️🔚
