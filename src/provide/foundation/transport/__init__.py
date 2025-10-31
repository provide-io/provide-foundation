#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

# Core transport abstractions
from provide.foundation.transport.base import Request, Response

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

# Transport types and configuration
from provide.foundation.transport.config import HTTPConfig, TransportConfig

# Error types
from provide.foundation.transport.errors import (
    HTTPResponseError,
    TransportConnectionError,
    TransportError,
    TransportNotFoundError,
    TransportTimeoutError,
)

# Transport implementations
try:
    from provide.foundation.transport.http import HTTPTransport

    _HAS_HTTPX = True
except ImportError:
    from provide.foundation.utils.stubs import create_dependency_stub

    _HAS_HTTPX = False
    HTTPTransport = create_dependency_stub("httpx", "transport")  # type: ignore[misc,assignment]

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

# Type definitions for client code
from provide.foundation.transport.types import (
    Data,
    Headers,
    HTTPMethod,
    Params,
    TransportType,
)

"""Provide Foundation Transport System
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
    ...     body={"name": John, "email": "john@example.com"}
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

__all__ = [
    # Internal flags (for tests)
    "_HAS_HTTPX",
    # Types
    "Data",
    "HTTPConfig",
    "HTTPMethod",
    "HTTPResponseError",
    # Transport implementations
    "HTTPTransport",
    "Headers",
    "LoggingMiddleware",
    "MetricsMiddleware",
    # Middleware
    "Middleware",
    "MiddlewarePipeline",
    # Core abstractions
    "Params",
    "Request",
    "Response",
    "RetryMiddleware",
    # Configuration
    "TransportConfig",
    "TransportConnectionError",
    # Errors
    "TransportError",
    "TransportNotFoundError",
    "TransportTimeoutError",
    # Types
    "TransportType",
    # Client API
    "UniversalClient",
    "create_default_pipeline",
    "delete",
    "get",
    "get_default_client",
    "get_transport",
    "get_transport_info",
    "head",
    "list_registered_transports",
    "options",
    "patch",
    "post",
    "put",
    # Registry
    "register_transport",
    "request",
    "stream",
]

# 🧱🏗️🔚
