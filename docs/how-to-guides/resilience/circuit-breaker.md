# Circuit Breakers

Learn how to use circuit breakers to prevent cascading failures and protect your system from overload.

## Overview

Circuit breakers automatically stop calling failing services to prevent resource exhaustion and cascading failures. When a service fails repeatedly, the circuit "opens" and immediately rejects calls without attempting the operation, giving the failing service time to recover.

This pattern is essential for building resilient distributed systems where one failing service shouldn't bring down the entire application.

## Circuit States

The circuit breaker has three states:

```
┌─────────┐
│ CLOSED  │ ◄─── Normal operation
└────┬────┘      All requests pass through
     │           Count failures
     │
     │ Failure threshold exceeded
     ▼
┌─────────┐
│  OPEN   │ ◄─── Circuit tripped
└────┬────┘      Requests fail immediately
     │           No calls to service
     │
     │ Timeout expires
     ▼
┌──────────┐
│HALF-OPEN │ ◄─── Testing recovery
└────┬─────┘     Allow one test request
     │
     ├─── Success: → CLOSED
     └─── Failure: → OPEN
```

### Closed State
- **Normal operation** - All requests pass through
- **Monitoring** - Counts failures
- **Transition** - Opens when failure threshold is exceeded

### Open State
- **Protection mode** - Requests fail immediately with `CircuitBreakerOpen` exception
- **No service calls** - Gives failing service time to recover
- **Transition** - Moves to half-open after timeout period

### Half-Open State
- **Recovery testing** - Allows limited test requests
- **Evaluation** - Monitors if service has recovered
- **Transition** - Returns to closed if tests succeed, back to open if they fail

## Basic Circuit Breaker

```python
from provide.foundation.resilience import circuit_breaker

@circuit_breaker(failure_threshold=5, timeout=60)
def call_external_api():
    """Call an external API with circuit breaker protection."""
    response = requests.get("https://api.example.com/data")
    return response.json()
```

**How it works:**
- After **5 consecutive failures**, the circuit opens
- Circuit stays open for **60 seconds**
- After timeout, allows one test request (half-open)
- If test succeeds, circuit closes; if it fails, stays open for another 60 seconds

## Configuration Options

### Failure Threshold

Number of consecutive failures before opening the circuit:

```python
@circuit_breaker(
    failure_threshold=3,  # Open after 3 failures
    timeout=30,
)
def unreliable_service():
    """Service with low failure tolerance."""
    pass
```

### Timeout Duration

How long the circuit stays open before testing recovery:

```python
@circuit_breaker(
    failure_threshold=5,
    timeout=120,  # Stay open for 2 minutes
)
def slow_recovery_service():
    """Service that needs time to recover."""
    pass
```

### Success Threshold (Half-Open)

Number of successful requests needed to close circuit from half-open:

```python
@circuit_breaker(
    failure_threshold=5,
    timeout=60,
    success_threshold=3,  # Need 3 successes to fully close
)
def cautious_recovery():
    """Require multiple successes before trusting service again."""
    pass
```

### Failure Window

Track failures within a time window instead of consecutively:

```python
@circuit_breaker(
    failure_threshold=10,
    failure_window=60,  # 10 failures within 60 seconds opens circuit
    timeout=120,
)
def rate_based_protection():
    """Open circuit based on failure rate, not consecutive failures."""
    pass
```

## Custom Failure Predicates

Define custom logic to determine what constitutes a "failure":

```python
def is_retriable_error(exception):
    """Only count certain errors as circuit breaker failures."""
    # Don't open circuit for client errors (4xx)
    if isinstance(exception, HTTPError):
        return exception.status_code >= 500  # Only server errors
    # Count network errors
    return isinstance(exception, (ConnectionError, TimeoutError))

@circuit_breaker(
    failure_threshold=5,
    timeout=60,
    failure_predicate=is_retriable_error,
)
def smart_http_call(url):
    """Circuit breaker that ignores client errors."""
    response = requests.get(url)
    if response.status_code >= 400:
        raise HTTPError(response.status_code)
    return response.json()
```

## Monitoring Circuit State

Check the circuit state programmatically:

```python
from provide.foundation.resilience import CircuitBreaker

# Create a reusable circuit breaker
api_circuit = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    name="external_api_circuit",
)

@api_circuit.protect
def call_api():
    """Protected by named circuit breaker."""
    return requests.get("https://api.example.com/data").json()

# Check circuit state
if api_circuit.state == CircuitState.OPEN:
    logger.warning("Circuit is open, API calls are being rejected")
elif api_circuit.state == CircuitState.HALF_OPEN:
    logger.info("Circuit is testing recovery")
else:
    logger.info("Circuit is closed, operating normally")

# Get circuit metrics
logger.info(
    "Circuit metrics",
    failure_count=api_circuit.failure_count,
    success_count=api_circuit.success_count,
    last_failure_time=api_circuit.last_failure_time,
)
```

## Handling Circuit Open Exceptions

Handle circuit breaker open exceptions gracefully:

```python
from provide.foundation.resilience import circuit_breaker, CircuitBreakerOpen
from provide.foundation import logger

@circuit_breaker(failure_threshold=3, timeout=30)
def fetch_user_data(user_id):
    """Fetch user data with circuit protection."""
    return api_client.get(f"/users/{user_id}")

def get_user_with_fallback(user_id):
    """Get user data with fallback when circuit is open."""
    try:
        return fetch_user_data(user_id)
    except CircuitBreakerOpen:
        logger.warning(
            "Circuit breaker open, using cached data",
            user_id=user_id,
        )
        # Return cached data or default
        return get_cached_user_data(user_id)
    except Exception as e:
        logger.error("Failed to fetch user data", error=str(e))
        raise
```

## Common Patterns

### Database Connection Protection

```python
@circuit_breaker(
    failure_threshold=3,
    timeout=60,
    success_threshold=2,
)
def execute_database_query(query, params):
    """Execute query with circuit breaker protection."""
    logger.debug("Executing database query", query=query[:100])

    connection = get_database_connection()
    cursor = connection.execute(query, params)
    result = cursor.fetchall()

    logger.debug("Query completed", row_count=len(result))
    return result
```

### Microservice Call Protection

```python
from provide.foundation.resilience import circuit_breaker, CircuitBreakerOpen

class UserServiceClient:
    """Client for user microservice with circuit protection."""

    def __init__(self):
        self.circuit = CircuitBreaker(
            failure_threshold=5,
            timeout=120,
            name="user_service",
        )

    @circuit.protect
    def get_user(self, user_id):
        """Get user from service."""
        response = requests.get(
            f"{self.service_url}/users/{user_id}",
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    def get_user_safe(self, user_id):
        """Get user with fallback."""
        try:
            return self.get_user(user_id)
        except CircuitBreakerOpen:
            logger.warning("User service circuit open")
            return {"id": user_id, "name": "Unknown"}
```

### External API Protection

```python
@circuit_breaker(
    failure_threshold=10,
    failure_window=60,  # 10 failures in 60 seconds
    timeout=300,  # Stay open for 5 minutes
)
def call_payment_gateway(transaction_data):
    """Call payment gateway with circuit protection."""
    logger.info(
        "Processing payment",
        amount=transaction_data["amount"],
        currency=transaction_data["currency"],
    )

    response = requests.post(
        "https://payment-gateway.example.com/charge",
        json=transaction_data,
        timeout=10,
    )

    if response.status_code >= 500:
        raise ServiceUnavailable("Payment gateway error")

    response.raise_for_status()
    return response.json()
```

## Circuit Breaker with Caching

Combine circuit breaker with caching for maximum resilience:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAPIClient:
    """API client with circuit breaker and caching."""

    def __init__(self):
        self.circuit = CircuitBreaker(
            failure_threshold=5,
            timeout=60,
        )
        self.cache = {}
        self.cache_ttl = timedelta(minutes=5)

    def get_data(self, key):
        """Get data with circuit breaker and cache fallback."""
        # Check cache first
        cached = self._get_from_cache(key)
        if cached:
            return cached

        # Try to fetch from API
        try:
            data = self._fetch_from_api(key)
            self._store_in_cache(key, data)
            return data
        except CircuitBreakerOpen:
            logger.warning(
                "Circuit open, using stale cache",
                key=key,
            )
            # Return stale cache if available
            return self._get_stale_cache(key)

    @circuit.protect
    def _fetch_from_api(self, key):
        """Fetch from API (protected by circuit breaker)."""
        response = requests.get(f"https://api.example.com/data/{key}")
        response.raise_for_status()
        return response.json()

    def _get_from_cache(self, key):
        """Get fresh data from cache."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_ttl:
                return data
        return None

    def _get_stale_cache(self, key):
        """Get stale data from cache as fallback."""
        if key in self.cache:
            data, _ = self.cache[key]
            return data
        return None

    def _store_in_cache(self, key, data):
        """Store data in cache."""
        self.cache[key] = (data, datetime.now())
```

## Best Practices

### ✅ DO: Set Appropriate Failure Thresholds

```python
# ✅ Good: Threshold based on expected error rate
@circuit_breaker(
    failure_threshold=5,  # Reasonable for most APIs
    timeout=60,
)
def api_call():
    pass

# ❌ Bad: Threshold too low (overly sensitive)
@circuit_breaker(
    failure_threshold=1,  # Opens on first failure!
    timeout=60,
)
def too_sensitive():
    pass
```

### ✅ DO: Use Different Circuits for Different Services

```python
# ✅ Good: Separate circuits for different services
payment_circuit = CircuitBreaker(failure_threshold=3, timeout=120)
user_circuit = CircuitBreaker(failure_threshold=5, timeout=60)

@payment_circuit.protect
def process_payment():
    pass

@user_circuit.protect
def get_user():
    pass
```

### ✅ DO: Implement Fallbacks

```python
# ✅ Good: Graceful degradation when circuit opens
def get_recommendations(user_id):
    try:
        return fetch_recommendations(user_id)
    except CircuitBreakerOpen:
        # Return default recommendations
        return get_default_recommendations()
```

### ✅ DO: Monitor Circuit State

```python
# ✅ Good: Log circuit state changes
from provide.foundation.resilience import CircuitState

def on_state_change(circuit, old_state, new_state):
    """Called when circuit state changes."""
    logger.warning(
        "Circuit state changed",
        circuit=circuit.name,
        old_state=old_state.name,
        new_state=new_state.name,
    )

api_circuit = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    on_state_change=on_state_change,
)
```

### ❌ DON'T: Share Circuits Across Unrelated Services

```python
# ❌ Bad: Single circuit for multiple services
@circuit_breaker(failure_threshold=5, timeout=60)
def call_any_service(service_url):
    # One service failure affects all services!
    return requests.get(service_url).json()

# ✅ Good: Separate circuits per service
@user_service_circuit.protect
def call_user_service():
    pass

@payment_service_circuit.protect
def call_payment_service():
    pass
```

### ❌ DON'T: Use Very Short Timeouts

```python
# ❌ Bad: Circuit opens and closes too quickly
@circuit_breaker(
    failure_threshold=3,
    timeout=1,  # Only 1 second - too short!
)
def flaky_call():
    pass

# ✅ Good: Give service time to recover
@circuit_breaker(
    failure_threshold=3,
    timeout=60,  # 1 minute minimum
)
def stable_call():
    pass
```

## Combining Circuit Breaker with Retry

Use both patterns together for maximum resilience:

```python
from provide.foundation.resilience import retry, circuit_breaker

# Circuit breaker on the outside, retry on the inside
@circuit_breaker(failure_threshold=5, timeout=60)
@retry(
    (NetworkError, TimeoutError),
    max_attempts=3,
    base_delay=1.0,
)
def resilient_api_call():
    """
    Protected by both retry and circuit breaker.

    - Retry handles transient failures (3 attempts)
    - Circuit breaker prevents cascading failures
    - If retries repeatedly fail, circuit opens
    """
    return requests.get("https://api.example.com/data").json()
```

**Order matters:**
- **Circuit breaker outside, retry inside** (recommended)
  - Circuit tracks overall failures including retries
  - If service is down, circuit opens and stops retry attempts

- **Retry outside, circuit breaker inside** (not recommended)
  - Retry will attempt even when circuit is open
  - Wastes resources on calls that will fail immediately

## Testing Circuit Breakers

Test circuit behavior in your tests:

```python
import pytest
from provide.foundation.resilience import CircuitBreaker, CircuitBreakerOpen

def test_circuit_opens_after_failures():
    """Test circuit opens after threshold failures."""
    circuit = CircuitBreaker(failure_threshold=3, timeout=60)

    @circuit.protect
    def failing_operation():
        raise RuntimeError("Service unavailable")

    # First 3 calls fail and circuit opens
    for i in range(3):
        with pytest.raises(RuntimeError):
            failing_operation()

    # 4th call rejected by open circuit
    with pytest.raises(CircuitBreakerOpen):
        failing_operation()

def test_circuit_half_open_recovery():
    """Test circuit recovery through half-open state."""
    circuit = CircuitBreaker(
        failure_threshold=2,
        timeout=0.1,  # Short timeout for testing
        success_threshold=2,
    )

    call_count = 0

    @circuit.protect
    def sometimes_failing():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise RuntimeError("Failing")
        return "Success"

    # Open circuit with failures
    for _ in range(2):
        with pytest.raises(RuntimeError):
            sometimes_failing()

    # Wait for timeout
    time.sleep(0.2)

    # Circuit moves to half-open, test succeeds
    assert sometimes_failing() == "Success"
    assert sometimes_failing() == "Success"

    # Circuit should now be closed
    assert circuit.state == CircuitState.CLOSED
```

## Next Steps

### Related Resilience Patterns
- **[Retry Patterns](retry.md)**: Automatically retry failed operations
- **[Production Monitoring](../production/monitoring.md)**: Monitor circuit breaker metrics

### Examples
- See `examples/production/02_error_handling.py` for circuit breaker examples
- See `examples/transport/01_http_client.py` for HTTP circuit protection

### API Reference
- **[API Reference: Resilience](../../reference/provide/foundation/resilience/index.md)**: Complete API documentation

---

**Tip**: Start with conservative thresholds (5-10 failures) and adjust based on your service's behavior. Always implement fallbacks for when circuits open.
