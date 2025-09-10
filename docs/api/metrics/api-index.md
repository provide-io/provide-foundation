# Metrics Collection API

Metrics collection system with optional OpenTelemetry integration and simple fallback.

## Overview

The Metrics module provides comprehensive metrics collection capabilities that work with or without OpenTelemetry. Features include:

- **Optional OpenTelemetry**: Full OTEL integration when available, simple fallback otherwise
- **Multiple Exporters**: Support for OTLP gRPC, HTTP, and console exporters
- **Common Metric Types**: Counters, gauges, histograms, and timers
- **Foundation Integration**: Automatic logging and telemetry integration
- **Zero Configuration**: Works out-of-the-box with environment-based setup

## Quick Start

### Basic Metrics Collection

```python
from provide.foundation import metrics

# Create meter for your application
meter = metrics.get_meter("my_app")

# Create counters
request_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of HTTP requests"
)

# Record metrics
request_counter.add(1, {"method": "GET", "status": "200"})
```

### With OpenTelemetry (when available)

```python
from provide.foundation.metrics import setup_metrics
from provide.foundation import logger

# Setup with OpenTelemetry if available
setup_metrics(
    service_name="my-service",
    otlp_endpoint="http://localhost:4317"
)

meter = metrics.get_meter("my_service")

# Create different metric types
request_counter = meter.create_counter("requests_total")
response_time = meter.create_histogram("response_time_seconds")
active_connections = meter.create_gauge("active_connections")

# Record metrics with labels
request_counter.add(1, {"endpoint": "/api/users", "method": "GET"})
response_time.record(0.245, {"endpoint": "/api/users"})
active_connections.set(42)
```

## Core Components

### Metric Types

#### Counters
Monotonically increasing values:

```python
# HTTP request counter
http_requests = meter.create_counter(
    "http_requests_total",
    description="Total HTTP requests",
    unit="requests"
)

# Increment counter
http_requests.add(1, {
    "method": "POST",
    "endpoint": "/api/users",
    "status_code": "201"
})
```

#### Histograms  
Distribution of values over time:

```python
# Request duration histogram
request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="HTTP request duration",
    unit="seconds"
)

# Record timing
request_duration.record(0.123, {"endpoint": "/api/users"})
```

#### Gauges
Current value that can go up or down:

```python
# Memory usage gauge
memory_usage = meter.create_gauge(
    "memory_usage_bytes", 
    description="Current memory usage",
    unit="bytes"
)

# Set current value
memory_usage.set(1024 * 1024 * 512)  # 512MB
```

### Simple Metrics (Fallback)

When OpenTelemetry is not available, simple in-memory metrics are used:

```python
from provide.foundation.metrics.simple import (
    SimpleCounter,
    SimpleHistogram,
    SimpleGauge
)

# Create simple metrics
counter = SimpleCounter("operations_total")
histogram = SimpleHistogram("processing_time_seconds")
gauge = SimpleGauge("queue_size")

# Use same API
counter.add(1, {"operation": "data_processing"})
histogram.record(1.234, {"dataset": "users"})
gauge.set(15)

# Get current values
print(f"Total operations: {counter.value}")
print(f"Average processing time: {histogram.mean}")
print(f"Current queue size: {gauge.value}")
```

## Configuration

### Environment Variables

```bash
# OpenTelemetry configuration
export OTEL_SERVICE_NAME="my-service"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"

# Metrics-specific configuration
export PROVIDE_METRICS_ENABLED=true
export PROVIDE_METRICS_EXPORT_INTERVAL=10000  # milliseconds
export PROVIDE_METRICS_EXPORT_TIMEOUT=5000    # milliseconds

# Exporter selection
export PROVIDE_METRICS_EXPORTER="otlp"  # otlp, console, none
```

### Programmatic Setup

```python
from provide.foundation.metrics import setup_metrics, MetricsConfig

# Basic setup
setup_metrics(service_name="my-service")

# Advanced configuration
config = MetricsConfig(
    service_name="my-service",
    export_interval_ms=5000,
    export_timeout_ms=2000,
    otlp_endpoint="https://api.honeycomb.io",
    otlp_headers={"x-honeycomb-team": "your-api-key"}
)

setup_metrics(config=config)
```

## Integration with Foundation

### Automatic HTTP Metrics

HTTP transport automatically collects metrics:

```python
from provide.foundation.transport import get

# This automatically records:
# - http_requests_total (counter)
# - http_request_duration_seconds (histogram)
# - http_request_size_bytes (histogram)
# - http_response_size_bytes (histogram)

response = await get("https://api.example.com/users")
```

### Logger Integration

Metrics integrate with Foundation's structured logging:

```python
from provide.foundation import logger, metrics

meter = metrics.get_meter("app")
error_counter = meter.create_counter("errors_total")

def handle_error(error):
    # Record metric
    error_counter.add(1, {"error_type": error.__class__.__name__})
    
    # Log with metric context
    logger.error("operation_failed", 
                error_type=error.__class__.__name__,
                metric_recorded=True)
```

### Performance Metrics

Built-in performance monitoring:

```python
from provide.foundation.metrics import timed_metric
from provide.foundation.utils import timed_block

# Using decorator
@timed_metric("database_query_duration")
async def fetch_users():
    return await db.query("SELECT * FROM users")

# Using context manager
meter = metrics.get_meter("app")
query_timer = meter.create_histogram("query_duration_seconds")

with timed_block(logger, "complex_operation") as ctx:
    start_time = time.time()
    result = process_data()
    duration = time.time() - start_time
    
    query_timer.record(duration, {"operation": "data_processing"})
    ctx["duration"] = duration
```

## Exporters

### OTLP Exporter (Recommended)

```python
from provide.foundation.metrics import setup_otlp_metrics

# gRPC OTLP
setup_otlp_metrics(
    endpoint="http://localhost:4317",
    protocol="grpc",
    headers={"authorization": "Bearer token"}
)

# HTTP OTLP  
setup_otlp_metrics(
    endpoint="http://localhost:4318/v1/metrics",
    protocol="http"
)
```

### Console Exporter (Development)

```python
from provide.foundation.metrics import setup_console_metrics

# Print metrics to console (useful for debugging)
setup_console_metrics()
```

### Custom Exporters

```python
from provide.foundation.metrics.exporters import BaseMetricExporter

class CustomExporter(BaseMetricExporter):
    def export(self, metrics_data):
        """Export metrics to custom destination."""
        for metric in metrics_data:
            # Send to custom backend
            send_to_custom_backend(metric)

# Register custom exporter
setup_metrics(exporter=CustomExporter())
```

## Best Practices

### Metric Naming

```python
# ✅ Good: Use descriptive names with units
http_request_duration_seconds = meter.create_histogram(
    "http_request_duration_seconds",
    description="Time taken to process HTTP requests",
    unit="seconds"
)

# ❌ Bad: Vague names without units
request_time = meter.create_histogram("request_time")
```

### Label Management

```python
# ✅ Good: Consistent, low-cardinality labels
request_counter.add(1, {
    "method": request.method,
    "status_class": f"{response.status_code // 100}xx",
    "endpoint": normalize_endpoint(request.path)
})

# ❌ Bad: High-cardinality labels
request_counter.add(1, {
    "user_id": request.user_id,  # Too many unique values
    "request_id": request.id,    # Unique per request
    "timestamp": str(time.time())  # Always unique
})
```

### Error Handling

```python
from provide.foundation.metrics import get_meter
from provide.foundation import logger

meter = get_meter("app")
error_counter = meter.create_counter("errors_total")

try:
    result = risky_operation()
except Exception as e:
    # Always record errors in metrics
    error_counter.add(1, {
        "error_type": e.__class__.__name__,
        "operation": "risky_operation"
    })
    
    # Log for debugging
    logger.exception("operation_failed", operation="risky_operation")
    raise
```

## Testing

Test metrics collection using Foundation's testing utilities:

```python
from provide.foundation.testing.metrics import MockMetrics

def test_metrics_collection():
    with MockMetrics() as mock:
        # Your code that records metrics
        counter = meter.create_counter("test_counter")
        counter.add(5, {"label": "value"})
        
        # Verify metrics were recorded
        metrics = mock.get_recorded_metrics()
        assert len(metrics) == 1
        assert metrics[0].value == 5
        assert metrics[0].labels == {"label": "value"}
```

## API Reference

::: provide.foundation.metrics

## Related Documentation

- [OpenTelemetry Guide](https://opentelemetry.io/docs/python/) - OpenTelemetry Python documentation
- [Transport API](../transport/api-index.md) - Automatic HTTP metrics
- [Logger API](../logger/api-index.md) - Logging integration
- [Testing Guide](../../guide/testing.md) - Testing metrics collection