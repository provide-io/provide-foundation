from __future__ import annotations

from provide.foundation.errors.auth import AuthenticationError, AuthorizationError
from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.config import (
    ConfigurationError,
    ConfigValidationError,
    ValidationError,
)
from provide.foundation.errors.context import (
    ErrorCategory,
    ErrorContext,
    ErrorSeverity,
    capture_error_context,
)
from provide.foundation.errors.decorators import (
    fallback_on_error,
    resilient,
    suppress_and_log,
)
from provide.foundation.errors.dependencies import (
    DependencyError,
    DependencyMismatchError,
)
from provide.foundation.errors.handlers import (
    ErrorHandler,
    error_boundary,
    handle_error,
    transactional,
)
from provide.foundation.errors.integration import (
    IntegrationError,
    NetworkError,
    TimeoutError,
)
from provide.foundation.errors.process import (
    CommandNotFoundError,
    ProcessError,
    ProcessTimeoutError,
)
from provide.foundation.errors.resources import (
    AlreadyExistsError,
    NotFoundError,
    ResourceError,
)
from provide.foundation.errors.runtime import ConcurrencyError, RuntimeError, StateError
from provide.foundation.errors.safe_decorators import log_only_error_context
from provide.foundation.errors.types import (
    ErrorCode,
    ErrorMetadata,
)

# Re-export from resilience module for compatibility
from provide.foundation.resilience.decorators import retry as retry_on_error

"""Foundation error handling system.

Provides a comprehensive exception hierarchy, error context management,
and utilities for robust error handling throughout the application.
"""

__all__ = [
    "AlreadyExistsError",
    "AuthenticationError",
    "AuthorizationError",
    "CommandNotFoundError",
    "ConcurrencyError",
    "ConfigValidationError",
    "ConfigurationError",
    "DependencyError",
    "DependencyMismatchError",
    "ErrorCategory",
    # Types
    "ErrorCode",
    # Context
    "ErrorContext",
    "ErrorHandler",
    "ErrorMetadata",
    "ErrorSeverity",
    # Base exceptions
    "FoundationError",
    "IntegrationError",
    "NetworkError",
    "NotFoundError",
    "ProcessError",
    "ProcessTimeoutError",
    "ResourceError",
    "RuntimeError",
    "StateError",
    "TimeoutError",
    "ValidationError",
    "capture_error_context",
    # Handlers
    "error_boundary",
    "fallback_on_error",
    "handle_error",
    "log_only_error_context",
    # Decorators
    "resilient",
    "retry_on_error",
    "suppress_and_log",
    "transactional",
]
