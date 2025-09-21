# Performance Optimization

Detailed guidance for optimizing Foundation's profiling system to minimize overhead while maximizing data quality.

## Performance Overview

Foundation's profiling system is designed for production use with minimal performance impact. Understanding the performance characteristics helps optimize for your specific workload.

### Overhead Breakdown

| Component | Typical Overhead | Optimization Potential |
|-----------|-----------------|----------------------|
| Sampling Decision | 0.001% | Fixed (very low) |
| Metrics Collection | 0.01-0.05% | High (configuration) |
| Memory Tracking | 0.02-0.10% | High (disable if not needed) |
| Buffer Management | 0.005-0.02% | Medium (tuning) |
| Export Operations | 0.01-0.50% | High (batching, async) |
| **Total (1% sampling)** | **0.03-0.67%** | **Configuration dependent** |

## Sampling Optimization

### Sample Rate Selection

Choose sample rates based on your performance requirements:

```python
# Performance-critical applications
ultra_low_overhead = ProfilingConfig(
    sample_rate=0.001,  # 0.1% - minimal overhead
    processor=ProcessorConfig(
        track_memory=False,
        enable_fast_path=True,
        minimal_metadata=True
    )
)

# Balanced production workloads
balanced_config = ProfilingConfig(
    sample_rate=0.02,   # 2% - good data quality
    processor=ProcessorConfig(
        track_memory=False,
        enable_fast_path=True,
        buffer_size=2000
    )
)

# Development and detailed monitoring
detailed_config = ProfilingConfig(
    sample_rate=0.10,   # 10% - rich data
    processor=ProcessorConfig(
        track_memory=True,
        capture_stack_traces=True,
        detailed_timing=True
    )
)
```

### Intelligent Sampling

Use adaptive sampling to optimize the tradeoff between overhead and data quality:

```python
from provide.foundation.profiling.sampling import IntelligentSampler

smart_sampler = IntelligentSampler(
    base_rate=0.005,     # Low baseline
    max_rate=0.05,       # Conservative maximum

    # Increase sampling for interesting events
    triggers={
        "slow_operations": {
            "condition": "latency > 100ms",
            "rate_multiplier": 10,
            "duration_seconds": 60
        },
        "error_events": {
            "condition": "log_level >= ERROR",
            "rate_multiplier": 20,
            "duration_seconds": 120
        }
    },

    # Reduce sampling under load
    load_shedding={
        "cpu_threshold": 0.80,       # Reduce when CPU > 80%
        "memory_threshold": 0.85,    # Reduce when memory > 85%
        "rate_reduction_factor": 0.5 # Cut rate in half
    }
)

register_profiling(hub, sampler=smart_sampler)
```

### Stratified Sampling

Sample different types of operations at different rates:

```python
from provide.foundation.profiling.sampling import StratifiedSampler

stratified_sampler = StratifiedSampler(
    strata=[
        {
            "name": "health_checks",
            "condition": "path.startswith('/health')",
            "rate": 0.001   # Very low sampling for health checks
        },
        {
            "name": "api_endpoints",
            "condition": "path.startswith('/api')",
            "rate": 0.02    # Normal sampling for API calls
        },
        {
            "name": "admin_operations",
            "condition": "path.startswith('/admin')",
            "rate": 0.10    # High sampling for admin operations
        }
    ],
    default_rate=0.01  # Default for unmatched operations
)
```

## Processor Optimization

### Fast Path Configuration

Enable optimizations that reduce processing overhead:

```python
from provide.foundation.profiling.config import ProcessorConfig

optimized_processor = ProcessorConfig(
    # Core optimizations
    enable_fast_path=True,           # Skip expensive operations when possible
    minimal_metadata=True,           # Reduce metadata collection
    skip_stack_traces=True,          # Don't capture stack traces

    # Memory optimizations
    track_memory=False,              # Disable memory tracking
    object_tracking=False,           # Don't track object counts

    # String optimizations
    intern_strings=True,             # Intern common strings
    max_string_length=100,           # Truncate long strings

    # Timestamp optimizations
    use_monotonic_time=True,         # Use faster monotonic clock
    timestamp_precision="ms"         # Millisecond precision (vs microsecond)
)
```

### Buffer Optimization

Optimize buffering for your workload:

```python
# High-throughput optimization
high_throughput_config = ProcessorConfig(
    # Larger buffers reduce flush frequency
    buffer_size=10000,
    buffer_flush_threshold=0.9,      # Flush when 90% full

    # Batch processing
    enable_batching=True,
    batch_size=500,                  # Process 500 items at once
    batch_timeout_ms=100,            # Don't wait too long

    # Background processing
    enable_background_processing=True,
    background_thread_count=2,       # Dedicated threads for processing
    thread_priority="normal"         # Don't interfere with main threads
)

# Low-latency optimization
low_latency_config = ProcessorConfig(
    # Smaller buffers for faster processing
    buffer_size=100,
    buffer_flush_threshold=0.5,      # Flush when 50% full

    # Immediate processing
    enable_batching=False,           # Process immediately
    enable_background_processing=False,  # Process in main thread

    # Minimal buffering
    max_buffer_memory_kb=1024,       # Limit buffer to 1MB
    flush_on_size=True              # Flush based on size
)
```

### Memory Management

Optimize memory usage patterns:

```python
memory_optimized_config = ProcessorConfig(
    # Memory tracking settings
    track_memory=False,              # Disable if not needed (saves ~30% overhead)
    memory_sampling_rate=0.1,        # Sample memory less frequently

    # Object pooling
    enable_object_pooling=True,      # Reuse metric objects
    pool_size=1000,                  # Pre-allocate 1000 objects

    # Garbage collection
    force_gc_interval_seconds=300,   # Trigger GC every 5 minutes
    gc_threshold_objects=10000,      # GC when 10k objects accumulated

    # String interning
    intern_common_strings=True,      # Intern frequently used strings
    string_intern_cache_size=5000    # Cache up to 5000 strings
)
```

## Export Optimization

### Batching and Compression

Optimize export operations for efficiency:

```python
from provide.foundation.profiling.exporters import OptimizedPrometheusExporter

optimized_exporter = OptimizedPrometheusExporter(
    pushgateway_url="http://prometheus:9091",

    # Batching configuration
    batch_size=1000,                 # Large batches reduce HTTP overhead
    batch_timeout_seconds=30,        # Maximum wait time
    max_batch_size=5000,            # Never exceed this size

    # Compression
    enable_compression=True,         # Compress payloads
    compression_level=6,             # Balance speed vs size
    compression_threshold=1024,      # Only compress if > 1KB

    # Connection optimization
    connection_pool_size=5,          # Reuse connections
    keep_alive=True,                 # Keep connections open
    timeout_seconds=10,              # Reasonable timeout

    # Async processing
    async_export=True,               # Don't block on exports
    max_concurrent_exports=3         # Limit concurrent exports
)
```

### Export Filtering

Reduce export volume by filtering data:

```python
filtered_exporter = DatadogExporter(
    api_key="${DATADOG_API_KEY}",

    # Metric filtering
    metric_filters={
        # Only export high-value metrics
        "include_metrics": [
            "messages_per_second",
            "avg_latency_ms",
            "error_rate",
            "p95_latency_ms"
        ],

        # Exclude noisy metrics
        "exclude_metrics": [
            "debug_message_count",
            "trace_operation_count"
        ],

        # Threshold filtering
        "min_message_count": 10,     # Only export if ≥10 messages
        "max_latency_outliers": 3    # Skip extreme outliers
    },

    # Time-based filtering
    time_filters={
        "business_hours_only": True,     # Only export during business hours
        "skip_weekends": True,           # Skip weekend exports
        "timezone": "US/Eastern"
    },

    # Sampling exports (don't export every metric)
    export_sample_rate=0.5           # Export 50% of collected metrics
)
```

### Fallback and Circuit Breaking

Protect performance with resilient export patterns:

```python
from provide.foundation.profiling.exporters import ResilientExporter

resilient_exporter = ResilientExporter(
    primary_exporter=DatadogExporter(),

    # Circuit breaker to prevent cascading failures
    circuit_breaker={
        "failure_threshold": 3,          # Trip after 3 failures
        "timeout_seconds": 60,           # Stay open for 60 seconds
        "half_open_max_calls": 2         # Test with 2 calls when half-open
    },

    # Fast fallback to prevent blocking
    fallback_exporter=FileExporter(
        output_directory="/tmp/profiling",
        format="compact"                 # Use compact format for speed
    ),

    # Performance limits
    max_export_time_seconds=5,           # Timeout exports after 5s
    max_queue_size=1000,                 # Drop old exports if queue full
    drop_oldest_on_overflow=True         # Don't block on full queue
)
```

## CPU Optimization

### Threading and Concurrency

Optimize threading for your application pattern:

```python
# CPU-bound application optimization
cpu_bound_config = ProcessorConfig(
    # Minimize thread overhead
    enable_background_processing=False,  # Process in main thread
    enable_batching=True,               # But batch for efficiency

    # Reduce context switching
    processing_interval_ms=100,         # Process every 100ms
    min_batch_size=50,                  # Wait for meaningful batches

    # CPU-friendly operations
    use_native_timing=True,             # Use fast native timing
    avoid_system_calls=True,            # Minimize system calls
    cache_expensive_operations=True     # Cache expensive computations
)

# I/O-bound application optimization
io_bound_config = ProcessorConfig(
    # Use background threads for I/O
    enable_background_processing=True,
    background_thread_count=3,          # More threads for I/O waiting

    # Aggressive batching
    buffer_size=5000,                   # Large buffer
    batch_size=1000,                    # Large batches
    batch_timeout_ms=50,               # Quick timeout

    # Async-friendly
    async_compatible=True,              # Work well with async code
    yield_frequently=True               # Yield control often
)
```

### CPU Profiling Integration

Monitor CPU usage of profiling itself:

```python
from provide.foundation.profiling.performance import CPUProfiler

# Profile the profiler
cpu_profiler = CPUProfiler(
    monitor_overhead=True,
    alert_threshold_percent=1.0,        # Alert if profiling uses >1% CPU
    sampling_interval_seconds=5,        # Check every 5 seconds
    auto_adjust=True                    # Automatically reduce sampling if needed
)

# Integrate with profiling config
performance_monitored_config = ProfilingConfig(
    sample_rate=0.02,
    performance_monitor=cpu_profiler,

    # Auto-adjustment settings
    auto_adjustment={
        "enabled": True,
        "cpu_threshold": 0.8,           # Reduce sampling if CPU > 80%
        "memory_threshold": 0.9,        # Reduce sampling if memory > 90%
        "adjustment_factor": 0.5,       # Cut sampling in half
        "recovery_delay_seconds": 300   # Wait 5 minutes before increasing
    }
)
```

## Memory Optimization

### Memory Pool Management

Use object pooling to reduce allocation overhead:

```python
from provide.foundation.profiling.memory import MemoryPool

# Configure memory pools
memory_config = ProcessorConfig(
    memory_management={
        # Object pools
        "enable_object_pooling": True,
        "metric_object_pool_size": 1000,
        "event_object_pool_size": 5000,
        "string_pool_size": 10000,

        # Memory limits
        "max_total_memory_mb": 100,     # Hard limit on profiling memory
        "gc_threshold_mb": 80,          # Trigger GC at 80MB
        "emergency_cleanup_mb": 95,     # Emergency cleanup at 95MB

        # Allocation optimization
        "pre_allocate_buffers": True,   # Pre-allocate common buffers
        "use_memory_mapped_files": True, # Use mmap for large buffers
        "zero_copy_operations": True    # Avoid unnecessary copying
    }
)
```

### Memory Leak Prevention

Prevent memory leaks in long-running applications:

```python
leak_prevention_config = ProcessorConfig(
    memory_safety={
        # Automatic cleanup
        "max_object_age_seconds": 3600,     # Clean up objects after 1 hour
        "cleanup_interval_seconds": 300,     # Run cleanup every 5 minutes
        "force_cleanup_on_threshold": True,  # Force cleanup at memory limits

        # Reference management
        "weak_references": True,             # Use weak references where possible
        "automatic_finalization": True,      # Auto-finalize unused objects
        "detect_circular_refs": True,        # Detect circular references

        # Monitoring
        "track_memory_growth": True,         # Monitor memory growth patterns
        "alert_on_leaks": True,             # Alert on potential leaks
        "memory_profiling": True            # Profile memory usage patterns
    }
)
```

## Benchmarking and Measurement

### Performance Benchmarks

Measure profiling performance impact:

```python
from provide.foundation.profiling.benchmarks import ProfilingBenchmark

# Run comprehensive benchmarks
benchmark = ProfilingBenchmark()

# Test different configurations
configs_to_test = [
    ("minimal", ProfilingConfig(sample_rate=0.001, track_memory=False)),
    ("balanced", ProfilingConfig(sample_rate=0.02, track_memory=False)),
    ("detailed", ProfilingConfig(sample_rate=0.02, track_memory=True))
]

for name, config in configs_to_test:
    result = benchmark.run_benchmark(
        config=config,
        duration_seconds=60,
        message_rate_per_second=1000,
        concurrent_threads=4
    )

    print(f"\n{name.upper()} Configuration:")
    print(f"  CPU overhead: {result.cpu_overhead_percent:.3f}%")
    print(f"  Memory overhead: {result.memory_overhead_mb:.1f}MB")
    print(f"  Latency impact: {result.latency_impact_ms:.2f}ms")
    print(f"  Throughput impact: {result.throughput_impact_percent:.2f}%")
```

### Real-time Performance Monitoring

Monitor performance in production:

```python
from provide.foundation.profiling.monitoring import PerformanceMonitor

# Setup continuous performance monitoring
perf_monitor = PerformanceMonitor(
    metrics_to_track=[
        "cpu_usage_percent",
        "memory_usage_mb",
        "processing_latency_ms",
        "export_latency_ms",
        "buffer_utilization_percent"
    ],

    alert_thresholds={
        "cpu_usage_percent": 1.0,        # Alert if >1% CPU
        "memory_usage_mb": 100,          # Alert if >100MB memory
        "processing_latency_ms": 10,     # Alert if >10ms processing
        "export_latency_ms": 1000        # Alert if >1s export time
    },

    monitoring_interval_seconds=30,      # Check every 30 seconds
    history_retention_hours=24          # Keep 24 hours of history
)

# Start monitoring
perf_monitor.start()

# Get performance report
report = perf_monitor.get_performance_report()
print(f"Average CPU overhead: {report.avg_cpu_overhead:.3f}%")
print(f"P95 processing latency: {report.p95_processing_latency:.1f}ms")
```

### Custom Performance Tests

Create application-specific performance tests:

```python
import asyncio
import threading
import time
from provide.foundation.profiling.testing import PerformanceTest

class CustomPerformanceTest(PerformanceTest):
    """Test profiling with your specific workload."""

    def setup_workload(self):
        """Setup test workload that mimics your application."""
        from provide.foundation import logger

        # Simulate your application's logging pattern
        async def api_request_simulation():
            logger.info("API request started", endpoint="/api/users", emoji="🔄")
            await asyncio.sleep(0.01)  # Simulate processing
            logger.info("Database query", table="users", emoji="🗄️")
            await asyncio.sleep(0.005)  # Simulate DB time
            logger.info("API request completed", status=200, emoji="✅")

        def background_task_simulation():
            for i in range(100):
                logger.debug(f"Processing item {i}")
                time.sleep(0.001)  # Simulate work

        return {
            "api_requests": api_request_simulation,
            "background_tasks": background_task_simulation
        }

    async def run_test(self, duration_seconds=300):
        """Run 5-minute performance test."""
        workload = self.setup_workload()

        # Start background tasks
        background_thread = threading.Thread(
            target=workload["background_tasks"]
        )
        background_thread.start()

        # Run API simulation
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            await workload["api_requests"]()
            await asyncio.sleep(0.1)  # 10 RPS

        # Wait for background tasks
        background_thread.join()

        return self.get_performance_metrics()

# Run the test
test = CustomPerformanceTest()
results = await test.run_test(duration_seconds=60)

print(f"Performance Results:")
print(f"  Total overhead: {results.total_overhead_percent:.3f}%")
print(f"  Memory impact: {results.memory_impact_mb:.1f}MB")
print(f"  Latency impact: {results.latency_impact_ms:.2f}ms")
```

## Optimization Checklist

### Production Deployment

- [ ] **Sample Rate**: Start with ≤2% sampling
- [ ] **Memory Tracking**: Disable unless needed
- [ ] **Fast Path**: Enable optimized code paths
- [ ] **Buffer Size**: Configure for your throughput
- [ ] **Export Batching**: Use large batches (≥100 items)
- [ ] **Compression**: Enable for export payloads
- [ ] **Circuit Breaker**: Protect against export failures
- [ ] **Monitoring**: Track profiling overhead metrics
- [ ] **Fallback**: Configure emergency export fallback

### Performance Monitoring

- [ ] **CPU Overhead**: Monitor and alert if >1%
- [ ] **Memory Usage**: Monitor and alert if >100MB
- [ ] **Export Latency**: Monitor and alert if >1s
- [ ] **Success Rate**: Monitor export success rate
- [ ] **Buffer Health**: Monitor buffer utilization
- [ ] **Adaptive Sampling**: Use for dynamic workloads
- [ ] **Regular Review**: Review metrics weekly

### Troubleshooting High Overhead

1. **Check Sample Rate**: Reduce if >5%
2. **Disable Memory Tracking**: Saves ~30% overhead
3. **Increase Buffer Size**: Reduces flush frequency
4. **Enable Fast Path**: Skips expensive operations
5. **Optimize Exports**: Use batching and compression
6. **Check for Leaks**: Monitor memory growth
7. **Review Configuration**: Disable unused features

This comprehensive performance guide ensures Foundation's profiling system operates efficiently in production while providing valuable performance insights.