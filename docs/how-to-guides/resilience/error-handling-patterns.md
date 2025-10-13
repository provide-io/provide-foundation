# How to Handle Errors Gracefully

`provide.foundation` provides powerful decorators to make your functions more resilient to failure without cluttering your business logic with `try...except` blocks.

## The `@retry` Decorator

Use the `@retry` decorator to automatically retry a function that fails with a transient error (like a temporary network issue).

```python
import httpx
from provide.foundation.resilience import retry
from provide.foundation.errors import NetworkError

# This function will be retried 3 times if it raises a NetworkError or httpx.RequestError.
# It will wait 1s, then 2s between retries (exponential backoff).
@retry(
    max_attempts=3,
    delay=1.0,
    backoff_multiplier=2.0,
    exceptions=(NetworkError, httpx.RequestError)
)
def fetch_data_from_unreliable_api():
    """Fetches data from an API that might occasionally fail."""
    logger.info("api_call_attempt", emoji="📡")
    response = httpx.get("https://api.example.com/data")

    # Raise an exception for server-side errors to trigger a retry
    if 500 <= response.status_code < 600:
        raise NetworkError(f"Server error: {response.status_code}")

    response.raise_for_status() # Raise for other client errors (4xx)
    return response.json()

try:
    data = fetch_data_from_unreliable_api()
    pout("Successfully fetched data!", color="green")
except (NetworkError, httpx.RequestError) as e:
    logger.error("api_call_failed_permanently", final_error=str(e), emoji="❌")
    perr("Could not fetch data after multiple retries.", color="red")
```

## The `@circuit_breaker` Decorator

The circuit breaker pattern prevents an application from repeatedly trying to execute an operation that is likely to fail. After a configured number of failures, the circuit breaker "trips" and subsequent calls will fail immediately for a period of time, giving the downstream service time to recover.

```python
from provide.foundation.resilience import circuit_breaker

# This function is protected by a circuit breaker.
# If it fails 5 times in a row, the circuit will open for 60 seconds.
# During that time, any calls will immediately fail without executing the function.
@circuit_breaker(failure_threshold=5, recovery_timeout=60.0)
def call_external_service():
    """Calls a critical but potentially unstable external service."""
    logger.info("external_service_call")
    # ... logic to call the service ...
    if service_is_down:
        raise ConnectionError("Service is unavailable")
    return "Success"

for i in range(10):
    try:
        call_external_service()
        pout(f"Call {i+1}: Success")
    except Exception as e:
        perr(f"Call {i+1}: Failed - {e}")
    time.sleep(1)
```

## The `@fallback` Decorator

Use `@fallback` to provide a default or "fallback" value when a function fails, allowing the application to continue with a degraded state instead of crashing.

```python
from provide.foundation.resilience import fallback

# If `get_user_preferences` fails for any reason, it will return a default dictionary.
@fallback(fallback_value={"theme": "dark", "notifications": "enabled"})
def get_user_preferences(user_id: str) -> dict:
    """Fetches user preferences, with a safe default on failure."""
    # This might fail due to network issues or a database error
    preferences = preferences_api.get(user_id)
    return preferences

# The application can continue even if the preferences API is down.
prefs = get_user_preferences("usr_123")
pout(f"User theme is: {prefs['theme']}")
```
