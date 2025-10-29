# provide/foundation/transport/middleware.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


def x_register_middleware__mutmut_orig(
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


def x_register_middleware__mutmut_1(
    name: str,
    middleware_class: type[Middleware],
    category: str = "XXtransport.middlewareXX",
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


def x_register_middleware__mutmut_2(
    name: str,
    middleware_class: type[Middleware],
    category: str = "TRANSPORT.MIDDLEWARE",
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


def x_register_middleware__mutmut_3(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = None

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


def x_register_middleware__mutmut_4(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
        name=None,
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


def x_register_middleware__mutmut_5(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
        name=name,
        value=None,
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


def x_register_middleware__mutmut_6(
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
        dimension=None,
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


def x_register_middleware__mutmut_7(
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
        metadata=None,
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_8(
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
        replace=None,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_9(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
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


def x_register_middleware__mutmut_10(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
        name=name,
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


def x_register_middleware__mutmut_11(
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


def x_register_middleware__mutmut_12(
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
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_13(
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
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_14(
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
            "XXcategoryXX": category,
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


def x_register_middleware__mutmut_15(
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
            "CATEGORY": category,
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


def x_register_middleware__mutmut_16(
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
            "XXpriorityXX": metadata.get("priority", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_17(
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
            "PRIORITY": metadata.get("priority", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_18(
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
            "priority": metadata.get(None, 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_19(
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
            "priority": metadata.get("priority", None),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_20(
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
            "priority": metadata.get(100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_21(
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
            "priority": metadata.get(
                "priority",
            ),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_22(
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
            "priority": metadata.get("XXpriorityXX", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_23(
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
            "priority": metadata.get("PRIORITY", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_24(
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
            "priority": metadata.get("priority", 101),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_25(
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
            "XXclass_nameXX": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_26(
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
            "CLASS_NAME": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def x_register_middleware__mutmut_27(
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
        replace=False,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


x_register_middleware__mutmut_mutants: ClassVar[MutantDict] = {
    "x_register_middleware__mutmut_1": x_register_middleware__mutmut_1,
    "x_register_middleware__mutmut_2": x_register_middleware__mutmut_2,
    "x_register_middleware__mutmut_3": x_register_middleware__mutmut_3,
    "x_register_middleware__mutmut_4": x_register_middleware__mutmut_4,
    "x_register_middleware__mutmut_5": x_register_middleware__mutmut_5,
    "x_register_middleware__mutmut_6": x_register_middleware__mutmut_6,
    "x_register_middleware__mutmut_7": x_register_middleware__mutmut_7,
    "x_register_middleware__mutmut_8": x_register_middleware__mutmut_8,
    "x_register_middleware__mutmut_9": x_register_middleware__mutmut_9,
    "x_register_middleware__mutmut_10": x_register_middleware__mutmut_10,
    "x_register_middleware__mutmut_11": x_register_middleware__mutmut_11,
    "x_register_middleware__mutmut_12": x_register_middleware__mutmut_12,
    "x_register_middleware__mutmut_13": x_register_middleware__mutmut_13,
    "x_register_middleware__mutmut_14": x_register_middleware__mutmut_14,
    "x_register_middleware__mutmut_15": x_register_middleware__mutmut_15,
    "x_register_middleware__mutmut_16": x_register_middleware__mutmut_16,
    "x_register_middleware__mutmut_17": x_register_middleware__mutmut_17,
    "x_register_middleware__mutmut_18": x_register_middleware__mutmut_18,
    "x_register_middleware__mutmut_19": x_register_middleware__mutmut_19,
    "x_register_middleware__mutmut_20": x_register_middleware__mutmut_20,
    "x_register_middleware__mutmut_21": x_register_middleware__mutmut_21,
    "x_register_middleware__mutmut_22": x_register_middleware__mutmut_22,
    "x_register_middleware__mutmut_23": x_register_middleware__mutmut_23,
    "x_register_middleware__mutmut_24": x_register_middleware__mutmut_24,
    "x_register_middleware__mutmut_25": x_register_middleware__mutmut_25,
    "x_register_middleware__mutmut_26": x_register_middleware__mutmut_26,
    "x_register_middleware__mutmut_27": x_register_middleware__mutmut_27,
}


def register_middleware(*args, **kwargs):
    result = _mutmut_trampoline(
        x_register_middleware__mutmut_orig, x_register_middleware__mutmut_mutants, args, kwargs
    )
    return result


register_middleware.__signature__ = _mutmut_signature(x_register_middleware__mutmut_orig)
x_register_middleware__mutmut_orig.__name__ = "x_register_middleware"


def x_get_middleware_by_category__mutmut_orig(
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


def x_get_middleware_by_category__mutmut_1(
    category: str = "XXtransport.middlewareXX",
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


def x_get_middleware_by_category__mutmut_2(
    category: str = "TRANSPORT.MIDDLEWARE",
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


def x_get_middleware_by_category__mutmut_3(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = None
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_4(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = None

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_5(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension != category:
            priority = entry.metadata.get("priority", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_6(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = None
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_7(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get(None, 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_8(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", None)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_9(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get(100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_10(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get(
                "priority",
            )
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_11(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("XXpriorityXX", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_12(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("PRIORITY", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_13(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 101)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_14(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 100)
            middleware.append(None)

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_15(
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
    middleware.sort(key=None)
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_16(
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
    middleware.sort(key=lambda x: None)
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_17(
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
    middleware.sort(key=lambda x: x[2])
    return [mw[0] for mw in middleware]


def x_get_middleware_by_category__mutmut_18(
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
    return [mw[1] for mw in middleware]


x_get_middleware_by_category__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_middleware_by_category__mutmut_1": x_get_middleware_by_category__mutmut_1,
    "x_get_middleware_by_category__mutmut_2": x_get_middleware_by_category__mutmut_2,
    "x_get_middleware_by_category__mutmut_3": x_get_middleware_by_category__mutmut_3,
    "x_get_middleware_by_category__mutmut_4": x_get_middleware_by_category__mutmut_4,
    "x_get_middleware_by_category__mutmut_5": x_get_middleware_by_category__mutmut_5,
    "x_get_middleware_by_category__mutmut_6": x_get_middleware_by_category__mutmut_6,
    "x_get_middleware_by_category__mutmut_7": x_get_middleware_by_category__mutmut_7,
    "x_get_middleware_by_category__mutmut_8": x_get_middleware_by_category__mutmut_8,
    "x_get_middleware_by_category__mutmut_9": x_get_middleware_by_category__mutmut_9,
    "x_get_middleware_by_category__mutmut_10": x_get_middleware_by_category__mutmut_10,
    "x_get_middleware_by_category__mutmut_11": x_get_middleware_by_category__mutmut_11,
    "x_get_middleware_by_category__mutmut_12": x_get_middleware_by_category__mutmut_12,
    "x_get_middleware_by_category__mutmut_13": x_get_middleware_by_category__mutmut_13,
    "x_get_middleware_by_category__mutmut_14": x_get_middleware_by_category__mutmut_14,
    "x_get_middleware_by_category__mutmut_15": x_get_middleware_by_category__mutmut_15,
    "x_get_middleware_by_category__mutmut_16": x_get_middleware_by_category__mutmut_16,
    "x_get_middleware_by_category__mutmut_17": x_get_middleware_by_category__mutmut_17,
    "x_get_middleware_by_category__mutmut_18": x_get_middleware_by_category__mutmut_18,
}


def get_middleware_by_category(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_middleware_by_category__mutmut_orig, x_get_middleware_by_category__mutmut_mutants, args, kwargs
    )
    return result


get_middleware_by_category.__signature__ = _mutmut_signature(x_get_middleware_by_category__mutmut_orig)
x_get_middleware_by_category__mutmut_orig.__name__ = "x_get_middleware_by_category"


def x_create_default_pipeline__mutmut_orig(
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


def x_create_default_pipeline__mutmut_1(
    enable_retry: bool = False,
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


def x_create_default_pipeline__mutmut_2(
    enable_retry: bool = True,
    enable_logging: bool = False,
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


def x_create_default_pipeline__mutmut_3(
    enable_retry: bool = True,
    enable_logging: bool = True,
    enable_metrics: bool = False,
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


def x_create_default_pipeline__mutmut_4(
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
    pipeline = None

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


def x_create_default_pipeline__mutmut_5(
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
        retry_policy = None
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_6(
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
            max_attempts=None,
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


def x_create_default_pipeline__mutmut_7(
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
            backoff=None,
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


def x_create_default_pipeline__mutmut_8(
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
            base_delay=None,
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


def x_create_default_pipeline__mutmut_9(
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
            max_delay=None,
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


def x_create_default_pipeline__mutmut_10(
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
            retryable_status_codes=None,
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_11(
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


def x_create_default_pipeline__mutmut_12(
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


def x_create_default_pipeline__mutmut_13(
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


def x_create_default_pipeline__mutmut_14(
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
            retryable_status_codes={408, 429, 500, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_15(
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
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_16(
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
            max_attempts=4,
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


def x_create_default_pipeline__mutmut_17(
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
            base_delay=2.0,
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


def x_create_default_pipeline__mutmut_18(
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
            max_delay=11.0,
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


def x_create_default_pipeline__mutmut_19(
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
            retryable_status_codes={409, 429, 500, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_20(
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
            retryable_status_codes={408, 430, 500, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_21(
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
            retryable_status_codes={408, 429, 501, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_22(
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
            retryable_status_codes={408, 429, 500, 503, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_23(
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
            retryable_status_codes={408, 429, 500, 502, 504, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_24(
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
            retryable_status_codes={408, 429, 500, 502, 503, 505},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_25(
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
        pipeline.add(None)

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_26(
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
        pipeline.add(RetryMiddleware(policy=None))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_27(
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
        pipeline.add(None)

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


def x_create_default_pipeline__mutmut_28(
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
        pipeline.add(None)

    return pipeline


x_create_default_pipeline__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_default_pipeline__mutmut_1": x_create_default_pipeline__mutmut_1,
    "x_create_default_pipeline__mutmut_2": x_create_default_pipeline__mutmut_2,
    "x_create_default_pipeline__mutmut_3": x_create_default_pipeline__mutmut_3,
    "x_create_default_pipeline__mutmut_4": x_create_default_pipeline__mutmut_4,
    "x_create_default_pipeline__mutmut_5": x_create_default_pipeline__mutmut_5,
    "x_create_default_pipeline__mutmut_6": x_create_default_pipeline__mutmut_6,
    "x_create_default_pipeline__mutmut_7": x_create_default_pipeline__mutmut_7,
    "x_create_default_pipeline__mutmut_8": x_create_default_pipeline__mutmut_8,
    "x_create_default_pipeline__mutmut_9": x_create_default_pipeline__mutmut_9,
    "x_create_default_pipeline__mutmut_10": x_create_default_pipeline__mutmut_10,
    "x_create_default_pipeline__mutmut_11": x_create_default_pipeline__mutmut_11,
    "x_create_default_pipeline__mutmut_12": x_create_default_pipeline__mutmut_12,
    "x_create_default_pipeline__mutmut_13": x_create_default_pipeline__mutmut_13,
    "x_create_default_pipeline__mutmut_14": x_create_default_pipeline__mutmut_14,
    "x_create_default_pipeline__mutmut_15": x_create_default_pipeline__mutmut_15,
    "x_create_default_pipeline__mutmut_16": x_create_default_pipeline__mutmut_16,
    "x_create_default_pipeline__mutmut_17": x_create_default_pipeline__mutmut_17,
    "x_create_default_pipeline__mutmut_18": x_create_default_pipeline__mutmut_18,
    "x_create_default_pipeline__mutmut_19": x_create_default_pipeline__mutmut_19,
    "x_create_default_pipeline__mutmut_20": x_create_default_pipeline__mutmut_20,
    "x_create_default_pipeline__mutmut_21": x_create_default_pipeline__mutmut_21,
    "x_create_default_pipeline__mutmut_22": x_create_default_pipeline__mutmut_22,
    "x_create_default_pipeline__mutmut_23": x_create_default_pipeline__mutmut_23,
    "x_create_default_pipeline__mutmut_24": x_create_default_pipeline__mutmut_24,
    "x_create_default_pipeline__mutmut_25": x_create_default_pipeline__mutmut_25,
    "x_create_default_pipeline__mutmut_26": x_create_default_pipeline__mutmut_26,
    "x_create_default_pipeline__mutmut_27": x_create_default_pipeline__mutmut_27,
    "x_create_default_pipeline__mutmut_28": x_create_default_pipeline__mutmut_28,
}


def create_default_pipeline(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_default_pipeline__mutmut_orig, x_create_default_pipeline__mutmut_mutants, args, kwargs
    )
    return result


create_default_pipeline.__signature__ = _mutmut_signature(x_create_default_pipeline__mutmut_orig)
x_create_default_pipeline__mutmut_orig.__name__ = "x_create_default_pipeline"


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_orig() -> None:
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_1() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_2() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_3() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description=None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_4() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_5() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_6() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_7() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_8() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_9() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "XXloggingXX",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_10() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "LOGGING",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_11() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="XXBuilt-in request/response loggingXX",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_12() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="built-in request/response logging",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_13() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="BUILT-IN REQUEST/RESPONSE LOGGING",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_14() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=11,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_15() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
            None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_16() -> None:
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
            None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_17() -> None:
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
            description=None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_18() -> None:
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
            priority=None,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_19() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_20() -> None:
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_21() -> None:
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_22() -> None:
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_23() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
            "XXretryXX",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_24() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
            "RETRY",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_25() -> None:
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
            description="XXAutomatic retry with exponential backoffXX",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_26() -> None:
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
            description="automatic retry with exponential backoff",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_27() -> None:
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
            description="AUTOMATIC RETRY WITH EXPONENTIAL BACKOFF",
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_28() -> None:
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
            priority=21,
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


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_29() -> None:
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
            None,
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_30() -> None:
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
            None,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_31() -> None:
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
            description=None,
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_32() -> None:
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
            priority=None,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_33() -> None:
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
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_34() -> None:
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
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_35() -> None:
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
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_36() -> None:
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
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_37() -> None:
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
            "XXmetricsXX",
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_38() -> None:
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
            "METRICS",
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_39() -> None:
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
            description="XXRequest/response metrics collectionXX",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_40() -> None:
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
            description="request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_41() -> None:
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
            description="REQUEST/RESPONSE METRICS COLLECTION",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Auto-register built-in middleware
def x__register_builtin_middleware__mutmut_42() -> None:
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
            priority=31,
        )

    except ImportError:
        # Registry not available yet
        pass


x__register_builtin_middleware__mutmut_mutants: ClassVar[MutantDict] = {
    "x__register_builtin_middleware__mutmut_1": x__register_builtin_middleware__mutmut_1,
    "x__register_builtin_middleware__mutmut_2": x__register_builtin_middleware__mutmut_2,
    "x__register_builtin_middleware__mutmut_3": x__register_builtin_middleware__mutmut_3,
    "x__register_builtin_middleware__mutmut_4": x__register_builtin_middleware__mutmut_4,
    "x__register_builtin_middleware__mutmut_5": x__register_builtin_middleware__mutmut_5,
    "x__register_builtin_middleware__mutmut_6": x__register_builtin_middleware__mutmut_6,
    "x__register_builtin_middleware__mutmut_7": x__register_builtin_middleware__mutmut_7,
    "x__register_builtin_middleware__mutmut_8": x__register_builtin_middleware__mutmut_8,
    "x__register_builtin_middleware__mutmut_9": x__register_builtin_middleware__mutmut_9,
    "x__register_builtin_middleware__mutmut_10": x__register_builtin_middleware__mutmut_10,
    "x__register_builtin_middleware__mutmut_11": x__register_builtin_middleware__mutmut_11,
    "x__register_builtin_middleware__mutmut_12": x__register_builtin_middleware__mutmut_12,
    "x__register_builtin_middleware__mutmut_13": x__register_builtin_middleware__mutmut_13,
    "x__register_builtin_middleware__mutmut_14": x__register_builtin_middleware__mutmut_14,
    "x__register_builtin_middleware__mutmut_15": x__register_builtin_middleware__mutmut_15,
    "x__register_builtin_middleware__mutmut_16": x__register_builtin_middleware__mutmut_16,
    "x__register_builtin_middleware__mutmut_17": x__register_builtin_middleware__mutmut_17,
    "x__register_builtin_middleware__mutmut_18": x__register_builtin_middleware__mutmut_18,
    "x__register_builtin_middleware__mutmut_19": x__register_builtin_middleware__mutmut_19,
    "x__register_builtin_middleware__mutmut_20": x__register_builtin_middleware__mutmut_20,
    "x__register_builtin_middleware__mutmut_21": x__register_builtin_middleware__mutmut_21,
    "x__register_builtin_middleware__mutmut_22": x__register_builtin_middleware__mutmut_22,
    "x__register_builtin_middleware__mutmut_23": x__register_builtin_middleware__mutmut_23,
    "x__register_builtin_middleware__mutmut_24": x__register_builtin_middleware__mutmut_24,
    "x__register_builtin_middleware__mutmut_25": x__register_builtin_middleware__mutmut_25,
    "x__register_builtin_middleware__mutmut_26": x__register_builtin_middleware__mutmut_26,
    "x__register_builtin_middleware__mutmut_27": x__register_builtin_middleware__mutmut_27,
    "x__register_builtin_middleware__mutmut_28": x__register_builtin_middleware__mutmut_28,
    "x__register_builtin_middleware__mutmut_29": x__register_builtin_middleware__mutmut_29,
    "x__register_builtin_middleware__mutmut_30": x__register_builtin_middleware__mutmut_30,
    "x__register_builtin_middleware__mutmut_31": x__register_builtin_middleware__mutmut_31,
    "x__register_builtin_middleware__mutmut_32": x__register_builtin_middleware__mutmut_32,
    "x__register_builtin_middleware__mutmut_33": x__register_builtin_middleware__mutmut_33,
    "x__register_builtin_middleware__mutmut_34": x__register_builtin_middleware__mutmut_34,
    "x__register_builtin_middleware__mutmut_35": x__register_builtin_middleware__mutmut_35,
    "x__register_builtin_middleware__mutmut_36": x__register_builtin_middleware__mutmut_36,
    "x__register_builtin_middleware__mutmut_37": x__register_builtin_middleware__mutmut_37,
    "x__register_builtin_middleware__mutmut_38": x__register_builtin_middleware__mutmut_38,
    "x__register_builtin_middleware__mutmut_39": x__register_builtin_middleware__mutmut_39,
    "x__register_builtin_middleware__mutmut_40": x__register_builtin_middleware__mutmut_40,
    "x__register_builtin_middleware__mutmut_41": x__register_builtin_middleware__mutmut_41,
    "x__register_builtin_middleware__mutmut_42": x__register_builtin_middleware__mutmut_42,
}


def _register_builtin_middleware(*args, **kwargs):
    result = _mutmut_trampoline(
        x__register_builtin_middleware__mutmut_orig,
        x__register_builtin_middleware__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_register_builtin_middleware.__signature__ = _mutmut_signature(x__register_builtin_middleware__mutmut_orig)
x__register_builtin_middleware__mutmut_orig.__name__ = "x__register_builtin_middleware"


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


# <3 🧱🤝🚚🪄
