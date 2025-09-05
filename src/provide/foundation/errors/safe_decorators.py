"""Safe error decorators that preserve original behavior."""

from collections.abc import Callable
import functools
import inspect
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def _get_logger():
    """Get logger instance lazily to avoid circular imports."""
    from provide.foundation.logger import logger

    return logger


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
            async def async_wrapper(*args, **kwargs):
                context = context_provider() if context_provider else {}
                logger = _get_logger()

                # Log function entry if debug/trace level
                if log_level in ("debug", "trace"):
                    log_method = getattr(logger, log_level)
                    log_method(
                        f"Entering {func.__name__}", function=func.__name__, **context
                    )

                try:
                    result = await func(*args, **kwargs)

                    # Log success if requested
                    if log_success:
                        log_method = getattr(logger, log_level, logger.debug)
                        log_method(
                            f"Successfully completed {func.__name__}",
                            function=func.__name__,
                            **context,
                        )

                    return result

                except Exception as e:
                    # Log error context without changing the error
                    logger.error(
                        f"Error in {func.__name__}",
                        exc_info=True,
                        function=func.__name__,
                        error_type=type(e).__name__,
                        error_message=str(e),
                        **context,
                    )
                    # Re-raise the original error unchanged
                    raise

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                context = context_provider() if context_provider else {}
                logger = _get_logger()

                # Log function entry if debug/trace level
                if log_level in ("debug", "trace"):
                    log_method = getattr(logger, log_level)
                    log_method(
                        f"Entering {func.__name__}", function=func.__name__, **context
                    )

                try:
                    result = func(*args, **kwargs)

                    # Log success if requested
                    if log_success:
                        log_method = getattr(logger, log_level, logger.debug)
                        log_method(
                            f"Successfully completed {func.__name__}",
                            function=func.__name__,
                            **context,
                        )

                    return result

                except Exception as e:
                    # Log error context without changing the error
                    logger.error(
                        f"Error in {func.__name__}",
                        exc_info=True,
                        function=func.__name__,
                        error_type=type(e).__name__,
                        error_message=str(e),
                        **context,
                    )
                    # Re-raise the original error unchanged
                    raise

            return wrapper  # type: ignore

    return decorator
