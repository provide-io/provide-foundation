# Circuit Breakers

Learn how to use circuit breakers to prevent cascading failures.

## Overview

Circuit breakers automatically stop calling failing services to prevent resource exhaustion.

## Basic Circuit Breaker

```python
from provide.foundation.resilience import circuit_breaker

@circuit_breaker(failure_threshold=5, timeout=60)
def call_external_api():
    """Call an external API with circuit breaker."""
    response = requests.get("https://api.example.com/data")
    return response.json()
```

## Circuit States

The circuit breaker has three states:

1. **Closed** - Normal operation, requests pass through
2. **Open** - Too many failures, requests fail immediately
3. **Half-Open** - Testing if service recovered

```python
# After 5 failures in a row, circuit opens
# After 60 seconds, circuit goes to half-open
# If next request succeeds, circuit closes
# If next request fails, circuit stays open for another 60s
```

## Next Steps

- **[Retry Patterns](retry.md)** - Retry failed operations
- **[API Reference: Resilience](../../reference/provide/foundation/resilience/index.md)**
