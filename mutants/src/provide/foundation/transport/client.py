# provide/foundation/transport/client.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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
        log.info(f"🌊 Streaming {method} {uri}")
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


def x_get_default_client__mutmut_orig() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is None:
        _default_client = UniversalClient(hub=get_hub())
    return _default_client


def x_get_default_client__mutmut_1() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is not None:
        _default_client = UniversalClient(hub=get_hub())
    return _default_client


def x_get_default_client__mutmut_2() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is None:
        _default_client = None
    return _default_client


def x_get_default_client__mutmut_3() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is None:
        _default_client = UniversalClient(hub=None)
    return _default_client

x_get_default_client__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_default_client__mutmut_1': x_get_default_client__mutmut_1, 
    'x_get_default_client__mutmut_2': x_get_default_client__mutmut_2, 
    'x_get_default_client__mutmut_3': x_get_default_client__mutmut_3
}

def get_default_client(*args, **kwargs):
    result = _mutmut_trampoline(x_get_default_client__mutmut_orig, x_get_default_client__mutmut_mutants, args, kwargs)
    return result 

get_default_client.__signature__ = _mutmut_signature(x_get_default_client__mutmut_orig)
x_get_default_client__mutmut_orig.__name__ = 'x_get_default_client'


async def x_request__mutmut_orig(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, method, **kwargs)


async def x_request__mutmut_1(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = None
    return await client.request(uri, method, **kwargs)


async def x_request__mutmut_2(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(None, method, **kwargs)


async def x_request__mutmut_3(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, None, **kwargs)


async def x_request__mutmut_4(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(method, **kwargs)


async def x_request__mutmut_5(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, **kwargs)


async def x_request__mutmut_6(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, method, )

x_request__mutmut_mutants : ClassVar[MutantDict] = {
'x_request__mutmut_1': x_request__mutmut_1, 
    'x_request__mutmut_2': x_request__mutmut_2, 
    'x_request__mutmut_3': x_request__mutmut_3, 
    'x_request__mutmut_4': x_request__mutmut_4, 
    'x_request__mutmut_5': x_request__mutmut_5, 
    'x_request__mutmut_6': x_request__mutmut_6
}

def request(*args, **kwargs):
    result = _mutmut_trampoline(x_request__mutmut_orig, x_request__mutmut_mutants, args, kwargs)
    return result 

request.__signature__ = _mutmut_signature(x_request__mutmut_orig)
x_request__mutmut_orig.__name__ = 'x_request'


async def x_get__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(uri, **kwargs)


async def x_get__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = None
    return await client.get(uri, **kwargs)


async def x_get__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(None, **kwargs)


async def x_get__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(**kwargs)


async def x_get__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(uri, )

x_get__mutmut_mutants : ClassVar[MutantDict] = {
'x_get__mutmut_1': x_get__mutmut_1, 
    'x_get__mutmut_2': x_get__mutmut_2, 
    'x_get__mutmut_3': x_get__mutmut_3, 
    'x_get__mutmut_4': x_get__mutmut_4
}

def get(*args, **kwargs):
    result = _mutmut_trampoline(x_get__mutmut_orig, x_get__mutmut_mutants, args, kwargs)
    return result 

get.__signature__ = _mutmut_signature(x_get__mutmut_orig)
x_get__mutmut_orig.__name__ = 'x_get'


async def x_post__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(uri, **kwargs)


async def x_post__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = None
    return await client.post(uri, **kwargs)


async def x_post__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(None, **kwargs)


async def x_post__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(**kwargs)


async def x_post__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(uri, )

x_post__mutmut_mutants : ClassVar[MutantDict] = {
'x_post__mutmut_1': x_post__mutmut_1, 
    'x_post__mutmut_2': x_post__mutmut_2, 
    'x_post__mutmut_3': x_post__mutmut_3, 
    'x_post__mutmut_4': x_post__mutmut_4
}

def post(*args, **kwargs):
    result = _mutmut_trampoline(x_post__mutmut_orig, x_post__mutmut_mutants, args, kwargs)
    return result 

post.__signature__ = _mutmut_signature(x_post__mutmut_orig)
x_post__mutmut_orig.__name__ = 'x_post'


async def x_put__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(uri, **kwargs)


async def x_put__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = None
    return await client.put(uri, **kwargs)


async def x_put__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(None, **kwargs)


async def x_put__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(**kwargs)


async def x_put__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(uri, )

x_put__mutmut_mutants : ClassVar[MutantDict] = {
'x_put__mutmut_1': x_put__mutmut_1, 
    'x_put__mutmut_2': x_put__mutmut_2, 
    'x_put__mutmut_3': x_put__mutmut_3, 
    'x_put__mutmut_4': x_put__mutmut_4
}

def put(*args, **kwargs):
    result = _mutmut_trampoline(x_put__mutmut_orig, x_put__mutmut_mutants, args, kwargs)
    return result 

put.__signature__ = _mutmut_signature(x_put__mutmut_orig)
x_put__mutmut_orig.__name__ = 'x_put'


async def x_patch__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(uri, **kwargs)


async def x_patch__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = None
    return await client.patch(uri, **kwargs)


async def x_patch__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(None, **kwargs)


async def x_patch__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(**kwargs)


async def x_patch__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(uri, )

x_patch__mutmut_mutants : ClassVar[MutantDict] = {
'x_patch__mutmut_1': x_patch__mutmut_1, 
    'x_patch__mutmut_2': x_patch__mutmut_2, 
    'x_patch__mutmut_3': x_patch__mutmut_3, 
    'x_patch__mutmut_4': x_patch__mutmut_4
}

def patch(*args, **kwargs):
    result = _mutmut_trampoline(x_patch__mutmut_orig, x_patch__mutmut_mutants, args, kwargs)
    return result 

patch.__signature__ = _mutmut_signature(x_patch__mutmut_orig)
x_patch__mutmut_orig.__name__ = 'x_patch'


async def x_delete__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(uri, **kwargs)


async def x_delete__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = None
    return await client.delete(uri, **kwargs)


async def x_delete__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(None, **kwargs)


async def x_delete__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(**kwargs)


async def x_delete__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(uri, )

x_delete__mutmut_mutants : ClassVar[MutantDict] = {
'x_delete__mutmut_1': x_delete__mutmut_1, 
    'x_delete__mutmut_2': x_delete__mutmut_2, 
    'x_delete__mutmut_3': x_delete__mutmut_3, 
    'x_delete__mutmut_4': x_delete__mutmut_4
}

def delete(*args, **kwargs):
    result = _mutmut_trampoline(x_delete__mutmut_orig, x_delete__mutmut_mutants, args, kwargs)
    return result 

delete.__signature__ = _mutmut_signature(x_delete__mutmut_orig)
x_delete__mutmut_orig.__name__ = 'x_delete'


async def x_head__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(uri, **kwargs)


async def x_head__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = None
    return await client.head(uri, **kwargs)


async def x_head__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(None, **kwargs)


async def x_head__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(**kwargs)


async def x_head__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(uri, )

x_head__mutmut_mutants : ClassVar[MutantDict] = {
'x_head__mutmut_1': x_head__mutmut_1, 
    'x_head__mutmut_2': x_head__mutmut_2, 
    'x_head__mutmut_3': x_head__mutmut_3, 
    'x_head__mutmut_4': x_head__mutmut_4
}

def head(*args, **kwargs):
    result = _mutmut_trampoline(x_head__mutmut_orig, x_head__mutmut_mutants, args, kwargs)
    return result 

head.__signature__ = _mutmut_signature(x_head__mutmut_orig)
x_head__mutmut_orig.__name__ = 'x_head'


async def x_options__mutmut_orig(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(uri, **kwargs)


async def x_options__mutmut_1(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = None
    return await client.options(uri, **kwargs)


async def x_options__mutmut_2(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(None, **kwargs)


async def x_options__mutmut_3(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(**kwargs)


async def x_options__mutmut_4(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(uri, )

x_options__mutmut_mutants : ClassVar[MutantDict] = {
'x_options__mutmut_1': x_options__mutmut_1, 
    'x_options__mutmut_2': x_options__mutmut_2, 
    'x_options__mutmut_3': x_options__mutmut_3, 
    'x_options__mutmut_4': x_options__mutmut_4
}

def options(*args, **kwargs):
    result = _mutmut_trampoline(x_options__mutmut_orig, x_options__mutmut_mutants, args, kwargs)
    return result 

options.__signature__ = _mutmut_signature(x_options__mutmut_orig)
x_options__mutmut_orig.__name__ = 'x_options'


async def x_stream__mutmut_orig(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(uri, **kwargs):
        yield chunk


async def x_stream__mutmut_1(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = None
    async for chunk in client.stream(uri, **kwargs):
        yield chunk


async def x_stream__mutmut_2(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(None, **kwargs):
        yield chunk


async def x_stream__mutmut_3(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(**kwargs):
        yield chunk


async def x_stream__mutmut_4(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(uri, ):
        yield chunk

x_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x_stream__mutmut_1': x_stream__mutmut_1, 
    'x_stream__mutmut_2': x_stream__mutmut_2, 
    'x_stream__mutmut_3': x_stream__mutmut_3, 
    'x_stream__mutmut_4': x_stream__mutmut_4
}

def stream(*args, **kwargs):
    result = _mutmut_trampoline(x_stream__mutmut_orig, x_stream__mutmut_mutants, args, kwargs)
    return result 

stream.__signature__ = _mutmut_signature(x_stream__mutmut_orig)
x_stream__mutmut_orig.__name__ = 'x_stream'


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


# <3 🧱🤝🚚🪄
