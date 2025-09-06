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
            log.info(f"🚀 {request.method} {request.uri}")
            
            if self.log_bodies and request.body:
                log.trace("Request body", body=request.body)
        
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Log incoming response."""
        if self.log_responses:
            status_emoji = self._get_status_emoji(response.status)
            log.info(f"{status_emoji} {response.status} ({response.elapsed_ms:.0f}ms)")
            
            if self.log_bodies and response.body:
                log.trace("Response body", body=response.text[:500])  # Truncate large bodies
        
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Log errors."""
        log.error(f"❌ {request.method} {request.uri} failed: {error}")
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
    """Automatic retry middleware with exponential backoff."""
    
    max_retries: int = field(default=3)
    backoff_factor: float = field(default=0.5)
    retryable_status_codes: set[int] = field(factory=lambda: {500, 502, 503, 504})
    retryable_exceptions: tuple[type[Exception], ...] = field(
        factory=lambda: (TransportError,)
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
        """Execute request with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await execute_func(request)
                
                # Check if status code is retryable
                if response.status in self.retryable_status_codes and attempt < self.max_retries:
                    wait_time = self.backoff_factor * (2 ** attempt)
                    log.info(f"🔄 Retry {attempt + 1}/{self.max_retries} after {wait_time:.1f}s (status {response.status})")
                    await asyncio.sleep(wait_time)
                    continue
                
                return response
                
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    wait_time = self.backoff_factor * (2 ** attempt)
                    log.info(f"🔄 Retry {attempt + 1}/{self.max_retries} after {wait_time:.1f}s (error: {e})")
                    await asyncio.sleep(wait_time)
                else:
                    break
        
        # All retries exhausted
        if last_exception:
            raise last_exception
        else:
            # This shouldn't happen, but just in case
            raise TransportError("Max retries exceeded")


@define
class MetricsMiddleware(Middleware):
    """Middleware for collecting transport metrics."""
    
    metrics: dict[str, Any] = field(factory=dict, init=False)
    
    async def process_request(self, request: Request) -> Request:
        """Record request start time."""
        request.metadata["start_time"] = time.perf_counter()
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Record response metrics."""
        if response.request and "start_time" in response.request.metadata:
            start_time = response.request.metadata["start_time"]
            total_time = time.perf_counter() - start_time
            
            # Update metrics
            method = response.request.method
            status = response.status
            
            if method not in self.metrics:
                self.metrics[method] = {"count": 0, "total_time": 0.0, "statuses": {}}
            
            self.metrics[method]["count"] += 1
            self.metrics[method]["total_time"] += total_time
            
            if status not in self.metrics[method]["statuses"]:
                self.metrics[method]["statuses"][status] = 0
            self.metrics[method]["statuses"][status] += 1
        
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Record error metrics."""
        method = request.method
        
        if method not in self.metrics:
            self.metrics[method] = {"count": 0, "total_time": 0.0, "errors": 0}
        
        self.metrics[method]["errors"] = self.metrics[method].get("errors", 0) + 1
        return error
    
    def get_metrics(self) -> dict[str, Any]:
        """Get collected metrics."""
        return dict(self.metrics)
    
    def reset_metrics(self) -> None:
        """Reset collected metrics."""
        self.metrics.clear()


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
    
    log.trace(f"Registered middleware {middleware_class.__name__} as '{name}'")


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