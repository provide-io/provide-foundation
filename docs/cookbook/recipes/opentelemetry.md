# OpenTelemetry Integration

Seamlessly extend provide.foundation with OpenTelemetry for distributed tracing, metrics, and observability.

## Overview

provide.foundation's emoji sets are designed to **enhance OpenTelemetry**, not replace it. You get:
- 🎯 OTEL-compliant field naming
- 👀 Visual emoji enhancement for local development
- 📊 Automatic span/metric enrichment
- 🔄 Seamless context propagation

## Quick Start

### Installation

```bash
pip install provide-foundation[opentelemetry]
```

### Basic Setup

```python
from provide.foundation import logger
from provide.foundation.otel import setup_otel

# Configure OTEL with emoji set enhancement
setup_otel(
    traces_endpoint="http://otel-collector:4317",
    metrics_endpoint="http://otel-collector:4317",
    service_name="my-service",
    semantic_layers=True,  # Enable semantic enrichment
)

# Use emoji sets - automatically exports to OTEL
logger.info("http_request",
    **{
        "http.method": "GET",           # OTEL standard field
        "http.status_code": 200,        # OTEL standard field
        "http.route": "/api/users",     # OTEL standard field
    }
)
# Local output: 📥 http_request method=GET status=200 ✅
# OTEL export: Full span with all attributes
```

## Distributed Tracing

### Automatic Trace Context

```python
from opentelemetry import trace
from provide.foundation import logger
from provide.foundation.otel import with_span

tracer = trace.get_tracer(__name__)

@with_span("process_order")
def process_order(order_id: str):
    """Process an order with distributed tracing."""
    
    # Semantic logging automatically enriches the current span
    logger.info("order_processing_started",
        order_id=order_id,
        **{"order.items_count": 5}  # Custom OTEL attribute
    )
    
    # Start a child span
    with tracer.start_as_current_span("validate_payment") as span:
        logger.info("payment_validation",
            **{
                "payment.method": "card",
                "payment.amount": 99.99,
            }
        )
    
    logger.info("order_processing_completed", order_id=order_id)

# Trace context is automatically propagated
process_order("ORD-123")
```

### Cross-Service Tracing

```python
import httpx
from provide.foundation.otel import inject_trace_context

async def call_payment_service(order_id: str):
    """Call payment service with trace context."""
    
    headers = {}
    inject_trace_context(headers)  # Add W3C trace headers
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://payment-service/charge",
            json={"order_id": order_id},
            headers=headers
        )
    
    # Log with emoji sets
    logger.info("payment_service_response",
        **{
            "http.status_code": response.status_code,
            "service.name": "payment-service",
            "rpc.method": "charge",
        }
    )
```

## Metrics Integration

### Automatic Metric Collection

```python
from provide.foundation.otel import setup_metrics
from provide.foundation import logger

# Setup metrics with emoji set integration
setup_metrics(
    export_interval_seconds=10,
    semantic_layer_metrics=True,  # Track layer usage
)

# Emoji sets automatically create metrics
logger.info("http_request",
    **{
        "http.method": "POST",
        "http.status_code": 201,
        "http.request.duration": 145.2,  # Auto-creates histogram
    }
)
# Creates metrics:
# - http_request_duration_histogram
# - http_requests_total (by method, status)
# - semantic_layer_usage (by layer name)
```

### Custom Metrics

```python
from opentelemetry import metrics
from provide.foundation import logger

meter = metrics.get_meter(__name__)
order_counter = meter.create_counter(
    "orders_processed",
    description="Total orders processed"
)

def process_order(order_id: str):
    # Log with emoji sets
    logger.info("order_processed",
        order_id=order_id,
        **{"order.total": 99.99}
    )
    
    # Update metrics
    order_counter.add(1, {"status": "success"})
```

## Semantic Layer Enhancement

### Visual Development, Standard Production

```python
from provide.foundation import logger
from provide.foundation.config import TelemetryConfig

# Development: Visual emoji logging
dev_config = TelemetryConfig(
    enable_emoji=True,
    format="pretty",
    enable_semantic_layers=True,
)

# Production: OTEL export without emoji
prod_config = TelemetryConfig(
    enable_emoji=False,
    format="json",
    enable_semantic_layers=True,
    otel_export=True,
)

# Same code, different output based on environment
logger.info("database_query",
    **{
        "db.system": "postgresql",      # OTEL standard
        "db.operation": "SELECT",       # OTEL standard
        "db.statement": "SELECT * FROM users",
    }
)

# Dev output: 🐘 database_query operation=SELECT ✅
# Prod output: {"db.system": "postgresql", ...} → OTEL
```

### Field Mapping & Validation

```python
from provide.foundation.emoji_sets import HTTP_EMOJI_SET

# Emoji sets validate OTEL fields
try:
    logger.info("http_request",
        **{
            "http.method": "INVALID",  # Will warn
            "http.status_code": "not_a_number",  # Will warn
        }
    )
except ValidationWarning as e:
    # In dev: Shows warning
    # In prod: Logs to error tracking
    pass

# Automatic field normalization
logger.info("http_request",
    **{
        "http.method": "get",  # Auto-uppercase to "GET"
        "http.url": "https://example.com/api/users",
        # Auto-extracts: http.scheme, http.host, http.target
    }
)
```

## Advanced Patterns

### Baggage Propagation

```python
from opentelemetry import baggage
from provide.foundation import logger

# Set baggage for cross-service context
baggage.set_baggage("user.id", "user-123")
baggage.set_baggage("tenant.id", "tenant-456")

# Emoji sets automatically include baggage
logger.info("service_call",
    service="downstream",
    # Baggage is automatically added to logs and spans
)
```

### Sampling with Semantic Awareness

```python
from provide.foundation.otel import SemanticSampler

# Sample based on emoji set fields
sampler = SemanticSampler(
    rules=[
        # Always sample errors
        {"http.status_code": lambda x: x >= 500, "sample_rate": 1.0},
        # Sample 10% of successful requests
        {"http.status_code": lambda x: x < 400, "sample_rate": 0.1},
        # Always sample LLM operations
        {"semantic_layer": "llm", "sample_rate": 1.0},
    ]
)

setup_otel(sampler=sampler)
```

### Export to Multiple Backends

```python
from provide.foundation.otel import setup_multi_export

# Export to multiple OTEL backends
setup_multi_export([
    {
        "name": "jaeger",
        "endpoint": "http://jaeger:4317",
        "export_types": ["traces"],
    },
    {
        "name": "prometheus",
        "endpoint": "http://prometheus:4317",
        "export_types": ["metrics"],
    },
    {
        "name": "elasticsearch",
        "endpoint": "http://elastic:4317",
        "export_types": ["logs"],
    },
])
```

## Testing with OTEL

```python
import pytest
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from provide.foundation import logger
from provide.foundation.otel import setup_test_otel

@pytest.fixture
def otel_test_setup():
    """Setup OTEL for testing."""
    exporter = InMemorySpanExporter()
    setup_test_otel(exporter=exporter)
    yield exporter
    exporter.clear()

def test_semantic_otel_integration(otel_test_setup):
    """Test that emoji sets create proper OTEL spans."""
    
    # Log with emoji sets
    logger.info("http_request",
        **{
            "http.method": "GET",
            "http.status_code": 200,
        }
    )
    
    # Verify OTEL span was created
    spans = otel_test_setup.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].attributes["http.method"] == "GET"
    assert spans[0].attributes["http.status_code"] == 200
    
    # Verify emoji set was applied
    events = spans[0].events
    assert any("📥" in event.name for event in events)  # Emoji was added
```

## Best Practices

### 1. Use OTEL Standard Fields

```python
# ✅ Good: Use OTEL standard fields
logger.info("request", **{
    "http.method": "GET",              # OTEL standard
    "http.status_code": 200,          # OTEL standard
    "http.request.body.size": 1024,   # OTEL standard
})

# ❌ Avoid: Custom field names when OTEL standard exists
logger.info("request", **{
    "method": "GET",           # Use http.method
    "status": 200,            # Use http.status_code
    "request_size": 1024,     # Use http.request.body.size
})
```

### 2. Layer Your Observability

```python
# Development: Full visual experience
if ENV == "development":
    setup_otel(
        semantic_layers=True,
        visual_logging=True,
        sample_rate=1.0,  # Sample everything locally
    )

# Staging: Visual + OTEL export
elif ENV == "staging":
    setup_otel(
        semantic_layers=True,
        visual_logging=True,
        export_endpoint="http://staging-otel:4317",
        sample_rate=0.5,
    )

# Production: Optimized OTEL export
else:
    setup_otel(
        semantic_layers=True,
        visual_logging=False,  # No emoji overhead
        export_endpoint="http://prod-otel:4317",
        sample_rate=0.1,  # Sample 10%
    )
```

### 3. Correlate Logs, Traces, and Metrics

```python
from provide.foundation import logger
from provide.foundation.otel import get_current_trace_id

# All telemetry includes trace context
logger.info("processing_started",
    trace_id=get_current_trace_id(),  # Automatic correlation
    **{"processing.items": 100}
)

# Metrics also include trace context
order_histogram.record(
    processing_time,
    {"trace_id": get_current_trace_id()}
)
```

## Troubleshooting

### OTEL Export Not Working

```python
from provide.foundation.otel import debug_otel

# Enable OTEL debug logging
debug_otel(enabled=True)

# Check export status
status = debug_otel.get_export_status()
print(f"Exported spans: {status['spans_exported']}")
print(f"Failed exports: {status['export_failures']}")
```

### Trace Context Lost

```python
# Ensure context propagation in async code
import contextvars
from provide.foundation.otel import trace_context_var

async def async_operation():
    # Preserve trace context
    ctx = trace_context_var.get()
    
    async with tracer.start_as_current_span("async_op"):
        logger.info("async_operation", context=ctx)
```

## Next Steps

- 📊 [Metrics Deep Dive](../patterns/monitoring.md)
- 🔍 [Distributed Tracing](../../tutorials/distributed-tracing.md)
- 🎯 [Performance Monitoring](../patterns/monitoring.md)
- 📖 [OTEL Specification](https://opentelemetry.io/docs/)