#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
import time
from typing import Any

from attrs import define, field

from provide.foundation.hub import get_component_registry
from provide.foundation.logger import get_logger
from provide.foundation.metrics import counter, histogram
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)
from provide.foundation.security import sanitize_headers, sanitize_uri
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.defaults import (
    DEFAULT_TRANSPORT_LOG_BODIES,
    DEFAULT_TRANSPORT_LOG_REQUESTS,
    DEFAULT_TRANSPORT_LOG_RESPONSES,
)
from provide.foundation.transport.errors import TransportError

"""Transport middleware system with Hub registration."""

log = get_logger(__name__)


class Middleware(ABC):
    """Abstract base class for transport middleware."""

    @abstractmethod
    async def process_request(self, request: Request) -> Request:
        """Process request before sending."""

    @abstractmethod
    async def process_response(self, response: Response) -> Response:
        """Process response after receiving."""

    @abstractmethod
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Process errors during request."""


@define(slots=True)
class LoggingMiddleware(Middleware):
    """Built-in telemetry middleware using foundation.logger."""

    log_requests: bool = field(default=DEFAULT_TRANSPORT_LOG_REQUESTS)
    log_responses: bool = field(default=DEFAULT_TRANSPORT_LOG_RESPONSES)
    log_bodies: bool = field(default=DEFAULT_TRANSPORT_LOG_BODIES)
    sanitize_logs: bool = field(default=True)

    async def process_request(self, request: Request) -> Request:
        """Log outgoing request."""
        if self.log_requests:
            # Sanitize URI and headers if enabled
            uri_str = str(request.uri)
            if self.sanitize_logs:
                uri_str = sanitize_uri(uri_str)
                headers = sanitize_headers(dict(request.headers)) if hasattr(request, "headers") else {}
            else:
                headers = dict(request.headers) if hasattr(request, "headers") else {}

            log.info(
                f"🚀 {request.method} {uri_str}",
                method=request.method,
                uri=uri_str,
                headers=headers,
            )

            if self.log_bodies and request.body:
                # Truncate request body to prevent logging secrets/PII
                body_str = str(request.body) if not isinstance(request.body, str) else request.body
                log.trace(
                    "Request body",
                    body=body_str[:500],  # Truncate large bodies (matches response behavior)
                    method=request.method,
                    uri=uri_str,
                )

        return request

    async def process_response(self, response: Response) -> Response:
        """Log incoming response."""
        if self.log_responses:
            # Sanitize URI and headers if enabled
            uri_str = str(response.request.uri) if response.request else None
            if self.sanitize_logs and uri_str:
                uri_str = sanitize_uri(uri_str)
                headers = sanitize_headers(dict(response.headers)) if hasattr(response, "headers") else {}
            else:
                headers = dict(response.headers) if hasattr(response, "headers") else {}

            status_emoji = self._get_status_emoji(response.status)
            log.info(
                f"{status_emoji} {response.status} ({response.elapsed_ms:.0f}ms)",
                status_code=response.status,
                elapsed_ms=response.elapsed_ms,
                method=response.request.method if response.request else None,
                uri=uri_str,
                headers=headers,
            )

            if self.log_bodies and response.body:
                log.trace(
                    "Response body",
                    body=response.text[:500],  # Truncate large bodies
                    status_code=response.status,
                    method=response.request.method if response.request else None,
                    uri=uri_str,
                )

        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Log errors."""
        # Sanitize URI if enabled
        uri_str = str(request.uri)
        if self.sanitize_logs:
            uri_str = sanitize_uri(uri_str)

        log.error(
            f"❌ {request.method} {uri_str} failed: {error}",
            method=request.method,
            uri=uri_str,
            error_type=error.__class__.__name__,
            error_message=str(error),
        )
        return error

    def _get_status_emoji(self, status_code: int) -> str:
        """Get emoji for status code."""
        if 200 <= status_code < 300:
            return "✅"
        if 300 <= status_code < 400:
            return "↩️"
        if 400 <= status_code < 500:
            return "⚠️"
        if 500 <= status_code < 600:
            return "❌"
        return "❓"


@define(slots=True)
class RetryMiddleware(Middleware):
    """Automatic retry middleware using unified retry logic."""

    policy: RetryPolicy = field(
        factory=lambda: RetryPolicy(
            max_attempts=3,
            base_delay=0.5,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(TransportError,),
            retryable_status_codes={500, 502, 503, 504},
        ),
    )
    time_source: Callable[[], float] | None = field(default=None)
    async_sleep_func: Callable[[float], Awaitable[None]] | None = field(default=None)

    async def process_request(self, request: Request) -> Request:
        """No request processing needed."""
        return request

    async def process_response(self, response: Response) -> Response:
        """No response processing needed (retries handled in execute)."""
        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Handle error, potentially with retries (this is called by client)."""
        return error

    async def execute_with_retry(
        self, execute_func: Callable[[Request], Awaitable[Response]], request: Request
    ) -> Response:
        """Execute request with retry logic using unified RetryExecutor."""
        executor = RetryExecutor(
            self.policy,
            time_source=self.time_source,
            async_sleep_func=self.async_sleep_func,
        )

        async def wrapped() -> Response:
            response = await execute_func(request)

            # Check if status code is retryable
            if self.policy.should_retry_response(response, attempt=1):
                # Convert to exception for executor to handle
                raise TransportError(f"Retryable HTTP status: {response.status}")

            return response

        try:
            return await executor.execute_async(wrapped)
        except TransportError as e:
            # If it's our synthetic error, extract the response
            if "Retryable HTTP status" in str(e):
                # The last response will be returned
                # For now, re-raise as this needs more sophisticated handling
                raise
            raise


@define(slots=True)
class MetricsMiddleware(Middleware):
    """Middleware for collecting transport metrics using foundation.metrics."""

    _counter_func: Callable = field(default=counter)
    _histogram_func: Callable = field(default=histogram)

    # Create metrics instances
    _request_counter: Any = field(init=False)
    _request_duration: Any = field(init=False)
    _error_counter: Any = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize metrics after creation."""
        self._request_counter = self._counter_func(
            "transport_requests_total",
            description="Total number of transport requests",
            unit="requests",
        )
        self._request_duration = self._histogram_func(
            "transport_request_duration_seconds",
            description="Duration of transport requests",
            unit="seconds",
        )
        self._error_counter = self._counter_func(
            "transport_errors_total",
            description="Total number of transport errors",
            unit="errors",
        )

    async def process_request(self, request: Request) -> Request:
        """Record request start time."""
        request.metadata["start_time"] = time.perf_counter()
        return request

    async def process_response(self, response: Response) -> Response:
        """Record response metrics."""
        if response.request and "start_time" in response.request.metadata:
            start_time = response.request.metadata["start_time"]
            duration = time.perf_counter() - start_time

            method = response.request.method
            status_class = f"{response.status // 100}xx"

            # Record metrics with labels
            self._request_counter.inc(
                1,
                method=method,
                status_code=str(response.status),
                status_class=status_class,
            )

            self._request_duration.observe(duration, method=method, status_class=status_class)

        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Record error metrics."""
        method = request.method
        error_type = error.__class__.__name__

        self._error_counter.inc(1, method=method, error_type=error_type)

        return error


@define(slots=True)
class MiddlewarePipeline:
    """Pipeline for executing middleware in order."""

    middleware: list[Middleware] = field(factory=list)

    def add(self, middleware: Middleware) -> None:
        """Add middleware to the pipeline."""
        self.middleware.append(middleware)
        log.trace(f"Added middleware: {middleware.__class__.__name__}")

    def remove(self, middleware_class: type[Middleware]) -> bool:
        """Remove middleware by class type."""
        for i, mw in enumerate(self.middleware):
            if isinstance(mw, middleware_class):
                del self.middleware[i]
                log.trace(f"Removed middleware: {middleware_class.__name__}")
                return True
        return False

    async def process_request(self, request: Request) -> Request:
        """Process request through all middleware."""
        for mw in self.middleware:
            request = await mw.process_request(request)
        return request

    async def process_response(self, response: Response) -> Response:
        """Process response through all middleware (in reverse order)."""
        for mw in reversed(self.middleware):
            response = await mw.process_response(response)
        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Process error through all middleware."""
        for mw in self.middleware:
            error = await mw.process_error(error, request)
        return error


def register_middleware(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
        name=name,
        value=middleware_class,
        dimension=category,
        metadata={
            "category": category,
            "priority": metadata.get("priority", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def get_middleware_by_category(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def create_default_pipeline(
    enable_retry: bool = True,
    enable_logging: bool = True,
    enable_metrics: bool = True,
) -> MiddlewarePipeline:
    """Create pipeline with default middleware.

    Args:
        enable_retry: Enable automatic retry middleware (default: True)
        enable_logging: Enable request/response logging middleware (default: True)
        enable_metrics: Enable metrics collection middleware (default: True)

    Returns:
        Configured middleware pipeline

    """
    pipeline = MiddlewarePipeline()

    # Add retry middleware first (so retries happen before logging each attempt)
    if enable_retry:
        # Use sensible retry defaults
        retry_policy = RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
            max_delay=10.0,
            # Retry on common transient failures
            retryable_status_codes={408, 429, 500, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


# Auto-register built-in middleware
def _register_builtin_middleware() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
            "retry",
            RetryMiddleware,
            description="Automatic retry with exponential backoff",
            priority=20,
        )

        register_middleware(
            "metrics",
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Register when module is imported
_register_builtin_middleware()


__all__ = [
    "LoggingMiddleware",
    "MetricsMiddleware",
    "Middleware",
    "MiddlewarePipeline",
    "RetryMiddleware",
    "create_default_pipeline",
    "get_middleware_by_category",
    "register_middleware",
]

# 🧱🏗️🔚
