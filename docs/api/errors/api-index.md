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

## API Reference

The error handling system is organized into several categories:

- **[api-Exception Hierarchy](api-exceptions.md)**: Structured exceptions with rich context
- **[api-Error Handling Decorators](api-decorators.md)**: Retry, fallback, and circuit breaker patterns
- **[api-Handler System](api-handlers.md)**: Configurable error policies and integration support

Each section provides detailed documentation with examples and production-ready patterns.