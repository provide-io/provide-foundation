# Tracer API Reference

The Foundation Tracer provides lightweight distributed tracing functionality without external dependencies, enabling operation timing and context tracking across your applications.

## Overview

The tracer module offers:

- **Span-based tracing**: Create hierarchical operation traces
- **Context propagation**: Automatic parent-child span relationships  
- **Zero dependencies**: No external tracing infrastructure required
- **Thread-safe**: Safe for concurrent and async use
- **Minimal overhead**: Designed for production performance

## Quick Start

```python
from provide.foundation.tracer import Span, with_span

# Manual span management
span = Span("operation_name")
span.set_tag("user_id", "123")
span.finish()

# Context manager (recommended)
with Span("database_query") as span:
    span.set_tag("query", "SELECT * FROM users")
    # Span automatically finished

# Helper function
with with_span("api_call") as span:
    span.set_tag("endpoint", "/users")
    # Automatic parent-child relationship
```

## Core Classes

### Span

Primary tracing primitive representing a unit of work.

#### Constructor

```python
Span(name: str, 
     span_id: str | None = None,
     trace_id: str | None = None, 
     parent_id: str | None = None,
     start_time: float | None = None)
```

**Parameters:**
- `name`: Descriptive name for the operation
- `span_id`: Unique span identifier (auto-generated if None)
- `trace_id`: Trace identifier (inherited from parent or auto-generated)
- `parent_id`: Parent span ID for hierarchy
- `start_time`: Start timestamp (defaults to current time)

**Example:**
```python
span = Span("user_authentication")
span = Span("db_query", parent_id=parent_span.span_id)
```

#### Methods

##### `set_tag(key: str, value: Any) -> None`

Add metadata to the span.

```python
span.set_tag("user_id", "usr_123")
span.set_tag("query_type", "SELECT")
span.set_tag("row_count", 42)
```

##### `set_error(error: str | Exception) -> None`

Mark span as errored and record error details.

```python
# With exception
try:
    risky_operation()
except ValueError as e:
    span.set_error(e)

# With string
span.set_error("Connection timeout")
```

##### `finish(end_time: float | None = None) -> None`

Complete the span and record end time.

```python
span.finish()  # Uses current time
span.finish(custom_end_time)  # Custom timestamp
```

##### `duration_ms() -> float`

Get span duration in milliseconds.

```python
duration = span.duration_ms()  # Returns float or -1 if not finished
```

##### `to_dict() -> dict[str, Any]`

Export span data as dictionary.

```python
data = span.to_dict()
# Returns: {
#   "span_id": "abc123",
#   "trace_id": "xyz789", 
#   "name": "operation",
#   "start_time": 1234567890.123,
#   "duration_ms": 150.5,
#   "status": "ok",
#   "tags": {"key": "value"},
#   "parent_id": None
# }
```

#### Properties

- `span_id: str` - Unique span identifier
- `trace_id: str` - Trace identifier  
- `name: str` - Span operation name
- `parent_id: str | None` - Parent span ID
- `start_time: float` - Start timestamp
- `end_time: float | None` - End timestamp (None if active)
- `status: str` - "ok" or "error"
- `tags: dict[str, Any]` - Span metadata
- `is_finished: bool` - Whether span is complete

#### Context Manager

Spans can be used as context managers for automatic lifecycle management:

```python
with Span("file_processing") as span:
    span.set_tag("filename", "data.csv")
    process_file("data.csv")
    span.set_tag("rows_processed", 1000)
# Span automatically finished, even if exception occurs
```

## Context Functions

### `get_current_span() -> Span | None`

Retrieve the currently active span.

```python
from provide.foundation.tracer import get_current_span

current = get_current_span()
if current:
    current.set_tag("additional_context", "value")
```

### `set_current_span(span: Span | None) -> None`

Set the active span for the current context.

```python
from provide.foundation.tracer import set_current_span

span = Span("background_task")
set_current_span(span)
# Later operations can access this span
```

### `get_current_trace_id() -> str | None`

Get the trace ID from the current span.

```python
from provide.foundation.tracer import get_current_trace_id

trace_id = get_current_trace_id()
if trace_id:
    logger.info("Processing request", trace_id=trace_id)
```

### `get_trace_context() -> dict[str, str]`

Get trace context headers for propagation.

```python
from provide.foundation.tracer import get_trace_context

# For HTTP headers or message metadata
context = get_trace_context()
# Returns: {"trace-id": "xyz789", "span-id": "abc123"}

# Use in HTTP requests
headers = {**base_headers, **context}
```

### `with_span(name: str, **tags) -> Span`

Context manager helper that creates child spans automatically.

```python
from provide.foundation.tracer import with_span

# Creates child of current span
with with_span("database_operation") as span:
    span.set_tag("table", "users")
    query_database()

# With initial tags
with with_span("api_call", method="GET", endpoint="/users") as span:
    make_api_call()
```

## Usage Patterns

### Basic Operation Tracking

```python
from provide.foundation.tracer import Span

def process_order(order_id: str):
    with Span("order_processing") as span:
        span.set_tag("order_id", order_id)
        
        # Process order steps
        validate_order(order_id)
        charge_payment(order_id) 
        ship_order(order_id)
        
        span.set_tag("status", "completed")
```

### Hierarchical Tracing

```python
from provide.foundation.tracer import with_span

def handle_request():
    with with_span("request_handler") as request_span:
        request_span.set_tag("endpoint", "/api/users")
        
        with with_span("auth_check") as auth_span:
            auth_span.set_tag("method", "jwt")
            authenticate_user()
        
        with with_span("database_query") as db_span:
            db_span.set_tag("query", "SELECT * FROM users")
            users = fetch_users()
            db_span.set_tag("result_count", len(users))
        
        request_span.set_tag("response_size", len(users))
```

### Error Handling

```python
from provide.foundation.tracer import Span

def risky_operation():
    with Span("risky_operation") as span:
        try:
            span.set_tag("attempt", 1)
            dangerous_code()
            span.set_tag("outcome", "success")
        except Exception as e:
            span.set_error(e)
            span.set_tag("error_type", type(e).__name__)
            raise
```

### Integration with Logging

```python
from provide.foundation import logger
from provide.foundation.tracer import with_span, get_current_trace_id

def logged_operation():
    with with_span("logged_operation") as span:
        trace_id = get_current_trace_id()
        
        logger.info("operation_started", 
                   trace_id=trace_id,
                   span_id=span.span_id)
        
        try:
            result = do_work()
            logger.info("operation_completed",
                       trace_id=trace_id, 
                       span_id=span.span_id,
                       result=result)
            return result
        except Exception as e:
            span.set_error(e)
            logger.error("operation_failed",
                        trace_id=trace_id,
                        span_id=span.span_id,
                        error=str(e))
            raise
```

### Async Operations

```python
import asyncio
from provide.foundation.tracer import with_span

async def async_operation():
    with with_span("async_task") as span:
        span.set_tag("task_type", "background")
        
        await asyncio.sleep(0.1)  # Simulate async work
        
        span.set_tag("completed", True)
```

### Cross-Service Tracing

```python
import requests
from provide.foundation.tracer import with_span, get_trace_context

def call_external_service():
    with with_span("external_api_call") as span:
        # Propagate trace context
        headers = {"Content-Type": "application/json"}
        headers.update(get_trace_context())
        
        span.set_tag("service", "payment-api")
        response = requests.post(
            "https://api.example.com/charge",
            headers=headers,
            json={"amount": 100}
        )
        
        span.set_tag("response_code", response.status_code)
        if not response.ok:
            span.set_error(f"HTTP {response.status_code}")
```

## Context Propagation

The tracer uses Python's `contextvars` for automatic context propagation:

```python
from provide.foundation.tracer import set_current_span, Span
import threading

def worker_function():
    # Spans are isolated per thread/task
    current = get_current_span()  # None in new thread
    
    with Span("worker_task") as span:
        span.set_tag("worker_id", threading.get_ident())

def main():
    with Span("main_operation") as main_span:
        main_span.set_tag("operation", "batch_process")
        
        # Start worker - gets clean context
        thread = threading.Thread(target=worker_function)
        thread.start()
        thread.join()
```

## Thread Safety

All tracer operations are thread-safe:

```python
import concurrent.futures
from provide.foundation.tracer import with_span

def parallel_task(task_id: int):
    with with_span(f"task_{task_id}") as span:
        span.set_tag("task_id", task_id)
        # Each thread gets isolated span context

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(parallel_task, i) for i in range(10)]
    # Each task creates independent span hierarchies
```

## Performance Considerations

- **Minimal overhead**: Span creation ~5μs
- **Memory efficient**: ~200 bytes per span
- **No external dependencies**: Pure Python implementation
- **Lazy evaluation**: Tags stored as references until export

```python
# For high-frequency operations, consider sampling
import random
from provide.foundation.tracer import with_span

def high_frequency_operation():
    # Sample 1% of operations
    if random.random() < 0.01:
        with with_span("sampled_operation") as span:
            span.set_tag("sampled", True)
            do_work()
    else:
        do_work()
```

## Integration Examples

Complete examples available in:
- Complex distributed tracing scenarios
- Basic usage patterns and examples

## See Also

- [Tracing User Guide](../../guide/tracing/) - Conceptual guide and patterns
- [Logger Integration](../logger/) - Combining tracing with structured logging
- [Performance Guide](../../guide/concepts/performance.md) - Optimization strategies