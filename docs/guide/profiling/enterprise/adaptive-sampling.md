# Adaptive Sampling

!!! info "Planned Enterprise Feature"
    Intelligent sampling that automatically adjusts collection rates based on system load, performance patterns, and resource utilization.

!!! warning "Implementation Status"
    This feature is planned for Foundation v1.1+. This documentation serves as a specification and design guide for the upcoming implementation.

## Overview

Adaptive sampling dynamically adjusts profiling sample rates based on real-time system conditions, ensuring optimal performance monitoring without impacting application performance. The system intelligently increases sampling during interesting events and reduces it during normal operations.

## Core Sampling Strategies

### Load-Based Sampling

Automatically adjust sampling based on system resource utilization:

```python
from provide.foundation.profiling.sampling import LoadBasedSampler

# Create load-based sampler
sampler = LoadBasedSampler(
    base_rate=0.01,          # Minimum sampling rate (1%)
    max_rate=0.20,           # Maximum sampling rate (20%)
    cpu_threshold=0.70,      # Increase sampling when CPU > 70%
    memory_threshold=0.80,   # Increase sampling when memory > 80%
    response_time_threshold=100,  # Increase when response time > 100ms
)

# Register with profiling system
from provide.foundation.profiling import register_profiling

register_profiling(
    hub,
    sampler=sampler,
    adaptive=True
)
```

Real-time sampling adjustment:

```python
# Sampler automatically adjusts based on system metrics
current_cpu = get_cpu_usage()       # 45% CPU usage
current_memory = get_memory_usage() # 60% memory usage
current_latency = get_avg_latency() # 50ms average latency

# Sampler calculates: base rate since all thresholds under limits
effective_rate = sampler.get_current_rate()  # Returns ~0.01 (1%)

# During high load:
# CPU: 85%, Memory: 90%, Latency: 150ms
# Sampler increases rate to ~0.18 (18%) for detailed monitoring
```

### Pattern-Based Sampling

Increase sampling during specific patterns or anomalies:

```python
from provide.foundation.profiling.sampling import PatternBasedSampler

sampler = PatternBasedSampler(
    base_rate=0.02,
    patterns={
        # Increase sampling for error patterns
        "error_burst": {
            "condition": "error_rate > 0.05",  # > 5% error rate
            "rate_multiplier": 10,             # 10x base rate
            "duration_seconds": 300            # Maintain for 5 minutes
        },

        # Increase sampling for slow operations
        "slow_operations": {
            "condition": "avg_latency > 200",  # > 200ms average
            "rate_multiplier": 5,              # 5x base rate
            "duration_seconds": 180            # Maintain for 3 minutes
        },

        # Increase sampling for memory spikes
        "memory_pressure": {
            "condition": "memory_growth_rate > 10",  # > 10MB/minute
            "rate_multiplier": 8,                    # 8x base rate
            "duration_seconds": 600                  # Maintain for 10 minutes
        }
    }
)

# Register pattern-based sampler
register_profiling(hub, sampler=sampler)
```

### Time-Based Sampling

Vary sampling rates based on time patterns:

```python
from provide.foundation.profiling.sampling import TimeBasedSampler

sampler = TimeBasedSampler(
    schedules={
        # High sampling during business hours
        "business_hours": {
            "time_pattern": "09:00-17:00",
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "rate": 0.10,  # 10% sampling
            "timezone": "US/Eastern"
        },

        # Medium sampling during extended hours
        "extended_hours": {
            "time_pattern": "06:00-09:00,17:00-22:00",
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "rate": 0.05,  # 5% sampling
        },

        # Low sampling during off-hours
        "off_hours": {
            "time_pattern": "22:00-06:00",
            "rate": 0.01,  # 1% sampling
        },

        # High sampling during weekends (maintenance window)
        "weekend_maintenance": {
            "days": ["saturday", "sunday"],
            "time_pattern": "02:00-06:00",
            "rate": 0.25,  # 25% sampling for detailed monitoring
        }
    },
    default_rate=0.02  # Default when no schedule matches
)
```

## Advanced Sampling Algorithms

### Machine Learning-Based Sampling

Use ML models to predict optimal sampling rates:

```python
from provide.foundation.profiling.sampling import MLBasedSampler

sampler = MLBasedSampler(
    model_type="random_forest",     # or "neural_network", "gradient_boost"
    features=[
        "cpu_usage",
        "memory_usage",
        "request_rate",
        "error_rate",
        "avg_latency",
        "hour_of_day",
        "day_of_week"
    ],
    target="optimal_sample_rate",
    training_window_days=30,        # Retrain model every 30 days
    min_rate=0.005,                 # Never go below 0.5%
    max_rate=0.30,                  # Never exceed 30%
    update_interval_minutes=5       # Recalculate rate every 5 minutes
)

# Sampler learns from historical data to predict optimal rates
# Automatically adapts to application-specific patterns
register_profiling(hub, sampler=sampler)
```

### Statistical Sampling

Use statistical methods to ensure representative sample collection:

```python
from provide.foundation.profiling.sampling import StatisticalSampler

sampler = StatisticalSampler(
    strategy="stratified",          # or "systematic", "cluster"
    strata=[
        {
            "name": "fast_operations",
            "condition": "execution_time < 10ms",
            "rate": 0.005,  # Low sampling for fast operations
            "min_samples_per_hour": 100
        },
        {
            "name": "medium_operations",
            "condition": "10ms <= execution_time < 100ms",
            "rate": 0.02,   # Medium sampling
            "min_samples_per_hour": 200
        },
        {
            "name": "slow_operations",
            "condition": "execution_time >= 100ms",
            "rate": 0.50,   # High sampling for slow operations
            "min_samples_per_hour": 50
        }
    ],
    confidence_level=0.95,          # 95% confidence in samples
    margin_of_error=0.05            # 5% margin of error
)
```

## Sampling Triggers

### Event-Driven Sampling

Increase sampling in response to specific events:

```python
from provide.foundation.profiling.sampling import EventDrivenSampler

sampler = EventDrivenSampler(
    base_rate=0.01,
    triggers=[
        {
            "name": "deployment_trigger",
            "event": "deployment_started",
            "rate": 0.25,               # 25% sampling during deployments
            "duration_minutes": 30,     # Maintain for 30 minutes
            "cooldown_minutes": 10      # Wait 10 minutes before retriggering
        },
        {
            "name": "alert_trigger",
            "event": "performance_alert",
            "rate": 0.50,               # 50% sampling during alerts
            "duration_minutes": 15,
            "auto_escalate": True       # Increase to 100% if alert persists
        },
        {
            "name": "user_request_trigger",
            "event": "debug_mode_enabled",
            "rate": 1.0,                # 100% sampling for debug sessions
            "duration_minutes": 60,
            "user_specific": True       # Only for requesting user
        }
    ]
)

# Trigger events programmatically
sampler.trigger_event("deployment_started")

# Or integrate with external systems
sampler.listen_for_events(
    webhook_url="/profiling/events",
    auth_token="your-webhook-token"
)
```

### Circuit Breaker Sampling

Protect system performance with circuit breaker patterns:

```python
from provide.foundation.profiling.sampling import CircuitBreakerSampler

sampler = CircuitBreakerSampler(
    base_rate=0.02,
    circuit_breaker={
        "failure_threshold": 5,         # Trip after 5 failures
        "success_threshold": 3,         # Reset after 3 successes
        "timeout_seconds": 60,          # Try reset after 60 seconds
        "failure_conditions": [
            "cpu_usage > 0.95",          # CPU > 95%
            "memory_usage > 0.90",       # Memory > 90%
            "response_time > 1000",      # Response time > 1s
            "error_rate > 0.10"          # Error rate > 10%
        ]
    },
    fallback_rate=0.001,               # Emergency low rate when circuit open
    recovery_rate=0.005                # Conservative rate during recovery
)

# Circuit breaker automatically protects against performance degradation
# while maintaining minimal monitoring capability
```

## Configuration and Customization

### Custom Sampling Functions

Create domain-specific sampling strategies:

```python
from provide.foundation.profiling.sampling import CustomSampler

def e_commerce_sampling_function(context: SamplingContext) -> float:
    """Custom sampling for e-commerce application."""

    # High sampling during peak shopping hours
    hour = context.current_time.hour
    if 10 <= hour <= 14 or 19 <= hour <= 22:  # Lunch and evening
        base_rate = 0.10
    else:
        base_rate = 0.02

    # Increase sampling for high-value operations
    if context.operation_name in ["checkout", "payment", "order_processing"]:
        base_rate *= 5

    # Increase sampling for VIP users
    if context.user_tier == "premium":
        base_rate *= 2

    # Reduce sampling for health checks
    if context.operation_name.startswith("health_"):
        base_rate *= 0.1

    # Dynamic adjustment based on cart value
    if hasattr(context, "cart_value") and context.cart_value > 1000:
        base_rate *= 3  # Monitor high-value transactions closely

    return min(base_rate, 0.80)  # Cap at 80%

sampler = CustomSampler(sampling_function=e_commerce_sampling_function)
```

### Multi-Dimensional Sampling

Sample based on multiple application dimensions:

```python
from provide.foundation.profiling.sampling import MultiDimensionalSampler

sampler = MultiDimensionalSampler(
    dimensions={
        "user_type": {
            "free": 0.005,      # 0.5% for free users
            "premium": 0.02,    # 2% for premium users
            "enterprise": 0.05  # 5% for enterprise users
        },
        "operation_type": {
            "read": 0.01,       # 1% for read operations
            "write": 0.05,      # 5% for write operations
            "delete": 0.20,     # 20% for delete operations
            "admin": 0.50       # 50% for admin operations
        },
        "data_size": {
            "small": 0.01,      # < 1KB: 1%
            "medium": 0.03,     # 1KB-1MB: 3%
            "large": 0.10       # > 1MB: 10%
        }
    },
    combination_strategy="multiplicative",  # Multiply rates across dimensions
    max_combined_rate=0.80                 # Cap combined rate
)

# Usage automatically considers all applicable dimensions
# Example: Enterprise user doing large write operation
# Rate = 0.05 * 0.05 * 0.10 = 0.00025 (capped by max_combined_rate)
```

## Integration with Monitoring Systems

### Prometheus Integration

Export sampling metrics to Prometheus:

```python
from provide.foundation.profiling.sampling import PrometheusIntegratedSampler

sampler = PrometheusIntegratedSampler(
    base_sampler=LoadBasedSampler(),
    prometheus_config={
        "pushgateway_url": "http://prometheus-pushgateway:9091",
        "job_name": "foundation_profiling",
        "metrics": [
            "current_sample_rate",
            "samples_collected_total",
            "samples_dropped_total",
            "sampling_overhead_seconds",
            "trigger_events_total"
        ],
        "push_interval_seconds": 30
    }
)

# Metrics automatically available in Prometheus for alerting and dashboards
```

### OpenTelemetry Integration

Integrate sampling decisions with OpenTelemetry spans:

```python
from provide.foundation.profiling.sampling import OTelIntegratedSampler

sampler = OTelIntegratedSampler(
    base_sampler=PatternBasedSampler(),
    otel_config={
        "trace_sample_rate_attribute": "profiling.sample_rate",
        "sampling_decision_attribute": "profiling.sampling_decision",
        "trigger_event_attribute": "profiling.trigger_event",
        "create_sampling_spans": True,
        "span_name_prefix": "profiling.sampling"
    }
)

# Sampling decisions become part of distributed traces
# Enables correlation between profiling data and trace data
```

## Performance Analysis

### Sampling Effectiveness Metrics

Monitor sampling strategy performance:

```python
from provide.foundation.profiling.sampling import SamplingAnalyzer

analyzer = SamplingAnalyzer(sampler)

# Get effectiveness metrics
metrics = analyzer.get_effectiveness_metrics(time_window_hours=24)

print(f"Sample coverage: {metrics.coverage_percentage:.1f}%")
print(f"Overhead: {metrics.overhead_percentage:.3f}%")
print(f"Detection accuracy: {metrics.anomaly_detection_accuracy:.1f}%")
print(f"False positive rate: {metrics.false_positive_rate:.3f}")

# Analyze sampling distribution
distribution = analyzer.get_sampling_distribution()
for operation_type, stats in distribution.items():
    print(f"{operation_type}:")
    print(f"  Samples: {stats.sample_count}")
    print(f"  Rate: {stats.effective_rate:.3f}")
    print(f"  Coverage: {stats.coverage:.1f}%")
```

### Adaptive Tuning

Automatically tune sampling parameters:

```python
from provide.foundation.profiling.sampling import AdaptiveTuner

tuner = AdaptiveTuner(
    sampler=sampler,
    optimization_goals={
        "minimize_overhead": 0.4,      # 40% weight
        "maximize_coverage": 0.3,      # 30% weight
        "maximize_anomaly_detection": 0.3  # 30% weight
    },
    tuning_interval_hours=24,          # Retune daily
    minimum_data_points=1000           # Need 1000 samples before tuning
)

# Tuner automatically adjusts sampler parameters
tuner.start_auto_tuning()

# Manual tuning trigger
tuner.tune_now()

# Get tuning history
history = tuner.get_tuning_history()
for adjustment in history:
    print(f"Adjustment at {adjustment.timestamp}:")
    print(f"  Parameter: {adjustment.parameter}")
    print(f"  Old value: {adjustment.old_value}")
    print(f"  New value: {adjustment.new_value}")
    print(f"  Improvement: {adjustment.improvement_metric:.3f}")
```

## Best Practices

### Production Deployment

1. **Start Conservative**: Begin with low base rates (0.5-1%) and increase gradually
2. **Monitor Overhead**: Track sampling overhead and adjust if it exceeds 0.5%
3. **Use Multiple Strategies**: Combine load-based and pattern-based sampling
4. **Set Safety Limits**: Always configure maximum sampling rates (typically 20-30%)

### Development and Testing

1. **Use High Sampling**: 50-100% sampling for development environments
2. **Test Sampling Logic**: Verify sampling triggers work as expected
3. **Validate Effectiveness**: Ensure sampling captures relevant performance data
4. **Profile Sampling Overhead**: Monitor the cost of sampling itself

### Monitoring and Alerting

1. **Alert on Sampling Rate**: Monitor unexpected sampling rate changes
2. **Track Coverage**: Ensure adequate sample coverage for critical operations
3. **Monitor Effectiveness**: Alert if anomaly detection accuracy drops
4. **Dashboard Sampling Metrics**: Visualize sampling rates and decisions

## Troubleshooting

### Common Issues

**Sampling rate stuck at minimum**
```python
# Check if circuit breaker is open
if sampler.circuit_breaker.is_open():
    print("Circuit breaker is open - check system health")

# Verify triggers are working
triggers = sampler.get_active_triggers()
print(f"Active triggers: {triggers}")
```

**High sampling overhead**
```python
# Reduce maximum sampling rate
sampler.max_rate = 0.10  # Reduce from default

# Increase sampling interval
sampler.update_interval_seconds = 60  # Check less frequently

# Optimize sampling decision logic
sampler.enable_fast_path = True  # Use optimized decision path
```

**Poor anomaly detection**
```python
# Increase sampling for anomalous patterns
sampler.anomaly_multiplier = 20  # Increase from default 10

# Extend trigger duration
sampler.triggers["anomaly_detection"]["duration_minutes"] = 30

# Lower anomaly threshold
sampler.anomaly_threshold = 2.0  # Reduce from default 3.0
```

### Debug Mode

Enable detailed logging for sampling decisions:

```python
import logging
logging.getLogger("provide.foundation.profiling.sampling").setLevel(logging.DEBUG)

# Also enable sampling decision traces
sampler.enable_decision_tracing = True
```