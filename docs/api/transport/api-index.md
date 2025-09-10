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
if response.status_code == 200:
    user_data = response.json()
    logger.info("user_created", user_id=user_data["id"])
```

### Using the Universal Client

```python
from provide.foundation.transport import UniversalClient

# Create client with configuration
client = UniversalClient(
    base_url="https://api.example.com",
    timeout=30.0,
    headers={"Authorization": "Bearer token123"}
)

# Use for multiple requests
users = await client.get("/users")
user = await client.post("/users", body={"name": "Alice"})
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
    base_url="https://api.example.com",
    timeout=30.0,
    headers={"User-Agent": "MyApp/1.0"},
    follow_redirects=True
)

# Client methods mirror HTTP functions
response = await client.get("/endpoint")
response = await client.post("/endpoint", body=data)
```

## Middleware System

The transport layer supports middleware for cross-cutting concerns:

### Built-in Middleware

```python
from provide.foundation.transport.middleware import (
    LoggingMiddleware,
    RetryMiddleware,
    AuthMiddleware
)

# Configure middleware
client = UniversalClient(
    base_url="https://api.example.com",
    middleware=[
        LoggingMiddleware(),
        RetryMiddleware(max_attempts=3),
        AuthMiddleware(token="bearer_token")
    ]
)
```

### Custom Middleware

```python
from provide.foundation.transport.middleware import BaseMiddleware

class CustomMiddleware(BaseMiddleware):
    async def process_request(self, request):
        """Process outgoing request."""
        request.headers["X-Custom-Header"] = "value"
        return request
    
    async def process_response(self, response):
        """Process incoming response."""
        if response.status_code >= 400:
            logger.warning("http_error", status=response.status_code)
        return response

# Use custom middleware
client = UniversalClient(middleware=[CustomMiddleware()])
```

## Configuration

Transport configuration through environment variables:

```bash
# Base configuration
export PROVIDE_TRANSPORT_TIMEOUT=30.0
export PROVIDE_TRANSPORT_MAX_REDIRECTS=5
export PROVIDE_TRANSPORT_VERIFY_SSL=true

# HTTP-specific configuration  
export PROVIDE_HTTP_USER_AGENT="MyApp/1.0"
export PROVIDE_HTTP_MAX_CONNECTIONS=100
export PROVIDE_HTTP_MAX_KEEPALIVE_CONNECTIONS=20

# Retry configuration
export PROVIDE_TRANSPORT_RETRY_ATTEMPTS=3
export PROVIDE_TRANSPORT_RETRY_BACKOFF=exponential
```

### Programmatic Configuration

```python
from provide.foundation.transport.config import TransportConfig

config = TransportConfig(
    timeout=60.0,
    max_redirects=10,
    verify_ssl=True,
    user_agent="MyApp/2.0",
    max_connections=50
)

client = UniversalClient(config=config)
```

## Error Handling

Transport operations integrate with Foundation's error handling:

```python
from provide.foundation.transport import get
from provide.foundation.transport.exceptions import (
    TransportError,
    TimeoutError,
    ConnectionError
)

try:
    response = await get("https://api.example.com/data")
    return response.json()
    
except TimeoutError:
    logger.error("request_timeout", url=url)
    return None
    
except ConnectionError as e:
    logger.error("connection_failed", error=str(e))
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
from provide.foundation.transport.auth import BearerAuth, BasicAuth

# Bearer token authentication
client = UniversalClient(
    auth=BearerAuth("your_token_here")
)

# Basic authentication
client = UniversalClient(
    auth=BasicAuth("username", "password")
)
```

## Testing

Test transport operations using Foundation's testing utilities:

```python
from provide.foundation.testing.transport import MockTransport

def test_api_call():
    with MockTransport() as mock:
        mock.add_response(
            "GET", 
            "https://api.example.com/users",
            json={"users": [{"id": 1, "name": "John"}]},
            status=200
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