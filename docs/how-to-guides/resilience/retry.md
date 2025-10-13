# How to Automatically Retry Operations

Use the `@retry` decorator to make functions resilient to transient failures.

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
