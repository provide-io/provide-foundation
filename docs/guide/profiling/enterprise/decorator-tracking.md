# Decorator-Based Tracking

!!! success "Enterprise Feature"
    Automatic function and method profiling with zero code changes and intelligent context preservation.

## Overview

Decorator-based tracking provides automatic performance monitoring for Python functions and methods without requiring manual instrumentation. The system intelligently tracks execution time, memory usage, and call patterns while preserving async context and exception information.

## Core Decorators

### @profile_function

Track individual function performance:

```python
from provide.foundation.profiling.decorators import profile_function

@profile_function
def process_data(data: list[dict]) -> dict:
    """Process user data with automatic profiling."""
    result = {}
    for item in data:
        result[item['id']] = transform_item(item)
    return result

@profile_function(
    name="data_transform",           # Custom metric name
    track_memory=True,               # Monitor memory usage
    track_args=True,                 # Log argument info
    sample_rate=0.1                  # Custom sampling rate
)
def transform_item(item: dict) -> dict:
    """Transform with detailed tracking."""
    # Expensive processing here
    return processed_item
```

### @profile_method

Class method profiling with context preservation:

```python
from provide.foundation.profiling.decorators import profile_method

class DataProcessor:
    @profile_method
    def __init__(self, config: ProcessorConfig):
        """Track initialization performance."""
        self.config = config
        self.setup_resources()

    @profile_method(track_memory=True)
    def process_batch(self, items: list[DataItem]) -> ProcessingResult:
        """Track batch processing with memory monitoring."""
        results = []
        for item in items:
            results.append(self._process_single(item))
        return ProcessingResult(results)

    @profile_method(
        name="single_item_processing",
        track_exceptions=True
    )
    def _process_single(self, item: DataItem) -> ProcessedItem:
        """Track individual item processing."""
        if item.requires_special_handling():
            return self._special_process(item)
        return self._standard_process(item)
```

### @profile_async

Async function profiling with context preservation:

```python
import asyncio
from provide.foundation.profiling.decorators import profile_async

@profile_async
async def fetch_user_data(user_id: int) -> UserData:
    """Async function with automatic profiling."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return UserData.from_json(response.json())

@profile_async(
    name="database_query",
    track_memory=True,
    context_fields=["user_id", "query_type"]
)
async def execute_query(query: str, user_id: int) -> QueryResult:
    """Database query with context tracking."""
    async with database.transaction():
        result = await database.execute(query, user_id=user_id)
        return QueryResult(result)

# Works with async context managers
@profile_async
async def process_with_context():
    """Maintains async context across calls."""
    async with AsyncContext() as ctx:
        await ctx.process_data()
        return ctx.get_results()
```

## Advanced Configuration

### Conditional Profiling

Profile functions only under specific conditions:

```python
from provide.foundation.profiling.decorators import profile_function
from provide.foundation.profiling.conditions import (
    when_env_set,
    when_debug_mode,
    when_load_high,
    when_user_flagged
)

@profile_function(
    condition=when_env_set("PROFILE_CRITICAL_PATH")
)
def critical_processing_function():
    """Only profile when explicitly enabled."""
    pass

@profile_function(
    condition=when_debug_mode() | when_load_high()
)
def expensive_operation():
    """Profile in debug mode OR when system load is high."""
    pass

@profile_function(
    condition=when_user_flagged("performance_tracking")
)
def user_specific_feature(user: User):
    """Profile only for users with performance tracking enabled."""
    pass
```

### Custom Metrics Collection

Extend profiling with domain-specific metrics:

```python
from provide.foundation.profiling.decorators import profile_function
from provide.foundation.profiling.collectors import (
    MemoryCollector,
    DatabaseCollector,
    CacheCollector
)

@profile_function(
    collectors=[
        MemoryCollector(),
        DatabaseCollector(track_queries=True),
        CacheCollector(track_hit_rate=True)
    ]
)
def data_processing_pipeline(dataset: Dataset) -> ProcessedDataset:
    """Collect comprehensive performance metrics."""
    # Memory usage automatically tracked
    processed = transform_data(dataset)

    # Database calls automatically tracked
    save_to_database(processed)

    # Cache operations automatically tracked
    cache.store(processed.cache_key, processed)

    return processed
```

### Context Propagation

Preserve and enhance context across function calls:

```python
from provide.foundation.profiling.decorators import profile_function
from provide.foundation.profiling.context import (
    TrackingContext,
    SpanContext
)

@profile_function(
    context_fields=["request_id", "user_id"],
    create_span=True
)
def handle_api_request(request: APIRequest) -> APIResponse:
    """Top-level request handler with span creation."""

    # Context automatically propagated to child functions
    user_data = fetch_user_data(request.user_id)
    result = process_request(request, user_data)

    return APIResponse(result)

@profile_function(inherit_context=True)
def fetch_user_data(user_id: int) -> UserData:
    """Inherits context from parent function."""
    # Automatically linked to parent span
    return database.get_user(user_id)

@profile_function(
    inherit_context=True,
    add_context={"operation": "data_processing"}
)
def process_request(request: APIRequest, user: UserData) -> ProcessResult:
    """Add additional context while inheriting parent context."""
    # Context now includes both inherited and added fields
    return business_logic.process(request, user)
```

## Integration Patterns

### Class-Level Profiling

Profile entire classes with selective method exclusion:

```python
from provide.foundation.profiling.decorators import profile_class

@profile_class(
    exclude_methods=["__init__", "__str__", "__repr__"],
    track_memory=True,
    sample_rate=0.05
)
class DataAnalyzer:
    """All methods automatically profiled except excluded ones."""

    def analyze_dataset(self, data: Dataset) -> AnalysisResult:
        """Automatically profiled."""
        return self._run_analysis(data)

    def _run_analysis(self, data: Dataset) -> AnalysisResult:
        """Also automatically profiled."""
        pass

    def __str__(self) -> str:
        """Excluded from profiling."""
        return f"DataAnalyzer({self.config})"
```

### Module-Level Registration

Profile all functions in a module:

```python
# analytics/processors.py
from provide.foundation.profiling.decorators import profile_module

# Register profiling for entire module
profile_module(
    __name__,
    exclude_patterns=["_private_*", "test_*"],
    sample_rate=0.02,
    track_memory=True
)

def public_function():
    """Automatically profiled."""
    pass

def _private_function():
    """Excluded by pattern."""
    pass

def test_function():
    """Excluded by pattern."""
    pass
```

### Framework Integration

#### FastAPI Integration

```python
from fastapi import FastAPI
from provide.foundation.profiling.decorators import profile_async
from provide.foundation.profiling.middleware import ProfilingMiddleware

app = FastAPI()
app.add_middleware(ProfilingMiddleware)

@app.get("/users/{user_id}")
@profile_async(
    name="api_get_user",
    context_fields=["user_id"],
    track_memory=True
)
async def get_user(user_id: int) -> UserResponse:
    """API endpoint with automatic profiling."""
    user_data = await fetch_user_data(user_id)
    return UserResponse.from_data(user_data)
```

#### Django Integration

```python
from django.http import JsonResponse
from provide.foundation.profiling.decorators import profile_function
from provide.foundation.profiling.django import ProfiledView

class UserDetailView(ProfiledView):
    """Django view with automatic profiling."""

    profiling_config = {
        "track_memory": True,
        "context_fields": ["user_id"],
        "sample_rate": 0.1
    }

    def get(self, request, user_id):
        """Automatically profiled by ProfiledView."""
        user = self.get_user_data(user_id)
        return JsonResponse(user.to_dict())

    @profile_function
    def get_user_data(self, user_id: int) -> UserData:
        """Additional explicit profiling."""
        return UserData.objects.get(id=user_id)
```

## Metrics and Analysis

### Collected Metrics

Each decorated function automatically collects:

| Metric | Description | Use Case |
|--------|-------------|----------|
| `execution_time_ms` | Function execution duration | Performance analysis |
| `memory_peak_mb` | Peak memory usage during execution | Memory optimization |
| `memory_delta_mb` | Memory change from start to finish | Memory leak detection |
| `call_count` | Number of times function called | Usage pattern analysis |
| `exception_count` | Number of exceptions raised | Error rate monitoring |
| `avg_args_size_kb` | Average size of function arguments | Data size impact |

### Accessing Metrics

```python
from provide.foundation.profiling.registry import get_function_metrics

# Get metrics for specific function
metrics = get_function_metrics("process_data")
print(f"Average execution time: {metrics.avg_execution_time_ms:.2f}ms")
print(f"Memory efficiency: {metrics.memory_efficiency_score:.2f}")

# Get metrics for all profiled functions
all_metrics = get_function_metrics()
for func_name, metrics in all_metrics.items():
    if metrics.avg_execution_time_ms > 100:  # Functions taking > 100ms
        print(f"Slow function: {func_name} ({metrics.avg_execution_time_ms:.0f}ms)")
```

### Performance Reports

Generate comprehensive performance reports:

```python
from provide.foundation.profiling.reports import generate_performance_report

# Generate report for specific time period
report = generate_performance_report(
    start_time=datetime.now() - timedelta(hours=1),
    include_memory=True,
    include_exceptions=True,
    format="json"
)

# Top slowest functions
print("Slowest Functions:")
for func in report.slowest_functions:
    print(f"  {func.name}: {func.avg_time_ms:.0f}ms")

# Memory usage leaders
print("Memory Usage Leaders:")
for func in report.memory_leaders:
    print(f"  {func.name}: {func.peak_memory_mb:.1f}MB")

# Exception-prone functions
print("Exception-Prone Functions:")
for func in report.exception_leaders:
    print(f"  {func.name}: {func.exception_rate:.1%}")
```

## Configuration and Tuning

### Global Configuration

Set default behavior for all decorators:

```python
from provide.foundation.profiling.config import set_decorator_defaults

set_decorator_defaults(
    sample_rate=0.02,           # 2% sampling by default
    track_memory=False,         # Disable memory tracking by default
    track_exceptions=True,      # Enable exception tracking
    context_inheritance=True,   # Enable context inheritance
    span_creation=False         # Disable span creation by default
)
```

### Environment-Based Configuration

Configure profiling behavior through environment variables:

```bash
# Enable decorator profiling
export PROVIDE_PROFILING_DECORATORS_ENABLED=true

# Set global sampling rate
export PROVIDE_PROFILING_DECORATORS_SAMPLE_RATE=0.05

# Enable memory tracking globally
export PROVIDE_PROFILING_DECORATORS_TRACK_MEMORY=true

# Set function name patterns to exclude
export PROVIDE_PROFILING_DECORATORS_EXCLUDE_PATTERNS="test_*,_private_*"
```

### Performance Tuning

Optimize decorator overhead:

```python
from provide.foundation.profiling.decorators import configure_performance

configure_performance(
    # Reduce overhead by batching metrics collection
    batch_size=100,
    batch_timeout_seconds=5,

    # Use efficient serialization
    use_fast_serialization=True,

    # Optimize memory tracking
    memory_sampling_interval=0.1,  # Sample memory every 100ms

    # Optimize context propagation
    context_pool_size=1000,        # Pre-allocate context objects
)
```

## Best Practices

### Production Deployment

1. **Use conservative sampling rates** (1-5%) in production
2. **Enable selective profiling** for critical code paths only
3. **Monitor overhead** regularly and adjust sampling
4. **Use conditional profiling** to enable detailed tracking on demand

### Development and Testing

1. **Use higher sampling rates** (10-100%) for development
2. **Enable memory tracking** for optimization work
3. **Profile test suites** to identify slow tests
4. **Use span creation** for distributed tracing integration

### Performance Optimization

1. **Profile before optimizing** to identify actual bottlenecks
2. **Monitor memory usage** for functions processing large datasets
3. **Track exception rates** to identify error-prone code paths
4. **Use context fields** for request-level performance analysis

## Troubleshooting

### Common Issues

**Decorators not collecting metrics**
```python
# Verify profiling is enabled
from provide.foundation.profiling.config import is_decorator_profiling_enabled
assert is_decorator_profiling_enabled()

# Check sampling rate
from provide.foundation.profiling.registry import get_decorator_config
config = get_decorator_config()
print(f"Sample rate: {config.sample_rate}")
```

**High overhead from profiling**
```python
# Reduce sampling rate
from provide.foundation.profiling.config import set_decorator_defaults
set_decorator_defaults(sample_rate=0.01)  # 1% sampling

# Disable memory tracking
set_decorator_defaults(track_memory=False)
```

**Missing context in child functions**
```python
# Ensure context inheritance is enabled
@profile_function(inherit_context=True)
def child_function():
    pass
```

### Debug Mode

Enable detailed logging for decorator operations:

```python
import logging
logging.getLogger("provide.foundation.profiling.decorators").setLevel(logging.DEBUG)
```