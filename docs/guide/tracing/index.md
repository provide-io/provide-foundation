# Distributed Tracing Guide

Foundation's tracer module provides lightweight distributed tracing for tracking operations across your applications without requiring external infrastructure like Jaeger or Zipkin.

## Overview

Distributed tracing helps you:

- 🔍 **Track request flows** across multiple services and components
- ⏱️ **Measure operation timings** and identify bottlenecks  
- 🏗️ **Visualize system architecture** through span relationships
- 🐛 **Debug complex interactions** by following execution paths
- 📊 **Gather performance metrics** for optimization

Foundation's tracer is designed to be:
- **Zero-dependency**: No external services required
- **Lightweight**: Minimal performance overhead
- **Simple**: Easy to instrument existing code
- **Flexible**: Works with any logging or monitoring system

## Core Concepts

### Traces
A **trace** represents the complete journey of a request through your system. Each trace has a unique `trace_id` that connects all related operations.

### Spans  
A **span** represents a single operation within a trace. Spans have:
- **Name**: Descriptive operation name (e.g., "database_query", "api_call")
- **Timing**: Start and end timestamps
- **Tags**: Key-value metadata about the operation
- **Status**: "ok" or "error" 
- **Hierarchy**: Parent-child relationships with other spans

### Context Propagation
**Context** automatically maintains the current span across function calls and async operations, enabling automatic parent-child relationships.

## Quick Start

### Basic Span Creation

```python
from provide.foundation.tracer import Span

# Manual span lifecycle
span = Span("user_login")
span.set_tag("user_id", "usr_123")
span.set_tag("method", "password")

# ... do work ...

span.finish()
```

### Context Manager (Recommended)

```python
from provide.foundation.tracer import Span

# Automatic lifecycle management
with Span("user_login") as span:
    span.set_tag("user_id", "usr_123")
    span.set_tag("method", "password")
    
    authenticate_user()
    # Span automatically finished, even if exception occurs
```

### Helper Function

```python
from provide.foundation.tracer import with_span

# Creates child spans automatically
def process_order():
    with with_span("order_processing") as span:
        span.set_tag("order_id", "ord_123")
        
        # This creates a child span
        with with_span("payment_processing") as payment_span:
            payment_span.set_tag("amount", 99.99)
            process_payment()
        
        # This creates another child span  
        with with_span("inventory_update") as inventory_span:
            inventory_span.set_tag("items_count", 3)
            update_inventory()
```

## Instrumentation Patterns

### Web Request Tracing

```python
from provide.foundation.tracer import with_span
from provide.foundation import logger

def handle_request(request):
    with with_span("http_request") as span:
        span.set_tag("method", request.method)
        span.set_tag("path", request.path)
        span.set_tag("remote_ip", request.remote_addr)
        
        try:
            # Process request with child spans
            user = authenticate_request(request)
            response = process_request(request, user)
            
            span.set_tag("user_id", user.id)
            span.set_tag("response_status", response.status_code)
            
            return response
            
        except Exception as e:
            span.set_error(e)
            span.set_tag("error_type", type(e).__name__)
            raise

def authenticate_request(request):
    with with_span("authentication") as span:
        span.set_tag("auth_method", "jwt")
        
        token = extract_token(request)
        user = validate_token(token)
        
        span.set_tag("user_id", user.id)
        span.set_tag("token_valid", True)
        
        return user

def process_request(request, user):
    with with_span("request_processing") as span:
        span.set_tag("user_id", user.id)
        
        # Database operations get their own spans
        data = fetch_user_data(user.id)
        result = transform_data(data)
        
        span.set_tag("data_size", len(result))
        return create_response(result)
```

### Database Operation Tracing

```python
from provide.foundation.tracer import with_span

class TracedDatabase:
    def query(self, sql: str, params: dict = None):
        with with_span("database_query") as span:
            span.set_tag("query_type", sql.split()[0].upper())  # SELECT, INSERT, etc.
            span.set_tag("table", self._extract_table(sql))
            span.set_tag("param_count", len(params) if params else 0)
            
            try:
                result = self._execute(sql, params)
                span.set_tag("row_count", len(result))
                span.set_tag("success", True)
                return result
                
            except Exception as e:
                span.set_error(e)
                span.set_tag("error_code", getattr(e, 'code', None))
                raise

    def transaction(self):
        return TracedTransaction(self)

class TracedTransaction:
    def __enter__(self):
        self.span = Span("database_transaction")
        self.span.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.span.set_error(f"{exc_type.__name__}: {exc_val}")
        else:
            self.span.set_tag("committed", True)
        return self.span.__exit__(exc_type, exc_val, exc_tb)
```

### Service-to-Service Tracing

```python
import requests
from provide.foundation.tracer import with_span, get_trace_context

def call_payment_service(amount: float, card_token: str):
    with with_span("payment_service_call") as span:
        span.set_tag("service", "payment-api")
        span.set_tag("amount", amount)
        span.set_tag("currency", "USD")
        
        # Propagate trace context via headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_api_token()}"
        }
        headers.update(get_trace_context())  # Add trace-id, span-id headers
        
        try:
            response = requests.post(
                "https://payment.example.com/charge",
                headers=headers,
                json={
                    "amount": amount,
                    "card_token": card_token
                },
                timeout=30
            )
            
            span.set_tag("response_status", response.status_code)
            span.set_tag("payment_id", response.json().get("payment_id"))
            
            if response.ok:
                span.set_tag("success", True)
                return response.json()
            else:
                span.set_error(f"Payment failed: HTTP {response.status_code}")
                raise PaymentError(response.json().get("error"))
                
        except requests.RequestException as e:
            span.set_error(e)
            span.set_tag("error_type", type(e).__name__)
            raise
```

### Background Task Tracing

```python
import asyncio
from provide.foundation.tracer import with_span, set_current_span

async def process_background_jobs():
    """Process background jobs with isolated trace contexts."""
    
    jobs = await get_pending_jobs()
    
    # Process each job in isolation
    tasks = []
    for job in jobs:
        task = asyncio.create_task(process_single_job(job))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

async def process_single_job(job):
    # Each job gets its own trace
    with with_span("background_job") as span:
        span.set_tag("job_id", job.id)
        span.set_tag("job_type", job.type)
        span.set_tag("priority", job.priority)
        
        try:
            result = await execute_job(job)
            span.set_tag("result", result)
            span.set_tag("success", True)
            
        except Exception as e:
            span.set_error(e)
            span.set_tag("retry_count", job.retry_count)
            
            # Schedule retry if needed
            if job.retry_count < 3:
                await schedule_retry(job)
            raise

async def execute_job(job):
    with with_span(f"job_{job.type}") as span:
        span.set_tag("job_id", job.id)
        
        if job.type == "email":
            return await send_email(job.data)
        elif job.type == "export":
            return await generate_export(job.data)
        else:
            raise ValueError(f"Unknown job type: {job.type}")
```

## Integration with Logging

Combine tracing with structured logging for comprehensive observability:

```python
from provide.foundation import logger
from provide.foundation.tracer import with_span, get_current_trace_id

def traced_operation(user_id: str):
    with with_span("user_operation") as span:
        trace_id = get_current_trace_id()
        
        span.set_tag("user_id", user_id)
        
        # Include trace context in logs
        logger.info("operation_started",
                   trace_id=trace_id,
                   span_id=span.span_id,
                   user_id=user_id)
        
        try:
            result = perform_operation(user_id)
            
            span.set_tag("result_size", len(result))
            logger.info("operation_completed",
                       trace_id=trace_id,
                       span_id=span.span_id,
                       result_count=len(result))
            
            return result
            
        except Exception as e:
            span.set_error(e)
            logger.error("operation_failed",
                        trace_id=trace_id,
                        span_id=span.span_id,
                        error=str(e),
                        error_type=type(e).__name__)
            raise
```

## Error Handling and Debugging

### Automatic Error Capture

```python
from provide.foundation.tracer import with_span

def error_prone_operation():
    with with_span("risky_operation") as span:
        span.set_tag("retry_attempt", 1)
        
        try:
            result = dangerous_operation()
            span.set_tag("success", True)
            return result
            
        except ValueError as e:
            # Span automatically marked as error
            span.set_error(e)
            span.set_tag("error_category", "validation")
            raise
            
        except ConnectionError as e:
            span.set_error(e)
            span.set_tag("error_category", "network")
            span.set_tag("retry_eligible", True)
            raise
```

### Custom Error Handling

```python
from provide.foundation.tracer import with_span

def robust_operation():
    with with_span("robust_operation") as span:
        for attempt in range(3):
            span.set_tag(f"attempt_{attempt + 1}", True)
            
            try:
                result = unreliable_service_call()
                span.set_tag("success_attempt", attempt + 1)
                return result
                
            except Exception as e:
                span.set_tag(f"attempt_{attempt + 1}_error", str(e))
                
                if attempt == 2:  # Last attempt
                    span.set_error(f"Failed after 3 attempts: {e}")
                    raise
                else:
                    # Continue to next attempt
                    time.sleep(2 ** attempt)  # Exponential backoff
```

## Performance Considerations

### Sampling for High-Volume Operations

```python
import random
from provide.foundation.tracer import with_span

def high_frequency_operation():
    # Sample 1% of operations for tracing
    should_trace = random.random() < 0.01
    
    if should_trace:
        with with_span("sampled_operation") as span:
            span.set_tag("sampled", True)
            span.set_tag("sample_rate", 0.01)
            return do_work()
    else:
        return do_work()
```

### Conditional Tracing

```python
import os
from provide.foundation.tracer import with_span

def conditionally_traced_operation():
    # Only trace in development or when explicitly enabled
    trace_enabled = os.getenv("ENABLE_TRACING", "false").lower() == "true"
    
    if trace_enabled:
        with with_span("traced_operation") as span:
            span.set_tag("environment", os.getenv("ENVIRONMENT", "unknown"))
            return perform_operation()
    else:
        return perform_operation()
```

### Lazy Tag Evaluation

```python
from provide.foundation.tracer import with_span

def expensive_operation():
    with with_span("expensive_operation") as span:
        # Set expensive tags only when needed
        span.set_tag("input_hash", lambda: hash_large_input(input_data))
        span.set_tag("system_state", lambda: get_system_metrics())
        
        result = do_work()
        
        # Simple tags are always set
        span.set_tag("result_count", len(result))
        return result
```

## Testing Traced Code

### Capturing Spans in Tests

```python
import pytest
from provide.foundation.tracer import get_current_span, set_current_span

def test_traced_function():
    # Reset trace context for test isolation
    set_current_span(None)
    
    # Call traced function
    result = my_traced_function()
    
    # Verify result
    assert result == expected_value
    
    # Verify no active span after completion
    assert get_current_span() is None

def test_span_hierarchy():
    spans = []
    
    def span_collector(span):
        spans.append(span.to_dict())
    
    # Mock span finishing to collect data
    with patch('provide.foundation.tracer.Span.finish', 
               side_effect=span_collector):
        my_hierarchical_function()
    
    # Verify span relationships
    assert len(spans) == 3
    root_span = next(s for s in spans if s['parent_id'] is None)
    child_spans = [s for s in spans if s['parent_id'] == root_span['span_id']]
    assert len(child_spans) == 2
```

### Mock Tracing

```python
from unittest.mock import patch, MagicMock

def test_without_actual_tracing():
    with patch('provide.foundation.tracer.Span') as mock_span_class:
        mock_span = MagicMock()
        mock_span_class.return_value.__enter__.return_value = mock_span
        
        result = traced_function()
        
        # Verify span was created with correct name
        mock_span_class.assert_called_with("expected_operation_name")
        
        # Verify tags were set
        mock_span.set_tag.assert_any_call("expected_key", "expected_value")
```

## Common Patterns

### Decorator for Automatic Tracing

```python
from functools import wraps
from provide.foundation.tracer import with_span

def trace_function(operation_name: str = None):
    """Decorator to automatically trace function calls."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"
            
            with with_span(name) as span:
                # Add function metadata
                span.set_tag("function", func.__name__)
                span.set_tag("module", func.__module__)
                span.set_tag("arg_count", len(args))
                span.set_tag("kwarg_count", len(kwargs))
                
                try:
                    result = func(*args, **kwargs)
                    span.set_tag("success", True)
                    return result
                except Exception as e:
                    span.set_error(e)
                    raise
                    
        return wrapper
    return decorator

# Usage
@trace_function("user_registration")
def register_user(email: str, password: str):
    # Function automatically traced
    return create_user(email, password)
```

### Class-based Tracing

```python
from provide.foundation.tracer import with_span

class TracedService:
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    def _trace_method(self, method_name: str):
        return with_span(f"{self.service_name}.{method_name}")
    
    def process_data(self, data):
        with self._trace_method("process_data") as span:
            span.set_tag("data_size", len(data))
            span.set_tag("service", self.service_name)
            
            result = self._transform_data(data)
            span.set_tag("result_size", len(result))
            return result
    
    def _transform_data(self, data):
        with self._trace_method("transform_data") as span:
            # Processing logic
            return transformed_data
```

## Best Practices

### 1. Meaningful Span Names
Use descriptive, hierarchical names:

```python
# ✅ Good
with_span("user_service.authenticate")
with_span("database.users.query") 
with_span("payment_gateway.charge")

# ❌ Bad  
with_span("function1")
with_span("db")
with_span("call")
```

### 2. Consistent Tagging

Establish tagging conventions across your application:

```python
# Standard tags for all operations
span.set_tag("service", "user-api")
span.set_tag("version", "1.2.0")
span.set_tag("environment", "production")

# Domain-specific tags
span.set_tag("user_id", user.id)
span.set_tag("tenant_id", tenant.id)
span.set_tag("correlation_id", request.correlation_id)
```

### 3. Error Context

Always provide useful error context:

```python
try:
    result = external_api_call()
except requests.HTTPError as e:
    span.set_error(e)
    span.set_tag("http_status", e.response.status_code)
    span.set_tag("endpoint", e.request.url)
    span.set_tag("retry_eligible", e.response.status_code >= 500)
    raise
```

### 4. Resource Cleanup

Ensure spans are properly finished:

```python
# ✅ Preferred: Use context managers
with with_span("operation") as span:
    do_work()

# ⚠️ Manual management: Ensure finish() is called
span = Span("operation")
try:
    do_work()
finally:
    span.finish()
```

### 5. Avoid Over-Instrumentation

Don't trace every function - focus on:
- Service boundaries (HTTP requests, database calls)
- Business operations (user registration, payment processing)  
- Error-prone operations (external API calls, file I/O)
- Performance-critical paths

```python
# ✅ Good: Service boundary
with with_span("user_registration"):
    validate_email()  # Don't trace
    hash_password()   # Don't trace  
    save_to_db()      # Trace this separately

# ❌ Bad: Over-instrumentation
with with_span("user_registration"):
    with with_span("validate_email"):
        with with_span("regex_check"):
            with with_span("string_match"):
                # Too granular!
```

## Next Steps

- 📖 Review the complete [Tracer API Reference](../../api/tracer/api-index.md)
- 🛠️ See working examples in [examples/15_distributed_tracing.py](https://github.com/provide-io/provide-foundation/blob/main/examples/15_distributed_tracing.py)
- 🔗 Learn about [Logger Integration](../logging/advanced.md) 
- ⚡ Optimize with [Performance Guidelines](../concepts/performance.md)