# Custom Middleware

Learn how to create custom HTTP middleware for logging, authentication, and more.

## Overview

Middleware allows you to intercept and modify HTTP requests and responses.

## Logging Middleware

```python
from provide.foundation.transport import HTTPClient
from provide.foundation import logger

async def logging_middleware(request, call_next):
    """Log all HTTP requests."""
    logger.info(
        "http_request",
        method=request.method,
        url=str(request.url)
    )

    response = await call_next(request)

    logger.info(
        "http_response",
        status=response.status_code,
        url=str(request.url)
    )

    return response

# Use middleware
client = HTTPClient(middleware=[logging_middleware])
```

## Authentication Middleware

```python
async def auth_middleware(request, call_next):
    """Add authentication header to all requests."""
    request.headers["Authorization"] = f"Bearer {get_token()}"
    return await call_next(request)
```

## Next Steps

- **[Making Requests](requests.md)** - HTTP requests
- **[API Reference: Transport](../../reference/provide/foundation/transport/index.md)**
