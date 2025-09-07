# Examples Gallery

Quick, copy-paste examples for common provide.foundation use cases.

## Logging Examples

### Basic Structured Logging

```python
from provide.foundation import logger

# Simple logging with context
logger.info("user_login", 
            user_id="user-123",
            ip="192.168.1.1",
            success=True)

# With error context
try:
    process_data()
except Exception as e:
    logger.exception("processing_failed",
                    error=str(e),
                    data_size=1024)
```

### Contextual Logging

```python
from provide.foundation import logger

# Add context via structured fields
logger.info("request_started",
            request_id="req-456",
            user_id="user-123")
process_request()
logger.info("request_completed",
            request_id="req-456",
            user_id="user-123")
```

### Async Logging

```python
import asyncio
from provide.foundation import logger

async def process_async_data():
    logger.info("async_processing_started")
    
    # Simulate async work
    await asyncio.sleep(1)
    
    logger.info("async_processing_completed",
               items_processed=100)

# Run async logging
asyncio.run(process_async_data())
```

## Configuration Examples

### Environment-Based Configuration

```python
import os
from provide.foundation.logger import TelemetryConfig

# Set environment variables
os.environ['PROVIDE_LOG_LEVEL'] = 'DEBUG'
os.environ['PROVIDE_EMOJI_SET'] = 'database'

# Load from environment
config = TelemetryConfig.from_env()
```

### Custom Configuration

```python
from provide.foundation.logger import TelemetryConfig, LoggingConfig

# Custom configuration
config = TelemetryConfig(
    logging=LoggingConfig(
        level="INFO",
        emoji_set="http",
        enable_colors=True
    )
)
```

## Domain-Action-Status Pattern

```python
from provide.foundation import logger

# Database operations
logger.info("database_connection_started", host="localhost")
logger.info("database_query_executed", table="users", count=42)
logger.info("database_connection_closed")

# HTTP operations  
logger.info("http_request_received", method="POST", path="/api/users")
logger.info("http_response_sent", status=201, response_time=0.045)
```

## Exception Handling

```python
from provide.foundation import logger

try:
    risky_operation()
except ValueError as e:
    logger.exception("validation_error",
                    input_value=user_input,
                    error_type="ValueError")
except Exception as e:
    logger.exception("unexpected_error",
                    operation="risky_operation")
```

## Performance Monitoring

```python
from provide.foundation import logger
import time

def monitored_function():
    start = time.time()
    logger.info("operation_started", function="monitored_function")
    
    # Do work
    time.sleep(0.1)
    
    duration = time.time() - start
    logger.info("operation_completed",
               function="monitored_function",
               duration_ms=duration * 1000)
```

## Next Steps

- Check out the [User Guide](../guide/index.md) for detailed patterns
- See the [API Reference](../api/api-index.md) for complete documentation
- Review [Configuration](../guide/config/index.md) for setup options