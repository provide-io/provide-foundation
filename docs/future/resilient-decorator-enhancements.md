# Resilient Decorator Enhancements

## Overview

The current `with_error_handling` decorator (candidate for renaming to `@resilient`) is a powerful error handling mechanism but could be enhanced with additional capabilities to make functions truly resilient to various failure modes.

## Current Capabilities

The decorator currently supports:

- **`fallback`** - Return value when errors occur
- **`log_errors`** - Toggle error logging on/off
- **`context_provider`** - Dynamic context function (e.g., get request_id)
- **`context`** - Static context dict for logging
- **`error_mapper`** - Transform exceptions before re-raising
- **`suppress`** - Tuple of exception types to suppress
- **`reraise`** - Whether to re-raise after logging

## Proposed Enhancements

### 1. Retry Logic

Add intelligent retry capabilities with exponential backoff:

```python
@resilient(
    retry_times=3,
    retry_delay=1.0,
    retry_backoff=2.0,  # exponential backoff multiplier
    retryable_exceptions=(TimeoutError, ConnectionError),
    jitter=True  # add randomness to prevent thundering herd
)
def api_call():
    pass
```

**Implementation considerations:**
- Use `asyncio.sleep()` for async functions
- Add jitter to prevent synchronized retries
- Track retry attempts in logging context

### 2. Performance Monitoring

Monitor execution time and detect performance issues:

```python
@resilient(
    measure_time=True,  # Log execution time
    timeout=30.0,  # Max execution time
    slow_threshold=10.0,  # Log warning if slower
    performance_callback=lambda duration: metrics.record(duration)
)
def slow_operation():
    pass
```

**Implementation considerations:**
- Use `time.perf_counter()` for accurate timing
- Integrate with metrics systems
- Support both sync and async timeout handling

### 3. Circuit Breaker Pattern

Prevent cascading failures by temporarily disabling failing functions:

```python
@resilient(
    circuit_breaker=True,
    failure_threshold=5,  # failures before circuit opens
    recovery_timeout=60.0,  # seconds before trying again
    half_open_requests=3  # test requests when recovering
)
def external_service_call():
    pass
```

**Implementation considerations:**
- Track state per function/instance
- Thread-safe state management
- Gradual recovery with half-open state

### 4. Error Aggregation & Batching

Collect and batch errors for analysis:

```python
@resilient(
    aggregate_errors=True,  # Collect multiple errors
    error_limit=10,  # Max errors before stopping
    error_buffer_time=5.0,  # Time window for aggregation
    flush_callback=lambda errors: send_to_monitoring(errors)
)
def batch_processor():
    pass
```

**Implementation considerations:**
- Use background thread for error flushing
- Memory-efficient error storage
- Configurable aggregation strategies

### 5. Notification & Alerting

Alert on error patterns and thresholds:

```python
@resilient(
    alert_on_error=True,
    alert_callback=lambda exc: slack.send_alert(exc),
    alert_threshold=3,  # errors before alerting
    alert_cooldown=300.0,  # seconds between alerts
    escalation_func=lambda count: page_oncall() if count > 10 else None
)
def critical_operation():
    pass
```

**Implementation considerations:**
- Rate limiting for alerts
- Escalation policies
- Integration with monitoring systems

### 6. Enhanced Logging Options

More granular control over logging behavior:

```python
@resilient(
    log_level="warning",  # dynamic log level
    log_success=True,  # log successful executions
    log_args=True,  # include function args in logs
    sanitize_args=lambda args, kwargs: sanitize_sensitive_data(args, kwargs),
    log_result=False,  # include return value
    structured_logging=True  # use structured format
)
def sensitive_operation(user_id, password):
    pass
```

**Implementation considerations:**
- Sensitive data sanitization
- Performance impact of logging args/results
- Structured vs unstructured logging

### 7. Error Recovery & Cleanup

Automatic recovery attempts and guaranteed cleanup:

```python
@resilient(
    recovery_func=lambda exc: fallback_service.call(),
    cleanup_func=lambda: close_connections(),
    recovery_exceptions=(ServiceUnavailableError,),
    always_cleanup=True  # cleanup even on success
)
def service_operation():
    pass
```

**Implementation considerations:**
- Exception handling in recovery/cleanup functions
- Resource management patterns
- Context managers integration

### 8. Failure Caching

Cache failure patterns to avoid repeated failures:

```python
@resilient(
    cache_errors=True,  # Cache which calls fail
    cache_ttl=300.0,  # How long to remember failures
    skip_if_cached_failure=True,  # Don't retry known failures
    cache_key_func=lambda args, kwargs: f"{args[0]}-{kwargs.get('id')}"
)
def expensive_operation(resource_id):
    pass
```

**Implementation considerations:**
- Memory-efficient caching
- Cache invalidation strategies
- Distributed cache support

### 9. Rate Limiting

Prevent overwhelming downstream services:

```python
@resilient(
    rate_limit=100,  # Max calls per period
    rate_period=60.0,  # Period in seconds
    rate_limit_fallback="cached_result",
    rate_limit_strategy="sliding_window"  # or "token_bucket"
)
def api_heavy_operation():
    pass
```

**Implementation considerations:**
- Multiple rate limiting algorithms
- Distributed rate limiting
- Graceful degradation

### 10. Telemetry & Metrics

Comprehensive observability:

```python
@resilient(
    emit_metrics=True,
    metric_name="service.api.call",
    metric_tags={"service": "auth", "endpoint": "login"},
    track_error_types=True,  # Track distribution of error types
    custom_metrics=lambda result, duration: {
        "response_size": len(result),
        "processing_time": duration
    }
)
def instrumented_operation():
    pass
```

**Implementation considerations:**
- Integration with metrics backends (Prometheus, StatsD)
- Low-overhead metrics collection
- Custom metric extraction

### 11. Conditional Handling

Apply error handling based on conditions:

```python
@resilient(
    when=lambda: is_production(),  # Only handle errors in production
    ignore_when=lambda exc: isinstance(exc, ExpectedError),
    condition_callback=lambda: get_feature_flag("error_handling"),
    environment_aware=True
)
def conditional_operation():
    pass
```

**Implementation considerations:**
- Dynamic condition evaluation
- Feature flag integration
- Environment-specific behavior

### 12. Advanced Stack Trace Control

Fine-grained control over error reporting:

```python
@resilient(
    include_traceback=True,
    traceback_limit=10,  # Limit traceback depth
    hide_internal_frames=True,  # Hide framework frames
    source_context=3,  # Lines of source code around error
    local_variables=True  # Include local variables (debug only)
)
def debuggable_operation():
    pass
```

**Implementation considerations:**
- Security implications of variable logging
- Performance impact of stack inspection
- Development vs production behavior

## Naming Rationale: `@resilient`

The name `@resilient` is recommended because:

1. **Comprehensive** - Covers all aspects: retry, recover, fallback, circuit break
2. **Industry Standard** - Common term in reliability engineering
3. **Concise** - Short and memorable
4. **Semantic** - Implies the function becomes resilient to failures
5. **Scalable** - Works for simple and complex use cases

### Alternative Names Considered:

- `@safeguard` - Good but implies protection rather than adaptation
- `@fortify` - Strong but more static feeling
- `@error_shield` - Clear but longer and less elegant
- `@robust` - Simple but less specific

## Implementation Strategy

### Phase 1: Core Enhancements
- Retry logic with exponential backoff
- Performance monitoring (timeout, timing)
- Enhanced logging options

### Phase 2: Resilience Patterns
- Circuit breaker implementation
- Error recovery mechanisms
- Failure caching

### Phase 3: Observability
- Comprehensive metrics integration
- Advanced alerting
- Telemetry collection

### Phase 4: Advanced Features
- Rate limiting
- Conditional handling
- Error aggregation

## Backward Compatibility

- Maintain current parameter names as aliases
- Provide migration guide from `with_error_handling` to `@resilient`
- Support both decorators during transition period
- Clear deprecation timeline

## Configuration Management

```python
# Global defaults
resilient.configure(
    default_log_level="error",
    metrics_backend="prometheus",
    alerting_enabled=True,
    circuit_breaker_enabled=False
)

# Per-environment overrides
@resilient.with_profile("production")
def production_operation():
    pass
```

## Integration Points

- **Metrics**: Prometheus, StatsD, CloudWatch
- **Logging**: Structlog, standard logging
- **Monitoring**: Sentry, Datadog, New Relic
- **Alerting**: Slack, PagerDuty, email
- **Caching**: Redis, Memcached, in-memory

## Example: Full-Featured Usage

```python
@resilient(
    # Basic error handling
    fallback=None,
    suppress=(TimeoutError,),

    # Retry logic
    retry_times=3,
    retry_delay=1.0,
    retry_backoff=2.0,

    # Performance monitoring
    timeout=30.0,
    slow_threshold=10.0,

    # Circuit breaker
    circuit_breaker=True,
    failure_threshold=5,

    # Observability
    emit_metrics=True,
    metric_name="api.user.login",
    log_success=True,

    # Recovery
    cleanup_func=lambda: cleanup_resources(),

    # Alerting
    alert_on_error=True,
    alert_threshold=2
)
async def user_login_api(username: str, password: str):
    """Comprehensive resilient API endpoint."""
    return await auth_service.authenticate(username, password)
```

This would transform a simple function into a production-ready, observable, and resilient operation with minimal code changes.