# ProfilingProcessor API

Detailed API documentation for the ProfilingProcessor class, which integrates with structlog to collect performance metrics.

!!! info "Implementation Status"
    ProfilingProcessor is currently implemented and available in Foundation's profiling system.

## Class Overview

::: provide.foundation.profiling.processor.ProfilingProcessor
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true
      show_signature_annotations: true
      separate_signature: true

## Constructor

```python
ProfilingProcessor(sample_rate: float = DEFAULT_PROFILING_SAMPLE_RATE) -> ProfilingProcessor
```

Creates a new ProfilingProcessor that can be added to structlog's processor chain.

**Parameters:**
- `sample_rate` (float): Fraction of messages to sample (0.0 to 1.0)

**Raises:**
- `ValueError`: If sample_rate is not between 0.0 and 1.0

**Example:**
```python
from provide.foundation.profiling.processor import ProfilingProcessor

# Conservative sampling for production
processor = ProfilingProcessor(sample_rate=0.01)  # 1%

# Detailed sampling for development
processor = ProfilingProcessor(sample_rate=0.50)  # 50%

# Complete sampling for testing
processor = ProfilingProcessor(sample_rate=1.0)   # 100%
```

## Core Properties

### sample_rate
- **Type:** `float`
- **Description:** Current sampling rate (0.0 to 1.0)
- **Read-only:** Set during initialization

### metrics
- **Type:** `ProfileMetrics`
- **Description:** Metrics collection instance
- **Thread Safety:** Thread-safe for read access

## Methods

### \_\_call\_\_

```python
def __call__(
    self,
    logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> structlog.types.EventDict
```

Main entry point called by structlog for each log event. This is the core method that integrates profiling into the structlog pipeline.

**Parameters:**
- `logger` (Any): The logger instance (unused by profiling)
- `method_name` (str): The logging method name (unused by profiling)
- `event_dict` (structlog.types.EventDict): The event dictionary to process

**Returns:** The `event_dict` unchanged (pass-through processor)

**Thread Safety:** This method is thread-safe and can be called concurrently.

**Performance:** Optimized for minimal overhead:
- Sampling decision: ~10 nanoseconds
- Metrics collection (when sampled): ~100-200 nanoseconds
- Total overhead: Sample rate × 200ns per message

**Example:**
```python
import structlog

# Create processor
processor = ProfilingProcessor(sample_rate=0.02)

# Add to structlog configuration
structlog.configure(
    processors=[
        processor,  # Add profiling processor
        structlog.processors.JSONRenderer()
    ]
)

# Normal logging automatically gets profiled
logger = structlog.get_logger()
logger.info("This message may be sampled for profiling")
```

### enable

```python
def enable(self) -> None
```

Enables metrics collection. Profiling is enabled by default on creation.

**Example:**
```python
processor = ProfilingProcessor()
processor.disable()  # Temporarily disable
# ... some processing ...
processor.enable()   # Re-enable profiling
```

### disable

```python
def disable(self) -> None
```

Disables metrics collection. When disabled, the processor becomes a complete pass-through with minimal overhead.

**Performance Impact:** Disabled processor adds ~1 nanosecond overhead per message.

**Example:**
```python
# Temporarily disable profiling during high-load periods
if system_load > 0.90:
    processor.disable()
else:
    processor.enable()
```

### reset

```python
def reset(self) -> None
```

Resets collected metrics to initial values. Useful for testing or periodic metric collection.

**Thread Safety:** This method is thread-safe.

**Example:**
```python
# Reset metrics for new measurement period
processor.reset()
print("Metrics reset - starting fresh measurement")
```

### get_metrics

```python
def get_metrics(self) -> ProfileMetrics
```

Returns the current metrics instance.

**Returns:** The ProfileMetrics instance containing collected data.

**Thread Safety:** Safe to call concurrently with metric collection.

**Example:**
```python
metrics = processor.get_metrics()
print(f"Current throughput: {metrics.messages_per_second:.1f} msg/sec")
```

## Internal Methods

### \_detect_emoji_processing

```python
def _detect_emoji_processing(self, event_dict: structlog.types.EventDict) -> bool
```

Analyzes an event dictionary to determine if emoji processing was involved.

**Parameters:**
- `event_dict` (structlog.types.EventDict): The event to analyze

**Returns:** `True` if emoji processing was detected

**Detection Logic:**
- Checks for Foundation-specific emoji fields: `emoji`, `emoji_prefix`, `logger_name_emoji`
- Fast string-based detection optimized for performance

**Example:**
```python
# These events would be detected as emoji processing
logger.info("User login", emoji="👤")
logger.error("Database error", emoji_prefix="🔌")

# This would not
logger.info("User login", user_id=12345)
```

## Integration Patterns

### Adding to Structlog

```python
import structlog
from provide.foundation.profiling.processor import ProfilingProcessor

# Create processor with desired sampling
profiling_processor = ProfilingProcessor(sample_rate=0.02)

# Configure structlog with profiling
structlog.configure(
    processors=[
        # Standard processors
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),

        # Add profiling processor
        profiling_processor,

        # Final rendering
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.LoggerAdapter,
    logger_factory=structlog.stdlib.LoggerFactory(),
    context_class=dict,
    cache_logger_on_first_use=True,
)
```

### Multiple Processors

```python
# Different sampling rates for different purposes
high_frequency_processor = ProfilingProcessor(sample_rate=0.50)  # Detailed
low_frequency_processor = ProfilingProcessor(sample_rate=0.01)   # Overview

# Conditional processing
def conditional_profiling_processor(logger, method_name, event_dict):
    """Apply different profiling based on log level."""
    if event_dict.get('level') == 'error':
        return high_frequency_processor(logger, method_name, event_dict)
    else:
        return low_frequency_processor(logger, method_name, event_dict)

# Add to processor chain
structlog.configure(
    processors=[
        conditional_profiling_processor,
        structlog.processors.JSONRenderer()
    ]
)
```

### Dynamic Sampling Control

```python
class AdaptiveProfilingProcessor:
    """Processor that adapts sampling rate based on system load."""

    def __init__(self, base_rate: float = 0.01):
        self.base_rate = base_rate
        self.processor = ProfilingProcessor(sample_rate=base_rate)
        self.last_adjustment = time.time()

    def __call__(self, logger, method_name, event_dict):
        # Adjust sampling rate every 60 seconds
        if time.time() - self.last_adjustment > 60:
            self._adjust_sampling_rate()
            self.last_adjustment = time.time()

        return self.processor(logger, method_name, event_dict)

    def _adjust_sampling_rate(self):
        """Adjust sampling based on system metrics."""
        import psutil

        cpu_percent = psutil.cpu_percent()
        if cpu_percent > 80:
            # Reduce sampling under high load
            new_rate = self.base_rate * 0.5
        elif cpu_percent < 20:
            # Increase sampling under low load
            new_rate = self.base_rate * 2.0
        else:
            new_rate = self.base_rate

        # Create new processor with adjusted rate
        self.processor = ProfilingProcessor(sample_rate=min(new_rate, 1.0))

    def get_metrics(self):
        return self.processor.get_metrics()
```

## Performance Characteristics

### Sampling Performance

```python
import time
import random

# Benchmark sampling decision overhead
processor = ProfilingProcessor(sample_rate=0.02)
iterations = 1_000_000

# Test with sampling
start = time.perf_counter()
for _ in range(iterations):
    # Simulate sampling decision
    should_sample = random.random() <= processor.sample_rate
elapsed_with_sampling = time.perf_counter() - start

# Test without sampling (disabled processor)
processor.disable()
start = time.perf_counter()
for _ in range(iterations):
    processor(None, "info", {"message": "test"})
elapsed_disabled = time.perf_counter() - start

print(f"Sampling overhead: {(elapsed_with_sampling - elapsed_disabled) * 1e9 / iterations:.0f} ns/call")
```

### Memory Overhead

```python
import sys
from provide.foundation.profiling.processor import ProfilingProcessor

# Measure memory overhead
processor = ProfilingProcessor()
print(f"Processor size: {sys.getsizeof(processor)} bytes")
print(f"Metrics size: {sys.getsizeof(processor.metrics)} bytes")

# Memory usage during operation
import tracemalloc

tracemalloc.start()

# Process many messages
for i in range(10000):
    processor(None, "info", {"message": f"test {i}", "emoji": "🔥"})

current, peak = tracemalloc.get_traced_memory()
print(f"Memory usage: {current / 1024:.1f} KB current, {peak / 1024:.1f} KB peak")
tracemalloc.stop()
```

## Thread Safety

The ProfilingProcessor is fully thread-safe:

```python
import threading
import structlog
from provide.foundation.profiling.processor import ProfilingProcessor

# Shared processor across threads
processor = ProfilingProcessor(sample_rate=0.10)

# Configure structlog with shared processor
structlog.configure(
    processors=[processor, structlog.processors.JSONRenderer()]
)

def worker_thread(thread_id: int):
    """Worker that logs messages - safe with shared processor."""
    logger = structlog.get_logger()

    for i in range(1000):
        logger.info(
            "Worker message",
            thread_id=thread_id,
            iteration=i,
            emoji="⚙️"
        )

# Start multiple threads using the same processor
threads = [
    threading.Thread(target=worker_thread, args=(i,))
    for i in range(5)
]

for t in threads:
    t.start()
for t in threads:
    t.join()

# Thread-safe metrics access
metrics = processor.get_metrics()
print(f"Total messages from all threads: {metrics.message_count}")
```

## Error Handling

The processor is designed to never break the logging pipeline:

```python
import structlog
from provide.foundation.profiling.processor import ProfilingProcessor

class TestProcessor(ProfilingProcessor):
    """Test processor that demonstrates error handling."""

    def _detect_emoji_processing(self, event_dict):
        # Simulate an error in emoji detection
        if event_dict.get("cause_error"):
            raise ValueError("Simulated error")

        return super()._detect_emoji_processing(event_dict)

# Even with errors, logging continues
processor = TestProcessor(sample_rate=1.0)
structlog.configure(processors=[processor, structlog.processors.JSONRenderer()])

logger = structlog.get_logger()

# This will cause an error in profiling, but logging continues
logger.info("This message will be logged despite profiling error", cause_error=True)
logger.info("This message will be processed normally")

print("Both messages were logged successfully")
```

## Testing Utilities

### Deterministic Testing

```python
from unittest.mock import patch
from provide.foundation.profiling.processor import ProfilingProcessor

def test_with_fixed_sampling():
    """Test with deterministic sampling."""
    processor = ProfilingProcessor(sample_rate=0.5)

    # Mock random.random to return predictable values
    with patch('random.random') as mock_random:
        # First call returns 0.3 (< 0.5, should sample)
        # Second call returns 0.7 (> 0.5, should not sample)
        mock_random.side_effect = [0.3, 0.7]

        # First message should be sampled
        processor(None, "info", {"message": "test1"})

        # Second message should not be sampled
        processor(None, "info", {"message": "test2"})

        # Verify sampling behavior
        assert mock_random.call_count == 2
        # Additional assertions based on expected behavior
```

### Metrics Validation

```python
def test_metrics_accuracy():
    """Test that metrics are calculated correctly."""
    processor = ProfilingProcessor(sample_rate=1.0)  # 100% sampling

    # Record known data
    with patch('time.perf_counter_ns') as mock_time:
        mock_time.side_effect = [0, 1_000_000, 1_000_000, 3_000_000]  # 1ms, 2ms

        processor(None, "info", {"message": "msg1", "emoji": "🔥"})
        processor(None, "info", {"message": "msg2"})

    metrics = processor.get_metrics()

    # Verify calculations
    assert metrics.message_count == 2
    assert metrics.emoji_message_count == 1
    assert metrics.total_duration_ns == 3_000_000  # 1ms + 2ms
    assert metrics.avg_latency_ms == 1.5  # (1ms + 2ms) / 2
    assert metrics.emoji_overhead_percent == 50.0  # 1 of 2 messages
```

## Configuration Best Practices

### Production Configuration

```python
# Conservative production setup
production_processor = ProfilingProcessor(
    sample_rate=0.01  # 1% sampling for minimal overhead
)

# Add early in processor chain for accurate timing
structlog.configure(
    processors=[
        production_processor,              # Early for accurate metrics
        structlog.stdlib.filter_by_level,  # Standard processors after
        structlog.stdlib.add_logger_name,
        structlog.processors.JSONRenderer()
    ]
)
```

### Development Configuration

```python
# Detailed development setup
development_processor = ProfilingProcessor(
    sample_rate=1.0  # 100% sampling for complete visibility
)

# More detailed processor chain
structlog.configure(
    processors=[
        development_processor,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()  # Pretty output for development
    ]
)
```

### Environment-Based Configuration

```python
import os

# Configure based on environment
env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    sample_rate = 0.005  # 0.5% for production
elif env == "staging":
    sample_rate = 0.02   # 2% for staging
else:
    sample_rate = 0.50   # 50% for development

processor = ProfilingProcessor(sample_rate=sample_rate)
```