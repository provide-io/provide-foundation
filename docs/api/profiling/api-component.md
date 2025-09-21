# ProfilingComponent API

Detailed API documentation for the ProfilingComponent class, which integrates profiling with Foundation's Hub architecture.

!!! info "Implementation Status"
    ProfilingComponent is currently implemented and available in Foundation's profiling system.

## Class Overview

::: provide.foundation.profiling.component.ProfilingComponent
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true
      show_signature_annotations: true
      separate_signature: true

## Constructor

```python
ProfilingComponent(sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> ProfilingComponent
```

Creates a new ProfilingComponent that can be registered with Foundation's Hub.

**Parameters:**
- `sample_rate` (float): Fraction of messages to sample (0.0 to 1.0)

**Default State:** Component is created in disabled state for safety.

**Example:**
```python
from provide.foundation.profiling.component import ProfilingComponent

# Create with default sampling (1%)
component = ProfilingComponent()

# Create with custom sampling
component = ProfilingComponent(sample_rate=0.05)  # 5%

print(f"Enabled: {component.enabled}")  # False by default
print(f"Sample rate: {component.processor.sample_rate}")
```

## Core Properties

### enabled
- **Type:** `bool`
- **Description:** Whether profiling is currently active
- **Default:** `False` (disabled for safety)
- **Thread Safety:** Safe to read, use methods to modify

### processor
- **Type:** `ProfilingProcessor`
- **Description:** The underlying processor that collects metrics
- **Access:** Read-only reference to internal processor

## Methods

### enable

```python
@resilient(
    fallback=None,
    context_provider=lambda: {"component": "profiler"},
)
def enable(self) -> None
```

Enables profiling metrics collection. Safe to call multiple times.

**Resilience:** Decorated with `@resilient` to prevent failures from breaking application.

**Side Effects:**
- Enables the internal processor
- Logs activation message using Foundation logger
- Sets `enabled` property to `True`

**Example:**
```python
component = ProfilingComponent()
component.enable()

assert component.enabled == True
```

### disable

```python
@resilient(
    fallback=None,
    context_provider=lambda: {"component": "profiler"},
)
def disable(self) -> None
```

Disables profiling metrics collection. Safe to call multiple times.

**Resilience:** Decorated with `@resilient` to prevent failures from breaking application.

**Side Effects:**
- Disables the internal processor
- Logs deactivation message using Foundation logger
- Sets `enabled` property to `False`

**Example:**
```python
component.enable()
# ... profiling active ...
component.disable()

assert component.enabled == False
```

### get_metrics

```python
def get_metrics(self) -> ProfileMetrics
```

Returns current profiling metrics.

**Returns:** The ProfileMetrics instance with collected data.

**Thread Safety:** Safe to call concurrently with metric collection.

**Example:**
```python
component = ProfilingComponent()
component.enable()

# Generate some activity...
from provide.foundation import logger
for i in range(100):
    logger.info(f"Test message {i}", emoji="🔥")

# Get metrics
metrics = component.get_metrics()
print(f"Processed {metrics.message_count} messages")
print(f"Throughput: {metrics.messages_per_second:.1f} msg/sec")
```

### reset

```python
@resilient(
    fallback=None,
    context_provider=lambda: {"component": "profiler", "operation": "reset"},
)
def reset(self) -> None
```

Resets profiling metrics to initial values.

**Resilience:** Decorated with `@resilient` to prevent failures.

**Side Effects:**
- Resets internal processor metrics
- Logs reset operation using Foundation logger

**Use Cases:**
- Testing scenarios requiring clean metrics
- Periodic metric collection windows
- Debugging and analysis

**Example:**
```python
component = ProfilingComponent()
component.enable()

# Collect some metrics...
logger.info("Test message")

# Reset for clean measurement
component.reset()

metrics = component.get_metrics()
assert metrics.message_count == 0
```

## Hub Integration

### Registration Function

```python
@resilient(
    fallback=None,
    context_provider=lambda: {"operation": "register_profiling"},
)
def register_profiling(hub: Hub, sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> None
```

Registers profiling component with Hub and adds CLI command.

**Parameters:**
- `hub` (Hub): The Hub instance to register with
- `sample_rate` (float): Sampling rate for metrics collection

**Side Effects:**
- Creates ProfilingComponent instance
- Registers component with Hub's component registry
- Registers CLI command (if available)

**Example:**
```python
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling

hub = get_hub()
register_profiling(hub, sample_rate=0.02)

# Access registered component
profiler = hub.get_component("profiler")
profiler.enable()
```

### Component Registry Integration

The component is registered directly with the Hub's component registry:

```python
from provide.foundation.hub.components import get_component_registry

# Internal registration process
registry = get_component_registry()
registry.register(
    name="profiler",
    value=profiler_instance,
    dimension="component",
    metadata={
        "type": "profiling",
        "sample_rate": sample_rate
    }
)
```

### Accessing from Hub

```python
from provide.foundation.hub import get_hub

hub = get_hub()

# Get profiler component
profiler = hub.get_component("profiler")

if profiler:
    print(f"Profiler available: {profiler.enabled}")
    metrics = profiler.get_metrics()
    print(f"Current metrics: {metrics.to_dict()}")
else:
    print("Profiler not registered")
```

## CLI Integration

When registering profiling, CLI commands are automatically added:

```python
# CLI commands registered automatically
from provide.foundation.profiling.cli import register_profile_command

try:
    register_profile_command(hub)
    print("✅ CLI commands registered")
except ImportError:
    print("⚠️  CLI components not available")
```

Available CLI commands:
- `provide profile` - Show current metrics
- `provide profile --json` - Show metrics in JSON format
- `provide profile --reset` - Reset metrics counters

## Lifecycle Management

### Application Startup

```python
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling

def setup_profiling():
    """Setup profiling during application startup."""
    hub = get_hub()

    # Register profiling component
    register_profiling(hub, sample_rate=0.01)

    # Enable profiling
    profiler = hub.get_component("profiler")
    if profiler:
        profiler.enable()
        print("✅ Profiling enabled")
    else:
        print("❌ Failed to setup profiling")

# Call during app initialization
setup_profiling()
```

### Application Shutdown

```python
import atexit

def cleanup_profiling():
    """Cleanup profiling during application shutdown."""
    try:
        hub = get_hub()
        profiler = hub.get_component("profiler")

        if profiler and profiler.enabled:
            # Get final metrics
            final_metrics = profiler.get_metrics()
            print(f"Final metrics: {final_metrics.to_dict()}")

            # Disable profiling
            profiler.disable()
            print("✅ Profiling disabled")

    except Exception as e:
        print(f"⚠️  Profiling cleanup error: {e}")

# Register cleanup handler
atexit.register(cleanup_profiling)
```

### Graceful Degradation

```python
def safe_profiling_setup():
    """Setup profiling with graceful degradation."""
    try:
        hub = get_hub()
        register_profiling(hub)

        profiler = hub.get_component("profiler")
        profiler.enable()

        return True

    except Exception as e:
        # Log error but don't fail application startup
        print(f"⚠️  Profiling setup failed: {e}")
        print("🔄 Application continuing without profiling")
        return False

# Use in production
profiling_enabled = safe_profiling_setup()
if profiling_enabled:
    print("📊 Profiling active")
```

## Error Handling and Resilience

### Resilient Decorators

All public methods use the `@resilient` decorator:

```python
from provide.foundation.errors.decorators import resilient

# Example of resilient method
@resilient(
    fallback=None,  # Return None on failure
    context_provider=lambda: {"component": "profiler"}
)
def enable(self) -> None:
    # Method implementation that won't crash application
    pass
```

### Error Recovery

```python
def monitor_profiling_health():
    """Monitor profiling component health."""
    try:
        hub = get_hub()
        profiler = hub.get_component("profiler")

        if not profiler:
            print("⚠️  Profiler component not found")
            return False

        if not profiler.enabled:
            print("⚠️  Profiler disabled")
            return False

        # Test metrics collection
        metrics = profiler.get_metrics()
        if metrics.start_time <= 0:
            print("⚠️  Profiler metrics invalid")
            return False

        return True

    except Exception as e:
        print(f"❌ Profiling health check failed: {e}")
        return False

# Use for monitoring
if not monitor_profiling_health():
    print("🔄 Attempting profiling recovery...")
    # Recovery logic here
```

## Performance Characteristics

### Memory Usage

```python
import sys
from provide.foundation.profiling.component import ProfilingComponent

component = ProfilingComponent()

print(f"Component size: {sys.getsizeof(component)} bytes")
print(f"Processor size: {sys.getsizeof(component.processor)} bytes")
print(f"Metrics size: {sys.getsizeof(component.processor.metrics)} bytes")

# Total memory footprint is typically < 1KB per component
```

### Method Performance

```python
import time

component = ProfilingComponent()

# Benchmark enable/disable operations
start = time.perf_counter()
for _ in range(1000):
    component.enable()
    component.disable()
elapsed = time.perf_counter() - start

print(f"Enable/disable: {elapsed * 1000:.2f}ms for 1000 operations")

# Benchmark metrics access
component.enable()
start = time.perf_counter()
for _ in range(10000):
    metrics = component.get_metrics()
elapsed = time.perf_counter() - start

print(f"get_metrics(): {elapsed * 1000:.2f}ms for 10000 calls")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Setup profiling on FastAPI startup."""
    hub = get_hub()
    register_profiling(hub, sample_rate=0.02)

    profiler = hub.get_component("profiler")
    profiler.enable()

    print("📊 Profiling enabled for FastAPI")

@app.get("/profiling/metrics")
async def get_profiling_metrics():
    """Endpoint to view profiling metrics."""
    hub = get_hub()
    profiler = hub.get_component("profiler")

    if not profiler:
        return {"error": "Profiling not available"}

    return profiler.get_metrics().to_dict()

@app.post("/profiling/reset")
async def reset_profiling_metrics():
    """Endpoint to reset profiling metrics."""
    hub = get_hub()
    profiler = hub.get_component("profiler")

    if not profiler:
        return {"error": "Profiling not available"}

    profiler.reset()
    return {"message": "Metrics reset successfully"}
```

### Django Integration

```python
# Django app configuration
from django.apps import AppConfig
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling

class ProfilingConfig(AppConfig):
    name = 'profiling'

    def ready(self):
        """Setup profiling when Django app is ready."""
        hub = get_hub()
        register_profiling(hub, sample_rate=0.01)

        profiler = hub.get_component("profiler")
        profiler.enable()

# Django views
from django.http import JsonResponse

def profiling_metrics_view(request):
    """Django view for profiling metrics."""
    hub = get_hub()
    profiler = hub.get_component("profiler")

    if not profiler:
        return JsonResponse({"error": "Profiling not available"})

    return JsonResponse(profiler.get_metrics().to_dict())
```

### Background Worker Integration

```python
from celery import Celery
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling

app = Celery('myapp')

@app.task
def setup_worker_profiling():
    """Setup profiling for Celery worker."""
    hub = get_hub()
    register_profiling(hub, sample_rate=0.005)  # Lower rate for workers

    profiler = hub.get_component("profiler")
    profiler.enable()

    return "Profiling enabled for worker"

@app.task
def get_worker_metrics():
    """Get profiling metrics from worker."""
    hub = get_hub()
    profiler = hub.get_component("profiler")

    if not profiler:
        return {"error": "Profiling not available"}

    return profiler.get_metrics().to_dict()

# Worker startup
from celery.signals import worker_ready

@worker_ready.connect
def setup_profiling_on_worker_start(sender=None, **kwargs):
    """Setup profiling when worker starts."""
    setup_worker_profiling.apply_async()
```

## Testing Support

### Test Fixtures

```python
import pytest
from provide.foundation.hub import get_hub
from provide.foundation.profiling.component import register_profiling
from provide.foundation.testmode import (
    reset_hub_state,
    reset_profiling_state
)

@pytest.fixture
def profiling_component():
    """Fixture providing a clean profiling component."""
    # Reset state
    reset_hub_state()
    reset_profiling_state()

    # Setup fresh profiling
    hub = get_hub()
    register_profiling(hub, sample_rate=1.0)  # 100% for testing

    profiler = hub.get_component("profiler")
    profiler.enable()

    yield profiler

    # Cleanup
    profiler.disable()
    reset_profiling_state()

def test_profiling_basic_operation(profiling_component):
    """Test basic profiling operation."""
    profiler = profiling_component

    # Generate test data
    from provide.foundation import logger
    logger.info("Test message 1")
    logger.info("Test message 2", emoji="🔥")

    # Verify metrics
    metrics = profiler.get_metrics()
    assert metrics.message_count >= 0
    assert isinstance(metrics.messages_per_second, (int, float))
```

### Mock Testing

```python
from unittest.mock import patch, MagicMock
from provide.foundation.profiling.component import ProfilingComponent

def test_component_with_mocked_processor():
    """Test component with mocked processor."""
    with patch('provide.foundation.profiling.component.ProfilingProcessor') as mock_processor_class:
        mock_processor = MagicMock()
        mock_processor_class.return_value = mock_processor

        component = ProfilingComponent(sample_rate=0.1)

        # Verify processor creation
        mock_processor_class.assert_called_once_with(sample_rate=0.1)

        # Test enable
        component.enable()
        mock_processor.enable.assert_called_once()

        # Test disable
        component.disable()
        mock_processor.disable.assert_called_once()

        # Test reset
        component.reset()
        mock_processor.reset.assert_called_once()
```

## String Representation

```python
def __repr__(self) -> str
```

Returns a string representation for debugging.

**Format:** `ProfilingComponent(enabled={status}, sample_rate={rate})`

**Example:**
```python
component = ProfilingComponent(sample_rate=0.05)
print(repr(component))
# Output: ProfilingComponent(enabled=disabled, sample_rate=0.05)

component.enable()
print(repr(component))
# Output: ProfilingComponent(enabled=enabled, sample_rate=0.05)
```