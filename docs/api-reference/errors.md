# Error Handling API

The `provide.foundation.errors` module provides a comprehensive error handling system with rich context, resilience decorators, and structured error logging.

## Overview

The error handling system provides:
- Hierarchical exception classes
- Rich context and metadata attachment
- Resilience decorators (retry, circuit breaker, fallback)
- Integration with the logging system
- Error boundaries for graceful degradation
- Structured error tracking

## Quick Start

```python
from provide.foundation.errors import (
    FoundationError,
    ValidationError,
    retry_on_error,
    with_error_handling
)

# Raise errors with context
raise ValidationError(
    "Invalid email format",
    email="invalid@",
    field="email",
    code="INVALID_EMAIL"
)

# Use resilience decorators
@retry_on_error(max_attempts=3, delay=1.0)
def flaky_network_call():
    """This will retry on failure."""
    response = make_api_call()
    return response

# Handle errors gracefully
@with_error_handling(default_return=None)
def safe_operation():
    """Returns None on error instead of raising."""
    return risky_operation()
```

## Exception Hierarchy

### Base Exception

All exceptions inherit from `FoundationError`:

```python
from provide.foundation.errors import FoundationError

try:
    # Your code
    process_data()
except FoundationError as e:
    # Catches any foundation error
    print(f"Error: {e}")
    print(f"Context: {e.context}")
    print(f"Code: {e.error_code}")
```

### Built-in Exceptions

```python
from provide.foundation.errors import (
    ConfigurationError,
    ValidationError,
    NetworkError,
    TimeoutError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    AlreadyExistsError
)

# Configuration errors
if not config.is_valid():
    raise ConfigurationError(
        "Invalid configuration",
        config_file="app.yaml",
        missing_fields=["database_url", "api_key"]
    )

# Validation errors
def validate_user(data):
    if not data.get("email"):
        raise ValidationError(
            "Email is required",
            field="email",
            value=None,
            code="REQUIRED_FIELD"
        )

# Network errors
try:
    response = http_client.get(url)
except requests.RequestException as e:
    raise NetworkError(
        "Failed to fetch data",
        url=url,
        method="GET",
        original_error=str(e)
    ) from e

# Timeout errors
@timeout(30)
def long_operation():
    # If this takes > 30 seconds
    raise TimeoutError(
        "Operation timed out",
        operation="data_processing",
        timeout_seconds=30
    )

# Authentication errors
if not verify_token(token):
    raise AuthenticationError(
        "Invalid authentication token",
        token_type="JWT",
        expired=is_expired(token)
    )

# Authorization errors
if not user.has_permission("admin"):
    raise AuthorizationError(
        "Insufficient permissions",
        required_role="admin",
        user_role=user.role,
        action="delete_user"
    )

# Not found errors
user = get_user(user_id)
if not user:
    raise NotFoundError(
        "User not found",
        resource_type="user",
        resource_id=user_id
    )

# Already exists errors
if user_exists(email):
    raise AlreadyExistsError(
        "User already exists",
        resource_type="user",
        identifier=email,
        field="email"
    )
```

## Adding Context to Errors

### Rich Context

Attach metadata to exceptions for better debugging:

```python
from provide.foundation.errors import FoundationError

class ProcessingError(FoundationError):
    """Custom processing error."""
    pass

# Raise with context
raise ProcessingError(
    "Failed to process order",
    order_id="ORD-123",
    customer_id="CUST-456",
    step="payment_validation",
    attempt=3,
    timestamp=datetime.now().isoformat()
)

# Access context in handlers
try:
    process_order(order)
except ProcessingError as e:
    print(f"Error: {e}")
    print(f"Order ID: {e.context.get('order_id')}")
    print(f"Step: {e.context.get('step')}")
    
    # Log with full context
    plog.error("Order processing failed", 
        error=str(e),
        **e.context
    )
```

### Error Codes

Use error codes for programmatic handling:

```python
from provide.foundation.errors import FoundationError

class APIError(FoundationError):
    """API-related errors."""
    pass

# Define error codes
ERROR_CODES = {
    "RATE_LIMIT": "You have exceeded the rate limit",
    "INVALID_KEY": "The API key is invalid",
    "EXPIRED_TOKEN": "The authentication token has expired",
    "RESOURCE_LOCKED": "The resource is currently locked"
}

# Raise with error code
raise APIError(
    ERROR_CODES["RATE_LIMIT"],
    error_code="RATE_LIMIT",
    limit=100,
    window="1 hour",
    retry_after=3600
)

# Handle by error code
try:
    api_call()
except APIError as e:
    if e.error_code == "RATE_LIMIT":
        wait_time = e.context.get("retry_after", 60)
        time.sleep(wait_time)
        retry_call()
    elif e.error_code == "INVALID_KEY":
        refresh_api_key()
    else:
        raise
```

## Resilience Decorators

### Retry on Error

Automatically retry operations that fail:

```python
from provide.foundation.errors import retry_on_error
import random

# Basic retry
@retry_on_error(max_attempts=3)
def unreliable_operation():
    if random.random() < 0.5:
        raise NetworkError("Connection failed")
    return "Success"

# Retry with backoff
@retry_on_error(
    max_attempts=5,
    delay=1.0,
    backoff_factor=2.0,  # Exponential backoff
    max_delay=30.0
)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Retry specific exceptions
@retry_on_error(
    max_attempts=3,
    exceptions=(NetworkError, TimeoutError),
    on_retry=lambda attempt, error: plog.warning(
        f"Retry attempt {attempt} after {error}"
    )
)
def api_request():
    return external_api.call()

# Conditional retry
def should_retry(error):
    """Determine if error is retryable."""
    if isinstance(error, HTTPError):
        return error.status_code in [502, 503, 504]
    return isinstance(error, (NetworkError, TimeoutError))

@retry_on_error(
    max_attempts=3,
    retry_condition=should_retry
)
def smart_request():
    return make_request()
```

### Circuit Breaker

Prevent cascading failures:

```python
from provide.foundation.errors import circuit_breaker

# Basic circuit breaker
@circuit_breaker(
    failure_threshold=5,  # Open after 5 failures
    recovery_timeout=60,  # Try again after 60 seconds
    expected_exception=NetworkError
)
def external_service_call():
    """Stops calling after repeated failures."""
    response = external_api.call()
    return response

# Advanced circuit breaker
@circuit_breaker(
    failure_threshold=10,
    recovery_timeout=120,
    success_threshold=3,  # Need 3 successes to close
    on_open=lambda: plog.error("Circuit opened!"),
    on_close=lambda: plog.info("Circuit closed")
)
def database_query(query):
    return db.execute(query)

# Check circuit status
if database_query.is_open():
    plog.warning("Database circuit is open, using cache")
    return get_from_cache()
else:
    return database_query(sql)
```

### Fallback on Error

Provide fallback values or behaviors:

```python
from provide.foundation.errors import fallback_on_error

# Simple fallback value
@fallback_on_error(default_return=[])
def get_user_list():
    """Returns empty list on error."""
    return fetch_users_from_api()

# Fallback function
def get_cached_data():
    """Fallback to cache."""
    return cache.get("last_known_data", [])

@fallback_on_error(fallback_function=get_cached_data)
def get_live_data():
    """Falls back to cache on error."""
    return fetch_live_data()

# Conditional fallback
@fallback_on_error(
    default_return=None,
    exceptions=(NetworkError, TimeoutError),
    on_fallback=lambda e: plog.warning(f"Using fallback due to: {e}")
)
def optional_enrichment(data):
    """Enrichment that can fail gracefully."""
    return enrich_with_external_data(data)
```

### Error Handling Wrapper

Comprehensive error handling:

```python
from provide.foundation.errors import with_error_handling

# Log and suppress errors
@with_error_handling(
    log_errors=True,
    suppress=True,
    default_return=None
)
def optional_operation():
    """Logs errors but doesn't raise them."""
    return risky_operation()

# Transform errors
@with_error_handling(
    transform_error=lambda e: ValueError(f"Invalid input: {e}"),
    exceptions=(ValidationError, TypeError)
)
def validate_input(data):
    """Transforms specific errors to ValueError."""
    return process_input(data)

# Error callback
def handle_error(error):
    """Custom error handler."""
    plog.error("Operation failed", error=str(error))
    send_alert(f"Error: {error}")
    
@with_error_handling(
    on_error=handle_error,
    reraise=True  # Still raise after handling
)
def critical_operation():
    return perform_critical_task()
```

## Error Boundaries

Create error boundaries for sections of code:

```python
from provide.foundation.errors import ErrorBoundary

# Basic error boundary
with ErrorBoundary() as boundary:
    risky_operation_1()
    risky_operation_2()
    risky_operation_3()

if boundary.error:
    plog.error(f"Error in boundary: {boundary.error}")
    # Handle error or use fallback

# Error boundary with handler
def error_handler(error):
    plog.error(f"Caught error: {error}")
    return "default_value"

with ErrorBoundary(on_error=error_handler) as boundary:
    result = complex_calculation()

# Use result or fallback from handler
final_result = boundary.result or "fallback"

# Nested boundaries
with ErrorBoundary() as outer:
    setup_operation()
    
    with ErrorBoundary(suppress=True) as inner:
        # This can fail without affecting outer
        optional_enhancement()
    
    if not inner.error:
        use_enhancement(inner.result)
    
    critical_operation()
```

## Error Aggregation

Collect multiple errors:

```python
from provide.foundation.errors import ErrorCollector

# Collect validation errors
collector = ErrorCollector()

# Validate multiple fields
if not data.get("email"):
    collector.add(ValidationError("Email required", field="email"))

if not data.get("name"):
    collector.add(ValidationError("Name required", field="name"))

if len(data.get("password", "")) < 8:
    collector.add(ValidationError(
        "Password too short",
        field="password",
        min_length=8
    ))

# Check if any errors
if collector.has_errors():
    # Raise all as one
    raise collector.as_exception(
        "Validation failed",
        error_count=len(collector.errors)
    )

# Or handle individually
for error in collector.errors:
    plog.warning(f"Validation error: {error}")
```

## Integration with Logging

Errors integrate seamlessly with the logging system:

```python
from provide.foundation import plog
from provide.foundation.errors import FoundationError

# Automatic error logging
try:
    dangerous_operation()
except FoundationError as e:
    # Log with full context
    plog.error(
        "Operation failed",
        error_type=type(e).__name__,
        error_message=str(e),
        error_code=e.error_code,
        **e.context
    )

# Use exception method
try:
    process_data()
except Exception as e:
    plog.exception("Processing failed")  # Includes traceback

# Structured error logging
@with_error_handling(
    on_error=lambda e: plog.error(
        "Handler failed",
        handler="process_request",
        error=str(e),
        traceback=traceback.format_exc()
    )
)
def process_request(request):
    return handle(request)
```

## Testing Error Handling

### Testing Exceptions

```python
import pytest
from provide.foundation.errors import ValidationError

def test_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError(
            "Invalid input",
            field="email",
            value="invalid"
        )
    
    error = exc_info.value
    assert str(error) == "Invalid input"
    assert error.context["field"] == "email"
    assert error.context["value"] == "invalid"

def test_error_context():
    error = ValidationError(
        "Test error",
        code="TEST_001",
        details={"key": "value"}
    )
    
    assert error.error_code == "TEST_001"
    assert error.context["details"]["key"] == "value"
```

### Testing Resilience

```python
from unittest.mock import Mock, patch

def test_retry_decorator():
    mock_func = Mock(side_effect=[
        NetworkError("Fail 1"),
        NetworkError("Fail 2"),
        "Success"
    ])
    
    @retry_on_error(max_attempts=3)
    def retryable():
        return mock_func()
    
    result = retryable()
    assert result == "Success"
    assert mock_func.call_count == 3

def test_circuit_breaker():
    mock_func = Mock(side_effect=NetworkError("Service down"))
    
    @circuit_breaker(failure_threshold=2, recovery_timeout=1)
    def protected():
        return mock_func()
    
    # First two calls fail and open circuit
    for _ in range(2):
        with pytest.raises(NetworkError):
            protected()
    
    # Circuit is open, should raise immediately
    with pytest.raises(CircuitOpenError):
        protected()
    
    assert mock_func.call_count == 2  # No third call

def test_fallback():
    @fallback_on_error(default_return="fallback")
    def may_fail(should_fail):
        if should_fail:
            raise ValueError("Failed")
        return "success"
    
    assert may_fail(False) == "success"
    assert may_fail(True) == "fallback"
```

## Best Practices

1. **Use specific exception types**:
   ```python
   # Good
   raise ValidationError("Invalid email", field="email")
   
   # Less specific
   raise FoundationError("Invalid email")
   ```

2. **Include relevant context**:
   ```python
   raise ProcessingError(
       "Failed to process order",
       order_id=order.id,
       customer_id=order.customer_id,
       step="payment",
       amount=order.total
   )
   ```

3. **Use error codes for programmatic handling**:
   ```python
   raise APIError(
       "Rate limit exceeded",
       error_code="RATE_LIMIT_EXCEEDED",
       retry_after=60
   )
   ```

4. **Chain exceptions to preserve context**:
   ```python
   try:
       external_call()
   except RequestException as e:
       raise NetworkError("External service failed") from e
   ```

5. **Use resilience decorators appropriately**:
   ```python
   # Retry for transient errors
   @retry_on_error(exceptions=(NetworkError, TimeoutError))
   
   # Circuit breaker for external services
   @circuit_breaker(failure_threshold=5)
   
   # Fallback for optional features
   @fallback_on_error(default_return=None)
   ```

## API Reference

### Exception Classes

- `FoundationError` - Base exception class
- `ConfigurationError` - Configuration issues
- `ValidationError` - Validation failures
- `NetworkError` - Network-related errors
- `TimeoutError` - Operation timeouts
- `AuthenticationError` - Authentication failures
- `AuthorizationError` - Authorization failures
- `NotFoundError` - Resource not found
- `AlreadyExistsError` - Resource already exists

### Decorators

- `@retry_on_error` - Retry on failure
- `@circuit_breaker` - Circuit breaker pattern
- `@fallback_on_error` - Provide fallback values
- `@with_error_handling` - Comprehensive error handling
- `@suppress_and_log` - Suppress and log errors

### Utilities

- `ErrorBoundary` - Context manager for error boundaries
- `ErrorCollector` - Collect multiple errors

## See Also

- [Logger](logger.md) - Logging integration
- [Configuration](config.md) - Configuration error handling
- [Best Practices](../guides/best-practices.md) - Error handling patterns