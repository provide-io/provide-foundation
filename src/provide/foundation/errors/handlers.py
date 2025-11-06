#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any, TypeVar

from attrs import define, field

from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.context import capture_error_context

"""Error handling utilities and context managers.

Provides tools for handling errors in a consistent and structured way.
"""

T = TypeVar("T")


@contextmanager
def error_boundary(
    *catch: type[Exception],
    on_error: Callable[[Exception], Any] | None = None,
    log_errors: bool = True,
    reraise: bool = True,
    context: dict[str, Any] | None = None,
    fallback: Any = None,
) -> Generator[None, None, None]:
    """Context manager for structured error handling with logging.

    Args:
        *catch: Exception types to catch (defaults to Exception if empty).
        on_error: Optional callback function when error is caught.
        log_errors: Whether to log caught errors.
        reraise: Whether to re-raise after handling.
        context: Additional context for error logging.
        fallback: Value to return if error is suppressed (when reraise=False).

    Yields:
        None

    Examples:
        >>> with error_boundary(ValueError, on_error=handle_error):
        ...     risky_operation()

        >>> # Suppress and log specific errors
        >>> with error_boundary(KeyError, reraise=False, fallback=None):
        ...     value = data["missing_key"]

    """
    # Default to catching all exceptions if none specified
    catch_types = catch if catch else (Exception,)

    try:
        yield
    except catch_types as e:
        if log_errors:
            # Build error context
            error_context = context or {}

            # Add error details
            error_context.update(
                {
                    "error.type": type(e).__name__,
                    "error.message": str(e),
                },
            )

            # If it's a FoundationError, merge its context
            if isinstance(e, FoundationError) and e.context:
                error_context.update(e.context)

            # Log the error
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().error(f"Error caught in boundary: {e}", exc_info=True, **error_context)

        # Call error handler if provided
        if on_error:
            try:
                on_error(e)
            except Exception as handler_error:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Error handler failed: {handler_error}",
                        exc_info=True,
                        original_error=str(e),
                    )

        # Re-raise if configured
        if reraise:
            raise

        # Return fallback value if not re-raising
        return fallback


@contextmanager
def transactional(
    rollback: Callable[[], None],
    commit: Callable[[], None] | None = None,
    on_error: Callable[[Exception], None] | None = None,
    log_errors: bool = True,
) -> Generator[None, None, None]:
    """Context manager for transactional operations with rollback.

    Args:
        rollback: Function to call on error to rollback changes.
        commit: Optional function to call on success.
        on_error: Optional error handler before rollback.
        log_errors: Whether to log errors.

    Yields:
        None

    Examples:
        >>> def rollback_changes():
        ...     db.rollback()
        ...
        >>> def commit_changes():
        ...     db.commit()
        ...
        >>> with transactional(rollback_changes, commit_changes):
        ...     db.execute("INSERT INTO users ...")
        ...     db.execute("UPDATE accounts ...")

    """
    try:
        yield
        # Call commit if provided and no exception occurred
        if commit:
            commit()
    except Exception as e:
        if log_errors:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().error("Transaction failed, rolling back", exc_info=True, error=str(e))

        # Call error handler if provided
        if on_error:
            try:
                on_error(e)
            except Exception as handler_error:
                if log_errors:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(
                        f"Transaction error handler failed: {handler_error}",
                        original_error=str(e),
                    )

        # Perform rollback
        try:
            rollback()
            if log_errors:
                from provide.foundation.hub.foundation import get_foundation_logger
            get_foundation_logger().info("Transaction rolled back successfully")
        except Exception as rollback_error:
            if log_errors:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().critical(f"Rollback failed: {rollback_error}", original_error=str(e))
            # Re-raise the rollback error as it's more critical
            raise rollback_error from e

        # Re-raise original exception
        raise


def handle_error(
    error: Exception,
    *,
    log: bool = True,
    capture_context: bool = True,
    reraise: bool = False,
    fallback: Any = None,
) -> Any:
    """Handle an error with logging and optional context capture.

    Args:
        error: The exception to handle.
        log: Whether to log the error.
        capture_context: Whether to capture error context.
        reraise: Whether to re-raise the error after handling.
        fallback: Value to return if not re-raising.

    Returns:
        The fallback value if not re-raising.

    Raises:
        Exception: The original error if reraise=True.

    Examples:
        >>> try:
        ...     risky_operation()
        ... except ValueError as e:
        ...     result = handle_error(e, fallback="default")

    """
    # Capture context if requested
    context = None
    if capture_context:
        context = capture_error_context(error)

    # Log if requested
    if log:
        log_context = context.to_dict() if context else {}
        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().error(f"Handling error: {error}", exc_info=True, **log_context)

    # Re-raise if requested
    if reraise:
        raise error

    return fallback


@define(kw_only=True, slots=True)
class ErrorHandler:
    """Configurable error handler with type-based policies.

    Attributes:
        policies: Mapping of error types to handler functions.
        default_action: Default handler for unmatched errors.
        log_all: Whether to log all handled errors.
        capture_context: Whether to capture error context.
        reraise_unhandled: Whether to re-raise unhandled errors.

    Examples:
        >>> def handle_validation(e: ValidationError):
        ...     return {"error": "Invalid input", "details": e.context}
        ...
        >>> handler = ErrorHandler(
        ...     policies={ValidationError: handle_validation},
        ...     default_action=lambda e: None
        ... )
        >>> result = handler.handle(some_error)

    """

    policies: dict[type[Exception], Callable[[Exception], Any]] = field(factory=dict)
    default_action: Callable[[Exception], Any] = field(default=lambda e: None)
    log_all: bool = True
    capture_context: bool = True
    reraise_unhandled: bool = False

    def add_policy(self, error_type: type[Exception], handler: Callable[[Exception], Any]) -> ErrorHandler:
        """Add or update a handler policy for an error type.

        Args:
            error_type: Exception type to handle.
            handler: Handler function for this error type.

        Returns:
            Self for method chaining.

        """
        self.policies[error_type] = handler
        return self

    def handle(self, error: Exception) -> Any:
        """Handle an error based on configured policies.

        Args:
            error: The exception to handle.

        Returns:
            Result from the handler function.

        Raises:
            Exception: The original error if reraise_unhandled=True and no handler matches.

        Examples:
            >>> result = handler.handle(ValidationError("Invalid"))

        """
        # Find matching handler
        handler = None
        for error_type, policy_handler in self.policies.items():
            if isinstance(error, error_type):
                handler = policy_handler
                break

        # Use default if no match
        if handler is None:
            handler = self.default_action

            # Check if we should re-raise unhandled
            if self.reraise_unhandled and handler is self.default_action:
                if self.log_all:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().warning(
                        f"No handler for {type(error).__name__}, re-raising",
                        error=str(error),
                    )
                raise error

        # Capture context if configured
        context = None
        if self.capture_context:
            context = capture_error_context(error)

        # Log if configured
        if self.log_all:
            log_context = context.to_dict() if context else {}
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().info(
                f"Handling {type(error).__name__} with {handler.__name__}",
                **log_context,
            )

        # Execute handler
        try:
            return handler(error)
        except Exception as handler_error:
            if self.log_all:
                from provide.foundation.hub.foundation import get_foundation_logger

                get_foundation_logger().error(
                    f"Error handler failed: {handler_error}",
                    exc_info=True,
                    original_error=str(error),
                    handler=handler.__name__,
                )
            raise handler_error from error


def create_error_handler(**policies: Callable[[Exception], Any]) -> ErrorHandler:
    """Create an error handler with policies from keyword arguments.

    Args:
        **policies: Error type names mapped to handler functions.

    Returns:
        Configured ErrorHandler instance.

    Examples:
        >>> handler = create_error_handler(
        ...     ValidationError=lambda e: {"error": str(e)},
        ...     NetworkError=lambda e: retry_operation(),
        ...     default=lambda e: None
        ... )

    """
    # Extract default if provided
    default = policies.pop("default", lambda e: None)

    # Import error types
    import provide.foundation.errors as errors_module

    # Build policies dict
    error_policies = {}
    for error_name, handler_func in policies.items():
        # Try to get the error class from errors module
        error_class = getattr(errors_module, error_name, None)
        if error_class and isinstance(error_class, type) and issubclass(error_class, Exception):
            error_policies[error_class] = handler_func
        else:
            from provide.foundation.hub.foundation import get_foundation_logger

            get_foundation_logger().warning(f"Unknown error type: {error_name}")

    return ErrorHandler(policies=error_policies, default_action=default)


# 🧱🏗️🔚
