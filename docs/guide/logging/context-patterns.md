# Implementation Patterns

Practical context usage patterns for production applications.

### Hierarchical Context

```python
class HierarchicalContext:
    """Build context hierarchy."""
    
    def __init__(self, parent: Optional["HierarchicalContext"] = None):
        self.parent = parent
        self.local_context = {}
        self._logger = None
    
    def bind(self, **kwargs) -> "HierarchicalContext":
        """Create child context with additional bindings."""
        child = HierarchicalContext(parent=self)
        child.local_context = kwargs
        return child
    
    def get_full_context(self) -> dict[str, Any]:
        """Get complete context including parents."""
        if self.parent:
            parent_context = self.parent.get_full_context()
            return {**parent_context, **self.local_context}
        return self.local_context
    
    @property
    def logger(self):
        """Get logger with full context."""
        if not self._logger:
            self._logger = logger.bind(**self.get_full_context())
        return self._logger

# Usage
app_context = HierarchicalContext()
app_context.local_context = {"app": "my-service", "version": "1.0"}

request_context = app_context.bind(request_id="req_123")
user_context = request_context.bind(user_id="usr_456")

# Full context is inherited
user_context.logger.info("action_performed")
# Includes: app, version, request_id, user_id
```

### Context Stack

```python
class ContextStack:
    """Manage stack of contexts."""
    
    def __init__(self):
        self.stack = []
        self._current_logger = logger
    
    def push(self, **context):
        """Push new context onto stack."""
        self.stack.append(context)
        self._update_logger()
    
    def pop(self):
        """Pop context from stack."""
        if self.stack:
            self.stack.pop()
            self._update_logger()
    
    def _update_logger(self):
        """Update logger with merged context."""
        merged = {}
        for context in self.stack:
            merged.update(context)
        self._current_logger = logger.bind(**merged)
    
    @property
    def current(self):
        """Get current logger with stacked context."""
        return self._current_logger
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()

# Usage
context_stack = ContextStack()

context_stack.push(operation="data_sync")
context_stack.current.info("sync_started")

context_stack.push(batch_id="batch_001")
context_stack.current.info("batch_processing")

context_stack.pop()  # Remove batch_id
context_stack.current.info("sync_completed")
```

## Dynamic Context

### Lazy Context Evaluation

```python
from typing import Callable, Any

class LazyContext:
    """Context with lazy evaluation."""
    
    def __init__(self):
        self.static_context = {}
        self.dynamic_context = {}
    
    def bind_static(self, **kwargs):
        """Bind static context values."""
        self.static_context.update(kwargs)
    
    def bind_dynamic(self, **kwargs: Callable[[], Any]):
        """Bind dynamic context functions."""
        self.dynamic_context.update(kwargs)
    
    def get_context(self) -> dict[str, Any]:
        """Evaluate and merge all context."""
        context = self.static_context.copy()
        
        # Evaluate dynamic context
        for key, func in self.dynamic_context.items():
            try:
                context[key] = func()
            except Exception as e:
                context[key] = f"<error: {e}>"
        
        return context
    
    def log(self, level: str, event: str, **kwargs):
        """Log with evaluated context."""
        context = self.get_context()
        merged = {**context, **kwargs}
        getattr(logger, level)(event, **merged)

# Usage
lazy_ctx = LazyContext()

# Static context
lazy_ctx.bind_static(
    service="api",
    environment="prod"
)

# Dynamic context - evaluated at log time
lazy_ctx.bind_dynamic(
    memory_mb=lambda: get_memory_usage() / 1024 / 1024,
    active_connections=lambda: count_active_connections(),
    queue_depth=lambda: get_queue_depth(),
    cpu_percent=lambda: psutil.cpu_percent()
)

# Context is evaluated when logging
lazy_ctx.log("info", "health_check")
```

### Conditional Context

```python
class ConditionalContext:
    """Add context based on conditions."""
    
    def __init__(self):
        self.conditions = []
    
    def add_condition(self, 
                     condition: Callable[[], bool],
                     context: dict[str, Any]):
        """Add conditional context."""
        self.conditions.append((condition, context))
    
    def get_context(self) -> dict[str, Any]:
        """Get context for met conditions."""
        context = {}
        
        for condition, ctx in self.conditions:
            try:
                if condition():
                    context.update(ctx)
            except Exception:
                pass  # Ignore failed conditions
        
        return context
    
    def with_logger(self) -> Any:
        """Get logger with conditional context."""
        return logger.bind(**self.get_context())

# Setup conditional context
cond_ctx = ConditionalContext()

# Add debug context only in debug mode
cond_ctx.add_condition(
    lambda: os.environ.get("DEBUG") == "true",
    {"debug_mode": True, "verbose": True}
)

# Add performance context under load
cond_ctx.add_condition(
    lambda: get_cpu_usage() > 80,
    {"high_load": True, "performance_monitoring": "enabled"}
)

# Add error context when errors are high
cond_ctx.add_condition(
    lambda: get_error_rate() > 0.05,
    {"error_alert": True, "monitoring_level": "critical"}
)

# Use conditional logger
cond_ctx.with_logger().info("system_status")
```

## Context Middleware

### FastAPI Context Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

class LoggingContextMiddleware(BaseHTTPMiddleware):
    """Add logging context to all requests."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = request.headers.get("X-Request-ID", 
                                        str(uuid.uuid4()))
        
        # Extract user info
        user_id = request.headers.get("X-User-ID")
        
        # Start timer
        start_time = time.time()
        
        # Bind context
        request.state.logger = logger.bind(
            request_id=request_id,
            user_id=user_id,
            method=request.method,
            path=request.url.path,
            client_host=request.client.host
        )
        
        await request.state.logger.ainfo("request_started")
        
        try:
            response = await call_next(request)
            
            duration_ms = (time.time() - start_time) * 1000
            await request.state.logger.ainfo("request_completed",
                                           status_code=response.status_code,
                                           duration_ms=duration_ms)
            
            # Add request ID to response
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            await request.state.logger.aerror("request_failed",
                                            error=str(e),
                                            duration_ms=duration_ms)
            raise

app.add_middleware(LoggingContextMiddleware)

@app.get("/api/data")
async def get_data(request: Request):
    """Endpoint using request context."""
    await request.state.logger.ainfo("fetching_data")
    
    data = await fetch_data()
    
    await request.state.logger.ainfo("data_fetched",
                                   record_count=len(data))
    return data
```

## Testing Context

### Test Context Isolation

```python
import pytest
from provide.foundation.testing import isolated_logger

def test_context_isolation():
    """Test that context doesn't leak between tests."""
    
    with isolated_logger() as test_logger:
        # Add test context
        bound_logger = test_logger.bind(test_id="test_001")
        bound_logger.info("test_event")
        
        # Verify context was added
        with capture_logs() as logs:
            bound_logger.info("another_event")
        
        assert logs[0]["test_id"] == "test_001"
    
    # Context should not leak to global logger
    with capture_logs() as logs:
        logger.info("global_event")
    
    assert "test_id" not in logs[0]

@pytest.fixture
def logger_with_context():
    """Fixture providing logger with test context."""
    test_context = {
        "test_run": str(uuid.uuid4()),
        "test_env": "pytest",
        "test_time": datetime.utcnow().isoformat()
    }
    
    return logger.bind(**test_context)

def test_with_fixture_context(logger_with_context):
    """Test using context from fixture."""
    logger_with_context.info("test_operation")
    
    # Context is automatically included
    with capture_logs() as logs:
        logger_with_context.info("test_event")
    
    assert logs[0]["test_env"] == "pytest"
```

## Best Practices

### 1. Use Structured Context

```python
# ✅ Good: Structured context
with logger.bind(request={"id": "123", "method": "GET", "path": "/api"}):
    logger.info("processing_request")

# ❌ Bad: Unstructured context
with logger.bind(request_info="GET /api request 123"):
    logger.info("processing_request")
```

### 2. Keep Context Minimal

```python
# ✅ Good: Essential context only
logger.bind(user_id=user.id, request_id=request.id)

# ❌ Bad: Excessive context
logger.bind(user=user.to_dict())  # Too much data
```

### 3. Use Consistent Keys

```python
# ✅ Good: Consistent naming
logger.bind(user_id="123", request_id="456", transaction_id="789")

# ❌ Bad: Inconsistent naming
logger.bind(user="123", req_id="456", trans="789")
```

### 4. Clean Up Context

```python
# ✅ Good: Context is properly scoped
with logger.bind(operation="sync"):
    perform_sync()
# Context automatically removed

# ❌ Bad: Context leaks
logger = logger.bind(operation="sync")
perform_sync()
# Context persists indefinitely
```

### 5. Document Context Fields

```python
# ✅ Good: Document expected context
class RequestContext:
    """Standard request context fields.
    
    Fields:
        request_id: Unique request identifier
        user_id: Authenticated user ID
        trace_id: Distributed trace identifier
        span_id: Current span identifier
    """
    pass
```

## Next Steps

- ⚡ [Performance Tuning](performance.md) - Optimize context performance
- 🚨 [Exception Handling](exceptions.md) - Context in error scenarios  
- 🔄 [Async Logging](async.md) - Context in async operations
- 🔧 [Basic Logging](basic.md) - Fundamental logging patterns
- 🏠 [Back to Logging Guide](index.md)
