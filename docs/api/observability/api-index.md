# Observability API

Advanced observability features for monitoring, tracing, and analyzing application behavior.

## Overview

The `observability` module provides comprehensive observability capabilities including distributed tracing, metrics collection, health checks, and performance monitoring. It's designed to give you deep insights into your application's behavior and performance.

## Key Features

- **Distributed Tracing**: OpenTelemetry-compatible distributed tracing
- **Metrics Collection**: Custom and automatic metrics collection
- **Health Checks**: Application and dependency health monitoring
- **Performance Monitoring**: Real-time performance analysis
- **Service Discovery**: Service mesh and discovery integration
- **Alerting Integration**: Integration with alerting systems

## Distributed Tracing

### Basic Tracing

```python
from provide.foundation.observability import tracer, trace_context

# Automatic tracing with decorator
@tracer.trace("user_operation")
async def get_user_profile(user_id: str):
    # Span automatically created and managed
    with tracer.span("database_query") as span:
        span.set_attribute("user_id", user_id)
        user = await db.get_user(user_id)
        span.set_attribute("found", user is not None)
    
    with tracer.span("profile_enrichment"):
        profile = await enrich_user_profile(user)
    
    return profile

# Manual span management
async def manual_tracing():
    with tracer.start_span("parent_operation") as parent:
        parent.set_attribute("operation_type", "batch_process")
        
        for item in items:
            with tracer.start_child_span("process_item", parent) as child:
                child.set_attribute("item_id", item.id)
                await process_item(item)
```

### Context Propagation

```python
from provide.foundation.observability import trace_context

# Automatic context propagation
@trace_context.propagate
async def service_call(request_data):
    # Trace context automatically propagated to downstream calls
    response = await external_service.call(request_data)
    return response

# Manual context management
async def manual_propagation():
    context = trace_context.current()
    
    # Pass context to async task
    await asyncio.create_task(
        background_task(data),
        context=context
    )
```

### Cross-Service Tracing

```python
from provide.foundation.observability import http_tracing
import httpx

# HTTP client with automatic trace propagation
async def call_downstream_service():
    async with http_tracing.traced_client() as client:
        # Trace context automatically added to headers
        response = await client.get("https://downstream-service/api/data")
        return response.json()

# Custom trace headers
headers = trace_context.to_headers()
# {'traceparent': '00-...', 'tracestate': '...'}
```

## Metrics Collection

### Custom Metrics

```python
from provide.foundation.observability import metrics

# Counter metrics
request_counter = metrics.counter(
    "http_requests_total",
    description="Total HTTP requests",
    labels=["method", "endpoint", "status"]
)

@app.route("/api/users")
def get_users():
    request_counter.inc(labels={"method": "GET", "endpoint": "/api/users", "status": "200"})
    return {"users": []}

# Histogram metrics
response_time_histogram = metrics.histogram(
    "http_request_duration_seconds",
    description="HTTP request duration",
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

@metrics.time(response_time_histogram)
async def timed_operation():
    # Operation duration automatically recorded
    await expensive_operation()
```

### Automatic Metrics

```python
from provide.foundation.observability import auto_metrics

# Automatic metrics from log events
@auto_metrics.from_logs("api_request_completed")
class APIMetrics:
    """Automatic metrics generation from structured logs."""
    
    requests_total = metrics.counter("api_requests_total", ["endpoint", "method"])
    request_duration = metrics.histogram("api_request_duration_seconds", ["endpoint"])
    error_rate = metrics.counter("api_errors_total", ["endpoint", "error_type"])

# System metrics collection
system_metrics = auto_metrics.system_collector(
    collect_cpu=True,
    collect_memory=True,
    collect_disk=True,
    collect_network=True,
    interval=30.0
)

await system_metrics.start()
```

## Health Checks

### Application Health

```python
from provide.foundation.observability import health_check, HealthStatus

class DatabaseHealthCheck:
    """Health check for database connectivity."""
    
    @health_check("database", critical=True)
    async def check_database(self) -> HealthStatus:
        try:
            await db.execute("SELECT 1")
            return HealthStatus.HEALTHY
        except Exception as e:
            return HealthStatus.UNHEALTHY(reason=str(e))

class ExternalAPIHealthCheck:
    """Health check for external API dependency."""
    
    @health_check("external_api", critical=False, timeout=5.0)
    async def check_external_api(self) -> HealthStatus:
        try:
            response = await httpx.get("https://api.example.com/health", timeout=5.0)
            return HealthStatus.HEALTHY if response.status_code == 200 else HealthStatus.DEGRADED
        except Exception:
            return HealthStatus.UNHEALTHY
```

### Health Endpoints

```python
from provide.foundation.observability import health_router
from fastapi import FastAPI

app = FastAPI()

# Add health check endpoints
health_router.register_checks([
    DatabaseHealthCheck(),
    ExternalAPIHealthCheck()
])

app.include_router(health_router, prefix="/health")

# Endpoints available:
# GET /health - Overall health status
# GET /health/detailed - Detailed health information
# GET /health/database - Specific component health
```

## Performance Monitoring

### Performance Profiling

```python
from provide.foundation.observability import profiler

# Profile specific operations
@profiler.profile("expensive_operation")
async def expensive_operation():
    # Operation is automatically profiled
    result = await complex_computation()
    return result

# Manual profiling
async with profiler.profile_context("batch_processing") as prof:
    for item in items:
        await process_item(item)
    
    # Profile results available
    stats = prof.get_stats()
    logger.info("profiling_complete", 
               total_time=stats.total_time,
               calls=stats.call_count)
```

### Resource Monitoring

```python
from provide.foundation.observability import resource_monitor

# Monitor resource usage
monitor = resource_monitor.ResourceMonitor(
    alert_cpu_threshold=80.0,
    alert_memory_threshold=85.0,
    sample_interval=10.0
)

@monitor.watch_resources
async def resource_intensive_operation():
    # Resource usage is monitored during execution
    await heavy_computation()

# Manual resource tracking
async with monitor.track_resources("data_processing") as tracker:
    await process_large_dataset()
    
    usage = tracker.get_usage()
    logger.info("resource_usage",
               max_cpu_percent=usage.max_cpu,
               max_memory_mb=usage.max_memory)
```

## Service Discovery

### Service Registration

```python
from provide.foundation.observability import service_registry

# Register service with discovery
registry = service_registry.ServiceRegistry()

await registry.register(
    service_name="user-service",
    service_id="user-service-001",
    host="localhost",
    port=8080,
    health_check_url="/health",
    metadata={
        "version": "1.0.0",
        "environment": "production"
    }
)

# Service heartbeat
await registry.heartbeat("user-service-001")
```

### Service Discovery

```python
# Discover services
services = await registry.discover("user-service")
for service in services:
    logger.info("discovered_service",
               service_id=service.id,
               host=service.host,
               port=service.port,
               healthy=service.is_healthy)

# Load-balanced service calls
client = service_registry.load_balanced_client("user-service")
response = await client.get("/api/users/123")
```

## Alerting Integration

### Alert Rules

```python
from provide.foundation.observability import alerting

# Define alert rules
alert_manager = alerting.AlertManager()

# Metric-based alerts
alert_manager.add_rule(
    name="high_error_rate",
    condition="api_errors_total / api_requests_total > 0.05",
    duration="5m",
    severity="critical",
    description="API error rate exceeded 5%"
)

# Log-based alerts
alert_manager.add_rule(
    name="database_connection_failed",
    condition=alerting.log_pattern("database_connection_failed"),
    count_threshold=5,
    duration="2m",
    severity="warning"
)
```

### Alert Channels

```python
# Configure alert channels
alert_manager.add_channel(
    alerting.SlackChannel(
        webhook_url="https://hooks.slack.com/...",
        channel="#alerts",
        severity_filter=["critical", "warning"]
    )
)

alert_manager.add_channel(
    alerting.EmailChannel(
        smtp_config=email_config,
        recipients=["oncall@company.com"],
        severity_filter=["critical"]
    )
)

# Custom alert handler
@alert_manager.handler("custom_handler")
async def custom_alert_handler(alert):
    """Custom alert processing."""
    logger.error("alert_triggered",
                alert_name=alert.name,
                severity=alert.severity,
                description=alert.description)
    
    # Custom notification logic
    await send_to_monitoring_system(alert)
```

## Integration with External Systems

### OpenTelemetry Integration

```python
from provide.foundation.observability import opentelemetry_bridge

# Setup OpenTelemetry bridge
otel_bridge = opentelemetry_bridge.setup(
    service_name="my-service",
    exporter_endpoint="http://jaeger:14268/api/traces",
    exporter_type="jaeger"
)

# All foundation traces are exported to OpenTelemetry
```

### Prometheus Integration

```python
from provide.foundation.observability import prometheus_exporter

# Export metrics to Prometheus
exporter = prometheus_exporter.PrometheusExporter(
    port=9090,
    endpoint="/metrics"
)

await exporter.start()

# Metrics automatically available at http://localhost:9090/metrics
```

## Observability Dashboard

### Dashboard Configuration

```python
from provide.foundation.observability import dashboard

# Create observability dashboard
dash = dashboard.ObservabilityDashboard(
    service_name="my-service",
    port=8090
)

# Add custom panels
dash.add_panel(
    dashboard.MetricsPanel(
        title="Request Rate",
        query="rate(http_requests_total[5m])",
        chart_type="line"
    )
)

dash.add_panel(
    dashboard.LogPanel(
        title="Recent Errors",
        query="level:ERROR",
        limit=100
    )
)

await dash.start()
# Dashboard available at http://localhost:8090
```

## Performance Analysis

### Bottleneck Detection

```python
from provide.foundation.observability import performance_analyzer

analyzer = performance_analyzer.PerformanceAnalyzer()

# Analyze performance bottlenecks
@analyzer.analyze("user_workflow")
async def user_workflow():
    user = await get_user()  # Automatically timed
    profile = await get_profile(user)  # Automatically timed
    recommendations = await get_recommendations(profile)  # Automatically timed
    return recommendations

# Get analysis results
analysis = analyzer.get_analysis("user_workflow")
logger.info("performance_analysis",
           bottlenecks=analysis.bottlenecks,
           total_time=analysis.total_time,
           recommendations=analysis.recommendations)
```

## Testing and Development

### Observability in Tests

```python
from provide.foundation.observability.testing import ObservabilityTestCase

class TestObservability(ObservabilityTestCase):
    """Test case with observability features."""
    
    async def test_tracing(self):
        # Traces are captured during tests
        await traced_operation()
        
        # Verify traces
        traces = self.get_traces()
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0].operation_name, "traced_operation")
    
    async def test_metrics(self):
        # Metrics are captured during tests
        await operation_that_increments_counter()
        
        # Verify metrics
        counter_value = self.get_metric_value("operations_total")
        self.assertEqual(counter_value, 1)
```

### Development Mode

```python
from provide.foundation.observability import dev_mode

# Enhanced observability for development
dev_mode.enable(
    detailed_tracing=True,
    metrics_console_output=True,
    performance_warnings=True,
    health_check_logging=True
)

# Automatic performance warnings
# WARNING: Operation 'slow_operation' took 2.3s (threshold: 1.0s)
```

## Best Practices

### Tracing Strategy
```python
# Trace meaningful operations, not every function
@tracer.trace("business_operation")
async def important_business_logic():
    # This should be traced
    pass

def utility_function():
    # This probably shouldn't be traced
    pass
```

### Metrics Naming
```python
# Use consistent metric naming
http_requests_total = metrics.counter("http_requests_total")  # Good
request_count = metrics.counter("requests")  # Avoid

# Include relevant labels
http_requests_total.inc(labels={
    "method": "GET",
    "endpoint": "/api/users",
    "status_code": "200"
})
```

### Health Check Design
```python
# Health checks should be fast and meaningful
@health_check("database", timeout=2.0)
async def check_database():
    # Quick connection test, not full functionality test
    await db.execute("SELECT 1")
    return HealthStatus.HEALTHY
```

## API Reference

::: provide.foundation.observability

## Related Documentation

- [Distributed Tracing Guide](../../guide/tracing/index.md) - Comprehensive tracing patterns
- [Performance Guide](../../guide/concepts/performance.md) - Performance monitoring strategies
- [Configuration Guide](../../guide/config/index.md) - Observability configuration