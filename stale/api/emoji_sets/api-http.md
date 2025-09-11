# HTTP Emoji Set

Visual enhancements for web requests, API calls, and HTTP operations.

## Overview

The HTTP emoji set provides visual context for web-based operations, making it easy to identify different types of HTTP activities at a glance. It covers HTTP methods, status codes, and common web operation patterns.

## Emoji Mappings

### HTTP Methods
- **GET requests**: 🔍 (retrieval/fetching)
- **POST requests**: ➕ (creating new resources)  
- **PUT requests**: ✏️ (updating existing resources)
- **DELETE requests**: 🗑️ (removing resources)
- **PATCH requests**: 🔧 (partial updates)

### Status Code Ranges
- **2xx Success**: ✅ (successful operations)
- **3xx Redirect**: ↩️ (redirection responses)
- **4xx Client Error**: ❌ (client-side errors)
- **5xx Server Error**: 💥 (server-side errors)

### Common HTTP Operations
- **Authentication**: 🔐 (login/auth operations)
- **Cache operations**: ⚡ (cache hits/misses)
- **Rate limiting**: 🚦 (throttling responses)
- **Timeout**: ⏱️ (request timeouts)

## Usage Examples

### Basic HTTP Request Logging

```python
from provide.foundation import get_logger

# Create HTTP-specific logger
http_log = get_logger("http")

# Request logging
http_log.info("request_started", method="GET", path="/api/users", client_ip="192.168.1.10")
http_log.info("request_completed", method="GET", path="/api/users", status=200, duration_ms=45)
http_log.error("request_failed", method="POST", path="/api/users", status=400, error="validation failed")

# Authentication logging
http_log.info("auth_success", user_id=123, method="POST", path="/auth/login")
http_log.warning("auth_failed", method="POST", path="/auth/login", reason="invalid_credentials")

# Cache operations
http_log.debug("cache_hit", key="user:123", path="/api/users/123")
http_log.debug("cache_miss", key="user:456", path="/api/users/456")
```

### FastAPI Integration

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import time
from provide.foundation import get_logger

class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_logger("http")

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request start
        self.logger.info("request_started",
                        method=request.method,
                        path=request.url.path,
                        query=str(request.url.query) if request.url.query else None,
                        user_agent=request.headers.get("user-agent"),
                        client_ip=request.client.host)
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log successful response
            self.logger.info("request_completed",
                           method=request.method,
                           path=request.url.path,
                           status=response.status_code,
                           duration_ms=round(duration_ms, 2))
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error response
            self.logger.error("request_failed",
                            method=request.method,
                            path=request.url.path,
                            error=str(e),
                            duration_ms=round(duration_ms, 2))
            raise

app = FastAPI()
app.add_middleware(HTTPLoggingMiddleware)
```

## Configuration

### Enabling HTTP Emoji Set

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        enabled_emoji_sets=["http"]
    )
)
setup_telemetry(config)
```

## Related Documentation

- [api-Base Emoji Types](api-base.md) - Core emoji system interfaces
- [api-Custom Emoji Sets](api-custom.md) - Creating custom emoji sets  
- [api-Database Emoji Set](api-database.md) - Database operation emojis
- [Testing Guide](../../guide/testing.md) - Testing HTTP logging