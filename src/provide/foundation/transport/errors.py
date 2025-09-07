"""
Transport-specific error types.
"""

from typing import TYPE_CHECKING

from provide.foundation.errors.base import FoundationError

if TYPE_CHECKING:
    from provide.foundation.transport.base import Request, Response


class TransportError(FoundationError):
    """Base transport error."""
    
    def __init__(
        self, 
        message: str,
        *,
        request: "Request | None" = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.request = request


class TransportConnectionError(TransportError):
    """Transport connection failed."""
    pass


class TransportTimeoutError(TransportError):
    """Transport request timed out."""
    pass


class HTTPResponseError(TransportError):
    """HTTP response error (4xx/5xx status codes)."""
    
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response: "Response",
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response = response


class TransportConfigurationError(TransportError):
    """Transport configuration error."""
    pass


class TransportNotFoundError(TransportError):
    """No transport found for the given URI scheme."""
    
    def __init__(
        self,
        message: str,
        *,
        scheme: str,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.scheme = scheme


__all__ = [
    "TransportError",
    "TransportConnectionError", 
    "TransportTimeoutError",
    "HTTPResponseError",
    "TransportConfigurationError",
    "TransportNotFoundError",
]