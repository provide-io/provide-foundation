# Context Management

Advanced context propagation and management patterns for provide.foundation logging.

## Overview

Context management enables you to:

- 🔗 **Bind Context** - Attach metadata to all logs in a scope
- 🌍 **Global Context** - Set application-wide context
- 🧵 **Thread-Local Context** - Maintain context per thread
- 🔄 **Context Propagation** - Pass context across boundaries
- 📦 **Context Inheritance** - Build hierarchical context

## Basic Context Binding

### Temporary Context

```python
from provide.foundation import logger

# Add context for a block of code
with logger.bind(request_id="req_123", user_id="user_456"):
    logger.info("processing_started")
    # All logs in this block include request_id and user_id
    
    process_request()
    
    logger.info("processing_completed")
    # Still includes the context

# Context is removed here
logger.info("other_operation")  # No request_id or user_id
```

### Permanent Context

```python
# Create logger with permanent context
api_logger = logger.bind(
    service="payment-api",
    version="2.1.0",
    environment="production"
)

# All logs from api_logger include the bound context
api_logger.info("service_started")
api_logger.info("request_processed", endpoint="/charge")
```

### Nested Context

```python
# Context can be nested and combined
with logger.bind(request_id="req_001"):
    logger.info("request_received")
    
    with logger.bind(user_id="usr_123"):
        logger.info("user_authenticated")
        # Has both request_id and user_id
        
        with logger.bind(transaction_id="txn_456"):
            logger.info("transaction_started")
            # Has all three IDs
```

## Thread-Local Context

### Thread Context Manager

```python
import threading
from contextvars import ContextVar
from typing import Any

# Context variables are thread-safe
request_context: ContextVar[dict[str, Any]] = ContextVar(
    "request_context",
    default={}
)

class ThreadLocalLogger:
    """Logger with thread-local context."""
    
    @staticmethod
    def bind(**kwargs) -> None:
        """Add to thread-local context."""
        current = request_context.get()
        updated = {**current, **kwargs}
        request_context.set(updated)
    
    @staticmethod
    def unbind(*keys) -> None:
        """Remove from thread-local context."""
        current = request_context.get()
        updated = {k: v for k, v in current.items() if k not in keys}
        request_context.set(updated)
    
    @staticmethod
    def log(level: str, event: str, **kwargs):
        """Log with thread-local context."""
        context = request_context.get()
        merged = {**context, **kwargs}
        getattr(logger, level)(event, **merged)

# Usage in threaded application
def worker_thread(worker_id: int):
    """Worker with its own context."""
    ThreadLocalLogger.bind(worker_id=worker_id)
    
    for task in get_tasks():
        ThreadLocalLogger.bind(task_id=task.id)
        ThreadLocalLogger.log("info", "task_started")
        
        process_task(task)
        
        ThreadLocalLogger.log("info", "task_completed")
        ThreadLocalLogger.unbind("task_id")

# Start workers
threads = [
    threading.Thread(target=worker_thread, args=(i,))
    for i in range(4)
]
for t in threads:
    t.start()
```

### Async Context Variables

```python
import asyncio
from contextvars import ContextVar

# Context variables work across async boundaries
trace_context: ContextVar[str] = ContextVar("trace_id")

async def process_with_context(trace_id: str):
    """Process with trace context."""
    trace_context.set(trace_id)
    
    # Context is preserved across await
    await logger.ainfo("processing_started", 
                      trace_id=trace_context.get())
    
    # Even across task boundaries
    await asyncio.gather(
        subtask_a(),
        subtask_b(),
        subtask_c()
    )

async def subtask_a():
    """Subtask automatically has trace context."""
    trace_id = trace_context.get()
    await logger.ainfo("subtask_a_executed", trace_id=trace_id)
```

## Global Context

### Application-Wide Context

```python
from provide.foundation import logger
from provide.foundation.config import Config

class GlobalContext:
    """Manage global logging context."""
    
    _instance = None
    _context = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def set(self, **kwargs):
        """Set global context values."""
        self._context.update(kwargs)
        self._apply_context()
    
    def remove(self, *keys):
        """Remove global context keys."""
        for key in keys:
            self._context.pop(key, None)
        self._apply_context()
    
    def clear(self):
        """Clear all global context."""
        self._context.clear()
        self._apply_context()
    
    def _apply_context(self):
        """Apply context to logger."""
        # Re-bind logger with updated context
        global logger
        logger = logger.bind(**self._context)

# Initialize global context at startup
global_context = GlobalContext()
global_context.set(
    application="my-app",
    version="1.2.3",
    deployment="blue",
    region="us-west-2",
    instance_id=get_instance_id()
)

# All logs now include global context
logger.info("application_started")
```

### Environment-Based Context

```python
import os
from typing import Any

def load_env_context() -> dict[str, Any]:
    """Load context from environment variables."""
    context = {}
    
    # Standard environment context
    if "PROVIDE_ENV" in os.environ:
        context["environment"] = os.environ["PROVIDE_ENV"]
    
    if "PROVIDE_REGION" in os.environ:
        context["region"] = os.environ["PROVIDE_REGION"]
    
    if "PROVIDE_SERVICE" in os.environ:
        context["service"] = os.environ["PROVIDE_SERVICE"]
    
    # K8s environment
    if "KUBERNETES_POD_NAME" in os.environ:
        context["pod_name"] = os.environ["KUBERNETES_POD_NAME"]
        context["namespace"] = os.environ.get("KUBERNETES_NAMESPACE", "default")
    
    # AWS environment
    if "AWS_REGION" in os.environ:
        context["aws_region"] = os.environ["AWS_REGION"]
    
    if "AWS_EXECUTION_ENV" in os.environ:
        context["aws_env"] = os.environ["AWS_EXECUTION_ENV"]
    
    return context

# Apply environment context at startup
env_context = load_env_context()
logger = logger.bind(**env_context)
```

## Context Propagation

### HTTP Request Context

```python
from flask import Flask, request, g
import uuid

app = Flask(__name__)

@app.before_request
def setup_request_context():
    """Setup context for each request."""
    # Generate or extract request ID
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    # Extract user context
    user_id = request.headers.get("X-User-ID")
    
    # Store in Flask's g object
    g.request_logger = logger.bind(
        request_id=request_id,
        user_id=user_id,
        method=request.method,
        path=request.path,
        remote_addr=request.remote_addr
    )
    
    g.request_logger.info("request_started")

@app.after_request
def log_response(response):
    """Log response with context."""
    if hasattr(g, "request_logger"):
        g.request_logger.info("request_completed",
                             status=response.status_code)
    return response

@app.route("/api/process")
def process():
    """Endpoint using request context."""
    g.request_logger.info("processing_data")
    
    # Context is available throughout request
    result = perform_processing()
    
    g.request_logger.info("processing_complete", 
                         result_size=len(result))
    return result
```

### Distributed Tracing Context

```python
from typing import Optional
import json

class TraceContext:
    """W3C Trace Context propagation."""
    
    def __init__(self, 
                 trace_id: str = None,
                 parent_id: str = None,
                 trace_flags: int = 0):
        self.trace_id = trace_id or self.generate_trace_id()
        self.parent_id = parent_id
        self.span_id = self.generate_span_id()
        self.trace_flags = trace_flags
    
    @staticmethod
    def generate_trace_id() -> str:
        """Generate 128-bit trace ID."""
        return uuid.uuid4().hex
    
    @staticmethod
    def generate_span_id() -> str:
        """Generate 64-bit span ID."""
        return uuid.uuid4().hex[:16]
    
    @classmethod
    def from_headers(cls, headers: dict) -> Optional["TraceContext"]:
        """Extract trace context from HTTP headers."""
        traceparent = headers.get("traceparent")
        if not traceparent:
            return None
        
        # Parse W3C traceparent header
        parts = traceparent.split("-")
        if len(parts) != 4:
            return None
        
        version, trace_id, parent_id, flags = parts
        return cls(
            trace_id=trace_id,
            parent_id=parent_id,
            trace_flags=int(flags, 16)
        )
    
    def to_headers(self) -> dict[str, str]:
        """Convert to HTTP headers."""
        traceparent = f"00-{self.trace_id}-{self.span_id}-{self.trace_flags:02x}"
        return {"traceparent": traceparent}
    
    def child_context(self) -> "TraceContext":
        """Create child context for nested operations."""
        return TraceContext(
            trace_id=self.trace_id,
            parent_id=self.span_id,
            trace_flags=self.trace_flags
        )

# Middleware for trace context
def trace_context_middleware(app):
    """Add trace context to all requests."""
    
    @app.before_request
    def setup_trace_context():
        # Extract or create trace context
        trace_ctx = TraceContext.from_headers(request.headers)
        if not trace_ctx:
            trace_ctx = TraceContext()
        
        # Bind to logger
        g.logger = logger.bind(
            trace_id=trace_ctx.trace_id,
            span_id=trace_ctx.span_id,
            parent_id=trace_ctx.parent_id
        )
        
        g.trace_context = trace_ctx
    
    @app.after_request
    def add_trace_headers(response):
        # Propagate trace context
        if hasattr(g, "trace_context"):
            for key, value in g.trace_context.to_headers().items():
                response.headers[key] = value
        return response
```

### Message Queue Context

```python
import json
from typing import Any

class MessageContext:
    """Context propagation for message queues."""
    
    @staticmethod
    def inject_context(message: dict[str, Any], 
                      context: dict[str, Any]) -> dict[str, Any]:
        """Inject context into message."""
        return {
            **message,
            "_context": context,
            "_timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def extract_context(message: dict[str, Any]) -> dict[str, Any]:
        """Extract context from message."""
        return message.get("_context", {})

# Producer
def send_message(queue, data: dict, **context):
    """Send message with context."""
    current_context = {
        "trace_id": get_current_trace_id(),
        "user_id": get_current_user_id(),
        **context
    }
    
    message = MessageContext.inject_context(data, current_context)
    
    logger.info("message_sent",
               queue=queue,
               **current_context)
    
    queue.send(json.dumps(message))

# Consumer
def process_message(message_str: str):
    """Process message with extracted context."""
    message = json.loads(message_str)
    context = MessageContext.extract_context(message)
    
    # Bind context for processing
    with logger.bind(**context):
        logger.info("message_received")
        
        # Process with context
        result = handle_message(message)
        
        logger.info("message_processed")
        return result
```

## Context Inheritance

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
