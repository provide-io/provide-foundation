# Transport Middleware

Extensible request/response processing pipeline for transport operations.

## Overview

Transport Middleware provides a pipeline architecture for processing HTTP requests and responses. It enables cross-cutting concerns like logging, metrics collection, retry logic, and custom request/response transformations.

## Core Abstractions

### Middleware Base Class

All middleware must implement the abstract `Middleware` class:

```python
from abc import ABC, abstractmethod
from provide.foundation.transport.base import Request, Response

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
```

### MiddlewarePipeline

The pipeline orchestrates middleware execution:

```python
from provide.foundation.transport.middleware import MiddlewarePipeline

pipeline = MiddlewarePipeline([
    LoggingMiddleware(),
    MetricsMiddleware(),
    RetryMiddleware()
])

# Pipeline is used automatically by UniversalClient
client = UniversalClient(middleware=pipeline)
```

## Built-in Middleware

### LoggingMiddleware

Provides comprehensive request/response logging using Foundation's structured logging:

```python
from provide.foundation.transport.middleware import LoggingMiddleware

@define
class LoggingMiddleware(Middleware):
    log_requests: bool = field(default=True)
    log_responses: bool = field(default=True)
    log_bodies: bool = field(default=False)
```

**Configuration:**
- `log_requests`: Log outgoing requests
- `log_responses`: Log incoming responses
- `log_bodies`: Include request/response bodies in logs (use with caution)

**Usage:**
```python
# Basic logging
logging_middleware = LoggingMiddleware()

# Detailed logging with bodies
detailed_logging = LoggingMiddleware(
    log_requests=True,
    log_responses=True,
    log_bodies=True  # Be careful with sensitive data
)

client = UniversalClient(
    middleware=MiddlewarePipeline([detailed_logging])
)
```

**Log Output:**
```
INFO: http_request_started method=GET uri=https://api.example.com/users
INFO: http_request_completed method=GET uri=https://api.example.com/users status=200 duration_ms=145
```

### MetricsMiddleware

Collects performance metrics for transport operations:

```python
from provide.foundation.transport.middleware import MetricsMiddleware

@define
class MetricsMiddleware(Middleware):
    """Built-in metrics collection middleware."""
```

**Metrics Collected:**
- Request count by method and status
- Response time histograms
- Error rates by transport type
- Connection pool statistics

**Usage:**
```python
metrics_middleware = MetricsMiddleware()

client = UniversalClient(
    middleware=MiddlewarePipeline([metrics_middleware])
)

# Metrics are automatically collected
response = await client.get("https://api.example.com/data")
```

### RetryMiddleware

Implements retry logic with configurable backoff strategies:

```python
from provide.foundation.transport.middleware import RetryMiddleware
from provide.foundation.resilience.retry import RetryPolicy, BackoffStrategy

# Default retry configuration
retry_middleware = RetryMiddleware()

# Custom retry policy
from provide.foundation.resilience.retry import RetryPolicy, BackoffStrategy

retry_policy = RetryPolicy(
    max_attempts=5,
    backoff=BackoffStrategy.EXPONENTIAL,
    base_delay=1.0,
    max_delay=30.0,
    jitter=True
)

retry_middleware = RetryMiddleware(policy=retry_policy)
```

**Configuration:**
- Uses `RetryPolicy` from the resilience module
- Supports exponential, linear, fixed, and Fibonacci backoff
- Configurable error types and HTTP status codes for retry

## Default Pipeline

### create_default_pipeline()

Creates a pre-configured middleware pipeline with common middleware:

```python
from provide.foundation.transport.middleware import create_default_pipeline

# Get default pipeline
pipeline = create_default_pipeline()

# Default includes:
# - LoggingMiddleware() 
# - MetricsMiddleware()
# - RetryMiddleware() with standard policy
```

## Custom Middleware

### Creating Custom Middleware

Implement the `Middleware` abstract class for custom functionality:

```python
from provide.foundation.transport.middleware import Middleware
from provide.foundation.transport.base import Request, Response
from provide.foundation.logger import get_logger

logger = get_logger(__name__)

class AuthenticationMiddleware(Middleware):
    """Add authentication headers to requests."""
    
    def __init__(self, token: str):
        self.token = token
    
    async def process_request(self, request: Request) -> Request:
        """Add Authorization header."""
        request.headers["Authorization"] = f"Bearer {self.token}"
        logger.debug("auth_header_added", uri=request.uri)
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Log authentication status."""
        if response.status == 401:
            logger.warning("authentication_failed", uri=response.request.uri)
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Handle authentication errors."""
        logger.error("auth_middleware_error", error=str(error))
        return error
```

### Request Transformation Middleware

```python
class RequestTransformMiddleware(Middleware):
    """Transform request data before sending."""
    
    async def process_request(self, request: Request) -> Request:
        """Transform request body."""
        if isinstance(request.body, dict):
            # Add timestamp to all requests
            request.body["timestamp"] = time.time()
            
            # Add request ID for tracking
            request_id = f"req_{uuid.uuid4().hex[:8]}"
            request.headers["X-Request-ID"] = request_id
            request.metadata["request_id"] = request_id
            
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Log request completion."""
        request_id = response.request.metadata.get("request_id")
        logger.info("request_completed", 
                   request_id=request_id, 
                   status=response.status,
                   duration_ms=response.elapsed_ms)
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Log request failure."""
        request_id = request.metadata.get("request_id")
        logger.error("request_failed", request_id=request_id, error=str(error))
        return error
```

### Response Caching Middleware

```python
import hashlib
from typing import Dict

class CachingMiddleware(Middleware):
    """Simple response caching middleware."""
    
    def __init__(self, cache_ttl: int = 300):
        self.cache: Dict[str, tuple[Response, float]] = {}
        self.cache_ttl = cache_ttl
    
    def _cache_key(self, request: Request) -> str:
        """Generate cache key for request."""
        key_data = f"{request.method}:{request.uri}:{str(request.params)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def process_request(self, request: Request) -> Request:
        """Check cache for GET requests."""
        if request.method.upper() == "GET":
            cache_key = self._cache_key(request)
            
            if cache_key in self.cache:
                cached_response, cached_time = self.cache[cache_key]
                
                if time.time() - cached_time < self.cache_ttl:
                    # Return cached response by storing in request metadata
                    request.metadata["cached_response"] = cached_response
                    logger.debug("cache_hit", uri=request.uri)
                    
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Cache successful GET responses."""
        request = response.request
        
        if (request.method.upper() == "GET" and 
            response.is_success() and 
            "cached_response" not in request.metadata):
            
            cache_key = self._cache_key(request)
            self.cache[cache_key] = (response, time.time())
            logger.debug("response_cached", uri=request.uri)
            
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """No special error handling for caching."""
        return error
```

## Pipeline Composition

### Middleware Ordering

Middleware execution order matters. The pipeline processes:

1. **Request Phase**: Middleware execute in order (first → last)
2. **Response Phase**: Middleware execute in reverse order (last → first)
3. **Error Phase**: All middleware process errors in order

```python
pipeline = MiddlewarePipeline([
    AuthenticationMiddleware("token123"),     # 1st: Add auth headers
    RequestTransformMiddleware(),             # 2nd: Transform request
    LoggingMiddleware(),                      # 3rd: Log request
    MetricsMiddleware(),                      # 4th: Start metrics
    RetryMiddleware(),                        # 5th: Handle retries
])

# Request flow: Auth → Transform → Logging → Metrics → Retry → Transport
# Response flow: Transport → Retry → Metrics → Logging → Transform → Auth
```

### Conditional Middleware

```python
class ConditionalMiddleware(Middleware):
    """Apply middleware only for specific conditions."""
    
    def __init__(self, condition: Callable[[Request], bool], 
                 wrapped_middleware: Middleware):
        self.condition = condition
        self.wrapped = wrapped_middleware
    
    async def process_request(self, request: Request) -> Request:
        if self.condition(request):
            return await self.wrapped.process_request(request)
        return request
    
    async def process_response(self, response: Response) -> Response:
        if self.condition(response.request):
            return await self.wrapped.process_response(response)
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        if self.condition(request):
            return await self.wrapped.process_error(error, request)
        return error

# Apply caching only for API calls
api_condition = lambda req: "api.example.com" in req.uri
conditional_cache = ConditionalMiddleware(api_condition, CachingMiddleware())
```

## Error Handling in Middleware

### Error Propagation

```python
class ErrorHandlingMiddleware(Middleware):
    """Handle and transform errors."""
    
    async def process_request(self, request: Request) -> Request:
        return request
    
    async def process_response(self, response: Response) -> Response:
        return response
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Transform or handle errors."""
        if isinstance(error, TimeoutError):
            # Convert to custom error
            return CustomTimeoutError(f"Request to {request.uri} timed out")
        
        if isinstance(error, ConnectionError):
            # Add context to error
            error.request_context = {
                "uri": request.uri,
                "method": request.method,
                "headers": dict(request.headers)
            }
        
        return error
```

### Error Recovery

```python
class ErrorRecoveryMiddleware(Middleware):
    """Attempt error recovery strategies."""
    
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Try to recover from certain errors."""
        
        if isinstance(error, HTTPResponseError) and error.status_code == 401:
            # Attempt token refresh
            if await self.refresh_auth_token():
                # Indicate retry should be attempted
                error.recoverable = True
                logger.info("auth_token_refreshed", uri=request.uri)
            
        return error
    
    async def refresh_auth_token(self) -> bool:
        """Refresh authentication token."""
        # Implementation for token refresh
        return True
```

## Testing Middleware

### Unit Testing

```python
import pytest
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.middleware import MiddlewarePipeline

@pytest.mark.asyncio
async def test_custom_middleware():
    middleware = AuthenticationMiddleware("test-token")
    
    request = Request(uri="https://api.example.com/data", method="GET")
    processed_request = await middleware.process_request(request)
    
    assert processed_request.headers["Authorization"] == "Bearer test-token"

@pytest.mark.asyncio
async def test_middleware_pipeline():
    pipeline = MiddlewarePipeline([
        AuthenticationMiddleware("token"),
        LoggingMiddleware(log_bodies=False)
    ])
    
    request = Request(uri="https://api.example.com/data", method="GET")
    processed_request = await pipeline.process_request(request)
    
    assert "Authorization" in processed_request.headers
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_middleware_with_client(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/data",
        json={"result": "success"},
        status_code=200
    )
    
    middleware = MiddlewarePipeline([
        AuthenticationMiddleware("test-token"),
        MetricsMiddleware()
    ])
    
    async with UniversalClient(middleware=middleware) as client:
        response = await client.get("https://api.example.com/data")
        
        assert response.is_success()
        # Verify middleware was applied
        # Check metrics, logs, etc.
```

## See Also

- [Transport Client](client.md) - UniversalClient and HTTP methods
- [Transport Registry](registry.md) - Transport discovery and registration
- [Resilience Patterns](../resilience/api-index.md) - Retry policies and patterns
- [Metrics](../metrics/api-index.md) - Metrics collection and reporting