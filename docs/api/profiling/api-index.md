# Profiling API Reference

API documentation for Foundation's profiling system.

!!! info "Current Implementation Status"
    Foundation's profiling system is currently in development. This page documents the implemented core components and provides specifications for planned enterprise features.

## Implemented Components

### ProfileMetrics
::: provide.foundation.profiling.metrics.ProfileMetrics
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### ProfilingProcessor
::: provide.foundation.profiling.processor.ProfilingProcessor
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### ProfilingComponent
::: provide.foundation.profiling.component.ProfilingComponent
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

## Utility Functions

### register_profiling
::: provide.foundation.profiling.component.register_profiling
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### reset_profiling_state
::: provide.foundation.testmode.internal.reset_profiling_state
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

## Planned Enterprise Features

The following components are documented in the implementation guides but are planned for future releases:

### Configuration System
- `ProfilingConfig` - Main configuration class
- `ProcessorConfig` - Processor-specific configuration
- `ExporterConfig` - Export configuration
- `AdaptiveSamplingConfig` - Adaptive sampling configuration

### Advanced Sampling
- `LoadBasedSampler` - System load-based sampling
- `PatternBasedSampler` - Pattern-triggered sampling
- `AdaptiveSampler` - Machine learning-based sampling
- `StatisticalSampler` - Statistically representative sampling

### Export System
- `PrometheusExporter` - Prometheus metrics export
- `DatadogExporter` - Datadog APM integration
- `OpenTelemetryExporter` - OpenTelemetry integration
- `FileExporter` - File-based export
- `MultiExporter` - Multiple destination export

### Decorator System
- `@profile_function` - Function profiling decorator
- `@profile_async` - Async function profiling
- `@profile_method` - Method profiling decorator
- `@profile_class` - Class-level profiling

### CLI Integration
- `show_profile_metrics` - CLI metrics display
- `register_profile_command` - CLI command registration

!!! note "Implementation Timeline"
    Enterprise features are planned for implementation in Foundation v1.1+. The current v1.0 release includes the core profiling infrastructure documented above.

## Type Definitions

### ProfileMetrics Fields

| Field | Type | Description |
|-------|------|-------------|
| `message_count` | `int` | Total number of log messages processed |
| `total_duration_ns` | `int` | Total processing time in nanoseconds |
| `emoji_message_count` | `int` | Number of messages with emoji processing |
| `dropped_count` | `int` | Number of messages dropped due to sampling |
| `start_time` | `float` | Timestamp when metrics collection started |

### ProfileMetrics Properties

| Property | Type | Description |
|----------|------|-------------|
| `messages_per_second` | `float` | Current throughput in messages per second |
| `avg_latency_ms` | `float` | Average processing latency in milliseconds |
| `emoji_overhead_percent` | `float` | Percentage of messages that used emoji processing |
| `uptime_seconds` | `float` | Seconds since metrics collection started |

### Export Result Types

```python
from typing import NamedTuple

class ExportResult(NamedTuple):
    success: bool
    exported_count: int
    error_message: str | None = None
    response_time_ms: float | None = None

    @classmethod
    def success(cls, exported_count: int, response_time_ms: float = None) -> 'ExportResult':
        """Create successful export result."""

    @classmethod
    def failure(cls, error: str) -> 'ExportResult':
        """Create failed export result."""
```

### Sampling Context

```python
from typing import Protocol

class SamplingContext(Protocol):
    """Context information available to sampling functions."""

    current_time: datetime
    operation_name: str
    log_level: str
    user_id: str | None
    request_id: str | None

    # System metrics
    cpu_usage_percent: float
    memory_usage_percent: float
    avg_latency_ms: float
    error_rate: float
```

## Exception Types

### ProfilingError
::: provide.foundation.profiling.errors.ProfilingError
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### SamplingError
::: provide.foundation.profiling.errors.SamplingError
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### ExporterError
::: provide.foundation.profiling.errors.ExporterError
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

### ConfigurationError
::: provide.foundation.profiling.errors.ConfigurationError
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true

## Constants and Defaults

### Default Values

```python
# Sampling defaults
DEFAULT_PROFILING_SAMPLE_RATE = 0.01  # 1%
DEFAULT_BUFFER_SIZE = 1000
DEFAULT_FLUSH_INTERVAL_SECONDS = 30

# Memory defaults
DEFAULT_MAX_MEMORY_MB = 100
DEFAULT_TRACK_MEMORY = False

# Export defaults
DEFAULT_BATCH_SIZE = 100
DEFAULT_EXPORT_TIMEOUT_SECONDS = 30
DEFAULT_MAX_RETRIES = 3

# Performance defaults
DEFAULT_ENABLE_FAST_PATH = True
DEFAULT_BACKGROUND_PROCESSING = True
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROVIDE_PROFILING_ENABLED` | `false` | Enable/disable profiling |
| `PROVIDE_PROFILING_SAMPLE_RATE` | `0.01` | Default sampling rate |
| `PROVIDE_PROFILING_TRACK_MEMORY` | `false` | Enable memory tracking |
| `PROVIDE_PROFILING_BUFFER_SIZE` | `1000` | Buffer size for metrics |
| `PROVIDE_PROFILING_CLI_ENABLED` | `true` | Enable CLI commands |
| `PROVIDE_PROFILING_EXPORTERS` | `""` | Comma-separated list of exporters |

## Version Information

```python
from provide.foundation.profiling import __version__

print(f"Profiling API version: {__version__}")
```

## Migration Guide

### From Basic Metrics to Profiling

If you were using basic metrics collection:

```python
# Old approach
from provide.foundation.logger.metrics import LogMetrics

metrics = LogMetrics()
# Limited functionality

# New approach
from provide.foundation.profiling import register_profiling

register_profiling(hub)
profiler = hub.get_component("profiler")
profiler.enable()
# Full profiling capabilities
```

### Upgrading Configurations

Configuration format changes:

```python
# Old configuration (deprecated)
config = {
    "profiling_enabled": True,
    "sample_rate": 0.02
}

# New configuration
from provide.foundation.profiling.config import ProfilingConfig

config = ProfilingConfig(
    enabled=True,
    sample_rate=0.02,
    processor=ProcessorConfig(...),
    exporters=[...]
)
```

## Best Practices

### Error Handling

```python
from provide.foundation.profiling.errors import ProfilingError

try:
    register_profiling(hub, sample_rate=0.02)
    profiler = hub.get_component("profiler")
    profiler.enable()
except ProfilingError as e:
    logger.warning(f"Profiling setup failed: {e}")
    # Continue without profiling
```

### Resource Cleanup

```python
import atexit

def cleanup_profiling():
    """Cleanup profiling resources on shutdown."""
    try:
        profiler = hub.get_component("profiler")
        if profiler:
            profiler.flush_remaining_data()
            profiler.disable()
    except Exception as e:
        logger.warning(f"Profiling cleanup failed: {e}")

atexit.register(cleanup_profiling)
```

### Thread Safety

All profiling operations are thread-safe:

```python
import threading
from provide.foundation import logger

def worker():
    """Worker function - profiling is thread-safe."""
    for i in range(100):
        logger.info(f"Processing item {i}")

# Safe to use across multiple threads
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```