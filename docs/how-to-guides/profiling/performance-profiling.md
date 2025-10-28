# How to Use Performance Profiling

Foundation provides lightweight performance profiling for monitoring logging and telemetry performance.

## Quick Start

```python
from provide.foundation.profiling import register_profiling
from provide.foundation import get_hub

# Register profiling component
hub = get_hub()
register_profiling(hub)

# Get profiler
profiler = hub.get_component("profiler")

# Enable profiling
profiler.enable()

# Your application code here
# ...

# Get metrics
metrics = profiler.get_metrics()
print(f"Processing {metrics.messages_per_second:.0f} msg/sec")
print(f"Average latency: {metrics.avg_latency_ms:.2f}ms")
```

## ProfileMetrics

Access performance metrics:

```python
from provide.foundation.profiling import ProfileMetrics

metrics = profiler.get_metrics()

# Message throughput
print(f"Messages/sec: {metrics.messages_per_second}")
print(f"Total messages: {metrics.total_messages}")

# Latency stats
print(f"Avg latency: {metrics.avg_latency_ms}ms")
print(f"P95 latency: {metrics.p95_latency_ms}ms")
print(f"Max latency: {metrics.max_latency_ms}ms")

# Error rate
print(f"Error rate: {metrics.error_rate}%")
```

## Best Practices

### ✅ DO: Enable in Development

```python
# ✅ Good: Profile in development
import os
from provide.foundation.profiling import register_profiling

if os.getenv("ENVIRONMENT") == "development":
    register_profiling(hub)
    profiler = hub.get_component("profiler")
    profiler.enable()
```

### ❌ DON'T: Leave Enabled in Production

Profiling adds overhead - use only when needed:

```python
# ❌ Bad: Always enabled
profiler.enable()  # Impacts performance!

# ✅ Good: Conditional enabling
if need_profiling:
    profiler.enable()
```

## Next Steps

- **[Logging](../logging/basic-logging.md)**: Structured logging
- **[Metrics](../observability/metrics.md)**: Application metrics

---

**Note**: Profiling is designed for Foundation internals. For application-level profiling, use Python's built-in profilers or external tools.
