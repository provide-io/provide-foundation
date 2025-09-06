# Errors API Reference

Comprehensive error handling system providing structured exceptions, error context management, and resilience patterns.

## Overview

The errors module provides Foundation's complete error handling system, featuring:
- **Structured Exception Hierarchy** - Domain-specific exceptions with rich context
- **Error Context Management** - Detailed diagnostic information for monitoring
- **Resilience Patterns** - Decorators for retry, circuit breaker, and fallback behaviors
- **Handler System** - Configurable error handling with type-based policies
- **Integration Support** - Error formatting for logging, monitoring, and external systems

## Quick Start

```python
from provide.foundation.errors import (
    FoundationError, ValidationError, 
    with_error_handling, retry_on_error,
    error_boundary, capture_error_context
)

# Basic structured exception
raise FoundationError("Operation failed", code="OP_001", user_id=123)

# Error handling decorator
@with_error_handling(fallback=None, suppress=(KeyError,))
def get_config(key: str):
    return config[key]

# Retry with exponential backoff
@retry_on_error(ConnectionError, max_attempts=3, delay=1.0, backoff=2.0)
def fetch_data():
    return api_call()

# Error boundary context
with error_boundary(ValidationError, log_errors=True):
    process_user_input(data)
```

## Exception Hierarchy

### `FoundationError`

Base exception for all Foundation errors with structured context support.

**Constructor**:
```python
FoundationError(
    message: str,
    *,
    code: str | None = None,
    context: dict[str, Any] | None = None,
    cause: Exception | None = None,
    **extra_context: Any
) -> None
```

**Parameters**:
- `message: str` - Human-readable error message
- `code: str | None` - Error code for programmatic handling
- `context: dict[str, Any] | None` - Diagnostic context data
- `cause: Exception | None` - Underlying exception that caused this error
- `**extra_context: Any` - Additional key-value pairs for context

```python
from provide.foundation.errors import FoundationError

# Basic usage
raise FoundationError("Database connection failed")

# With error code
raise FoundationError("Invalid input", code="VALIDATION_001")

# With context
raise FoundationError(
    "User authentication failed", 
    code="AUTH_001",
    user_id="usr_123",
    method="oauth",
    attempt_count=3
)

# With underlying cause
try:
    db.connect()
except ConnectionError as e:
    raise FoundationError(
        "Database unavailable", 
        code="DB_001", 
        cause=e,
        host="localhost",
        port=5432
    )
```

**Methods**:

#### `add_context(key: str, value: Any) -> FoundationError`

Add context data to the error.

```python
error = FoundationError("Processing failed")
error.add_context("batch_id", "batch_001")
error.add_context("aws.region", "us-east-1")  # Namespaced key
```

#### `to_dict() -> dict[str, Any]`

Convert exception to dictionary for structured logging.

```python
error = FoundationError("Operation failed", code="OP_001", user_id=123)
error_dict = error.to_dict()
# {
#     "error.type": "FoundationError",
#     "error.message": "Operation failed",
#     "error.code": "OP_001",
#     "error.user_id": 123
# }
```

### Domain-Specific Exceptions

#### Configuration Errors

```python
from provide.foundation.errors import (
    ConfigurationError,      # General configuration issues
    ConfigValidationError,   # Configuration validation failures
    ValidationError          # Input validation errors
)

# Configuration loading
raise ConfigurationError(
    "Missing required config file",
    config_path="/etc/app/config.yaml"
)

# Schema validation
raise ConfigValidationError(
    "Invalid configuration schema",
    field="database.port",
    expected="integer",
    actual="string"
)

# Input validation
raise ValidationError(
    "Email format invalid",
    field="email",
    value="invalid-email",
    pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
)
```

#### Resource Errors

```python
from provide.foundation.errors import (
    ResourceError,         # General resource issues
    NotFoundError,        # Resource not found
    AlreadyExistsError    # Resource already exists
)

# Resource not found
raise NotFoundError(
    "User not found",
    resource_type="user",
    identifier="usr_123"
)

# Resource conflict
raise AlreadyExistsError(
    "Email already registered", 
    resource_type="user",
    email="user@example.com"
)
```

#### Integration Errors

```python
from provide.foundation.errors import (
    IntegrationError,    # External service issues
    NetworkError,        # Network connectivity problems
    TimeoutError         # Operation timeouts
)

# External API failure
raise IntegrationError(
    "Payment processor unavailable",
    service="stripe",
    endpoint="/v1/charges",
    status_code=503
)

# Network connectivity
raise NetworkError(
    "Connection refused",
    host="api.example.com",
    port=443,
    timeout=30.0
)

# Operation timeout
raise TimeoutError(
    "Database query timeout",
    operation="SELECT",
    timeout=5.0,
    query="SELECT * FROM users WHERE active = true"
)
```

#### Process Errors

```python
from provide.foundation.errors import (
    ProcessError,           # General process execution errors
    ProcessTimeoutError,    # Process timeout
    CommandNotFoundError    # Command not found
)

# Process execution failure
raise ProcessError(
    "Build script failed",
    command=["npm", "run", "build"],
    exit_code=1,
    stderr="Module not found"
)

# Process timeout
raise ProcessTimeoutError(
    "Test execution timeout",
    command=["pytest", "tests/"],
    timeout=300.0
)

# Command not available
raise CommandNotFoundError(
    "Docker not installed",
    command="docker",
    path="/usr/local/bin:/usr/bin:/bin"
)
```

#### Authentication & Authorization

```python
from provide.foundation.errors import (
    AuthenticationError,    # Authentication failures
    AuthorizationError      # Authorization/permission issues
)

# Authentication failure
raise AuthenticationError(
    "Invalid credentials",
    user_id="usr_123",
    method="password",
    ip_address="192.168.1.100"
)

# Permission denied
raise AuthorizationError(
    "Insufficient permissions",
    user_id="usr_123",
    required_role="admin",
    user_role="user",
    resource="admin_panel"
)
```

#### Runtime Errors

```python
from provide.foundation.errors import (
    RuntimeError,      # General runtime issues
    StateError,        # Invalid state transitions
    ConcurrencyError   # Concurrency/threading issues
)

# Invalid state
raise StateError(
    "Cannot start already running process",
    current_state="running",
    requested_action="start",
    process_id="proc_123"
)

# Concurrency issue
raise ConcurrencyError(
    "Resource locked by another thread",
    resource_id="res_456",
    lock_holder="thread_789",
    wait_timeout=10.0
)
```

## Error Context Management

### `ErrorContext`

Rich error context container for diagnostics and monitoring.

```python
from provide.foundation.errors import ErrorContext, ErrorSeverity, ErrorCategory

# Create context
ctx = ErrorContext(
    severity=ErrorSeverity.HIGH,
    category=ErrorCategory.EXTERNAL
)

# Add namespaced metadata
ctx.add_namespace("aws", {
    "region": "us-east-1",
    "account": "123456789012"
})

ctx.add_namespace("http", {
    "method": "POST",
    "status": 500,
    "url": "/api/users"
})

# Add tags for filtering
ctx.add_tags("production", "payment-api", "critical")

# Convert to different formats
log_data = ctx.to_dict()
terraform_diagnostic = ctx.to_terraform_diagnostic()
```

**Attributes**:
- `timestamp: datetime` - When the error occurred
- `severity: ErrorSeverity` - Error severity level (LOW, MEDIUM, HIGH, CRITICAL)
- `category: ErrorCategory` - Error category (USER, SYSTEM, EXTERNAL)
- `metadata: dict[str, dict[str, Any]]` - Namespace-based metadata storage
- `tags: set[str]` - Set of tags for categorization
- `trace_id: str | None` - Optional distributed trace ID
- `span_id: str | None` - Optional distributed span ID

**Methods**:

#### `add_namespace(namespace: str, data: dict[str, Any]) -> ErrorContext`

Add namespaced metadata for specific systems.

```python
ctx.add_namespace("terraform", {
    "provider": "aws", 
    "version": "5.0",
    "resource": "aws_instance.web"
})

ctx.add_namespace("kubernetes", {
    "namespace": "production",
    "pod": "web-server-xyz",
    "node": "worker-node-1"
})
```

#### `to_dict() -> dict[str, Any]`

Convert to flattened dictionary with namespaced keys.

```python
result = ctx.to_dict()
# {
#     "timestamp": "2024-01-15T10:30:45.123456Z",
#     "severity": "high",
#     "category": "external", 
#     "aws.region": "us-east-1",
#     "aws.account": "123456789012",
#     "http.method": "POST",
#     "http.status": 500,
#     "tags": ["critical", "payment-api", "production"]
# }
```

### `capture_error_context()`

Automatically capture error context from exceptions.

```python
from provide.foundation.errors import capture_error_context, ErrorSeverity

try:
    risky_operation()
except Exception as e:
    ctx = capture_error_context(
        e,
        severity=ErrorSeverity.HIGH,
        aws={"region": "us-east-1"},
        http={"status": 500, "method": "POST"}
    )
    
    # Use context for logging
    logger.error("operation_failed", **ctx.to_dict())
```

## Error Handling Decorators

### `@with_error_handling`

Automatic error handling with logging and context.

```python
from provide.foundation.errors import with_error_handling

@with_error_handling(
    fallback=None,
    suppress=(KeyError, AttributeError),
    log_errors=True,
    context_provider=lambda: {"request_id": get_request_id()},
    error_mapper=lambda e: ValidationError(f"Invalid input: {e}")
)
def process_user_data(data):
    return data["required_field"].process()

# Async support
@with_error_handling(fallback={})
async def fetch_user_profile(user_id: str):
    return await api_client.get(f"/users/{user_id}")
```

**Parameters**:
- `fallback: Any` - Value to return when suppressed errors occur
- `suppress: tuple[type[Exception], ...]` - Exception types to suppress
- `log_errors: bool` - Whether to log errors (default: True)
- `context_provider: Callable[[], dict[str, Any]]` - Function providing additional context
- `error_mapper: Callable[[Exception], Exception]` - Transform exceptions before re-raising

### `@retry_on_error`

Retry operations with configurable policies.

```python
from provide.foundation.errors import retry_on_error, RetryPolicy

# Simple retry
@retry_on_error(ConnectionError, TimeoutError, max_attempts=3, delay=1.0)
def fetch_data():
    return api_call()

# Exponential backoff
@retry_on_error(
    NetworkError,
    max_attempts=5,
    delay=2.0,
    backoff=2.0,  # 2x multiplier: 2s, 4s, 8s, 16s
    on_retry=lambda attempt, error: logger.warning(f"Retry {attempt}: {error}")
)
def unreliable_service():
    return external_api()

# Using RetryPolicy
from provide.foundation.errors.types import BackoffStrategy

policy = RetryPolicy(
    max_attempts=3,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,
    max_delay=60.0,
    retryable_errors=(ConnectionError, TimeoutError)
)

@retry_on_error(policy=policy)
def critical_operation():
    return database_operation()
```

### `@suppress_and_log`

Suppress specific exceptions and log them.

```python
from provide.foundation.errors import suppress_and_log

@suppress_and_log(KeyError, AttributeError, fallback={}, log_level="warning")
def get_nested_config(config, *keys):
    result = config
    for key in keys:
        result = result[key]
    return result

# Usage
value = get_nested_config(config, "database", "host", "primary")
# Returns {} if any key is missing, logs warning
```

### `@fallback_on_error`

Call fallback function when errors occur.

```python
from provide.foundation.errors import fallback_on_error

def get_cached_data(*args, **kwargs):
    return cache.get("user_data")

@fallback_on_error(get_cached_data, NetworkError, TimeoutError)
def get_user_data(user_id: str):
    return api_client.get(f"/users/{user_id}")

# If API fails, automatically calls get_cached_data with same arguments
user = get_user_data("usr_123")
```

### `@circuit_breaker`

Circuit breaker pattern to prevent cascading failures.

```python
from provide.foundation.errors import circuit_breaker

@circuit_breaker(
    failure_threshold=5,     # Open after 5 failures
    recovery_timeout=60.0,   # Wait 60s before trying again
    expected_exception=(NetworkError, TimeoutError)
)
def external_service_call():
    return api.get("/status")

# Circuit states: closed -> open -> half_open -> closed
# When open, immediately raises RuntimeError without calling function
```

## Error Boundaries and Handlers

### `error_boundary()`

Context manager for structured error handling.

```python
from provide.foundation.errors import error_boundary

# Basic usage
with error_boundary(ValueError, KeyError, log_errors=True):
    risky_operation()

# With error handler callback
def handle_validation_error(error):
    logger.warning(f"Validation failed: {error}")
    send_error_notification(error)

with error_boundary(
    ValidationError,
    on_error=handle_validation_error,
    context={"user_id": "usr_123", "operation": "signup"}
):
    validate_user_input(data)

# Suppress errors and return fallback
with error_boundary(
    ConnectionError, 
    reraise=False, 
    fallback="service_unavailable"
) as result:
    api_response = external_service()
    
if result == "service_unavailable":
    # Handle fallback case
    pass
```

### `transactional()`

Transactional operations with automatic rollback.

```python
from provide.foundation.errors import transactional

def rollback_changes():
    db.rollback()
    cache.clear()
    
def commit_changes():
    db.commit()
    cache.sync()

with transactional(rollback_changes, commit_changes):
    db.execute("INSERT INTO users ...")
    db.execute("UPDATE accounts ...")
    cache.set("user_count", new_count)
    # Commits on success, rolls back on any exception
```

### `ErrorHandler`

Configurable error handler with type-based policies.

```python
from provide.foundation.errors import ErrorHandler

def handle_validation(error):
    return {"status": "invalid", "message": str(error)}

def handle_auth(error):
    return {"status": "unauthorized", "redirect": "/login"}

def handle_network(error):
    # Retry logic
    time.sleep(1)
    return retry_operation()

# Create handler with policies
handler = ErrorHandler(
    policies={
        ValidationError: handle_validation,
        AuthenticationError: handle_auth,
        NetworkError: handle_network,
    },
    default_action=lambda e: {"status": "error", "message": "Unknown error"},
    log_all=True,
    capture_context=True
)

# Use handler
try:
    process_request(data)
except Exception as e:
    response = handler.handle(e)
    return JsonResponse(response)
```

## Error Types and Metadata

### `ErrorCode`

Structured error codes for programmatic handling.

```python
from provide.foundation.errors.types import ErrorCode

# Standard error codes
class AppErrorCodes:
    USER_NOT_FOUND = ErrorCode("USER_001", "User not found")
    INVALID_EMAIL = ErrorCode("USER_002", "Invalid email format") 
    PAYMENT_FAILED = ErrorCode("PAY_001", "Payment processing failed")
    DB_CONNECTION = ErrorCode("DB_001", "Database connection failed")

# Usage
raise ValidationError(
    "Email validation failed",
    code=AppErrorCodes.INVALID_EMAIL.code,
    email=user_email
)
```

### `RetryPolicy`

Configurable retry behavior.

```python
from provide.foundation.errors.types import RetryPolicy, BackoffStrategy

# Exponential backoff policy
policy = RetryPolicy(
    max_attempts=5,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,
    max_delay=60.0,
    jitter=True,  # Add randomness to delays
    retryable_errors=(NetworkError, TimeoutError)
)

# Check if error should be retried
should_retry = policy.should_retry(error, attempt=2)

# Calculate delay for attempt
delay = policy.calculate_delay(attempt=3)  # ~8 seconds with jitter
```

### `ErrorMetadata`

Rich metadata container for errors.

```python
from provide.foundation.errors.types import ErrorMetadata

metadata = ErrorMetadata(
    correlation_id="req_123",
    user_id="usr_456",
    tags=["critical", "payment"],
    environment="production",
    service="payment-api",
    version="1.2.3"
)

# Convert to context
error_context = metadata.to_context()
```

## Integration Examples

### Logging Integration

```python
from provide.foundation.errors import FoundationError, capture_error_context

try:
    process_payment(amount=100.0, user_id="usr_123")
except Exception as e:
    # Capture rich error context
    context = capture_error_context(
        e,
        payment={"amount": 100.0, "currency": "USD"},
        user={"id": "usr_123", "tier": "premium"},
        request={"id": "req_456", "ip": "192.168.1.100"}
    )
    
    # Log with structured context
    logger.error(
        "payment_processing_failed",
        **context.to_dict()
    )
    
    # Re-raise as FoundationError with context
    raise FoundationError(
        "Payment processing failed",
        code="PAY_001",
        cause=e,
        **context.to_dict()
    )
```

### Monitoring Integration

```python
from provide.foundation.errors import ErrorHandler

def send_to_monitoring(error):
    """Send error to monitoring system."""
    if isinstance(error, FoundationError):
        metrics.increment("errors.foundation", tags={
            "error_type": type(error).__name__,
            "error_code": error.code,
            "severity": "high"
        })
        
        # Send to APM
        apm.capture_exception(error, extra=error.context)
    
    return None  # Don't change error handling

# Global error handler
global_handler = ErrorHandler(
    policies={Exception: send_to_monitoring},
    default_action=lambda e: None,
    log_all=False,  # Monitoring handles logging
    reraise_unhandled=True
)

# Apply to critical functions
@global_handler
def critical_business_logic():
    # Any error here will be sent to monitoring
    pass
```

### API Error Responses

```python
from provide.foundation.errors import (
    ValidationError, AuthenticationError, 
    NotFoundError, ErrorHandler
)

def format_api_error(error):
    """Format error for API response."""
    if isinstance(error, ValidationError):
        return {
            "error": "validation_failed",
            "message": error.message,
            "code": error.code,
            "details": error.context
        }, 400
    
    elif isinstance(error, AuthenticationError):
        return {
            "error": "authentication_failed", 
            "message": "Invalid credentials"
        }, 401
        
    elif isinstance(error, NotFoundError):
        return {
            "error": "not_found",
            "message": error.message,
            "resource": error.context.get("resource_type")
        }, 404
    
    else:
        return {
            "error": "internal_error",
            "message": "An unexpected error occurred"
        }, 500

# API error handler
api_handler = ErrorHandler(
    policies={Exception: format_api_error},
    log_all=True,
    capture_context=True
)

# Flask route example
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        user = create_user_account(user_data)
        return {"user": user.to_dict()}, 201
        
    except Exception as e:
        error_response, status_code = api_handler.handle(e)
        return error_response, status_code
```

## Best Practices

### 1. Use Structured Error Context

```python
# ✅ Good - Rich context
raise FoundationError(
    "Database query failed",
    code="DB_001",
    query="SELECT * FROM users",
    duration_ms=5000,
    connection_pool="primary"
)

# ❌ Bad - Generic error
raise Exception("Database error")
```

### 2. Layer Error Handling

```python
# ✅ Good - Layered approach
@retry_on_error(NetworkError, max_attempts=3)
@with_error_handling(context_provider=get_request_context)
def fetch_user_data(user_id: str):
    with error_boundary(ValidationError):
        return api_client.get(f"/users/{user_id}")

# ❌ Bad - No error handling structure
def fetch_user_data(user_id: str):
    return api_client.get(f"/users/{user_id}")
```

### 3. Handle Errors at Appropriate Levels

```python
# ✅ Good - Handle at service boundary
class UserService:
    @with_error_handling(fallback=None, suppress=(NotFoundError,))
    def get_user(self, user_id: str) -> User | None:
        return self.repository.find_by_id(user_id)
    
    def create_user(self, data: dict) -> User:
        # Don't suppress validation errors - let them bubble up
        return self.repository.create(data)
```

### 4. Use Appropriate Error Types

```python
# ✅ Good - Specific error types
def validate_email(email: str):
    if not email:
        raise ValidationError("Email is required", field="email")
    
    if "@" not in email:
        raise ValidationError(
            "Invalid email format", 
            field="email",
            value=email,
            pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
        )

# ❌ Bad - Generic exceptions
def validate_email(email: str):
    if not email or "@" not in email:
        raise ValueError("Bad email")
```

## Thread Safety

All error handling utilities are thread-safe:

```python
import threading
from provide.foundation.errors import ErrorHandler, retry_on_error

# Thread-safe error handler
handler = ErrorHandler(
    policies={NetworkError: lambda e: "retry_later"}
)

@retry_on_error(ConnectionError, max_attempts=3)
def worker_function(worker_id: int):
    # Safe to use from multiple threads
    try:
        result = perform_work(worker_id)
        return result
    except Exception as e:
        return handler.handle(e)

# Safe to run multiple workers
threads = [
    threading.Thread(target=worker_function, args=(i,))
    for i in range(10)
]
for t in threads:
    t.start()
```

## See Also

- [Logger API](../logger/) - Structured logging integration
- [Process API](../process/) - Process execution error handling  
- [Configuration Guide](../../guide/configuration/) - Error handling configuration
- [Monitoring Guide](../../guide/monitoring/) - Error monitoring and alerting