# 📚 API Reference

## Errors API

The `provide.foundation` error handling system provides a comprehensive, extensible framework for managing errors throughout your application with rich context, structured logging integration, and support for diagnostic metadata.

### `FoundationError` Base Class

All exceptions in the system inherit from `FoundationError`.

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
        **extra_context: Any
    )
```

*   **`message`**: A human-readable error message.
*   **`code`**: An optional, machine-readable error code (e.g., `"AUTH_001"`).
*   **`context`**: A dictionary for attaching arbitrary structured data to the error.
*   **`cause`**: The original exception, for chaining (`raise new_error from old_error`).
*   **`**extra_context`**: Any additional keyword arguments are automatically added to the `context` dictionary.

#### `to_dict()`

Converts the exception to a dictionary suitable for structured logging.

```python
def to_dict(self) -> dict[str, Any]:
```

!!! info "Automatic Namespacing"
    When converting the error's `context` to a dictionary, this method automatically adds an `error.` prefix to any context key that does not already contain a dot (`.`).

    *   `user_id=123` becomes `"error.user_id": 123`
    *   `"http.status_code"=500` remains `"http.status_code": 500`

    This helps to avoid key collisions and keeps error-specific context organized.

### Built-in Exception Hierarchy

| Exception | Purpose | Default Code |
|---|---|---|
| `ConfigurationError` | Configuration issues | `CONFIG_ERROR` |
| `ValidationError` | Data validation failures | `VALIDATION_ERROR` |
| `RuntimeError` | Runtime operational errors | `RUNTIME_ERROR` |
| `IntegrationError` | External service failures | `INTEGRATION_ERROR` |
| `NetworkError` | Network-related failures | `NETWORK_ERROR` |
| `TimeoutError` | Operation timeouts | `TIMEOUT_ERROR` |
| `AuthenticationError` | Authentication failures | `AUTH_ERROR` |
| `AuthorizationError` | Authorization failures | `AUTHZ_ERROR` |
| `NotFoundError` | Resource not found | `NOT_FOUND_ERROR` |
| `AlreadyExistsError` | Resource already exists | `ALREADY_EXISTS_ERROR` |
| `StateError` | Invalid state transitions | `STATE_ERROR` |
| `ConcurrencyError` | Concurrency conflicts | `CONCURRENCY_ERROR` |

### Error Context

Adding rich, structured context to errors is a core feature.

#### Simple Context

You can add context via keyword arguments at creation time or using the `add_context` method.

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
```

#### Namespaced Context

Using dot-notation for context keys is a recommended best practice for organization.

```python
error = NetworkError("API call failed")
error.add_context("http.method", "POST")
error.add_context("http.status", 500)
error.add_context("aws.region", "us-east-1")
```

### Decorators for Error Handling

The library provides several decorators to handle errors in a clean, declarative way.

#### `@retry_on_error`

Automatically retries a function if it fails with specific exceptions.

```python
from provide.foundation.errors import NetworkError, TimeoutError
from provide.foundation.errors.decorators import retry_on_error

@retry_on_error(NetworkError, TimeoutError, max_attempts=3)
def api_call():
    return fetch_data_from_external_service()
```

#### `@with_error_handling`

A general-purpose decorator to suppress exceptions and provide a fallback value.

```python
from provide.foundation.errors.decorators import with_error_handling

@with_error_handling(
    fallback="default_value",
    suppress=(KeyError, AttributeError),
    log_errors=True
)
def get_nested_value(data):
    return data["key"].attribute
```

### Context Manager for Error Handling

For advanced error handling patterns, refer to the `provide.foundation.errors.handlers` module.

---

Next, learn about the component and command management system in the [**Hub API**](./hub.md).