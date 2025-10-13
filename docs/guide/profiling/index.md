# Performance Profiling

!!! info "Enterprise-Grade Performance Monitoring"
    Foundation's profiling system provides lightweight, production-ready performance monitoring with zero-config defaults and enterprise-grade extensibility.

!!! note "Current Implementation Status"
    Foundation v1.0 includes core profiling infrastructure (ProfileMetrics, ProfilingProcessor, ProfilingComponent). Enterprise features like adaptive sampling, exporters, and decorators are planned for v1.1+.

## Overview

Foundation's profiling system enables real-time performance monitoring of your application's logging and telemetry operations. Built on top of the existing structured logging infrastructure, it provides:

- **Zero-config operation** - Works out of the box with sensible defaults
- **Minimal overhead** - Configurable sampling to maintain performance
- **Thread-safe collection** - Safe for concurrent applications
- **Enterprise integration** - Export to monitoring systems like Prometheus, Datadog, OpenTelemetry
- **Rich metrics** - Throughput, latency, emoji processing overhead, and more

## Quick Start

### Basic Usage

```python
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

# Register profiling with your application's Hub
hub = get_hub()
register_profiling(hub)

# Enable profiling
profiler = hub.get_component("profiler")
profiler.enable()

# Your existing logging works as normal
from provide.foundation import logger
logger.info("Processing user request", user_id=12345, emoji="👤")
logger.error("Database connection failed", emoji="🔌")

# View metrics at any time
metrics = profiler.get_metrics()
print(f"Throughput: {metrics.messages_per_second:.0f} msg/sec")
print(f"Average latency: {metrics.avg_latency_ms:.2f}ms")
print(f"Emoji overhead: {metrics.emoji_overhead_percent:.1f}%")
```

### CLI Integration

Foundation can register profiling CLI commands when profiling is enabled (CLI integration may require additional setup):

```bash
# Show current performance metrics (when CLI is available)
provide profile

# Show metrics in JSON format
provide profile --json

# Reset metrics counters
provide profile --reset
```

If CLI commands are not available, you can access metrics programmatically:

```python
# Direct metrics access
profiler = hub.get_component("profiler")
if profiler:
    metrics = profiler.get_metrics()
    print(f"Throughput: {metrics.messages_per_second:.0f} msg/sec")
```

## Core Concepts

### Sampling-Based Collection

Profiling uses configurable sampling to minimize performance impact:

```python
# Low overhead: 1% sampling (default)
register_profiling(hub, sample_rate=0.01)

# Higher accuracy: 10% sampling
register_profiling(hub, sample_rate=0.10)

# Full monitoring: 100% sampling (development only)
register_profiling(hub, sample_rate=1.0)
```

### Metrics Collected

| Metric | Description | Use Case |
|--------|-------------|----------|
| `messages_per_second` | Logging throughput | Performance monitoring |
| `avg_latency_ms` | Average processing time | Latency analysis |
| `emoji_overhead_percent` | Cost of emoji processing | Optimization insights |
| `total_messages` | Total processed count | Volume tracking |
| `dropped_messages` | Sampling exclusions | Accuracy assessment |

### Thread Safety

All profiling operations are thread-safe and async-compatible:

```python
import asyncio
import threading
from provide.foundation import logger

async def async_worker():
    """Async logging is automatically profiled."""
    logger.info("Async operation completed", emoji="⚡")

def thread_worker():
    """Thread-safe profiling across workers."""
    for i in range(100):
        logger.debug(f"Processing item {i}")

# Safe concurrent usage
await asyncio.gather(*[async_worker() for _ in range(10)])
threads = [threading.Thread(target=thread_worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Integration Patterns

### Web Applications

```python
from fastapi import FastAPI
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

app = FastAPI()

@app.on_event("startup")
async def setup_profiling():
    hub = get_hub()
    register_profiling(hub)

    profiler = hub.get_component("profiler")
    profiler.enable()

@app.get("/metrics")
async def get_metrics():
    hub = get_hub()
    profiler = hub.get_component("profiler")
    return profiler.get_metrics().to_dict()
```

### Background Services

```python
import time
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

class DataProcessor:
    def __init__(self):
        hub = get_hub()
        register_profiling(hub, sample_rate=0.05)  # 5% sampling

        self.profiler = hub.get_component("profiler")
        self.profiler.enable()

    def process_batch(self, items):
        """Process with automatic profiling."""
        from provide.foundation import logger

        start_time = time.time()
        for item in items:
            logger.info("Processing item", item_id=item.id, emoji="⚙️")

        # Log performance summary
        duration = time.time() - start_time
        metrics = self.profiler.get_metrics()

        logger.info(
            "Batch completed",
            duration_seconds=duration,
            throughput_msg_per_sec=metrics.messages_per_second,
            emoji="✅"
        )
```

## Performance Considerations

### Overhead Analysis

Profiling overhead varies by sampling rate:

| Sample Rate | Overhead | Use Case |
|-------------|----------|----------|
| 1% (default) | < 0.1% | Production monitoring |
| 5% | < 0.5% | Development/staging |
| 10% | < 1% | Performance analysis |
| 100% | 2-5% | Development only |

### Best Practices

1. **Production**: Use 1-5% sampling for continuous monitoring
2. **Development**: Use 10-100% sampling for detailed analysis
3. **Load testing**: Disable profiling or use minimal sampling
4. **CI/CD**: Reset metrics between test runs for accurate benchmarks

## Enterprise Features

Foundation's profiling system will include enterprise-grade capabilities:

!!! warning "Planned Features"
    The following enterprise features are documented but planned for implementation in v1.1+:

- **[Decorator-Based Tracking](enterprise/decorator-tracking.md)** - Automatic function profiling
- **[Adaptive Sampling](enterprise/adaptive-sampling.md)** - Dynamic sampling based on load
- **[Exporter Abstraction](enterprise/exporters.md)** - Integration with monitoring systems

For current implementation capabilities, see the [API Reference](../../api/profiling/api-index.md).

## Implementation Guides

Detailed guides for specific scenarios:

- **[Getting Started](implementation/getting-started.md)** - Step-by-step setup
- **[Configuration](implementation/configuration.md)** - Advanced configuration options
- **[Best Practices](implementation/best-practices.md)** - Production deployment patterns
- **[Performance](implementation/performance.md)** - Optimization strategies

## API Reference

Complete API documentation:

- **[Profiling API Overview](../../api/profiling/api-index.md)** - Complete API reference
- **[ProfileMetrics](../../api/profiling/api-metrics.md)** - Metrics data structure
- **[ProfilingProcessor](../../api/profiling/api-processor.md)** - Structlog processor
- **[ProfilingComponent](../../api/profiling/api-component.md)** - Hub component

## Troubleshooting

### Common Issues

**Profiling not collecting metrics**
```python
# Verify profiler is enabled
profiler = hub.get_component("profiler")
assert profiler.enabled

# Check sampling rate
print(f"Sample rate: {profiler.processor.sample_rate}")
```

**High performance overhead**
```python
# Reduce sampling rate
profiler.disable()
register_profiling(hub, sample_rate=0.01)  # 1% sampling
profiler.enable()
```

**Missing CLI commands**
```python
# Ensure CLI integration is registered
from provide.foundation.profiling.cli import register_profile_command
register_profile_command(hub)
```

### Debug Mode

Enable detailed logging for profiling operations:

```python
import logging
logging.getLogger("provide.foundation.profiling").setLevel(logging.DEBUG)
```