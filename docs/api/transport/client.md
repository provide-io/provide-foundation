# Transport Client

Universal HTTP client with middleware support and Foundation integration.

## Overview

The Transport Client provides a unified interface for making HTTP requests with built-in telemetry, error handling, and middleware processing. It automatically discovers transports through the Hub registry and supports both individual requests and managed client sessions.

## UniversalClient

The primary client class for making requests with session management and middleware.

### Constructor

```python
from provide.foundation.transport import UniversalClient

@define
class UniversalClient:
    middleware: MiddlewarePipeline = field(factory=create_default_pipeline)
    default_headers: Headers = field(factory=dict)
    default_timeout: float | None = field(default=None)
```

**Parameters:**
- `middleware`: Middleware pipeline for request/response processing
- `default_headers`: Headers to include in all requests
- `default_timeout`: Default timeout for requests (overrides global config)

### Context Manager Usage

```python
# Recommended: Use as async context manager
async with UniversalClient() as client:
    response = await client.get("https://api.example.com/users")
    data = response.json()

# Manual lifecycle management
client = UniversalClient()
try:
    response = await client.get("https://api.example.com/users")
finally:
    await client.__aexit__(None, None, None)
```

### Request Methods

All HTTP methods are supported with consistent signatures:

```python
async def request(
    self,
    uri: str,
    method: str | HTTPMethod = HTTPMethod.GET,
    *,
    headers: Headers | None = None,
    params: Params | None = None,
    body: Data = None,
    timeout: float | None = None,
    **kwargs
) -> Response
```

**HTTP Method Shortcuts:**

```python
# GET request
response = await client.get(
    "https://api.example.com/users",
    headers={"Accept": "application/json"},
    params={"page": 1, "limit": 10}
)

# POST request with JSON body
response = await client.post(
    "https://api.example.com/users",
    body={"name": "Alice", "email": "alice@example.com"},
    headers={"Content-Type": "application/json"}
)

# PUT request
response = await client.put(
    "https://api.example.com/users/123",
    body={"name": "Alice Updated"}
)

# PATCH request
response = await client.patch(
    "https://api.example.com/users/123",
    body={"email": "alice-new@example.com"}
)

# DELETE request
response = await client.delete("https://api.example.com/users/123")

# HEAD request
response = await client.head("https://api.example.com/users/123")

# OPTIONS request
response = await client.options("https://api.example.com/users")
```

### Streaming Responses

```python
async def stream(
    self, 
    uri: str, 
    method: str | HTTPMethod = HTTPMethod.GET, 
    **kwargs
) -> AsyncIterator[bytes]
```

**Example:**
```python
async with UniversalClient() as client:
    async for chunk in client.stream("https://api.example.com/large-file"):
        process_chunk(chunk)
```

### Configuration

```python
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    create_default_pipeline
)

# Custom configuration
pipeline = create_default_pipeline()
client = UniversalClient(
    middleware=pipeline,
    default_headers={
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json"
    },
    default_timeout=60.0
)
```

## Global Functions

Convenience functions that use a shared default client instance.

### get_default_client()

Get or create the global default client:

```python
from provide.foundation.transport import get_default_client

client = get_default_client()
response = await client.get("https://api.example.com/data")
```

### HTTP Method Functions

All HTTP methods are available as module-level functions:

```python
from provide.foundation.transport import get, post, put, patch, delete, head, options

# Simple GET
response = await get("https://api.example.com/users")

# POST with data
response = await post(
    "https://api.example.com/users",
    body={"name": "Bob"},
    headers={"Content-Type": "application/json"}
)

# All methods support the same parameters as client methods
response = await put(
    "https://api.example.com/users/456",
    body={"name": "Bob Updated"},
    timeout=30.0
)
```

### request()

Generic request function:

```python
from provide.foundation.transport import request
from provide.foundation.transport.types import HTTPMethod

response = await request(
    "https://api.example.com/data",
    method=HTTPMethod.POST,
    body={"key": "value"}
)
```

### stream()

Global streaming function:

```python
from provide.foundation.transport import stream

async for chunk in stream("https://api.example.com/large-data"):
    handle_chunk(chunk)
```

## Request and Response Objects

### Request

```python
@define
class Request:
    uri: str
    method: str = "GET"
    headers: Headers = field(factory=dict)
    params: Params = field(factory=dict)
    body: Data = None
    timeout: float | None = None
    metadata: dict[str, Any] = field(factory=dict)
```

**Properties:**
- `transport_type`: Inferred from URI scheme
- `base_url`: Extracted base URL from URI

### Response

```python
@define
class Response:
    status: int
    headers: Headers = field(factory=dict)
    body: bytes | str | None = None
    metadata: dict[str, Any] = field(factory=dict)
    elapsed_ms: float = 0
    request: Request | None = None
```

**Methods:**
- `is_success() -> bool`: Check if status indicates success (2xx)
- `json() -> Any`: Parse response body as JSON
- `text -> str`: Get response body as text string

**Example:**
```python
response = await get("https://api.example.com/users/123")

if response.is_success():
    user_data = response.json()
    print(f"User: {user_data['name']}")
else:
    print(f"Error: {response.status}")
    print(f"Response time: {response.elapsed_ms}ms")
```

## Advanced Usage

### Custom Headers and Parameters

```python
# Headers for authentication
headers = {
    "Authorization": "Bearer your-token-here",
    "Accept": "application/json",
    "X-API-Version": "v2"
}

# Query parameters
params = {
    "page": 2,
    "limit": 50,
    "sort": "created_at",
    "order": "desc"
}

response = await get(
    "https://api.example.com/users",
    headers=headers,
    params=params
)
```

### Request Body Types

```python
# JSON body (dict)
json_response = await post(
    "https://api.example.com/users",
    body={"name": "Charlie", "age": 30}
)

# String body
text_response = await post(
    "https://api.example.com/webhook",
    body="raw text data",
    headers={"Content-Type": "text/plain"}
)

# Bytes body
binary_response = await post(
    "https://api.example.com/upload",
    body=b"binary data",
    headers={"Content-Type": "application/octet-stream"}
)
```

### Timeout Configuration

```python
# Per-request timeout
response = await get(
    "https://api.example.com/slow-endpoint",
    timeout=120.0  # 2 minutes
)

# Client-level default timeout
client = UniversalClient(default_timeout=60.0)
async with client:
    # All requests default to 60 seconds
    response = await client.get("https://api.example.com/data")
```

### Error Handling

```python
from provide.foundation.transport.errors import (
    TransportTimeoutError,
    TransportConnectionError,
    HTTPResponseError
)

try:
    response = await get("https://api.example.com/data")
    
    if not response.is_success():
        # Handle HTTP errors (4xx, 5xx)
        logger.warning("http_error", status=response.status, uri=response.request.uri)
        
except TransportTimeoutError:
    logger.error("request_timeout", uri="https://api.example.com/data")
    
except TransportConnectionError as e:
    logger.error("connection_failed", error=str(e))
    
except HTTPResponseError as e:
    logger.error("http_response_error", status=e.status_code)
```

## Client Lifecycle

### Connection Pooling

The client automatically manages connection pools:

```python
# Connections are automatically pooled and reused
async with UniversalClient() as client:
    # These requests share connections
    users = await client.get("https://api.example.com/users")
    posts = await client.get("https://api.example.com/posts")
    comments = await client.get("https://api.example.com/comments")

# Connections are properly closed when exiting context
```

### Resource Cleanup

```python
# Automatic cleanup with context manager
async with UniversalClient() as client:
    response = await client.get("https://api.example.com/data")
    # Transport connections automatically closed

# Manual cleanup if not using context manager
client = UniversalClient()
try:
    response = await client.get("https://api.example.com/data")
finally:
    await client.__aexit__(None, None, None)
```

## Testing

Mock HTTP responses for testing using pytest-httpx:

```python
import pytest
from pytest_httpx import HTTPXMock
from provide.foundation.transport import UniversalClient

@pytest.mark.asyncio
async def test_client_request(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users",
        json={"users": [{"id": 1, "name": "Test User"}]},
        status_code=200
    )
    
    async with UniversalClient() as client:
        response = await client.get("https://api.example.com/users")
        data = response.json()
        
        assert response.is_success()
        assert len(data["users"]) == 1
        assert data["users"][0]["name"] == "Test User"
```

## See Also

- [Transport Registry](registry.md) - Transport discovery and registration
- [Transport Middleware](middleware.md) - Request/response processing
- [Transport API](api-index.md) - Complete transport system overview
- [Resilience Patterns](../resilience/api-index.md) - Retry and circuit breaker patterns