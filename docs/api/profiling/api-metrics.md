# ProfileMetrics API

Detailed API documentation for the ProfileMetrics class, which stores and calculates profiling statistics.

!!! info "Implementation Status"
    ProfileMetrics is currently implemented and available in Foundation's profiling system.

## Class Overview

::: provide.foundation.profiling.metrics.ProfileMetrics
    options:
      show_source: true
      show_root_heading: true
      show_symbol_type_heading: true
      show_signature_annotations: true
      separate_signature: true

## Constructor

```python
ProfileMetrics() -> ProfileMetrics
```

Creates a new ProfileMetrics instance with all counters initialized to zero and start time set to current time.

**Example:**
```python
from provide.foundation.profiling.metrics import ProfileMetrics

metrics = ProfileMetrics()
print(f"Started at: {metrics.start_time}")
```

## Core Fields

### message_count
- **Type:** `int`
- **Description:** Total number of log messages processed
- **Thread Safety:** Updates are protected by internal lock

### total_duration_ns
- **Type:** `int`
- **Description:** Cumulative processing time in nanoseconds
- **Thread Safety:** Updates are protected by internal lock

### emoji_message_count
- **Type:** `int`
- **Description:** Number of messages that included emoji processing
- **Thread Safety:** Updates are protected by internal lock

### dropped_count
- **Type:** `int`
- **Description:** Number of messages that were dropped due to sampling
- **Thread Safety:** Updates are protected by internal lock

### start_time
- **Type:** `float`
- **Description:** Unix timestamp when metrics collection started
- **Thread Safety:** Read-only after initialization

## Methods

### record_message

```python
def record_message(
    self,
    duration_ns: int,
    has_emoji: bool,
    field_count: int
) -> None
```

Records metrics for a single log message.

**Parameters:**
- `duration_ns` (int): Processing time in nanoseconds
- `has_emoji` (bool): Whether the message included emoji processing
- `field_count` (int): Number of fields in the log message

**Thread Safety:** This method is thread-safe and can be called concurrently.

**Example:**
```python
import time

start = time.perf_counter_ns()
# ... log processing ...
end = time.perf_counter_ns()

metrics.record_message(
    duration_ns=end - start,
    has_emoji=True,
    field_count=5
)
```

### reset

```python
def reset(self) -> None
```

Resets all metrics to initial values and updates start time to current time.

**Thread Safety:** This method is thread-safe.

**Example:**
```python
# Reset metrics for new measurement period
metrics.reset()
print(f"Metrics reset at: {metrics.start_time}")
```

### to_dict

```python
def to_dict(self) -> dict[str, float | int]
```

Converts metrics to a dictionary suitable for serialization or export.

**Returns:** Dictionary containing all metrics and calculated properties.

**Example:**
```python
data = metrics.to_dict()
print(f"Throughput: {data['messages_per_second']:.1f} msg/sec")
print(f"Latency: {data['avg_latency_ms']:.2f}ms")
```

**Return Value Structure:**
```python
{
    # Raw metrics
    "total_messages": int,
    "emoji_messages": int,
    "dropped_messages": int,
    "total_duration_ns": int,
    "uptime_seconds": float,

    # Calculated metrics
    "messages_per_second": float,
    "avg_latency_ms": float,
    "emoji_overhead_percent": float,

    # Timestamps
    "start_time": float,
    "current_time": float
}
```

## Calculated Properties

### messages_per_second
- **Type:** `float`
- **Description:** Current throughput in messages per second
- **Calculation:** `message_count / uptime_seconds`
- **Returns:** `0.0` if no time has elapsed

**Example:**
```python
throughput = metrics.messages_per_second
print(f"Processing {throughput:.1f} messages per second")
```

### avg_latency_ms
- **Type:** `float`
- **Description:** Average processing latency in milliseconds
- **Calculation:** `(total_duration_ns / message_count) / 1_000_000`
- **Returns:** `0.0` if no messages processed

**Example:**
```python
latency = metrics.avg_latency_ms
if latency > 10:
    print(f"⚠️  High latency detected: {latency:.2f}ms")
```

### emoji_overhead_percent
- **Type:** `float`
- **Description:** Percentage of messages that used emoji processing
- **Calculation:** `(emoji_message_count / message_count) * 100`
- **Returns:** `0.0` if no messages processed

**Example:**
```python
overhead = metrics.emoji_overhead_percent
print(f"Emoji processing overhead: {overhead:.1f}%")
```

### uptime_seconds
- **Type:** `float`
- **Description:** Seconds since metrics collection started
- **Calculation:** `time.time() - start_time`

**Example:**
```python
uptime = metrics.uptime_seconds
print(f"Collecting metrics for {uptime:.0f} seconds")
```

## Thread Safety

ProfileMetrics is fully thread-safe:

```python
import threading
from provide.foundation.profiling.metrics import ProfileMetrics

metrics = ProfileMetrics()

def worker():
    """Thread worker - safe to call concurrently."""
    for i in range(1000):
        metrics.record_message(
            duration_ns=1000000,  # 1ms
            has_emoji=i % 10 == 0,  # 10% emoji
            field_count=3
        )

# Start multiple threads
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Total messages: {metrics.message_count}")
print(f"Throughput: {metrics.messages_per_second:.0f} msg/sec")
```

## Performance Characteristics

### Memory Usage
- **Base overhead:** ~200 bytes per ProfileMetrics instance
- **Per-message overhead:** 0 bytes (no per-message storage)
- **Thread safety overhead:** One `threading.Lock` per instance

### CPU Performance
- **record_message():** ~100-200 nanoseconds per call
- **Calculated properties:** ~50-100 nanoseconds per access
- **Thread contention:** Minimal due to fast operations under lock

### Benchmarks

```python
import time
from provide.foundation.profiling.metrics import ProfileMetrics

# Benchmark record_message performance
metrics = ProfileMetrics()
iterations = 100_000

start = time.perf_counter()
for i in range(iterations):
    metrics.record_message(1000000, False, 3)
elapsed = time.perf_counter() - start

ns_per_call = (elapsed * 1_000_000_000) / iterations
print(f"record_message: {ns_per_call:.0f} ns/call")
```

## Usage Patterns

### Basic Metrics Collection

```python
from provide.foundation.profiling.metrics import ProfileMetrics

metrics = ProfileMetrics()

# Record some sample data
for i in range(100):
    metrics.record_message(
        duration_ns=2_000_000,  # 2ms
        has_emoji=i % 5 == 0,   # 20% emoji
        field_count=4
    )

# View results
print(f"Processed {metrics.message_count} messages")
print(f"Average latency: {metrics.avg_latency_ms:.1f}ms")
print(f"Emoji usage: {metrics.emoji_overhead_percent:.0f}%")
```

### Periodic Reporting

```python
import time
import threading

def periodic_reporter(metrics: ProfileMetrics, interval_seconds: int = 60):
    """Report metrics every interval."""
    while True:
        time.sleep(interval_seconds)

        data = metrics.to_dict()
        print(f"""
📊 Metrics Report:
   Messages/sec: {data['messages_per_second']:.0f}
   Avg latency: {data['avg_latency_ms']:.1f}ms
   Emoji overhead: {data['emoji_overhead_percent']:.0f}%
   Uptime: {data['uptime_seconds']:.0f}s
        """)

# Start background reporting
metrics = ProfileMetrics()
reporter_thread = threading.Thread(
    target=periodic_reporter,
    args=(metrics, 30),  # Report every 30 seconds
    daemon=True
)
reporter_thread.start()
```

### Metrics Aggregation

```python
from typing import List

def aggregate_metrics(metrics_list: List[ProfileMetrics]) -> ProfileMetrics:
    """Aggregate multiple ProfileMetrics instances."""
    if not metrics_list:
        return ProfileMetrics()

    # Start with first metrics instance
    aggregated = ProfileMetrics()

    # Find earliest start time
    aggregated.start_time = min(m.start_time for m in metrics_list)

    # Sum all counters
    for metrics in metrics_list:
        aggregated.message_count += metrics.message_count
        aggregated.total_duration_ns += metrics.total_duration_ns
        aggregated.emoji_message_count += metrics.emoji_message_count
        aggregated.dropped_count += metrics.dropped_count

    return aggregated

# Example usage
worker_metrics = [ProfileMetrics() for _ in range(3)]
# ... workers populate their metrics ...

combined = aggregate_metrics(worker_metrics)
print(f"Combined throughput: {combined.messages_per_second:.0f} msg/sec")
```

## Serialization and Export

### JSON Export

```python
import json

def export_metrics_json(metrics: ProfileMetrics) -> str:
    """Export metrics as JSON string."""
    data = metrics.to_dict()
    return json.dumps(data, indent=2)

# Usage
json_data = export_metrics_json(metrics)
print(json_data)
```

### CSV Export

```python
import csv
import io

def export_metrics_csv(metrics_list: List[ProfileMetrics]) -> str:
    """Export multiple metrics instances as CSV."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        "timestamp", "messages_per_second", "avg_latency_ms",
        "emoji_overhead_percent", "total_messages"
    ])

    # Write data
    for metrics in metrics_list:
        data = metrics.to_dict()
        writer.writerow([
            data["current_time"],
            data["messages_per_second"],
            data["avg_latency_ms"],
            data["emoji_overhead_percent"],
            data["total_messages"]
        ])

    return output.getvalue()
```

## Error Handling

ProfileMetrics operations are designed to be robust:

```python
# All operations handle edge cases gracefully
metrics = ProfileMetrics()

# Division by zero protection
print(metrics.messages_per_second)  # Returns 0.0 when no time elapsed
print(metrics.avg_latency_ms)       # Returns 0.0 when no messages

# Negative values are handled
try:
    metrics.record_message(-1000, False, 1)  # Will be recorded as-is
except Exception:
    pass  # No exceptions thrown

# Thread safety ensures consistency
# Even under high concurrency, metrics remain consistent
```

## Integration Examples

### With Prometheus

```python
from prometheus_client import Gauge, Counter

# Create Prometheus metrics
throughput_gauge = Gauge('foundation_messages_per_second', 'Messages per second')
latency_gauge = Gauge('foundation_avg_latency_ms', 'Average latency in ms')
total_counter = Counter('foundation_messages_total', 'Total messages processed')

def update_prometheus_metrics(metrics: ProfileMetrics):
    """Update Prometheus metrics from ProfileMetrics."""
    throughput_gauge.set(metrics.messages_per_second)
    latency_gauge.set(metrics.avg_latency_ms)

    # Update counter (must handle reset scenarios)
    current_total = total_counter._value._value
    if metrics.message_count >= current_total:
        total_counter._value._value = metrics.message_count
```

### With Datadog

```python
import datadog

def send_to_datadog(metrics: ProfileMetrics, tags: List[str] = None):
    """Send metrics to Datadog."""
    timestamp = int(time.time())
    tags = tags or []

    datadog.api.Metric.send([
        {
            'metric': 'foundation.profiling.throughput',
            'points': [(timestamp, metrics.messages_per_second)],
            'tags': tags
        },
        {
            'metric': 'foundation.profiling.latency',
            'points': [(timestamp, metrics.avg_latency_ms)],
            'tags': tags
        },
        {
            'metric': 'foundation.profiling.emoji_overhead',
            'points': [(timestamp, metrics.emoji_overhead_percent)],
            'tags': tags
        }
    ])
```