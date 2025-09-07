"""
HTTP/HTTPS transport implementation using httpx.
"""

import time
from collections.abc import AsyncIterator
from typing import Any

import httpx
from attrs import define, field

from provide.foundation.logger import get_logger
from provide.foundation.transport.base import Request, Response, TransportBase
from provide.foundation.transport.config import HTTPConfig
from provide.foundation.transport.errors import (
    HTTPResponseError,
    TransportConnectionError,
    TransportTimeoutError,
)
from provide.foundation.transport.types import TransportType

log = get_logger(__name__)


@define
class HTTPTransport(TransportBase):
    """HTTP/HTTPS transport using httpx backend."""
    
    SCHEMES = ["http", "https"]
    
    config: HTTPConfig = field(factory=HTTPConfig.from_env)
    _client: httpx.AsyncClient | None = field(default=None, init=False)
    
    def supports(self, transport_type: TransportType) -> bool:
        """Check if this transport supports the given type."""
        return transport_type.value in self.SCHEMES
    
    async def connect(self) -> None:
        """Initialize httpx client with configuration."""
        if self._client is not None:
            return
        
        limits = httpx.Limits(
            max_connections=self.config.pool_connections,
            max_keepalive_connections=self.config.pool_maxsize,
        )
        
        timeout = httpx.Timeout(self.config.timeout)
        
        self._client = httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            verify=self.config.verify_ssl,
            follow_redirects=self.config.follow_redirects,
            max_redirects=self.config.max_redirects,
            http2=self.config.http2,
        )
        
        log.trace("HTTP transport connected", 
                 pool_connections=self.config.pool_connections,
                 http2=self.config.http2)
    
    async def disconnect(self) -> None:
        """Close httpx client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            log.trace("HTTP transport disconnected")
    
    async def execute(self, request: Request) -> Response:
        """Execute HTTP request."""
        await self.connect()
        
        if self._client is None:
            raise TransportConnectionError("HTTP client not connected")
        
        # Log request with emoji
        log.info(f"🚀 {request.method} {request.uri}")
        
        start_time = time.perf_counter()
        
        try:
            # Determine request body format
            json_data = None
            data = None
            
            if request.body is not None:
                if isinstance(request.body, dict):
                    json_data = request.body
                elif isinstance(request.body, (str, bytes)):
                    data = request.body
                else:
                    # Try to serialize as JSON
                    import json
                    json_data = request.body
            
            # Make the request
            httpx_response = await self._client.request(
                method=request.method,
                url=request.uri,
                headers=request.headers,
                params=request.params,
                json=json_data,
                data=data,
                timeout=request.timeout or self.config.timeout,
            )
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            # Log response with status emoji
            status_emoji = self._get_status_emoji(httpx_response.status_code)
            log.info(f"{status_emoji} {httpx_response.status_code} ({elapsed_ms:.0f}ms)")
            
            # Create response object
            response = Response(
                status=httpx_response.status_code,
                headers=dict(httpx_response.headers),
                body=httpx_response.content,
                metadata={
                    "http_version": str(httpx_response.http_version),
                    "reason_phrase": httpx_response.reason_phrase,
                    "encoding": httpx_response.encoding,
                    "is_redirect": httpx_response.is_redirect,
                    "url": str(httpx_response.url),
                },
                elapsed_ms=elapsed_ms,
                request=request,
            )
            
            return response
            
        except httpx.ConnectError as e:
            log.error(f"❌ Connection failed: {e}")
            raise TransportConnectionError(f"Failed to connect: {e}", request=request) from e
            
        except httpx.TimeoutException as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            log.error(f"⏱️ Request timed out ({elapsed_ms:.0f}ms)")
            raise TransportTimeoutError(f"Request timed out: {e}", request=request) from e
            
        except httpx.RequestError as e:
            log.error(f"❌ Request failed: {e}")
            raise TransportConnectionError(f"Request failed: {e}", request=request) from e
            
        except Exception as e:
            log.error(f"❌ Unexpected error: {e}", exc_info=True)
            raise TransportConnectionError(f"Unexpected error: {e}", request=request) from e
    
    async def stream(self, request: Request) -> AsyncIterator[bytes]:
        """Stream HTTP response."""
        await self.connect()
        
        if self._client is None:
            raise TransportConnectionError("HTTP client not connected")
        
        log.info(f"🌊 Streaming {request.method} {request.uri}")
        
        try:
            async with self._client.stream(
                method=request.method,
                url=request.uri,
                headers=request.headers,
                params=request.params,
                timeout=request.timeout or self.config.timeout,
            ) as response:
                
                # Log response start
                status_emoji = self._get_status_emoji(response.status_code)
                log.info(f"{status_emoji} {response.status_code} (streaming)")
                
                # Stream the response
                async for chunk in response.aiter_bytes():
                    yield chunk
                    
        except httpx.ConnectError as e:
            raise TransportConnectionError(f"Failed to connect: {e}", request=request) from e
            
        except httpx.TimeoutException as e:
            raise TransportTimeoutError(f"Stream timed out: {e}", request=request) from e
            
        except httpx.RequestError as e:
            raise TransportConnectionError(f"Stream failed: {e}", request=request) from e
    
    def _get_status_emoji(self, status_code: int) -> str:
        """Get emoji for HTTP status code."""
        if 200 <= status_code < 300:
            return "✅"  # Success
        elif 300 <= status_code < 400:
            return "↩️"  # Redirect
        elif 400 <= status_code < 500:
            return "⚠️"  # Client error
        elif 500 <= status_code < 600:
            return "❌"  # Server error
        else:
            return "❓"  # Unknown


# Auto-register HTTP transport
def _register_http_transport():
    """Register HTTP transport with the Hub."""
    try:
        from provide.foundation.transport.registry import register_transport
        
        register_transport(
            TransportType.HTTP,
            HTTPTransport,
            schemes=HTTPTransport.SCHEMES,
            description="HTTP/HTTPS transport using httpx",
            version="1.0.0",
        )
        
        # Also register HTTPS explicitly
        register_transport(
            TransportType.HTTPS,
            HTTPTransport,
            schemes=HTTPTransport.SCHEMES,
            description="HTTP/HTTPS transport using httpx", 
            version="1.0.0",
        )
        
    except ImportError:
        # Registry not available yet, will be registered later
        pass


# Register when module is imported
_register_http_transport()


__all__ = [
    "HTTPTransport",
]