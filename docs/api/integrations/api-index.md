# Integrations API

Third-party framework and service integrations for provide-foundation.

## Overview

The `integrations` module provides seamless integration with popular frameworks and services, enabling provide-foundation's structured logging and utilities to work effortlessly with your existing technology stack.

## Key Features

- **Framework Integration**: Direct support for Flask, FastAPI, Django, and other frameworks
- **Service Integration**: Integration with databases, message queues, and external APIs
- **Middleware Support**: Request/response logging and context propagation
- **Configuration Hooks**: Framework-specific configuration patterns
- **Plugin Architecture**: Extensible integration system

## Web Framework Integrations

### FastAPI Integration

```python
from fastapi import FastAPI
from provide.foundation.integrations.fastapi import setup_foundation_logging

app = FastAPI()

# Setup foundation logging for FastAPI
setup_foundation_logging(
    app,
    service_name="my-api",
    log_requests=True,
    log_responses=True,
    include_request_body=False
)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    # Request automatically logged with context
    from provide.foundation import logger
    logger.info("user_lookup", user_id=user_id)
    return {"user_id": user_id, "name": "John Doe"}
```

### Flask Integration

```python
from flask import Flask
from provide.foundation.integrations.flask import FoundationLogging

app = Flask(__name__)

# Initialize foundation logging
foundation = FoundationLogging(app)
# Or: foundation.init_app(app)

@app.route('/api/data')
def get_data():
    from provide.foundation import logger
    logger.info("data_request", endpoint="/api/data")
    return {"data": "example"}
```

### Django Integration

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'provide.foundation.integrations.django',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'foundation': {
            'class': 'provide.foundation.integrations.django.FoundationHandler',
            'service_name': 'django-app',
        },
    },
    'root': {
        'handlers': ['foundation'],
        'level': 'INFO',
    },
}

# views.py
from provide.foundation import logger
from django.http import JsonResponse

def my_view(request):
    logger.info("django_request", 
                path=request.path,
                method=request.method)
    return JsonResponse({"status": "ok"})
```

## Database Integrations

### SQLAlchemy Integration

```python
from sqlalchemy import create_engine, event
from provide.foundation.integrations.sqlalchemy import setup_logging

engine = create_engine("postgresql://localhost/mydb")

# Setup automatic query logging
setup_logging(engine, 
              log_queries=True,
              log_slow_queries=True,
              slow_query_threshold=1.0)

# Queries are automatically logged with timing and parameters
```

### Async Database Integration

```python
from provide.foundation.integrations.databases import AsyncDatabaseLogger
import databases

database = databases.Database("postgresql://localhost/mydb")

# Wrap database with logging
logged_db = AsyncDatabaseLogger(database, service_name="my-service")

async def get_users():
    # Queries automatically logged with context
    async with logged_db.transaction():
        users = await logged_db.fetch_all("SELECT * FROM users WHERE active = :active", 
                                         values={"active": True})
        return users
```

## Message Queue Integrations

### Celery Integration

```python
from celery import Celery
from provide.foundation.integrations.celery import setup_foundation_logging

app = Celery('myapp')

# Setup foundation logging for Celery
setup_foundation_logging(app, service_name="worker")

@app.task
def process_data(data):
    from provide.foundation import logger
    
    logger.info("task_started", 
                task="process_data",
                data_size=len(data))
    
    # Process data
    result = expensive_processing(data)
    
    logger.info("task_completed",
                task="process_data", 
                result_size=len(result))
    
    return result
```

### Redis Integration

```python
from provide.foundation.integrations.redis import LoggedRedisClient
import redis

# Create logged Redis client
redis_client = LoggedRedisClient(
    redis.Redis(host='localhost', port=6379),
    service_name="cache-service"
)

async def cache_operations():
    # All Redis operations are automatically logged
    await redis_client.set("user:123", json.dumps(user_data))
    cached_user = await redis_client.get("user:123")
    return json.loads(cached_user)
```

## HTTP Client Integrations

### Requests Integration

```python
from provide.foundation.integrations.requests import LoggedSession
import requests

# Create session with automatic logging
session = LoggedSession(service_name="api-client")

# All requests are logged with timing and status
response = session.get("https://api.example.com/users")
data = session.post("https://api.example.com/users", 
                   json={"name": "John"})
```

### HTTPX Integration

```python
from provide.foundation.integrations.httpx import LoggedAsyncClient
import httpx

async def api_calls():
    async with LoggedAsyncClient(service_name="async-client") as client:
        # All async requests are logged
        response = await client.get("https://api.example.com/data")
        return response.json()
```

## Cloud Service Integrations

### AWS Integration

```python
from provide.foundation.integrations.aws import setup_boto3_logging
import boto3

# Setup logging for all boto3 calls
setup_boto3_logging(service_name="aws-service")

# Create AWS clients (automatically logged)
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Operations are logged with service, operation, and timing
s3.get_object(Bucket='my-bucket', Key='data.json')
```

### Google Cloud Integration

```python
from provide.foundation.integrations.gcp import setup_gcp_logging
from google.cloud import storage

# Setup logging for GCP clients
setup_gcp_logging(service_name="gcp-service")

client = storage.Client()
bucket = client.bucket('my-bucket')

# GCP operations automatically logged
blob = bucket.blob('data.json')
content = blob.download_as_bytes()
```

## Monitoring Integrations

### Prometheus Integration

```python
from provide.foundation.integrations.prometheus import PrometheusIntegration
from prometheus_client import start_http_server

# Setup Prometheus metrics from logs
prometheus = PrometheusIntegration()
prometheus.setup_log_metrics()

# Start metrics server
start_http_server(8000)

# Log events are automatically converted to Prometheus metrics
from provide.foundation import logger
logger.info("http_request_completed", 
           method="GET", 
           status_code=200,
           duration_ms=45.2)
# Creates: http_requests_total{method="GET", status="200"}
# Creates: http_request_duration_seconds
```

### DataDog Integration

```python
from provide.foundation.integrations.datadog import DataDogIntegration

# Setup DataDog logging
datadog = DataDogIntegration(
    api_key="your-api-key",
    service_name="my-service"
)

# Structured logs are sent to DataDog with proper tags
from provide.foundation import logger
logger.info("user_action", 
           user_id="123",
           action="login",
           success=True)
```

## Custom Integrations

### Creating Custom Integrations

```python
from provide.foundation.integrations.base import BaseIntegration
from provide.foundation import logger

class CustomServiceIntegration(BaseIntegration):
    """Integration for custom service."""
    
    def __init__(self, service_name: str, config: dict):
        super().__init__(service_name)
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the service."""
        # Add custom log processors or handlers
        pass
    
    def wrap_client(self, client):
        """Wrap client with logging."""
        original_method = client.api_call
        
        def logged_api_call(*args, **kwargs):
            start_time = time.time()
            
            logger.info("api_call_started",
                       service=self.service_name,
                       method=original_method.__name__)
            
            try:
                result = original_method(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.info("api_call_completed",
                           service=self.service_name,
                           duration_ms=duration * 1000,
                           status="success")
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                
                logger.error("api_call_failed",
                            service=self.service_name,
                            duration_ms=duration * 1000,
                            error=str(e))
                raise
        
        client.api_call = logged_api_call
        return client

# Usage
integration = CustomServiceIntegration("my-service", config)
client = integration.wrap_client(MyServiceClient())
```

## Middleware Components

### Request Logging Middleware

```python
from provide.foundation.integrations.middleware import RequestLoggingMiddleware

class MyMiddleware(RequestLoggingMiddleware):
    """Custom request logging middleware."""
    
    def extract_request_info(self, request):
        """Extract information from request."""
        return {
            "method": request.method,
            "path": request.path,
            "user_agent": request.headers.get("User-Agent"),
            "ip": request.client.host if hasattr(request, 'client') else None
        }
    
    def extract_response_info(self, response):
        """Extract information from response."""
        return {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type")
        }
```

### Context Propagation Middleware

```python
from provide.foundation.integrations.middleware import ContextPropagationMiddleware

class TracingMiddleware(ContextPropagationMiddleware):
    """Middleware for request tracing."""
    
    def generate_request_id(self, request):
        """Generate unique request ID."""
        return str(uuid.uuid4())
    
    def extract_trace_context(self, request):
        """Extract tracing context from headers."""
        return {
            "trace_id": request.headers.get("X-Trace-ID"),
            "parent_span": request.headers.get("X-Parent-Span")
        }
```

## Configuration

### Integration Configuration

```python
from provide.foundation.integrations import IntegrationConfig

config = IntegrationConfig(
    service_name="my-app",
    integrations={
        "fastapi": {
            "log_requests": True,
            "log_responses": False,
            "include_headers": ["authorization", "content-type"]
        },
        "sqlalchemy": {
            "log_queries": True,
            "slow_query_threshold": 0.5,
            "log_parameters": False
        },
        "redis": {
            "log_commands": True,
            "log_pipeline_commands": False
        }
    }
)

# Apply configuration to all integrations
config.apply_all()
```

### Environment-Based Configuration

```python
# Environment variables for integration configuration
import os

config = {
    "log_requests": os.getenv("LOG_REQUESTS", "true").lower() == "true",
    "slow_query_threshold": float(os.getenv("SLOW_QUERY_THRESHOLD", "1.0")),
    "service_name": os.getenv("SERVICE_NAME", "my-service")
}
```

## Testing Integration

### Mock Integrations for Testing

```python
from provide.foundation.integrations.testing import MockIntegration

def test_integration():
    with MockIntegration("test-service") as mock:
        # Integration calls are mocked and logged
        result = my_function_that_uses_integration()
        
        # Verify integration calls
        assert mock.call_count("api_call") == 3
        assert mock.last_call("api_call").args == ("expected", "args")
```

## Performance Considerations

- **Minimal Overhead**: Integrations add <1ms overhead per operation
- **Async Support**: Full async/await support for modern frameworks
- **Batching**: Automatic batching for high-throughput operations
- **Sampling**: Configurable sampling for high-volume operations

## Best Practices

### Integration Setup
```python
# Setup integrations early in application lifecycle
def setup_app():
    setup_foundation_logging(app)
    setup_database_logging(db)
    setup_cache_logging(cache)
    
    # Continue with app setup
```

### Error Handling
```python
# Integrations should not break application flow
try:
    setup_optional_integration(service)
except IntegrationError:
    logger.warning("integration_setup_failed", 
                  service=service.name,
                  fallback="disabled")
```

### Configuration Management
```python
# Use environment-based configuration for integrations
integration_config = {
    "enabled": get_env_bool("INTEGRATION_ENABLED", True),
    "log_level": get_env("INTEGRATION_LOG_LEVEL", "INFO"),
    "options": get_env_dict("INTEGRATION_OPTIONS", {})
}
```

## API Reference

::: provide.foundation.integrations

## Related Documentation

- [Web Service Example](../../examples/web-service.md) - Framework integration examples
- [Configuration Guide](../../guide/config/index.md) - Integration configuration patterns
- [Performance Guide](../../guide/concepts/performance.md) - Integration performance impact