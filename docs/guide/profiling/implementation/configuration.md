# Profiling Configuration

Comprehensive guide to configuring Foundation's profiling system for different environments and use cases.

## Configuration Sources

### Environment Variables

Set profiling behavior through environment variables:

```bash
# Basic profiling control
export PROVIDE_PROFILING_ENABLED=true
export PROVIDE_PROFILING_SAMPLE_RATE=0.02

# Advanced configuration
export PROVIDE_PROFILING_TRACK_MEMORY=false
export PROVIDE_PROFILING_BUFFER_SIZE=1000
export PROVIDE_PROFILING_FLUSH_INTERVAL_SECONDS=30

# CLI integration
export PROVIDE_PROFILING_CLI_ENABLED=true
export PROVIDE_PROFILING_CLI_COMMAND_NAME=profile

# Exporter configuration
export PROVIDE_PROFILING_EXPORTERS=prometheus,datadog
export PROVIDE_PROFILING_PROMETHEUS_PUSHGATEWAY_URL=http://prometheus:9091
export PROVIDE_PROFILING_DATADOG_API_KEY=your-api-key
```

### Configuration Files

Use YAML or JSON configuration files:

```yaml
# profiling.yaml
profiling:
  enabled: true
  sample_rate: 0.02

  processor:
    track_memory: false
    buffer_size: 1000
    flush_interval_seconds: 30

  cli:
    enabled: true
    command_name: "profile"
    include_reset_option: true

  exporters:
    - name: prometheus
      type: prometheus
      config:
        pushgateway_url: "http://prometheus:9091"
        job_name: "foundation-profiling"
        labels:
          environment: "production"

    - name: datadog
      type: datadog
      config:
        api_key: "${DATADOG_API_KEY}"
        site: "datadoghq.com"
        tags:
          - "service:api"
          - "environment:prod"
```

```python
# Load configuration from file
from provide.foundation.profiling.config import ProfilingConfig

config = ProfilingConfig.from_file("profiling.yaml")
register_profiling(hub, config=config)
```

### Programmatic Configuration

Configure directly in code:

```python
from provide.foundation.profiling.config import (
    ProfilingConfig,
    ProcessorConfig,
    ExporterConfig
)

config = ProfilingConfig(
    enabled=True,
    sample_rate=0.02,

    processor=ProcessorConfig(
        track_memory=False,
        buffer_size=1000,
        flush_interval_seconds=30,
        enable_fast_path=True
    ),

    cli=CLIConfig(
        enabled=True,
        command_name="profile",
        include_reset_option=True
    ),

    exporters=[
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            config={
                "pushgateway_url": "http://prometheus:9091",
                "job_name": "foundation-profiling"
            }
        )
    ]
)

register_profiling(hub, config=config)
```

## Sampling Configuration

### Basic Sampling

Control how much data is collected:

```python
# Conservative sampling (minimal overhead)
config = ProfilingConfig(sample_rate=0.005)  # 0.5%

# Balanced sampling (recommended for production)
config = ProfilingConfig(sample_rate=0.02)   # 2%

# Detailed sampling (development/staging)
config = ProfilingConfig(sample_rate=0.10)   # 10%

# Complete sampling (testing only)
config = ProfilingConfig(sample_rate=1.0)    # 100%
```

### Adaptive Sampling

Configure dynamic sampling based on conditions:

```python
from provide.foundation.profiling.config import AdaptiveSamplingConfig

config = ProfilingConfig(
    adaptive_sampling=AdaptiveSamplingConfig(
        enabled=True,
        base_rate=0.01,          # Minimum sampling rate
        max_rate=0.20,           # Maximum sampling rate

        # Load-based adjustments
        cpu_threshold=0.70,      # Increase sampling when CPU > 70%
        memory_threshold=0.80,   # Increase sampling when memory > 80%
        latency_threshold_ms=100, # Increase when latency > 100ms

        # Pattern-based triggers
        error_rate_threshold=0.05,    # Increase when error rate > 5%
        slow_operation_threshold=200,  # Increase when operations > 200ms

        # Time-based scheduling
        business_hours_rate=0.05,     # Higher sampling during business hours
        off_hours_rate=0.01,          # Lower sampling during off hours

        # Update frequency
        update_interval_seconds=60    # Recalculate rate every minute
    )
)
```

### Conditional Sampling

Sample only under specific conditions:

```python
from provide.foundation.profiling.config import ConditionalSamplingConfig

config = ProfilingConfig(
    conditional_sampling=ConditionalSamplingConfig(
        conditions=[
            {
                "name": "high_value_users",
                "condition": "user.tier == 'premium'",
                "sample_rate": 0.10
            },
            {
                "name": "critical_operations",
                "condition": "operation in ['checkout', 'payment']",
                "sample_rate": 0.50
            },
            {
                "name": "error_scenarios",
                "condition": "logger.level >= ERROR",
                "sample_rate": 1.0
            }
        ],
        default_rate=0.01  # Default when no conditions match
    )
)
```

## Processor Configuration

### Memory Tracking

Configure memory usage monitoring:

```python
from provide.foundation.profiling.config import ProcessorConfig

config = ProfilingConfig(
    processor=ProcessorConfig(
        # Memory tracking settings
        track_memory=True,
        memory_sampling_interval_ms=100,  # Sample memory every 100ms
        memory_precision="MB",            # Track in MB vs KB/bytes

        # Memory thresholds for alerts
        memory_warning_threshold_mb=100,  # Warn at 100MB usage
        memory_critical_threshold_mb=500, # Critical at 500MB usage

        # Memory growth rate monitoring
        track_memory_growth=True,
        memory_growth_window_seconds=60,  # Track growth over 1 minute
        memory_leak_threshold_mb_per_min=10  # Alert if growing >10MB/min
    )
)
```

### Performance Optimization

Optimize processor performance:

```python
config = ProfilingConfig(
    processor=ProcessorConfig(
        # Buffer configuration
        buffer_size=5000,                 # Larger buffer for high throughput
        buffer_flush_threshold=0.8,       # Flush when 80% full
        max_buffer_memory_mb=50,          # Limit buffer memory usage

        # Batch processing
        enable_batching=True,
        batch_size=100,                   # Process in batches of 100
        batch_timeout_ms=500,             # Flush batches every 500ms

        # Threading
        enable_background_processing=True,
        background_thread_count=2,        # Use 2 background threads
        thread_queue_size=1000,           # Queue size per thread

        # Fast path optimization
        enable_fast_path=True,            # Skip expensive operations when possible
        fast_path_sample_rate=0.1,        # Use fast path for 90% of samples

        # Compression
        enable_compression=True,          # Compress buffered data
        compression_level=6               # Balance compression vs speed
    )
)
```

### Error Handling

Configure error handling behavior:

```python
config = ProfilingConfig(
    processor=ProcessorConfig(
        # Error tolerance
        ignore_sampling_errors=True,      # Don't crash on sampling failures
        max_consecutive_errors=10,        # Disable after 10 consecutive errors
        error_recovery_timeout_seconds=300, # Try to recover after 5 minutes

        # Error reporting
        report_errors_to_logger=True,     # Log profiling errors
        error_log_level="WARNING",        # Log level for errors
        include_error_tracebacks=False,   # Don't include full tracebacks

        # Circuit breaker
        enable_circuit_breaker=True,
        circuit_breaker_failure_threshold=5,
        circuit_breaker_timeout_seconds=60
    )
)
```

## Exporter Configuration

### Multiple Exporters

Configure multiple export destinations:

```python
from provide.foundation.profiling.config import ExporterConfig

config = ProfilingConfig(
    exporters=[
        # Prometheus for metrics
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            enabled=True,
            config={
                "pushgateway_url": "http://prometheus:9091",
                "job_name": "foundation-profiling",
                "push_interval_seconds": 30,
                "labels": {
                    "environment": "production",
                    "service": "api-server"
                }
            }
        ),

        # Datadog for APM
        ExporterConfig(
            name="datadog",
            type="datadog",
            enabled=True,
            config={
                "api_key": "${DATADOG_API_KEY}",
                "site": "datadoghq.com",
                "service": "foundation-profiling",
                "env": "production",
                "tags": ["team:platform", "component:profiling"]
            }
        ),

        # File export for debugging
        ExporterConfig(
            name="debug_file",
            type="file",
            enabled=False,  # Only enable for debugging
            config={
                "output_directory": "/var/log/profiling",
                "file_format": "jsonl",
                "rotation_policy": "size",
                "max_file_size": "100MB"
            }
        )
    ]
)
```

### Export Filtering

Filter what data gets exported:

```python
config = ProfilingConfig(
    exporters=[
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            config={
                "pushgateway_url": "http://prometheus:9091"
            },
            filters={
                # Only export specific metrics
                "include_metrics": [
                    "messages_per_second",
                    "avg_latency_ms",
                    "error_rate"
                ],

                # Exclude debug-level data
                "exclude_log_levels": ["DEBUG"],

                # Only export during business hours
                "time_filter": {
                    "start_hour": 6,
                    "end_hour": 22,
                    "timezone": "US/Eastern"
                },

                # Sample exports (don't export every metric)
                "export_sample_rate": 0.5
            }
        )
    ]
)
```

### Export Buffering

Configure export buffering and batching:

```python
config = ProfilingConfig(
    exporters=[
        ExporterConfig(
            name="datadog",
            type="datadog",
            config={
                "api_key": "${DATADOG_API_KEY}",

                # Buffering configuration
                "buffer_size": 1000,              # Buffer up to 1000 metrics
                "flush_interval_seconds": 60,     # Flush every minute
                "max_buffer_age_seconds": 300,    # Force flush after 5 minutes

                # Batch configuration
                "batch_size": 100,                # Send in batches of 100
                "max_batch_size": 500,            # Never exceed 500 per batch
                "batch_timeout_ms": 5000,         # Wait max 5s to fill batch

                # Memory management
                "max_memory_usage_mb": 100,       # Limit buffer memory
                "drop_oldest_on_overflow": True,  # Drop old data if buffer full

                # Compression
                "compress_batches": True,
                "compression_type": "gzip"
            }
        )
    ]
)
```

## Environment-Specific Configuration

### Development Environment

```python
# Development configuration
dev_config = ProfilingConfig(
    enabled=True,
    sample_rate=0.50,  # High sampling for detailed insights

    processor=ProcessorConfig(
        track_memory=True,              # Enable memory tracking
        enable_fast_path=False,         # Disable optimizations for accuracy
        buffer_size=100,                # Small buffer for quick feedback
        flush_interval_seconds=10       # Frequent flushing
    ),

    cli=CLIConfig(
        enabled=True,
        include_reset_option=True,      # Allow resetting metrics
        include_debug_commands=True     # Enable debug commands
    ),

    exporters=[
        ExporterConfig(
            name="console",
            type="console",             # Output to console
            config={"format": "pretty", "colors": True}
        ),
        ExporterConfig(
            name="file",
            type="file",
            config={
                "output_directory": "./profiling",
                "file_format": "json",
                "pretty_print": True    # Human-readable JSON
            }
        )
    ]
)
```

### Staging Environment

```python
# Staging configuration
staging_config = ProfilingConfig(
    enabled=True,
    sample_rate=0.10,  # Moderate sampling

    processor=ProcessorConfig(
        track_memory=True,
        enable_fast_path=True,
        buffer_size=1000,
        flush_interval_seconds=30
    ),

    adaptive_sampling=AdaptiveSamplingConfig(
        enabled=True,
        base_rate=0.05,
        max_rate=0.30,
        cpu_threshold=0.80,
        memory_threshold=0.85
    ),

    exporters=[
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            config={
                "pushgateway_url": "http://prometheus-staging:9091",
                "job_name": "foundation-profiling-staging"
            }
        )
    ]
)
```

### Production Environment

```python
# Production configuration
prod_config = ProfilingConfig(
    enabled=True,
    sample_rate=0.02,  # Conservative sampling

    processor=ProcessorConfig(
        track_memory=False,             # Disable memory tracking for performance
        enable_fast_path=True,
        buffer_size=5000,               # Large buffer
        flush_interval_seconds=60,      # Less frequent flushing
        enable_circuit_breaker=True     # Protection against failures
    ),

    adaptive_sampling=AdaptiveSamplingConfig(
        enabled=True,
        base_rate=0.01,
        max_rate=0.15,                  # Conservative maximum
        update_interval_seconds=300     # Less frequent updates
    ),

    exporters=[
        ExporterConfig(
            name="datadog",
            type="datadog",
            config={
                "api_key": "${DATADOG_API_KEY}",
                "buffer_size": 2000,
                "flush_interval_seconds": 60,
                "retry_config": {
                    "max_retries": 3,
                    "backoff_multiplier": 2.0
                }
            }
        ),
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            config={
                "pushgateway_url": "http://prometheus:9091",
                "push_interval_seconds": 60
            }
        )
    ]
)
```

## Advanced Configuration

### Custom Metrics

Define custom metrics collection:

```python
from provide.foundation.profiling.config import CustomMetricsConfig

config = ProfilingConfig(
    custom_metrics=CustomMetricsConfig(
        enabled=True,
        metrics=[
            {
                "name": "business_operation_latency",
                "type": "histogram",
                "description": "Latency of business operations",
                "buckets": [10, 50, 100, 200, 500, 1000],
                "labels": ["operation_type", "user_tier"]
            },
            {
                "name": "feature_usage_count",
                "type": "counter",
                "description": "Count of feature usage",
                "labels": ["feature_name", "user_id"]
            },
            {
                "name": "system_resource_usage",
                "type": "gauge",
                "description": "Current system resource usage",
                "labels": ["resource_type"]
            }
        ]
    )
)
```

### Security Configuration

Configure security settings:

```python
from provide.foundation.profiling.config import SecurityConfig

config = ProfilingConfig(
    security=SecurityConfig(
        # Data sanitization
        sanitize_user_data=True,
        pii_fields_to_remove=[
            "email", "phone", "ssn", "credit_card"
        ],
        hash_sensitive_fields=True,

        # Export security
        require_tls_for_exports=True,
        validate_export_certificates=True,

        # Access control
        require_authentication=True,
        allowed_roles=["admin", "monitoring"],

        # Data retention
        max_data_retention_days=30,
        auto_purge_old_data=True
    )
)
```

### Integration Configuration

Configure integrations with other systems:

```python
from provide.foundation.profiling.config import IntegrationConfig

config = ProfilingConfig(
    integrations=IntegrationConfig(
        # OpenTelemetry integration
        opentelemetry={
            "enabled": True,
            "trace_integration": True,
            "metrics_integration": True,
            "resource_attributes": {
                "service.name": "foundation-profiling",
                "service.version": "1.0.0"
            }
        },

        # Sentry integration
        sentry={
            "enabled": True,
            "dsn": "${SENTRY_DSN}",
            "send_performance_data": True,
            "sample_rate": 0.1
        },

        # Custom webhook integration
        webhooks=[
            {
                "name": "alerts",
                "url": "https://alerts.company.com/webhook",
                "events": ["high_latency", "error_spike"],
                "auth_header": "Bearer ${WEBHOOK_TOKEN}"
            }
        ]
    )
)
```

## Configuration Validation

### Schema Validation

Validate configuration against schema:

```python
from provide.foundation.profiling.config import validate_config

# Validate configuration
try:
    validate_config(config)
    print("✅ Configuration is valid")
except ValidationError as e:
    print(f"❌ Configuration error: {e}")
```

### Runtime Validation

Check configuration at runtime:

```python
from provide.foundation.profiling.config import ConfigValidator

validator = ConfigValidator()

# Check if configuration is feasible
validation_result = validator.validate_runtime_config(config)

if not validation_result.is_valid:
    print("Configuration issues:")
    for issue in validation_result.issues:
        print(f"  - {issue.severity}: {issue.message}")
```

### Performance Impact Assessment

Assess performance impact of configuration:

```python
from provide.foundation.profiling.config import assess_performance_impact

impact = assess_performance_impact(config)

print(f"Estimated overhead: {impact.estimated_overhead_percent:.2f}%")
print(f"Memory usage: {impact.estimated_memory_mb:.1f}MB")
print(f"CPU impact: {impact.cpu_impact_level}")

if impact.has_warnings:
    print("Performance warnings:")
    for warning in impact.warnings:
        print(f"  - {warning}")
```

## Configuration Best Practices

### Environment Separation

```python
# Use environment-specific configurations
import os

env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    config = load_production_config()
elif env == "staging":
    config = load_staging_config()
else:
    config = load_development_config()
```

### Secret Management

```python
# Use proper secret management
from provide.foundation.profiling.config import SecretResolver

config = ProfilingConfig.from_file(
    "profiling.yaml",
    secret_resolver=SecretResolver(
        backends=["env", "vault", "aws_secrets"]
    )
)
```

### Configuration Monitoring

```python
# Monitor configuration changes
from provide.foundation.profiling.config import ConfigWatcher

watcher = ConfigWatcher(
    config_file="profiling.yaml",
    on_change=lambda new_config: reload_profiling_config(new_config),
    validate_before_reload=True
)
watcher.start()
```

## Troubleshooting Configuration

### Common Issues

**Configuration not loading**
```python
# Debug configuration loading
from provide.foundation.profiling.config import debug_config_loading

debug_config_loading(
    config_file="profiling.yaml",
    show_resolution_steps=True,
    validate_environment_vars=True
)
```

**Invalid sampling rate**
```python
# Validate sampling rate
if not 0.0 <= config.sample_rate <= 1.0:
    raise ValueError(f"Sample rate must be between 0.0 and 1.0, got {config.sample_rate}")
```

**Exporter connection failures**
```python
# Test exporter connections
for exporter_config in config.exporters:
    try:
        exporter = create_exporter(exporter_config)
        health = exporter.health_check()
        if not health.is_healthy():
            print(f"Exporter {exporter_config.name} is unhealthy: {health.error}")
    except Exception as e:
        print(f"Failed to create exporter {exporter_config.name}: {e}")
```