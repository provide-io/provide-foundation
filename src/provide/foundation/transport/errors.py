from __future__ import annotations

"""Transport-specific error types."""

from typing import TYPE_CHECKING

from provide.foundation.errors.base import FoundationError

if TYPE_CHECKING:
    from provide.foundation.transport.base import Request, Response


class TransportError(FoundationError):
    """Base transport error."""

    def __init__(self, message: str, *, request: "Request | None" = None, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.request = request


class TransportConnectionError(TransportError):
    """Transport connection failed."""


class TransportTimeoutError(TransportError):
    """Transport request timed out."""


class HTTPResponseError(TransportError):
    """HTTP response error (4xx/5xx status codes)."""

    def __init__(self, message: str, *, status_code: int, response: "Response", **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response = response


class TransportConfigurationError(TransportError):
    """Transport configuration error."""


class TransportNotFoundError(TransportError):
    """No transport found for the given URI scheme."""

    def __init__(self, message: str, *, scheme: str, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme


__all__ = [
    "HTTPResponseError",
    "TransportConfigurationError",
    "TransportConnectionError",
    "TransportError",
    "TransportNotFoundError",
    "TransportTimeoutError",
]
