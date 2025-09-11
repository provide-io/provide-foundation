# Transport Layer API

Protocol-agnostic transport system with HTTP/HTTPS support and middleware pipeline.

## Overview

The Transport module provides a modern, async-first transport layer built on httpx with Foundation's telemetry integration. It offers:

- **Protocol Agnostic**: Extensible design for different transport protocols
- **HTTP/HTTPS Support**: Full-featured HTTP client with modern async/await
- **Middleware Pipeline**: Extensible request/response processing
- **Foundation Integration**: Built-in telemetry and error handling
- **Hub Registry**: Service discovery and transport registration
- **Zero Hardcoded Defaults**: All configuration from environment variables

## Quick Start

### Simple HTTP Requests

```python
from provide.foundation.transport import get, post

# Simple GET request
response = await get("https://api.example.com/users")
data = response.json()

# POST with JSON body
response = await post(
    "https://api.example.com/users",
    body={"name": "John", "email": "john@example.com"}
)

# Response handling
if response.status == 200:
    user_data = response.json()
    logger.info("user_created", user_id=user_data["id"])
```

### Using the Universal Client

```python
from provide.foundation.transport import UniversalClient

# Create client with configuration
client = UniversalClient(
    default_headers={"Authorization": "Bearer token123"},
    default_timeout=30.0
)

# Use for multiple requests
users = await client.get("https://api.example.com/users")
user = await client.post("https://api.example.com/users", body={"name": "Alice"})
```

## Core Components

### HTTP Functions

Convenience functions for common HTTP operations:

```python
from provide.foundation.transport import get, post, put, delete, patch

# HTTP methods
response = await get(url, headers=None, params=None)
response = await post(url, body=None, headers=None)
response = await put(url, body=None, headers=None)
response = await delete(url, headers=None)
response = await patch(url, body=None, headers=None)
```

### UniversalClient

Full-featured HTTP client with middleware support:

```python
from provide.foundation.transport import UniversalClient

client = UniversalClient(
    default_headers={"User-Agent": "MyApp/1.0"},
    default_timeout=30.0
)

# Client methods mirror HTTP functions
response = await client.get("https://api.example.com/endpoint")
response = await client.post("https://api.example.com/endpoint", body=data)
```

## Middleware System

The transport layer supports middleware for cross-cutting concerns:

### Built-in Middleware

```python
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    RetryMiddleware,
    MetricsMiddleware,
    create_default_pipeline
)

# Configure middleware
pipeline = create_default_pipeline()
client = UniversalClient(
    middleware=pipeline
)
```

### Custom Middleware

```python
from provide.foundation.transport.middleware import Middleware

class CustomMiddleware(Middleware):
    async def process_request(self, request):
        """Process outgoing request."""
        request.headers["X-Custom-Header"] = "value"
        return request
    
    async def process_response(self, response):
        """Process incoming response."""
        if response.status >= 400:
            logger.warning("http_error", status=response.status)
        return response
    
    async def process_error(self, error, request):
        """Process errors during request."""
        logger.error("transport_error", error=str(error))
        return error

# Use custom middleware
from provide.foundation.transport.middleware import MiddlewarePipeline
pipeline = MiddlewarePipeline([CustomMiddleware()])
client = UniversalClient(middleware=pipeline)
```

## Configuration

Transport configuration through environment variables:

```bash
# Base configuration
export PROVIDE_TRANSPORT_TIMEOUT=30.0
export PROVIDE_TRANSPORT_MAX_RETRIES=3
export PROVIDE_TRANSPORT_RETRY_BACKOFF_FACTOR=0.5
export PROVIDE_TRANSPORT_VERIFY_SSL=true

# HTTP-specific configuration  
export PROVIDE_HTTP_POOL_CONNECTIONS=10
export PROVIDE_HTTP_POOL_MAXSIZE=100
export PROVIDE_HTTP_FOLLOW_REDIRECTS=true
export PROVIDE_HTTP_USE_HTTP2=false
export PROVIDE_HTTP_MAX_REDIRECTS=5
```

### Programmatic Configuration

```python
from provide.foundation.transport.config import HTTPConfig

config = HTTPConfig(
    timeout=60.0,
    max_redirects=10,
    verify_ssl=True,
    pool_connections=20,
    pool_maxsize=200
)

# Configuration is applied globally through environment variables
# Individual client instances use middleware for customization
```

## Error Handling

Transport operations integrate with Foundation's error handling:

```python
from provide.foundation.transport import get
from provide.foundation.transport.errors import (
    TransportError,
    TransportTimeoutError,
    TransportConnectionError,
    HTTPResponseError,
    TransportNotFoundError,
)

try:
    response = await get("https://api.example.com/data")
    return response.json()
    
except TransportTimeoutError:
    logger.error("request_timeout", url="https://api.example.com/data")
    return None
    
except TransportConnectionError as e:
    logger.error("connection_failed", error=str(e))
    return None
    
except HTTPResponseError as e:
    logger.error("http_error", status=e.status_code, error=str(e))
    return None
    
except TransportError as e:
    logger.error("transport_error", error=str(e))
    raise
```

## Integration with Foundation

### Logging Integration

All transport operations are automatically logged:

```python
# Request/response logging happens automatically
response = await get("https://api.example.com/users")

# Logs generated:
# INFO: http_request_started url=https://api.example.com/users method=GET
# INFO: http_request_completed status=200 duration_ms=245
```

### Hub Registration

Register transport services with the Foundation hub:

```python
from provide.foundation.hub import register_component
from provide.foundation.transport import UniversalClient

# Register named transport service
@register_component("api_client", category="transport")
def create_api_client():
    return UniversalClient(
        base_url="https://api.example.com",
        timeout=30.0
    )

# Use registered service
from provide.foundation.hub import get_hub
hub = get_hub()
client = hub.get_component("api_client")
```

## Advanced Usage

### Streaming Responses

```python
from provide.foundation.transport import UniversalClient

client = UniversalClient()

# Stream large responses
async with client.stream("GET", "https://api.example.com/large-data") as response:
    async for chunk in response.aiter_bytes():
        process_chunk(chunk)
```

### File Upload/Download

```python
# File upload
with open("document.pdf", "rb") as f:
    response = await post(
        "https://api.example.com/upload",
        files={"document": f}
    )

# File download
response = await get("https://api.example.com/download/file.zip")
with open("downloaded.zip", "wb") as f:
    f.write(response.content)
```

### Authentication

```python
# Authentication through headers
client = UniversalClient(
    default_headers={"Authorization": "Bearer your_token_here"}
)

# Basic authentication via headers
import base64
auth_string = base64.b64encode(b"username:password").decode("ascii")
client = UniversalClient(
    default_headers={"Authorization": f"Basic {auth_string}"}
)
```

## Testing

Test transport operations using pytest-httpx:

```python
import pytest
from pytest_httpx import HTTPXMock
from provide.foundation.transport import get

@pytest.mark.asyncio
async def test_api_call(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET", 
        url="https://api.example.com/users",
        json={"users": [{"id": 1, "name": "John"}]},
        status_code=200
    )
    
    response = await get("https://api.example.com/users")
    data = response.json()
    
    assert len(data["users"]) == 1
    assert data["users"][0]["name"] == "John"
```

## API Reference

::: provide.foundation.transport

## Related Documentation

- [Resilience Patterns](../resilience/api-index.md) - Retry and circuit breaker patterns
- [Error Handling](../errors/api-index.md) - Error handling utilities
- [Hub System](../hub/api-index.md) - Component registration
- [Testing Guide](../../guide/testing.md) - Testing HTTP clients