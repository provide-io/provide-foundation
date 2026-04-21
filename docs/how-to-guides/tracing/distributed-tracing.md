# How to Use Distributed Tracing

Foundation provides distributed tracing with optional OpenTelemetry integration.

## Quick Start

```python
from provide.foundation.tracer import with_span, get_current_trace_id
from provide.foundation import logger

@with_span("process_order")
def process_order(order_id: str):
    """Process an order with automatic tracing."""
    trace_id = get_current_trace_id()

    logger.info("processing_order", order_id=order_id, trace_id=trace_id)

    # Your logic here
    validate_order(order_id)
    charge_customer(order_id)
    ship_order(order_id)

    logger.info("order_processed", order_id=order_id, trace_id=trace_id)
```

## Manual Span Management

```python
from provide.foundation.tracer import Span, set_current_span, get_current_span

# Create span
span = Span(name="database_query", attributes={"table": "users"})
set_current_span(span)

try:
    # Your code
    result = execute_query()
    span.set_attribute("rows_returned", len(result))
except Exception as e:
    span.set_status(error=True, description=str(e))
    raise
finally:
    span.end()
```

## Trace Context

Access current trace context:

```python
from provide.foundation.tracer import get_trace_context, get_current_trace_id

# Get full trace context
context = get_trace_context()
print(f"Trace ID: {context.trace_id}")
print(f"Span ID: {context.span_id}")

# Or just get trace ID
trace_id = get_current_trace_id()
```

## OpenTelemetry Integration

Enable OpenTelemetry for full distributed tracing:

```python
from provide.foundation import get_hub, TelemetryConfig

config = TelemetryConfig(
    service_name="my-service",
    tracing_enabled=True,
    otlp_endpoint="http://localhost:4317"
)

hub = get_hub()
hub.initialize_foundation(config)

# Traces automatically exported to OTLP endpoint
```

## Environment Configuration

```bash
# Enable tracing
export PROVIDE_TRACING_ENABLED=true

# Set OTLP endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Set service name
export OTEL_SERVICE_NAME=my-service

# Set trace sample rate
export PROVIDE_TRACE_SAMPLE_RATE=1.0  # 100% sampling
```

## Best Practices

### ✅ DO: Add Meaningful Attributes

```python
# ✅ Good: Rich span attributes
@with_span("process_payment", attributes={
    "payment_method": "card",
    "currency": "USD"
})
def process_payment(amount: float):
    pass
```

### ✅ DO: Propagate Trace Context

```python
# ✅ Good: Include trace_id in logs
from provide.foundation.tracer import get_current_trace_id
from provide.foundation import logger

trace_id = get_current_trace_id()
logger.info("operation_completed", trace_id=trace_id)
```

## Next Steps

- **[Logging](../logging/basic-logging.md)**: Combine tracing with logging
- **[Metrics](../observability/metrics.md)**: Complete observability stack

---

**Tip**: See `examples/tracing/` for complete examples of distributed tracing.
