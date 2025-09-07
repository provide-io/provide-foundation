# Timing Utilities

Performance measurement and logging tools for monitoring application performance.

## Performance Timing

### `timed_block(logger, operation_name, **kwargs)`

Context manager for timing and logging operations.

**Parameters:**
- `logger`: Logger instance to use for output
- `operation_name` (str): Name of the operation being timed
- `**kwargs`: Additional context to include in logs

**Returns:**
- Context manager that yields a dictionary for adding runtime context

**Example:**
```python
from provide.foundation import get_logger
from provide.foundation.utils import timed_block

logger = get_logger(__name__)

# Basic timing
with timed_block(logger, "database_query"):
    # Your operation here
    result = db.query("SELECT * FROM users")

# With additional context
with timed_block(logger, "data_processing", batch_size=1000) as ctx:
    # Add runtime context
    ctx["records_processed"] = process_data(data)
    ctx["errors_encountered"] = 0
```

**Output:**
```
2023-01-01 12:00:00 [info] Operation started operation=database_query
2023-01-01 12:00:01 [info] Operation completed operation=database_query duration_seconds=1.234
```

### `measure_time(func)`

Decorator for measuring function execution time.

**Parameters:**
- `func`: Function to measure

**Returns:**
- Decorated function that logs execution time

**Example:**
```python
from provide.foundation.utils import measure_time

@measure_time
def expensive_operation():
    """This function will have its execution time logged."""
    time.sleep(1)
    return "result"

result = expensive_operation()  # Logs execution time automatically
```

### `StopWatch`

High-precision stopwatch for detailed timing measurements.

**Methods:**
- `start()`: Start timing
- `stop()`: Stop timing and return elapsed time
- `reset()`: Reset the stopwatch
- `elapsed()`: Get current elapsed time without stopping
- `lap()`: Record a lap time

**Example:**
```python
from provide.foundation.utils import StopWatch

# Create stopwatch
sw = StopWatch()

# Timing with laps
sw.start()
phase_1()
lap1 = sw.lap()  # Returns elapsed time and continues

phase_2() 
lap2 = sw.lap()

total_time = sw.stop()

print(f"Phase 1: {lap1:.3f}s")
print(f"Phase 2: {lap2 - lap1:.3f}s") 
print(f"Total: {total_time:.3f}s")
```

## Performance Monitoring

### `PerformanceTracker`

Track performance metrics over time.

**Methods:**
- `record(operation, duration)`: Record an operation timing
- `get_stats(operation)`: Get statistics for an operation
- `get_all_stats()`: Get statistics for all operations
- `reset()`: Clear all recorded data

**Example:**
```python
from provide.foundation.utils import PerformanceTracker

# Create tracker
tracker = PerformanceTracker()

# Record operations
tracker.record("api_call", 0.150)
tracker.record("api_call", 0.200)
tracker.record("database_query", 0.050)

# Get statistics
api_stats = tracker.get_stats("api_call")
print(f"API calls: avg={api_stats.avg:.3f}s, max={api_stats.max:.3f}s")

# Get all stats
all_stats = tracker.get_all_stats()
for operation, stats in all_stats.items():
    print(f"{operation}: {stats}")
```

### `benchmark(func, iterations=1000, warmup=10)`

Benchmark function performance over multiple iterations.

**Parameters:**
- `func`: Function to benchmark
- `iterations` (int): Number of iterations to run (default: 1000)
- `warmup` (int): Number of warmup iterations (default: 10)

**Returns:**
- `BenchmarkResult`: Object containing timing statistics

**Example:**
```python
from provide.foundation.utils import benchmark

def calculation():
    return sum(range(1000))

# Benchmark the function
result = benchmark(calculation, iterations=5000)

print(f"Average: {result.avg:.6f}s")
print(f"Min/Max: {result.min:.6f}s / {result.max:.6f}s")
print(f"Std Dev: {result.std_dev:.6f}s")
print(f"Operations/sec: {result.ops_per_sec:.0f}")
```

## Advanced Timing Patterns

### Nested Timing

```python
from provide.foundation import get_logger
from provide.foundation.utils import timed_block

logger = get_logger(__name__)

with timed_block(logger, "full_request") as request_ctx:
    request_ctx["request_id"] = "req-123"
    
    with timed_block(logger, "authentication") as auth_ctx:
        # Auth logic
        auth_ctx["user_id"] = authenticate_user()
    
    with timed_block(logger, "business_logic") as logic_ctx:
        # Main processing
        result = process_request()
        logic_ctx["records_processed"] = len(result)
    
    request_ctx["success"] = True
```

### Conditional Timing

```python
from provide.foundation.utils import timed_block
import os

# Only time operations in debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if DEBUG:
    timer_context = timed_block(logger, "debug_operation")
else:
    timer_context = nullcontext()

with timer_context:
    # Operation is only timed in debug mode
    expensive_debug_operation()
```

### Async Timing Support

```python
import asyncio
from provide.foundation.utils import timed_block

async def async_operation():
    async with timed_block(logger, "async_database_query") as ctx:
        result = await db.async_query("SELECT * FROM users")
        ctx["rows_returned"] = len(result)
        return result

# Usage
result = await async_operation()
```