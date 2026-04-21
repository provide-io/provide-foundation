# Custom Log Processors

Learn how to create custom log processors to transform, enrich, filter, and sanitize log events in Foundation applications.

## Overview

Log processors are the heart of Foundation's logging pipeline. They transform log events before they're written, allowing you to add context, filter sensitive data, format output, and implement custom logic. Foundation uses a processor chain where each processor can modify the event dictionary.

**What you'll learn:**
- Create custom processors for event transformation
- Add contextual information to logs
- Filter and sanitize sensitive data
- Implement conditional processing
- Build async processors
- Handle errors in processors
- Test custom processors
- Optimize processor performance

**Key Features:**
- 🔧 **Flexible API**: Simple function-based processor interface
- 📊 **Event Enrichment**: Add context, metrics, and metadata
- 🔒 **Data Sanitization**: Remove or mask sensitive information
- ⚡ **High Performance**: Minimal overhead, async support
- 🎯 **Conditional Logic**: Process based on log level, context, or custom rules
- 🧪 **Testable**: Easy to unit test and mock

## Prerequisites

```bash
# Foundation includes structlog processors
uv add provide-foundation

# For advanced async processing
uv add provide-foundation[async]
```

## Processor Basics

### Simple Processor

A processor is a callable that receives the logger, method name, and event dictionary:

```python
from provide.foundation import get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation import logger

def add_hostname_processor(logger_instance, method_name, event_dict):
    """Add hostname to every log event."""
    import socket
    event_dict["hostname"] = socket.gethostname()
    return event_dict

# Register the processor
hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name="my-app",
        logging=LoggingConfig(
            processors=[add_hostname_processor]
        )
    )
)

# Now all logs include hostname
logger.info("user_login", user_id="123")
# Output: {"event": "user_login", "hostname": "app-server-01", ...}
```

### Processor Signature

Every processor must follow this signature:

```python
from typing import Any

def my_processor(
    logger_instance: Any,  # The logger instance
    method_name: str,      # Method name (debug, info, warning, error)
    event_dict: dict[str, Any]  # Mutable event dictionary
) -> dict[str, Any]:
    """Process a log event.

    Args:
        logger_instance: The logger that created the event
        method_name: The log level method called (info, error, etc.)
        event_dict: The event dictionary to modify

    Returns:
        The modified event dictionary (or raise to suppress)
    """
    # Modify event_dict in place or create new dict
    event_dict["custom_field"] = "custom_value"
    return event_dict
```

## Context Enrichment

### Add Request Context

Add request information to all logs within a request:

```python
import contextvars
from provide.foundation import logger

# Context variable for request ID
request_context = contextvars.ContextVar("request_context", default={})

def add_request_context_processor(logger_instance, method_name, event_dict):
    """Add request context to logs."""
    context = request_context.get()

    if context:
        event_dict["request_id"] = context.get("request_id")
        event_dict["user_id"] = context.get("user_id")
        event_dict["client_ip"] = context.get("client_ip")

    return event_dict

# In your request handler
def handle_request(request):
    """Handle an HTTP request."""
    # Set context for this request
    request_context.set({
        "request_id": request.headers.get("X-Request-ID"),
        "user_id": request.user.id,
        "client_ip": request.remote_addr
    })

    # All logs in this context will include request info
    logger.info("request_started", path=request.path)
    process_request(request)
    logger.info("request_completed", status=200)
```

### Add Application Metadata

Include application version, environment, and deployment info:

```python
import os
from datetime import datetime
from provide.foundation import logger

# Load at startup
APP_METADATA = {
    "version": os.getenv("APP_VERSION", "unknown"),
    "environment": os.getenv("ENVIRONMENT", "dev"),
    "deployed_at": datetime.now().isoformat(),
    "region": os.getenv("AWS_REGION", "local")
}

def add_app_metadata_processor(logger_instance, method_name, event_dict):
    """Add application metadata to logs."""
    event_dict.update({
        "app_version": APP_METADATA["version"],
        "environment": APP_METADATA["environment"],
        "region": APP_METADATA["region"]
    })
    return event_dict

# All logs now include app context
logger.info("application_started")
# {"event": "application_started", "app_version": "1.2.3", "environment": "production", ...}
```

### Add Performance Metrics

Track performance metrics in logs:

```python
import time
from provide.foundation import logger

def add_duration_processor(logger_instance, method_name, event_dict):
    """Calculate duration if start_time is present."""
    if "start_time" in event_dict:
        duration_ms = (time.time() - event_dict["start_time"]) * 1000
        event_dict["duration_ms"] = round(duration_ms, 2)
        # Remove start_time from output
        del event_dict["start_time"]

    return event_dict

# Usage
start = time.time()
process_data()
logger.info("data_processed", start_time=start, records=1000)
# {"event": "data_processed", "duration_ms": 123.45, "records": 1000}
```

## Data Sanitization

### Filter Sensitive Data

Remove or mask sensitive information from logs:

```python
import re
from provide.foundation import logger

# Patterns for sensitive data
SENSITIVE_KEYS = {"password", "api_key", "token", "secret", "credit_card"}
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')

def sanitize_sensitive_data_processor(logger_instance, method_name, event_dict):
    """Remove or mask sensitive data."""

    def sanitize_value(key: str, value: Any) -> Any:
        """Sanitize a single value."""
        # Mask sensitive keys
        if isinstance(key, str) and any(s in key.lower() for s in SENSITIVE_KEYS):
            return "***REDACTED***"

        # Mask email addresses in strings
        if isinstance(value, str):
            value = EMAIL_PATTERN.sub("***@***.***", value)
            value = CREDIT_CARD_PATTERN.sub("****-****-****-****", value)

        # Recursively sanitize dicts
        elif isinstance(value, dict):
            return {k: sanitize_value(k, v) for k, v in value.items()}

        # Recursively sanitize lists
        elif isinstance(value, list):
            return [sanitize_value("", v) for v in value]

        return value

    # Sanitize all event fields
    for key in list(event_dict.keys()):
        event_dict[key] = sanitize_value(key, event_dict[key])

    return event_dict

# Usage
logger.info(
    "user_created",
    user_id="123",
    email="user@example.com",
    password="secret123",  # Will be redacted
    api_key="sk_live_abc123"  # Will be redacted
)
# Output: {"event": "user_created", "email": "***@***.***", "password": "***REDACTED***", ...}
```

### PII Masking

Mask personally identifiable information:

```python
from provide.foundation import logger

def mask_pii_processor(logger_instance, method_name, event_dict):
    """Mask PII fields."""
    pii_fields = {"ssn", "tax_id", "passport", "drivers_license"}

    for field in pii_fields:
        if field in event_dict and event_dict[field]:
            value = str(event_dict[field])
            # Show last 4 digits only
            if len(value) > 4:
                event_dict[field] = "*" * (len(value) - 4) + value[-4:]

    return event_dict

# Usage
logger.info("identity_verified", ssn="123-45-6789")
# Output: {"event": "identity_verified", "ssn": "*****6789"}
```

## Conditional Processing

### Log Level Filtering

Apply processors only for specific log levels:

```python
from provide.foundation.logger.levels import LogLevel
from provide.foundation import logger

def production_only_processor(logger_instance, method_name, event_dict):
    """Only process in production environment."""
    import os

    if os.getenv("ENVIRONMENT") != "production":
        return event_dict

    # Add production-specific context
    event_dict["environment"] = "production"
    event_dict["region"] = os.getenv("AWS_REGION", "unknown")
    event_dict["alert_pagerduty"] = method_name in ("error", "critical")

    return event_dict

def error_only_enrichment(logger_instance, method_name, event_dict):
    """Add extra context for errors."""
    if method_name not in ("error", "critical"):
        return event_dict

    # Add debugging context for errors
    import sys
    event_dict["python_version"] = sys.version
    event_dict["severity"] = "HIGH" if method_name == "critical" else "MEDIUM"

    return event_dict
```

### Sampling Processor

Sample high-volume logs to reduce noise:

```python
import random
from provide.foundation import logger

class SamplingProcessor:
    """Sample logs based on rate."""

    def __init__(self, sample_rate: float = 0.1):
        """Initialize with sample rate (0.0-1.0)."""
        self.sample_rate = sample_rate

    def __call__(self, logger_instance, method_name, event_dict):
        """Sample the log event."""
        # Always log errors and warnings
        if method_name in ("error", "critical", "warning"):
            return event_dict

        # Sample info and debug logs
        if random.random() > self.sample_rate:
            # Suppress this log by raising DropEvent
            from structlog.exceptions import DropEvent
            raise DropEvent

        event_dict["sampled"] = True
        return event_dict

# Use with 10% sampling for info logs
sampler = SamplingProcessor(sample_rate=0.1)
```

## Advanced Processors

### Async Processor

Process events asynchronously for expensive operations:

```python
import asyncio
from provide.foundation import logger

class AsyncEnrichmentProcessor:
    """Async processor for expensive enrichment."""

    def __init__(self):
        self.cache = {}

    async def enrich_user_data(self, user_id: str) -> dict:
        """Fetch user data (simulated)."""
        if user_id in self.cache:
            return self.cache[user_id]

        # Simulate async API call
        await asyncio.sleep(0.01)
        user_data = {"name": f"User{user_id}", "role": "member"}

        self.cache[user_id] = user_data
        return user_data

    def __call__(self, logger_instance, method_name, event_dict):
        """Add user data if user_id present."""
        user_id = event_dict.get("user_id")

        if not user_id:
            return event_dict

        # Run async enrichment
        try:
            loop = asyncio.get_event_loop()
            user_data = loop.run_until_complete(
                self.enrich_user_data(user_id)
            )
            event_dict["user_name"] = user_data["name"]
            event_dict["user_role"] = user_data["role"]
        except Exception as e:
            event_dict["enrichment_error"] = str(e)

        return event_dict
```

### Batching Processor

Buffer events for batch processing:

```python
from queue import Queue
from threading import Thread, Event
import time
from provide.foundation import logger

class BatchingProcessor:
    """Buffer and process logs in batches."""

    def __init__(self, batch_size: int = 100, flush_interval: float = 5.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.queue: Queue = Queue()
        self.stop_event = Event()

        # Start background thread
        self.thread = Thread(target=self._process_batches, daemon=True)
        self.thread.start()

    def _process_batches(self):
        """Process batches in background."""
        batch = []
        last_flush = time.time()

        while not self.stop_event.is_set():
            try:
                # Get event with timeout
                event = self.queue.get(timeout=1.0)
                batch.append(event)

                # Flush if batch is full or interval elapsed
                should_flush = (
                    len(batch) >= self.batch_size or
                    time.time() - last_flush >= self.flush_interval
                )

                if should_flush and batch:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()

            except Exception:
                continue

        # Flush remaining
        if batch:
            self._flush_batch(batch)

    def _flush_batch(self, batch: list[dict]):
        """Send batch to external service."""
        logger.debug("batch_flushed", count=len(batch))
        # Send to log aggregation service
        # send_to_datadog(batch)

    def __call__(self, logger_instance, method_name, event_dict):
        """Queue event for batching."""
        self.queue.put(event_dict.copy())
        return event_dict

    def shutdown(self):
        """Stop background processing."""
        self.stop_event.set()
        self.thread.join(timeout=10)
```

### Metric Collection Processor

Collect metrics from log events:

```python
from collections import defaultdict
from threading import Lock
from provide.foundation import logger

class MetricsProcessor:
    """Collect metrics from log events."""

    def __init__(self):
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)
        self.lock = Lock()

    def __call__(self, logger_instance, method_name, event_dict):
        """Extract metrics from events."""
        event_name = event_dict.get("event", "unknown")

        with self.lock:
            # Count events
            self.counters[f"{event_name}.count"] += 1
            self.counters[f"log.{method_name}.count"] += 1

            # Track durations
            if "duration_ms" in event_dict:
                self.timers[f"{event_name}.duration"].append(
                    event_dict["duration_ms"]
                )

        return event_dict

    def get_metrics(self) -> dict:
        """Get collected metrics."""
        with self.lock:
            metrics = dict(self.counters)

            # Calculate timer stats
            for key, values in self.timers.items():
                if values:
                    metrics[f"{key}.avg"] = sum(values) / len(values)
                    metrics[f"{key}.max"] = max(values)
                    metrics[f"{key}.min"] = min(values)

            return metrics

    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.counters.clear()
            self.timers.clear()

# Usage
metrics_processor = MetricsProcessor()

# Later, export metrics
metrics = metrics_processor.get_metrics()
logger.info("metrics_export", metrics=metrics)
```

## Error Handling

### Safe Processor Wrapper

Wrap processors to handle errors gracefully:

```python
from provide.foundation import logger

def safe_processor(processor_func):
    """Wrap a processor to handle errors safely."""
    def wrapper(logger_instance, method_name, event_dict):
        try:
            return processor_func(logger_instance, method_name, event_dict)
        except Exception as e:
            # Log the error but don't break logging
            event_dict["processor_error"] = str(e)
            event_dict["failed_processor"] = processor_func.__name__
            return event_dict

    wrapper.__name__ = processor_func.__name__
    return wrapper

# Usage
@safe_processor
def risky_processor(logger_instance, method_name, event_dict):
    """Processor that might fail."""
    # Risky operation
    external_data = fetch_from_api()  # Could fail
    event_dict["external_data"] = external_data
    return event_dict
```

## Processor Ordering

### Order Matters

Processors run in the order they're defined:

```python
from provide.foundation import get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def add_timestamp(logger_instance, method_name, event_dict):
    """Add timestamp first."""
    import time
    event_dict["timestamp"] = time.time()
    return event_dict

def format_timestamp(logger_instance, method_name, event_dict):
    """Format timestamp (requires timestamp field)."""
    if "timestamp" in event_dict:
        from datetime import datetime
        ts = datetime.fromtimestamp(event_dict["timestamp"])
        event_dict["timestamp"] = ts.isoformat()
    return event_dict

def add_severity(logger_instance, method_name, event_dict):
    """Add severity based on method name."""
    severity_map = {
        "debug": 10,
        "info": 20,
        "warning": 30,
        "error": 40,
        "critical": 50
    }
    event_dict["severity"] = severity_map.get(method_name, 0)
    return event_dict

# Correct order: timestamp → format → severity
processors = [
    add_timestamp,       # Runs first
    format_timestamp,    # Needs timestamp
    add_severity,        # Independent
]

hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name="app",
        logging=LoggingConfig(processors=processors)
    )
)
```

## Testing Custom Processors

### Unit Testing

```python
import pytest
from provide.testkit import FoundationTestCase

class TestCustomProcessors(FoundationTestCase):
    """Test custom log processors."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        super().setup_method()

    def test_add_hostname_processor(self) -> None:
        """Test hostname processor."""
        event_dict = {"event": "test"}

        result = add_hostname_processor(None, "info", event_dict)

        assert "hostname" in result
        assert isinstance(result["hostname"], str)

    def test_sanitize_processor(self) -> None:
        """Test sanitization processor."""
        event_dict = {
            "event": "user_created",
            "email": "user@example.com",
            "password": "secret123",
            "user_id": "123"
        }

        result = sanitize_sensitive_data_processor(None, "info", event_dict)

        # Password should be redacted
        assert result["password"] == "***REDACTED***"

        # Email should be masked
        assert "@" not in result["email"] or "***" in result["email"]

        # user_id should be unchanged
        assert result["user_id"] == "123"

    def test_conditional_processor(self) -> None:
        """Test conditional processing."""
        error_dict = {"event": "error_occurred"}
        info_dict = {"event": "info_message"}

        # Should add context for errors
        error_result = error_only_enrichment(None, "error", error_dict)
        assert "severity" in error_result

        # Should not modify info logs
        info_result = error_only_enrichment(None, "info", info_dict)
        assert "severity" not in info_result
```

### Integration Testing

```python
from provide.foundation import logger, get_hub
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.testkit import set_log_stream_for_testing
import io

def test_processor_integration():
    """Test processors in logging pipeline."""
    # Create test stream
    stream = io.StringIO()
    set_log_stream_for_testing(stream)

    # Configure with custom processor
    hub = get_hub()
    hub.initialize_foundation(
        TelemetryConfig(
            service_name="test",
            logging=LoggingConfig(
                processors=[add_hostname_processor],
                log_format="json"
            )
        )
    )

    # Log something
    logger.info("test_event", key="value")

    # Check output
    output = stream.getvalue()
    assert "hostname" in output
    assert "test_event" in output
```

## Best Practices

### ✅ DO: Keep Processors Fast

```python
# ✅ GOOD: Fast, synchronous processor
def add_request_id(logger_instance, method_name, event_dict):
    """Add request ID from context."""
    event_dict["request_id"] = request_context.get("request_id", "none")
    return event_dict
```

### ❌ DON'T: Block in Processors

```python
# ❌ BAD: Blocking I/O in processor
def slow_processor(logger_instance, method_name, event_dict):
    """Don't do expensive operations!"""
    user_data = requests.get(f"https://api.example.com/users/{user_id}").json()
    event_dict["user_data"] = user_data  # Blocks logging!
    return event_dict

# ✅ GOOD: Use cached or async approach
cache = {}
def fast_processor(logger_instance, method_name, event_dict):
    """Use cached data."""
    user_id = event_dict.get("user_id")
    if user_id in cache:
        event_dict["user_name"] = cache[user_id]
    return event_dict
```

### ✅ DO: Handle Missing Fields Gracefully

```python
# ✅ GOOD: Check before accessing
def safe_enrichment(logger_instance, method_name, event_dict):
    """Safely enrich with optional fields."""
    user_id = event_dict.get("user_id")

    if user_id:
        event_dict["user_context"] = get_user_context(user_id)

    return event_dict
```

### ❌ DON'T: Mutate Original Objects

```python
# ❌ BAD: Mutating passed objects
def bad_processor(logger_instance, method_name, event_dict):
    """Don't mutate objects from event_dict!"""
    if "config" in event_dict:
        event_dict["config"]["modified"] = True  # Mutates original!
    return event_dict

# ✅ GOOD: Copy if you need to modify
def good_processor(logger_instance, method_name, event_dict):
    """Copy before modifying."""
    if "config" in event_dict:
        event_dict["config"] = {**event_dict["config"], "modified": True}
    return event_dict
```

### ✅ DO: Use Processor Classes for State

```python
# ✅ GOOD: Class-based processor with state
class CountingProcessor:
    """Processor with state."""

    def __init__(self):
        self.count = 0

    def __call__(self, logger_instance, method_name, event_dict):
        """Add counter to events."""
        self.count += 1
        event_dict["log_number"] = self.count
        return event_dict

processor = CountingProcessor()
```

### ❌ DON'T: Raise Exceptions Without Handling

```python
# ❌ BAD: Unhandled exceptions break logging
def unsafe_processor(logger_instance, method_name, event_dict):
    """Might break logging!"""
    required_field = event_dict["required"]  # KeyError if missing!
    return event_dict

# ✅ GOOD: Handle errors gracefully
def safe_processor(logger_instance, method_name, event_dict):
    """Handles errors properly."""
    try:
        required_field = event_dict["required"]
    except KeyError:
        event_dict["error"] = "missing_required_field"
    return event_dict
```

### ✅ DO: Document Processor Behavior

```python
# ✅ GOOD: Well-documented processor
def add_trace_context(logger_instance, method_name, event_dict):
    """Add distributed tracing context to log events.

    Adds the following fields if available in context:
    - trace_id: Unique identifier for the trace
    - span_id: Unique identifier for this span
    - parent_span_id: Parent span identifier

    Requires trace context to be set via contextvars.
    """
    from provide.foundation.tracer.context import get_current_trace

    trace = get_current_trace()
    if trace:
        event_dict.update({
            "trace_id": trace.trace_id,
            "span_id": trace.span_id,
            "parent_span_id": trace.parent_span_id
        })

    return event_dict
```

### ❌ DON'T: Log Inside Processors

```python
# ❌ BAD: Logging in a processor creates recursion risk
def logging_processor(logger_instance, method_name, event_dict):
    """Don't log in processors!"""
    logger.info("processing_event")  # Can cause infinite recursion!
    return event_dict

# ✅ GOOD: Use print for debugging or external logging
def debug_processor(logger_instance, method_name, event_dict):
    """Debug processor output."""
    if os.getenv("DEBUG_PROCESSORS"):
        print(f"Processing: {event_dict.get('event')}", file=sys.stderr)
    return event_dict
```

### ✅ DO: Test Processor Performance

```python
# ✅ GOOD: Benchmark processor performance
import time

def benchmark_processor(processor_func, iterations=1000):
    """Benchmark a processor."""
    event_dict = {"event": "test", "data": "sample"}

    start = time.time()
    for _ in range(iterations):
        processor_func(None, "info", event_dict.copy())
    duration = time.time() - start

    avg_ms = (duration / iterations) * 1000
    print(f"{processor_func.__name__}: {avg_ms:.4f}ms per call")

# Usage
benchmark_processor(add_hostname_processor)
benchmark_processor(sanitize_sensitive_data_processor)
```

### ❌ DON'T: Store Large Data in Events

```python
# ❌ BAD: Adding large data to every log
def bad_context_processor(logger_instance, method_name, event_dict):
    """Don't add huge objects!"""
    event_dict["entire_request_body"] = huge_json_blob  # Too large!
    return event_dict

# ✅ GOOD: Add summaries or IDs
def good_context_processor(logger_instance, method_name, event_dict):
    """Add summary data only."""
    event_dict["request_size"] = len(huge_json_blob)
    event_dict["request_hash"] = hashlib.sha256(huge_json_blob).hexdigest()[:8]
    return event_dict
```

### ✅ DO: Use Sampling for High-Volume Logs

```python
# ✅ GOOD: Sample verbose debug logs
import random

def sampling_processor(logger_instance, method_name, event_dict):
    """Sample debug logs at 1%."""
    if method_name == "debug" and random.random() > 0.01:
        from structlog.exceptions import DropEvent
        raise DropEvent
    return event_dict
```

## Next Steps

### Related Guides
- **[Structured Events](structured-events.md)**: Learn event naming conventions
- **[Basic Logging](basic-logging.md)**: Foundation logging basics
- **[Exception Logging](exception-logging.md)**: Log and handle exceptions

### Examples
- See `examples/telemetry/03_custom_processors.py` for processor examples
- See `examples/production/07_log_pipeline.py` for production patterns

### API Reference
- **[Processors API](../../reference/provide/foundation/logger/processors/index.md)**: Built-in processors
- **[Logger Config](../../reference/provide/foundation/logger/config/index.md)**: Configuration options

---

**Tip**: Keep processors fast and focused on a single concern. Use processor chaining to build complex pipelines from simple, testable components. Always handle errors gracefully to avoid breaking the logging pipeline.
