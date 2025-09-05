# Exception Logging

Exception handling and logging patterns in provide.foundation.

## Overview

provide.foundation provides comprehensive exception logging capabilities with automatic traceback capture, structured error context, and integration with the error handling system. Exception logging preserves full stack traces while adding semantic context for debugging.

## Basic Exception Logging

### Using exception()

Log exceptions with full traceback:

```python
from provide.foundation import logger

try:
    risky_operation()
except Exception as e:
    # Logs with full stack trace
    logger.exception("Operation failed")
    # Re-raise if needed
    raise
```

### Using error() with exc_info

Control traceback inclusion:

```python
try:
    process_data()
except ValueError as e:
    # With traceback
    logger.error("Invalid data", exc_info=True)
    
    # Without traceback (just the error message)
    logger.error("Invalid data", error=str(e), exc_info=False)
```

### Structured Exception Context

Add context to exception logs:

```python
try:
    user = fetch_user(user_id)
    process_user(user)
except UserNotFoundError as e:
    logger.exception(
        "User processing failed",
        user_id=user_id,
        error_type=type(e).__name__,
        error_code=getattr(e, 'code', None),
        attempt=retry_count,
        context={
            "endpoint": "/api/users",
            "method": "GET",
            "timestamp": datetime.now().isoformat()
        }
    )
```

## Error Decorators

### @with_error_handling

Automatic error logging decorator:

```python
from provide.foundation.errors import with_error_handling

@with_error_handling(
    fallback=None,
    log_errors=True,
    suppress=(KeyError, ValueError)
)
def process_data(data: dict):
    """Process with automatic error handling."""
    # Exceptions are logged automatically
    result = data['required_key']
    validate(result)  # May raise ValueError
    return transform(result)

# Async version works the same
@with_error_handling(log_errors=True)
async def async_process(data: dict):
    result = await fetch_data()
    return process(result)
```

### Context Provider

Add dynamic context to error logs:

```python
def get_request_context():
    """Provide context for error logging."""
    return {
        "request_id": current_request.id,
        "user_id": current_user.id,
        "timestamp": time.time()
    }

@with_error_handling(
    context_provider=get_request_context,
    log_errors=True
)
def handle_request():
    # Errors include request context
    process_request()
```

### Error Mapping

Transform exceptions before logging:

```python
def map_database_errors(exc: Exception) -> Exception:
    """Map database errors to domain errors."""
    if isinstance(exc, IntegrityError):
        return ValidationError(f"Data validation failed: {exc}")
    return exc

@with_error_handling(
    error_mapper=map_database_errors,
    log_errors=True
)
def save_record(record):
    # Database errors are mapped and logged
    database.save(record)
```

## Retry with Logging

### @with_retry

Retry operations with exception logging:

```python
from provide.foundation.errors import with_retry

@with_retry(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    log_retries=True,
    exceptions=(ConnectionError, TimeoutError)
)
def unstable_connection():
    """Retries on specific exceptions."""
    response = make_request()
    if not response.ok:
        raise ConnectionError(f"Failed: {response.status}")
    return response.data

# Each retry logs:
# - Attempt number
# - Exception that triggered retry
# - Delay before next attempt
```

### Custom Retry Logic

Implement custom retry with logging:

```python
async def retry_with_logging(func, max_attempts=3):
    """Custom retry with detailed logging."""
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_attempts}",
                       function=func.__name__)
            result = await func()
            if attempt > 1:
                logger.info(f"Succeeded after {attempt} attempts",
                           function=func.__name__)
            return result
            
        except Exception as e:
            logger.warning(
                f"Attempt {attempt} failed",
                function=func.__name__,
                error=str(e),
                exc_info=(attempt == max_attempts)  # Full trace on last attempt
            )
            
            if attempt == max_attempts:
                logger.error(f"All {max_attempts} attempts failed",
                            function=func.__name__)
                raise
            
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Custom Exception Types

### Foundation Errors

Use foundation's error types with logging:

```python
from provide.foundation.errors import (
    FoundationError,
    ConfigurationError,
    ValidationError
)

class ServiceError(FoundationError):
    """Custom service error with context."""
    
    def __init__(self, message: str, service: str, **context):
        super().__init__(message, **context)
        self.service = service

try:
    result = call_service()
except Exception as e:
    # Wrap and log with context
    error = ServiceError(
        f"Service call failed: {e}",
        service="user-api",
        endpoint="/users",
        original_error=str(e)
    )
    logger.error("Service error", 
                error=error.to_dict(),
                exc_info=True)
    raise error
```

### Error Serialization

Serialize exceptions for structured logging:

```python
def serialize_exception(exc: Exception) -> dict:
    """Convert exception to loggable dict."""
    return {
        "type": type(exc).__name__,
        "module": type(exc).__module__,
        "message": str(exc),
        "args": exc.args,
        "attributes": {
            k: v for k, v in vars(exc).items()
            if not k.startswith('_')
        }
    }

try:
    dangerous_operation()
except Exception as e:
    logger.error("Operation failed",
                exception=serialize_exception(e),
                exc_info=True)
```

## Exception Chains

### Handling Cause Chains

Log exception chains properly:

```python
def process_with_chain():
    try:
        data = load_data()
    except IOError as e:
        raise ProcessingError("Failed to load") from e

try:
    process_with_chain()
except ProcessingError as e:
    # Logs the full chain
    logger.exception("Processing failed")
    
    # Or manually log the chain
    logger.error(
        "Processing error with cause",
        error=str(e),
        cause=str(e.__cause__) if e.__cause__ else None,
        exc_info=True
    )
```

### Context Managers

Use context managers for exception handling:

```python
from contextlib import contextmanager

@contextmanager
def logged_operation(operation_name: str):
    """Context manager with exception logging."""
    logger.info(f"Starting {operation_name}")
    try:
        yield
        logger.info(f"Completed {operation_name}")
    except Exception as e:
        logger.exception(
            f"Failed {operation_name}",
            operation=operation_name,
            error_type=type(e).__name__
        )
        raise

# Usage
with logged_operation("data_import"):
    import_data()
    process_data()
    validate_data()
```

## Pattern Examples

### API Error Handler

Centralized API error handling:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with logging."""
    
    # Generate error ID for tracking
    error_id = str(uuid.uuid4())
    
    # Log with full context
    logger.exception(
        "Unhandled API error",
        error_id=error_id,
        path=request.url.path,
        method=request.method,
        client=request.client.host if request.client else None,
        headers=dict(request.headers),
        error_type=type(exc).__name__
    )
    
    # Return sanitized error response
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_id": error_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### Background Task Errors

Handle errors in background tasks:

```python
import asyncio
from typing import Coroutine

class TaskManager:
    """Manage background tasks with error logging."""
    
    def __init__(self):
        self.tasks = set()
    
    def create_task(self, coro: Coroutine, name: str = None):
        """Create monitored background task."""
        task = asyncio.create_task(coro)
        task.add_done_callback(
            lambda t: self._handle_task_result(t, name)
        )
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task
    
    def _handle_task_result(self, task: asyncio.Task, name: str):
        """Log task exceptions."""
        try:
            task.result()
        except asyncio.CancelledError:
            logger.info(f"Task cancelled: {name or task.get_name()}")
        except Exception:
            logger.exception(
                f"Background task failed: {name or task.get_name()}",
                task_name=name,
                task_id=id(task)
            )
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# Good: Appropriate levels for different scenarios
try:
    result = operation()
except ValidationError as e:
    logger.warning("Validation failed", error=str(e))  # Expected error
except ConnectionError as e:
    logger.error("Connection failed", exc_info=True)  # Recoverable error
except Exception as e:
    logger.exception("Critical failure")  # Unexpected error
```

### 2. Include Context

```python
# Good: Rich context for debugging
logger.exception(
    "Payment processing failed",
    user_id=user.id,
    amount=payment.amount,
    currency=payment.currency,
    payment_method=payment.method,
    attempt=retry_count,
    processing_time=time.time() - start_time
)
```

### 3. Sanitize Sensitive Data

```python
# Good: Remove sensitive information
def sanitize_error(exc: Exception) -> str:
    """Remove sensitive data from error messages."""
    message = str(exc)
    # Remove passwords, tokens, etc.
    message = re.sub(r'password=\S+', 'password=***', message)
    message = re.sub(r'token=\S+', 'token=***', message)
    return message

logger.error("Auth failed", error=sanitize_error(e))
```

### 4. Structured Over Strings

```python
# Bad: Concatenated strings
logger.error(f"Failed to process user {user_id} with error {e}")

# Good: Structured fields
logger.error("Failed to process user",
            user_id=user_id,
            error=str(e),
            error_type=type(e).__name__)
```

## Related Topics

- [Basic Usage](basic.md) - Core logging concepts
- [Configuration](config.md) - Logger configuration  
- [Async Logging](async.md) - Async error handling