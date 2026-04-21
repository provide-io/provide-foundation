# How to Log Exceptions

Properly logging exceptions is crucial for debugging and operational visibility. `provide.foundation` provides simple and powerful ways to capture error context with full stack traces and structured metadata.

## Overview

Exception logging serves multiple purposes:
- **Debugging** - Understand what went wrong and where
- **Monitoring** - Alert on error rates and patterns
- **Auditing** - Track failures for compliance
- **Context** - Preserve relevant data for post-mortem analysis

Foundation's structured logging ensures exceptions are logged with rich context, making them easy to search, filter, and analyze in log aggregation systems.

## Basic Exception Logging

### Using `logger.exception()`

The `logger.exception()` method is the preferred way to log exceptions. It should be called from within an `except` block and automatically captures the full stack trace.

```python
from provide.foundation import logger

def risky_operation():
    raise ValueError("Something went wrong")

try:
    risky_operation()
except Exception:
    logger.exception(
        "Operation failed unexpectedly",
        operation_name="risky_operation",
        user_id="user_xyz",
    )
```

**Output includes:**
- Event message: "Operation failed unexpectedly"
- Structured fields: `operation_name`, `user_id`
- Full stack trace with file names and line numbers
- Exception type and message

### Using `logger.error()` with `exc_info`

For more control, you can use `logger.error()` and pass `exc_info=True` to include the traceback.

```python
try:
    risky_operation()
except Exception as e:
    logger.error(
        "Operation failed",
        exc_info=True,
        error_type=type(e).__name__,
        error_details=str(e),
    )
```

## Exception Logging Patterns

### Pattern 1: Log and Re-raise

Log the exception for visibility, then re-raise it for upstream handling:

```python
def process_payment(transaction):
    """Process payment with exception logging."""
    try:
        payment_gateway.charge(transaction)
    except PaymentError as e:
        logger.exception(
            "Payment processing failed",
            transaction_id=transaction.id,
            amount=transaction.amount,
            error_code=e.code,
        )
        raise  # Re-raise for caller to handle
```

**When to use:** When you want visibility at this layer but need upstream code to handle the error.

### Pattern 2: Log and Transform

Log the original exception, then raise a different exception type:

```python
from provide.foundation.errors import DatabaseError

def save_user(user_data):
    """Save user with exception transformation."""
    try:
        db.insert("users", user_data)
    except ConnectionError as e:
        logger.exception(
            "Database connection failed during user save",
            user_email=user_data.get("email"),
        )
        raise DatabaseError("Failed to save user") from e
```

**When to use:** When converting low-level exceptions to domain-specific exceptions.

### Pattern 3: Log and Handle

Log the exception and handle it completely (don't re-raise):

```python
def send_notification(user_id, message):
    """Send notification with graceful failure."""
    try:
        notification_service.send(user_id, message)
    except NotificationError as e:
        logger.exception(
            "Failed to send notification",
            user_id=user_id,
            notification_type=message.type,
        )
        # Don't raise - notification failure shouldn't break the flow
        return False
    return True
```

**When to use:** When the operation is optional or has a sensible fallback.

### Pattern 4: Log with Retry Context

Log exceptions within retry loops to track retry attempts:

```python
from provide.foundation.resilience import retry

@retry(NetworkError, max_attempts=3, base_delay=1.0)
def call_external_api(endpoint):
    """Call API with retry and exception logging."""
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.exception(
            "API call failed",
            endpoint=endpoint,
            status_code=getattr(e.response, 'status_code', None),
            attempt="will_retry",  # Retry decorator will retry
        )
        raise
```

## Adding Context to Exceptions

### User Context

Include user information for debugging user-specific issues:

```python
def process_user_action(user_id, action):
    """Process action with user context."""
    try:
        result = perform_action(action)
    except Exception:
        logger.exception(
            "User action failed",
            user_id=user_id,
            user_email=get_user_email(user_id),
            action_type=action.type,
            action_id=action.id,
            session_id=get_current_session_id(),
        )
        raise
```

### Request Context

Capture HTTP request details for API debugging:

```python
def handle_api_request(request):
    """Handle API request with request context."""
    try:
        response = process_request(request)
    except Exception:
        logger.exception(
            "API request processing failed",
            method=request.method,
            path=request.path,
            request_id=request.headers.get("X-Request-ID"),
            user_agent=request.headers.get("User-Agent"),
            client_ip=request.remote_addr,
        )
        raise
```

### Business Context

Add domain-specific information:

```python
def finalize_order(order):
    """Finalize order with business context."""
    try:
        payment_result = process_payment(order)
        inventory_result = reserve_inventory(order)
        ship_order(order)
    except Exception:
        logger.exception(
            "Order finalization failed",
            order_id=order.id,
            customer_id=order.customer_id,
            total_amount=order.total,
            order_status=order.status,
            payment_status=getattr(payment_result, 'status', 'unknown'),
            inventory_status=getattr(inventory_result, 'status', 'unknown'),
        )
        raise
```

## Correlation IDs

Use correlation IDs to track requests across multiple services:

```python
import uuid
from contextvars import ContextVar

# Global context variable for correlation ID
correlation_id: ContextVar[str] = ContextVar("correlation_id", default=None)

def set_correlation_id(cid=None):
    """Set correlation ID for current context."""
    if cid is None:
        cid = str(uuid.uuid4())
    correlation_id.set(cid)
    return cid

def get_correlation_id():
    """Get current correlation ID."""
    return correlation_id.get()

def api_handler(request):
    """API handler with correlation ID."""
    # Extract or generate correlation ID
    cid = request.headers.get("X-Correlation-ID") or set_correlation_id()

    try:
        result = process_request(request)
    except Exception:
        logger.exception(
            "Request processing failed",
            correlation_id=cid,
            request_path=request.path,
        )
        raise

    return result
```

**Benefits:**
- Track errors across microservices
- Correlate logs from different systems
- Debug distributed request flows

## Exception Aggregation Patterns

### Collecting Multiple Failures

When processing batches, collect all failures for comprehensive error reporting:

```python
from typing import NamedTuple

class ProcessingResult(NamedTuple):
    success_count: int
    failure_count: int
    errors: list

def process_batch(items):
    """Process batch and collect all failures."""
    successes = 0
    failures = 0
    errors = []

    for item in items:
        try:
            process_item(item)
            successes += 1
        except Exception as e:
            failures += 1
            errors.append({
                "item_id": item.id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            })
            logger.exception(
                "Item processing failed",
                item_id=item.id,
                batch_position=items.index(item),
            )

    # Log batch summary
    if failures > 0:
        logger.error(
            "Batch processing completed with failures",
            total_items=len(items),
            successes=successes,
            failures=failures,
            failure_rate=failures / len(items),
            errors=errors[:5],  # First 5 errors for visibility
        )

    return ProcessingResult(successes, failures, errors)
```

### Error Rate Tracking

Monitor error rates over time:

```python
from collections import deque
from datetime import datetime, timedelta

class ErrorRateTracker:
    """Track error rate over time window."""

    def __init__(self, window_seconds=60):
        self.window = timedelta(seconds=window_seconds)
        self.errors = deque()

    def record_error(self, exception):
        """Record an error occurrence."""
        now = datetime.now()
        self.errors.append((now, exception))

        # Remove old errors outside window
        cutoff = now - self.window
        while self.errors and self.errors[0][0] < cutoff:
            self.errors.popleft()

        # Log if error rate is high
        error_count = len(self.errors)
        if error_count > 10:  # More than 10 errors in window
            logger.warning(
                "High error rate detected",
                error_count=error_count,
                window_seconds=self.window.total_seconds(),
                recent_errors=[
                    type(e).__name__ for _, e in list(self.errors)[-5:]
                ],
            )

# Global tracker
error_tracker = ErrorRateTracker(window_seconds=60)

def monitored_operation():
    """Operation with error rate monitoring."""
    try:
        perform_operation()
    except Exception as e:
        error_tracker.record_error(e)
        logger.exception("Operation failed")
        raise
```

## Custom Exception Handlers

### Application-Wide Exception Handler

Set up a global exception handler for your application:

```python
import sys
from provide.foundation import logger

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions globally."""
    # Don't log KeyboardInterrupt
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical(
        "Uncaught exception",
        exc_type=exc_type.__name__,
        exc_message=str(exc_value),
        exc_info=(exc_type, exc_value, exc_traceback),
    )

# Install global handler
sys.excepthook = global_exception_handler
```

### Async Exception Handler

Handle exceptions in async code:

```python
import asyncio
from provide.foundation import logger

def async_exception_handler(loop, context):
    """Handle exceptions in async tasks."""
    exception = context.get("exception")
    message = context.get("message", "Async exception occurred")

    if exception:
        logger.exception(
            message,
            task=context.get("task"),
            future=context.get("future"),
        )
    else:
        logger.error(message, context=context)

# Set async exception handler
loop = asyncio.get_event_loop()
loop.set_exception_handler(async_exception_handler)
```

## Production Patterns

### Exception with Metric Tracking

Log exceptions and track metrics:

```python
from provide.foundation.metrics import Counter

# Define metrics
error_counter = Counter("app_errors_total", labels=["error_type", "operation"])

def tracked_operation(operation_name):
    """Operation with error tracking."""
    try:
        perform_operation()
    except Exception as e:
        error_type = type(e).__name__

        # Track metric
        error_counter.increment(labels={
            "error_type": error_type,
            "operation": operation_name,
        })

        # Log exception
        logger.exception(
            "Tracked operation failed",
            operation=operation_name,
            error_type=error_type,
        )
        raise
```

### Exception with Alerting

Trigger alerts for critical errors:

```python
def critical_operation():
    """Operation where failures trigger alerts."""
    try:
        result = perform_critical_task()
    except Exception as e:
        # Log with high severity
        logger.critical(
            "Critical operation failed - ALERT",
            operation="critical_task",
            severity="high",
            alert_team=True,  # Signal to monitoring system
            error_type=type(e).__name__,
        )

        # Send immediate notification
        send_pagerduty_alert(
            f"Critical operation failed: {type(e).__name__}",
            details=str(e),
        )

        raise
```

### Exception Sanitization

Sanitize sensitive data before logging:

```python
from provide.foundation.security import mask_secrets

def safe_exception_logging(user_data):
    """Log exceptions without exposing sensitive data."""
    try:
        process_user(user_data)
    except Exception:
        # Sanitize data before logging
        safe_data = {
            "user_id": user_data.get("user_id"),
            "email": mask_email(user_data.get("email")),
            "account_type": user_data.get("account_type"),
            # Exclude password, API keys, etc.
        }

        logger.exception(
            "User processing failed",
            user_data=safe_data,
        )
        raise

def mask_email(email):
    """Mask email for logging."""
    if not email or "@" not in email:
        return "***"
    username, domain = email.split("@")
    return f"{username[0]}***@{domain}"
```

## Best Practices

### ✅ DO: Always Preserve Stack Traces

```python
# ✅ Good: Preserves full stack trace
try:
    operation()
except Exception:
    logger.exception("Operation failed")
    raise

# ❌ Bad: Loses stack trace
try:
    operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")  # No traceback!
    raise
```

### ✅ DO: Add Structured Context

```python
# ✅ Good: Rich structured context
try:
    process_order(order)
except Exception:
    logger.exception(
        "Order processing failed",
        order_id=order.id,
        customer_id=order.customer_id,
        amount=order.total,
    )

# ❌ Bad: String concatenation loses structure
try:
    process_order(order)
except Exception:
    logger.exception(
        f"Order {order.id} for customer {order.customer_id} failed"
    )
```

### ✅ DO: Use Appropriate Log Levels

```python
# ✅ Good: Appropriate severity levels
try:
    optional_operation()
except Exception:
    logger.warning("Optional operation failed")  # Not critical

try:
    critical_operation()
except Exception:
    logger.critical("Critical operation failed")  # Needs immediate attention
```

### ❌ DON'T: Log the Same Exception Multiple Times

```python
# ❌ Bad: Logs exception at every layer
def layer1():
    try:
        layer2()
    except Exception:
        logger.exception("Layer 1 failed")
        raise

def layer2():
    try:
        operation()
    except Exception:
        logger.exception("Layer 2 failed")  # Duplicate!
        raise

# ✅ Good: Log once at the appropriate layer
def layer1():
    try:
        layer2()
    except Exception:
        logger.exception("Operation failed", layer="layer1")
        raise

def layer2():
    operation()  # Let exception propagate
```

### ❌ DON'T: Swallow Exceptions Silently

```python
# ❌ Bad: Silent failure
try:
    important_operation()
except Exception:
    pass  # Lost forever!

# ✅ Good: At minimum, log it
try:
    important_operation()
except Exception:
    logger.exception("Operation failed but continuing")
    # Explicitly choosing to continue
```

## Next Steps

### Related Guides
- **[Basic Logging](basic-logging.md)**: Core logging patterns
- **[Structured Events](structured-events.md)**: Event-driven logging

### Error Handling & Resilience
- **[Retry Patterns](../resilience/retry.md)**: Automatically retry failed operations
- **[Circuit Breakers](../resilience/circuit-breaker.md)**: Prevent cascading failures
- **[Production Monitoring](../production/monitoring.md)**: Production-focused error handling

### Examples
- See `examples/telemetry/05_exception_handling.py` for comprehensive exception logging examples
- See `examples/production/02_error_handling.py` for production error patterns

---

**Tip**: Always log exceptions with `logger.exception()` or `exc_info=True` to preserve stack traces. Add structured context fields to make errors searchable and debuggable.
