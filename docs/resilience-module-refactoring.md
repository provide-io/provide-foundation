# Resilience Module Refactoring

## Overview
Refactor retry, circuit breaker, and fallback patterns from the `errors` module into a dedicated `resilience` module. This aligns with industry standards (Polly, Hystrix, resilience4j) where these patterns are treated as resilience strategies rather than error handling.

## Motivation
- **Semantic Correctness**: Retry, circuit breaker, and fallback are resilience patterns, not error types
- **Industry Alignment**: Matches patterns from Polly (.NET), Hystrix (Java), resilience4j
- **Clean Separation**: Errors define what went wrong; resilience defines how to recover
- **Code Reuse**: Eliminate duplication between `RetryPolicy` and `RetryMiddleware`

## Implementation Checklist

### Phase 1: Test Creation (TDD)
- [ ] Create `tests/resilience/` directory
- [ ] Create `tests/resilience/test_retry_executor.py`
  - [ ] Test sync execution with various retry scenarios
  - [ ] Test async execution with various retry scenarios
  - [ ] Test integration with RetryPolicy
  - [ ] Test all backoff strategies (fixed, linear, exponential, fibonacci)
  - [ ] Test jitter application
  - [ ] Test retry callbacks
  - [ ] Test exception filtering
  - [ ] Test logging behavior
- [ ] Create `tests/resilience/test_retry_policy.py`
  - [ ] Test policy configuration
  - [ ] Test delay calculation for all strategies
  - [ ] Test should_retry logic
  - [ ] Test max_attempts enforcement
  - [ ] Test retryable_errors filtering
- [ ] Create `tests/resilience/test_retry_decorator.py`
  - [ ] Test @retry decorator with sync functions
  - [ ] Test @retry decorator with async functions
  - [ ] Test decorator with RetryPolicy
  - [ ] Test decorator with inline parameters
- [ ] Create `tests/resilience/test_circuit_breaker.py`
  - [ ] Test circuit breaker state transitions (closed -> open -> half-open)
  - [ ] Test failure threshold triggering
  - [ ] Test timeout behavior
  - [ ] Test success reset
- [ ] Create `tests/resilience/test_fallback.py`
  - [ ] Test fallback chain execution
  - [ ] Test fallback with retry
  - [ ] Test fallback with circuit breaker
- [ ] Create `tests/resilience/test_integration.py`
  - [ ] Test retry + circuit breaker combination
  - [ ] Test retry + fallback combination
  - [ ] Test middleware integration

### Phase 2: Module Implementation
- [ ] Create `src/provide/foundation/resilience/__init__.py`
- [ ] Create `src/provide/foundation/resilience/retry.py`
  - [ ] Implement `RetryPolicy` class (moved from errors/types.py)
  - [ ] Implement `RetryExecutor` class
  - [ ] Implement `BackoffStrategy` enum
- [ ] Create `src/provide/foundation/resilience/decorators.py`
  - [ ] Implement `@retry` decorator (replaces @retry_on_error)
  - [ ] Implement `@circuit_breaker` decorator
  - [ ] Implement `@fallback` decorator
- [ ] Create `src/provide/foundation/resilience/circuit.py`
  - [ ] Implement `CircuitBreaker` class
  - [ ] Implement `CircuitState` enum
  - [ ] Implement state transition logic
- [ ] Create `src/provide/foundation/resilience/fallback.py`
  - [ ] Implement `FallbackChain` class
  - [ ] Implement fallback strategies

### Phase 3: Migration
- [ ] Update `src/provide/foundation/transport/middleware.py`
  - [ ] Import RetryPolicy from resilience module
  - [ ] Update RetryMiddleware to use RetryExecutor
  - [ ] Remove duplicate retry logic
- [ ] Update `src/provide/foundation/errors/types.py`
  - [ ] Remove RetryPolicy (moved to resilience)
  - [ ] Add deprecation warning and re-export for compatibility
- [ ] Update `src/provide/foundation/errors/decorators.py`
  - [ ] Remove @retry_on_error implementation
  - [ ] Add deprecation warning and re-export for compatibility
- [ ] Move circuit breaker from errors to resilience
  - [ ] Move @circuit_breaker decorator
  - [ ] Update imports

### Phase 4: Update Dependencies
- [ ] Find all imports of `RetryPolicy`
- [ ] Find all imports of `@retry_on_error`
- [ ] Find all imports of `@circuit_breaker`
- [ ] Update imports to use resilience module
- [ ] Maintain backward compatibility exports

### Phase 5: Testing & Validation
- [ ] Run all existing tests to ensure compatibility
- [ ] Run new resilience tests
- [ ] Verify middleware behavior unchanged
- [ ] Verify decorator behavior unchanged
- [ ] Check test coverage (target: 100%)

## API Design

### RetryExecutor
```python
class RetryExecutor:
    def __init__(self, policy: RetryPolicy):
        self.policy = policy
    
    async def execute_async(self, func, *args, **kwargs):
        """Execute async function with retry logic."""
        
    def execute_sync(self, func, *args, **kwargs):
        """Execute sync function with retry logic."""
```

### Unified RetryPolicy
```python
@attrs.define
class RetryPolicy:
    max_attempts: int = 3
    backoff: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    base_delay: float = 1.0
    max_delay: float = 60.0
    jitter: bool = True
    retryable_errors: tuple[type[Exception], ...] | None = None
    retryable_status_codes: set[int] | None = None  # For HTTP
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt."""
    
    def should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if should retry."""
    
    def should_retry_response(self, response: Any, attempt: int) -> bool:
        """Check if HTTP response should be retried."""
```

### Updated RetryMiddleware
```python
@attrs.define
class RetryMiddleware(Middleware):
    policy: RetryPolicy = attrs.field(
        factory=lambda: RetryPolicy(
            max_attempts=3,
            base_delay=0.5,
            retryable_status_codes={500, 502, 503, 504}
        )
    )
    
    async def execute_with_retry(self, execute_func, request):
        executor = RetryExecutor(self.policy)
        
        async def wrapped():
            response = await execute_func(request)
            if self.policy.should_retry_response(response, attempt=1):
                raise TransportError(f"Retryable status: {response.status}")
            return response
        
        return await executor.execute_async(wrapped)
```

## Migration Path

### Backward Compatibility
During migration, maintain backward compatibility by re-exporting from errors module:

```python
# src/provide/foundation/errors/types.py
from provide.foundation.resilience.retry import RetryPolicy
import warnings

def __getattr__(name):
    if name == "RetryPolicy":
        warnings.warn(
            "Importing RetryPolicy from errors.types is deprecated. "
            "Use provide.foundation.resilience.retry instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return RetryPolicy
    raise AttributeError(f"module {__name__} has no attribute {name}")
```

## Success Criteria
1. All existing tests pass without modification
2. New resilience tests achieve 100% coverage
3. No duplicate retry logic between decorator and middleware
4. Clean separation between error definition and resilience patterns
5. Performance unchanged or improved
6. Clear migration path with deprecation warnings

## Timeline
- Phase 1 (Tests): 2 hours
- Phase 2 (Implementation): 3 hours
- Phase 3 (Migration): 1 hour
- Phase 4 (Updates): 1 hour
- Phase 5 (Validation): 1 hour

Total: ~8 hours of focused work

## References
- [Polly Resilience Framework](https://github.com/App-vNext/Polly)
- [Hystrix Circuit Breaker](https://github.com/Netflix/Hystrix)
- [resilience4j](https://resilience4j.readme.io/)
- [tenacity Python library](https://github.com/jd/tenacity)