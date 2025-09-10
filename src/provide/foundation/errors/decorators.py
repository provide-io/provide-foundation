"""Decorators for error handling and resilience patterns.

Provides decorators for common error handling patterns like retry,
fallback, and error suppression.
"""

from collections.abc import Callable
import functools
import inspect
from typing import Any, TypeVar

from provide.foundation.errors.base import FoundationError

F = TypeVar("F", bound=Callable[..., Any])


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""
    from provide.foundation.logger import logger

    return logger


def with_error_handling(
    func: F | None = None,
    *,
    fallback: Any = None,
    log_errors: bool = True,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    error_mapper: Callable[[Exception], Exception] | None = None,
    suppress: tuple[type[Exception], ...] | None = None,
) -> Callable[[F], F] | F:
    """Decorator for automatic error handling with logging.

    Args:
        fallback: Value to return when an error occurs.
        log_errors: Whether to log errors.
        context_provider: Function that provides additional logging context.
        error_mapper: Function to transform exceptions before re-raising.
        suppress: Tuple of exception types to suppress (return fallback instead).

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
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    # Check if we should suppress this error
                    if suppress and isinstance(e, suppress):
                        if log_errors:
                            context = context_provider() if context_provider else {}
                            _get_logger().info(
                                f"Suppressed {type(e).__name__} in {func.__name__}",
                                function=func.__name__,
                                error=str(e),
                                **context,
                            )
                        return fallback

                    # Log the error if configured
                    if log_errors:
                        context = context_provider() if context_provider else {}
                        _get_logger().error(
                            f"Error in {func.__name__}: {e}",
                            exc_info=True,
                            function=func.__name__,
                            **context,
                        )

                    # Map the error if mapper provided
                    if error_mapper and not isinstance(e, FoundationError):
                        mapped = error_mapper(e)
                        if mapped is not e:
                            raise mapped from e

                    # Re-raise the original error
                    raise

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Check if we should suppress this error
                    if suppress and isinstance(e, suppress):
                        if log_errors:
                            context = context_provider() if context_provider else {}
                            _get_logger().info(
                                f"Suppressed {type(e).__name__} in {func.__name__}",
                                function=func.__name__,
                                error=str(e),
                                **context,
                            )
                        return fallback

                    # Log the error if configured
                    if log_errors:
                        context = context_provider() if context_provider else {}
                        _get_logger().error(
                            f"Error in {func.__name__}: {e}",
                            exc_info=True,
                            function=func.__name__,
                            **context,
                        )

                    # Map the error if mapper provided
                    if error_mapper and not isinstance(e, FoundationError):
                        mapped = error_mapper(e)
                        if mapped is not e:
                            raise mapped from e

                    # Re-raise the original error
                    raise

            return wrapper  # type: ignore

    # Support both @with_error_handling and @with_error_handling(...) forms
    if func is None:
        # Called as @with_error_handling(...) with arguments
        return decorator
    else:
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
                if log_level in ("debug", "info", "warning", "error", "critical"):
                    log_method = getattr(_get_logger(), log_level)
                else:
                    log_method = _get_logger().warning

                log_method(
                    f"Suppressed {type(e).__name__} in {func.__name__}: {e}",
                    function=func.__name__,
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
                    _get_logger().warning(
                        f"Using fallback for {func.__name__} due to {type(e).__name__}",
                        function=func.__name__,
                        error_type=type(e).__name__,
                        error=str(e),
                        fallback=fallback_func.__name__,
                    )

                # Call fallback with same arguments
                try:
                    return fallback_func(*args, **kwargs)
                except Exception as fallback_error:
                    _get_logger().error(
                        f"Fallback function {fallback_func.__name__} also failed",
                        exc_info=True,
                        original_error=str(e),
                        fallback_error=str(fallback_error),
                    )
                    # Re-raise the fallback error
                    raise fallback_error from e

        return wrapper  # type: ignore

    return decorator


