# Distributed Tracing Guide

`provide.foundation`'s tracer module provides lightweight distributed tracing for tracking operations across your applications.

## Overview

Distributed tracing helps you:

- 🔍 **Track request flows** across multiple services and components
- ⏱️ **Measure operation timings** and identify bottlenecks
- 🐛 **Debug complex interactions** by following execution paths

Foundation's tracer is designed to be:
- **Lightweight**: Minimal performance overhead
- **Simple**: Easy to instrument existing code

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

    # ... do work ...
    # Span automatically finished, even if exception occurs
```

### Helper Function

```python
from provide.foundation.tracer.context import SpanContext

# Creates child spans automatically
def process_order():
    with SpanContext("order_processing") as span:
        span.set_tag("order_id", "ord_123")

        # This creates a child span
        with SpanContext("payment_processing") as payment_span:
            payment_span.set_tag("amount", 99.99)
            # ... process payment ...

        # This creates another child span
        with SpanContext("inventory_update") as inventory_span:
            inventory_span.set_tag("items_count", 3)
            # ... update inventory ...
```

## Integration with Logging

Combine tracing with structured logging for comprehensive observability:

```python
from provide.foundation import logger
from provide.foundation.tracer.context import SpanContext, get_current_trace_id

def traced_operation(user_id: str):
    with SpanContext("user_operation") as span:
        trace_id = get_current_trace_id()

        span.set_tag("user_id", user_id)

        # Include trace context in logs
        logger.info("operation_started",
                   trace_id=trace_id,
                   span_id=span.span_id,
                   user_id=user_id)

        try:
            # ... perform operation ...
            logger.info("operation_completed",
                       trace_id=trace_id,
                       span_id=span.span_id)

        except Exception as e:
            span.set_error(e)
            logger.error("operation_failed",
                        trace_id=trace_id,
                        span_id=span.span_id,
                        error=str(e),
                        error_type=type(e).__name__)
            raise
```

## Next Steps

- 📖 Review the complete [Tracer API Reference](../../api/reference/provide/foundation/tracer/index.md)
- 🔗 Learn about [Logger Integration](../logging/advanced.md)