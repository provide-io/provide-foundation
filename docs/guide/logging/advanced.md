# Advanced Logging

Advanced logging patterns, techniques, and optimizations for production systems.

## Overview

Advanced logging capabilities in provide.foundation include:

- 🎯 **Custom Processors** - Extend the logging pipeline
- 🔍 **Filtering & Routing** - Control log flow
- 📊 **Metrics Integration** - Log-based metrics
- 🌐 **Distributed Tracing** - Correlation across services
- 🔄 **Log Aggregation** - Centralized logging patterns

## Custom Processors

### Creating a Processor

```python
from provide.foundation.logger import Processor
from typing import Any

class RedactProcessor(Processor):
    """Redact sensitive information from logs."""
    
    def __init__(self, fields_to_redact: list[str]):
        self.fields_to_redact = fields_to_redact
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Process log event."""
        for field in self.fields_to_redact:
            if field in event_dict:
                event_dict[field] = "***REDACTED***"
        return event_dict

# Register processor
from provide.foundation import logger

logger.add_processor(RedactProcessor([
    "password", "api_key", "token", "secret"
]))

# Usage
logger.info("user_login", 
            username="john",
            password="secret123")  # Will be redacted
# Output: user_login username=john password=***REDACTED***
```

### Sampling Processor

```python
import random
from typing import Any

class SamplingProcessor(Processor):
    """Sample logs based on rate."""
    
    def __init__(self, sample_rate: float = 0.1):
        self.sample_rate = sample_rate
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any] | None:
        """Sample events based on rate."""
        # Always log errors
        if method_name in ["error", "critical"]:
            return event_dict
        
        # Sample other levels
        if random.random() < self.sample_rate:
            return event_dict
        
        return None  # Drop the log

# Use for high-frequency events
logger.add_processor(SamplingProcessor(0.01))  # 1% sampling
```

### Enrichment Processor

```python
import os
import socket
from datetime import datetime

class EnrichmentProcessor(Processor):
    """Add metadata to all logs."""
    
    def __init__(self):
        self.hostname = socket.gethostname()
        self.pid = os.getpid()
        self.service = os.getenv("PROVIDE_APP_NAME", "unknown")
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Enrich log with metadata."""
        event_dict.update({
            "hostname": self.hostname,
            "pid": self.pid,
            "service": self.service,
            "timestamp_ms": int(datetime.now().timestamp() * 1000)
        })
        return event_dict

logger.add_processor(EnrichmentProcessor())
```

## Filtering and Routing

### Level-Based Filtering

```python
from provide.foundation.logger import LevelFilter

class ErrorOnlyFilter(LevelFilter):
    """Only allow error and above."""
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> bool:
        return method_name in ["error", "critical"]

# Create filtered logger
error_logger = logger.filter(ErrorOnlyFilter())

# Only errors are logged
error_logger.info("This won't be logged")
error_logger.error("This will be logged")
```

### Event-Based Filtering

```python
class EventFilter:
    """Filter based on event patterns."""
    
    def __init__(self, include_patterns: list[str] = None, 
                 exclude_patterns: list[str] = None):
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> bool:
        event = event_dict.get("event", "")
        
        # Check exclusions first
        for pattern in self.exclude_patterns:
            if pattern in event:
                return False
        
        # Check inclusions
        if self.include_patterns:
            return any(pattern in event for pattern in self.include_patterns)
        
        return True

# Filter specific events
audit_logger = logger.filter(EventFilter(
    include_patterns=["audit_", "security_"],
    exclude_patterns=["debug_"]
))
```

### Multi-Handler Routing

```python
from provide.foundation.logger import Router, Handler

class FileHandler(Handler):
    """Write logs to file."""
    
    def __init__(self, filepath: str):
        self.file = open(filepath, 'a')
    
    def emit(self, event_dict: dict[str, Any]):
        self.file.write(json.dumps(event_dict) + '\n')
        self.file.flush()

class MetricsHandler(Handler):
    """Send logs to metrics system."""
    
    def emit(self, event_dict: dict[str, Any]):
        if "duration_ms" in event_dict:
            metrics.histogram("operation.duration", 
                            event_dict["duration_ms"])

# Route to multiple handlers
router = Router()
router.add_handler(FileHandler("/var/log/app.log"), 
                  filter=lambda e: e.get("level") >= "INFO")
router.add_handler(MetricsHandler(),
                  filter=lambda e: "metrics" in e)

logger.add_handler(router)
```

## Distributed Tracing

### Trace Context Propagation

```python
import uuid
from contextvars import ContextVar
from provide.foundation import logger

# Context variables for tracing
trace_id_var: ContextVar[str] = ContextVar('trace_id', default=None)
span_id_var: ContextVar[str] = ContextVar('span_id', default=None)

class TraceProcessor(Processor):
    """Add trace context to logs."""
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        trace_id = trace_id_var.get()
        span_id = span_id_var.get()
        
        if trace_id:
            event_dict["trace_id"] = trace_id
        if span_id:
            event_dict["span_id"] = span_id
        
        return event_dict

logger.add_processor(TraceProcessor())

# Usage
def handle_request(request):
    """Handle request with tracing."""
    # Set trace context
    trace_id = request.headers.get("X-Trace-Id") or str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    
    trace_id_var.set(trace_id)
    span_id_var.set(span_id)
    
    logger.info("request_started", 
                method=request.method,
                path=request.path)
    
    # All subsequent logs include trace_id and span_id
    process_request(request)
```

### Cross-Service Correlation

```python
import httpx
from provide.foundation import logger

async def call_service(url: str, data: dict):
    """Call another service with trace propagation."""
    
    # Get current trace context
    trace_id = trace_id_var.get() or str(uuid.uuid4())
    parent_span = span_id_var.get()
    span_id = str(uuid.uuid4())
    
    # Create child span
    span_id_var.set(span_id)
    
    headers = {
        "X-Trace-Id": trace_id,
        "X-Parent-Span": parent_span,
        "X-Span-Id": span_id
    }
    
    logger.info("service_call_started",
                url=url,
                trace_id=trace_id,
                span_id=span_id,
                parent_span=parent_span)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
    
    logger.info("service_call_completed",
                url=url,
                status=response.status_code,
                trace_id=trace_id,
                span_id=span_id)
    
    return response
```

## Performance Optimization

### Lazy Evaluation

```python
from provide.foundation import logger
from functools import partial

class LazyValue:
    """Defer expensive computations."""
    
    def __init__(self, func, *args, **kwargs):
        self.func = partial(func, *args, **kwargs)
        self._value = None
        self._computed = False
    
    def __str__(self):
        if not self._computed:
            self._value = self.func()
            self._computed = True
        return str(self._value)

def expensive_computation():
    """Expensive operation."""
    import time
    time.sleep(0.1)  # Simulate work
    return "computed_value"

# Only computed if DEBUG is enabled
logger.debug("debug_info",
            expensive_data=LazyValue(expensive_computation))
```

### Buffered Logging

```python
from collections import deque
import threading
import time

class BufferedLogger:
    """Buffer logs for batch processing."""
    
    def __init__(self, base_logger, buffer_size: int = 1000, 
                 flush_interval: float = 1.0):
        self.base_logger = base_logger
        self.buffer = deque(maxlen=buffer_size)
        self.lock = threading.Lock()
        self.flush_interval = flush_interval
        self._start_flusher()
    
    def log(self, level: str, event: str, **kwargs):
        """Add to buffer."""
        with self.lock:
            self.buffer.append({
                "level": level,
                "event": event,
                "timestamp": time.time(),
                **kwargs
            })
    
    def flush(self):
        """Flush buffer to base logger."""
        with self.lock:
            batch = list(self.buffer)
            self.buffer.clear()
        
        for entry in batch:
            level = entry.pop("level")
            getattr(self.base_logger, level)(**entry)
    
    def _start_flusher(self):
        """Start background flush thread."""
        def flusher():
            while True:
                time.sleep(self.flush_interval)
                self.flush()
        
        thread = threading.Thread(target=flusher, daemon=True)
        thread.start()

# Use for high-volume logging
buffered = BufferedLogger(logger)
for i in range(10000):
    buffered.log("info", "item_processed", item_id=i)
```

### Async Logging

```python
import asyncio
from asyncio import Queue

class AsyncLogger:
    """Asynchronous logging handler."""
    
    def __init__(self, base_logger):
        self.base_logger = base_logger
        self.queue: Queue = Queue(maxsize=10000)
        self.running = False
    
    async def start(self):
        """Start async processor."""
        self.running = True
        asyncio.create_task(self._processor())
    
    async def stop(self):
        """Stop async processor."""
        self.running = False
        await self.queue.join()
    
    async def log(self, level: str, event: str, **kwargs):
        """Queue log entry."""
        await self.queue.put({
            "level": level,
            "event": event,
            **kwargs
        })
    
    async def _processor(self):
        """Process queued logs."""
        while self.running:
            try:
                entry = await asyncio.wait_for(
                    self.queue.get(), 
                    timeout=1.0
                )
                level = entry.pop("level")
                getattr(self.base_logger, level)(**entry)
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue

# Usage
async def main():
    async_logger = AsyncLogger(logger)
    await async_logger.start()
    
    # Log asynchronously
    await async_logger.log("info", "async_operation", status="started")
    
    # Process work...
    
    await async_logger.stop()
```

## Metrics from Logs

### Log-Based Metrics

```python
from provide.foundation import logger
from collections import defaultdict
import time

class MetricsProcessor(Processor):
    """Extract metrics from logs."""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.histograms = defaultdict(list)
        self.gauges = {}
        self.last_flush = time.time()
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Extract metrics from log."""
        
        # Count events
        event = event_dict.get("event", "unknown")
        self.counters[f"log.{event}.count"] += 1
        
        # Track durations
        if "duration_ms" in event_dict:
            self.histograms[f"log.{event}.duration_ms"].append(
                event_dict["duration_ms"]
            )
        
        # Track gauges
        if "queue_size" in event_dict:
            self.gauges["queue.size"] = event_dict["queue_size"]
        
        # Flush periodically
        if time.time() - self.last_flush > 10:
            self.flush_metrics()
        
        return event_dict
    
    def flush_metrics(self):
        """Send metrics to monitoring system."""
        # Send to StatsD, Prometheus, etc.
        for name, value in self.counters.items():
            statsd.increment(name, value)
        
        for name, values in self.histograms.items():
            for value in values:
                statsd.histogram(name, value)
        
        for name, value in self.gauges.items():
            statsd.gauge(name, value)
        
        # Reset
        self.counters.clear()
        self.histograms.clear()
        self.last_flush = time.time()

logger.add_processor(MetricsProcessor())
```

### Performance Metrics

```python
from provide.foundation import logger
import psutil
import gc

class SystemMetricsLogger:
    """Log system metrics periodically."""
    
    def __init__(self, interval: float = 60.0):
        self.interval = interval
        self._start_monitoring()
    
    def _start_monitoring(self):
        """Start monitoring thread."""
        import threading
        
        def monitor():
            while True:
                self._log_metrics()
                time.sleep(self.interval)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def _log_metrics(self):
        """Log current system metrics."""
        process = psutil.Process()
        
        logger.info("system_metrics",
            cpu_percent=process.cpu_percent(),
            memory_mb=process.memory_info().rss / 1024 / 1024,
            threads=process.num_threads(),
            open_files=len(process.open_files()),
            gc_stats={
                f"gen{i}": gc.get_count()[i]
                for i in range(len(gc.get_count()))
            }
        )

# Start monitoring
SystemMetricsLogger(interval=30)
```

## Log Aggregation Patterns

### Structured Event Stream

```python
from provide.foundation import logger
import json
from datetime import datetime

class EventStream:
    """Structured event stream for aggregation."""
    
    def __init__(self, stream_name: str):
        self.stream_name = stream_name
        self.sequence = 0
    
    def emit(self, event_type: str, **data):
        """Emit structured event."""
        self.sequence += 1
        
        event = {
            "stream": self.stream_name,
            "sequence": self.sequence,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        logger.info("stream_event", **event)
        return event

# Usage
order_stream = EventStream("orders")

order_stream.emit("order_created", 
                 order_id="ord_123",
                 customer_id="cust_456",
                 total=99.99)

order_stream.emit("order_shipped",
                 order_id="ord_123",
                 carrier="fedex",
                 tracking="1234567890")
```

### Centralized Logging

```python
import httpx
import asyncio
from typing import Any

class CentralizedLogger:
    """Send logs to central aggregation service."""
    
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.batch = []
        self.batch_size = 100
        self.flush_interval = 5.0
        self._start_flusher()
    
    async def log(self, event_dict: dict[str, Any]):
        """Add log to batch."""
        self.batch.append(event_dict)
        
        if len(self.batch) >= self.batch_size:
            await self.flush()
    
    async def flush(self):
        """Send batch to aggregation service."""
        if not self.batch:
            return
        
        batch_to_send = self.batch[:self.batch_size]
        self.batch = self.batch[self.batch_size:]
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.endpoint,
                    json={"logs": batch_to_send},
                    headers={"X-API-Key": self.api_key}
                )
                response.raise_for_status()
            except Exception as e:
                logger.error("log_aggregation_failed",
                           error=str(e),
                           batch_size=len(batch_to_send))
    
    def _start_flusher(self):
        """Start background flush task."""
        async def flusher():
            while True:
                await asyncio.sleep(self.flush_interval)
                await self.flush()
        
        asyncio.create_task(flusher())

# Setup
central = CentralizedLogger(
    endpoint="https://logs.example.com/ingest",
    api_key=os.getenv("LOG_API_KEY")
)

# Add processor to send all logs
class CentralizedProcessor(Processor):
    def __init__(self, central_logger):
        self.central = central_logger
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        asyncio.create_task(self.central.log(event_dict))
        return event_dict

logger.add_processor(CentralizedProcessor(central))
```

## Security Logging

### Audit Trail

```python
from provide.foundation import logger
import hashlib
from datetime import datetime

class AuditLogger:
    """Tamper-resistant audit logging."""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.chain_hash = self._get_last_hash()
    
    def _get_last_hash(self) -> str:
        """Get hash of last log entry."""
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get("hash", "")
        except FileNotFoundError:
            pass
        return ""
    
    def log_audit_event(self, action: str, user: str, **details):
        """Log audit event with hash chain."""
        
        timestamp = datetime.utcnow().isoformat()
        
        # Create event
        event = {
            "timestamp": timestamp,
            "action": action,
            "user": user,
            "details": details,
            "previous_hash": self.chain_hash
        }
        
        # Calculate hash
        event_str = json.dumps(event, sort_keys=True)
        event_hash = hashlib.sha256(event_str.encode()).hexdigest()
        event["hash"] = event_hash
        
        # Update chain
        self.chain_hash = event_hash
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
        
        # Also log normally
        logger.info("audit_event",
                   action=action,
                   user=user,
                   hash=event_hash[:8],
                   **details)
        
        return event_hash

# Usage
audit = AuditLogger("/var/log/audit.jsonl")

audit.log_audit_event(
    action="user.permission.changed",
    user="admin@example.com",
    target_user="user@example.com",
    permission="admin",
    granted=True
)
```

### Security Event Detection

```python
from collections import defaultdict
import time

class SecurityMonitor(Processor):
    """Detect security events from logs."""
    
    def __init__(self):
        self.failed_logins = defaultdict(list)
        self.rate_limits = defaultdict(list)
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Monitor for security events."""
        
        event = event_dict.get("event", "")
        now = time.time()
        
        # Monitor failed logins
        if "login_failed" in event:
            user = event_dict.get("username", "unknown")
            self.failed_logins[user].append(now)
            
            # Check for brute force
            recent = [t for t in self.failed_logins[user] if now - t < 300]  # 5 min
            if len(recent) >= 5:
                logger.warning("security_alert",
                             alert_type="brute_force_detected",
                             username=user,
                             attempts=len(recent))
        
        # Monitor rate limits
        if "rate_limit_exceeded" in event:
            ip = event_dict.get("ip", "unknown")
            self.rate_limits[ip].append(now)
            
            # Check for abuse
            recent = [t for t in self.rate_limits[ip] if now - t < 60]  # 1 min
            if len(recent) >= 10:
                logger.warning("security_alert",
                             alert_type="rate_limit_abuse",
                             ip=ip,
                             violations=len(recent))
        
        return event_dict

logger.add_processor(SecurityMonitor())
```

## Error Tracking Integration

```python
import sentry_sdk
from provide.foundation import logger

class SentryProcessor(Processor):
    """Send errors to Sentry."""
    
    def __init__(self, dsn: str):
        sentry_sdk.init(dsn=dsn)
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        """Send errors to Sentry."""
        
        if method_name in ["error", "critical"]:
            # Extract error info
            error = event_dict.get("error")
            if isinstance(error, Exception):
                sentry_sdk.capture_exception(error)
            else:
                sentry_sdk.capture_message(
                    event_dict.get("event", "Unknown error"),
                    level=method_name,
                    extra=event_dict
                )
        
        return event_dict

# Setup
logger.add_processor(SentryProcessor(
    dsn=os.getenv("SENTRY_DSN")
))
```

## Best Practices

### 1. Processor Order Matters

```python
# Order processors correctly
logger.add_processor(EnrichmentProcessor())     # Add metadata first
logger.add_processor(RedactProcessor([...]))    # Then redact
logger.add_processor(SamplingProcessor(0.1))    # Then sample
logger.add_processor(CentralizedProcessor())    # Finally send
```

### 2. Fail Gracefully

```python
class ResilientProcessor(Processor):
    """Processor that doesn't break logging."""
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        try:
            # Risky processing
            return self.process(event_dict)
        except Exception as e:
            # Log the error but don't break
            logger.error("processor_failed", 
                        processor=self.__class__.__name__,
                        error=str(e))
            return event_dict  # Return unmodified
```

### 3. Monitor Performance

```python
class TimedProcessor(Processor):
    """Monitor processor performance."""
    
    def __init__(self, wrapped: Processor):
        self.wrapped = wrapped
        self.total_time = 0
        self.call_count = 0
    
    def __call__(self, logger, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        start = time.perf_counter()
        result = self.wrapped(logger, method_name, event_dict)
        elapsed = time.perf_counter() - start
        
        self.total_time += elapsed
        self.call_count += 1
        
        if self.call_count % 1000 == 0:
            avg_ms = (self.total_time / self.call_count) * 1000
            logger.debug("processor_performance",
                        processor=self.wrapped.__class__.__name__,
                        avg_ms=avg_ms,
                        total_calls=self.call_count)
        
        return result
```

## Next Steps

- 🔄 [Async Logging](async.md) - Asynchronous logging patterns
- 🎯 [Context Management](context.md) - Managing log context
- ⚠️ [Exception Handling](exceptions.md) - Exception logging
- ⚡ [Performance Tuning](performance.md) - Optimization techniques
- 📚 [Basic Logging](basic.md) - Fundamentals
- 🏠 [Back to Logging Guide](index.md)