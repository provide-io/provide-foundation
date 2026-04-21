# Structured Events

Learn how to use structured event logging with Domain-Action-Status patterns for better observability.

## Overview

Structured events provide a consistent way to log important application events with rich context that's both human-readable and machine-parseable. Foundation's Domain-Action-Status (DAS) pattern creates predictable, searchable log events that work seamlessly with log aggregation systems.

**Key benefits:**
- **Searchability** - Consistent naming makes events easy to find
- **Aggregation** - Group related events for metrics
- **Alerting** - Pattern-based alerts on event types
- **Analysis** - Query and analyze event patterns
- **Debugging** - Rich context for troubleshooting

## Basic Event Logging

Use structured key-value pairs to capture event context:

```python
from provide.foundation import logger

# Simple event with context
logger.info(
    "user_login",
    user_id="user_123",
    source="web_app",
    ip_address="192.168.1.100"
)

# Event with duration
logger.info(
    "api_request_completed",
    endpoint="/users",
    method="GET",
    duration_ms=45,
    status_code=200
)
```

**Output:**
```json
{
  "event": "user_login",
  "user_id": "user_123",
  "source": "web_app",
  "ip_address": "192.168.1.100",
  "timestamp": "2025-10-24T10:00:00Z",
  "level": "info"
}
```

## Domain-Action-Status Pattern

The DAS pattern organizes events into three components:

- **Domain** - System area (auth, payment, api, database)
- **Action** - What happened (login, process, request, query)
- **Status** - Outcome (success, failed, started, completed)

### Pattern Format

```
{domain}_{action}_{status}
```

### Authentication Domain

Track authentication events:

```python
# Login events
logger.info("auth_login_success", user_id="user_123", duration_ms=45)
logger.warning("auth_login_failed", username="alice", reason="invalid_password")
logger.info("auth_login_started", username="alice", source="mobile_app")

# Logout events
logger.info("auth_logout_success", user_id="user_123", session_duration_s=3600)

# Token events
logger.info("auth_token_issued", user_id="user_123", token_type="jwt", ttl_s=3600)
logger.warning("auth_token_expired", user_id="user_123", token_id="tok_456")
logger.error("auth_token_invalid", token_id="tok_789", reason="signature_mismatch")

# Password events
logger.info("auth_password_changed", user_id="user_123")
logger.warning("auth_password_reset_requested", email="user@example.com")
```

### Payment Domain

Track payment processing:

```python
# Payment lifecycle
logger.info(
    "payment_process_started",
    order_id="ORD-123",
    amount=99.99,
    currency="USD",
    payment_method="credit_card"
)

logger.info(
    "payment_process_success",
    order_id="ORD-123",
    transaction_id="txn_456",
    amount=99.99,
    duration_ms=1234
)

logger.error(
    "payment_process_failed",
    order_id="ORD-123",
    amount=99.99,
    reason="insufficient_funds",
    error_code="E1001"
)

# Refund events
logger.info("payment_refund_initiated", transaction_id="txn_456", amount=99.99)
logger.info("payment_refund_completed", refund_id="ref_789", amount=99.99)

# Fraud detection
logger.warning(
    "payment_fraud_detected",
    order_id="ORD-123",
    user_id="user_123",
    risk_score=0.95,
    rules_triggered=["velocity", "location"]
)
```

### API Domain

Track API requests and responses:

```python
# Request lifecycle
logger.info(
    "api_request_started",
    endpoint="/users",
    method="GET",
    request_id="req_123"
)

logger.info(
    "api_request_completed",
    endpoint="/users",
    method="GET",
    status_code=200,
    duration_ms=45,
    request_id="req_123"
)

logger.error(
    "api_request_failed",
    endpoint="/users",
    method="POST",
    status_code=500,
    error="database_unavailable",
    request_id="req_456"
)

# Rate limiting
logger.warning(
    "api_ratelimit_exceeded",
    user_id="user_123",
    endpoint="/users",
    limit=100,
    window_s=60
)

# Validation errors
logger.warning(
    "api_validation_failed",
    endpoint="/users",
    field="email",
    error="invalid_format",
    value="not-an-email"
)
```

### Database Domain

Track database operations:

```python
# Query events
logger.debug("database_query_started", table="users", operation="SELECT")

logger.debug(
    "database_query_completed",
    table="users",
    operation="SELECT",
    rows_returned=10,
    duration_ms=23
)

logger.warning(
    "database_query_slow",
    table="orders",
    operation="SELECT",
    duration_ms=5000,  # Over 5 seconds
    rows_returned=10000
)

# Connection events
logger.info("database_connection_opened", host="db.example.com", port=5432)
logger.warning("database_connection_failed", host="db.example.com", error="timeout")
logger.info("database_connection_closed", duration_s=3600)

# Transaction events
logger.debug("database_transaction_started", isolation_level="READ_COMMITTED")
logger.info("database_transaction_committed", changes=5, duration_ms=100)
logger.warning("database_transaction_rollback", reason="constraint_violation")
```

## Event Enrichment

Add contextual data to all events in a scope:

### Context Binding

```python
from provide.foundation import logger

# Bind request context
request_logger = logger.bind(
    request_id="req_123",
    user_id="user_123",
    session_id="sess_456"
)

# All subsequent logs include bound context
request_logger.info("page_view", page="/dashboard")
request_logger.info("action_taken", action="export_report")
request_logger.info("page_exit", time_on_page_s=45)
```

**Output:**
```json
{
  "event": "page_view",
  "page": "/dashboard",
  "request_id": "req_123",
  "user_id": "user_123",
  "session_id": "sess_456"
}
```

### Correlation IDs

Track requests across services:

```python
import uuid

def process_request(request):
    """Process request with correlation tracking."""
    # Get or generate correlation ID
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

    # Bind to logger
    log = logger.bind(correlation_id=correlation_id)

    log.info("request_received", path=request.path, method=request.method)

    try:
        result = handle_request(request)
        log.info("request_completed", status="success")
        return result
    except Exception as e:
        log.error("request_failed", error=str(e))
        raise
```

### User Context

Add user information to events:

```python
def with_user_context(user_id: str):
    """Create logger with user context."""
    return logger.bind(
        user_id=user_id,
        user_role=get_user_role(user_id),
        tenant_id=get_tenant_id(user_id)
    )

# Usage
user_log = with_user_context("user_123")
user_log.info("feature_accessed", feature="export")
user_log.info("data_downloaded", format="csv", rows=1000)
```

## Event Schemas

Define consistent event structures:

### Order Events Schema

```python
from typing import TypedDict

class OrderEvent(TypedDict):
    """Schema for order-related events."""
    order_id: str
    customer_id: str
    total_amount: float
    currency: str
    items_count: int
    status: str

def log_order_event(action: str, status: str, order_data: OrderEvent):
    """Log order event with consistent schema."""
    logger.info(
        f"order_{action}_{status}",
        order_id=order_data["order_id"],
        customer_id=order_data["customer_id"],
        total_amount=order_data["total_amount"],
        currency=order_data["currency"],
        items_count=order_data["items_count"],
        order_status=order_data["status"]
    )

# Usage
order = OrderEvent(
    order_id="ORD-123",
    customer_id="cust_456",
    total_amount=99.99,
    currency="USD",
    items_count=3,
    status="pending"
)

log_order_event("create", "success", order)
log_order_event("process", "started", order)
log_order_event("fulfill", "completed", order)
```

### Error Events Schema

```python
from dataclasses import dataclass

@dataclass
class ErrorContext:
    """Schema for error events."""
    error_type: str
    error_message: str
    error_code: str | None = None
    stack_trace: str | None = None
    user_id: str | None = None
    request_id: str | None = None

def log_error_event(domain: str, action: str, error: ErrorContext):
    """Log error event with consistent schema."""
    logger.error(
        f"{domain}_{action}_failed",
        error_type=error.error_type,
        error_message=error.error_message,
        error_code=error.error_code,
        user_id=error.user_id,
        request_id=error.request_id,
        exc_info=error.stack_trace
    )

# Usage
try:
    process_payment(order)
except PaymentError as e:
    log_error_event(
        "payment",
        "process",
        ErrorContext(
            error_type="PaymentError",
            error_message=str(e),
            error_code="E1001",
            user_id=order.customer_id,
            request_id=current_request_id()
        )
    )
```

## Event Metrics

Track event counts and patterns:

### Event Counter

```python
from collections import defaultdict
from datetime import datetime, timedelta

class EventMetrics:
    """Track event metrics."""

    def __init__(self):
        self.events = defaultdict(int)
        self.last_reset = datetime.now()

    def record_event(self, event_name: str):
        """Record event occurrence."""
        self.events[event_name] += 1

        # Log event
        logger.info(
            event_name,
            event_count=self.events[event_name],
            time_since_reset=(datetime.now() - self.last_reset).total_seconds()
        )

    def get_metrics(self) -> dict[str, int]:
        """Get event counts."""
        return dict(self.events)

    def reset(self):
        """Reset counters."""
        self.events.clear()
        self.last_reset = datetime.now()

# Usage
metrics = EventMetrics()

metrics.record_event("api_request_completed")
metrics.record_event("api_request_completed")
metrics.record_event("api_request_failed")

# Get summary
logger.info("metrics_summary", metrics=metrics.get_metrics())
```

### Event Timing

```python
import time
from contextlib import contextmanager

@contextmanager
def timed_event(event_name: str, **context):
    """Context manager for timed events."""
    start = time.time()

    logger.info(f"{event_name}_started", **context)

    try:
        yield
        duration_ms = (time.time() - start) * 1000
        logger.info(
            f"{event_name}_completed",
            duration_ms=duration_ms,
            **context
        )
    except Exception as e:
        duration_ms = (time.time() - start) * 1000
        logger.error(
            f"{event_name}_failed",
            duration_ms=duration_ms,
            error=str(e),
            **context
        )
        raise

# Usage
with timed_event("database_query", table="users", operation="SELECT"):
    results = db.query("SELECT * FROM users WHERE active = true")

with timed_event("api_call", endpoint="/users", method="GET"):
    response = http_client.get("/users")
```

## Multi-Domain Events

Track events spanning multiple domains:

### Order Fulfillment Flow

```python
def fulfill_order(order_id: str):
    """Fulfill order with comprehensive event logging."""
    log = logger.bind(order_id=order_id)

    # Order domain
    log.info("order_fulfill_started")

    try:
        # Payment domain
        log.info("payment_charge_started")
        payment = process_payment(order_id)
        log.info("payment_charge_success", transaction_id=payment.id)

        # Inventory domain
        log.info("inventory_reserve_started")
        reservation = reserve_inventory(order_id)
        log.info("inventory_reserve_success", reservation_id=reservation.id)

        # Shipping domain
        log.info("shipping_create_started")
        shipment = create_shipment(order_id)
        log.info("shipping_create_success", tracking_number=shipment.tracking)

        # Notification domain
        log.info("notification_send_started", type="order_confirmation")
        send_confirmation_email(order_id)
        log.info("notification_send_success")

        # Final order status
        log.info("order_fulfill_completed", status="shipped")

    except PaymentError as e:
        log.error("payment_charge_failed", error=str(e))
        log.error("order_fulfill_failed", reason="payment_failed")
        raise
    except InventoryError as e:
        log.error("inventory_reserve_failed", error=str(e))
        log.error("order_fulfill_failed", reason="out_of_stock")
        raise
```

## Event Querying Patterns

Structure events for easy querying:

### Searchable Events

```python
# Events designed for search
logger.info(
    "user_action",
    action_type="purchase",  # Filterable
    category="electronics",  # Facetable
    amount=99.99,           # Aggregatable
    user_segment="premium",  # Groupable
    ab_test_variant="B"     # Analyzable
)

# Query examples (in log aggregation system):
# - All purchases: event:"user_action" AND action_type:"purchase"
# - Total revenue: SUM(amount) WHERE action_type:"purchase"
# - By category: GROUP BY category WHERE action_type:"purchase"
# - A/B test: GROUP BY ab_test_variant WHERE action_type:"purchase"
```

### Time-Based Events

```python
from datetime import datetime

logger.info(
    "session_activity",
    session_id="sess_123",
    user_id="user_456",
    activity_type="page_view",
    page="/dashboard",
    timestamp_iso=datetime.now().isoformat(),
    hour_of_day=datetime.now().hour,
    day_of_week=datetime.now().strftime("%A")
)

# Enables queries like:
# - Peak hours: GROUP BY hour_of_day
# - Weekly patterns: GROUP BY day_of_week
# - Time series: ORDER BY timestamp_iso
```

## Production Patterns

### High-Volume Events

For high-throughput scenarios, use sampling:

```python
import random

def log_high_volume_event(event_name: str, sample_rate: float = 0.01, **context):
    """Log event with sampling for high volumes."""
    if random.random() < sample_rate:
        logger.info(
            event_name,
            sampled=True,
            sample_rate=sample_rate,
            **context
        )

# Only log 1% of cache hits
log_high_volume_event("cache_hit", sample_rate=0.01, key="user:123")

# Always log cache misses
logger.info("cache_miss", key="user:123")
```

### Event Batching

Batch events for efficiency:

```python
from typing import Any

class EventBatcher:
    """Batch events for efficient logging."""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.batch: list[dict[str, Any]] = []

    def add_event(self, event_name: str, **context):
        """Add event to batch."""
        self.batch.append({"event": event_name, **context})

        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        """Flush batch to logs."""
        if self.batch:
            logger.info(
                "events_batch",
                event_count=len(self.batch),
                events=self.batch
            )
            self.batch.clear()

# Usage
batcher = EventBatcher(batch_size=100)

for item in process_items():
    batcher.add_event("item_processed", item_id=item.id, status="success")

batcher.flush()  # Flush remaining events
```

### Sensitive Data Masking

Mask sensitive information in events:

```python
import re

def mask_email(email: str) -> str:
    """Mask email for logging."""
    if "@" not in email:
        return "***"
    username, domain = email.split("@")
    return f"{username[0]}***@{domain}"

def mask_credit_card(card: str) -> str:
    """Mask credit card number."""
    return f"****-****-****-{card[-4:]}"

logger.info(
    "payment_process_started",
    user_email=mask_email("user@example.com"),  # u***@example.com
    card_number=mask_credit_card("4111111111111111"),  # ****-****-****-1111
    amount=99.99
)
```

## Best Practices

### ✅ DO: Use Consistent Naming

```python
# ✅ Good: Consistent DAS pattern
logger.info("auth_login_success")
logger.info("auth_logout_success")
logger.info("auth_token_issued")

# ❌ Bad: Inconsistent naming
logger.info("user_logged_in")
logger.info("logout_successful")
logger.info("token_created")
```

### ✅ DO: Include Rich Context

```python
# ✅ Good: Detailed context
logger.info(
    "order_created",
    order_id="ORD-123",
    customer_id="cust_456",
    total_amount=99.99,
    items_count=3,
    payment_method="credit_card"
)

# ❌ Bad: Minimal context
logger.info("order_created", order_id="ORD-123")
```

### ✅ DO: Use Appropriate Log Levels

```python
# ✅ Good: Correct severity
logger.debug("cache_hit", key="user:123")  # Low importance
logger.info("user_login_success", user_id="123")  # Normal operation
logger.warning("api_ratelimit_exceeded", user_id="123")  # Concerning
logger.error("payment_process_failed", order_id="ORD-123")  # Error
logger.critical("database_connection_lost")  # Critical failure

# ❌ Bad: Everything at same level
logger.info("cache_hit")  # Too noisy
logger.info("database_connection_lost")  # Too quiet
```

### ✅ DO: Structure for Searchability

```python
# ✅ Good: Structured for queries
logger.info(
    "api_request_completed",
    endpoint="/users",
    method="GET",
    status_code=200,
    duration_ms=45
)

# ❌ Bad: String concatenation
logger.info("API GET /users completed in 45ms with status 200")
```

### ❌ DON'T: Log Sensitive Data

```python
# ❌ Bad: Exposes sensitive data
logger.info("auth_login_success", password="secret123")

# ✅ Good: Masked or omitted
logger.info("auth_login_success", user_id="123")  # No password
```

### ❌ DON'T: Use Dynamic Event Names

```python
# ❌ Bad: Dynamic event names (hard to search)
logger.info(f"user_{action}_completed")  # Changes per action

# ✅ Good: Static event names with context
logger.info("user_action_completed", action=action)
```

## Event Catalog

Maintain an event catalog for your application:

```python
# events.py
class Events:
    """Centralized event definitions."""

    # Authentication
    AUTH_LOGIN_SUCCESS = "auth_login_success"
    AUTH_LOGIN_FAILED = "auth_login_failed"
    AUTH_LOGOUT_SUCCESS = "auth_logout_success"

    # Payments
    PAYMENT_PROCESS_STARTED = "payment_process_started"
    PAYMENT_PROCESS_SUCCESS = "payment_process_success"
    PAYMENT_PROCESS_FAILED = "payment_process_failed"

    # API
    API_REQUEST_STARTED = "api_request_started"
    API_REQUEST_COMPLETED = "api_request_completed"
    API_REQUEST_FAILED = "api_request_failed"

# Usage
from events import Events

logger.info(Events.AUTH_LOGIN_SUCCESS, user_id="123")
logger.error(Events.PAYMENT_PROCESS_FAILED, order_id="ORD-123")
```

## Next Steps

### Related Guides
- **[Basic Logging](basic-logging.md)**: Core logging patterns
- **[Exception Logging](exception-logging.md)**: Error logging with context
- **[Custom Processors](custom-processors.md)**: Extend logging with processors

### Examples
- See `examples/telemetry/04_das_pattern.py` for DAS pattern examples
- See `examples/production/01_production_patterns.py` for production event patterns

### API Reference
- **[API Reference: Logger](../../reference/provide/foundation/logger/index.md)**: Complete logger API

---

**Tip**: Start with basic DAS naming (domain_action_status) and add rich context. Use log aggregation queries to validate your event structure is searchable and useful.
