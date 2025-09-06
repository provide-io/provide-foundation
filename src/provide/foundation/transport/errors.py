"""
Transport-specific error types.
"""

from attrs import define

from provide.foundation.errors.base import FoundationError
from provide.foundation.transport.base import Request, Response


@define
class TransportError(FoundationError):
    """Base transport error."""
    
    request: Request | None = None


@define  
class TransportConnectionError(TransportError):
    """Transport connection failed."""
    pass


@define
class TransportTimeoutError(TransportError):
    """Transport request timed out."""
    pass


@define
class HTTPResponseError(TransportError):
    """HTTP response error (4xx/5xx status codes)."""
    
    status_code: int
    response: Response


@define
class TransportConfigurationError(TransportError):
    """Transport configuration error."""
    pass


@define
class TransportNotFoundError(TransportError):
    """No transport found for the given URI scheme."""
    
    scheme: str


__all__ = [
    "TransportError",
    "TransportConnectionError", 
    "TransportTimeoutError",
    "HTTPResponseError",
    "TransportConfigurationError",
    "TransportNotFoundError",
]