# Resilience Patterns API

Resilience patterns for handling failures and improving application reliability.

## Overview

The Resilience module provides unified implementations of common reliability patterns:

- **Retry** - Automatic retry with configurable backoff strategies
- **Circuit Breaker** - Fail fast when a service is unreliable
- **Fallback** - Graceful degradation when primary operations fail

These patterns help build robust applications that can handle transient failures and cascading issues gracefully.

## Core Components

- **Retry** - RetryPolicy, RetryExecutor, BackoffStrategy
- **Circuit Breaker** - CircuitBreaker, CircuitState  
- **Fallback** - FallbackChain
- **Decorators** - @retry, @circuit_breaker, @fallback

## Quick Start

### Simple Retry

```python
from provide.foundation.resilience import retry

@retry(max_attempts=3, backoff="exponential")
async def unreliable_api_call():
    """Automatically retry on failure with exponential backoff."""
    response = await http_client.get("/api/data")
    response.raise_for_status()
    return response.json()

# Usage
try:
    data = await unreliable_api_call()
except Exception as e:
    logger.error("All retry attempts failed", error=str(e))
```

### Circuit Breaker

```python
from provide.foundation.resilience import circuit_breaker

@circuit_breaker(failure_threshold=5, recovery_timeout=30)
async def external_service_call():
    """Stop calling failing service after threshold is reached."""
    return await external_service.get_data()

# Usage
try:
    data = await external_service_call()
except CircuitBreakerOpenError:
    logger.warning("Circuit breaker is open, using fallback")
    data = get_cached_data()
```

### Fallback Chain

```python
from provide.foundation.resilience import fallback

@fallback([
    lambda: get_from_cache(),
    lambda: get_from_backup_service(),
    lambda: get_default_data()
])
async def get_user_data(user_id: str):
    """Try primary service, fall back to alternatives."""
    return await primary_service.get_user(user_id)

# Usage
data = await get_user_data("user123")  # Always returns something
```

## Combined Patterns

Resilience patterns can be combined for maximum reliability:

```python
from provide.foundation.resilience import retry, circuit_breaker, fallback

@fallback([lambda: get_cached_data()])
@circuit_breaker(failure_threshold=3)
@retry(max_attempts=2, backoff="linear")
async def robust_data_fetch():
    """Ultra-reliable data fetching with multiple resilience layers."""
    return await unreliable_service.get_data()
```

## Configuration Examples

### Retry Policies

```python
from provide.foundation.resilience import RetryPolicy, BackoffStrategy

# Exponential backoff with jitter
policy = RetryPolicy(
    max_attempts=5,
    backoff_strategy=BackoffStrategy.EXPONENTIAL,
    base_delay=1.0,
    max_delay=60.0,
    jitter=True
)

# Linear backoff
policy = RetryPolicy(
    max_attempts=3,
    backoff_strategy=BackoffStrategy.LINEAR,
    base_delay=2.0,
    multiplier=1.5
)
```

### Circuit Breaker Configuration

```python
from provide.foundation.resilience import CircuitBreaker

# Custom circuit breaker
breaker = CircuitBreaker(
    failure_threshold=10,      # Open after 10 failures
    recovery_timeout=60,       # Try recovery after 60 seconds
    expected_exception=HTTPError  # Only count HTTP errors as failures
)
```

## Error Handling

Resilience patterns provide specific exceptions:

```python
from provide.foundation.resilience.exceptions import (
    RetryExhaustedError,
    CircuitBreakerOpenError,
    FallbackExhaustedError
)

try:
    result = await resilient_operation()
except RetryExhaustedError:
    logger.error("All retry attempts failed")
except CircuitBreakerOpenError:
    logger.warning("Circuit breaker is open")
except FallbackExhaustedError:
    logger.error("All fallback options failed")
```

## Integration with Foundation

Resilience patterns integrate seamlessly with Foundation's logging and error handling:

```python
from provide.foundation import logger
from provide.foundation.resilience import retry

@retry(max_attempts=3)
async def logged_operation():
    """Retry with automatic logging."""
    logger.info("operation_started")
    
    try:
        result = await some_operation()
        logger.info("operation_success", result=result)
        return result
    except Exception as e:
        logger.error("operation_failed", error=str(e))
        raise
```

## Performance Considerations

- **Retry**: Adds latency proportional to backoff strategy
- **Circuit Breaker**: Minimal overhead when closed, prevents cascading failures
- **Fallback**: Sequential execution until success, plan fallback order carefully

## Testing

Foundation provides testing utilities for resilience patterns:

```python
from provide.foundation.testing.resilience import (
    MockCircuitBreaker,
    MockRetryExecutor
)

def test_retry_behavior():
    with MockRetryExecutor(max_attempts=3) as mock:
        mock.configure_failures(2)  # Fail first 2 attempts
        
        result = resilient_function()
        
        assert mock.attempt_count == 3
        assert result == "success"
```

## API Reference

::: provide.foundation.resilience

## Related Documentation

- [Error Handling Guide](../../guide/logging/exceptions.md) - Exception handling patterns
- [Testing Guide](../../guide/testing.md) - Testing resilient code
- [Configuration Guide](../../guide/config/index.md) - Configuring resilience patterns