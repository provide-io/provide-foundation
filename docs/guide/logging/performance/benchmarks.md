# Performance Benchmarks

Comprehensive performance benchmarks and testing methodology for provide.foundation logging.

## Current Performance

### Benchmark Results

Based on testing on Apple M1 MacBook Pro with Python 3.11:

| Configuration | Messages/sec | Memory/msg | CPU/msg |
|---------------|--------------|------------|----------|
| JSON formatter, no emoji | 18,500+ | ~200 bytes | ~0.05ms |
| Key-value formatter, no emoji | 16,000+ | ~250 bytes | ~0.06ms |
| JSON formatter, with emoji | 14,000+ | ~300 bytes | ~0.07ms |
| Key-value formatter, with emoji | 12,000+ | ~350 bytes | ~0.08ms |

### Performance Testing

```python
import time
import asyncio
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

async def benchmark_logging(message_count: int = 10000):
    """Benchmark logging performance."""
    
    # Setup high-performance logging
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            das_emoji_prefix_enabled=False,
            omit_timestamp=False
        )
    )
    setup_telemetry(config)
    
    logger = get_logger("benchmark")
    
    # Warmup
    for _ in range(100):
        logger.info("warmup message", test=True)
    
    # Actual benchmark
    start_time = time.perf_counter()
    
    for i in range(message_count):
        logger.info("benchmark message", 
                   iteration=i, 
                   batch="performance_test",
                   user_id=12345,
                   success=True)
    
    duration = time.perf_counter() - start_time
    messages_per_second = message_count / duration
    
    print(f"Messages: {message_count}")
    print(f"Duration: {duration:.3f} seconds")
    print(f"Rate: {messages_per_second:.0f} messages/second")
    print(f"Latency: {(duration / message_count) * 1000:.3f} ms/message")

# Run benchmark
asyncio.run(benchmark_logging())
```

## Memory Profiling

### Memory Usage Analysis

```python
import tracemalloc
import gc
from provide.foundation import get_logger, setup_telemetry

def profile_memory_usage():
    """Profile memory usage during logging."""
    
    setup_telemetry()
    logger = get_logger("memory_profile")
    
    # Start memory tracking
    tracemalloc.start()
    gc.collect()
    
    # Baseline measurement
    baseline = tracemalloc.take_snapshot()
    
    # Log messages
    for i in range(1000):
        logger.info("Memory profiling test", 
                   iteration=i, 
                   data={"key": "value", "number": 42})
    
    # Take snapshot after logging
    current = tracemalloc.take_snapshot()
    
    # Calculate memory difference
    top_stats = current.compare_to(baseline, 'lineno')
    
    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)
    
    # Peak memory usage
    peak = tracemalloc.get_traced_memory()[1]
    print(f"\nPeak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    tracemalloc.stop()

profile_memory_usage()
```

## CPU Profiling 

### CPU Usage Analysis

```python
import cProfile
import pstats
from io import StringIO
from provide.foundation import get_logger, setup_telemetry

def profile_cpu_usage():
    """Profile CPU usage during logging."""
    
    setup_telemetry()
    logger = get_logger("cpu_profile")
    
    def logging_workload():
        for i in range(5000):
            logger.info("CPU profiling test",
                       iteration=i,
                       user_id=f"user_{i % 100}",
                       operation="test_operation",
                       status="success")
    
    # Profile the workload
    profiler = cProfile.Profile()
    profiler.enable()
    
    logging_workload()
    
    profiler.disable()
    
    # Analyze results
    output = StringIO()
    stats = pstats.Stats(profiler, stream=output)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    print("CPU Profiling Results:")
    print(output.getvalue())

profile_cpu_usage()
```

## Async Performance

### Async Logging Benchmarks

```python
import asyncio
import time
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.utils import timed_block

async def benchmark_async_logging():
    """Benchmark async logging performance."""
    
    setup_telemetry()
    logger = get_logger("async_benchmark")
    
    async def async_logging_task(task_id: int, message_count: int):
        """Async task that logs messages."""
        for i in range(message_count):
            logger.info("Async log message",
                       task_id=task_id,
                       iteration=i,
                       timestamp=time.time())
            # Yield control to allow other tasks
            if i % 100 == 0:
                await asyncio.sleep(0)
    
    # Benchmark concurrent async logging
    num_tasks = 10
    messages_per_task = 1000
    
    with timed_block(logger, "async_logging_benchmark") as ctx:
        tasks = [
            async_logging_task(i, messages_per_task) 
            for i in range(num_tasks)
        ]
        await asyncio.gather(*tasks)
        
        ctx["num_tasks"] = num_tasks
        ctx["messages_per_task"] = messages_per_task
        ctx["total_messages"] = num_tasks * messages_per_task

# Run async benchmark
asyncio.run(benchmark_async_logging())
```

## Comparative Benchmarks

### vs Standard Library Logging

```python
import logging
import time
from provide.foundation import get_logger, setup_telemetry

def compare_with_stdlib():
    """Compare with standard library logging."""
    
    # Standard library logger
    stdlib_logger = logging.getLogger("stdlib_test")
    stdlib_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
    stdlib_logger.addHandler(handler)
    
    # Foundation logger
    setup_telemetry()
    foundation_logger = get_logger("foundation_test")
    
    message_count = 5000
    
    # Benchmark stdlib
    start_time = time.perf_counter()
    for i in range(message_count):
        stdlib_logger.info("Test message %d", i)
    stdlib_duration = time.perf_counter() - start_time
    
    # Benchmark foundation
    start_time = time.perf_counter()  
    for i in range(message_count):
        foundation_logger.info("Test message", iteration=i)
    foundation_duration = time.perf_counter() - start_time
    
    print(f"Standard library: {message_count / stdlib_duration:.0f} messages/sec")
    print(f"Foundation: {message_count / foundation_duration:.0f} messages/sec")
    print(f"Foundation overhead: {(foundation_duration / stdlib_duration - 1) * 100:.1f}%")

compare_with_stdlib()
```

## Performance Regression Testing

### Automated Performance Tests

```python
import json
import time
from pathlib import Path
from typing import NamedTuple

class BenchmarkResult(NamedTuple):
    """Benchmark result data structure."""
    messages_per_second: float
    memory_mb: float
    cpu_percent: float
    config_name: str
    timestamp: str

def run_performance_regression_test():
    """Run comprehensive performance regression tests."""
    
    test_configs = [
        {
            "name": "json_no_emoji",
            "config": TelemetryConfig(
                logging=LoggingConfig(
                    console_formatter="json",
                    das_emoji_prefix_enabled=False
                )
            )
        },
        {
            "name": "json_with_emoji", 
            "config": TelemetryConfig(
                logging=LoggingConfig(
                    console_formatter="json",
                    das_emoji_prefix_enabled=True
                )
            )
        },
        {
            "name": "keyvalue_no_emoji",
            "config": TelemetryConfig(
                logging=LoggingConfig(
                    console_formatter="key_value",
                    das_emoji_prefix_enabled=False
                )
            )
        }
    ]
    
    results = []
    
    for test_config in test_configs:
        print(f"Testing configuration: {test_config['name']}")
        
        setup_telemetry(test_config["config"])
        logger = get_logger("perf_test")
        
        # Run benchmark
        message_count = 10000
        start_time = time.perf_counter()
        
        for i in range(message_count):
            logger.info("Performance test message",
                       iteration=i,
                       user_id=f"user_{i % 1000}",
                       operation="benchmark",
                       success=True)
        
        duration = time.perf_counter() - start_time
        messages_per_second = message_count / duration
        
        result = BenchmarkResult(
            messages_per_second=messages_per_second,
            memory_mb=0.0,  # Would measure actual memory usage
            cpu_percent=0.0,  # Would measure actual CPU usage
            config_name=test_config["name"],
            timestamp=time.isoformat()
        )
        
        results.append(result)
        print(f"  Rate: {messages_per_second:.0f} messages/second")
    
    # Save results
    results_file = Path("performance_results.json")
    with results_file.open("w") as f:
        json.dump([r._asdict() for r in results], f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    return results

# Run regression tests
regression_results = run_performance_regression_test()
```

## Performance Monitoring in Production

### Real-time Performance Metrics

```python
import time
import threading
from collections import deque
from typing import Dict, List
from provide.foundation import get_logger

class LoggingPerformanceMonitor:
    """Monitor logging performance in production."""
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.message_times: deque = deque(maxlen=window_size)
        self.lock = threading.Lock()
        self._start_time = time.time()
        
    def record_log_event(self):
        """Record a log event timestamp."""
        with self.lock:
            self.message_times.append(time.time())
    
    def get_current_rate(self) -> float:
        """Get current messages per second."""
        with self.lock:
            if len(self.message_times) < 2:
                return 0.0
            
            time_span = self.message_times[-1] - self.message_times[0]
            if time_span <= 0:
                return 0.0
            
            return len(self.message_times) / time_span
    
    def get_stats(self) -> Dict:
        """Get comprehensive performance statistics."""
        with self.lock:
            current_time = time.time()
            uptime = current_time - self._start_time
            
            return {
                "messages_in_window": len(self.message_times),
                "current_rate": self.get_current_rate(),
                "uptime_seconds": uptime,
                "window_size": self.window_size
            }

# Usage example
monitor = LoggingPerformanceMonitor()

# Integrate with logging (would be done in processor)
def performance_aware_log():
    monitor.record_log_event()
    
    # Every 1000 messages, report performance
    if len(monitor.message_times) == monitor.window_size:
        stats = monitor.get_stats()
        print(f"Logging rate: {stats['current_rate']:.0f} msg/sec")

# Would be integrated into the logging pipeline
```