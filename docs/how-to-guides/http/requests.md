# Making HTTP Requests

Learn how to make HTTP requests with Foundation's transport client built on httpx.

## Overview

Foundation provides a powerful HTTP client with automatic retries, logging, middleware support, and async/await patterns. Built on httpx, it adds production-focused features while maintaining a familiar API.

**Key features:**
- Async-first with httpx backend
- Automatic request/response logging
- Middleware support for cross-cutting concerns
- Connection pooling and keep-alive
- Timeout management
- Streaming support for large responses

## Prerequisites

Install transport extras:
```bash
uv add provide-foundation[transport]
```

## Basic Requests

### GET Request

Fetch data from an API:

```python
from provide.foundation.transport import HTTPClient

async def fetch_data():
    """Simple GET request."""
    async with HTTPClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# Use in async context
data = await fetch_data()
```

### POST Request

Send data to an API:

```python
async def create_user(name: str, email: str):
    """Create a new user."""
    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/users",
            json={"name": name, "email": email}
        )
        return response.json()
```

### PUT and PATCH Requests

Update existing resources:

```python
# Full update with PUT
async def update_user(user_id: str, user_data: dict):
    """Update user with PUT."""
    async with HTTPClient() as client:
        response = await client.put(
            f"https://api.example.com/users/{user_id}",
            json=user_data
        )
        return response.json()

# Partial update with PATCH
async def patch_user(user_id: str, changes: dict):
    """Partially update user with PATCH."""
    async with HTTPClient() as client:
        response = await client.patch(
            f"https://api.example.com/users/{user_id}",
            json=changes
        )
        return response.json()
```

### DELETE Request

Remove resources:

```python
async def delete_user(user_id: str):
    """Delete a user."""
    async with HTTPClient() as client:
        response = await client.delete(
            f"https://api.example.com/users/{user_id}"
        )
        return response.status_code == 204
```

## Headers and Authentication

### Custom Headers

Add headers to requests:

```python
async def authenticated_request():
    """Request with custom headers."""
    headers = {
        "Authorization": "Bearer your-token-here",
        "Content-Type": "application/json",
        "User-Agent": "MyApp/1.0",
        "X-API-Version": "2.0"
    }

    async with HTTPClient() as client:
        response = await client.get(
            "https://api.example.com/protected",
            headers=headers
        )
        return response.json()
```

### Bearer Token Authentication

Common authentication pattern:

```python
from provide.foundation.config import get_config

async def call_authenticated_api(endpoint: str):
    """Call API with bearer token."""
    config = get_config()

    headers = {
        "Authorization": f"Bearer {config.api_token}"
    }

    async with HTTPClient() as client:
        response = await client.get(
            f"https://api.example.com{endpoint}",
            headers=headers
        )
        return response.json()
```

### Basic Authentication

HTTP Basic Auth:

```python
import base64

async def basic_auth_request(username: str, password: str):
    """Request with HTTP Basic Auth."""
    # Encode credentials
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    headers = {
        "Authorization": f"Basic {credentials}"
    }

    async with HTTPClient() as client:
        response = await client.get(
            "https://api.example.com/data",
            headers=headers
        )
        return response.json()
```

## Query Parameters

### Simple Query Parameters

Add query parameters to requests:

```python
async def search_users(query: str, limit: int = 10):
    """Search users with query parameters."""
    params = {
        "q": query,
        "limit": limit,
        "sort": "created_at",
        "order": "desc"
    }

    async with HTTPClient() as client:
        response = await client.get(
            "https://api.example.com/users/search",
            params=params
        )
        return response.json()
```

### Complex Query Parameters

Handle lists and nested parameters:

```python
async def filter_items(categories: list[str], tags: list[str]):
    """Filter with multiple values."""
    # httpx handles lists automatically
    params = {
        "category": categories,  # ?category=a&category=b
        "tag": tags,
        "include_archived": "false"
    }

    async with HTTPClient() as client:
        response = await client.get(
            "https://api.example.com/items",
            params=params
        )
        return response.json()
```

## Request Body Formats

### JSON Payload

Most common API format:

```python
async def create_order(items: list[dict], customer_id: str):
    """Create order with JSON payload."""
    payload = {
        "customer_id": customer_id,
        "items": items,
        "total": sum(item["price"] for item in items),
        "currency": "USD"
    }

    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/orders",
            json=payload  # Automatically sets Content-Type: application/json
        )
        return response.json()
```

### Form Data

Send form-encoded data:

```python
async def login(username: str, password: str):
    """Login with form data."""
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }

    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/auth/token",
            data=data  # Sends as application/x-www-form-urlencoded
        )
        return response.json()
```

### Multipart Form Data

Upload files with other fields:

```python
async def upload_profile(user_id: str, avatar_path: str, bio: str):
    """Upload file with multipart form data."""
    files = {
        "avatar": open(avatar_path, "rb")
    }

    data = {
        "user_id": user_id,
        "bio": bio
    }

    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/profile/upload",
            files=files,
            data=data
        )
        return response.json()
```

## File Operations

### Upload Single File

Upload a file to an API:

```python
from pathlib import Path

async def upload_file(file_path: Path):
    """Upload a single file."""
    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, "application/octet-stream")}

        async with HTTPClient() as client:
            response = await client.post(
                "https://api.example.com/upload",
                files=files
            )
            return response.json()
```

### Upload Multiple Files

Upload several files at once:

```python
async def upload_multiple_files(file_paths: list[Path]):
    """Upload multiple files."""
    files = [
        ("files", (path.name, open(path, "rb"), "application/octet-stream"))
        for path in file_paths
    ]

    async with HTTPClient() as client:
        response = await client.post(
            "https://api.example.com/bulk-upload",
            files=files
        )
        return response.json()
```

### Download File

Download and save a file:

```python
async def download_file(url: str, save_path: Path):
    """Download file to disk."""
    async with HTTPClient() as client:
        response = await client.get(url)

        # Save to file
        save_path.write_bytes(response.content)

        return save_path

# Usage
await download_file(
    "https://example.com/report.pdf",
    Path("downloads/report.pdf")
)
```

### Stream Large Files

Download large files efficiently:

```python
async def download_large_file(url: str, save_path: Path):
    """Download large file with streaming."""
    async with HTTPClient() as client:
        async with client.stream("GET", url) as response:
            with open(save_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)

    return save_path
```

## Timeouts

### Configure Timeouts

Set request timeouts:

```python
from httpx import Timeout

async def request_with_timeout():
    """Request with custom timeout."""
    timeout = Timeout(
        connect=5.0,  # Max time to establish connection
        read=30.0,    # Max time to read response
        write=10.0,   # Max time to send request
        pool=5.0      # Max time to get connection from pool
    )

    async with HTTPClient(timeout=timeout) as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### Per-Request Timeout

Override timeout for specific requests:

```python
async def quick_health_check():
    """Health check with short timeout."""
    async with HTTPClient() as client:
        try:
            response = await client.get(
                "https://api.example.com/health",
                timeout=2.0  # 2 second timeout
            )
            return response.status_code == 200
        except httpx.TimeoutException:
            return False
```

## Error Handling

### Handle HTTP Errors

Catch and handle HTTP errors:

```python
from provide.foundation import logger
import httpx

async def safe_api_call(url: str):
    """API call with comprehensive error handling."""
    async with HTTPClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raises for 4xx/5xx
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(
                "http_error",
                status=e.response.status_code,
                url=str(url),
                response=e.response.text[:200]
            )
            raise

        except httpx.TimeoutException:
            logger.error("request_timeout", url=str(url))
            raise

        except httpx.RequestError as e:
            logger.error("request_failed", url=str(url), error=str(e))
            raise
```

### Retry Failed Requests

Automatically retry transient failures:

```python
from provide.foundation.resilience import retry, NetworkError

@retry(
    (httpx.TimeoutException, httpx.NetworkError),
    max_attempts=3,
    base_delay=1.0
)
async def resilient_request(url: str):
    """Request with automatic retries."""
    async with HTTPClient() as client:
        response = await client.get(url)

        # Retry on server errors
        if response.status_code >= 500:
            raise NetworkError(f"Server error: {response.status_code}")

        return response.json()
```

## Response Handling

### Check Status Codes

Validate response status:

```python
async def check_response_status():
    """Handle different status codes."""
    async with HTTPClient() as client:
        response = await client.get("https://api.example.com/data")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logger.warning("resource_not_found")
            return None
        elif response.status_code >= 500:
            logger.error("server_error", status=response.status_code)
            raise ServerError()
        else:
            response.raise_for_status()
```

### Parse Response Formats

Handle different content types:

```python
async def parse_response(url: str):
    """Parse response based on content type."""
    async with HTTPClient() as client:
        response = await client.get(url)

        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            return response.json()
        elif "text/html" in content_type:
            return response.text
        elif "application/xml" in content_type:
            import xml.etree.ElementTree as ET
            return ET.fromstring(response.content)
        else:
            return response.content
```

### Access Response Headers

Read response headers:

```python
async def get_response_headers():
    """Access response headers."""
    async with HTTPClient() as client:
        response = await client.get("https://api.example.com/data")

        # Get specific headers
        content_type = response.headers.get("content-type")
        rate_limit = response.headers.get("x-ratelimit-remaining")
        request_id = response.headers.get("x-request-id")

        logger.info(
            "response_headers",
            content_type=content_type,
            rate_limit=rate_limit,
            request_id=request_id
        )

        return response.json()
```

## Connection Management

### Reuse Client

Reuse client for multiple requests:

```python
class APIClient:
    """Reusable API client."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.client = None

    async def __aenter__(self):
        """Create client."""
        self.client = HTTPClient(
            base_url=self.base_url,
            headers=self.headers
        )
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args):
        """Close client."""
        await self.client.__aexit__(*args)

    async def get_user(self, user_id: str):
        """Get user by ID."""
        response = await self.client.get(f"/users/{user_id}")
        return response.json()

    async def list_users(self, limit: int = 10):
        """List users."""
        response = await self.client.get("/users", params={"limit": limit})
        return response.json()

# Usage
async with APIClient("https://api.example.com", "your-api-key") as api:
    user = await api.get_user("123")
    users = await api.list_users(limit=50)
```

### Connection Pooling

Configure connection pool:

```python
import httpx

async def configure_connection_pool():
    """Client with custom connection pool."""
    limits = httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100,
        keepalive_expiry=30.0
    )

    async with HTTPClient(limits=limits) as client:
        # Make multiple requests efficiently
        tasks = [
            client.get(f"https://api.example.com/item/{i}")
            for i in range(50)
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Streaming Responses

### Stream JSON Lines

Process streaming JSON data:

```python
import json

async def stream_json_lines(url: str):
    """Process streaming JSON lines."""
    async with HTTPClient() as client:
        async with client.stream("GET", url) as response:
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    # Process each JSON object
                    yield data
```

### Server-Sent Events (SSE)

Handle server-sent events:

```python
async def subscribe_to_events(url: str):
    """Subscribe to server-sent events."""
    async with HTTPClient() as client:
        async with client.stream("GET", url) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    event_data = line[6:]  # Remove "data: " prefix
                    yield json.loads(event_data)
```

## Best Practices

### ✅ DO: Use Context Managers

```python
# ✅ Good: Automatic cleanup
async def good_request():
    async with HTTPClient() as client:
        return await client.get("https://api.example.com")

# ❌ Bad: Manual cleanup required
async def bad_request():
    client = HTTPClient()
    response = await client.get("https://api.example.com")
    await client.aclose()  # Easy to forget!
    return response
```

### ✅ DO: Set Appropriate Timeouts

```python
# ✅ Good: Reasonable timeout
async with HTTPClient(timeout=30.0) as client:
    response = await client.get(url)

# ❌ Bad: No timeout (can hang forever)
async with HTTPClient(timeout=None) as client:
    response = await client.get(url)
```

### ✅ DO: Handle Errors Gracefully

```python
# ✅ Good: Comprehensive error handling
try:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()
except httpx.HTTPStatusError as e:
    logger.error("http_error", status=e.response.status_code)
    return None
except httpx.TimeoutException:
    logger.error("timeout", url=url)
    return None
```

### ✅ DO: Reuse Clients

```python
# ✅ Good: Reuse client for multiple requests
async with HTTPClient() as client:
    user = await client.get("/users/1")
    posts = await client.get("/users/1/posts")
    comments = await client.get("/users/1/comments")

# ❌ Bad: Create new client for each request
for i in range(100):
    async with HTTPClient() as client:  # Wasteful!
        await client.get(f"/items/{i}")
```

### ❌ DON'T: Ignore Status Codes

```python
# ❌ Bad: Assuming success
response = await client.get(url)
data = response.json()  # Might fail if status is 404!

# ✅ Good: Check status
response = await client.get(url)
if response.status_code == 200:
    data = response.json()
else:
    logger.error("request_failed", status=response.status_code)
```

## Common Patterns

### Pagination

Handle paginated API responses:

```python
async def fetch_all_pages(base_url: str):
    """Fetch all pages from paginated API."""
    all_items = []
    page = 1

    async with HTTPClient() as client:
        while True:
            response = await client.get(
                base_url,
                params={"page": page, "per_page": 100}
            )
            data = response.json()

            items = data.get("items", [])
            all_items.extend(items)

            # Check if there are more pages
            if not data.get("has_more"):
                break

            page += 1

    return all_items
```

### Rate Limiting

Respect API rate limits:

```python
import asyncio
from datetime import datetime, timedelta

class RateLimitedClient:
    """HTTP client with rate limiting."""

    def __init__(self, requests_per_second=10):
        self.delay = 1.0 / requests_per_second
        self.last_request = None

    async def get(self, url: str):
        """GET request with rate limiting."""
        # Wait if needed
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.delay:
                await asyncio.sleep(self.delay - elapsed)

        async with HTTPClient() as client:
            response = await client.get(url)
            self.last_request = datetime.now()
            return response
```

## Next Steps

### Related Guides
- **[Custom Middleware](middleware.md)**: Add middleware for auth, logging, retries
- **[Retry Patterns](../resilience/retry.md)**: Automatically retry failed requests
- **[Circuit Breakers](../resilience/circuit-breaker.md)**: Protect against cascading failures

### Examples
- See `examples/transport/01_http_client.py` for comprehensive HTTP client examples
- See `examples/production/` for production HTTP patterns

### API Reference
- **[API Reference: Transport](../../reference/provide/foundation/transport/index.md)**: Complete API documentation

---

**Tip**: Always use async context managers (`async with`) with HTTPClient to ensure proper connection cleanup. Set appropriate timeouts to prevent hanging requests.
