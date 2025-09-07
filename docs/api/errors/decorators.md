# Error Handling Decorators

Retry, fallback, and circuit breaker patterns for resilient error handling.

## `@with_error_handling`

Comprehensive error handling decorator with fallback support.

**Parameters:**
- `fallback`: Fallback value or function to return on error
- `suppress`: Exception types to suppress (return fallback instead)
- `log_errors` (bool): Whether to log caught errors (default: True)
- `logger`: Custom logger to use

**Example:**
```python
from provide.foundation.errors import with_error_handling

@with_error_handling(fallback="default_value", suppress=(KeyError, ValueError))
def get_config(key: str):
    return config[key]

@with_error_handling(fallback=lambda: {"status": "error"})
def api_call():
    return external_service.fetch_data()
```

## `@retry_on_error`

Retry operations with exponential backoff and jitter.

**Parameters:**
- `exceptions`: Exception types to retry on
- `max_attempts` (int): Maximum retry attempts (default: 3)
- `delay` (float): Initial delay between retries (default: 1.0)
- `backoff` (float): Backoff multiplier (default: 2.0)
- `jitter` (bool): Add random jitter to delays (default: True)
- `max_delay` (float): Maximum delay between retries

**Example:**
```python
from provide.foundation.errors import retry_on_error

@retry_on_error(
    (ConnectionError, TimeoutError), 
    max_attempts=5, 
    delay=0.5, 
    backoff=2.0,
    max_delay=30.0
)
def fetch_data():
    return api_client.get("/data")

@retry_on_error(ValueError, max_attempts=3)
def parse_response(data):
    return json.loads(data)
```

## `@suppress_and_log`

Suppress specified exceptions and log them.

**Example:**
```python
from provide.foundation.errors import suppress_and_log

@suppress_and_log(FileNotFoundError, return_value=None)
def read_optional_file(path):
    with open(path) as f:
        return f.read()
```

## `@fallback_on_error`

Provide fallback behavior on any error.

**Example:**
```python
from provide.foundation.errors import fallback_on_error

@fallback_on_error(lambda: "Service unavailable")
def get_status():
    return health_service.check()
```

## `@circuit_breaker`

Circuit breaker pattern for failing fast on repeated errors.

**Parameters:**
- `failure_threshold` (int): Failures before opening circuit
- `recovery_timeout` (float): Seconds before attempting recovery
- `expected_exception`: Exception type that triggers circuit

**Example:**
```python
from provide.foundation.errors import circuit_breaker

@circuit_breaker(failure_threshold=5, recovery_timeout=60)
def external_service_call():
    return service.api_call()
```