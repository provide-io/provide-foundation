"""
Foundation error handling system.

Provides a comprehensive exception hierarchy, error context management,
and utilities for robust error handling throughout the application.
"""

from provide.foundation.errors.context import (
    ErrorCategory,
    ErrorContext,
    ErrorSeverity,
    capture_error_context,
)
from provide.foundation.errors.decorators import (
    fallback_on_error,
    retry_on_error,
    suppress_and_log,
    with_error_handling,
)
from provide.foundation.errors.exceptions import (
    AlreadyExistsError,
    AuthenticationError,
    AuthorizationError,
    ConcurrencyError,
    ConfigurationError,
    FoundationError,
    IntegrationError,
    NetworkError,
    NotFoundError,
    ResourceError,
    RuntimeError,
    StateError,
    TimeoutError,
    ValidationError,
)
from provide.foundation.errors.handlers import (
    ErrorHandler,
    error_boundary,
    handle_error,
    transactional,
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
