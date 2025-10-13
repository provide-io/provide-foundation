# Spec: Resilient Decorator Enhancements

This document outlines planned enhancements for the `@resilient` decorator (formerly `with_error_handling`).

## Overview

The goal is to evolve the decorator into a comprehensive tool for building fault-tolerant functions, incorporating patterns like retry, circuit breaking, and performance monitoring.

## Proposed Enhancements

### 1. Retry Logic

Add intelligent retry capabilities with exponential backoff.

```python
@resilient(
    retry_times=3,
    retry_delay=1.0,
    retry_backoff=2.0,
    retryable_exceptions=(TimeoutError, ConnectionError),
    jitter=True
)
def api_call():
    pass
```

### 2. Performance Monitoring

Monitor execution time and detect performance issues.

```python
@resilient(
    measure_time=True,
    timeout=30.0,
    slow_threshold=10.0,
    performance_callback=lambda duration: metrics.record(duration)
)
def slow_operation():
    pass
```

### 3. Circuit Breaker Pattern

Prevent cascading failures by temporarily disabling failing functions.

```python
@resilient(
    circuit_breaker=True,
    failure_threshold=5,
    recovery_timeout=60.0,
    half_open_requests=3
)
def external_service_call():
    pass
```

### 4. Rate Limiting

Prevent overwhelming downstream services.

```python
@resilient(
    rate_limit=100,
    rate_period=60.0,
    rate_limit_strategy="sliding_window"
)
def api_heavy_operation():
    pass
```

## Example: Full-Featured Usage

```python
@resilient(
    # Basic error handling
    fallback=None,
    suppress=(TimeoutError,),

    # Retry logic
    retry_times=3,
    retry_delay=1.0,

    # Performance monitoring
    timeout=30.0,
    slow_threshold=10.0,

    # Circuit breaker
    circuit_breaker=True,
    failure_threshold=5,

    # Observability
    emit_metrics=True,
    metric_name="api.user.login"
)
async def user_login_api(username: str, password: str):
    """A production-ready, observable, and resilient operation."""
    return await auth_service.authenticate(username, password)
```
