# How to Use Metrics

Foundation provides a lightweight metrics system for collecting and reporting application metrics. This guide shows you how to use built-in metrics and create custom metrics.

## Quick Start

```python
from provide.foundation.metrics import counter, gauge, histogram
from provide.foundation import logger

# Create metrics
request_counter = counter("http_requests_total", "Total HTTP requests")
active_connections = gauge("active_connections", "Number of active connections")
request_duration = histogram("http_request_duration_seconds", "HTTP request duration")

# Use metrics
request_counter.inc()  # Increment counter
active_connections.set(42)  # Set gauge value
request_duration.observe(0.123)  # Record histogram observation

logger.info("metrics_recorded", requests=request_counter.value)
```

## Available Metric Types

### Counter

Counters are monotonically increasing values (can only go up):

```python
from provide.foundation.metrics import counter

# Create counter
requests = counter("api_requests", "Total API requests")

# Increment by 1
requests.inc()

# Increment by N
requests.inc(5)

# Get current value
print(requests.value)  # 6
```

**Use counters for:**
- Total requests processed
- Total errors encountered
- Total bytes sent/received
- Total cache hits/misses

### Gauge

Gauges are values that can go up and down:

```python
from provide.foundation.metrics import gauge

# Create gauge
memory_usage = gauge("memory_usage_bytes", "Current memory usage")

# Set value
memory_usage.set(1024 * 1024 * 100)  # 100 MB

# Increment
memory_usage.inc(1024)

# Decrement
memory_usage.dec(512)

# Get current value
print(memory_usage.value)
```

**Use gauges for:**
- Current memory usage
- Active connections
- Queue size
- Temperature readings
- Cache size

### Histogram

Histograms track distributions of values:

```python
from provide.foundation.metrics import histogram

# Create histogram
response_time = histogram(
    "http_response_time_seconds",
    "HTTP response time in seconds"
)

# Record observations
response_time.observe(0.123)
response_time.observe(0.456)
response_time.observe(0.089)

# Get statistics
stats = response_time.stats()
print(stats["count"])  # Total observations
print(stats["sum"])    # Sum of all values
print(stats["mean"])   # Average value
```

**Use histograms for:**
- Request/response latencies
- Request sizes
- Response sizes
- Processing durations

## Metrics with Labels

Add labels to metrics for multi-dimensional data:

```python
from provide.foundation.metrics import counter

# Create labeled counter
http_requests = counter(
    "http_requests_total",
    "Total HTTP requests",
    labels=["method", "status"]
)

# Increment with label values
http_requests.labels(method="GET", status="200").inc()
http_requests.labels(method="POST", status="201").inc()
http_requests.labels(method="GET", status="404").inc()

# Access specific label combination
get_200_requests = http_requests.labels(method="GET", status="200")
print(get_200_requests.value)  # 1
```

## Integration with Logging

Combine metrics with structured logging:

```python
from provide.foundation import logger
from provide.foundation.metrics import counter, histogram
import time

# Metrics
requests_total = counter("requests_total", "Total requests")
request_duration = histogram("request_duration_seconds", "Request duration")

def handle_request(request_id: str):
    """Handle HTTP request with metrics and logging."""
    start_time = time.time()

    # Log request start
    logger.info("request_started", request_id=request_id)

    try:
        # Process request
        result = process(request_id)

        # Record metrics
        requests_total.labels(status="success").inc()
        duration = time.time() - start_time
        request_duration.observe(duration)

        # Log success
        logger.info(
            "request_completed",
            request_id=request_id,
            duration_ms=round(duration * 1000, 2)
        )

        return result

    except Exception as e:
        # Record error metrics
        requests_total.labels(status="error").inc()
        duration = time.time() - start_time
        request_duration.observe(duration)

        # Log error
        logger.error(
            "request_failed",
            request_id=request_id,
            error=str(e),
            duration_ms=round(duration * 1000, 2)
        )
        raise
```

## OpenTelemetry Integration

Foundation integrates with OpenTelemetry for distributed metrics:

```python
from provide.foundation import get_hub, TelemetryConfig
from provide.foundation.metrics import counter

# Enable OpenTelemetry metrics
config = TelemetryConfig(
    service_name="my-service",
    metrics_enabled=True,
    otlp_endpoint="http://localhost:4317"
)

hub = get_hub()
hub.initialize_foundation(config)

# Metrics automatically exported to OpenTelemetry
requests = counter("http_requests_total", "Total requests")
requests.inc()
```

## Best Practices

### ✅ DO: Use Descriptive Names

```python
# ✅ Good: Clear metric names
http_requests_total = counter("http_requests_total", "Total HTTP requests")
memory_usage_bytes = gauge("memory_usage_bytes", "Memory usage in bytes")

# ❌ Bad: Vague names
count = counter("count", "Count")
value = gauge("value", "Value")
```

### ✅ DO: Include Units in Names

```python
# ✅ Good: Units in metric names
response_time_seconds = histogram("response_time_seconds", "Response time")
memory_bytes = gauge("memory_bytes", "Memory usage")

# ❌ Bad: Missing units
response_time = histogram("response_time", "Response time")  # Seconds? Milliseconds?
```

### ✅ DO: Use Labels for Dimensions

```python
# ✅ Good: Use labels for dimensions
requests = counter("requests_total", "Requests", labels=["method", "status"])
requests.labels(method="GET", status="200").inc()

# ❌ Bad: Multiple metrics
get_requests_200 = counter("get_requests_200", "GET 200 requests")
post_requests_201 = counter("post_requests_201", "POST 201 requests")
```

### ❌ DON'T: Use High-Cardinality Labels

```python
# ❌ Bad: User ID creates too many unique label combinations
requests = counter("requests", "Requests", labels=["user_id"])
requests.labels(user_id="user_12345").inc()  # Creates thousands of metrics!

# ✅ Good: Use low-cardinality labels
requests = counter("requests", "Requests", labels=["endpoint", "method"])
requests.labels(endpoint="/api/users", method="GET").inc()
```

## Environment Configuration

Control metrics via environment variables:

```bash
# Enable/disable metrics
export PROVIDE_METRICS_ENABLED=true

# Set OpenTelemetry endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Set service name
export OTEL_SERVICE_NAME=my-service
```

## Next Steps

- **[Monitoring Guide](../production/monitoring.md)**: Production monitoring patterns
- **[Architecture](../../explanation/architecture.md)**: Understanding Foundation's design
- **[Logging](../logging/basic-logging.md)**: Combine metrics with structured logging

---

**Tip**: Start with simple counters and gauges, then add histograms when you need distribution data.
