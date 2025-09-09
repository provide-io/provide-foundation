"""Decorators for error handling and resilience patterns.

Provides decorators for common error handling patterns like retry,
fallback, and error suppression.
"""

from collections.abc import Callable
import functools
import inspect
import time
from typing import Any, TypeVar

from attrs import define, field

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


@define(kw_only=True, slots=True)
class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures.

    Attributes:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception types that trigger the breaker.
    """

    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    expected_exception: tuple[type[Exception], ...] = field(default=(Exception,))

    # Internal state
    _failure_count: int = field(init=False, default=0)
    _last_failure_time: float | None = field(init=False, default=None)
    _state: str = field(init=False, default="closed")  # closed, open, half_open

    def __call__(self, func: F) -> F:
        """Decorator to apply circuit breaker to a function."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check circuit state
            if self._state == "open":
                # Check if we should try half-open
                if (
                    self._last_failure_time
                    and (time.time() - self._last_failure_time) > self.recovery_timeout
                ):
                    self._state = "half_open"
                    _get_logger().info(
                        f"Circuit breaker for {func.__name__} entering half-open state",
                        function=func.__name__,
                    )
                else:
                    raise RuntimeError(f"Circuit breaker is open for {func.__name__}")

            try:
                result = func(*args, **kwargs)

                # Success - reset on half-open or reduce failure count
                if self._state == "half_open":
                    self._state = "closed"
                    self._failure_count = 0
                    _get_logger().info(
                        f"Circuit breaker for {func.__name__} closed after successful recovery",
                        function=func.__name__,
                    )
                elif self._failure_count > 0:
                    self._failure_count = max(0, self._failure_count - 1)

                return result

            except self.expected_exception as e:
                self._failure_count += 1
                self._last_failure_time = time.time()

                # Check if we should open the circuit
                if self._failure_count >= self.failure_threshold:
                    self._state = "open"
                    _get_logger().error(
                        f"Circuit breaker for {func.__name__} opened after {self._failure_count} failures",
                        function=func.__name__,
                        failures=self._failure_count,
                        error=str(e),
                    )
                else:
                    _get_logger().warning(
                        f"Circuit breaker for {func.__name__} failure {self._failure_count}/{self.failure_threshold}",
                        function=func.__name__,
                        failures=self._failure_count,
                        threshold=self.failure_threshold,
                        error=str(e),
                    )

                raise

        return wrapper  # type: ignore


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception types that trigger the breaker.

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()
    """
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception,
    )
    return breaker
