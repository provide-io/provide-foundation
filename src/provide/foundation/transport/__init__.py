"""
Provide Foundation Transport System
==================================

Protocol-agnostic transport layer with HTTP/HTTPS support using Foundation Hub registry.

Key Features:
- Hub-based transport registration and discovery
- Async-first with httpx backend for HTTP/HTTPS
- Built-in telemetry with foundation.logger
- Middleware pipeline for extensibility
- No hardcoded defaults - all configuration from environment
- Modern Python 3.11+ typing

Example Usage:
    >>> from provide.foundation.transport import get, post
    >>> 
    >>> # Simple requests
    >>> response = await get("https://api.example.com/users")
    >>> data = response.json()
    >>> 
    >>> # POST with JSON body
    >>> response = await post(
    ...     "https://api.example.com/users",
    ...     body={"name": "John", "email": "john@example.com"}
    ... )
    >>> 
    >>> # Using client for multiple requests
    >>> from provide.foundation.transport import UniversalClient
    >>> 
    >>> async with UniversalClient() as client:
    ...     users = await client.get("https://api.example.com/users")
    ...     posts = await client.get("https://api.example.com/posts")
    >>> 
    >>> # Custom transport registration
    >>> from provide.foundation.transport import register_transport
    >>> from provide.foundation.transport.types import TransportType
    >>> 
    >>> register_transport(TransportType("custom"), MyCustomTransport)

Environment Configuration:
    TRANSPORT_TIMEOUT=30.0
    TRANSPORT_MAX_RETRIES=3
    TRANSPORT_RETRY_BACKOFF_FACTOR=0.5
    TRANSPORT_VERIFY_SSL=true
    
    HTTP_POOL_CONNECTIONS=10
    HTTP_POOL_MAXSIZE=100
    HTTP_FOLLOW_REDIRECTS=true
    HTTP_USE_HTTP2=true
    HTTP_MAX_REDIRECTS=5
"""

# Core transport abstractions
from provide.foundation.transport.base import Request, Response

# Transport types and configuration
from provide.foundation.transport.config import HTTPConfig, TransportConfig
from provide.foundation.transport.types import HTTPMethod, TransportType

# Error types
from provide.foundation.transport.errors import (
    HTTPResponseError,
    TransportConnectionError,
    TransportError,
    TransportNotFoundError,
    TransportTimeoutError,
)

# Transport implementations
from provide.foundation.transport.http import HTTPTransport

# Middleware system
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewarePipeline,
    RetryMiddleware,
    create_default_pipeline,
)

# Registry and discovery
from provide.foundation.transport.registry import (
    get_transport,
    get_transport_info,
    list_registered_transports,
    register_transport,
)

# High-level client API
from provide.foundation.transport.client import (
    UniversalClient,
    delete,
    get,
    get_default_client,
    head,
    options,
    patch,
    post,
    put,
    request,
    stream,
)

__all__ = [
    # Core abstractions
    "Request",
    "Response",
    
    # Configuration
    "TransportConfig",
    "HTTPConfig",
    
    # Types
    "TransportType",
    "HTTPMethod",
    
    # Errors
    "TransportError",
    "TransportConnectionError",
    "TransportTimeoutError", 
    "HTTPResponseError",
    "TransportNotFoundError",
    
    # Transport implementations
    "HTTPTransport",
    
    # Middleware
    "Middleware",
    "MiddlewarePipeline",
    "LoggingMiddleware",
    "RetryMiddleware",
    "MetricsMiddleware",
    "create_default_pipeline",
    
    # Registry
    "register_transport",
    "get_transport",
    "get_transport_info",
    "list_registered_transports",
    
    # Client API
    "UniversalClient",
    "get_default_client",
    "request",
    "get",
    "post",
    "put",
    "patch", 
    "delete",
    "head",
    "options",
    "stream",
]