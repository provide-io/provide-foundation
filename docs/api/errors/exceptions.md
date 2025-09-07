# Exception Hierarchy

Structured exceptions with rich context support for comprehensive error information.

## `FoundationError`

Base exception for all Foundation errors with structured context support.

**Constructor**:
```python
FoundationError(
    message: str,
    *,
    code: str | None = None,
    cause: Exception | None = None,
    **context: Any
)
```

**Parameters:**
- `message` (str): Error message
- `code` (str, optional): Error code for categorization
- `cause` (Exception, optional): Underlying exception that caused this error
- `**context`: Additional context fields

**Example:**
```python
from provide.foundation.errors import FoundationError

# Basic usage
raise FoundationError("Operation failed")

# With error code
raise FoundationError("Invalid input", code="VALIDATION_001")

# With context
raise FoundationError(
    "Database connection failed", 
    code="DB_001",
    host="localhost",
    port=5432,
    user_id=123
)

# With underlying cause
try:
    connection.connect()
except ConnectionError as e:
    raise FoundationError("Failed to connect to database", cause=e) from e
```

**Methods:**

#### `add_context(key: str, value: Any) -> FoundationError`

Add additional context to the exception.

**Example:**
```python
error = FoundationError("Processing failed")
error.add_context("batch_id", "batch_123")
error.add_context("records_processed", 500)
```

#### `to_dict() -> dict[str, Any]`

Convert exception to dictionary format for logging/serialization.

**Returns:**
```python
{
    "error.type": "FoundationError",
    "error.message": "Operation failed",
    "error.code": "OP_001",
    "error.user_id": 123
}
```

## Domain-Specific Exceptions

### Validation Errors

```python
from provide.foundation.errors import ValidationError, FieldValidationError

# Generic validation error
raise ValidationError("Invalid request data", field="email", value="invalid-email")

# Field-specific validation
raise FieldValidationError("email", "invalid-email", "Must be valid email address")
```

### Configuration Errors

```python
from provide.foundation.errors import ConfigurationError, MissingConfigError

# Missing configuration
raise MissingConfigError("DATABASE_URL", "Database URL must be configured")

# Invalid configuration
raise ConfigurationError("Invalid log level", key="LOG_LEVEL", value="INVALID")
```

### Resource Errors

```python
from provide.foundation.errors import (
    ResourceError, ResourceNotFoundError, 
    ResourceExhaustedError, ResourceLockError
)

# Resource not found
raise ResourceNotFoundError("user", user_id=123)

# Resource exhausted
raise ResourceExhaustedError("connection_pool", current=100, max=100)

# Resource locked
raise ResourceLockError("config_file", path="/etc/app.conf")
```

### Integration Errors

```python
from provide.foundation.errors import (
    IntegrationError, ExternalServiceError,
    AuthenticationError, AuthorizationError
)

# External service failure
raise ExternalServiceError("payment_gateway", status_code=500, response="Internal Error")

# Authentication failure
raise AuthenticationError("Invalid credentials", user="john_doe")

# Authorization failure  
raise AuthorizationError("Insufficient permissions", user="john_doe", resource="admin_panel")
```

### Platform Errors

```python
from provide.foundation.errors import (
    PlatformError, UnsupportedPlatformError,
    SystemResourceError, PermissionError
)

# Unsupported platform
raise UnsupportedPlatformError("windows", supported=["linux", "darwin"])

# System resource issues
raise SystemResourceError("disk_space", available="100MB", required="1GB")
```

## Error Context

### `ErrorContext`

Structured context information for errors.

**Methods:**
- `add(key: str, value: Any)`: Add context field
- `remove(key: str)`: Remove context field  
- `update(context: dict)`: Update multiple fields
- `to_dict()`: Convert to dictionary
- `clear()`: Clear all context

**Example:**
```python
from provide.foundation.errors import ErrorContext

context = ErrorContext()
context.add("user_id", 123)
context.add("operation", "data_processing")
context.update({"batch_id": "batch_456", "retry_count": 2})

print(context.to_dict())
# {"user_id": 123, "operation": "data_processing", "batch_id": "batch_456", "retry_count": 2}
```

### `capture_error_context()`

Capture current execution context for error reporting.

**Returns:**
- `dict`: Context information including stack trace, timing, system info

**Example:**
```python
from provide.foundation.errors import capture_error_context

try:
    risky_operation()
except Exception as e:
    context = capture_error_context()
    raise FoundationError("Operation failed", **context) from e
```

**Captured Context:**
- Stack trace information
- Execution timing
- System information (memory, CPU)
- Thread/process information
- Environment variables (filtered)

## Exception Hierarchy Tree

```
Exception
└── FoundationError
    ├── ValidationError
    │   └── FieldValidationError
    ├── ConfigurationError
    │   ├── MissingConfigError
    │   └── InvalidConfigError
    ├── ResourceError
    │   ├── ResourceNotFoundError
    │   ├── ResourceExhaustedError
    │   └── ResourceLockError
    ├── IntegrationError
    │   ├── ExternalServiceError
    │   ├── AuthenticationError
    │   └── AuthorizationError
    ├── PlatformError
    │   ├── UnsupportedPlatformError
    │   ├── SystemResourceError
    │   └── PermissionError
    └── ProcessError
        ├── ProcessTimeoutError
        └── ProcessFailedError
```

## Best Practices

### 1. Use Appropriate Exception Types

```python
# Good: Specific exception type
raise ValidationError("Invalid email format", field="email", value=user_email)

# Less ideal: Generic exception
raise FoundationError("Email validation failed")
```

### 2. Add Rich Context

```python
# Good: Rich context for debugging
raise ResourceExhaustedError(
    "Database connection pool exhausted",
    pool_size=100,
    active_connections=100,
    pending_requests=25,
    user_id=user_id,
    endpoint=request.path
)
```

### 3. Chain Exceptions Properly

```python
# Good: Preserve original exception
try:
    external_api.call()
except requests.RequestException as e:
    raise ExternalServiceError("API call failed", service="payment") from e
```

### 4. Use Error Codes for Categorization

```python
# Good: Consistent error codes
raise ValidationError("Invalid input", code="VAL_001", field="email")
raise ValidationError("Required field missing", code="VAL_002", field="password")
```