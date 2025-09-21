# Profiling Best Practices

Production-tested guidelines for deploying and operating Foundation's profiling system effectively.

## Production Deployment

### Sampling Strategy

**Start Conservative and Iterate**

```python
# Week 1: Conservative baseline
register_profiling(hub, sample_rate=0.005)  # 0.5%

# Week 2: Increase if overhead acceptable
register_profiling(hub, sample_rate=0.01)   # 1%

# Week 3: Optimize based on data
register_profiling(hub, sample_rate=0.02)   # 2% (typical production target)
```

**Use Adaptive Sampling for Dynamic Workloads**

```python
from provide.foundation.profiling.sampling import LoadBasedSampler

# Automatically adjust based on system load
sampler = LoadBasedSampler(
    base_rate=0.01,          # 1% baseline
    max_rate=0.10,           # Never exceed 10%
    cpu_threshold=0.75,      # Increase when CPU > 75%
    memory_threshold=0.85,   # Increase when memory > 85%
    latency_threshold_ms=200 # Increase when slow
)

register_profiling(hub, sampler=sampler)
```

### Performance Monitoring

**Monitor Profiling Overhead**

```python
# Set up overhead monitoring
from provide.foundation.profiling.monitoring import OverheadMonitor

monitor = OverheadMonitor(
    alert_threshold_percent=1.0,  # Alert if overhead > 1%
    measurement_interval_minutes=5,
    metrics_export=True
)

# Alert if profiling impact is too high
@monitor.on_high_overhead
def handle_high_overhead(overhead_percent):
    logger.warning(
        "Profiling overhead high - reducing sample rate",
        overhead_percent=overhead_percent,
        emoji="⚠️"
    )
    # Automatically reduce sampling
    profiler.update_sample_rate(profiler.sample_rate * 0.5)
```

**Track Key Performance Indicators**

```python
# Monitor these metrics in production
key_metrics = [
    "profiling_overhead_percent",     # < 1%
    "sample_rate_current",            # Track adaptive changes
    "export_success_rate",            # > 95%
    "export_latency_p95_ms",         # < 1000ms
    "buffer_utilization_percent",     # < 80%
    "dropped_samples_rate"            # < 5%
]
```

### Resource Management

**Memory Management**

```python
from provide.foundation.profiling.config import ProcessorConfig

config = ProfilingConfig(
    processor=ProcessorConfig(
        # Limit memory usage
        max_buffer_memory_mb=100,        # Cap buffer at 100MB
        buffer_flush_threshold=0.8,      # Flush at 80% capacity
        enable_compression=True,         # Compress buffered data

        # Memory leak protection
        max_buffer_age_seconds=300,      # Force flush old data
        drop_oldest_on_overflow=True,    # Drop old vs crash

        # Garbage collection hints
        force_gc_interval_seconds=600    # Trigger GC every 10 minutes
    )
)
```

**CPU Optimization**

```python
config = ProfilingConfig(
    processor=ProcessorConfig(
        # Reduce CPU impact
        enable_fast_path=True,           # Use optimized code paths
        batch_processing=True,           # Process in batches
        background_processing=True,      # Use background threads

        # Limit processing frequency
        max_processing_rate_per_second=1000,  # Limit to 1000 samples/sec
        processing_queue_size=5000,      # Limit queue depth

        # Optimize expensive operations
        skip_stack_traces=True,          # Don't capture stack traces
        minimal_metadata=True            # Reduce metadata collection
    )
)
```

## Environment-Specific Guidelines

### Development Environment

```python
# Development: High visibility, detailed data
dev_config = ProfilingConfig(
    sample_rate=1.0,  # 100% sampling for complete visibility

    processor=ProcessorConfig(
        track_memory=True,               # Enable all tracking
        track_exceptions=True,
        capture_stack_traces=True,
        detailed_timing=True
    ),

    exporters=[
        # Console output for immediate feedback
        ConsoleExporter(format="pretty", colors=True),

        # File export for analysis
        FileExporter(
            output_directory="./profiling",
            format="json",
            pretty_print=True
        )
    ]
)
```

### Staging Environment

```python
# Staging: Production-like with more detailed monitoring
staging_config = ProfilingConfig(
    sample_rate=0.10,  # 10% sampling for good coverage

    adaptive_sampling=AdaptiveSamplingConfig(
        enabled=True,
        base_rate=0.05,
        max_rate=0.50,  # Higher ceiling for testing
        pattern_detection=True
    ),

    exporters=[
        PrometheusExporter(
            pushgateway_url="http://prometheus-staging:9091",
            labels={"environment": "staging"}
        ),

        # Detailed logging for debugging
        FileExporter(
            output_directory="/var/log/profiling",
            rotation_policy="hourly",
            format="jsonl"
        )
    ]
)
```

### Production Environment

```python
# Production: Conservative, reliable, monitored
prod_config = ProfilingConfig(
    sample_rate=0.02,  # 2% baseline

    processor=ProcessorConfig(
        # Optimized for production
        enable_fast_path=True,
        track_memory=False,              # Disable expensive tracking
        minimal_metadata=True,

        # Resilience features
        enable_circuit_breaker=True,
        max_consecutive_errors=5,
        error_recovery_timeout_seconds=300
    ),

    adaptive_sampling=AdaptiveSamplingConfig(
        enabled=True,
        base_rate=0.01,
        max_rate=0.15,                   # Conservative ceiling
        cpu_threshold=0.80,              # React to high load
        update_interval_seconds=300      # Stable adjustments
    ),

    exporters=[
        # Primary monitoring
        DatadogExporter(
            api_key="${DATADOG_API_KEY}",
            buffer_size=2000,
            retry_config=RetryConfig(max_retries=3)
        ),

        # Backup/secondary monitoring
        PrometheusExporter(
            pushgateway_url="http://prometheus:9091",
            fallback=True
        ),

        # Emergency logging
        FileExporter(
            output_directory="/var/log/profiling/emergency",
            enabled=False,  # Only enabled during incidents
            format="compact"
        )
    ]
)
```

## Integration Patterns

### Web Applications

**FastAPI with Request Context**

```python
from fastapi import FastAPI, Request
from provide.foundation.profiling.decorators import profile_async

app = FastAPI()

@app.middleware("http")
async def profiling_middleware(request: Request, call_next):
    """Add request context to profiling."""
    from provide.foundation.profiling.context import set_profiling_context

    # Set context for all profiling within this request
    with set_profiling_context({
        "request_id": request.headers.get("x-request-id"),
        "user_agent": request.headers.get("user-agent"),
        "endpoint": str(request.url.path),
        "method": request.method
    }):
        response = await call_next(request)
        return response

@app.get("/api/users/{user_id}")
@profile_async(
    name="get_user_api",
    context_fields=["user_id"],
    track_memory=True
)
async def get_user(user_id: int):
    """API endpoint with automatic profiling."""
    # Profiling automatically includes request context
    return await fetch_user_data(user_id)
```

**Django with Class-Based Views**

```python
from django.views.generic import View
from provide.foundation.profiling.django import ProfiledViewMixin

class UserListView(ProfiledViewMixin, View):
    """Django view with automatic profiling."""

    # Profiling configuration
    profiling_config = {
        "sample_rate": 0.05,
        "track_memory": True,
        "context_fields": ["user.id", "request.path"]
    }

    def get(self, request):
        """Automatically profiled by ProfiledViewMixin."""
        users = self.get_user_list()
        return JsonResponse({"users": users})

    @profile_function(name="user_list_query")
    def get_user_list(self):
        """Additional explicit profiling."""
        return User.objects.filter(active=True)[:100]
```

### Background Workers

**Celery Task Profiling**

```python
from celery import Celery
from provide.foundation.profiling.decorators import profile_function

app = Celery('myapp')

@app.task
@profile_function(
    name="process_batch_task",
    track_memory=True,
    context_fields=["batch_id", "user_id"]
)
def process_user_batch(batch_id: str, user_ids: list[int]):
    """Celery task with profiling."""
    from provide.foundation import logger

    logger.info(
        "Starting batch processing",
        batch_id=batch_id,
        user_count=len(user_ids),
        emoji="⚙️"
    )

    results = []
    for user_id in user_ids:
        result = process_single_user(user_id)
        results.append(result)

    logger.info(
        "Batch processing complete",
        batch_id=batch_id,
        success_count=len(results),
        emoji="✅"
    )

    return results

@profile_function(name="single_user_processing")
def process_single_user(user_id: int):
    """Individual user processing with profiling."""
    # Processing logic here
    pass
```

**RQ Worker Setup**

```python
import rq
from provide.foundation.profiling import register_profiling
from provide.foundation.hub import get_hub

def setup_worker_profiling():
    """Setup profiling for RQ worker."""
    hub = get_hub()

    # Lower sampling for workers to reduce overhead
    register_profiling(hub, sample_rate=0.005)

    profiler = hub.get_component("profiler")
    profiler.enable()

    # Add worker context
    from provide.foundation.profiling.context import set_profiling_context
    set_profiling_context({
        "worker_type": "rq",
        "worker_id": os.getpid(),
        "queue_name": os.getenv("RQ_QUEUE", "default")
    })

# Initialize profiling when worker starts
setup_worker_profiling()
```

### Microservices

**Service-to-Service Profiling**

```python
import httpx
from provide.foundation.profiling.decorators import profile_async

class UserService:
    """User service with profiled external calls."""

    @profile_async(
        name="fetch_user_profile",
        context_fields=["user_id"],
        track_memory=True
    )
    async def get_user_profile(self, user_id: int) -> UserProfile:
        """Fetch user profile from external service."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://user-service/api/users/{user_id}",
                timeout=5.0
            )
            response.raise_for_status()
            return UserProfile.from_json(response.json())

    @profile_async(name="update_user_preferences")
    async def update_preferences(self, user_id: int, prefs: dict) -> bool:
        """Update user preferences."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://user-service/api/users/{user_id}/preferences",
                json=prefs,
                timeout=10.0
            )
            return response.status_code == 200
```

## Monitoring and Alerting

### Key Metrics to Monitor

```python
# Production monitoring checklist
monitoring_metrics = {
    # Performance metrics
    "foundation.profiling.overhead_percent": {
        "alert_threshold": 1.0,
        "critical_threshold": 2.0,
        "description": "Profiling CPU overhead"
    },

    "foundation.profiling.memory_usage_mb": {
        "alert_threshold": 100,
        "critical_threshold": 200,
        "description": "Profiling memory usage"
    },

    "foundation.profiling.sample_rate": {
        "min_threshold": 0.001,
        "max_threshold": 0.20,
        "description": "Current sampling rate"
    },

    # Export metrics
    "foundation.profiling.export_success_rate": {
        "alert_threshold": 0.95,
        "critical_threshold": 0.90,
        "description": "Export success rate"
    },

    "foundation.profiling.export_latency_p95": {
        "alert_threshold": 1000,
        "critical_threshold": 5000,
        "description": "Export latency P95 (ms)"
    },

    # Data quality metrics
    "foundation.profiling.dropped_samples_rate": {
        "alert_threshold": 0.05,
        "critical_threshold": 0.10,
        "description": "Rate of dropped samples"
    }
}
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: foundation_profiling
    rules:
      - alert: ProfilingOverheadHigh
        expr: foundation_profiling_overhead_percent > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Foundation profiling overhead is high"
          description: "Profiling overhead is {{ $value }}%, exceeding 1% threshold"

      - alert: ProfilingExportsFailing
        expr: rate(foundation_profiling_export_failures_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Foundation profiling exports are failing"
          description: "{{ $value | humanizePercentage }} of profiling exports are failing"

      - alert: ProfilingSampleRateUnusual
        expr: |
          foundation_profiling_sample_rate > 0.20 or
          foundation_profiling_sample_rate < 0.001
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Foundation profiling sample rate is unusual"
          description: "Sample rate is {{ $value }}, outside normal range"
```

### Health Checks

```python
from provide.foundation.profiling.health import ProfilingHealthChecker

def check_profiling_health():
    """Comprehensive profiling health check."""
    checker = ProfilingHealthChecker()

    health_report = checker.check_all([
        "profiler_enabled",
        "sample_rate_reasonable",
        "export_success_rate",
        "memory_usage",
        "cpu_overhead",
        "buffer_health"
    ])

    if not health_report.is_healthy():
        # Log health issues
        from provide.foundation import logger
        for issue in health_report.issues:
            logger.warning(
                "Profiling health issue",
                issue=issue.description,
                severity=issue.severity,
                emoji="⚠️"
            )

    return health_report

# Integrate with your application's health endpoint
@app.get("/health")
async def health_check():
    """Application health check including profiling."""
    health = {
        "status": "healthy",
        "profiling": check_profiling_health().to_dict()
    }

    return health
```

## Security Considerations

### Data Sanitization

```python
from provide.foundation.profiling.config import SecurityConfig

secure_config = ProfilingConfig(
    security=SecurityConfig(
        # Remove sensitive data
        sanitize_user_data=True,
        pii_fields=["email", "phone", "ssn", "address"],
        hash_user_ids=True,

        # Limit data collection
        max_field_length=1000,      # Truncate long fields
        exclude_headers=["authorization", "cookie"],
        exclude_query_params=["token", "api_key"],

        # Export security
        require_tls=True,
        validate_certificates=True,
        encrypt_at_rest=True
    )
)
```

### Access Control

```python
from provide.foundation.profiling.auth import ProfilingAuth

# Restrict profiling command access
auth = ProfilingAuth(
    require_authentication=True,
    allowed_roles=["admin", "sre", "monitoring"],
    token_validation_endpoint="https://auth.company.com/validate"
)

# Apply to CLI commands
register_profiling(hub, auth=auth)
```

## Troubleshooting

### Performance Issues

**High Overhead Diagnosis**

```python
from provide.foundation.profiling.diagnostics import PerformanceDiagnostic

# Analyze what's causing overhead
diagnostic = PerformanceDiagnostic()
analysis = diagnostic.analyze_overhead()

print(f"Total overhead: {analysis.total_overhead_percent:.2f}%")
print("Breakdown:")
for component, overhead in analysis.component_breakdown.items():
    print(f"  {component}: {overhead:.3f}%")

# Recommendations
for recommendation in analysis.recommendations:
    print(f"💡 {recommendation}")
```

**Memory Usage Optimization**

```python
from provide.foundation.profiling.diagnostics import MemoryDiagnostic

# Analyze memory usage patterns
diagnostic = MemoryDiagnostic()
memory_report = diagnostic.analyze_memory_usage()

if memory_report.has_leaks:
    print("🚨 Potential memory leaks detected:")
    for leak in memory_report.potential_leaks:
        print(f"  {leak.component}: {leak.growth_rate_mb_per_hour:.1f} MB/hour")

# Optimization suggestions
for suggestion in memory_report.optimization_suggestions:
    print(f"💡 {suggestion}")
```

### Common Problems and Solutions

**Problem: Exports Failing Intermittently**

```python
# Solution: Add resilience and monitoring
resilient_config = ProfilingConfig(
    exporters=[
        ExporterConfig(
            name="datadog",
            type="datadog",
            config={
                "api_key": "${DATADOG_API_KEY}",

                # Add resilience
                "retry_config": {
                    "max_retries": 5,
                    "backoff_multiplier": 2.0,
                    "jitter": True
                },

                # Circuit breaker
                "circuit_breaker": {
                    "failure_threshold": 3,
                    "timeout_seconds": 60
                },

                # Fallback
                "fallback_exporter": "file"
            }
        )
    ]
)
```

**Problem: Sample Rate Too Aggressive**

```python
# Solution: Implement adaptive sampling with safety limits
from provide.foundation.profiling.sampling import SafeAdaptiveSampler

safe_sampler = SafeAdaptiveSampler(
    base_rate=0.01,
    max_rate=0.05,                    # Conservative maximum
    overhead_limit_percent=0.5,       # Never exceed 0.5% overhead
    auto_reduce_on_high_load=True,    # Automatically reduce under load
    emergency_disable_threshold=2.0   # Disable if overhead > 2%
)
```

**Problem: Missing Data in Monitoring System**

```python
# Solution: Add data validation and monitoring
validated_config = ProfilingConfig(
    exporters=[
        ExporterConfig(
            name="prometheus",
            type="prometheus",
            config={
                "pushgateway_url": "http://prometheus:9091",

                # Validation
                "validate_before_export": True,
                "schema_validation": True,

                # Monitoring
                "export_monitoring": True,
                "success_rate_threshold": 0.95,

                # Debugging
                "debug_failed_exports": True,
                "log_export_attempts": True
            }
        )
    ]
)
```

## Migration and Upgrades

### Gradual Rollout

```python
# Phase 1: Enable with minimal sampling
phase1_config = ProfilingConfig(
    sample_rate=0.001,  # 0.1% sampling
    exporters=[FileExporter(output_directory="/tmp/profiling")]
)

# Phase 2: Increase sampling and add monitoring
phase2_config = ProfilingConfig(
    sample_rate=0.01,   # 1% sampling
    exporters=[
        FileExporter(output_directory="/var/log/profiling"),
        PrometheusExporter(pushgateway_url="http://prometheus:9091")
    ]
)

# Phase 3: Full production deployment
phase3_config = ProfilingConfig(
    sample_rate=0.02,   # 2% sampling
    adaptive_sampling=AdaptiveSamplingConfig(enabled=True),
    exporters=[
        DatadogExporter(api_key="${DATADOG_API_KEY}"),
        PrometheusExporter(pushgateway_url="http://prometheus:9091")
    ]
)
```

### A/B Testing Profiling Changes

```python
from provide.foundation.profiling.testing import ABTestingConfig

# Test different sampling rates
ab_config = ABTestingConfig(
    test_name="sampling_rate_optimization",
    variants=[
        {"name": "control", "sample_rate": 0.01},      # 1%
        {"name": "treatment", "sample_rate": 0.03}     # 3%
    ],
    traffic_split={"control": 0.8, "treatment": 0.2}, # 80/20 split
    success_metrics=["overhead_percent", "data_quality_score"],
    duration_days=7
)

register_profiling(hub, ab_testing=ab_config)
```

This comprehensive guide provides the foundation for successfully deploying and operating profiling in production environments. Always start conservatively, monitor carefully, and iterate based on real-world performance data.