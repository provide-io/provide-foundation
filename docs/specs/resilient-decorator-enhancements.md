# Spec: Resilient Decorator Enhancements

This document outlines planned enhancements for the `@resilient` decorator.

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

### 2. Circuit Breaker Pattern

Prevent cascading failures by temporarily disabling failing functions.

```python
@resilient(
    circuit_breaker=True,
    failure_threshold=5,
    recovery_timeout=60.0,
)
def external_service_call():
    pass
```

### 3. Rate Limiting

Prevent overwhelming downstream services.

```python
@resilient(
    rate_limit=100,
    rate_period=60.0,
)
def api_heavy_operation():
    pass
```
