# Logger API

The `provide.foundation.logger` module provides structured logging with emoji support, semantic layers, and high performance.

## Overview

The logger system provides:
- Structured logging with contextual key-value pairs
- Emoji-enhanced visual parsing
- Domain-specific semantic layers (LLM, HTTP, Database)
- Thread-safe operations
- Async compatibility
- Performance >14,000 msg/sec

## Quick Start

```python
from provide.foundation import logger, plog

# Use the global logger
logger.info("Application started", version="1.0.0")

# Use plog alias (recommended)
plog.info("Request received", method="GET", path="/api/users")

# Get a module-specific logger
from provide.foundation.logger import get_logger
log = get_logger(__name__)
log.debug("Processing item", item_id=123)
```

## Core Components

### Global Logger Instance

The `logger` and `plog` are pre-configured global instances ready for use:

```python
from provide.foundation import logger, plog

# Both are aliases to the same logger
logger.info("Using logger")
plog.info("Using plog")  # Recommended alias

# Add structured context
plog.info("User action", 
    user_id="123",
    action="login",
    ip="192.168.1.1"
)

# Log at different levels
plog.debug("Debug information", details={"key": "value"})
plog.info("Informational message")
plog.warning("Warning message", threshold=0.8)
plog.error("Error occurred", error_code="E001")
plog.critical("Critical failure", service="database")
```

### Module-Specific Loggers

Create loggers for specific modules or components:

```python
from provide.foundation.logger import get_logger

# Create a module logger
log = get_logger(__name__)

# Or with a custom name
api_log = get_logger("api.endpoints")
db_log = get_logger("database.queries")

# Use like the global logger
api_log.info("Endpoint called", endpoint="/users", method="GET")
db_log.debug("Query executed", query="SELECT * FROM users", rows=10)
```

### Structured Context

Add persistent context to all log messages:

```python
from provide.foundation import plog

# Bind context to logger
request_log = plog.bind(
    request_id="req-123",
    user_id="user-456",
    session_id="sess-789"
)

# All messages include bound context
request_log.info("Processing request")  
# Output includes: request_id, user_id, session_id

request_log.error("Request failed", error="timeout")
# Output includes: request_id, user_id, session_id, error

# Create child loggers with additional context
step_log = request_log.bind(step="validation")
step_log.info("Validating input")
# Output includes all parent context plus step
```

### Lazy Evaluation

Use lambda functions for expensive computations:

```python
from provide.foundation import plog

# Expensive computation only runs if debug is enabled
plog.debug("Database state", 
    stats=lambda: calculate_expensive_stats()
)

# Use for any expensive operation
plog.info("Processing complete",
    summary=lambda: generate_summary(results)
)
```

## Configuration

### Setup Function

Configure the logger at application startup:

```python
from provide.foundation import setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Basic setup
setup_telemetry(
    service_name="my-service",
    log_level="INFO"
)

# Advanced configuration
config = TelemetryConfig(
    service_name="my-service",
    logging=LoggingConfig(
        level="DEBUG",
        format="console",  # or "json"
        use_colors=True,
        show_timestamp=True,
        show_caller=True,
        emoji_mode="emoji"  # or "text", "none"
    )
)
setup_telemetry(config)
```

### Environment Variables

Configure via environment variables:

```bash
# Basic configuration
export TELEMETRY_SERVICE_NAME="my-service"
export TELEMETRY_LOG_LEVEL="DEBUG"
export TELEMETRY_LOG_FORMAT="json"

# Advanced options
export TELEMETRY_USE_COLORS="false"
export TELEMETRY_SHOW_TIMESTAMP="true"
export TELEMETRY_EMOJI_MODE="text"
export TELEMETRY_SEMANTIC_LAYERS="llm,http"
```

Load from environment:

```python
from provide.foundation.logger.config import TelemetryConfig

# Load configuration from environment
config = TelemetryConfig.from_env()
setup_telemetry(config)
```

## Semantic Layers

Use domain-specific logging with specialized emoji mappings:

### LLM Layer

```python
from provide.foundation import plog

# Enable LLM semantic layer
from provide.foundation import setup_telemetry
setup_telemetry(semantic_layers=["llm"])

# LLM-specific logging
plog.info("LLM request",
    llm_provider="openai",
    llm_model="gpt-4",
    llm_tokens=500
)
# Output: 🤖 LLM request

plog.info("Prompt sent",
    llm_action="prompt",
    prompt_tokens=100
)
# Output: 💭 Prompt sent
```

### HTTP Layer

```python
# Enable HTTP semantic layer
setup_telemetry(semantic_layers=["http"])

# HTTP-specific logging
plog.info("API request",
    http_method="GET",
    http_path="/users",
    http_status=200
)
# Output: 🔽 API request (for GET)

plog.error("Request failed",
    http_method="POST",
    http_status=500
)
# Output: 🔺❌ Request failed (POST with error)
```

### Database Layer

```python
# Enable Database semantic layer
setup_telemetry(semantic_layers=["database"])

# Database-specific logging
plog.info("Query executed",
    db_operation="select",
    db_table="users",
    db_rows=10
)
# Output: 🔍 Query executed

plog.info("Data inserted",
    db_operation="insert",
    db_table="orders"
)
# Output: ➕ Data inserted
```

## Performance Considerations

### High-Performance Logging

```python
from provide.foundation import plog

# Use structured fields instead of string formatting
# Good - structured
plog.info("User logged in", user_id=123, ip="192.168.1.1")

# Less efficient - string formatting
plog.info(f"User {user_id} logged in from {ip}")

# Batch context binding
batch_log = plog.bind(
    batch_id="batch-001",
    total_items=1000
)
for i, item in enumerate(items):
    batch_log.debug("Processing", item=i)
```

### Conditional Logging

```python
# Check log level before expensive operations
if plog.isEnabledFor("DEBUG"):
    debug_info = expensive_debug_calculation()
    plog.debug("Debug info", data=debug_info)

# Or use lazy evaluation
plog.debug("Debug info", 
    data=lambda: expensive_debug_calculation()
)
```

## Testing with Logger

### Capture Log Output

```python
import io
from provide.foundation import setup_telemetry, plog

def test_logging():
    # Capture logs to a string
    output = io.StringIO()
    setup_telemetry(
        service_name="test",
        log_format="json",
        output_stream=output
    )
    
    # Your code that logs
    plog.info("Test message", value=42)
    
    # Check output
    logs = output.getvalue()
    assert "Test message" in logs
    assert '"value": 42' in logs
```

### Mock Logger

```python
from unittest.mock import Mock, patch

@patch('provide.foundation.plog')
def test_with_mock_logger(mock_log):
    # Your code
    my_function()
    
    # Verify logging
    mock_log.info.assert_called_with(
        "Expected message",
        expected_field="value"
    )
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, Request
from provide.foundation import plog, setup_telemetry

app = FastAPI()

@app.on_event("startup")
async def startup():
    setup_telemetry(service_name="api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_log = plog.bind(
        request_id=request.headers.get("X-Request-ID"),
        method=request.method,
        path=request.url.path
    )
    
    request_log.info("Request received")
    response = await call_next(request)
    request_log.info("Request completed", status=response.status_code)
    
    return response
```

### Async Context

```python
import asyncio
from provide.foundation import plog

async def async_operation(item_id):
    log = plog.bind(item_id=item_id)
    log.info("Starting async operation")
    
    try:
        result = await process_item(item_id)
        log.info("Operation completed", result=result)
    except Exception as e:
        log.error("Operation failed", error=str(e))
        raise
```

## Best Practices

1. **Use structured logging**:
   ```python
   # Good
   plog.info("User action", user_id=123, action="login")
   
   # Avoid
   plog.info(f"User {user_id} performed {action}")
   ```

2. **Bind context early**:
   ```python
   # Bind request context once
   request_log = plog.bind(request_id=req_id)
   request_log.info("Starting")
   # ... use request_log throughout
   ```

3. **Use appropriate log levels**:
   ```python
   plog.debug("Detailed diagnostic info")
   plog.info("Normal operations")
   plog.warning("Warning conditions")
   plog.error("Error conditions")
   plog.critical("Critical failures")
   ```

4. **Include relevant context**:
   ```python
   plog.error("Database connection failed",
       host=db_host,
       port=db_port,
       error=str(e),
       retry_count=retries
   )
   ```

5. **Use semantic layers for domain-specific logging**:
   ```python
   setup_telemetry(semantic_layers=["http", "database"])
   ```

## API Reference

### Functions

- `setup_telemetry(config)` - Configure the logging system
- `get_logger(name)` - Get a named logger instance
- `reset_foundation_setup()` - Reset logger configuration (for testing)

### Classes

- `FoundationLogger` - Main logger class
- `TelemetryConfig` - Configuration data class
- `LoggingConfig` - Logging-specific configuration

### Global Instances

- `logger` - Global logger instance
- `plog` - Recommended alias for logger

## See Also

- [Configuration](config.md) - Detailed configuration options
- [Console Output](console.md) - CLI output functions
- [Semantic Layers](semantic-layers.md) - Domain-specific logging