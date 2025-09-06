# User Guide

Comprehensive guide to using provide.foundation in your applications.

## Guide Organization

<div class="feature-grid">
  <div class="feature-card">
    <h3>📖 Core Concepts</h3>
    <p>Understand the fundamental principles behind provide.foundation</p>
    <ul>
      <li><a href="concepts/structured-logging/">Structured Logging</a></li>
      <li><a href="concepts/emoji-sets/">Emoji Sets</a></li>
      <li><a href="concepts/emoji-system/">Emoji System</a></li>
      <li><a href="concepts/das-pattern/">Domain-Action-Status Pattern</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>⚙️ Config</h3>
    <p>Learn how to configure provide.foundation for your needs</p>
    <ul>
      <li><a href="config/environment/">Environment Variables</a></li>
      <li><a href="config/files/">Config Files</a></li>
      <li><a href="config/runtime/">Runtime Config</a></li>
      <li><a href="config/best-practices/">Best Practices</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>📝 Logging & Tracing</h3>
    <p>Master logging and distributed tracing</p>
    <ul>
      <li><a href="logging/basic/">Basic Logging</a></li>
      <li><a href="logging/advanced/">Advanced Patterns</a></li>
      <li><a href="tracing/">Distributed Tracing</a></li>
      <li><a href="logging/performance/">Performance Tuning</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🖥️ CLI Framework</h3>
    <p>Build powerful command-line interfaces</p>
    <ul>
      <li><a href="cli/commands/">Command Registration</a></li>
      <li><a href="cli/nested/">Nested Commands</a></li>
      <li><a href="cli/arguments/">Arguments & Options</a></li>
      <li><a href="cli/output/">Output Formatting</a></li>
    </ul>
  </div>

  <div class="feature-card">
    <h3>🔧 System Utilities</h3>
    <p>Leverage cross-platform system utilities</p>
    <ul>
      <li><a href="utilities/platform/">Platform Detection</a></li>
      <li><a href="utilities/process/">Process Execution</a></li>
      <li><a href="utilities/console/">Console Output</a></li>
      <li><a href="utilities/registry/">Registry Pattern</a></li>
    </ul>
  </div>
</div>

## Quick Reference

### Environment Variables

```bash
# Logging configuration
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_CONSOLE_FORMATTER=key_value  # or "json"
export PROVIDE_LOG_OMIT_TIMESTAMP=false

# Service configuration
export PROVIDE_SERVICE_NAME=my-service
export PROVIDE_ENVIRONMENT=production
```

### Common Patterns

#### Contextual Logging
```python
# From examples/06_trace_logging.py
from provide.foundation import logger

# Add context via structured fields
logger.info("processing_started", request_id="abc-123")
logger.debug("step_1_completed", request_id="abc-123")
```

See [examples/06_trace_logging.py](https://github.com/provide-io/provide-foundation/blob/main/examples/06_trace_logging.py) for complete example.

#### Error Handling
```python
from provide.foundation.errors import with_error_handling

@with_error_handling
def risky_operation():
    # Automatic error logging and recovery
    pass
```

#### CLI with Subcommands
```python
# From examples/12_cli_application.py
from provide.foundation.hub import register_command

@register_command("db.migrate")
def migrate():
    """Run database migrations."""
    pass

@register_command("db.seed")
def seed():
    """Seed the database."""
    pass
```

See [examples/12_cli_application.py](https://github.com/provide-io/provide-foundation/blob/main/examples/12_cli_application.py) for complete example.

## Best Practices

### 1. Use Structured Data
```python
# Good - structured data
logger.info("user_action", 
            action="login",
            user_id=user.id,
            ip=request.ip)

# Avoid - string formatting
logger.info(f"User {user.id} logged in from {request.ip}")
```

### 2. Use Domain-Action-Status Pattern
```python
# From examples/04_das_logging.py
from provide.foundation import logger

logger.info("http_request_started", method="GET", path="/api/users")
logger.info("http_request_completed", status=200, duration_ms=42)
```

See [examples/04_das_logging.py](https://github.com/provide-io/provide-foundation/blob/main/examples/04_das_logging.py) for complete example.

### 3. Request Tracing
```python
# From examples/06_trace_logging.py
async def handle_request(request):
    # Add request_id to all logs for this request
    logger.info("request_received", request_id=request.id)
    result = await process(request)
    logger.info("request_completed", request_id=request.id, result=result)
    return result
```

### 4. Performance Optimization
```python
# Use appropriate log levels
logger.debug("detailed_info")  # Development only
logger.info("important_event")  # Production
logger.error("error_occurred")  # Always

# Log important events
for item in items:
    logger.info("item_processed", item_id=item.id)
```

## Advanced Topics

These advanced topics are covered in the existing guides:
- **Custom Emoji Sets** - See [Emoji Sets Guide](concepts/emoji-sets.md)
- **Distributed Tracing** - See [Tracing Guide](tracing/)  
- **Production Strategies** - See [Performance Guide](logging/performance.md)
- **Error Handling** - See [Advanced Logging Guide](logging/advanced.md)

## Next Steps

- Explore the [API Reference](../api/index.md) for detailed documentation
- Browse the [Examples](../getting-started/examples.md) for practical patterns
- Review the [Architecture](../architecture/index.md) for technical details