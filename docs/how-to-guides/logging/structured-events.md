# Structured Events

Learn how to use structured event logging with Domain-Action-Status patterns for better observability.

## Overview

Structured events provide a consistent way to log important application events with rich context that's both human-readable and machine-parseable.

## Basic Event Logging

Use structured key-value pairs to capture event context:

```python
from provide.foundation import logger

logger.info(
    "user_login",
    user_id="user_123",
    source="web_app",
    ip_address="192.168.1.100",
    emoji="🔐"
)
```

## Domain-Action-Status Pattern

Organize events using the DAS (Domain-Action-Status) pattern:

```python
# Domain: Authentication, Action: Login, Status: Success
logger.info("auth_login_success", user_id="user_123", duration_ms=45)

# Domain: Payment, Action: Process, Status: Failed
logger.error("payment_process_failed", order_id="ORD-456", reason="insufficient_funds")

# Domain: API, Action: Request, Status: Started
logger.debug("api_request_started", endpoint="/users", method="GET")
```

## Event Enrichment

Add contextual data to all events in a scope:

```python
# Bind context that applies to all subsequent log calls
logger = logger.bind(
    request_id="req_789",
    user_id="user_123",
    session_id="sess_456"
)

# All these logs will include the bound context
logger.info("page_view", page="/dashboard")
logger.info("action_taken", action="export_report")
```

## Next Steps

- **[Custom Processors](custom-processors.md)** - Create custom log processors
- **[Exception Logging](exception-logging.md)** - Handle errors effectively
- **[API Reference: Logger](../../reference/provide/foundation/logger/index.md)** - Complete logger API

---

**See also:** [examples/telemetry/04_das_pattern.py](https://github.com/provide-io/provide-foundation/blob/main/examples/telemetry/04_das_pattern.py)
