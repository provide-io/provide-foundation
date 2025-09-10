# Web Service

HTTP service development with structured logging and request/response tracking.

## Overview

This example demonstrates building a web service using provide-foundation for structured logging, request tracking, and error handling in HTTP applications.

## Code Example

```python
#!/usr/bin/env python3
"""
Web Service Example

Demonstrates HTTP service with structured logging and request tracking.
"""

from provide.foundation import Context, logger, setup_telemetry
from provide.foundation.console import pout, perr
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
import uuid
from typing import Any


# Initialize FastAPI app
app = FastAPI(title="Example Web Service", version="1.0.0")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Middleware to log all HTTP requests and responses."""
    # Generate request ID for tracing
    request_id = str(uuid.uuid4())
    
    # Start timing
    start_time = time.time()
    
    # Log request start
    logger.info("http_request_start",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                user_agent=request.headers.get("user-agent", "unknown"))
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log successful response
        logger.info("http_request_complete",
                   request_id=request_id,
                   method=request.method,
                   url=str(request.url),
                   status_code=response.status_code,
                   duration_ms=round(duration * 1000, 2),
                   status="success")
        
        return response
        
    except Exception as e:
        # Calculate duration for failed requests too
        duration = time.time() - start_time
        
        # Log failed response
        logger.exception("http_request_failed",
                        request_id=request_id,
                        method=request.method,
                        url=str(request.url),
                        duration_ms=round(duration * 1000, 2),
                        error=str(e))
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "request_id": request_id}
        )


@app.get("/")
async def root():
    """Root endpoint returning service information."""
    logger.info("endpoint_called", endpoint="root", operation="service_info")
    
    return {
        "service": "example-web-service",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    logger.debug("health_check_called", endpoint="health")
    
    return {
        "status": "healthy",
        "timestamp": time.time()
    }


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user information by ID."""
    logger.info("user_lookup_start", 
                endpoint="get_user",
                user_id=user_id,
                operation="user_retrieval")
    
    try:
        # Simulate user lookup
        if user_id == "invalid":
            logger.warning("user_not_found", user_id=user_id, status="not_found")
            raise HTTPException(status_code=404, detail="User not found")
        
        # Simulate database lookup
        user_data = {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
            "active": True
        }
        
        logger.info("user_lookup_complete",
                   user_id=user_id,
                   status="success",
                   operation="user_retrieval")
        
        return user_data
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.exception("user_lookup_failed",
                        user_id=user_id,
                        error=str(e),
                        operation="user_retrieval")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/users")
async def create_user(user_data: dict[str, Any]):
    """Create a new user."""
    user_id = str(uuid.uuid4())
    
    logger.info("user_creation_start",
                endpoint="create_user",
                user_id=user_id,
                operation="user_creation")
    
    try:
        # Validate required fields
        required_fields = ["name", "email"]
        missing_fields = [field for field in required_fields if field not in user_data]
        
        if missing_fields:
            logger.warning("user_creation_validation_failed",
                          user_id=user_id,
                          missing_fields=missing_fields,
                          status="validation_error")
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {missing_fields}"
            )
        
        # Simulate user creation
        created_user = {
            "id": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "active": True,
            "created_at": time.time()
        }
        
        logger.info("user_creation_complete",
                   user_id=user_id,
                   email=user_data["email"],
                   status="success",
                   operation="user_creation")
        
        return created_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.exception("user_creation_failed",
                        user_id=user_id,
                        error=str(e),
                        operation="user_creation")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    ctx = Context.from_env()
    setup_telemetry()
    
    logger.info("service_startup",
                service="example-web-service",
                version="1.0.0",
                profile=ctx.profile,
                status="started")
    
    pout("🚀 Web service started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("service_shutdown",
                service="example-web-service",
                status="stopped")
    
    pout("🛑 Web service stopped")


def main():
    """Main entry point for running the web service."""
    ctx = Context.from_env()
    
    # Configure server settings
    host = "0.0.0.0"
    port = 8000
    debug = ctx.debug
    
    pout(f"🌐 Starting web service on {host}:{port}")
    
    # Start the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        debug=debug,
        log_config=None  # Use our custom logging
    )


if __name__ == "__main__":
    main()
```

## Key Features Demonstrated

### Request/Response Logging
- Automatic logging of all HTTP requests and responses
- Request ID generation for tracing
- Duration tracking for performance monitoring
- Status code and error logging

### Structured Error Handling
- Proper exception handling with structured logging
- HTTP exception mapping with appropriate status codes
- Error context preservation for debugging

### Performance Monitoring
- Request duration measurement
- Health check endpoints for monitoring
- Structured performance metrics

### Service Lifecycle
- Startup and shutdown event handling
- Service configuration management
- Graceful error handling

## Running the Web Service

### Basic Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn
```

2. Set environment variables:
```bash
export FOUNDATION_LOG_LEVEL=INFO
export FOUNDATION_PROFILE=development
export FOUNDATION_SERVICE_NAME=example-web-service
export FOUNDATION_DEBUG=true
```

3. Run the service:
```bash
python web_service.py
```

### Testing the Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get service info
curl http://localhost:8000/

# Get user
curl http://localhost:8000/users/123

# Create user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# Test error handling
curl http://localhost:8000/users/invalid
```

## Expected Output

### Startup
```
🚀 Web service started successfully
INFO service_startup service=example-web-service version=1.0.0 profile=development status=started
```

### Request Logs
```
INFO http_request_start request_id=abc123 method=GET url=http://localhost:8000/users/123 user_agent=curl/7.68.0
INFO user_lookup_start endpoint=get_user user_id=123 operation=user_retrieval
✅ INFO user_lookup_complete user_id=123 status=success operation=user_retrieval
✅ INFO http_request_complete request_id=abc123 method=GET url=http://localhost:8000/users/123 status_code=200 duration_ms=12.34 status=success
```

### Error Logs
```
⚠️  WARNING user_not_found user_id=invalid status=not_found
❌ INFO http_request_complete request_id=def456 method=GET url=http://localhost:8000/users/invalid status_code=404 duration_ms=5.67 status=success
```

## Configuration Options

### Environment Variables
```bash
# Service configuration
export FOUNDATION_SERVICE_NAME=my-web-service
export FOUNDATION_SERVICE_VERSION=2.0.0

# Logging configuration
export FOUNDATION_LOG_LEVEL=DEBUG
export FOUNDATION_JSON_OUTPUT=true

# Performance settings
export FOUNDATION_DEBUG=false
export FOUNDATION_PROFILE=production
```

### Production Configuration
```python
def create_production_app():
    """Create app with production configuration."""
    ctx = Context(
        profile="production",
        log_level="INFO",
        debug=False,
        json_output=True,
        service_name="web-service",
        service_version="1.0.0"
    )
    
    setup_telemetry()
    return app
```

## Advanced Patterns

### Custom Request Context
```python
@app.middleware("http")
async def context_middleware(request: Request, call_next):
    """Add request context to all log messages."""
    request_id = str(uuid.uuid4())
    
    # Add context to all subsequent log messages
    with logger.bind(request_id=request_id):
        response = await call_next(request)
        return response
```

### Metrics Collection
```python
from collections import defaultdict

request_metrics = defaultdict(int)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Collect request metrics."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Update metrics
        endpoint = f"{request.method} {request.url.path}"
        request_metrics[f"{endpoint}_count"] += 1
        request_metrics[f"{endpoint}_duration"] += time.time() - start_time
        
        return response
    except Exception as e:
        request_metrics[f"{endpoint}_errors"] += 1
        raise
```

## Next Steps

- Explore [Data Pipeline](data-pipeline.md) for data processing workflows
- Learn about [CLI Tool](cli-tool.md) for command-line interfaces
- Review [Basic Application](basic-app.md) for simpler application patterns