#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.errors.base import FoundationError

"""Transport-specific error types."""

if TYPE_CHECKING:
    from provide.foundation.transport.base import Request, Response


class TransportError(FoundationError):
    """Base transport error."""

    def __init__(self, message: str, *, request: Request | None = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.request = request


class TransportConnectionError(TransportError):
    """Transport connection failed."""


class TransportTimeoutError(TransportError):
    """Transport request timed out."""


class HTTPResponseError(TransportError):
    """HTTP response error (4xx/5xx status codes)."""

    def __init__(self, message: str, *, status_code: int, response: Response, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.status_code = status_code
        self.response = response


class TransportConfigurationError(TransportError):
    """Transport configuration error."""


class TransportNotFoundError(TransportError):
    """No transport found for the given URI scheme."""

    def __init__(self, message: str, *, scheme: str, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme


class TransportCacheEvictedError(TransportError):
    """Transport was evicted from cache due to failures."""

    def __init__(
        self,
        message: str,
        *,
        scheme: str,
        consecutive_failures: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.scheme = scheme
        self.consecutive_failures = consecutive_failures


__all__ = [
    "HTTPResponseError",
    "TransportCacheEvictedError",
    "TransportConfigurationError",
    "TransportConnectionError",
    "TransportError",
    "TransportNotFoundError",
    "TransportTimeoutError",
]

# 🧱🏗️🔚
