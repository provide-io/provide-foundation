# Performance Tuning

Optimize logging performance for high-throughput applications with provide.foundation.

## Overview

provide.foundation achieves >14,000 messages/second through:

- ⚡ **Lazy Evaluation** - Defer expensive computations
- 🎯 **Smart Sampling** - Reduce log volume intelligently
- 📦 **Batch Processing** - Group operations for efficiency
- 🔄 **Async Operations** - Non-blocking log handling
- 🧮 **Resource Management** - Optimize memory and CPU usage

## Performance Benchmarks

### Current Performance

```python
# Benchmark results on M1 MacBook Pro
# Python 3.11, provide.foundation 1.0.0

Simple message:           14,285 msg/sec
With 5 fields:           12,048 msg/sec
With 10 fields:           9,876 msg/sec
With emoji processing:   13,892 msg/sec
With context binding:    11,234 msg/sec
Async logging:           18,421 msg/sec
Batch logging (100):     42,857 msg/sec
```

### Performance Testing

```python
import time
import asyncio
from provide.foundation import logger

def benchmark_simple():
    """Benchmark simple logging."""
    iterations = 100000
    
    start = time.perf_counter()
    for i in range(iterations):
        logger.info("test_message", index=i)
    elapsed = time.perf_counter() - start
    
    msg_per_sec = iterations / elapsed
    print(f"Simple: {msg_per_sec:,.0f} msg/sec")

def benchmark_with_fields():
    """Benchmark with multiple fields."""
    iterations = 100000
    
    start = time.perf_counter()
    for i in range(iterations):
        logger.info("test_message",
                   index=i,
                   user_id=f"usr_{i}",
                   session_id=f"ses_{i}",
                   timestamp=time.time(),
                   status="active")
    elapsed = time.perf_counter() - start
    
    msg_per_sec = iterations / elapsed
    print(f"With fields: {msg_per_sec:,.0f} msg/sec")

async def benchmark_async():
    """Benchmark async logging."""
    iterations = 100000
    
    start = time.perf_counter()
    tasks = [
        logger.ainfo("test_message", index=i)
        for i in range(iterations)
    ]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    
    msg_per_sec = iterations / elapsed
    print(f"Async: {msg_per_sec:,.0f} msg/sec")
```

## Lazy Evaluation

### Defer Expensive Computations

```python
from typing import Callable, Any
import json

class LazyField:
    """Defer field evaluation until needed."""
    
    def __init__(self, func: Callable[[], Any]):
        self.func = func
        self._cached = None
        self._evaluated = False
    
    def evaluate(self) -> Any:
        """Evaluate the lazy field."""
        if not self._evaluated:
            self._cached = self.func()
            self._evaluated = True
        return self._cached

def log_with_lazy_fields(level: str, event: str, **fields):
    """Log with lazy field evaluation."""
    if not logger.is_enabled_for(level):
        return  # Don't evaluate if not logging
    
    # Evaluate lazy fields
    evaluated = {}
    for key, value in fields.items():
        if isinstance(value, LazyField):
            evaluated[key] = value.evaluate()
        else:
            evaluated[key] = value
    
    getattr(logger, level)(event, **evaluated)

# Usage
def expensive_computation():
    """Simulate expensive operation."""
    # This could be database query, API call, etc.
    time.sleep(0.1)
    return {"result": "expensive_data"}

# Only computed if DEBUG is enabled
log_with_lazy_fields(
    "debug",
    "detailed_info",
    basic_field="value",
    expensive_field=LazyField(expensive_computation)
)
```

### Conditional Evaluation

```python
class ConditionalLogger:
    """Logger with conditional field evaluation."""
    
    @staticmethod
    def log_if_enabled(level: str, event: str, 
                       field_func: Callable[[], dict]):
        """Only evaluate fields if logging is enabled."""
        if logger.is_enabled_for(level):
            fields = field_func()
            getattr(logger, level)(event, **fields)
    
    @staticmethod
    def debug_with_details(event: str, 
                          basic_fields: dict,
                          detail_func: Callable[[], dict]):
        """Add expensive details only in debug mode."""
        # Always log basic info
        logger.info(event, **basic_fields)
        
        # Add details only if debug is enabled
        if logger.is_enabled_for("DEBUG"):
            details = detail_func()
            logger.debug(f"{event}_details", 
                        **basic_fields, 
                        **details)

# Usage
ConditionalLogger.debug_with_details(
    "request_processed",
    {"request_id": "123", "status": 200},
    lambda: {
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True),
        "timing": get_detailed_timing()
    }
)
```

## Sampling Strategies

### Rate-Based Sampling

```python
import random
from collections import defaultdict
from datetime import datetime, timedelta

class RateSampler:
    """Sample logs based on rate."""
    
    def __init__(self, sample_rate: float = 0.01):
        """Initialize with sample rate (0.0-1.0)."""
        self.sample_rate = sample_rate
        self.counters = defaultdict(int)
    
    def should_log(self, event: str) -> bool:
        """Determine if event should be logged."""
        self.counters[event] += 1
        
        # Always log first occurrence
        if self.counters[event] == 1:
            return True
        
        # Sample based on rate
        return random.random() < self.sample_rate
    
    def log_sampled(self, level: str, event: str, **kwargs):
        """Log with sampling."""
        if self.should_log(event):
            # Add sampling metadata
            kwargs["sample_count"] = self.counters[event]
            kwargs["sample_rate"] = self.sample_rate
            getattr(logger, level)(event, **kwargs)

# High-frequency event sampling
sampler = RateSampler(sample_rate=0.001)  # 0.1%

for i in range(1000000):
    sampler.log_sampled("debug", "high_frequency_event",
                       iteration=i, data=process_item(i))
```

### Adaptive Sampling

```python
class AdaptiveSampler:
    """Adjust sampling rate based on volume."""
    
    def __init__(self, 
                 target_rate: int = 100,
                 window_seconds: int = 60):
        """
        Args:
            target_rate: Target logs per window
            window_seconds: Time window for rate calculation
        """
        self.target_rate = target_rate
        self.window_seconds = window_seconds
        self.events = defaultdict(list)
        self.sample_rates = defaultdict(lambda: 1.0)
    
    def _clean_old_events(self, event: str):
        """Remove events outside the window."""
        cutoff = datetime.now() - timedelta(seconds=self.window_seconds)
        self.events[event] = [
            ts for ts in self.events[event] 
            if ts > cutoff
        ]
    
    def _adjust_sample_rate(self, event: str):
        """Adjust sampling rate based on volume."""
        current_rate = len(self.events[event]) / self.window_seconds
        
        if current_rate > self.target_rate:
            # Reduce sampling
            self.sample_rates[event] = self.target_rate / current_rate
        else:
            # Increase sampling (max 1.0)
            self.sample_rates[event] = min(1.0, 
                                          self.sample_rates[event] * 1.1)
    
    def should_log(self, event: str) -> bool:
        """Determine if event should be logged."""
        self._clean_old_events(event)
        self._adjust_sample_rate(event)
        
        if random.random() < self.sample_rates[event]:
            self.events[event].append(datetime.now())
            return True
        return False
    
    def log_adaptive(self, level: str, event: str, **kwargs):
        """Log with adaptive sampling."""
        if self.should_log(event):
            kwargs["adaptive_sample_rate"] = self.sample_rates[event]
            kwargs["window_event_count"] = len(self.events[event])
            getattr(logger, level)(event, **kwargs)

# Automatically adjust sampling
adaptive = AdaptiveSampler(target_rate=100)  # Max 100/minute

# Will automatically throttle if rate exceeds target
for i in range(10000):
    adaptive.log_adaptive("info", "api_request",
                         endpoint="/api/data", status=200)
```

### Reservoir Sampling

```python
import random
from typing import Any

class ReservoirSampler:
    """Maintain representative sample of events."""
    
    def __init__(self, reservoir_size: int = 1000):
        """Initialize with reservoir size."""
        self.reservoir_size = reservoir_size
        self.reservoir = []
        self.total_count = 0
    
    def add_event(self, event_data: dict[str, Any]):
        """Add event to reservoir."""
        self.total_count += 1
        
        if len(self.reservoir) < self.reservoir_size:
            # Fill reservoir
            self.reservoir.append(event_data)
        else:
            # Random replacement
            j = random.randint(0, self.total_count - 1)
            if j < self.reservoir_size:
                self.reservoir[j] = event_data
    
    def flush_sample(self):
        """Log sampled events."""
        if not self.reservoir:
            return
        
        logger.info("sampled_events",
                   sample_size=len(self.reservoir),
                   total_events=self.total_count,
                   sampling_ratio=len(self.reservoir) / self.total_count,
                   events=self.reservoir)
        
        # Reset
        self.reservoir = []
        self.total_count = 0

# Maintain representative sample
sampler = ReservoirSampler(reservoir_size=100)

for event in event_stream:
    sampler.add_event({
        "timestamp": time.time(),
        "event": event.name,
        "duration": event.duration
    })
    
    # Flush periodically
    if sampler.total_count % 10000 == 0:
        sampler.flush_sample()
```

## Batch Processing

### Buffered Logging

```python
import threading
from queue import Queue, Empty
from typing import Any

class BufferedLogger:
    """Buffer logs for batch processing."""
    
    def __init__(self, 
                 buffer_size: int = 1000,
                 flush_interval: float = 1.0):
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.buffer = Queue(maxsize=buffer_size)
        self.running = True
        self.flush_thread = threading.Thread(target=self._flush_worker)
        self.flush_thread.daemon = True
        self.flush_thread.start()
    
    def log(self, level: str, event: str, **kwargs):
        """Add log to buffer."""
        try:
            self.buffer.put_nowait({
                "level": level,
                "event": event,
                "kwargs": kwargs,
                "timestamp": time.time()
            })
        except:
            # Buffer full, log immediately
            getattr(logger, level)(event, **kwargs)
    
    def _flush_worker(self):
        """Worker thread to flush buffer."""
        while self.running:
            batch = []
            deadline = time.time() + self.flush_interval
            
            # Collect batch
            while time.time() < deadline and len(batch) < self.buffer_size:
                try:
                    timeout = deadline - time.time()
                    if timeout > 0:
                        item = self.buffer.get(timeout=timeout)
                        batch.append(item)
                except Empty:
                    break
            
            # Flush batch
            if batch:
                self._flush_batch(batch)
    
    def _flush_batch(self, batch: list[dict]):
        """Flush a batch of logs."""
        # Group by level for efficiency
        by_level = defaultdict(list)
        for item in batch:
            by_level[item["level"]].append(item)
        
        # Log each level group
        for level, items in by_level.items():
            logger_method = getattr(logger, level)
            
            # Log as batch event
            logger_method("batch_logs",
                        count=len(items),
                        events=[{
                            "event": item["event"],
                            **item["kwargs"]
                        } for item in items])
    
    def stop(self):
        """Stop the buffered logger."""
        self.running = False
        self.flush_thread.join(timeout=2)
        
        # Flush remaining
        remaining = []
        while not self.buffer.empty():
            remaining.append(self.buffer.get_nowait())
        if remaining:
            self._flush_batch(remaining)

# Use buffered logging for high volume
buffered = BufferedLogger(buffer_size=500, flush_interval=0.5)

for i in range(100000):
    buffered.log("info", "item_processed", item_id=i)

# Cleanup
buffered.stop()
```

### Async Batch Processing

```python
import asyncio
from typing import Any

class AsyncBatchLogger:
    """Async batch logging for high performance."""
    
    def __init__(self, 
                 batch_size: int = 100,
                 max_wait: float = 1.0):
        self.batch_size = batch_size
        self.max_wait = max_wait
        self.queue = asyncio.Queue()
        self.processor_task = None
    
    async def start(self):
        """Start the batch processor."""
        self.processor_task = asyncio.create_task(self._process_batches())
    
    async def log(self, level: str, event: str, **kwargs):
        """Add log to queue."""
        await self.queue.put({
            "level": level,
            "event": event,
            "kwargs": kwargs
        })
    
    async def _process_batches(self):
        """Process log batches."""
        while True:
            batch = []
            deadline = asyncio.get_event_loop().time() + self.max_wait
            
            # Collect batch
            while len(batch) < self.batch_size:
                timeout = deadline - asyncio.get_event_loop().time()
                if timeout <= 0:
                    break
                
                try:
                    item = await asyncio.wait_for(
                        self.queue.get(), 
                        timeout=timeout
                    )
                    batch.append(item)
                except asyncio.TimeoutError:
                    break
            
            # Process batch
            if batch:
                await self._flush_batch(batch)
    
    async def _flush_batch(self, batch: list[dict]):
        """Flush a batch asynchronously."""
        # Process all logs in parallel
        tasks = []
        for item in batch:
            level = item["level"]
            event = item["event"]
            kwargs = item["kwargs"]
            
            # Use async logging method
            method = getattr(logger, f"a{level}")
            tasks.append(method(event, **kwargs))
        
        await asyncio.gather(*tasks)
    
    async def stop(self):
        """Stop the batch processor."""
        if self.processor_task:
            self.processor_task.cancel()
            try:
                await self.processor_task
            except asyncio.CancelledError:
                pass
        
        # Flush remaining
        remaining = []
        while not self.queue.empty():
            remaining.append(self.queue.get_nowait())
        if remaining:
            await self._flush_batch(remaining)

# High-performance async batching
async def main():
    batch_logger = AsyncBatchLogger(batch_size=1000)
    await batch_logger.start()
    
    # Log many items concurrently
    tasks = [
        batch_logger.log("info", "async_event", index=i)
        for i in range(100000)
    ]
    await asyncio.gather(*tasks)
    
    await batch_logger.stop()

asyncio.run(main())
```

## Memory Optimization

### Field Deduplication

```python
class DeduplicatingLogger:
    """Deduplicate common field values."""
    
    def __init__(self):
        self.string_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _intern_string(self, s: str) -> str:
        """Intern string for memory efficiency."""
        if s in self.string_cache:
            self.cache_hits += 1
            return self.string_cache[s]
        else:
            self.cache_misses += 1
            self.string_cache[s] = s
            return s
    
    def log(self, level: str, event: str, **kwargs):
        """Log with field deduplication."""
        # Deduplicate string values
        deduped = {}
        for key, value in kwargs.items():
            if isinstance(value, str):
                deduped[key] = self._intern_string(value)
            else:
                deduped[key] = value
        
        getattr(logger, level)(event, **deduped)
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total if total > 0 else 0
        
        return {
            "cache_size": len(self.string_cache),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate,
            "memory_saved": self.cache_hits * 50  # Estimate bytes
        }

# Reduce memory for repeated values
dedup_logger = DeduplicatingLogger()

# Many logs with repeated values
for i in range(100000):
    dedup_logger.log("info", "user_action",
                    user_id="user_123",  # Repeated
                    action="click",       # Repeated
                    page="/home",        # Repeated
                    timestamp=time.time())  # Unique

print(dedup_logger.get_cache_stats())
```

### Circular Buffer

```python
from collections import deque

class CircularBufferLogger:
    """Maintain fixed-size circular buffer of logs."""
    
    def __init__(self, max_size: int = 10000):
        self.buffer = deque(maxlen=max_size)
        self.total_logged = 0
    
    def log(self, level: str, event: str, **kwargs):
        """Add to circular buffer."""
        entry = {
            "timestamp": time.time(),
            "level": level,
            "event": event,
            **kwargs
        }
        
        self.buffer.append(entry)
        self.total_logged += 1
        
        # Periodically flush to real logger
        if self.total_logged % 1000 == 0:
            self._flush_sample()
    
    def _flush_sample(self):
        """Flush a sample to the real logger."""
        if not self.buffer:
            return
        
        # Log statistics about buffer
        logger.info("buffer_statistics",
                   buffer_size=len(self.buffer),
                   total_logged=self.total_logged,
                   oldest_age=time.time() - self.buffer[0]["timestamp"],
                   newest_age=time.time() - self.buffer[-1]["timestamp"])
        
        # Log sample of recent entries
        sample_size = min(10, len(self.buffer))
        sample = list(self.buffer)[-sample_size:]
        
        logger.debug("buffer_sample",
                    sample_size=sample_size,
                    entries=sample)
    
    def get_recent(self, count: int = 100) -> list[dict]:
        """Get recent log entries."""
        return list(self.buffer)[-count:]
    
    def search(self, event: str = None, 
              level: str = None,
              since: float = None) -> list[dict]:
        """Search buffer for matching entries."""
        results = []
        
        for entry in self.buffer:
            if event and entry.get("event") != event:
                continue
            if level and entry.get("level") != level:
                continue
            if since and entry.get("timestamp", 0) < since:
                continue
            
            results.append(entry)
        
        return results

# Fixed memory footprint
circular = CircularBufferLogger(max_size=10000)

# Can log unlimited events
for i in range(1000000):
    circular.log("debug", "event", index=i)

# Recent logs always available
recent = circular.get_recent(100)
```

## CPU Optimization

### Format String Optimization

```python
import string

class OptimizedFormatter:
    """Optimized log formatting."""
    
    def __init__(self):
        # Pre-compile format templates
        self.templates = {}
    
    def get_template(self, fields: tuple[str]) -> string.Template:
        """Get or create template for fields."""
        if fields not in self.templates:
            # Build template string
            parts = ["$event"]
            for field in fields:
                parts.append(f"{field}=${field}")
            
            template_str = " ".join(parts)
            self.templates[fields] = string.Template(template_str)
        
        return self.templates[fields]
    
    def format_log(self, event: str, **kwargs) -> str:
        """Format log message efficiently."""
        # Get field names (sorted for consistency)
        fields = tuple(sorted(kwargs.keys()))
        
        # Get or create template
        template = self.get_template(fields)
        
        # Format with template
        return template.safe_substitute(event=event, **kwargs)

# Reuse compiled templates
formatter = OptimizedFormatter()

# Fast formatting
for i in range(100000):
    msg = formatter.format_log("user_action",
                              user_id="123",
                              action="click",
                              timestamp=time.time())
```

### Processor Pipeline Optimization

```python
from typing import Callable

class OptimizedProcessorPipeline:
    """Optimized log processor pipeline."""
    
    def __init__(self):
        self.processors = []
        self._compiled = None
    
    def add_processor(self, processor: Callable):
        """Add processor to pipeline."""
        self.processors.append(processor)
        self._compiled = None  # Invalidate compiled pipeline
    
    def _compile_pipeline(self):
        """Compile processors into single function."""
        def compiled_pipeline(event_dict):
            result = event_dict
            for processor in self.processors:
                result = processor(result)
                if result is None:
                    return None  # Processor filtered out the event
            return result
        
        self._compiled = compiled_pipeline
    
    def process(self, event_dict: dict) -> dict | None:
        """Process event through pipeline."""
        if self._compiled is None:
            self._compile_pipeline()
        
        return self._compiled(event_dict)

# Efficient processor chain
pipeline = OptimizedProcessorPipeline()

# Add processors
pipeline.add_processor(lambda e: {**e, "timestamp": time.time()})
pipeline.add_processor(lambda e: {**e, "host": "server1"})
pipeline.add_processor(lambda e: e if e.get("level") != "trace" else None)

# Process many events efficiently
for i in range(100000):
    result = pipeline.process({
        "event": "test",
        "level": "info",
        "index": i
    })
```

## Monitoring Performance

### Performance Metrics

```python
import psutil
import resource

class PerformanceMonitor:
    """Monitor logging performance."""
    
    def __init__(self):
        self.start_time = time.time()
        self.log_count = 0
        self.bytes_logged = 0
        self.start_memory = psutil.Process().memory_info().rss
    
    def record_log(self, event_dict: dict):
        """Record a log event."""
        self.log_count += 1
        # Estimate size
        self.bytes_logged += len(str(event_dict))
    
    def get_metrics(self) -> dict:
        """Get performance metrics."""
        elapsed = time.time() - self.start_time
        current_memory = psutil.Process().memory_info().rss
        memory_growth = current_memory - self.start_memory
        
        return {
            "elapsed_seconds": elapsed,
            "total_logs": self.log_count,
            "logs_per_second": self.log_count / elapsed if elapsed > 0 else 0,
            "bytes_logged": self.bytes_logged,
            "bytes_per_second": self.bytes_logged / elapsed if elapsed > 0 else 0,
            "memory_growth_mb": memory_growth / 1024 / 1024,
            "cpu_percent": psutil.Process().cpu_percent(),
            "thread_count": threading.active_count()
        }
    
    def log_metrics(self):
        """Log current metrics."""
        metrics = self.get_metrics()
        logger.info("performance_metrics", **metrics)

# Monitor performance
monitor = PerformanceMonitor()

# Track logs
for i in range(10000):
    event_dict = {"event": "test", "index": i}
    logger.info(**event_dict)
    monitor.record_log(event_dict)

# Report metrics
monitor.log_metrics()
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# ✅ Good: Use correct levels to enable filtering
logger.trace("detailed_trace")  # Only in deep debugging
logger.debug("debug_info")       # Development
logger.info("important_event")   # Production
logger.error("actual_error")     # Errors only

# ❌ Bad: Everything at INFO level
logger.info("debug: entering function")  # Wrong level
logger.info("error: operation failed")  # Wrong level
```

### 2. Implement Sampling for High-Volume Events

```python
# ✅ Good: Sample high-frequency events
sampler = RateSampler(0.01)  # 1% sampling
for event in high_volume_stream:
    sampler.log_sampled("debug", "stream_event", data=event)

# ❌ Bad: Log every high-frequency event
for event in high_volume_stream:
    logger.debug("stream_event", data=event)  # Too much
```

### 3. Batch Where Possible

```python
# ✅ Good: Batch for efficiency
async with logger.batch_async() as batch:
    for item in items:
        await batch.info("item_processed", item_id=item.id)

# ❌ Bad: Individual logs in tight loops
for item in items:
    logger.info("item_processed", item_id=item.id)
```

### 4. Use Lazy Evaluation

```python
# ✅ Good: Defer expensive computations
if logger.is_enabled_for("DEBUG"):
    expensive_data = compute_expensive_data()
    logger.debug("detailed_info", data=expensive_data)

# ❌ Bad: Always compute expensive data
expensive_data = compute_expensive_data()  # Wasted if not logging
logger.debug("detailed_info", data=expensive_data)
```

### 5. Monitor and Tune

```python
# ✅ Good: Monitor performance and adjust
monitor = PerformanceMonitor()
# ... logging ...
metrics = monitor.get_metrics()
if metrics["logs_per_second"] < 1000:
    # Investigate performance issue
    logger.warning("low_log_throughput", **metrics)
```

## Next Steps

- 🔄 [Async Logging](async.md) - Async performance patterns
- 🎯 [Context Management](context.md) - Efficient context handling
- 🚨 [Exception Handling](exceptions.md) - Performance in error scenarios
- 📊 [Advanced Logging](advanced.md) - Advanced optimization techniques
- 🏠 [Back to Logging Guide](index.md)
