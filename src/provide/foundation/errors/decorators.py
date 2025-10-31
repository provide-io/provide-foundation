#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import functools
import inspect
from typing import Any, Protocol, TypeVar, overload

"""Decorators for error handling and resilience patterns.

Provides decorators for common error handling patterns like retry,
fallback, and error suppression.
"""


class HasName(Protocol):
    """Protocol for objects that have a __name__ attribute."""

    __name__: str


F = TypeVar("F", bound=Callable[..., Any])


class ResilientErrorHandler:
    """Encapsulates error handling logic for the resilient decorator."""

    def __init__(
        self,
        fallback: Any = None,
        log_errors: bool = True,
        context_provider: Callable[[], dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        error_mapper: Callable[[Exception], Exception] | None = None,
        suppress: tuple[type[Exception], ...] | None = None,
        reraise: bool = True,
    ) -> None:
        self.fallback = fallback
        self.log_errors = log_errors
        self.context_provider = context_provider
        self.context = context
        self.error_mapper = error_mapper
        self.suppress = suppress
        self.reraise = reraise

    def build_context(self) -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = {}
        if self.context_provider:
            log_context.update(self.context_provider())
        if self.context:
            log_context.update(self.context)
        return log_context

    def should_suppress(self, exception: Exception) -> bool:
        """Check if the error should be suppressed."""
        return self.suppress is not None and isinstance(exception, self.suppress)

    def log_suppressed(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            f"Suppressed {type(exception).__name__} in {func_name}",
            function=func_name,
            error=str(exception),
            **log_context,
        )

    def log_error(self, exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if not self.log_errors:
            return
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(
            f"Error in {func_name}: {exception}",
            exc_info=True,
            function=func_name,
            **log_context,
        )

    def map_error(self, exception: Exception) -> Exception:
        """Apply error mapping if configured.

        The error_mapper is applied to all exceptions, including FoundationError types.
        This allows translating low-level foundation errors into higher-level,
        domain-specific exceptions while preserving error handling benefits.

        If the original exception is a FoundationError and the mapped exception is also
        a FoundationError, the rich diagnostic context (code, context, cause) is
        automatically preserved.
        """
        if self.error_mapper:
            mapped = self.error_mapper(exception)
            if mapped is not exception:
                # Auto-preserve FoundationError context when mapping between FoundationError types
                from provide.foundation.errors.base import FoundationError

                if isinstance(exception, FoundationError) and isinstance(mapped, FoundationError):
                    # Preserve code if mapped error doesn't have custom code
                    if mapped.code == mapped._default_code() and exception.code != exception._default_code():
                        mapped.code = exception.code

                    # Merge contexts (mapped error's context takes precedence)
                    merged_context = {**exception.context, **mapped.context}
                    mapped.context = merged_context

                    # Preserve cause chain if not already set
                    if not mapped.cause and exception.cause:
                        mapped.cause = exception.cause
                        mapped.__cause__ = exception.cause

                return mapped
        return exception

    def process_error(self, exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = self.build_context()

        # Check if we should suppress this error
        if self.should_suppress(exception):
            self.log_suppressed(exception, func_name, log_context)
            return self.fallback

        # Log the error if configured
        self.log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not self.reraise:
            return self.fallback

        # Map the error if mapper provided and raise
        mapped_error = self.map_error(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception


def _create_async_wrapper(func: F, handler: ResilientErrorHandler) -> F:
    """Create an async wrapper for error handling."""

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return handler.process_error(e, getattr(func, "__name__", "<anonymous>"))

    return async_wrapper  # type: ignore


def _create_sync_wrapper(func: F, handler: ResilientErrorHandler) -> F:
    """Create a sync wrapper for error handling."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handler.process_error(e, getattr(func, "__name__", "<anonymous>"))

    return wrapper  # type: ignore


@overload
def resilient(
    func: F,
) -> F: ...


@overload
def resilient(
    func: None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F]: ...


def resilient(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    context: dict[str, Any] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
    reraise: bool = True,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        context: Static context dict to include in logs (alternative to context_provider).
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).
        reraise: Whether to re-raise exceptions after logging (default: True).

    Returns:
        Decorated function.

    Note:
        **Preserving Context in error_mapper:**
        When using error_mapper with FoundationError exceptions, the original
        exception's context dictionary is not automatically transferred to the
        mapped exception. To preserve rich context, manually copy it:

        >>> from provide.foundation.errors import FoundationError
        >>> @resilient(
        ...     error_mapper=lambda e: (
        ...         ValidationError(
        ...             str(e),
        ...             context=e.context if isinstance(e, FoundationError) else {}
        ...         ) if isinstance(e, FoundationError)
        ...         else DomainError(str(e))
        ...     )
        ... )
        ... def process_data(data):
        ...     # Low-level FoundationError will be mapped to ValidationError
        ...     # with context preserved
        ...     pass

    Examples:
        >>> @resilient(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @resilient(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @resilient(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def decorator(func: F) -> F:
        # Create error handler with all configuration
        handler = ResilientErrorHandler(
            fallback=fallback,
            log_errors=log_errors,
            context_provider=context_provider,
            context=context,
            error_mapper=error_mapper,
            suppress=suppress,
            reraise=reraise,
        )

        # Return appropriate wrapper based on function type
        if inspect.iscoroutinefunction(func):
            return _create_async_wrapper(func, handler)
        return _create_sync_wrapper(func, handler)

    # Support both @resilient and @resilient(...) forms
    if func is None:
        return decorator
    return decorator(func)


def suppress_and_log(
    *exceptions: type[Exception],
    fallback: Any = None,
    log_level: str = "warning",
) -> Callable[[F], F]:
    """Decorator to suppress specific exceptions and log them.

    Args:
        *exceptions: Exception types to suppress.
        fallback: Value to return when exception is suppressed.
        log_level: Log level to use ('debug', 'info', 'warning', 'error').

    Returns:
        Decorated function.

    Examples:
        >>> @suppress_and_log(KeyError, AttributeError, fallback={})
        ... def get_nested_value(data):
        ...     return data["key"].attribute

    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                # Get appropriate log method
                from provide.foundation.hub.foundation import get_foundation_logger

                if log_level in ("debug", "info", "warning", "error", "critical"):
                    log_method = getattr(get_foundation_logger(), log_level)
                else:
                    log_method = get_foundation_logger().warning

                log_method(
                    f"Suppressed {type(e).__name__} in {getattr(func, '__name__', '<anonymous>')}: {e}",
                    function=getattr(func, "__name__", "<anonymous>"),
                    error_type=type(e).__name__,
                    error=str(e),
                    fallback=fallback,
                )

                return fallback

        return wrapper  # type: ignore

    return decorator


def fallback_on_error(
    fallback_func: Callable[..., Any],
    *exceptions: type[Exception],
    log_errors: bool = True,
) -> Callable[[F], F]:
    """Decorator to call a fallback function when errors occur.

    Args:
        fallback_func: Function to call when an error occurs.
        *exceptions: Specific exception types to handle (all if empty).
        log_errors: Whether to log errors before calling fallback.

    Returns:
        Decorated function.

    Examples:
        >>> def use_cache():
        ...     return cached_value
        ...
        >>> @fallback_on_error(use_cache, NetworkError)
        ... def fetch_from_api():
        ...     return api_call()

    """
    catch_types = exceptions if exceptions else (Exception,)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except catch_types as e:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        f"Using fallback for {getattr(func, '__name__', '<anonymous>')} due to {type(e).__name__}",
                        function=getattr(func, "__name__", "<anonymous>"),
                        error_type=type(e).__name__,
                        error=str(e),
                        fallback=getattr(fallback_func, "__name__", "<anonymous>"),
                    )

                # Call fallback with same arguments
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Fallback function {getattr(fallback_func, '__name__', '<anonymous>')} also failed",
                        exc_info=True,
                        original_error=str(e),
                        fallback_error=str(fallback_error),
                    )
                    # Re-raise the fallback error
                    raise fallback_error from e

        return wrapper  # type: ignore

    return decorator


# 🧱🏗️🔚
