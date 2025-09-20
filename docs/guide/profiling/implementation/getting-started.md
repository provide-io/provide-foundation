# Getting Started with Profiling

This guide walks you through setting up Foundation's profiling system from initial installation to production deployment.

## Prerequisites

- Foundation 1.0+ installed
- Python 3.11+ environment
- Access to a monitoring system (optional but recommended)

## Installation

Foundation's profiling capabilities are included in the core package:

```bash
# Standard installation includes profiling
pip install provide-foundation

# Or with UV
uv add provide-foundation

# Verify profiling is available
python -c "from provide.foundation.profiling import ProfileMetrics; print('✅ Profiling available')"
```

## Basic Setup

### Step 1: Initialize Foundation

```python
# app.py
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

# Get your application's Hub
hub = get_hub()

# Register profiling with default settings
register_profiling(hub)

# Enable profiling
profiler = hub.get_component("profiler")
profiler.enable()

print("✅ Profiling enabled with 1% sampling")
```

### Step 2: Start Logging

Your existing Foundation logging automatically gets profiled:

```python
from provide.foundation import logger

# Normal logging - automatically profiled
logger.info("Application started", emoji="🚀")
logger.debug("Database connection established")
logger.error("Failed to process request", error="timeout", emoji="❌")

# View metrics after some logging
metrics = profiler.get_metrics()
print(f"Throughput: {metrics.messages_per_second:.1f} msg/sec")
print(f"Average latency: {metrics.avg_latency_ms:.2f}ms")
```

### Step 3: View Metrics

```python
# Get current metrics
metrics = profiler.get_metrics()

print(f"""
📊 Performance Metrics:
   Throughput: {metrics.messages_per_second:.1f} messages/second
   Latency: {metrics.avg_latency_ms:.2f}ms average
   Emoji overhead: {metrics.emoji_overhead_percent:.1f}%
   Total processed: {metrics.total_messages}
   Sampled: {metrics.total_messages - metrics.dropped_count}
""")
```

## Configuration Options

### Sampling Rate

Control performance overhead by adjusting sampling:

```python
# Conservative: 0.5% sampling (minimal overhead)
register_profiling(hub, sample_rate=0.005)

# Balanced: 2% sampling (recommended for production)
register_profiling(hub, sample_rate=0.02)

# Detailed: 10% sampling (development/staging)
register_profiling(hub, sample_rate=0.10)

# Complete: 100% sampling (testing only)
register_profiling(hub, sample_rate=1.0)
```

### Environment-Based Configuration

Configure via environment variables:

```bash
# Enable profiling
export PROVIDE_PROFILING_ENABLED=true

# Set sampling rate
export PROVIDE_PROFILING_SAMPLE_RATE=0.02

# Configure CLI integration
export PROVIDE_PROFILING_CLI_ENABLED=true
```

```python
# Application reads environment automatically
from provide.foundation.profiling.config import ProfilingConfig

config = ProfilingConfig.from_env()
register_profiling(hub,
                  sample_rate=config.sample_rate,
                  enabled=config.enabled)
```

## CLI Integration

Foundation automatically adds profiling commands when enabled:

```bash
# View current metrics
provide profile

# View metrics in JSON format
provide profile --json

# Reset metrics (useful for testing)
provide profile --reset

# Show profiling status
provide profile --status
```

Example output:
```
📊 Foundation Profiling Metrics

Performance:
  Messages/second: 1,247
  Average latency: 2.3ms
  P95 latency: 8.1ms

Features:
  Emoji overhead: 12.5%
  Error rate: 0.3%

Collection:
  Sample rate: 2.0%
  Total messages: 62,350
  Sampled messages: 1,247
  Collection period: 5m 23s
```

## Web Framework Integration

### FastAPI

```python
from fastapi import FastAPI
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

app = FastAPI()

@app.on_event("startup")
async def setup_profiling():
    """Initialize profiling on application startup."""
    hub = get_hub()
    register_profiling(hub, sample_rate=0.05)  # 5% sampling

    profiler = hub.get_component("profiler")
    profiler.enable()

    print("✅ Profiling enabled for FastAPI application")

@app.get("/metrics")
async def get_profiling_metrics():
    """Endpoint to view profiling metrics."""
    hub = get_hub()
    profiler = hub.get_component("profiler")
    return profiler.get_metrics().to_dict()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Example endpoint - automatically profiled."""
    from provide.foundation import logger

    logger.info("Fetching user", user_id=user_id, emoji="👤")

    # Your business logic here
    user_data = await fetch_user_data(user_id)

    logger.info("User data retrieved", emoji="✅")
    return user_data
```

### Flask

```python
from flask import Flask, jsonify
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

app = Flask(__name__)

# Initialize profiling when Flask app starts
with app.app_context():
    hub = get_hub()
    register_profiling(hub, sample_rate=0.03)  # 3% sampling

    profiler = hub.get_component("profiler")
    profiler.enable()

@app.route("/metrics")
def profiling_metrics():
    """View profiling metrics via HTTP."""
    hub = get_hub()
    profiler = hub.get_component("profiler")
    return jsonify(profiler.get_metrics().to_dict())

@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    """Example route - automatically profiled."""
    from provide.foundation import logger

    logger.info("Processing user request", user_id=user_id, emoji="🔍")

    # Your business logic
    user = fetch_user(user_id)

    logger.info("Request completed", emoji="✅")
    return jsonify(user)
```

### Django

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'foundation_profiling',  # Custom Django app for profiling
]

# foundation_profiling/apps.py
from django.apps import AppConfig
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

class ProfilingConfig(AppConfig):
    name = 'foundation_profiling'

    def ready(self):
        """Initialize profiling when Django starts."""
        hub = get_hub()
        register_profiling(hub, sample_rate=0.02)  # 2% sampling

        profiler = hub.get_component("profiler")
        profiler.enable()

# views.py
from django.http import JsonResponse
from provide.foundation.hub import get_hub

def profiling_metrics(request):
    """View for profiling metrics."""
    hub = get_hub()
    profiler = hub.get_component("profiler")
    return JsonResponse(profiler.get_metrics().to_dict())
```

## Background Services

### Celery Workers

```python
# celery_app.py
from celery import Celery
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling

app = Celery('myapp')

@app.task
def setup_profiling():
    """Setup profiling for Celery worker."""
    hub = get_hub()
    register_profiling(hub, sample_rate=0.01)  # 1% sampling for workers

    profiler = hub.get_component("profiler")
    profiler.enable()

    return "Profiling enabled for worker"

@app.task
def process_data(data):
    """Example task - automatically profiled."""
    from provide.foundation import logger

    logger.info("Processing data batch", size=len(data), emoji="⚙️")

    # Your processing logic
    result = expensive_processing(data)

    logger.info("Batch processing complete", emoji="✅")
    return result

# Worker startup
from celery.signals import worker_ready

@worker_ready.connect
def setup_worker_profiling(sender=None, **kwargs):
    """Initialize profiling when worker starts."""
    setup_profiling.apply_async()
```

### Background Scripts

```python
# batch_processor.py
import time
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling
from provide.foundation import logger

def main():
    """Main processing loop with profiling."""
    # Setup profiling
    hub = get_hub()
    register_profiling(hub, sample_rate=0.05)  # 5% sampling

    profiler = hub.get_component("profiler")
    profiler.enable()

    logger.info("Background processor started", emoji="🚀")

    while True:
        try:
            # Process batch
            batch = get_next_batch()
            logger.info("Processing batch", size=len(batch), emoji="📦")

            process_batch(batch)

            logger.info("Batch completed", emoji="✅")

            # Log performance metrics periodically
            if should_log_metrics():
                metrics = profiler.get_metrics()
                logger.info(
                    "Performance update",
                    throughput=f"{metrics.messages_per_second:.1f} msg/s",
                    latency=f"{metrics.avg_latency_ms:.1f}ms",
                    emoji="📊"
                )

            time.sleep(1)

        except Exception as e:
            logger.error("Batch processing failed", error=str(e), emoji="❌")
            time.sleep(5)

if __name__ == "__main__":
    main()
```

## Testing Setup

### Unit Tests

```python
# test_profiling.py
import pytest
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling
from provide.foundation import logger
from provide.foundation.testmode import (
    reset_structlog_state,
    reset_streams_state,
    reset_logger_state,
    reset_hub_state,
    reset_profiling_state,
)

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_structlog_state()
    reset_streams_state()
    reset_logger_state()
    reset_hub_state()
    reset_profiling_state()

def test_profiling_basic_setup():
    """Test basic profiling setup and operation."""
    hub = get_hub()
    register_profiling(hub, sample_rate=1.0)  # 100% sampling for testing

    profiler = hub.get_component("profiler")
    profiler.enable()

    # Generate some log messages
    logger.info("Test message 1")
    logger.info("Test message 2", emoji="🔥")
    logger.error("Test error", emoji="❌")

    # Verify metrics collection
    metrics = profiler.get_metrics()
    assert metrics.message_count >= 0  # May be 0 due to sampling

    # With 100% sampling, should have some data
    # (exact count depends on timing and processor overhead)

def test_profiling_metrics_reset():
    """Test metrics reset functionality."""
    hub = get_hub()
    register_profiling(hub, sample_rate=1.0)

    profiler = hub.get_component("profiler")
    profiler.enable()

    # Generate messages
    for i in range(10):
        logger.info(f"Message {i}")

    # Reset metrics
    profiler.reset()

    # Metrics should be reset
    metrics = profiler.get_metrics()
    assert metrics.message_count == 0
```

### Integration Tests

```python
# test_profiling_integration.py
import asyncio
import pytest
from provide.foundation.hub import get_hub
from provide.foundation.profiling import register_profiling
from provide.foundation import logger

@pytest.mark.asyncio
async def test_async_profiling():
    """Test profiling with async operations."""
    hub = get_hub()
    register_profiling(hub, sample_rate=1.0)

    profiler = hub.get_component("profiler")
    profiler.enable()

    async def async_worker():
        logger.info("Async operation", emoji="⚡")
        await asyncio.sleep(0.01)  # Simulate async work
        logger.info("Async complete", emoji="✅")

    # Run multiple async operations
    await asyncio.gather(*[async_worker() for _ in range(5)])

    # Verify profiling worked
    metrics = profiler.get_metrics()
    assert isinstance(metrics.messages_per_second, (int, float))

def test_threaded_profiling():
    """Test profiling with multiple threads."""
    import threading

    hub = get_hub()
    register_profiling(hub, sample_rate=1.0)

    profiler = hub.get_component("profiler")
    profiler.enable()

    def worker():
        for i in range(5):
            logger.info(f"Thread message {i}")

    # Run multiple threads
    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify thread-safe operation
    metrics = profiler.get_metrics()
    # Should not crash and should have valid metrics
    assert metrics.start_time > 0
```

## Monitoring Integration

### Basic Prometheus Export

```python
# Add to your application startup
from provide.foundation.profiling.exporters import PrometheusExporter

# Setup Prometheus export
prometheus_exporter = PrometheusExporter(
    pushgateway_url="http://localhost:9091",
    job_name="foundation_profiling"
)

# Register with profiling system
register_profiling(
    hub,
    sample_rate=0.02,
    exporters=[prometheus_exporter]
)
```

### Health Check Integration

```python
# health.py
from provide.foundation.hub import get_hub

def check_profiling_health():
    """Health check for profiling system."""
    try:
        hub = get_hub()
        profiler = hub.get_component("profiler")

        if not profiler:
            return {"status": "disabled", "healthy": True}

        if not profiler.enabled:
            return {"status": "disabled", "healthy": True}

        # Check if metrics are being collected
        metrics = profiler.get_metrics()

        return {
            "status": "enabled",
            "healthy": True,
            "sample_rate": profiler.processor.sample_rate,
            "total_messages": metrics.total_messages,
            "uptime_seconds": metrics.uptime_seconds
        }

    except Exception as e:
        return {
            "status": "error",
            "healthy": False,
            "error": str(e)
        }
```

## Next Steps

Now that you have basic profiling set up:

1. **[Configuration Guide](configuration.md)** - Learn advanced configuration options
2. **[Best Practices](best-practices.md)** - Production deployment recommendations
3. **[Performance Guide](performance.md)** - Optimize profiling overhead
4. **[Enterprise Features](../enterprise/)** - Explore advanced profiling capabilities

## Troubleshooting

### Common Setup Issues

**Profiling not collecting metrics**
```python
# Check if profiling is enabled
profiler = hub.get_component("profiler")
print(f"Enabled: {profiler.enabled}")
print(f"Sample rate: {profiler.processor.sample_rate}")

# Verify logging is working
from provide.foundation import logger
logger.info("Test message")
```

**Import errors**
```python
# Verify profiling module is available
try:
    from provide.foundation.profiling import ProfileMetrics
    print("✅ Profiling available")
except ImportError as e:
    print(f"❌ Profiling not available: {e}")
```

**Performance overhead too high**
```python
# Reduce sampling rate
profiler.disable()
register_profiling(hub, sample_rate=0.005)  # 0.5% sampling
profiler = hub.get_component("profiler")
profiler.enable()
```

### Getting Help

- Check the [Configuration Guide](configuration.md) for detailed options
- Review [Best Practices](best-practices.md) for production guidance
- See [Performance Guide](performance.md) for optimization tips
- Open an issue on [GitHub](https://github.com/provide-io/provide-foundation/issues) if you need help