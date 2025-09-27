# Error Handling

Comprehensive error handling utilities for robust applications.

## Related API Reference

For detailed API documentation, see:
- [Error API Overview](../../api/errors/api-index.md) - Exception classes and utilities
- [Error Decorators API](../../api/errors/api-decorators.md) - Decorator-based error handling
- [Error Handlers API](../../api/errors/api-handlers.md) - Custom error handling logic

## Overview

provide.foundation's error handling system provides structured exceptions, automatic retry logic, error decorators, and integration with the logging system. It ensures consistent error handling across applications with proper context preservation.

## Exception Classes

### FoundationError Base

Base exception class with structured context:

```python
from provide.foundation.errors import FoundationError

# Basic usage
raise FoundationError("Operation failed")

# With error code
raise FoundationError("Invalid input", code="VAL_001")

# With context
raise FoundationError(
    "Database connection failed",
    host="db.example.com",
    port=5432,
    attempts=3
)

# Chain exceptions
try:
    risky_operation()
except Exception as e:
    raise FoundationError(
        "Operation failed",
        cause=e,
        operation="data_sync"
    ) from e
```

### Built-in Error Types

Specialized error classes:

```python
from provide.foundation.errors import (
    ConfigurationError,
    ValidationError,
    NetworkError,
    TimeoutError,
    RetryableError
)

# Configuration errors
if not config.get("api_key"):
    raise ConfigurationError(
        "Missing API key",
        config_file="settings.yml",
        required_keys=["api_key", "api_secret"]
    )

# Validation errors
if not is_valid_email(email):
    raise ValidationError(
        "Invalid email format",
        field="email",
        value=email,
        pattern=EMAIL_REGEX
    )

# Network errors with retry hints
raise NetworkError(
    "Connection timeout",
    endpoint="https://api.example.com",
    timeout=30,
    retryable=True
)
```

## Error Decorators

### @resilient

Automatic error handling and logging:

```python
from provide.foundation.errors import resilient

@resilient(
    fallback=None,
    log_errors=True,
    suppress=(KeyError, ValueError)
)
def process_data(data: dict):
    """Process with automatic error handling."""
    result = data['key']  # KeyError suppressed
    validate(result)      # ValueError suppressed
    return transform(result)

# With context provider
def get_context():
    return {
        "user_id": current_user.id,
        "request_id": request.id
    }

@resilient(
    context_provider=get_context,
    log_errors=True
)
def handle_request():
    # Errors logged with context
    process_request()
```

### @with_retry

Retry operations with backoff:

```python
from provide.foundation.errors import with_retry

@with_retry(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    exceptions=(NetworkError, TimeoutError),
    log_retries=True
)
def call_api():
    """Retry on network errors."""
    response = requests.get("https://api.example.com")
    if response.status_code >= 500:
        raise NetworkError(f"Server error: {response.status_code}")
    return response.json()

# Custom retry policy
from provide.foundation.errors import RetryPolicy

policy = RetryPolicy(
    max_attempts=5,
    delay=0.5,
    backoff=1.5,
    max_delay=30.0,
    jitter=True
)

@with_retry(policy=policy)
async def async_operation():
    result = await fetch_data()
    return result
```

### @with_fallback

Provide fallback values:

```python
from provide.foundation.errors import with_fallback

@with_fallback(default=[])
def get_user_list():
    """Return empty list on error."""
    return fetch_users()

@with_fallback(
    default=None,
    exceptions=(ValueError, KeyError),
    log_errors=True
)
def get_config_value(key: str):
    """Return None for missing config."""
    return parse_config()[key]
```

## Error Context

### Adding Context

Enrich errors with diagnostic information:

```python
def process_file(path: str):
    try:
        data = read_file(path)
        result = transform(data)
        return result
    except Exception as e:
        # Create rich error context
        error = FoundationError(
            f"Failed to process file: {path}",
            cause=e
        )
        
        # Add context progressively
        error.add_context("file.path", path)
        error.add_context("file.size", os.path.getsize(path))
        error.add_context("file.modified", os.path.getmtime(path))
        
        # Log with full context
        logger.error("File processing failed", 
                    **error.to_dict())
        raise error
```

### Serialization

Convert errors for logging/API responses:

```python
try:
    dangerous_operation()
except FoundationError as e:
    # Convert to dict for structured logging
    error_dict = e.to_dict()
    # {
    #     "error.type": "FoundationError",
    #     "error.message": "...",
    #     "error.code": "...",
    #     "error.context": {...}
    # }
    
    # API response
    return JSONResponse(
        status_code=500,
        content={
            "error": error_dict,
            "request_id": request.id
        }
    )
```

## Exception Chains

### Preserving Cause Chains

Maintain exception context:

```python
def load_config():
    try:
        with open("config.yml") as f:
            return yaml.load(f)
    except FileNotFoundError as e:
        raise ConfigurationError(
            "Configuration file not found",
            path="config.yml"
        ) from e

def initialize():
    try:
        config = load_config()
        setup_database(config)
    except ConfigurationError as e:
        # Chain preserved
        logger.exception("Initialization failed")
        raise
```

## Pattern Examples

### Service Error Handler

Centralized service error handling:

```python
class ServiceClient:
    """Client with comprehensive error handling."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    @with_retry(
        max_attempts=3,
        exceptions=(NetworkError,)
    )
    @with_error_handling(
        log_errors=True,
        error_mapper=self._map_errors
    )
    async def call(self, endpoint: str, **kwargs):
        """Make API call with error handling."""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = await self._make_request(url, **kwargs)
            return self._handle_response(response)
            
        except aiohttp.ClientError as e:
            raise NetworkError(
                f"Request failed: {e}",
                endpoint=endpoint,
                url=url
            ) from e
    
    def _map_errors(self, exc: Exception) -> Exception:
        """Map client errors to domain errors."""
        if isinstance(exc, aiohttp.ClientResponseError):
            if exc.status == 404:
                return ValidationError("Resource not found")
            elif exc.status == 401:
                return ConfigurationError("Invalid credentials")
        return exc
```

### Batch Processing

Error handling in batch operations:

```python
def process_batch(items: list, continue_on_error=True):
    """Process batch with error tracking."""
    results = []
    errors = []
    
    for i, item in enumerate(items):
        try:
            result = process_item(item)
            results.append(result)
            
        except Exception as e:
            error = FoundationError(
                f"Item {i} failed",
                item_id=item.id,
                index=i,
                cause=e
            )
            errors.append(error)
            
            if not continue_on_error:
                logger.error("Batch processing aborted",
                           completed=len(results),
                           failed=len(errors))
                raise error
    
    # Log summary
    logger.info("Batch completed",
               total=len(items),
               successful=len(results),
               failed=len(errors))
    
    return results, errors
```

### Async Error Aggregation

Handle multiple async errors:

```python
async def parallel_operations(tasks: list):
    """Run tasks in parallel with error aggregation."""
    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )
    
    successes = []
    failures = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            failures.append({
                "task": i,
                "error": str(result),
                "type": type(result).__name__
            })
        else:
            successes.append(result)
    
    if failures:
        error = FoundationError(
            f"{len(failures)} of {len(tasks)} tasks failed",
            failures=failures,
            success_count=len(successes)
        )
        logger.error("Parallel execution partial failure",
                    **error.to_dict())
        
        if len(failures) == len(tasks):
            raise error
    
    return successes, failures
```

## Error Handling Pattern Guidelines

Choosing the right error handling approach depends on your specific needs:

### Use @resilient Decorator When:

- **Need automatic error recovery** with fallback values
- **Want to suppress specific exceptions** gracefully
- **Require error mapping/transformation** from generic to domain-specific errors
- **Adding resilience to entire functions/methods**
- **Need dynamic context injection** for debugging

Example use cases:
- API endpoints that should return default values on failure
- External service calls that need graceful degradation
- Data processing functions with fallback logic

```python
@resilient(
    fallback="default_value",
    suppress=(NetworkError, TimeoutError),
    error_mapper=lambda e: ServiceError(f"External service failed: {e}"),
    context_provider=lambda: {"service": "payment", "user_id": get_current_user_id()}
)
def fetch_user_preferences():
    return external_api.get_preferences()
```

### Use error_boundary() Context Manager When:

- **Handling errors in specific code blocks**
- **Need fine-grained control** over error flow
- **Implementing try-catch-finally patterns**
- **Working with temporary error handling**
- **Want transactional error behavior**

Example use cases:
- Risky operations within larger functions
- Block-level error suppression
- Database transaction blocks

```python
def process_user_data(user_data):
    validated_data = validate_user_data(user_data)

    # Handle specific operation errors
    with error_boundary(
        ValidationError,
        on_error=lambda e: log_validation_failure(e),
        fallback=None,
        reraise=False
    ):
        optional_enrichment = enrich_user_data(validated_data)
        validated_data.update(optional_enrichment or {})

    return save_user_data(validated_data)
```

### Use ErrorHandler Class When:

- **Building plugin systems** with error routing
- **Need type-based error handling policies**
- **Implementing complex error strategies**
- **Creating reusable error handlers**
- **Want centralized error processing**

Example use cases:
- Application-wide error handling
- Plugin architectures
- Complex error routing logic

```python
def create_api_error_handler():
    handler = ErrorHandler(
        policies={
            ValidationError: lambda e: {"error": "validation", "details": e.context},
            AuthenticationError: lambda e: {"error": "auth", "message": "Invalid credentials"},
            NetworkError: lambda e: {"error": "network", "retry_after": 30}
        },
        default_action=lambda e: {"error": "internal", "message": "Service unavailable"},
        reraise_unhandled=False
    )
    return handler

@app.errorhandler(Exception)
def handle_api_error(error):
    result = api_error_handler.handle(error)
    return jsonify(result), get_status_code(error)
```

### Use transactional() Context Manager When:

- **Managing database transactions**
- **Implementing rollback logic**
- **Handling atomic operations**
- **Ensuring cleanup on failure**
- **Need guaranteed state consistency**

Example use cases:
- Database operations
- File system changes
- Multi-step atomic operations

```python
def transfer_funds(from_account, to_account, amount):
    def rollback_transfer():
        # Restore original balances
        from_account.balance += amount
        to_account.balance -= amount
        db.session.rollback()

    def commit_transfer():
        db.session.commit()
        audit_log.record_transfer(from_account, to_account, amount)

    with transactional(
        rollback=rollback_transfer,
        commit=commit_transfer,
        on_error=lambda e: notify_admin_of_transfer_failure(e)
    ):
        from_account.balance -= amount
        to_account.balance += amount
        db.session.flush()  # Validate constraints
```

## Best Practices

### 1. Use Specific Error Types

```python
# Good: Specific error types
if not is_valid:
    raise ValidationError("Invalid format", field="email")

# Bad: Generic errors
if not is_valid:
    raise Exception("Invalid")
```

### 2. Include Context

```python
# Good: Rich context
raise NetworkError(
    "API call failed",
    endpoint=url,
    method="POST",
    status_code=response.status,
    retry_after=response.headers.get("Retry-After")
)

# Bad: No context
raise NetworkError("Failed")
```

### 3. Chain Exceptions

```python
# Good: Preserve cause
try:
    parse_json(data)
except JSONDecodeError as e:
    raise ValidationError("Invalid JSON") from e

# Bad: Lost context
try:
    parse_json(data)
except:
    raise ValidationError("Invalid JSON")
```

### 4. Handle Gracefully

```python
# Good: Graceful degradation
@with_fallback(default=DEFAULT_CONFIG)
def load_user_config():
    return load_config()

# Bad: Crash on error
def load_user_config():
    return load_config()  # May crash
```

## Related Topics

- [Exception Logging](../logging/exceptions.md) - Logging exceptions
- [Error Handling API](../../api/errors/api-index.md) - Error handling API reference
- [Error Decorators](../../api/errors/api-decorators.md) - Error handling decorators