# How to Automatically Retry Operations

Use the `@retry` decorator to make functions resilient to transient failures.

## Overview

The retry pattern automatically re-executes operations that fail due to temporary issues like network timeouts, rate limiting, or service unavailability. Foundation's `@retry` decorator provides flexible retry strategies with exponential backoff, jitter, and custom failure predicates.

## Basic Retry

The decorator will re-execute the function if it raises one of the specified exceptions.

```python
# From: examples/production/02_error_handling.py
from provide.foundation.resilience import retry, BackoffStrategy
from provide.foundation.errors import NetworkError

attempt_count = 0

@retry(
    NetworkError,
    max_attempts=3,
    base_delay=0.1,
    backoff=BackoffStrategy.EXPONENTIAL,
)
def unreliable_api_call():
    """Simulate an unreliable API call."""
    global attempt_count
    attempt_count += 1
    logger.info(f"API call attempt {attempt_count}")
    if attempt_count < 3:
        raise NetworkError(f"API temporarily unavailable (attempt {attempt_count})")
    return {"status": "success"}

try:
    result = unreliable_api_call()
    logger.info("API call succeeded", result=result)
except NetworkError as e:
    logger.error("API call failed after all retries", error=str(e))
```

## Backoff Strategies

Foundation provides several backoff strategies for controlling retry timing:

### Exponential Backoff

Delay doubles with each retry attempt:

```python
from provide.foundation.resilience import retry, BackoffStrategy

@retry(
    ConnectionError,
    max_attempts=5,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,  # 1s, 2s, 4s, 8s, 16s
)
def connect_to_database():
    """Connect with exponential backoff."""
    pass
```

### Linear Backoff

Delay increases linearly:

```python
@retry(
    TimeoutError,
    max_attempts=5,
    base_delay=2.0,
    backoff=BackoffStrategy.LINEAR,  # 2s, 4s, 6s, 8s, 10s
)
def fetch_data():
    """Fetch data with linear backoff."""
    pass
```

### Fixed Delay

Constant delay between retries:

```python
@retry(
    ValueError,
    max_attempts=3,
    base_delay=1.0,
    backoff=BackoffStrategy.FIXED,  # 1s, 1s, 1s
)
def validate_input(data):
    """Validate with fixed delay."""
    pass
```

## Jitter Configuration

Add randomness to prevent thundering herd problems:

```python
from provide.foundation.resilience import retry, JitterStrategy

@retry(
    NetworkError,
    max_attempts=5,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,
    jitter=JitterStrategy.FULL,  # Randomize delay: [0, calculated_delay]
)
def distributed_api_call():
    """API call with jitter to prevent simultaneous retries."""
    pass

# Jitter strategies:
# - JitterStrategy.NONE: No randomization
# - JitterStrategy.FULL: Random delay in [0, calculated_delay]
# - JitterStrategy.EQUAL: Random delay in [calculated_delay/2, calculated_delay]
```

## Maximum Delay Limits

Cap the maximum retry delay:

```python
@retry(
    TimeoutError,
    max_attempts=10,
    base_delay=1.0,
    max_delay=30.0,  # Never wait more than 30 seconds
    backoff=BackoffStrategy.EXPONENTIAL,
)
def slow_operation():
    """Operation with capped retry delay."""
    pass
```

## Multiple Exception Types

Retry on any of several exception types:

```python
from provide.foundation.errors import NetworkError, TimeoutError, RateLimitError

@retry(
    (NetworkError, TimeoutError, RateLimitError),  # Tuple of exceptions
    max_attempts=3,
    base_delay=1.0,
)
def multi_failure_operation():
    """Retry on multiple error types."""
    pass
```

## Conditional Retry with Predicates

Use custom logic to determine if a retry should happen:

```python
def should_retry_on_status(exception):
    """Only retry on specific HTTP status codes."""
    if isinstance(exception, HTTPError):
        return exception.status_code in [429, 502, 503, 504]
    return False

@retry(
    HTTPError,
    max_attempts=5,
    base_delay=2.0,
    retry_on=should_retry_on_status,  # Custom predicate
)
def http_request(url):
    """Retry only on specific HTTP errors."""
    pass
```

## Retry with Callbacks

Execute code before/after retry attempts:

```python
from provide.foundation import logger

def before_retry(attempt, exception, delay):
    """Called before each retry."""
    logger.warning(
        "Retrying operation",
        attempt=attempt,
        exception=type(exception).__name__,
        delay_seconds=delay,
    )

def after_retry(attempt, result):
    """Called after successful retry."""
    logger.info("Operation succeeded", attempt=attempt, result=result)

@retry(
    NetworkError,
    max_attempts=3,
    base_delay=1.0,
    on_retry=before_retry,
    on_success=after_retry,
)
def monitored_operation():
    """Operation with retry callbacks for monitoring."""
    pass
```

## Async Function Retries

Retry asynchronous functions:

```python
import asyncio
from provide.foundation.resilience import retry

@retry(
    asyncio.TimeoutError,
    max_attempts=3,
    base_delay=1.0,
)
async def async_api_call():
    """Async operation with automatic retry."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

## Common Patterns

### Database Connection Retry

```python
@retry(
    (ConnectionError, TimeoutError),
    max_attempts=5,
    base_delay=1.0,
    max_delay=30.0,
    backoff=BackoffStrategy.EXPONENTIAL,
    jitter=JitterStrategy.FULL,
)
def connect_to_database(connection_string):
    """Connect to database with retry logic."""
    logger.info("Attempting database connection")
    db = Database(connection_string)
    db.connect()
    logger.info("Database connection established")
    return db
```

### HTTP API Retry

```python
from provide.foundation.errors import NetworkError, TimeoutError

@retry(
    (NetworkError, TimeoutError, RateLimitError),
    max_attempts=3,
    base_delay=2.0,
    backoff=BackoffStrategy.EXPONENTIAL,
)
def call_external_api(endpoint, payload):
    """Call external API with retry on transient failures."""
    logger.info("API request", endpoint=endpoint)

    response = requests.post(endpoint, json=payload, timeout=10)

    if response.status_code == 429:  # Rate limited
        raise RateLimitError("API rate limit exceeded")
    elif response.status_code >= 500:  # Server error
        raise NetworkError(f"Server error: {response.status_code}")

    response.raise_for_status()
    return response.json()
```

### File Upload Retry

```python
@retry(
    (IOError, NetworkError),
    max_attempts=3,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,
)
def upload_file(file_path, destination_url):
    """Upload file with retry on network failures."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(destination_url, files=files)
        response.raise_for_status()

    logger.info("File uploaded successfully", path=file_path)
```

## Best Practices

### ✅ DO: Use Exponential Backoff with Jitter

```python
# ✅ Good: Prevents thundering herd
@retry(
    NetworkError,
    max_attempts=5,
    base_delay=1.0,
    backoff=BackoffStrategy.EXPONENTIAL,
    jitter=JitterStrategy.FULL,
)
def distributed_call():
    pass
```

### ✅ DO: Set Maximum Delay Limits

```python
# ✅ Good: Prevents indefinite waits
@retry(
    TimeoutError,
    max_attempts=10,
    base_delay=1.0,
    max_delay=60.0,  # Cap at 1 minute
)
def bounded_retry():
    pass
```

### ✅ DO: Retry Only Transient Errors

```python
# ✅ Good: Only retry recoverable errors
@retry(
    (NetworkError, TimeoutError, RateLimitError),
    max_attempts=3,
)
def transient_failures_only():
    pass

# ❌ Bad: Don't retry permanent failures
@retry(
    (ValueError, KeyError),  # These won't fix themselves!
    max_attempts=3,
)
def permanent_failures():
    pass
```

### ✅ DO: Log Retry Attempts

```python
# ✅ Good: Track retry behavior
def log_retry(attempt, exception, delay):
    logger.warning(
        "Retry attempt",
        attempt=attempt,
        exception=str(exception),
        next_delay=delay,
    )

@retry(
    NetworkError,
    max_attempts=3,
    on_retry=log_retry,
)
def monitored_operation():
    pass
```

### ❌ DON'T: Use Excessive Max Attempts

```python
# ❌ Bad: Too many retries
@retry(
    NetworkError,
    max_attempts=100,  # Excessive!
)
def over_retry():
    pass

# ✅ Good: Reasonable retry count
@retry(
    NetworkError,
    max_attempts=3,  # Or 5 at most
)
def reasonable_retry():
    pass
```

## Combining Retry with Circuit Breaker

For maximum resilience, combine retry with circuit breakers:

```python
from provide.foundation.resilience import retry, circuit_breaker

@circuit_breaker(failure_threshold=5, timeout=60)
@retry(
    NetworkError,
    max_attempts=3,
    base_delay=1.0,
)
def resilient_service_call():
    """Protected by both retry and circuit breaker."""
    # Circuit breaker prevents calls if service is down
    # Retry handles transient failures within the circuit
    pass
```

## Next Steps

### Related Resilience Patterns
- **[Circuit Breakers](circuit-breaker.md)**: Prevent cascading failures
- **[Production Monitoring](../production/monitoring.md)**: Monitor retry behavior

### Examples
- See `examples/production/02_error_handling.py` for comprehensive retry examples
- See `examples/transport/01_http_client.py` for HTTP retry patterns

### API Reference
- **[API Reference: Resilience](../../reference/provide/foundation/resilience/index.md)**: Complete API documentation

---

**Tip**: Start with simple fixed retries and add exponential backoff with jitter for production use. Always set reasonable `max_attempts` and `max_delay` limits.
