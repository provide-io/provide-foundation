# Custom HTTP Middleware

Learn how to create custom HTTP middleware for logging, authentication, rate limiting, and more.

## Overview

Middleware allows you to intercept and modify HTTP requests and responses, enabling cross-cutting concerns like:
- **Logging** - Track all requests and responses
- **Authentication** - Verify API keys, tokens, or sessions
- **Rate Limiting** - Protect against abuse
- **Caching** - Cache responses for performance
- **Error Handling** - Centralized error responses
- **Request/Response Modification** - Add headers, transform payloads

Foundation's middleware system is compatible with modern Python HTTP clients and servers.

## Prerequisites

Install transport extras:
```bash
uv add provide-foundation[transport]
```

## Basic Middleware

### Logging Middleware

Log all HTTP requests and responses:

```python
from provide.foundation.transport import HTTPClient
from provide.foundation import logger

async def logging_middleware(request, call_next):
    """Log all HTTP requests and responses."""
    # Log request
    logger.info(
        "http_request",
        method=request.method,
        url=str(request.url),
        headers=dict(request.headers),
    )

    # Process request
    response = await call_next(request)

    # Log response
    logger.info(
        "http_response",
        status=response.status_code,
        url=str(request.url),
        duration_ms=response.elapsed.total_seconds() * 1000,
    )

    return response

# Use middleware
client = HTTPClient(middleware=[logging_middleware])
response = await client.get("https://api.example.com/data")
```

### Authentication Middleware

Add authentication headers to all requests:

```python
async def auth_middleware(request, call_next):
    """Add authentication header to all requests."""
    # Get token (from config, env, etc.)
    token = get_api_token()

    # Add authorization header
    request.headers["Authorization"] = f"Bearer {token}"

    return await call_next(request)

# Use middleware
client = HTTPClient(middleware=[auth_middleware])
```

### Timing Middleware

Measure request duration:

```python
import time

async def timing_middleware(request, call_next):
    """Measure request duration."""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        "request_timing",
        url=str(request.url),
        duration_seconds=duration,
        status=response.status_code,
    )

    return response
```

## Authentication Patterns

### API Key Authentication

Add API key to headers or query parameters:

```python
class APIKeyAuth:
    """API key authentication middleware."""

    def __init__(self, api_key, header_name="X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    async def __call__(self, request, call_next):
        """Add API key to request."""
        request.headers[self.header_name] = self.api_key
        return await call_next(request)

# Usage
api_key_auth = APIKeyAuth(api_key="secret-key-123")
client = HTTPClient(middleware=[api_key_auth])
```

### OAuth2 Bearer Token

Handle OAuth2 bearer token authentication:

```python
from datetime import datetime, timedelta

class OAuth2Middleware:
    """OAuth2 bearer token authentication."""

    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = None

    async def get_token(self):
        """Get or refresh access token."""
        # Check if token is still valid
        if self.token and self.token_expiry > datetime.now():
            return self.token

        # Request new token
        response = await httpx.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        data = response.json()

        # Store token and expiry
        self.token = data["access_token"]
        expires_in = data.get("expires_in", 3600)
        self.token_expiry = datetime.now() + timedelta(seconds=expires_in)

        logger.info("OAuth2 token refreshed", expires_in=expires_in)
        return self.token

    async def __call__(self, request, call_next):
        """Add bearer token to request."""
        token = await self.get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        return await call_next(request)

# Usage
oauth = OAuth2Middleware(
    token_url="https://auth.example.com/oauth/token",
    client_id="my-client-id",
    client_secret="my-client-secret",
)
client = HTTPClient(middleware=[oauth])
```

### JWT Token with Refresh

Automatically refresh JWT tokens:

```python
import jwt
from datetime import datetime

class JWTAuthMiddleware:
    """JWT authentication with automatic refresh."""

    def __init__(self, get_token_func, refresh_token_func):
        self.get_token = get_token_func
        self.refresh_token = refresh_token_func
        self.current_token = None

    def is_token_expired(self, token):
        """Check if JWT token is expired."""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = payload.get("exp")
            if exp:
                return datetime.fromtimestamp(exp) < datetime.now()
        except jwt.DecodeError:
            return True
        return False

    async def __call__(self, request, call_next):
        """Add JWT token, refreshing if needed."""
        # Get current token
        if not self.current_token:
            self.current_token = await self.get_token()

        # Refresh if expired
        if self.is_token_expired(self.current_token):
            logger.info("JWT token expired, refreshing")
            self.current_token = await self.refresh_token()

        # Add token to request
        request.headers["Authorization"] = f"Bearer {self.current_token}"
        return await call_next(request)
```

## Request Modification

### Add Custom Headers

Add standard headers to all requests:

```python
async def custom_headers_middleware(request, call_next):
    """Add custom headers to all requests."""
    request.headers["User-Agent"] = "MyApp/1.0"
    request.headers["X-Client-Version"] = "2.5.0"
    request.headers["X-Request-ID"] = str(uuid.uuid4())

    return await call_next(request)
```

### Request Body Transformation

Modify request payloads:

```python
import json

async def request_transform_middleware(request, call_next):
    """Transform request body."""
    if request.method in ["POST", "PUT", "PATCH"]:
        # Read current body
        body = json.loads(request.content)

        # Add metadata
        body["client_version"] = "1.0.0"
        body["timestamp"] = datetime.now().isoformat()

        # Update request body
        request.content = json.dumps(body).encode()
        request.headers["Content-Length"] = str(len(request.content))

    return await call_next(request)
```

### Query Parameter Injection

Add query parameters to all requests:

```python
from urllib.parse import urlencode, urlparse, parse_qs

async def query_param_middleware(request, call_next):
    """Add query parameters to all requests."""
    # Parse current URL
    parsed = urlparse(str(request.url))
    params = parse_qs(parsed.query)

    # Add new parameters
    params["api_version"] = ["2"]
    params["format"] = ["json"]

    # Rebuild URL
    new_query = urlencode(params, doseq=True)
    request.url = request.url.copy_with(query=new_query.encode())

    return await call_next(request)
```

## Response Handling

### Response Transformation

Modify response data:

```python
async def response_transform_middleware(request, call_next):
    """Transform response data."""
    response = await call_next(request)

    # Only transform JSON responses
    if "application/json" in response.headers.get("content-type", ""):
        data = response.json()

        # Add metadata
        transformed = {
            "data": data,
            "meta": {
                "request_id": response.headers.get("x-request-id"),
                "timestamp": datetime.now().isoformat(),
            },
        }

        # Create new response with transformed data
        response._content = json.dumps(transformed).encode()

    return response
```

### Error Response Handling

Standardize error responses:

```python
async def error_handling_middleware(request, call_next):
    """Handle and transform error responses."""
    try:
        response = await call_next(request)

        # Check for error status codes
        if response.status_code >= 400:
            logger.error(
                "http_error",
                status=response.status_code,
                url=str(request.url),
                response_body=response.text[:200],
            )

            # Optionally transform error response
            if response.status_code >= 500:
                # Server error
                raise ServerError(f"Server error: {response.status_code}")

        return response

    except httpx.RequestError as e:
        logger.exception("request_failed", url=str(request.url))
        raise NetworkError(f"Request failed: {e}") from e
```

## Rate Limiting

### Simple Rate Limiter

Implement client-side rate limiting:

```python
import asyncio
from collections import deque
from datetime import datetime, timedelta

class RateLimitMiddleware:
    """Client-side rate limiting middleware."""

    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = timedelta(seconds=time_window)
        self.requests = deque()

    async def __call__(self, request, call_next):
        """Enforce rate limit."""
        now = datetime.now()

        # Remove old requests outside time window
        cutoff = now - self.time_window
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

        # Check if rate limit exceeded
        if len(self.requests) >= self.max_requests:
            wait_time = (self.requests[0] + self.time_window - now).total_seconds()
            logger.warning(
                "rate_limit_reached",
                wait_seconds=wait_time,
                max_requests=self.max_requests,
            )
            await asyncio.sleep(wait_time)

        # Record this request
        self.requests.append(now)

        return await call_next(request)

# Usage: Max 100 requests per minute
rate_limiter = RateLimitMiddleware(max_requests=100, time_window=60)
client = HTTPClient(middleware=[rate_limiter])
```

### Token Bucket Rate Limiter

More sophisticated rate limiting:

```python
class TokenBucketRateLimiter:
    """Token bucket rate limiting."""

    def __init__(self, rate=10, burst=20):
        """
        Args:
            rate: Tokens added per second
            burst: Maximum bucket size
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()

    async def acquire(self):
        """Acquire a token, waiting if necessary."""
        while True:
            now = time.time()
            elapsed = now - self.last_update

            # Add new tokens based on elapsed time
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now

            # Try to acquire token
            if self.tokens >= 1:
                self.tokens -= 1
                return

            # Wait for next token
            wait_time = (1 - self.tokens) / self.rate
            await asyncio.sleep(wait_time)

    async def __call__(self, request, call_next):
        """Rate limit using token bucket."""
        await self.acquire()
        return await call_next(request)

# Usage: 10 requests/sec with burst of 20
rate_limiter = TokenBucketRateLimiter(rate=10, burst=20)
client = HTTPClient(middleware=[rate_limiter])
```

## Retry Middleware

Automatically retry failed requests:

```python
from provide.foundation.resilience import BackoffStrategy

class RetryMiddleware:
    """Retry failed requests with exponential backoff."""

    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def __call__(self, request, call_next):
        """Retry request on failure."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = await call_next(request)

                # Retry on 5xx errors
                if response.status_code < 500:
                    return response

                logger.warning(
                    "server_error_retrying",
                    status=response.status_code,
                    attempt=attempt + 1,
                    max_retries=self.max_retries,
                )

            except httpx.RequestError as e:
                last_exception = e
                logger.warning(
                    "request_error_retrying",
                    error=str(e),
                    attempt=attempt + 1,
                    max_retries=self.max_retries,
                )

            # Don't sleep after last attempt
            if attempt < self.max_retries:
                # Exponential backoff
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)

        # All retries failed
        if last_exception:
            raise last_exception
        return response  # Return last error response

# Usage
retry_middleware = RetryMiddleware(max_retries=3, base_delay=1.0)
client = HTTPClient(middleware=[retry_middleware])
```

## Caching Middleware

Cache responses for performance:

```python
from datetime import datetime, timedelta

class CachingMiddleware:
    """Cache HTTP responses."""

    def __init__(self, ttl=300):
        """
        Args:
            ttl: Cache time-to-live in seconds
        """
        self.ttl = timedelta(seconds=ttl)
        self.cache = {}

    def _cache_key(self, request):
        """Generate cache key from request."""
        return f"{request.method}:{str(request.url)}"

    async def __call__(self, request, call_next):
        """Cache GET requests."""
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        cache_key = self._cache_key(request)

        # Check cache
        if cache_key in self.cache:
            response, timestamp = self.cache[cache_key]
            age = datetime.now() - timestamp

            if age < self.ttl:
                logger.debug("cache_hit", url=str(request.url), age_seconds=age.total_seconds())
                return response

        # Cache miss - make request
        logger.debug("cache_miss", url=str(request.url))
        response = await call_next(request)

        # Cache successful responses
        if response.status_code == 200:
            self.cache[cache_key] = (response, datetime.now())

        return response

# Usage: Cache for 5 minutes
cache = CachingMiddleware(ttl=300)
client = HTTPClient(middleware=[cache])
```

## Middleware Composition

Combine multiple middleware:

```python
from provide.foundation.transport import HTTPClient
from provide.foundation import logger

# Create individual middleware
logging_mw = logging_middleware
auth_mw = auth_middleware
retry_mw = RetryMiddleware(max_retries=3)
cache_mw = CachingMiddleware(ttl=300)

# Compose middleware stack (order matters!)
client = HTTPClient(
    middleware=[
        logging_mw,    # 1. Log first (outermost)
        auth_mw,       # 2. Add auth
        cache_mw,      # 3. Check cache
        retry_mw,      # 4. Retry on failure (innermost)
    ]
)

# Middleware execution order:
# Request:  logging → auth → cache → retry → HTTP call
# Response: HTTP call → retry → cache → auth → logging
```

## Production Patterns

### Correlation ID Middleware

Track requests across services:

```python
import uuid
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id")

async def correlation_id_middleware(request, call_next):
    """Add correlation ID to requests."""
    # Get or generate correlation ID
    correlation_id = correlation_id_var.get(None) or str(uuid.uuid4())

    # Add to request headers
    request.headers["X-Correlation-ID"] = correlation_id

    # Make request
    response = await call_next(request)

    # Log for tracing
    logger.info(
        "http_request_completed",
        correlation_id=correlation_id,
        status=response.status_code,
    )

    return response
```

### Circuit Breaker Middleware

Protect against cascading failures:

```python
from provide.foundation.resilience import CircuitBreaker, CircuitBreakerOpen

class CircuitBreakerMiddleware:
    """Circuit breaker for HTTP requests."""

    def __init__(self, failure_threshold=5, timeout=60):
        self.circuit = CircuitBreaker(
            failure_threshold=failure_threshold,
            timeout=timeout,
        )

    async def __call__(self, request, call_next):
        """Protect request with circuit breaker."""
        @self.circuit.protect
        async def make_request():
            response = await call_next(request)
            # Consider 5xx as failures
            if response.status_code >= 500:
                raise ServerError(f"Server error: {response.status_code}")
            return response

        try:
            return await make_request()
        except CircuitBreakerOpen:
            logger.error("circuit_breaker_open", url=str(request.url))
            # Return cached response or error
            raise ServiceUnavailable("Service circuit breaker is open")
```

### Metrics Collection Middleware

Track HTTP metrics:

```python
from provide.foundation.metrics import Counter, Histogram

# Define metrics
http_requests_total = Counter(
    "http_requests_total",
    labels=["method", "status", "endpoint"]
)
http_request_duration = Histogram(
    "http_request_duration_seconds",
    labels=["method", "endpoint"]
)

async def metrics_middleware(request, call_next):
    """Collect HTTP metrics."""
    start_time = time.time()

    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 0  # Failed request
        raise
    finally:
        duration = time.time() - start_time

        # Record metrics
        http_requests_total.increment(labels={
            "method": request.method,
            "status": str(status),
            "endpoint": str(request.url.path),
        })

        http_request_duration.observe(
            duration,
            labels={
                "method": request.method,
                "endpoint": str(request.url.path),
            },
        )

    return response
```

## Best Practices

### ✅ DO: Order Middleware Correctly

```python
# ✅ Good: Logical order
client = HTTPClient(
    middleware=[
        logging_middleware,      # Log everything
        auth_middleware,          # Add auth
        caching_middleware,       # Check cache
        retry_middleware,         # Retry failures
    ]
)

# ❌ Bad: Cache before auth
client = HTTPClient(
    middleware=[
        caching_middleware,  # Cache without auth!
        auth_middleware,
    ]
)
```

### ✅ DO: Handle Errors Gracefully

```python
# ✅ Good: Error handling
async def safe_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("middleware_error")
        raise  # Re-raise after logging
```

### ✅ DO: Log Middleware Actions

```python
# ✅ Good: Visibility
async def transparent_middleware(request, call_next):
    logger.debug("middleware_processing", url=str(request.url))
    response = await call_next(request)
    logger.debug("middleware_completed", status=response.status_code)
    return response
```

### ❌ DON'T: Modify Response Objects Directly

```python
# ❌ Bad: Mutating response
async def bad_middleware(request, call_next):
    response = await call_next(request)
    response.status_code = 200  # Don't mutate!
    return response

# ✅ Good: Create new response if needed
async def good_middleware(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return httpx.Response(
            status_code=200,
            json={"error": "Not found"},
        )
    return response
```

## Next Steps

### Related Guides
- **[Making Requests](requests.md)**: HTTP request patterns
- **[Retry Patterns](../resilience/retry.md)**: Retry logic
- **[Circuit Breakers](../resilience/circuit-breaker.md)**: Circuit breaker pattern

### Examples
- See `examples/transport/01_http_client.py` for middleware examples
- See `examples/production/` for production middleware patterns

### API Reference
- **[API Reference: Transport](../../reference/provide/foundation/transport/index.md)**: Complete API documentation

---

**Tip**: Keep middleware focused on a single responsibility. Combine multiple simple middleware instead of creating one complex middleware that does everything.
