"""
Custom exceptions for OpenObserve integration.
"""

from provide.foundation.errors import FoundationError


class OpenObserveError(FoundationError):
    """Base exception for OpenObserve-related errors."""

    pass


class OpenObserveConnectionError(OpenObserveError):
    """Error connecting to OpenObserve API."""

    pass


class OpenObserveAuthenticationError(OpenObserveError):
    """Authentication failed with OpenObserve."""

    pass


class OpenObserveQueryError(OpenObserveError):
    """Error executing query in OpenObserve."""

    pass


class OpenObserveStreamingError(OpenObserveError):
    """Error during streaming operations."""

    pass


class OpenObserveConfigError(OpenObserveError):
    """Configuration error for OpenObserve."""

    pass
