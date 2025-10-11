# Dogfooding Improvements for provide.foundation

This document tracks where provide.foundation should use its own robust features instead of external libraries or ad-hoc implementations.

## ✅ Completed Improvements

### 1. CLI Helpers: Replaced Ad-Hoc Parsing with Parsers Module
**Status**: ✅ Completed
**Files Changed**: `src/provide/foundation/cli/helpers.py`

- **Before**: Manual type detection (`value.isdigit()`, `value.lower() == "true"`)
- **After**: Uses `parse_typed_value()` from parsers module
- **Impact**: Consistent parsing behavior across the entire library
- **Benefits**:
  - Reduced code duplication
  - Better error messages
  - Standardized type conversion logic

### 2. Discovery: Added @resilient Decorator for Error Handling
**Status**: ✅ Completed
**Files Changed**: `src/provide/foundation/hub/discovery.py`

- **Before**: Manual try/except blocks with `print()` to stderr
- **After**: Uses `@resilient` decorator with `log_errors=False` (avoids circular dependencies)
- **Impact**: Standardized error handling and suppression
- **Benefits**:
  - Consistent error logging context (function, module)
  - Configurable error behavior
  - Reduced boilerplate

### 3. OpenObserve Client: Added @resilient Decorator to test_connection()
**Status**: ✅ Completed
**Files Changed**: `src/provide/foundation/integrations/openobserve/client.py`

- **Before**: Manual try/except with direct log.error()
- **After**: Uses `@resilient` decorator with context and suppression
- **Impact**: Standardized connection testing
- **Benefits**:
  - Automatic error logging with context
  - Returns fallback value (False) instead of raising

### 4. Coordinator: Uses utils/environment Helpers
**Status**: ✅ Completed
**Files Changed**: `src/provide/foundation/logger/setup/coordinator.py`

- **Before**: Direct `os.environ.get()` calls
- **After**: Uses `get_str()` from `utils/environment/getters`
- **Impact**: More consistent environment variable access
- **Note**: Limited to `get_str()` to avoid circular dependencies (other getters use the logger)

## 🚨 Critical Priority: OpenObserve Integration Should Use Foundation Transport

**Status**: ⚠️ BLOCKED - Breaking Change Required
**Priority**: CRITICAL
**Effort**: Large (3-5 days)
**Impact**: Breaking change - requires async refactor

### The Problem

The OpenObserve integration currently uses the external `requests` library (synchronous HTTP) instead of Foundation's own sophisticated transport system:

**Current State**:
```python
# src/provide/foundation/integrations/openobserve/client.py
import requests
from requests.adapters import HTTPAdapter

class OpenObserveClient:
    def __init__(self, ...):
        self.session = requests.Session()
        # Manual retry configuration
        retry = Retry(total=max_retries, ...)
```

**Should Be**:
```python
# Using Foundation's transport with built-in features
from provide.foundation.transport import UniversalClient, post

class OpenObserveClient:
    async def __init__(self, ...):
        self._client = UniversalClient()
        # Automatic retry via middleware
        # Automatic logging via middleware
        # Automatic metrics via middleware
```

### Why This is Critical

Foundation provides a complete, battle-tested HTTP transport system with:

1. **`UniversalClient`** - Async client with middleware pipeline
2. **`HTTPTransport`** - httpx-based backend with HTTP/2 support
3. **Built-in middleware**:
   - `RetryMiddleware` - Configurable retry logic
   - `LoggingMiddleware` - Automatic request/response logging
   - `MetricsMiddleware` - Performance tracking
4. **Proper error handling** - Typed transport exceptions
5. **Connection pooling** - Performance optimizations
6. **Security features** - URI sanitization, secret masking

### Affected Files

- `src/provide/foundation/integrations/openobserve/client.py` - Main client
- `src/provide/foundation/integrations/openobserve/streaming.py` - Log streaming
- `src/provide/foundation/integrations/openobserve/otlp.py` - OTLP bulk API (line 242)

### Migration Requirements

**Breaking Changes**:
1. All OpenObserve client methods must become `async`
2. All call sites must use `async`/`await`
3. Existing sync code using OpenObserveClient will break

**Benefits After Migration**:
- Automatic telemetry for all HTTP requests
- Built-in retry and error handling
- Better performance (async I/O, connection pooling)
- HTTP/2 support
- Consistent logging across all HTTP operations
- Simplified client code (no manual retry setup)

### Recommended Approach

1. **Phase 1**: Create async version alongside existing client
   - `OpenObserveAsyncClient` using Foundation transport
   - Deprecate `OpenObserveClient`

2. **Phase 2**: Update internal uses to async version
   - Update CLI commands
   - Update integrations

3. **Phase 3**: Remove deprecated sync client
   - Breaking change release
   - Migration guide

### Decision Points

Before starting this work:

- [ ] Confirm breaking change is acceptable
- [ ] Plan migration strategy for existing users
- [ ] Document async migration guide
- [ ] Update all examples and documentation
- [ ] Consider providing sync wrapper (run_sync helper)

## 📊 Summary

| Category | Status | Files Modified | Tests Passing |
|----------|--------|----------------|---------------|
| CLI Helpers | ✅ Complete | 1 | ✅ 18 tests |
| Discovery Error Handling | ✅ Complete | 1 | ✅ 4 tests |
| OpenObserve @resilient | ✅ Complete | 1 | ✅ 123 tests |
| Coordinator Environment | ✅ Complete | 1 | ✅ 27 tests |
| **OpenObserve Transport** | ⚠️ Pending | 3 | N/A (not started) |

## Next Steps

1. **Immediate**: Get approval for breaking change in OpenObserve integration
2. **Planning**: Design async migration strategy
3. **Implementation**: Create `OpenObserveAsyncClient` using Foundation transport
4. **Documentation**: Write migration guide for users
5. **Testing**: Comprehensive async integration tests
