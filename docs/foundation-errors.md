# Foundation Error Handling System

The `provide.foundation` error handling system provides a comprehensive, extensible framework for managing errors throughout your application with rich context, structured logging integration, and support for diagnostic metadata.

## Table of Contents

- [Quick Start](#quick-start)
- [Import Patterns](#import-patterns)
- [Exception Hierarchy](#exception-hierarchy)
- [Error Context](#error-context)
- [Error Handlers](#error-handlers)
- [Decorators](#decorators)
- [Integration with Logging](#integration-with-logging)
- [Terraform/Pyvider Integration](#terraformpyvider-integration)
- [Best Practices](#best-practices)

## Quick Start

```python
from provide.foundation import (
    FoundationError,
    error_boundary,
    with_error_handling,
    retry_on_error,
)

# Basic error with context
raise FoundationError(
    "Operation failed",
    code="OP_001",
    user_id=123,
    request_id="req_abc"
)

# Error boundary for safe execution
with error_boundary(ValueError, reraise=False):
    risky_operation()

# Decorator for automatic error handling
@with_error_handling(fallback=None, suppress=(KeyError,))
def get_value(data, key):
    return data[key]

# Retry on specific errors
@retry_on_error(NetworkError, max_attempts=3)
def api_call():
    return fetch_data()
```

## Import Patterns

The error system follows a clean import pattern to avoid namespace pollution:

### Essential Imports (Top Level)

Only the most commonly used components are available at the top level:

```python
from provide.foundation import (
    FoundationError,        # Base exception class
    error_boundary,         # Context manager for error handling
    with_error_handling,    # Decorator for error handling
    retry_on_error,        # Decorator for retry logic
)
```

### Specific Error Types

Import specific error types from the `errors` module when needed:

```python
from provide.foundation.errors import (
    ValidationError,
    ConfigurationError,
    NetworkError,
    TimeoutError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    AlreadyExistsError,
    StateError,
    ConcurrencyError,
)
```

### Advanced Features

Import advanced features when needed:

```python
# Error context management
from provide.foundation.errors.context import (
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
    capture_error_context,
)

# Additional decorators
from provide.foundation.errors.decorators import (
    suppress_and_log,
    fallback_on_error,
    circuit_breaker,
)

# Error handlers
from provide.foundation.errors.handlers import (
    transactional,
    handle_error,
    ErrorHandler,
)

# Types and policies
from provide.foundation.errors.types import (
    ErrorCode,
    ErrorMetadata,
    RetryPolicy,
)
```

## Exception Hierarchy

All exceptions inherit from `FoundationError` and provide consistent interfaces:

```python
class FoundationError(Exception):
    """Base exception for all Foundation errors."""
    
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any  # Additional kwargs become context
    )
```

### Built-in Exception Types

| Exception | Purpose | Default Code |
|-----------|---------|--------------|
| `ConfigurationError` | Configuration issues | `CONFIG_ERROR` |
| `ValidationError` | Data validation failures | `VALIDATION_ERROR` |
| `RuntimeError` | Runtime operational errors | `RUNTIME_ERROR` |
| `IntegrationError` | External service failures | `INTEGRATION_ERROR` |
| `ResourceError` | Resource operation failures | `RESOURCE_ERROR` |
| `NetworkError` | Network-related failures | `NETWORK_ERROR` |
| `TimeoutError` | Operation timeouts | `TIMEOUT_ERROR` |
| `AuthenticationError` | Authentication failures | `AUTH_ERROR` |
| `AuthorizationError` | Authorization failures | `AUTHZ_ERROR` |
| `NotFoundError` | Resource not found | `NOT_FOUND_ERROR` |
| `AlreadyExistsError` | Resource already exists | `ALREADY_EXISTS_ERROR` |
| `StateError` | Invalid state transitions | `STATE_ERROR` |
| `ConcurrencyError` | Concurrency conflicts | `CONCURRENCY_ERROR` |

### Creating Custom Exceptions

Extend `FoundationError` for domain-specific errors:

```python
class DatabaseError(FoundationError):
    """Database-specific errors."""
    
    def __init__(self, message: str, *, query: str = None, **kwargs):
        if query:
            kwargs.setdefault('context', {})['db.query'] = query
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "DATABASE_ERROR"

# Usage
raise DatabaseError(
    "Query failed",
    query="SELECT * FROM users",
    db_host="localhost",
    error_code="DEADLOCK"
)
```

## Error Context

The error system uses a flexible, namespace-based context system:

### Simple Context

```python
# Context via kwargs
raise ValidationError(
    "Invalid email",
    field="email",
    value="not-an-email",
    user_id=123
)

# Add context after creation
error = FoundationError("Operation failed")
error.add_context("request.id", "req_123")
error.add_context("user.id", 456)
```

### Namespaced Context

Use dot notation for organizing context:

```python
error = NetworkError("API call failed")
error.add_context("http.method", "POST")
error.add_context("http.status", 500)
error.add_context("http.url", "https://api.example.com/users")
error.add_context("aws.region", "us-east-1")
error.add_context("aws.request_id", "abc-123")
```

### Rich Error Context

For advanced use cases, use `ErrorContext`:

```python
from provide.foundation.errors.context import (
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
)

ctx = ErrorContext(
    severity=ErrorSeverity.HIGH,
    category=ErrorCategory.EXTERNAL,
    trace_id="trace_123",
    span_id="span_456"
)

ctx.add_namespace("terraform", {
    "provider": "aws",
    "resource": "aws_instance.example",
    "workspace": "production"
})

ctx.add_namespace("aws", {
    "region": "us-east-1",
    "account": "123456789"
})

ctx.add_tags("production", "critical", "database")
```

## Error Handlers

### Error Boundary

Use `error_boundary` for safe execution blocks:

```python
from provide.foundation import error_boundary

# Suppress specific errors
with error_boundary(KeyError, ValueError, reraise=False):
    risky_operation()

# Log and re-raise
with error_boundary(
    Exception,
    log_errors=True,
    context={"operation": "data_processing"}
):
    process_data()

# Custom error handler
def handle_error(e: Exception):
    logger.info(f"Handled: {e}")
    send_alert(e)

with error_boundary(Exception, on_error=handle_error):
    critical_operation()
```

### Transactional Operations

Handle rollback scenarios:

```python
from provide.foundation.errors.handlers import transactional

def rollback():
    db.rollback()
    cache.clear()

def commit():
    db.commit()
    cache.persist()

with transactional(rollback, commit):
    db.execute("INSERT INTO users ...")
    cache.set("user:123", data)
    # Automatically commits on success, rolls back on error
```

### Error Handler Class

Create reusable error handling policies:

```python
from provide.foundation.errors.handlers import ErrorHandler

handler = ErrorHandler(
    policies={
        ValidationError: lambda e: {"error": "Invalid input", "field": e.context.get("field")},
        NetworkError: lambda e: retry_with_backoff(),
        AuthenticationError: lambda e: redirect_to_login(),
    },
    default_action=lambda e: log_and_alert(e),
    log_all=True
)

try:
    operation()
except Exception as e:
    result = handler.handle(e)
```

## Decorators

### Basic Error Handling

```python
@with_error_handling(
    fallback="default_value",
    suppress=(KeyError, AttributeError),
    log_errors=True
)
def get_nested_value(data):
    return data["key"].attribute
```

### Retry Logic

```python
from provide.foundation import retry_on_error
from provide.foundation.errors.types import RetryPolicy

# Simple retry
@retry_on_error(
    NetworkError, TimeoutError,
    max_attempts=3,
    delay=1.0,
    backoff=2.0  # Exponential backoff
)
def api_call():
    return fetch_data()

# Advanced retry with policy
policy = RetryPolicy(
    max_attempts=5,
    backoff="exponential",
    base_delay=1.0,
    max_delay=30.0,
    jitter=True
)

@retry_on_error(policy=policy)
def unreliable_operation():
    return external_service()

# With retry callback
def on_retry(attempt: int, error: Exception):
    logger.warning(f"Retry {attempt}: {error}")
    metrics.increment("retry.count")

@retry_on_error(
    NetworkError,
    max_attempts=3,
    on_retry=on_retry
)
def monitored_call():
    return api.request()
```

### Suppress and Log

```python
from provide.foundation.errors.decorators import suppress_and_log

@suppress_and_log(
    KeyError, AttributeError,
    fallback={},
    log_level="warning"
)
def get_config():
    return parse_config_file()
```

### Fallback Functions

```python
from provide.foundation.errors.decorators import fallback_on_error

def use_cache():
    return cache.get("data")

@fallback_on_error(use_cache, NetworkError)
def fetch_fresh_data():
    return api.get_data()
```

### Circuit Breaker

```python
from provide.foundation.errors.decorators import circuit_breaker

@circuit_breaker(
    failure_threshold=5,
    recovery_timeout=60.0,
    expected_exception=(NetworkError, TimeoutError)
)
def external_service_call():
    return service.request()
```

## Integration with Logging

Errors automatically integrate with the Foundation logging system:

```python
from provide.foundation import logger, FoundationError

try:
    operation()
except FoundationError as e:
    # Automatic structured logging
    logger.error("Operation failed", **e.to_dict())
    # Output includes all context with semantic layers
```

### Automatic Context Extraction

```python
error = ValidationError(
    "Invalid configuration",
    field="timeout",
    value=-1,
    config_source="environment"
)

# Logger receives structured context
logger.error(error.message, **error.to_dict())
# Logs: error.type=ValidationError error.code=VALIDATION_ERROR 
#       validation.field=timeout validation.value=-1 config_source=environment
```

## Terraform/Pyvider Integration

The error system supports Terraform diagnostics through namespaced context:

### Basic Integration

```python
error = IntegrationError(
    "Provider initialization failed",
    service="terraform"
)

# Add Terraform-specific context
error.add_context("terraform.provider", "registry.terraform.io/hashicorp/aws")
error.add_context("terraform.resource_type", "aws_instance")
error.add_context("terraform.resource_address", "module.compute.aws_instance.web[0]")
error.add_context("terraform.workspace", "production")

# Add provider-specific context
error.add_context("aws.region", "us-east-1")
error.add_context("aws.error_code", "UnauthorizedOperation")
error.add_context("aws.request_id", "req-12345")
```

### Custom Terraform Error

```python
class TerraformError(FoundationError):
    """Terraform-specific error."""
    
    def __init__(
        self,
        message: str,
        *,
        resource_address: str = None,
        provider: str = None,
        **kwargs
    ):
        if resource_address:
            kwargs.setdefault('context', {})['terraform.resource_address'] = resource_address
        if provider:
            kwargs.setdefault('context', {})['terraform.provider'] = provider
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "TERRAFORM_ERROR"
    
    def to_diagnostic(self) -> dict:
        """Convert to Terraform diagnostic format."""
        return {
            "severity": "error",
            "summary": self.message,
            "detail": {
                k.replace("terraform.", ""): v
                for k, v in self.context.items()
                if k.startswith("terraform.")
            }
        }
```

### Using ErrorContext for Diagnostics

```python
from provide.foundation.errors.context import ErrorContext, capture_error_context

try:
    terraform_operation()
except Exception as e:
    ctx = capture_error_context(
        e,
        severity=ErrorSeverity.HIGH,
        terraform={
            "provider": "aws",
            "version": "5.0.0",
            "resource": "aws_instance.example"
        },
        aws={
            "region": "us-east-1",
            "account": "123456789"
        }
    )
    
    # Convert to Terraform diagnostic
    diagnostic = ctx.to_terraform_diagnostic()
    send_to_terraform(diagnostic)
```

## Best Practices

### 1. Use Appropriate Exception Types

```python
# Good - specific exception type
raise ValidationError("Invalid email format", field="email")

# Avoid - generic exception
raise FoundationError("Invalid email format")
```

### 2. Provide Rich Context

```python
# Good - rich context
raise NetworkError(
    "API request failed",
    service="user-service",
    endpoint="/api/v1/users",
    status_code=500,
    request_id="req_123",
    retry_count=3
)

# Avoid - minimal context
raise NetworkError("API request failed")
```

### 3. Use Namespace Convention

```python
# Good - namespaced keys
error.add_context("http.method", "POST")
error.add_context("http.status", 500)
error.add_context("aws.region", "us-east-1")

# Avoid - flat keys
error.add_context("method", "POST")
error.add_context("status", 500)
error.add_context("region", "us-east-1")
```

### 4. Chain Exceptions

```python
try:
    parse_config()
except JSONDecodeError as e:
    raise ConfigurationError(
        "Failed to parse configuration file",
        config_file="/etc/app/config.json",
        cause=e  # Preserve original exception
    )
```

### 5. Use Decorators for Cross-Cutting Concerns

```python
# Good - declarative error handling
@retry_on_error(NetworkError, max_attempts=3)
@with_error_handling(fallback=None)
def fetch_user_data(user_id):
    return api.get_user(user_id)

# Avoid - manual error handling everywhere
def fetch_user_data(user_id):
    for attempt in range(3):
        try:
            return api.get_user(user_id)
        except NetworkError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
```

### 6. Log at Appropriate Levels

```python
# Use error_boundary with appropriate log levels
with error_boundary(
    ValidationError,  # User errors
    log_errors=True,  # Log as warnings, not errors
    reraise=False
):
    validate_user_input()
```

### 7. Create Domain-Specific Errors

```python
# Create specific errors for your domain
class PaymentError(FoundationError):
    """Payment processing errors."""
    
    def __init__(self, message: str, *, amount: float = None, currency: str = None, **kwargs):
        if amount is not None:
            kwargs.setdefault('context', {})['payment.amount'] = amount
        if currency:
            kwargs.setdefault('context', {})['payment.currency'] = currency
        super().__init__(message, **kwargs)
    
    def _default_code(self) -> str:
        return "PAYMENT_ERROR"
```

## Migration Guide

If migrating from another error system:

1. **Replace base exceptions** with `FoundationError`
2. **Convert error codes** to the `code` parameter
3. **Move metadata** to the `context` dict with namespaces
4. **Use decorators** instead of manual try/except blocks
5. **Leverage error_boundary** for cleanup operations

Example migration:

```python
# Before
try:
    result = api_call()
except APIError as e:
    logger.error(f"API failed: {e}")
    if e.retryable:
        retry_api_call()
    raise

# After
@retry_on_error(NetworkError, max_attempts=3)
def api_call_wrapper():
    try:
        return api_call()
    except APIError as e:
        raise NetworkError(
            "API call failed",
            service="api",
            status_code=e.status_code,
            cause=e
        )
```

## Performance Considerations

The error system is designed for production use:

- **Lazy imports**: Heavy features imported only when needed
- **Efficient context**: Flat dict structure, no deep nesting
- **Minimal overhead**: Decorators add negligible performance impact
- **Thread-safe**: All operations are thread-safe
- **Async-compatible**: Works with async/await code

## Troubleshooting

### Import Errors

If you get import errors, ensure you're using the correct import pattern:

```python
# Correct
from provide.foundation import FoundationError
from provide.foundation.errors import ValidationError

# Incorrect (unless explicitly exported)
from provide.foundation import ValidationError
```

### Context Not Appearing in Logs

Ensure you're using the `to_dict()` method:

```python
# Correct
logger.error("Error occurred", **error.to_dict())

# Incorrect - context not expanded
logger.error("Error occurred", error=error)
```

### Decorator Not Working

Check decorator parameters:

```python
# Correct - exception types as positional args
@retry_on_error(NetworkError, TimeoutError, max_attempts=3)

# Incorrect - missing exception types
@retry_on_error(max_attempts=3)  # Won't retry anything
```

## API Reference

For detailed API documentation, see the module docstrings:

- `provide.foundation.errors.exceptions` - Exception classes
- `provide.foundation.errors.context` - Error context management
- `provide.foundation.errors.handlers` - Error handling utilities
- `provide.foundation.errors.decorators` - Decorator functions
- `provide.foundation.errors.types` - Type definitions and constants