# Dogfooding Next Steps

## Completed Work ✅

### 1. Eliminated format_duration() Duplication
- **File**: `src/provide/foundation/cli/helpers.py`
- **Change**: Replaced custom `format_duration()` with import from `formatting.numbers`
- **Tests**: All 115 CLI tests passing
- **Benefit**: Single source of truth for duration formatting

## In Progress 🚧

### 2. Logger Auto-Sanitization Processor
- **Created**: `src/provide/foundation/logger/processors/sanitization.py`
- **Status**: Processor created but not yet integrated into pipeline
- **Next Steps**:
  1. Add configuration fields to `LoggingConfig`:
     - `sanitization_enabled: bool = True`
     - `sanitization_mask_patterns: bool = True`
     - `sanitization_sanitize_dicts: bool = True`
  2. Add sanitization processor to `_build_core_processors_list()` in `logger/processors/main.py`
  3. Position it early in pipeline (after contextvars, before enrichment)
  4. Add tests for sanitization processor
  5. Update documentation

## Remaining High-Value Work 📋

### 3. Integrate timed_block() for Performance Monitoring
**Files to Update**:
- `src/provide/foundation/hub/initialization.py` - Time Hub init
- `src/provide/foundation/config/loader.py` - Time config loading
- `src/provide/foundation/logger/setup/coordinator.py` - Time logger setup

**Pattern**:
```python
from provide.foundation.utils.timing import timed_block

with timed_block("Hub initialization"):
    # initialization code
```

**Benefit**: Automatic performance logging for critical operations

### 4. Replace json Operations with provide_dumps/loads
**Files to Update** (~20 files):
- `src/provide/foundation/config/loader.py` (line 127)
- `src/provide/foundation/cli/helpers.py` (lines 138, 143)
- `src/provide/foundation/parsers/primitives.py`
- `src/provide/foundation/transport/base.py`
- Others using `json.dumps()/loads()` for string serialization

**Pattern**:
```python
# Before
import json
data = json.dumps(config)

# After
from provide.foundation.serialization import provide_dumps
data = provide_dumps(config)
```

**Benefit**: Consistent serialization with tracking

### 5. Implement ContextScopedCache for Config Resolution
**Files to Update**:
- `src/provide/foundation/config/loader.py` - Cache during resolution
- `src/provide/foundation/hub/components.py` - Cache during discovery

**Pattern**:
```python
from provide.foundation.utils.scoped_cache import ContextScopedCache

with ContextScopedCache.scope("config_resolution") as cache:
    # Resolution code that caches intermediate results
    if cache.get("parsed_config") is None:
        config = parse_config()
        cache.set("parsed_config", config)
```

**Benefit**: Prevent redundant parsing/resolution

## Updated DOGFOODING.md Entry

Add to the "Completed Improvements" section:

```markdown
### 9. CLI Format Duration: Uses formatting Module
**Status**: ✅ Completed
**Files Changed**: `src/provide/foundation/cli/helpers.py`

- **Before**: Custom `format_duration()` implementation
- **After**: Delegates to `formatting.numbers.format_duration()`
- **Impact**: Eliminated code duplication
- **Benefits**:
  - Single source of truth for formatting
  - Consistent behavior across framework
  - Maintains CLI-specific spacing for readability

### 10. Logger Sanitization Processor: Auto-Masks Secrets
**Status**: 🚧 In Progress
**Files**: `src/provide/foundation/logger/processors/sanitization.py` (created)

- **What**: Processor that automatically sanitizes all logged data
- **Uses**: Foundation's own `mask_secrets()` and `sanitize_dict()`
- **Impact**: Security-by-default for all log messages
- **Next**: Integration into logger pipeline with configuration
```

## Summary

**Phase 1 Complete**: ✅ Eliminated duplication (1 improvement)
**Phase 2 In Progress**: 🚧 Security hardening (processor created, needs integration)
**Phases 3-5 Remaining**: Performance, consistency, and caching improvements

**Test Status**: All 115 CLI tests passing, codebase stable

**Recommendation**: Continue with Phase 2 completion (logger sanitization) before moving to Phases 3-5.
