# Advanced Context Patterns

Sophisticated context management including global context and propagation.

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

