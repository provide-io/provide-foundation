#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import functools
import inspect
from typing import Any, TypeVar

from provide.foundation.hub.foundation import get_foundation_logger

"""Safe error decorators that preserve original behavior."""

F = TypeVar("F", bound=Callable[..., Any])


def _get_func_name(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", "<anonymous>")


def _log_function_entry(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def _log_function_success(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def _log_function_error(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def log_only_error_context(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "debug",
    log_success: bool = False,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator


# 🧱🏗️🔚
