"""
Transport middleware system with Hub registration.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any

from attrs import define, field

from provide.foundation.hub import get_component_registry
from provide.foundation.hub.components import ComponentCategory
from provide.foundation.logger import get_logger
from provide.foundation.metrics import counter, histogram
from provide.foundation.resilience.retry import BackoffStrategy, RetryExecutor, RetryPolicy
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.errors import TransportError

log = get_logger(__name__)


class Middleware(ABC):
    """Abstract base class for transport middleware."""
    
    @abstractmethod
    async def process_request(self, request: Request) -> Request:
        """Process request before sending."""
        pass
    
    @abstractmethod 
    async def process_response(self, response: Response) -> Response:
        """Process response after receiving."""
        pass
    
    @abstractmethod
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Process errors during request."""
        pass


@define
class LoggingMiddleware(Middleware):
    """Built-in telemetry middleware using foundation.logger."""
    
    log_requests: bool = field(default=True)
    log_responses: bool = field(default=True)
    log_bodies: bool = field(default=False)
    
    async def process_request(self, request: Request) -> Request:
        """Log outgoing request."""
        if self.log_requests:
            log.info(
                f"🚀 {request.method} {request.uri}",
                method=request.method,
                uri=str(request.uri),
                headers=dict(request.headers) if hasattr(request, 'headers') else {},
            )
            
            if self.log_bodies and request.body:
                log.trace("Request body", body=request.body, method=request.method, uri=str(request.uri))
        
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Log incoming response."""
        if self.log_responses:
            status_emoji = self._get_status_emoji(response.status)
            log.info(
                f"{status_emoji} {response.status} ({response.elapsed_ms:.0f}ms)",
                status_code=response.status,
                elapsed_ms=response.elapsed_ms,
                method=response.request.method if response.request else None,
                uri=str(response.request.uri) if response.request else None,
                headers=dict(response.headers) if hasattr(response, 'headers') else {},
            )
            
            if self.log_bodies and response.body:
                log.trace(
                    "Response body", 
                    body=response.text[:500],  # Truncate large bodies
                    status_code=response.status,
                    method=response.request.method if response.request else None,
                    uri=str(response.request.uri) if response.request else None,
                )
        
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Log errors."""
        log.error(
            f"❌ {request.method} {request.uri} failed: {error}",
            method=request.method,
            uri=str(request.uri),
            error_type=error.__class__.__name__,
            error_message=str(error),
        )
        return error
    
    def _get_status_emoji(self, status_code: int) -> str:
        """Get emoji for status code."""
        if 200 <= status_code < 300:
            return "✅"
        elif 300 <= status_code < 400:
            return "↩️" 
        elif 400 <= status_code < 500:
            return "⚠️"
        elif 500 <= status_code < 600:
            return "❌"
        else:
            return "❓"


@define
class RetryMiddleware(Middleware):
    """Automatic retry middleware using unified retry logic."""
    
    policy: RetryPolicy = field(
        factory=lambda: RetryPolicy(
            max_attempts=3,
            base_delay=0.5,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(TransportError,),
            retryable_status_codes={500, 502, 503, 504},
        )
    )
    
    async def process_request(self, request: Request) -> Request:
        """No request processing needed."""
        return request
    
    async def process_response(self, response: Response) -> Response:
        """No response processing needed (retries handled in execute)."""
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Handle error, potentially with retries (this is called by client)."""
        return error
    
    async def execute_with_retry(self, execute_func, request: Request) -> Response:
        """Execute request with retry logic using unified RetryExecutor."""
        executor = RetryExecutor(self.policy)
        
        async def wrapped():
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


@define
class MetricsMiddleware(Middleware):
    """Middleware for collecting transport metrics using foundation.metrics."""
    
    # Create metrics instances
    _request_counter = counter(
        "transport_requests_total",
        description="Total number of transport requests",
        unit="requests"
    )
    _request_duration = histogram(
        "transport_request_duration_seconds", 
        description="Duration of transport requests",
        unit="seconds"
    )
    _error_counter = counter(
        "transport_errors_total",
        description="Total number of transport errors", 
        unit="errors"
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
            self._request_counter.inc(1, 
                method=method,
                status_code=str(response.status),
                status_class=status_class
            )
            
            self._request_duration.observe(duration,
                method=method,
                status_class=status_class
            )
        
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Record error metrics."""
        method = request.method
        error_type = error.__class__.__name__
        
        self._error_counter.inc(1,
            method=method,
            error_type=error_type
        )
        
        return error


@define
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
    **metadata
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
            **metadata
        },
        replace=True,
    )
    
    log.debug(f"Registered middleware {middleware_class.__name__} as '{name}'")


def get_middleware_by_category(category: str = "transport.middleware") -> list[type[Middleware]]:
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


def create_default_pipeline() -> MiddlewarePipeline:
    """Create pipeline with default middleware."""
    pipeline = MiddlewarePipeline()
    
    # Add built-in middleware
    pipeline.add(LoggingMiddleware())
    pipeline.add(MetricsMiddleware())
    
    return pipeline


# Auto-register built-in middleware
def _register_builtin_middleware():
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
    "Middleware",
    "LoggingMiddleware",
    "RetryMiddleware", 
    "MetricsMiddleware",
    "MiddlewarePipeline",
    "register_middleware",
    "get_middleware_by_category",
    "create_default_pipeline",
]