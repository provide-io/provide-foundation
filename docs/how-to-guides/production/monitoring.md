# Monitoring & Observability

Learn how to monitor Foundation applications in production.

## Overview

Foundation provides built-in structured logging and metrics for production observability.

## Structured JSON Logging

Enable JSON logs for log aggregation:

```bash
export PROVIDE_LOG_FORMAT=json
```

Output:
```json
{
  "event": "user_login",
  "level": "info",
  "timestamp": "2025-10-21T17:30:00.000Z",
  "user_id": "user_123",
  "source": "web_app"
}
```

## Log Aggregation

Send logs to aggregation services:

```python
# logs go to stdout, docker/k8s captures them
from provide.foundation import logger

logger.info(
    "request_processed",
    duration_ms=45.2,
    status=200,
    endpoint="/api/users"
)
```

## Metrics Collection

```python
from provide.foundation.metrics import Counter, Histogram

# Track requests
request_counter = Counter("http_requests_total")
request_counter.inc()

# Track latency
latency_histogram = Histogram("http_request_duration_seconds")
with latency_histogram.time():
    process_request()
```

## Health Checks

```python
from provide.foundation import get_hub

def health_check():
    """Return application health status."""
    hub = get_hub()

    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": hub.get_component_status()
    }
```

## Next Steps

- **[Deployment Patterns](deployment.md)** - Deploy to production
- **[Structured Events](../logging/structured-events.md)** - Event logging
