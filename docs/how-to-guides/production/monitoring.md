# Monitoring & Observability

Learn how to monitor Foundation applications in production with structured logging, metrics, tracing, and alerting.

## Overview

Production monitoring is essential for maintaining reliable services. Foundation provides built-in support for structured logging, metrics collection, distributed tracing, and integration with observability platforms. This guide shows you how to implement comprehensive monitoring for your applications.

**What you'll learn:**
- Configure structured JSON logging for log aggregation
- Collect and export application metrics
- Implement distributed tracing
- Set up health checks and readiness probes
- Integrate with observability platforms (Datadog, Grafana, etc.)
- Monitor performance and resource usage
- Create alerts and dashboards
- Troubleshoot production issues

**Key Features:**
- 📊 **Structured Logging**: JSON logs with semantic events
- 📈 **Metrics Collection**: Built-in counters, gauges, and histograms
- 🔍 **Distributed Tracing**: OpenTelemetry integration
- ❤️ **Health Checks**: Liveness and readiness endpoints
- 🚨 **Alerting**: Integration with PagerDuty, Slack, etc.
- 📉 **Dashboards**: Pre-built Grafana dashboards

## Prerequisites

```bash
# Core observability
uv add provide-foundation

# OpenTelemetry support
uv add provide-foundation[otel]

# Prometheus metrics export
uv add provide-foundation[prometheus]
```

## Structured Logging for Observability

### JSON Log Format

Enable JSON logging for log aggregation systems:

```python
from provide.foundation import get_hub, logger
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Configure JSON logging
hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name="my-service",
        logging=LoggingConfig(
            log_format="json",
            log_level="INFO"
        )
    )
)

# All logs are now JSON
logger.info(
    "user_login",
    user_id="user_123",
    source="web_app",
    duration_ms=45.2
)
```

**Output:**
```json
{
  "event": "user_login",
  "level": "info",
  "timestamp": "2025-10-24T17:30:00.000Z",
  "user_id": "user_123",
  "source": "web_app",
  "duration_ms": 45.2,
  "service": "my-service"
}
```

### Log Aggregation Integration

Configure for popular log aggregation platforms:

```python
import os
from provide.foundation import logger

# Environment-based configuration
environment = os.getenv("ENVIRONMENT", "dev")
service_name = os.getenv("SERVICE_NAME", "app")
version = os.getenv("APP_VERSION", "unknown")

# Add standard fields to all logs
def add_standard_fields(logger_instance, method_name, event_dict):
    """Add standard observability fields."""
    event_dict.update({
        "service": service_name,
        "version": version,
        "environment": environment,
        "host": os.getenv("HOSTNAME", "unknown")
    })
    return event_dict

hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name=service_name,
        logging=LoggingConfig(
            processors=[add_standard_fields],
            log_format="json"
        )
    )
)
```

### Semantic Event Logging

Use meaningful event names for better searchability:

```python
from provide.foundation import logger

# ✅ GOOD: Semantic event names (Domain-Action-Status pattern)
logger.info("http_request_completed", method="GET", path="/api/users", status=200, duration_ms=123)
logger.error("database_query_failed", query="SELECT * FROM users", error="connection timeout")
logger.info("cache_hit", key="user:123", ttl_seconds=300)

# These events are easily searchable in your log aggregation system:
# - Filter by event type: event:http_request_completed
# - Find all errors: level:error
# - Track performance: event:http_request_completed AND duration_ms:>1000
```

## Metrics Collection

### Counter Metrics

Track event counts and rates:

```python
from provide.foundation.metrics import Counter
from provide.foundation import logger

# Create counters
http_requests_total = Counter(
    name="http_requests_total",
    description="Total HTTP requests",
    labels=["method", "path", "status"]
)

api_errors_total = Counter(
    name="api_errors_total",
    description="Total API errors",
    labels=["error_type"]
)

# Increment counters
def handle_request(method: str, path: str):
    """Handle HTTP request."""
    try:
        result = process_request(method, path)
        http_requests_total.inc(labels={"method": method, "path": path, "status": "200"})
        return result
    except ValueError as e:
        api_errors_total.inc(labels={"error_type": "validation_error"})
        http_requests_total.inc(labels={"method": method, "path": path, "status": "400"})
        raise
    except Exception as e:
        api_errors_total.inc(labels={"error_type": "internal_error"})
        http_requests_total.inc(labels={"method": method, "path": path, "status": "500"})
        raise
```

### Gauge Metrics

Track current values that can go up and down:

```python
from provide.foundation.metrics import Gauge

# Create gauges
active_connections = Gauge(
    name="active_connections",
    description="Number of active database connections"
)

queue_size = Gauge(
    name="queue_size",
    description="Current queue depth",
    labels=["queue_name"]
)

memory_usage_bytes = Gauge(
    name="memory_usage_bytes",
    description="Current memory usage in bytes"
)

# Update gauges
def update_connection_gauge():
    """Update connection pool gauge."""
    pool = get_connection_pool()
    active_connections.set(pool.active_count)

def update_queue_gauge(queue_name: str, size: int):
    """Update queue size gauge."""
    queue_size.set(size, labels={"queue_name": queue_name})
```

### Histogram Metrics

Track distributions of values (latency, size, etc.):

```python
from provide.foundation.metrics import Histogram
import time

# Create histograms
http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    description="HTTP request latency",
    labels=["method", "path"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

response_size_bytes = Histogram(
    name="response_size_bytes",
    description="HTTP response size",
    buckets=[100, 1000, 10000, 100000, 1000000]
)

# Measure durations
def handle_api_request(method: str, path: str):
    """Handle API request with metrics."""
    start_time = time.time()

    try:
        response = process_request(method, path)

        # Record duration
        duration = time.time() - start_time
        http_request_duration_seconds.observe(
            duration,
            labels={"method": method, "path": path}
        )

        # Record response size
        response_size_bytes.observe(len(response))

        return response

    except Exception as e:
        # Still record duration for failed requests
        duration = time.time() - start_time
        http_request_duration_seconds.observe(
            duration,
            labels={"method": method, "path": path}
        )
        raise
```

## Distributed Tracing

### OpenTelemetry Integration

Configure distributed tracing with OpenTelemetry:

```python
from provide.foundation import get_hub, logger
from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.tracer import create_tracer

# Configure with OpenTelemetry
hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(
        service_name="my-service",
        enable_tracing=True,
        otlp_endpoint="http://otel-collector:4317"
    )
)

# Create tracer
tracer = create_tracer("my-service")

# Trace operations
def process_order(order_id: str):
    """Process an order with tracing."""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        # Log within trace context
        logger.info("order_processing_started", order_id=order_id)

        # Child span for database query
        with tracer.start_as_current_span("fetch_order_data") as db_span:
            db_span.set_attribute("db.system", "postgresql")
            order_data = fetch_from_db(order_id)

        # Child span for payment processing
        with tracer.start_as_current_span("process_payment") as payment_span:
            payment_span.set_attribute("payment.amount", order_data["total"])
            process_payment(order_data)

        logger.info("order_processing_completed", order_id=order_id)
```

### Trace Context Propagation

Propagate trace context across service boundaries:

```python
from provide.foundation.tracer import inject_trace_context, extract_trace_context
import requests

def call_downstream_service(url: str, data: dict):
    """Call downstream service with trace context."""
    # Inject trace context into headers
    headers = {}
    inject_trace_context(headers)

    # Make request with propagated context
    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=30
    )

    return response.json()

def handle_incoming_request(headers: dict, body: dict):
    """Handle request and extract trace context."""
    # Extract trace context from headers
    trace_context = extract_trace_context(headers)

    with tracer.start_as_current_span("handle_request", context=trace_context) as span:
        # Process request with correct trace parent
        result = process_request(body)
        return result
```

## Health Checks

### Liveness and Readiness Probes

Implement health check endpoints:

```python
from provide.foundation import get_hub, logger
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HealthCheck:
    """Health check result."""
    healthy: bool
    components: dict[str, bool]
    version: str
    uptime_seconds: float

class HealthMonitor:
    """Monitor application health."""

    def __init__(self):
        self.start_time = datetime.now()
        self.hub = get_hub()

    async def liveness_probe(self) -> bool:
        """Check if application is alive (basic check)."""
        # Application is alive if it can respond
        return True

    async def readiness_probe(self) -> HealthCheck:
        """Check if application is ready to serve traffic."""
        components = {}

        # Check database connectivity
        try:
            db_pool = self.hub.get_component("database")
            await db_pool.execute("SELECT 1")
            components["database"] = True
        except Exception as e:
            logger.error("database_health_check_failed", error=str(e))
            components["database"] = False

        # Check cache connectivity
        try:
            cache = self.hub.get_component("cache")
            await cache.ping()
            components["cache"] = True
        except Exception as e:
            logger.error("cache_health_check_failed", error=str(e))
            components["cache"] = False

        # Check external API
        try:
            api_client = self.hub.get_component("api_client")
            await api_client.health_check()
            components["external_api"] = True
        except Exception as e:
            logger.warning("external_api_health_check_failed", error=str(e))
            components["external_api"] = False

        # Overall health
        healthy = all(components.values())
        uptime = (datetime.now() - self.start_time).total_seconds()

        return HealthCheck(
            healthy=healthy,
            components=components,
            version=os.getenv("APP_VERSION", "unknown"),
            uptime_seconds=uptime
        )

# Flask/FastAPI integration
from fastapi import FastAPI, Response

app = FastAPI()
health_monitor = HealthMonitor()

@app.get("/health/live")
async def liveness():
    """Liveness probe endpoint."""
    is_alive = await health_monitor.liveness_probe()
    if is_alive:
        return {"status": "alive"}
    return Response(status_code=503)

@app.get("/health/ready")
async def readiness():
    """Readiness probe endpoint."""
    health = await health_monitor.readiness_probe()

    if health.healthy:
        return health.__dict__
    return Response(
        content=json.dumps(health.__dict__),
        status_code=503,
        media_type="application/json"
    )
```

## Alerting

### Error Rate Alerts

Monitor error rates and alert on anomalies:

```python
from provide.foundation import logger
from provide.foundation.metrics import Counter
from datetime import datetime, timedelta
import asyncio

error_counter = Counter("errors_total", labels=["severity"])

class ErrorRateMonitor:
    """Monitor and alert on error rates."""

    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold  # 5% error rate
        self.window_size = timedelta(minutes=5)
        self.error_count = 0
        self.total_count = 0
        self.window_start = datetime.now()

    def record_request(self, success: bool):
        """Record a request outcome."""
        self.total_count += 1

        if not success:
            self.error_count += 1
            error_counter.inc(labels={"severity": "error"})

        # Reset window if needed
        if datetime.now() - self.window_start > self.window_size:
            if self.total_count > 0:
                error_rate = self.error_count / self.total_count

                if error_rate > self.threshold:
                    self.trigger_alert(error_rate)

            # Reset counters
            self.error_count = 0
            self.total_count = 0
            self.window_start = datetime.now()

    def trigger_alert(self, error_rate: float):
        """Trigger alert for high error rate."""
        logger.error(
            "high_error_rate_detected",
            error_rate=error_rate,
            threshold=self.threshold,
            window_minutes=self.window_size.total_seconds() / 60
        )

        # Send to alerting platform
        send_pagerduty_alert(
            title=f"High error rate: {error_rate:.2%}",
            severity="error",
            details={
                "error_rate": error_rate,
                "threshold": self.threshold
            }
        )
```

### Performance Degradation Alerts

Alert on latency spikes:

```python
from provide.foundation.metrics import Histogram
import statistics

latency_histogram = Histogram("request_latency_seconds")

class LatencyMonitor:
    """Monitor request latency."""

    def __init__(self, p95_threshold: float = 1.0):
        self.p95_threshold = p95_threshold
        self.recent_latencies: list[float] = []
        self.max_samples = 1000

    def record_latency(self, latency: float):
        """Record a request latency."""
        latency_histogram.observe(latency)
        self.recent_latencies.append(latency)

        # Keep only recent samples
        if len(self.recent_latencies) > self.max_samples:
            self.recent_latencies.pop(0)

        # Check p95
        if len(self.recent_latencies) >= 100:
            p95 = statistics.quantiles(self.recent_latencies, n=20)[18]  # 95th percentile

            if p95 > self.p95_threshold:
                logger.warning(
                    "high_latency_detected",
                    p95_latency=p95,
                    threshold=self.p95_threshold
                )
```

## Dashboard Integration

### Prometheus Metrics Export

Export metrics in Prometheus format:

```python
from prometheus_client import start_http_server, Counter, Histogram, Gauge
from provide.foundation import logger

# Start Prometheus metrics server
start_http_server(9090)
logger.info("prometheus_metrics_enabled", port=9090)

# Metrics are now available at http://localhost:9090/metrics
```

### Grafana Dashboard JSON

Example Grafana dashboard configuration:

```json
{
  "dashboard": {
    "title": "My Service Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(api_errors_total[5m]) / rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Latency p95",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds)"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

### ✅ DO: Use Structured Logging

```python
# ✅ GOOD: Structured events with context
logger.info(
    "payment_processed",
    payment_id="pay_123",
    amount_cents=1000,
    currency="USD",
    duration_ms=123
)
```

### ❌ DON'T: Log Unstructured Strings

```python
# ❌ BAD: Hard to parse and search
logger.info(f"Processed payment pay_123 for $10.00 in 123ms")
```

### ✅ DO: Track Key Metrics

```python
# ✅ GOOD: Track important business metrics
transactions_total.inc(labels={"type": "purchase", "status": "success"})
revenue_total.inc(amount_cents)
```

### ❌ DON'T: Ignore Performance Metrics

```python
# ❌ BAD: No observability into performance
def process_order(order):
    result = slow_operation()  # How slow? No idea!
    return result
```

### ✅ DO: Implement Health Checks

```python
# ✅ GOOD: Comprehensive health checks
@app.get("/health/ready")
async def readiness():
    checks = {
        "database": await check_database(),
        "cache": await check_cache(),
        "api": await check_external_api()
    }
    healthy = all(checks.values())
    return {"healthy": healthy, "checks": checks}
```

### ❌ DON'T: Skip Health Endpoints

```python
# ❌ BAD: No way for orchestrator to check health
# Missing /health endpoints means blind deployments
```

### ✅ DO: Use Consistent Event Names

```python
# ✅ GOOD: Domain-Action-Status pattern
logger.info("database_query_started", table="users")
logger.info("database_query_completed", table="users", duration_ms=45)
logger.error("database_query_failed", table="users", error="timeout")
```

### ❌ DON'T: Use Random Event Names

```python
# ❌ BAD: Inconsistent naming
logger.info("query started")
logger.info("completed db query")
logger.error("DB ERROR!")
```

### ✅ DO: Monitor Error Budgets

```python
# ✅ GOOD: Track SLIs and error budgets
class SLIMonitor:
    """Track Service Level Indicators."""

    def __init__(self, error_budget: float = 0.001):  # 99.9% SLO
        self.error_budget = error_budget
        self.success_count = 0
        self.total_count = 0

    def record(self, success: bool):
        """Record request outcome."""
        self.total_count += 1
        if success:
            self.success_count += 1

    def current_sli(self) -> float:
        """Get current SLI."""
        if self.total_count == 0:
            return 1.0
        return self.success_count / self.total_count

    def budget_remaining(self) -> float:
        """Get remaining error budget."""
        sli = self.current_sli()
        target = 1.0 - self.error_budget
        return max(0, sli - target)
```

### ✅ DO: Set Up Alerts for Critical Issues

```python
# ✅ GOOD: Alert on critical conditions
if error_rate > 0.05:  # 5% errors
    send_pagerduty_alert("High error rate", severity="critical")

if p95_latency > 1.0:  # 1 second p95
    send_slack_alert("Latency spike detected", channel="#ops")
```

### ❌ DON'T: Alert on Everything

```python
# ❌ BAD: Too many alerts cause alert fatigue
for log_line in logs:
    if "error" in log_line.lower():
        send_pagerduty_alert(log_line)  # Way too noisy!
```

## Next Steps

### Related Guides
- **[Deployment Patterns](deployment.md)**: Deploy to production
- **[Structured Events](../logging/structured-events.md)**: Event naming conventions
- **[Basic Logging](../logging/basic-logging.md)**: Logging fundamentals

### Examples
- See `examples/production/08_monitoring.py` for monitoring examples
- See `examples/production/09_health_checks.py` for health check patterns

### API Reference
- **[Metrics API](../../reference/provide/foundation/metrics/index.md)**: Metrics collection
- **[Tracer API](../../reference/provide/foundation/tracer/index.md)**: Distributed tracing

---

**Tip**: Start with structured JSON logging and basic metrics. Add distributed tracing as your system grows. Focus on monitoring what matters: error rates, latency, and business metrics. Use health checks to enable zero-downtime deployments.
