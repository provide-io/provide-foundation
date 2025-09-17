from __future__ import annotations

"""Decorators for error handling and resilience patterns.

Provides decorators for common error handling patterns like retry,
fallback, and error suppression.
"""

from collections.abc import Callable
import functools
import inspect
from typing import Any, Protocol, TypeVar

from provide.foundation.errors.base import FoundationError


class HasName(Protocol):
    """Protocol for objects that have a __name__ attribute."""

    __name__: str


F = TypeVar("F", bound=Callable[..., Any])


def with_error_handling(
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

    Examples:
        >>> @with_error_handling(fallback=None, suppress=(KeyError,))
        ... def get_value(data, key):
        ...     return data[key]

        >>> @with_error_handling(
        ...     context_provider=lambda: {"request_id": get_request_id()}
        ... )
        ... def process_request():
        ...     # errors will be logged with request_id
        ...     pass

        >>> @with_error_handling(
        ...     reraise=False,
        ...     context={"component": "orchestrator", "method": "run"}
        ... )
        ... def run():
        ...     # errors will be logged but not re-raised
        ...     pass

    """

    def _build_error_context() -> dict[str, Any]:
        """Build logging context from provider and static context."""
        log_context = {}
        if context_provider:
            log_context.update(context_provider())
        if context:
            log_context.update(context)
        return log_context

    def _should_suppress_error(exception: Exception) -> bool:
        """Check if the error should be suppressed."""
        return suppress is not None and isinstance(exception, suppress)

    def _log_suppressed_error(exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log a suppressed error."""
        if log_errors:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().info(
                f"Suppressed {type(exception).__name__} in {func_name}",
                function=func_name,
                error=str(exception),
                **log_context,
            )

    def _log_error(exception: Exception, func_name: str, log_context: dict[str, Any]) -> None:
        """Log an error with full details."""
        if log_errors:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().error(
                f"Error in {func_name}: {exception}",
                exc_info=True,
                function=func_name,
                **log_context,
            )

    def _handle_error_mapping(exception: Exception) -> Exception:
        """Apply error mapping if configured."""
        if error_mapper and not isinstance(exception, FoundationError):
            mapped = error_mapper(exception)
            if mapped is not exception:
                return mapped
        return exception

    def _process_error(exception: Exception, func_name: str) -> Any:
        """Process an error according to configuration."""
        log_context = _build_error_context()

        # Check if we should suppress this error
        if _should_suppress_error(exception):
            _log_suppressed_error(exception, func_name, log_context)
            return fallback

        # Log the error if configured
        _log_error(exception, func_name, log_context)

        # If reraise=False, return fallback instead of raising
        if not reraise:
            return fallback

        # Map the error if mapper provided and raise
        mapped_error = _handle_error_mapping(exception)
        if mapped_error is not exception:
            raise mapped_error from exception

        # Re-raise the original error
        raise exception

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    return _process_error(e, getattr(func, "__name__", "<anonymous>"))

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return _process_error(e, getattr(func, "__name__", "<anonymous>"))

        return wrapper  # type: ignore

    # Support both @with_error_handling and @with_error_handling(...) forms
    if func is None:
        # Called as @with_error_handling(...) with arguments
        return decorator
    # Called as @with_error_handling (no parentheses)
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
        def wrapper(*args, **kwargs):
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
        def wrapper(*args, **kwargs):
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
