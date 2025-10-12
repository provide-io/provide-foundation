# Error Handling

Comprehensive error handling utilities for robust applications.

## Overview

`provide.foundation`'s error handling system provides structured exceptions, automatic retry logic, error decorators, and integration with the logging system. It ensures consistent error handling across applications with proper context preservation.

## Exception Classes

### FoundationError Base

Base exception class with structured context:

```python
from provide.foundation.errors import FoundationError

# Basic usage
raise FoundationError("Operation failed")

# With context
raise FoundationError(
    "Database connection failed",
    host="db.example.com",
    port=5432,
    attempts=3
)
```

### Built-in Error Types

Specialized error classes:

```python
from provide.foundation.errors import (
    ConfigurationError,
    ValidationError,
    NetworkError,
    TimeoutError,
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
    )

# Network errors
raise NetworkError(
    "Connection timeout",
    endpoint="https://api.example.com",
    timeout=30,
)
```

## Error Decorators

### @resilient

Automatic error handling and logging:

```python
from provide.foundation.errors.decorators import resilient

@resilient(
    fallback=None,
    suppress=(KeyError, ValueError)
)
def process_data(data: dict):
    """Process with automatic error handling."""
    result = data['key']  # KeyError suppressed
    validate(result)      # ValueError suppressed
    return transform(result)
```

## Related Topics

- [Exception Logging](../logging/exceptions.md) - Logging exceptions
- [Error Handling API](../../api/reference/provide/foundation/errors/index.md) - Error handling API reference
- [Error Decorators](../../api/reference/provide/foundation/errors/decorators.md) - Error handling decorators