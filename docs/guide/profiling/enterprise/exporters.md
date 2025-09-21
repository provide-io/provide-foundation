# Exporter Abstraction

!!! info "Planned Enterprise Feature"
    Universal exporter interface enabling seamless integration with any monitoring, metrics, or observability backend system.

!!! warning "Implementation Status"
    This feature is planned for Foundation v1.1+. This documentation serves as a specification and design guide for the upcoming implementation.

## Overview

The exporter abstraction provides a unified interface for sending profiling data to external monitoring systems. This design enables seamless integration with popular platforms like Prometheus, Datadog, New Relic, OpenTelemetry, and custom monitoring solutions without vendor lock-in.

## Core Exporter Interface

### Base Exporter

All exporters implement the universal `ProfilingExporter` interface:

```python
from provide.foundation.profiling.exporters import ProfilingExporter

class CustomExporter(ProfilingExporter):
    """Custom exporter implementing the universal interface."""

    def __init__(self, config: ExporterConfig):
        self.config = config
        self.client = self._initialize_client()

    async def export_metrics(self, metrics: ProfileMetrics) -> ExportResult:
        """Export profiling metrics to external system."""
        try:
            payload = self._format_metrics(metrics)
            response = await self.client.send(payload)
            return ExportResult.success(
                exported_count=len(payload),
                response_time_ms=response.duration_ms
            )
        except Exception as e:
            return ExportResult.failure(error=str(e))

    async def export_traces(self, traces: list[ProfileTrace]) -> ExportResult:
        """Export profiling traces to external system."""
        # Implementation specific to your monitoring backend
        pass

    def health_check(self) -> HealthStatus:
        """Check connectivity to external system."""
        return HealthStatus.healthy() if self._can_connect() else HealthStatus.unhealthy()
```

### Configuration System

Unified configuration for all exporters:

```python
from provide.foundation.profiling.exporters import ExporterConfig

# Environment-based configuration
config = ExporterConfig.from_env(
    prefix="PROFILING_EXPORTER",
    required_fields=["endpoint", "api_key"]
)

# Explicit configuration
config = ExporterConfig(
    name="production_metrics",
    endpoint="https://api.monitoring.com/v1/metrics",
    auth=AuthConfig(
        type="api_key",
        api_key=os.getenv("MONITORING_API_KEY"),
        headers={"X-Source": "foundation-profiling"}
    ),
    batch_size=100,
    flush_interval_seconds=30,
    retry_config=RetryConfig(
        max_retries=3,
        backoff_multiplier=2.0,
        max_backoff_seconds=60
    ),
    compression="gzip",
    format="json"
)
```

## Built-in Exporters

### Prometheus Exporter

Export metrics to Prometheus pushgateway or pull endpoint:

```python
from provide.foundation.profiling.exporters import PrometheusExporter

# Push-based export to pushgateway
prometheus_exporter = PrometheusExporter(
    pushgateway_url="http://pushgateway:9091",
    job_name="foundation_profiling",
    instance_label="web-server-01",
    metrics_mapping={
        "messages_per_second": {
            "name": "foundation_log_messages_per_second",
            "type": "gauge",
            "help": "Rate of log messages processed per second"
        },
        "avg_latency_ms": {
            "name": "foundation_log_processing_latency_milliseconds",
            "type": "gauge",
            "help": "Average log processing latency in milliseconds"
        },
        "emoji_overhead_percent": {
            "name": "foundation_emoji_processing_overhead_percent",
            "type": "gauge",
            "help": "Percentage overhead from emoji processing"
        }
    },
    additional_labels={
        "environment": "production",
        "service": "api-server",
        "version": "1.2.3"
    }
)

# Pull-based export (Prometheus scrapes your app)
prometheus_exporter = PrometheusExporter(
    mode="pull",
    metrics_port=8080,
    metrics_path="/metrics",
    registry=custom_prometheus_registry
)
```

### OpenTelemetry Exporter

Integration with OpenTelemetry ecosystem:

```python
from provide.foundation.profiling.exporters import OpenTelemetryExporter

otel_exporter = OpenTelemetryExporter(
    # OTLP endpoint configuration
    otlp_endpoint="http://jaeger:14268/api/traces",
    otlp_protocol="http/protobuf",  # or "grpc"

    # Resource identification
    service_name="foundation_profiling",
    service_version="1.0.0",
    service_namespace="production",

    # Span configuration
    span_name_prefix="profiling",
    create_child_spans=True,

    # Metrics configuration
    metrics_endpoint="http://otel-collector:4318/v1/metrics",
    metrics_protocol="http/protobuf",

    # Custom attributes
    resource_attributes={
        "deployment.environment": "production",
        "host.name": "web-01",
        "process.pid": os.getpid()
    },

    # Sampling configuration
    trace_sampler="parentbased_traceidratio",
    trace_sample_rate=0.1
)
```

### Datadog Exporter

Direct integration with Datadog APM and metrics:

```python
from provide.foundation.profiling.exporters import DatadogExporter

datadog_exporter = DatadogExporter(
    api_key=os.getenv("DATADOG_API_KEY"),
    app_key=os.getenv("DATADOG_APP_KEY"),
    site="datadoghq.com",  # or "datadoghq.eu", "ddog-gov.com"

    # Metrics configuration
    metrics_config={
        "namespace": "foundation.profiling",
        "tags": [
            "environment:production",
            "service:api-server",
            "team:platform"
        ]
    },

    # APM configuration
    apm_config={
        "service": "foundation-profiling",
        "env": "production",
        "version": "1.0.0"
    },

    # Custom metrics mapping
    custom_metrics={
        "processing_rate": {
            "metric_name": "foundation.log.processing_rate",
            "metric_type": "rate",
            "source_field": "messages_per_second"
        },
        "emoji_overhead": {
            "metric_name": "foundation.log.emoji_overhead",
            "metric_type": "gauge",
            "source_field": "emoji_overhead_percent"
        }
    }
)
```

### New Relic Exporter

Integration with New Relic monitoring:

```python
from provide.foundation.profiling.exporters import NewRelicExporter

newrelic_exporter = NewRelicExporter(
    license_key=os.getenv("NEW_RELIC_LICENSE_KEY"),
    account_id=os.getenv("NEW_RELIC_ACCOUNT_ID"),
    region="US",  # or "EU"

    # Metrics API configuration
    metrics_api_url="https://metric-api.newrelic.com/metric/v1",

    # Event API configuration
    events_api_url="https://insights-collector.newrelic.com/v1/accounts/{account_id}/events",

    # Custom event types
    event_types={
        "ProfileMetrics": {
            "attributes": [
                "messages_per_second",
                "avg_latency_ms",
                "emoji_overhead_percent"
            ]
        },
        "ProfileTrace": {
            "attributes": [
                "function_name",
                "execution_time_ms",
                "memory_usage_mb"
            ]
        }
    },

    # Common attributes
    common_attributes={
        "service.name": "foundation-profiling",
        "environment": "production",
        "host": socket.gethostname()
    }
)
```

## Multi-Exporter Configuration

### Parallel Export

Send data to multiple monitoring systems simultaneously:

```python
from provide.foundation.profiling.exporters import MultiExporter

multi_exporter = MultiExporter(
    exporters=[
        PrometheusExporter(pushgateway_url="http://prometheus:9091"),
        DatadogExporter(api_key=datadog_api_key),
        OpenTelemetryExporter(otlp_endpoint="http://jaeger:14268")
    ],

    # Export strategy
    strategy="parallel",        # or "sequential", "failover"

    # Failure handling
    failure_policy="continue",  # Continue even if some exporters fail
    min_success_count=1,        # At least 1 exporter must succeed

    # Performance tuning
    max_concurrent_exports=3,
    export_timeout_seconds=30
)

# Register with profiling system
from provide.foundation.profiling import register_profiling

register_profiling(
    hub,
    exporters=[multi_exporter]
)
```

### Conditional Export

Export to different systems based on conditions:

```python
from provide.foundation.profiling.exporters import ConditionalExporter

conditional_exporter = ConditionalExporter(
    conditions=[
        {
            "condition": lambda metrics: metrics.avg_latency_ms > 100,
            "exporter": DatadogExporter(),  # Send to Datadog for slow operations
            "description": "High latency alerts"
        },
        {
            "condition": lambda metrics: metrics.error_rate > 0.05,
            "exporter": NewRelicExporter(),  # Send to New Relic for errors
            "description": "Error rate monitoring"
        },
        {
            "condition": lambda metrics: True,  # Always
            "exporter": PrometheusExporter(),  # Always send to Prometheus
            "description": "Base metrics collection"
        }
    ]
)
```

## Custom Exporters

### HTTP API Exporter

Generic HTTP exporter for custom APIs:

```python
from provide.foundation.profiling.exporters import HTTPExporter

custom_api_exporter = HTTPExporter(
    endpoint="https://your-monitoring-api.com/metrics",
    method="POST",
    headers={
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "X-Source": "foundation-profiling"
    },

    # Payload transformation
    payload_transformer=lambda metrics: {
        "timestamp": int(time.time()),
        "source": "foundation-profiling",
        "metrics": {
            "throughput": metrics.messages_per_second,
            "latency_p95": metrics.p95_latency_ms,
            "error_rate": metrics.error_rate,
            "emoji_usage": metrics.emoji_message_count
        },
        "metadata": {
            "service": "api-server",
            "environment": "production",
            "host": socket.gethostname()
        }
    },

    # Error handling
    retry_config=RetryConfig(
        max_retries=3,
        retry_on_status_codes=[429, 500, 502, 503, 504],
        backoff_strategy="exponential"
    )
)
```

### Database Exporter

Export metrics to database for custom analytics:

```python
from provide.foundation.profiling.exporters import DatabaseExporter

database_exporter = DatabaseExporter(
    connection_string="postgresql://user:pass@localhost/monitoring",
    table_name="profiling_metrics",

    # Schema mapping
    column_mapping={
        "timestamp": "recorded_at",
        "messages_per_second": "throughput",
        "avg_latency_ms": "avg_latency",
        "emoji_overhead_percent": "emoji_overhead",
        "total_messages": "message_count"
    },

    # Batch configuration
    batch_size=1000,
    batch_timeout_seconds=60,

    # Connection pooling
    pool_size=5,
    max_overflow=10
)
```

### File-Based Exporter

Export to structured files for analysis:

```python
from provide.foundation.profiling.exporters import FileExporter

file_exporter = FileExporter(
    output_directory="/var/log/profiling",
    file_format="jsonl",  # or "csv", "parquet"

    # File rotation
    rotation_policy="time",  # or "size"
    rotation_interval="1h",  # Rotate hourly
    max_file_size="100MB",

    # Compression
    compression="gzip",

    # File naming
    filename_template="profiling-{timestamp}-{hostname}.jsonl.gz",

    # Custom serialization
    serializer=lambda metrics: {
        "timestamp": metrics.timestamp.isoformat(),
        "performance": {
            "throughput": metrics.messages_per_second,
            "latency": {
                "avg": metrics.avg_latency_ms,
                "p95": metrics.p95_latency_ms,
                "p99": metrics.p99_latency_ms
            }
        },
        "features": {
            "emoji_usage_percent": metrics.emoji_overhead_percent,
            "error_rate": metrics.error_rate
        },
        "system": {
            "host": socket.gethostname(),
            "pid": os.getpid(),
            "python_version": platform.python_version()
        }
    }
)
```

## Advanced Features

### Buffering and Batching

Optimize export performance with intelligent buffering:

```python
from provide.foundation.profiling.exporters import BufferedExporter

buffered_exporter = BufferedExporter(
    base_exporter=PrometheusExporter(),

    # Buffer configuration
    buffer_size=1000,                    # Buffer up to 1000 metrics
    flush_interval_seconds=30,           # Flush every 30 seconds
    flush_on_shutdown=True,              # Flush remaining data on shutdown

    # Memory management
    max_memory_usage_mb=50,              # Flush if buffer exceeds 50MB
    drop_oldest_on_overflow=True,        # Drop old data if buffer full

    # Adaptive flushing
    adaptive_flushing=True,              # Adjust flush interval based on load
    min_flush_interval_seconds=5,        # Never flush more frequently than 5s
    max_flush_interval_seconds=300,      # Never wait longer than 5 minutes

    # Compression
    compress_buffer=True,                # Compress buffered data
    compression_threshold=100            # Compress when buffer has >100 items
)
```

### Error Handling and Resilience

Robust error handling for production deployments:

```python
from provide.foundation.profiling.exporters import ResilientExporter

resilient_exporter = ResilientExporter(
    base_exporter=DatadogExporter(),

    # Circuit breaker
    circuit_breaker={
        "failure_threshold": 5,          # Trip after 5 consecutive failures
        "recovery_timeout_seconds": 60,  # Try to recover after 60 seconds
        "half_open_max_calls": 3         # Test with 3 calls when half-open
    },

    # Retry configuration
    retry_config={
        "max_retries": 3,
        "initial_delay_seconds": 1,
        "max_delay_seconds": 60,
        "backoff_multiplier": 2.0,
        "jitter": True                   # Add randomness to prevent thundering herd
    },

    # Fallback exporter
    fallback_exporter=FileExporter(    # Fall back to file when primary fails
        output_directory="/var/log/profiling/fallback"
    ),

    # Health monitoring
    health_check_interval_seconds=30,    # Check health every 30 seconds
    unhealthy_threshold_failures=3,      # Consider unhealthy after 3 failures

    # Dead letter queue
    dlq_exporter=FileExporter(          # Failed exports go to DLQ
        output_directory="/var/log/profiling/dlq"
    )
)
```

### Performance Monitoring

Monitor exporter performance itself:

```python
from provide.foundation.profiling.exporters import MonitoredExporter

monitored_exporter = MonitoredExporter(
    base_exporter=PrometheusExporter(),

    # Self-monitoring configuration
    monitor_config={
        "track_export_latency": True,
        "track_export_size": True,
        "track_success_rate": True,
        "track_error_types": True
    },

    # Performance alerts
    alert_thresholds={
        "export_latency_p95_ms": 1000,   # Alert if P95 export latency > 1s
        "success_rate_percent": 95,       # Alert if success rate < 95%
        "queue_depth": 1000               # Alert if export queue > 1000 items
    },

    # Self-metrics export
    self_metrics_exporter=PrometheusExporter(
        job_name="profiling_exporter_metrics"
    )
)
```

## Integration Patterns

### Kubernetes Deployment

Deploy exporters in Kubernetes with proper configuration:

```yaml
# ConfigMap for exporter configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: profiling-exporters-config
data:
  exporters.yaml: |
    exporters:
      - name: prometheus
        type: prometheus
        config:
          pushgateway_url: http://prometheus-pushgateway:9091
          job_name: foundation-profiling
          labels:
            environment: production
            cluster: k8s-prod

      - name: datadog
        type: datadog
        config:
          api_key_secret: datadog-api-key
          site: datadoghq.com
          tags:
            - "environment:production"
            - "service:foundation"

---
# Deployment with exporter configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-profiling
spec:
  template:
    spec:
      containers:
      - name: app
        image: your-app:latest
        env:
        - name: PROFILING_EXPORTERS_CONFIG
          value: /etc/profiling/exporters.yaml
        volumeMounts:
        - name: exporters-config
          mountPath: /etc/profiling
      volumes:
      - name: exporters-config
        configMap:
          name: profiling-exporters-config
```

### Docker Compose Setup

Configure exporters in Docker Compose environment:

```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - PROFILING_PROMETHEUS_PUSHGATEWAY_URL=http://prometheus-pushgateway:9091
      - PROFILING_DATADOG_API_KEY=${DATADOG_API_KEY}
      - PROFILING_OTEL_ENDPOINT=http://jaeger:14268/api/traces
    depends_on:
      - prometheus-pushgateway
      - jaeger

  prometheus-pushgateway:
    image: prom/pushgateway:latest
    ports:
      - "9091:9091"

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "14268:14268"
      - "16686:16686"
```

## Best Practices

### Production Deployment

1. **Use Multiple Exporters**: Don't rely on single monitoring system
2. **Configure Fallbacks**: Always have backup export mechanism
3. **Monitor Exporter Health**: Track export success rates and latency
4. **Use Circuit Breakers**: Protect against cascading failures
5. **Buffer Appropriately**: Balance memory usage with data loss risk

### Performance Optimization

1. **Batch Exports**: Combine multiple metrics into single export
2. **Compress Data**: Use compression for large payloads
3. **Async Export**: Never block application on export operations
4. **Sample Exports**: Don't export every single metric in high-volume scenarios
5. **Connection Pooling**: Reuse connections to external systems

### Security Considerations

1. **Secure Credentials**: Use secrets management for API keys
2. **Encrypt in Transit**: Always use HTTPS/TLS for exports
3. **Validate Inputs**: Sanitize metric data before export
4. **Rate Limiting**: Respect external API rate limits
5. **Network Segmentation**: Isolate monitoring traffic when possible

## Troubleshooting

### Common Issues

**Exports failing silently**
```python
# Enable debug logging for all exporters
import logging
logging.getLogger("provide.foundation.profiling.exporters").setLevel(logging.DEBUG)

# Check exporter health
health = exporter.health_check()
if not health.is_healthy():
    print(f"Exporter unhealthy: {health.error_message}")
```

**High export latency**
```python
# Check buffer configuration
if hasattr(exporter, 'buffer_stats'):
    stats = exporter.buffer_stats()
    print(f"Buffer usage: {stats.usage_percent:.1f}%")
    print(f"Average flush time: {stats.avg_flush_time_ms:.0f}ms")

# Optimize batch size
exporter.update_config(batch_size=50)  # Reduce batch size
```

**Missing metrics in monitoring system**
```python
# Verify export success
last_export = exporter.get_last_export_result()
if not last_export.success:
    print(f"Last export failed: {last_export.error}")

# Check metric filtering
filtered_count = exporter.get_filtered_metrics_count()
if filtered_count > 0:
    print(f"{filtered_count} metrics were filtered out")
```

### Debug Mode

Enable comprehensive debugging for export operations:

```python
from provide.foundation.profiling.exporters import enable_debug_mode

enable_debug_mode(
    trace_exports=True,          # Trace all export operations
    log_payloads=True,           # Log exported payloads (be careful with PII)
    measure_performance=True,     # Measure export performance
    validate_schemas=True        # Validate payload schemas
)
```