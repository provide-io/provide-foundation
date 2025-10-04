# Code Cleanup & Release Preparation - Next Steps

## Session Summary (2025-10-03)

### ✅ Completed: Performance Caching Improvements

**Files Modified (6 source + 3 test files):**

1. **src/provide/foundation/formatting/text.py**
   - Moved ANSI regex to module constant `ANSI_PATTERN`
   - Performance: 1.3x faster, scales with iterations

2. **src/provide/foundation/cli/commands/logs/tail.py**
   - Moved key-value pattern to module constant `KEY_VALUE_PATTERN`

3. **src/provide/foundation/tools/resolver.py**
   - Added `__init__` with `_pattern_cache` dictionary
   - Caches compiled regex patterns for version matching

4. **src/provide/foundation/platform/detection.py**
   - Added `@cached()` to: `get_os_name()`, `get_arch_name()`, `get_platform_string()`, `get_os_version()`, `get_cpu_type()`
   - Performance: 9.2x faster after first call

5. **src/provide/foundation/platform/info.py**
   - Added `@cached()` to: `get_system_info()`, `is_windows()`, `is_macos()`, `is_linux()`, `is_arm()`, `is_64bit()`

6. **src/provide/foundation/console/output.py**
   - Added `_get_color_env_settings()` with `@cached()` for environment variable lookups
   - Performance: 10-20x faster for repeated checks

**Test Files Updated:**
- tests/platform/test_platform_detection.py
- tests/platform/test_platform_info.py
- tests/platform/test_platform_coverage.py
- Added `setup_method()` to clear caches + inline `cache_clear()` between assertions

**Results:**
- ✅ 205/205 tests passing
- ✅ 81.55% code coverage (exceeds 80% requirement)
- ✅ No regressions
- ✅ Benchmarks validated: >14K msg/sec, parser caching at 987K ops/sec

### ✅ Started: Legacy Code Removal

**Completed:**
- ✅ Removed `generate_key_pair()` from `src/provide/foundation/crypto/keys.py` (lines 177-185)
- ✅ Removed import from `src/provide/foundation/crypto/__init__.py` (line 80)
- ✅ Removed stub from `src/provide/foundation/crypto/__init__.py` (lines 166-168)
- ✅ Removed export from `src/provide/foundation/crypto/__init__.py` (lines 255-256)

---

## 🔄 REMAINING WORK - Priority Order

### Priority 1: CRITICAL - Remove Remaining Legacy Code

#### 1.1 EventSets Legacy Aliases
**File:** `src/provide/foundation/eventsets/sets/das.py`
**Lines:** 126-128
**Action:** Remove these legacy aliases:
```python
# Legacy aliases (REMOVE THESE)
das_event_set = DASEventSet()
default_event_set = das_event_set
```

#### 1.2 Logger Legacy Comment
**File:** `src/provide/foundation/logger/core.py`
**Line:** 327
**Action:** Remove backward compatibility comment:
```python
# Backward compatibility: provide global logger object with lazy access
# (REMOVE THIS COMMENT)
```

#### 1.3 Context Legacy Alias
**File:** `src/provide/foundation/context/__init__.py`
**Line:** ~15
**Action:** Find and remove `Context` legacy alias export
**Search for:** `Context.*Legacy alias`

#### 1.4 CLI Decorators Legacy Function
**File:** `src/provide/foundation/cli/decorators.py`
**Line:** 135+
**Action:** Remove `all_options()` decorator (described as "legacy all-in-one option handling")
**Alternative:** Check if it's used anywhere first with: `grep -r "all_options" tests/ src/`

#### 1.5 File Lock Backward Compatibility
**File:** `src/provide/foundation/file/lock.py`
**Line:** ~202
**Action:** Remove backward compatibility code for old lock files
**Search for:** `backward compatibility with old lock files`

#### 1.6 TestMode Legacy State
**File:** `src/provide/foundation/testmode/orchestration.py`
**Line:** ~311
**Action:** Remove legacy state handling code
**Search for:** `Legacy state not available`

---

### Priority 2: HIGH - NotImplementedError Stubs

#### 2.1 OpenObserve HTTP API
**File:** `src/provide/foundation/integrations/openobserve/__init__.py`
**Line:** 66
**Current:**
```python
raise NotImplementedError("HTTP API ingestion not yet implemented")
```
**Decision needed:** Either implement HTTP API ingestion OR remove the stub entirely
**Recommended:** Remove stub if not planned for immediate release

#### 2.2 Transport Streaming
**File:** `src/provide/foundation/transport/base.py`
**Line:** 154
**Current:**
```python
raise NotImplementedError(f"{self.__class__.__name__} does not support streaming")
```
**Action:** Change to proper error or document as intentional limitation

---

### Priority 3: HIGH - Move Inline Defaults to Config

#### 3.1 Add Constants to config/defaults.py

**Add these constants:**
```python
# Bulkhead defaults
DEFAULT_BULKHEAD_MAX_CONCURRENT = 10
DEFAULT_BULKHEAD_MAX_QUEUE_SIZE = 100
DEFAULT_BULKHEAD_TIMEOUT = 30.0

# EventSet defaults
DEFAULT_EVENT_KEY = "default"

# Component defaults
DEFAULT_COMPONENT_DIMENSION = "component"

# State config defaults
DEFAULT_STATE_CONFIG_NAME = ""

# File operation defaults
DEFAULT_FILE_OP_IS_ATOMIC = False
DEFAULT_FILE_OP_IS_SAFE = True
DEFAULT_FILE_OP_HAS_BACKUP = False
```

#### 3.2 Update Files to Use Defaults

**File:** `src/provide/foundation/resilience/bulkhead.py`
**Lines:** 27-29
**Change:**
```python
# FROM:
max_concurrent: int = field(default=10)
max_queue_size: int = field(default=100)
timeout: float = field(default=30.0)

# TO:
max_concurrent: int = field(default_factory=lambda: DEFAULT_BULKHEAD_MAX_CONCURRENT)
max_queue_size: int = field(default_factory=lambda: DEFAULT_BULKHEAD_MAX_QUEUE_SIZE)
timeout: float = field(default_factory=lambda: DEFAULT_BULKHEAD_TIMEOUT)
```
**Don't forget:** `from provide.foundation.config.defaults import ...`

**File:** `src/provide/foundation/eventsets/types.py`
**Line:** 28
**Change:** `default_key: str = field(default="default")` → use `DEFAULT_EVENT_KEY`

**File:** `src/provide/foundation/hub/components.py`
**Line:** 51
**Change:** `dimension: str = field(default="component")` → use `DEFAULT_COMPONENT_DIMENSION`

**File:** `src/provide/foundation/state/config.py`
**Line:** 26
**Change:** `config_name: str = field(default="")` → use `DEFAULT_STATE_CONFIG_NAME`

**File:** `src/provide/foundation/file/operations/types.py`
**Lines:** 105-107
**Change:** Use `DEFAULT_FILE_OP_*` constants

---

### Priority 4: Code Quality Fixes

#### 4.1 Ruff Issues (3 total)

**Run:** `PYTHONPATH=src .venv/bin/ruff check --fix --unsafe-fixes src/provide/foundation/`

**Known Issues:**
1. `crypto/certificates/generator.py:126` - Duplicate imports (ec, rsa appear on lines 121 AND 126)
2. `file/operations/detectors/batch.py:102` - Unused variable `operation_type`

#### 4.2 MyPy Type Errors (~30 total)

**Run:** `PYTHONPATH=src .venv/bin/mypy src/provide/foundation/`

**Common patterns to fix:**
- Overloaded function signatures in decorators
- Incompatible types in resilience/metrics/tracer modules
- Missing type stubs for third-party dependencies
- Signature mismatches in context/core.py

**Systematic approach:**
1. Fix by module (resilience → metrics → tracer → context)
2. Add missing `-> None` return types
3. Add proper `TypeVar` constraints
4. Update `Any` to specific types where possible

---

## Execution Commands

### Code Quality Check
```bash
# Activate environment
source .venv/bin/activate

# Run ruff
PYTHONPATH=src .venv/bin/ruff check --fix --unsafe-fixes src/provide/foundation/
PYTHONPATH=src .venv/bin/ruff format src/provide/foundation/

# Run mypy (incremental fixes)
PYTHONPATH=src .venv/bin/mypy src/provide/foundation/ | head -50
```

### Testing
```bash
# Quick test of modified areas
PYTHONPATH=src timeout 120 .venv/bin/pytest tests/crypto/ tests/eventsets/ tests/context/ -q

# Full test suite
PYTHONPATH=src timeout 300 .venv/bin/pytest -n auto -q --tb=line

# Coverage check (must be >80%)
PYTHONPATH=src timeout 300 .venv/bin/pytest --cov=src/provide/foundation --cov-report=term-missing
```

### Verification Searches
```bash
# Check for remaining legacy code
grep -r "Legacy" src/provide/foundation/ --include="*.py"
grep -r "backward compatibility" src/provide/foundation/ --include="*.py" -i
grep -r "Backward compatibility" src/provide/foundation/ --include="*.py"

# Check for NotImplementedError
grep -r "NotImplementedError" src/provide/foundation/ --include="*.py"

# Check for inline defaults (field with default=)
grep -r 'field(default=' src/provide/foundation/ --include="*.py" | grep -v "default_factory" | head -20

# Verify no TODOs/FIXMEs/HACKs
grep -r "TODO\|FIXME\|HACK\|XXX" src/provide/foundation/ --include="*.py"
```

---

## Quick Start Template for Next Session

```markdown
Continue code cleanup for release preparation:

1. Remove remaining 6 legacy code instances (Priority 1)
2. Handle 2 NotImplementedError stubs (Priority 2)
3. Move ~8 inline defaults to config/defaults.py (Priority 3)
4. Fix ruff issues (3 files) (Priority 4)
5. Fix mypy errors incrementally (Priority 4)
6. Run full test suite

Reference: /Users/tim/code/gh/provide-io/provide-foundation/NEXT_STEPS.md
```

---

## Current State

- **Test Status:** ✅ 205/205 passing
- **Coverage:** ✅ 81.55% (exceeds 80% requirement)
- **Performance:** ✅ Caching optimizations complete
- **Legacy Code:** 🔄 1/7 removed (generate_key_pair done)
- **Code Quality:** ⚠️ 3 ruff issues, ~30 mypy errors
- **Ready for Release:** ❌ Must complete Priority 1-2 items

---

## Files Already Modified This Session

**Source files (do not re-modify unless needed):**
- src/provide/foundation/formatting/text.py
- src/provide/foundation/cli/commands/logs/tail.py
- src/provide/foundation/tools/resolver.py
- src/provide/foundation/platform/detection.py
- src/provide/foundation/platform/info.py
- src/provide/foundation/console/output.py
- src/provide/foundation/crypto/keys.py (legacy removed)
- src/provide/foundation/crypto/__init__.py (legacy removed)

**Test files (already updated with cache clearing):**
- tests/platform/test_platform_detection.py
- tests/platform/test_platform_info.py
- tests/platform/test_platform_coverage.py
