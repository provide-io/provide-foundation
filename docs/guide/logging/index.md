# Logging Guide

Foundation's structured logging system provides beautiful, high-performance logging with emoji-enhanced visual parsing and comprehensive observability features.

## Overview

Foundation logging offers:

- 📊 **Structured Data** - Key-value pairs for analysis and searchability
- 🎨 **Visual Enhancement** - Emoji prefixes for quick visual parsing
- ⚡ **High Performance** - >14,000 messages/second throughput
- 🔒 **Thread Safety** - Safe for concurrent and async applications
- 🎯 **Domain-Specific** - Specialized emoji sets for different domains
- 🔄 **Async Compatible** - Full async/await support

## Logging Guide Structure

### [📚 Basic Logging](basic.md)
Fundamental logging patterns and usage:
- Log levels and hierarchy
- Structured data with key-value pairs
- Message formatting and best practices
- Context binding and named loggers
- Output formats (pretty, JSON, compact, plain)
- Emoji system basics
- Exception logging
- Performance tips

### [⚙️ Advanced Patterns](advanced.md)
Advanced logging techniques and patterns:
- Custom processors and formatters
- Dynamic log level configuration
- Logger hierarchies and inheritance
- Custom emoji sets and domain mapping
- Filtering and sampling strategies
- Integration with external systems
- Production patterns and monitoring

### [🔄 Async Logging](async.md)
Asynchronous logging patterns:
- Async/await compatibility
- Context propagation in async code
- Performance considerations for async apps
- Integration with asyncio applications
- Error handling in async contexts

### [🎯 Context Management](context.md)
Managing log context and correlation:
- Request IDs and trace correlation
- Context propagation patterns
- Thread-local and async-local context
- Context managers and decorators
- Scoped logging contexts
- Cross-service context propagation

### [⚠️ Exception Handling](exceptions.md)
Effective exception and error logging:
- Exception logging best practices
- Automatic traceback capture
- Error context and metadata
- Error boundaries and recovery
- Structured error information
- Integration with error tracking systems

### [⚡ Performance Tuning](performance.md)
Optimizing logging performance:
- Benchmarking and profiling
- Level-based filtering optimization
- Lazy evaluation techniques
- Batching and buffering strategies
- Memory usage optimization
- Production performance patterns

## Quick Reference

### Essential Imports

```python
from provide.foundation import logger, setup_telemetry
from provide.foundation import LoggingConfig, TelemetryConfig
from provide.foundation import get_logger
```

### Basic Logging

```python
# Simple structured logging
logger.info("User action completed", 
           user_id="usr_123", 
           action="login", 
           duration_ms=245)

# Exception logging with context
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed", 
                    operation="user_creation",
                    user_data={"email": "user@example.com"})
```

### Configuration

```python
# Environment-based setup
import os
os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "json"

# Programmatic setup
config = TelemetryConfig(
    service_name="my-service",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="key_value",
        das_emoji_prefix_enabled=True
    )
)
setup_telemetry(config)
```

### Named Loggers

```python
# Component-specific loggers
db_logger = get_logger("database")
api_logger = get_logger("api.handlers")
auth_logger = get_logger("auth.service")

# Each maintains separate context
db_logger.info("Query executed", table="users", duration_ms=15)
api_logger.info("Request processed", endpoint="/api/users", status=200)
```

### Domain-Action-Status Pattern

```python
# Clear, searchable event names
logger.info("database_connection_established", host="localhost", port=5432)
logger.info("api_request_completed", method="GET", path="/users", status=200)
logger.error("payment_processing_failed", amount=99.99, error="card_declined")
```

## Log Levels

| Level | Numeric | Usage | Examples |
|-------|---------|--------|----------|
| `TRACE` | 5 | Ultra-verbose debugging | Function entry/exit, variable states |
| `DEBUG` | 10 | Development debugging | SQL queries, API calls, calculations |
| `INFO` | 20 | Normal operations | Business events, system status |
| `WARNING` | 30 | Concerning situations | Retries, fallbacks, deprecations |
| `ERROR` | 40 | Error conditions | Failures, exceptions, invalid states |
| `CRITICAL` | 50 | System failures | Service unavailable, data corruption |

## Output Formats

### Key-Value Format (Development)
```
✅ user_login user_id=usr_123 ip=192.168.1.1 success=true duration_ms=150
```

### JSON Format (Production)
```json
{"event": "user_login", "level": "info", "user_id": "usr_123", "ip": "192.168.1.1", "success": true, "duration_ms": 150, "timestamp": "2024-01-20T10:30:00Z"}
```

### Compact Format (CI/CD)
```
[INFO] user_login user_id=usr_123 success=true
```

## Environment Variables Quick Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PROVIDE_LOG_LEVEL` | `DEBUG` | Minimum log level |
| `PROVIDE_LOG_CONSOLE_FORMATTER` | `key_value` | Output format |
| `PROVIDE_LOG_DAS_EMOJI_ENABLED` | `true` | Enable DAS emoji prefixes |
| `PROVIDE_LOG_MODULE_LEVELS` | `{}` | Per-module log levels |
| `PROVIDE_LOG_FILE` | `None` | Log file path |

## Common Patterns

### Request Logging
```python
def handle_request(request):
    request_logger = logger.bind(request_id=request.id)
    request_logger.info("request_started", method=request.method, path=request.path)
    
    try:
        response = process_request(request)
        request_logger.info("request_completed", status=response.status, duration_ms=get_duration())
        return response
    except Exception as e:
        request_logger.exception("request_failed", error=str(e))
        raise
```

### Database Operations
```python
def query_users(filters):
    with logger.bind(operation="query_users"):
        logger.info("database_query_started", table="users", filters=filters)
        
        try:
            users = db.execute(query, filters)
            logger.info("database_query_completed", 
                       row_count=len(users), 
                       duration_ms=query_time)
            return users
        except Exception as e:
            logger.exception("database_query_failed", query=query, filters=filters)
            raise
```

### Background Tasks
```python
async def process_background_job(job):
    job_logger = logger.bind(job_id=job.id, job_type=job.type)
    job_logger.info("job_started", priority=job.priority)
    
    try:
        result = await execute_job(job)
        job_logger.info("job_completed", result=result, duration_ms=get_duration())
    except Exception as e:
        job_logger.exception("job_failed", error=str(e), retry_count=job.retry_count)
        raise
```

## Best Practices

### ✅ Do

- **Use structured data**: `logger.info("user_action", user_id=123, action="login")`
- **Follow DAS pattern**: `"domain_action_status"` event names
- **Include context**: Request IDs, user IDs, correlation data
- **Log at appropriate levels**: DEBUG for development, INFO for business events
- **Use named loggers**: Separate loggers for different components

### ❌ Don't

- **Log sensitive data**: Passwords, tokens, personal information
- **Use string formatting**: `f"User {id} logged in"` (not searchable)
- **Over-log in hot paths**: Sample high-frequency operations
- **Ignore performance**: Check log levels before expensive operations
- **Mix concerns**: Keep business logic separate from logging

## Integration Examples

### FastAPI Integration
```python
from fastapi import FastAPI, Request
from provide.foundation import logger
import time

app = FastAPI()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = generate_request_id()
    
    request_logger = logger.bind(request_id=request_id)
    request_logger.info("http_request_started", 
                       method=request.method, 
                       url=str(request.url))
    
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    
    request_logger.info("http_request_completed",
                       status_code=response.status_code,
                       duration_ms=duration)
    
    return response
```

### Error Boundaries
```python
from functools import wraps

def log_exceptions(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info(f"{operation_name}_completed", 
                           function=func.__name__)
                return result
            except Exception as e:
                logger.exception(f"{operation_name}_failed",
                               function=func.__name__,
                               error_type=type(e).__name__)
                raise
        return wrapper
    return decorator

@log_exceptions("user_registration")
def register_user(email, password):
    # Registration logic here
    return create_user(email, password)
```

## Related Documentation

- 📖 **[Configuration Guide](../config/index.md)** - Configuring logging behavior
- 🔍 **[Tracing Guide](../tracing/index.md)** - Distributed tracing integration  
- 📊 **[API Reference](../../api/logger/index.md)** - Complete logging API
- 🏗️ **[Architecture](../../architecture/index.md)** - Technical specifications
- 💡 **[Examples](../../getting-started/examples.md)** - Working code examples

## Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/provide-io/provide-foundation/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/provide-io/provide-foundation/discussions)  
- 📚 **Full Documentation**: [docs.provide.foundation](https://docs.provide.foundation)