# Code Cleanup & Release Preparation - Next Steps

## 🔄 REMAINING WORK - Priority Order

---

### Priority 2: HIGH - Remove Remaining Legacy Code

#### 2.1 EventSets Legacy Aliases
**File:** `src/provide/foundation/eventsets/sets/das.py`
**Lines:** 126-128
**Action:** Remove these legacy aliases:
```python
# Legacy aliases (REMOVE THESE)
das_event_set = DASEventSet()
default_event_set = das_event_set
```

#### 2.2 Logger Legacy Comment
**File:** `src/provide/foundation/logger/core.py`
**Line:** 327
**Action:** Remove backward compatibility comment:
```python
# Backward compatibility: provide global logger object with lazy access
# (REMOVE THIS COMMENT)
```

#### 2.3 Context Legacy Alias
**File:** `src/provide/foundation/context/__init__.py`
**Line:** ~15
**Action:** Find and remove `Context` legacy alias export
**Search for:** `Context.*Legacy alias`

#### 2.4 CLI Decorators Legacy Function
**File:** `src/provide/foundation/cli/decorators.py`
**Line:** 135+
**Action:** Remove `all_options()` decorator (described as "legacy all-in-one option handling")
**Alternative:** Check if it's used anywhere first with: `grep -r "all_options" tests/ src/`

#### 2.5 File Lock Backward Compatibility
**File:** `src/provide/foundation/file/lock.py`
**Line:** ~202
**Action:** Remove backward compatibility code for old lock files
**Search for:** `backward compatibility with old lock files`

#### 2.6 TestMode Legacy State
**File:** `src/provide/foundation/testmode/orchestration.py`
**Line:** ~311
**Action:** Remove legacy state handling code
**Search for:** `Legacy state not available`

---

### Priority 3: HIGH - NotImplementedError Stubs

#### 3.1 OpenObserve HTTP API
**File:** `src/provide/foundation/integrations/openobserve/__init__.py`
**Line:** 66
**Current:**
```python
raise NotImplementedError("HTTP API ingestion not yet implemented")
```
**Decision needed:** Either implement HTTP API ingestion OR remove the stub entirely
**Recommended:** Remove stub if not planned for immediate release

#### 3.2 Transport Streaming
**File:** `src/provide/foundation/transport/base.py`
**Line:** 154
**Current:**
```python
raise NotImplementedError(f"{self.__class__.__name__} does not support streaming")
```
**Action:** Change to proper error or document as intentional limitation

---

### Priority 4: HIGH - Move Inline Defaults to Config

#### 4.1 Add Constants to config/defaults.py

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

#### 4.2 Update Files to Use Defaults

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

### Priority 5: Code Quality Fixes

#### 5.1 Ruff Issues (3 total)

**Run:** `ruff check --fix --unsafe-fixes src/provide/foundation/`

**Known Issues:**
1. `crypto/certificates/generator.py:126` - Duplicate imports (ec, rsa appear on lines 121 AND 126)
2. `file/operations/detectors/batch.py:102` - Unused variable `operation_type`

#### 5.2 MyPy Type Errors (~30 total)

**Run:** `mypy src/provide/foundation/`

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
ruff check --fix --unsafe-fixes src/provide/foundation/
ruff format src/provide/foundation/

# Run mypy (incremental fixes)
bin/mypy src/provide/foundation/ | head -50
```

### Testing
```bash
# Quick test of modified areas
timeout 120 pytest tests/crypto/ tests/eventsets/ tests/context/ -q

# Test concurrency/resilience
timeout 120 pytest tests/concurrency/ tests/resilience/ -q

# Full test suite
timeout 300 pytest -n auto -q --tb=line

# Coverage check (must be >80%)
timeout 300 pytest --cov=src/provide/foundation --cov-report=term-missing
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

# Find circular import patterns
grep -r "TYPE_CHECKING" src/provide/foundation/ --include="*.py"
grep -r "import.*if.*TYPE_CHECKING" src/provide/foundation/ --include="*.py" -A 3
```
