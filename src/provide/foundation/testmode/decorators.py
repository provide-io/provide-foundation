#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
import functools
from typing import Any, TypeVar

from provide.foundation.logger import get_logger
from provide.foundation.testmode.detection import is_in_test_mode

"""Test mode decorators for optional features.

Provides reusable decorators for marking functions that should be skipped
in test mode. This is particularly useful for optional features that modify
system state (process titles, systemd notifications, etc.) and would interfere
with test isolation.

The decorators automatically:
- Check if running in test mode
- Skip execution and return a default value
- Log the skip for debugging
- Register the function in a global registry for validation

Example:
    >>> from provide.foundation.testmode import skip_in_test_mode
    >>>
    >>> @skip_in_test_mode(return_value=True)
    >>> def set_process_title(title: str) -> bool:
    ...     setproctitle.setproctitle(title)
    ...     return True
"""

log = get_logger(__name__)

# Global registry of test-unsafe functions
# This allows validation tests to verify all test-unsafe features are properly decorated
_TEST_UNSAFE_FEATURES: dict[str, dict[str, Any]] = {}

F = TypeVar("F", bound=Callable[..., Any])


def skip_in_test_mode(
    return_value: Any = None,
    log_level: str = "debug",
    reason: str | None = None,
) -> Callable[[F], F]:
    """Decorator to skip function execution in test mode.

    Marks a function as test-unsafe and automatically skips execution when
    running in test mode. The function is registered in a global registry
    for validation purposes.

    This decorator is reusable for any scenario where you want to conditionally
    skip function execution based on runtime detection.

    Args:
        return_value: Value to return when skipped (default: None)
        log_level: Log level for skip message (default: "debug")
        reason: Optional custom reason for skipping (for logging)

    Returns:
        Decorated function that checks test mode before execution

    Example:
        >>> @skip_in_test_mode(return_value=True)
        >>> def set_system_state(value: str) -> bool:
        ...     # This won't run in tests
        ...     os.system(f"something {value}")
        ...     return True

        >>> @skip_in_test_mode(return_value=None, reason="systemd not available in tests")
        >>> def notify_systemd(status: str) -> None:
        ...     systemd.notify(status)

    """

    def decorator(func: F) -> F:
        # Register this function as test-unsafe
        func_id = f"{func.__module__}.{func.__name__}"
        _TEST_UNSAFE_FEATURES[func_id] = {
            "function": func,
            "return_value": return_value,
            "reason": reason or "Test mode detected - preventing test interference",
        }

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if is_in_test_mode():
                # Determine log message
                skip_reason = reason or "Test mode detected - preventing test interference"

                # Get the logger method (debug, info, warning, etc.)
                log_method = getattr(log, log_level, log.debug)

                # Log the skip
                log_method(
                    f"Skipping {func.__name__} in test mode",
                    function=func.__name__,
                    reason=skip_reason,
                    return_value=return_value,
                )

                return return_value

            # Not in test mode - execute normally
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def get_test_unsafe_features() -> dict[str, dict[str, Any]]:
    """Get the registry of all test-unsafe features.

    This is primarily used by validation tests to ensure all test-unsafe
    features are properly decorated.

    Returns:
        Dictionary mapping function IDs to their metadata

    Example:
        >>> features = get_test_unsafe_features()
        >>> assert "process.title.set_process_title" in features

    """
    return _TEST_UNSAFE_FEATURES.copy()


def is_test_unsafe(func: Callable[..., Any]) -> bool:
    """Check if a function is registered as test-unsafe.

    Args:
        func: The function to check

    Returns:
        True if the function is decorated with @skip_in_test_mode

    Example:
        >>> @skip_in_test_mode()
        >>> def my_function():
        ...     pass
        >>>
        >>> is_test_unsafe(my_function)
        True

    """
    func_id = f"{func.__module__}.{func.__name__}"
    return func_id in _TEST_UNSAFE_FEATURES


__all__ = [
    "get_test_unsafe_features",
    "is_test_unsafe",
    "skip_in_test_mode",
]

# 🧱🏗️🔚
