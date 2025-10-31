#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from attrs import define, field

from provide.foundation.hub import Hub, get_hub
from provide.foundation.logger import get_logger
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.cache import TransportCache
from provide.foundation.transport.errors import TransportError
from provide.foundation.transport.middleware import (
    MiddlewarePipeline,
    create_default_pipeline,
)
from provide.foundation.transport.registry import get_transport
from provide.foundation.transport.types import Data, Headers, HTTPMethod, Params

"""Universal transport client with middleware support."""

log = get_logger(__name__)


@define(slots=True)
class UniversalClient:
    """Universal client that works with any transport via Hub registry.

    The client uses a TransportCache that automatically evicts transports
    that exceed the failure threshold (default: 3 consecutive failures).
    """

    hub: Hub = field()
    middleware: MiddlewarePipeline = field(factory=create_default_pipeline)
    default_headers: Headers = field(factory=dict)
    default_timeout: float | None = field(default=None)
    _cache: TransportCache = field(factory=TransportCache, init=False)

    async def request(
        self,
        uri: str,
        method: str | HTTPMethod = HTTPMethod.GET,
        *,
        headers: Headers | None = None,
        params: Params | None = None,
        body: Data = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> Response:
        """Make a request using appropriate transport.

        Args:
            uri: Full URI to make request to
            method: HTTP method or protocol-specific method
            headers: Request headers
            params: Query parameters
            body: Request body (dict for JSON, str/bytes for raw)
            timeout: Request timeout override
            **kwargs: Additional request metadata

        Returns:
            Response from the transport

        """
        # Normalize method
        if isinstance(method, HTTPMethod):
            method = method.value

        # Merge headers
        request_headers = dict(self.default_headers)
        if headers:
            request_headers.update(headers)

        # Create request object
        request = Request(
            uri=uri,
            method=method,
            headers=request_headers,
            params=params or {},
            body=body,
            timeout=timeout or self.default_timeout,
            metadata=kwargs,
        )

        # Process through middleware
        request = await self.middleware.process_request(request)

        try:
            # Get transport for this URI
            transport = await self._get_transport(request.transport_type.value)

            # Execute request
            response = await transport.execute(request)

            # Mark success in cache
            self._cache.mark_success(request.transport_type.value)

            # Process response through middleware
            response = await self.middleware.process_response(response)

            return response

        except Exception as e:
            # Mark failure if it's a transport error
            if isinstance(e, TransportError):
                self._cache.mark_failure(request.transport_type.value, e)

            # Process error through middleware
            e = await self.middleware.process_error(e, request)
            raise e

    async def stream(
        self,
        uri: str,
        method: str | HTTPMethod = HTTPMethod.GET,
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """Stream data from URI.

        Args:
            uri: URI to stream from
            method: HTTP method or protocol-specific method
            **kwargs: Additional request parameters

        Yields:
            Chunks of response data

        """
        # Normalize method
        if isinstance(method, HTTPMethod):
            method = method.value

        # Create request
        request = Request(uri=uri, method=method, headers=dict(self.default_headers), **kwargs)

        # Get transport
        transport = await self._get_transport(request.transport_type.value)

        # Stream response
        async for chunk in transport.stream(request):
            yield chunk

    async def get(self, uri: str, **kwargs: Any) -> Response:
        """GET request."""
        return await self.request(uri, HTTPMethod.GET, **kwargs)

    async def post(self, uri: str, **kwargs: Any) -> Response:
        """POST request."""
        return await self.request(uri, HTTPMethod.POST, **kwargs)

    async def put(self, uri: str, **kwargs: Any) -> Response:
        """PUT request."""
        return await self.request(uri, HTTPMethod.PUT, **kwargs)

    async def patch(self, uri: str, **kwargs: Any) -> Response:
        """PATCH request."""
        return await self.request(uri, HTTPMethod.PATCH, **kwargs)

    async def delete(self, uri: str, **kwargs: Any) -> Response:
        """DELETE request."""
        return await self.request(uri, HTTPMethod.DELETE, **kwargs)

    async def head(self, uri: str, **kwargs: Any) -> Response:
        """HEAD request."""
        return await self.request(uri, HTTPMethod.HEAD, **kwargs)

    async def options(self, uri: str, **kwargs: Any) -> Response:
        """OPTIONS request."""
        return await self.request(uri, HTTPMethod.OPTIONS, **kwargs)

    async def _get_transport(self, scheme: str) -> Any:
        """Get or create transport for scheme.

        Raises:
            TransportCacheEvictedError: If transport was evicted due to failures
        """

        def _factory(s: str) -> Any:
            """Factory to create transport from registry."""
            return get_transport(f"{s}://example.com")

        return await self._cache.get_or_create(scheme, _factory)

    async def __aenter__(self) -> UniversalClient:
        """Context manager entry."""
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Context manager exit - cleanup all transports."""
        transports = self._cache.clear()
        for transport in transports.values():
            try:
                await transport.disconnect()
            except Exception as e:
                log.error(f"Error disconnecting transport: {e}")

    def reset_transport_cache(self) -> None:
        """Reset the transport cache.

        Useful for testing or forcing reconnection after configuration changes.
        """
        log.info("🔄 Resetting transport cache")
        self._cache.clear()


# Global client instance for convenience functions
_default_client: UniversalClient | None = None


def get_default_client() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is None:
        _default_client = UniversalClient(hub=get_hub())
    return _default_client


async def request(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, method, **kwargs)


async def get(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(uri, **kwargs)


async def post(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(uri, **kwargs)


async def put(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(uri, **kwargs)


async def patch(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(uri, **kwargs)


async def delete(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(uri, **kwargs)


async def head(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(uri, **kwargs)


async def options(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(uri, **kwargs)


async def stream(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(uri, **kwargs):
        yield chunk


__all__ = [
    "UniversalClient",
    "delete",
    "get",
    "get_default_client",
    "head",
    "options",
    "patch",
    "post",
    "put",
    "request",
    "stream",
]

# 🧱🏗️🔚
