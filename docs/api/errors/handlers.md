# Handler System

Configurable error policies and integration support for logging, monitoring, and external systems.

## `error_boundary()`

Context manager for handling errors at specific boundaries.

**Parameters:**
- `expected_exceptions`: Exception types to handle
- `log_errors` (bool): Whether to log errors (default: True)
- `reraise` (bool): Whether to reraise after handling (default: True)
- `handler`: Custom error handler function

**Example:**
```python
from provide.foundation.errors import error_boundary

with error_boundary(ValidationError, log_errors=True, reraise=False):
    process_user_input(data)

# Custom handler
def custom_handler(error):
    send_alert(f"Critical error: {error}")

with error_boundary(CriticalError, handler=custom_handler):
    critical_operation()
```

## `transactional()`

Decorator for transactional operations with rollback support.

**Example:**
```python
from provide.foundation.errors import transactional

@transactional(rollback_on=(DatabaseError, ValidationError))
def update_user_profile(user_id, data):
    db.begin_transaction()
    try:
        user = db.get_user(user_id)
        user.update(data)
        db.commit()
    except Exception:
        db.rollback()
        raise
```

## `ErrorHandler`

Configurable error handler with type-based policies.

**Methods:**
- `register(exception_type, handler)`: Register handler for exception type
- `handle(exception)`: Handle an exception using registered handlers
- `set_default_handler(handler)`: Set default handler for unregistered types

**Example:**
```python
from provide.foundation.errors import ErrorHandler

handler = ErrorHandler()

# Register specific handlers
handler.register(ValidationError, lambda e: {"error": "validation", "details": str(e)})
handler.register(AuthenticationError, lambda e: {"error": "auth", "redirect": "/login"})

# Set default
handler.set_default_handler(lambda e: {"error": "internal", "message": "Something went wrong"})

# Use handler
try:
    risky_operation()
except Exception as e:
    response = handler.handle(e)
    return jsonify(response), 400
```

## Integration Support

### Logging Integration

```python
from provide.foundation.errors import setup_error_logging
from provide.foundation import get_logger

logger = get_logger(__name__)

# Automatic error logging
setup_error_logging(logger, include_context=True, include_stack_trace=True)

try:
    operation()
except Exception as e:
    # Error is automatically logged with full context
    pass
```

### Monitoring Integration

```python
from provide.foundation.errors import ErrorMetrics

metrics = ErrorMetrics()

try:
    operation()
except Exception as e:
    metrics.record_error(type(e).__name__, severity="high")
    raise

# Get metrics
error_stats = metrics.get_stats()
print(f"Total errors: {error_stats.total}")
print(f"Error rate: {error_stats.rate_per_minute}")
```

### API Error Responses

```python
from provide.foundation.errors import format_api_error

try:
    api_operation()
except ValidationError as e:
    error_response = format_api_error(e, include_details=True)
    return jsonify(error_response), 400
except AuthenticationError as e:
    error_response = format_api_error(e, include_details=False)
    return jsonify(error_response), 401
```

## Best Practices

1. **Layer Error Handling**: Handle errors at appropriate boundaries
2. **Use Appropriate Error Types**: Choose specific exception types
3. **Add Context**: Include relevant debugging information
4. **Log Strategically**: Log at the right level and location