# Making HTTP Requests

Learn how to make HTTP requests with Foundation's transport client.

## Overview

Foundation provides an HTTP client built on httpx with automatic retries and logging.

## Basic GET Request

```python
from provide.foundation.transport import HTTPClient

async def fetch_data():
    async with HTTPClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

## POST Request

```python
async def create_user(name: str, email: str):
    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/users",
            json={"name": name, "email": email}
        )
        return response.json()
```

## With Headers

```python
headers = {
    "Authorization": "Bearer token_here",
    "Content-Type": "application/json"
}

response = await client.get(
    "https://api.example.com/protected",
    headers=headers
)
```

## Next Steps

- **[Custom Middleware](middleware.md)** - Add middleware
- **[API Reference: Transport](../../reference/provide/foundation/transport/index.md)**

**See also:** [examples/transport/01_http_client.py](https://github.com/provide-io/provide-foundation/blob/main/examples/transport/01_http_client.py)
