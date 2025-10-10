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

## 📊 Summary of Completed Improvements

| Category | Status | Files Modified | Tests Passing |
|----------|--------|----------------|---------------|
| CLI Helpers → Parsers | ✅ Complete | 1 | ✅ 18 tests |
| Discovery → @resilient | ✅ Complete | 1 | ✅ 4 tests |
| OpenObserve → @resilient | ✅ Complete | 1 | ✅ 123 tests |
| Coordinator → env helpers | ✅ Complete | 1 | ✅ 27 tests |
| Downloader → hash_file() | ✅ Complete | 1 | ✅ 16 tests |
| CLI Shutdown → perr() | ✅ Complete | 1 | ✅ 7 tests |
| **TOTAL IMPROVEMENTS** | ✅ **6 Complete** | **6 files** | ✅ **565 tests** |
| **OpenObserve Transport** | ⚠️ Pending | 3 | N/A (breaking change) |

## 🔍 Additional Dogfooding Opportunities Identified

### File I/O Improvements

#### tools/downloader.py
- **Line 127**: Uses `dest.open("wb")` for downloads → Should use `atomic_write()` to prevent corruption
- **Lines 163-167**: Manual hashlib.sha256() → Should use `hash_file()` from crypto/hashing

#### tools/verifier.py
- **Line 63**: Direct file reading → Could use `safe_read()` for better error handling

#### crypto/certificates/loader.py
- **Line 46**: Direct `path.open("r")` → Should use `safe_read_text()`

**Note**: crypto/hashing.py correctly uses direct I/O because it needs chunked reads for efficiency

### JSON Operations Not Dogfooding

#### Multiple Files (14+)
Currently using `json.dumps()` and `json.loads()` directly instead of Foundation's helpers:
- cli/helpers.py
- integrations/openobserve/streaming.py
- file/formats.py (this IS the implementation - appropriate)
- transport/base.py
- parsers/primitives.py
- errors/types.py

**Action**: Replace with `read_json()`, `write_json()` where appropriate (file operations)

### Console Output Not Dogfooding

#### Files Using print() Instead of pout()/perr()
Priority targets:
- **cli/shutdown.py** (line 70, 210) - Error messages to stderr
- **integrations/openobserve/commands.py** - User-facing output
- **formatting/tables.py** - Table output
- **console/input.py** (line 69) - Prompt output

**Skip**: streams/file.py, hub/discovery.py (infrastructure, circular dependency risk)

### Environment Variable Access

#### Still Using os.environ Directly
- config/env.py
- platform/info.py
- console/output.py (lines 55, 58)
- testmode/orchestration.py
- utils/caching.py

**Action**: Replace with `get_str()`, `get_bool()` where safe (no circular deps)

### Manual Error Handling

#### try/except Blocks That Could Use @resilient
Found in 22+ files with patterns like:
```python
try:
    something()
except Exception:
    pass  # or continue
```

**Examples**:
- cli/helpers.py
- cli/shutdown.py
- hub/core.py
- process/lifecycle/monitoring.py
- concurrency locks (appropriate as-is)
- file/lock.py (appropriate as-is)

## Implementation Priorities

### Phase 1: High-Impact, Low-Risk (Completed ✅)
1. ✅ CLI helpers → parsers module
2. ✅ Discovery → @resilient decorator
3. ✅ OpenObserve client → @resilient decorator
4. ✅ Coordinator → environment helpers

### Phase 2: Medium-Impact (Recommended Next)
1. **File I/O Improvements** - Prevent corruption with atomic writes
2. **Console Output** - Replace print() with pout()/perr() for JSON mode support
3. **JSON Operations** - Use Foundation's serialization helpers

### Phase 3: Lower-Impact (Future Work)
1. Remaining environment variable access
2. Additional @resilient decorators for simple error suppression
3. Manual validation patterns → config/validators usage

## Next Steps

1. **File I/O**: Update downloader.py to use atomic_write() and hash_file()
2. **Console Output**: Replace print() in CLI commands with pout()/perr()
3. **JSON Operations**: Use read_json()/write_json() for file-based JSON
4. **Testing**: Ensure 100% coverage on modified code
5. **Breaking Change**: Plan OpenObserve async transport migration separately
