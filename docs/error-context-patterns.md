# Error Context Patterns

## Understanding Error Context Scope

Each error instance has its own context - this is by design and ensures errors are independent:

```python
# Each error has its own context
error1 = NetworkError("Failed to connect")
error1.add_context("host", "api.example.com")

error2 = NetworkError("Timeout")
error2.add_context("host", "db.example.com")

# error1.context = {"host": "api.example.com"}
# error2.context = {"host": "db.example.com"}
# These are completely independent
```

## Common Patterns for Context Management

### 1. Request-Scoped Context with ContextVars

For web applications or services where you want all errors within a request to share common context:

```python
from contextvars import ContextVar
from provide.foundation import FoundationError

# Define request-scoped context
request_context = ContextVar('request_context', default={})

def set_request_context(**kwargs):
    """Set context for current request."""
    ctx = request_context.get().copy()
    ctx.update(kwargs)
    request_context.set(ctx)

def create_error(error_class, message: str, **kwargs):
    """Create error with request context included."""
    error = error_class(message, **kwargs)
    error.context.update(request_context.get())
    return error

# Usage in request handler
def handle_request(request_id: str, user_id: int):
    # Set request context at start
    set_request_context(request_id=request_id, user_id=user_id)
    
    try:
        # Any error created will have request context
        if not authorized:
            raise create_error(
                AuthorizationError,
                "Access denied",
                resource="admin_panel"
            )
    except Exception as e:
        # Error automatically has request_id and user_id in context
        logger.error("Request failed", **e.to_dict())
```

### 2. Error Chain Context Propagation

When creating related errors, propagate context from parent to child:

```python
def chain_error(parent: FoundationError, error_class, message: str, **extra):
    """Create chained error that inherits parent context."""
    child = error_class(message, cause=parent, **extra)
    # Inherit parent context
    for key, value in parent.context.items():
        if key not in child.context:  # Don't override child's context
            child.context[key] = value
    return child

# Usage
try:
    fetch_user_data()
except NetworkError as e:
    # Create higher-level error that keeps network context
    raise chain_error(
        e,
        IntegrationError,
        "User service unavailable",
        service="user-service"
    )
```

### 3. Error Factory for Consistent Context

Create errors with consistent context across a module or service:

```python
class ServiceErrorFactory:
    """Factory for creating errors with service context."""
    
    def __init__(self, service_name: str, version: str):
        self.base_context = {
            "service.name": service_name,
            "service.version": version,
        }
    
    def create(self, error_class, message: str, **context):
        """Create error with service context."""
        error = error_class(message)
        error.context.update(self.base_context)
        error.context.update(context)
        return error
    
    def network_error(self, message: str, **context):
        """Convenience method for NetworkError."""
        return self.create(NetworkError, message, **context)
    
    def validation_error(self, message: str, field: str, **context):
        """Convenience method for ValidationError."""
        return self.create(ValidationError, message, field=field, **context)

# Usage
errors = ServiceErrorFactory("payment-api", "2.1.0")

# All errors will have service.name and service.version
raise errors.network_error(
    "Gateway timeout",
    host="payment-gateway.com",
    timeout=30
)
```

### 4. Middleware Pattern for Web Frameworks

For Flask, FastAPI, or similar frameworks:

```python
from provide.foundation import FoundationError
from provide.foundation.errors import capture_error_context

# Flask example
@app.errorhandler(FoundationError)
def handle_foundation_error(error):
    # Add request context to error
    error.add_context("http.method", request.method)
    error.add_context("http.path", request.path)
    error.add_context("http.remote_addr", request.remote_addr)
    
    # Log with full context
    logger.error(error.message, **error.to_dict())
    
    # Return JSON response
    return jsonify({
        "error": error.message,
        "code": error.code,
        "request_id": error.context.get("request_id")
    }), 500

# FastAPI example
@app.exception_handler(FoundationError)
async def foundation_error_handler(request: Request, error: FoundationError):
    # Add request context
    error.add_context("http.method", request.method)
    error.add_context("http.url", str(request.url))
    error.add_context("http.client", request.client.host)
    
    # Log and return response
    logger.error(error.message, **error.to_dict())
    return JSONResponse(
        status_code=500,
        content={
            "error": error.message,
            "code": error.code,
            "context": error.context
        }
    )
```

### 5. Decorator for Automatic Context

Add context automatically via decorators:

```python
from functools import wraps
from provide.foundation import FoundationError

def with_context(**context):
    """Decorator that adds context to any FoundationError raised."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FoundationError as e:
                # Add decorator context to error
                for key, value in context.items():
                    if key not in e.context:
                        e.context[key] = value
                raise
        return wrapper
    return decorator

# Usage
@with_context(module="user_service", operation="create_user")
def create_user(data):
    if not data.get("email"):
        raise ValidationError("Email required", field="email")
    # Any FoundationError raised will have module and operation context
```

### 6. Context Manager for Scoped Context

```python
from contextlib import contextmanager
from contextvars import ContextVar

error_context_var = ContextVar('error_context', default={})

@contextmanager
def error_context(**kwargs):
    """Context manager that adds context to errors in scope."""
    old_context = error_context_var.get()
    new_context = {**old_context, **kwargs}
    token = error_context_var.set(new_context)
    try:
        yield
    finally:
        error_context_var.reset(token)

class ContextAwareError(FoundationError):
    """Error that automatically includes scoped context."""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, **kwargs)
        self.context.update(error_context_var.get())

# Usage
with error_context(operation="batch_process", batch_id="batch_123"):
    for item in items:
        with error_context(item_id=item.id):
            # Errors here will have operation, batch_id, and item_id
            if not item.valid:
                raise ContextAwareError("Invalid item")
```

## Best Practices

1. **Keep context instance-specific** - Don't share context between error instances
2. **Use ContextVars for request scope** - Better than global variables
3. **Document context keys** - Use consistent namespacing (e.g., `http.*`, `db.*`)
4. **Don't mutate shared context** - Always copy before modifying
5. **Be mindful of sensitive data** - Don't include passwords, tokens in context

## Example: Complete Request Handler

```python
from contextvars import ContextVar
from provide.foundation import logger, FoundationError
from provide.foundation.errors import NetworkError, ValidationError

# Request-scoped context
request_ctx = ContextVar('request_ctx', default={})

def init_request_context(request_id: str, user_id: str = None):
    """Initialize request context."""
    request_ctx.set({
        "request.id": request_id,
        "request.timestamp": datetime.now().isoformat(),
        "user.id": user_id,
    })

def create_error(error_class, message: str, **kwargs):
    """Create error with request context."""
    error = error_class(message, **kwargs)
    error.context.update(request_ctx.get())
    return error

async def handle_api_request(request):
    # Initialize context for this request
    init_request_context(
        request_id=request.headers.get("X-Request-ID", str(uuid4())),
        user_id=request.user.id if request.user else None
    )
    
    try:
        # Validate input
        if not request.data.get("email"):
            raise create_error(
                ValidationError,
                "Email is required",
                field="email"
            )
        
        # Make external call
        try:
            result = await external_api.call(request.data)
        except TimeoutError as e:
            raise create_error(
                NetworkError,
                "External API timeout",
                service="external_api",
                timeout=30,
                cause=e
            )
        
        return {"success": True, "data": result}
        
    except FoundationError as e:
        # Error already has request context
        logger.error(e.message, **e.to_dict())
        return {"error": e.message, "code": e.code}, 400
```

## Summary

- **Error context is instance-specific** - Each error has its own context
- **Use ContextVars** for request-scoped context that all errors should include
- **Use factories or builders** for consistent error creation
- **Chain context** when creating related errors
- **Document your context keys** for consistency across the application