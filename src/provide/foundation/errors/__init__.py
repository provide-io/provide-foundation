"""
Foundation error handling system.

Provides a comprehensive exception hierarchy, error context management,
and utilities for robust error handling throughout the application.
"""

from provide.foundation.errors.exceptions import (
    FoundationError,
    ConfigurationError,
    ValidationError,
    RuntimeError,
    IntegrationError,
    ResourceError,
    NetworkError,
    TimeoutError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    AlreadyExistsError,
    StateError,
    ConcurrencyError,
)
from provide.foundation.errors.context import (
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
    capture_error_context,
)
from provide.foundation.errors.handlers import (
    error_boundary,
    transactional,
    handle_error,
    ErrorHandler,
)
from provide.foundation.errors.decorators import (
    with_error_handling,
    retry_on_error,
    suppress_and_log,
    fallback_on_error,
)
from provide.foundation.errors.types import (
    ErrorCode,
    ErrorMetadata,
    RetryPolicy,
)

__all__ = [
    # Base exceptions
    "FoundationError",
    "ConfigurationError",
    "ValidationError",
    "RuntimeError",
    "IntegrationError",
    "ResourceError",
    "NetworkError",
    "TimeoutError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "AlreadyExistsError",
    "StateError",
    "ConcurrencyError",
    # Context
    "ErrorContext",
    "ErrorSeverity",
    "ErrorCategory",
    "capture_error_context",
    # Handlers
    "error_boundary",
    "transactional",
    "handle_error",
    "ErrorHandler",
    # Decorators
    "with_error_handling",
    "retry_on_error",
    "suppress_and_log",
    "fallback_on_error",
    # Types
    "ErrorCode",
    "ErrorMetadata",
    "RetryPolicy",
]