# Next Dogfooding Plan - Foundation Improvements

## Current Session Status

### ✅ Completed in This Session:
1. **Standardized Logger Variable Names**
   - Renamed `plog` → `log` (12 files: crypto, platform, process, console)
   - Renamed `logger` → `log` (6 files: archive, docs, eventsets)
   - Fixed test mocks (console/test_input.py)
   - **54 files** now use `log = get_logger(__name__)`
   - **2 files** use `slog = get_system_logger(__name__)` for bootstrap logging
   - Result: **992+ tests passing**

2. **Renamed Serialization Functions**
   - `provide_dumps` → `json_dumps`
   - `provide_loads` → `json_loads`
   - Updated 5 source files + tests
   - Result: **976 tests passing**

3. **Dogfooding: Console Module Improvements** (IN PROGRESS)
   - ✅ Replaced `os.environ.get()` with Foundation's `get_str()`, `get_bool()` in console/output.py
   - ✅ Replaced `json.dumps()` with `json_dumps()` in console/output.py
   - ✅ Replaced `json.loads()`/`json.dumps()` with `json_loads()`/`json_dumps()` in console/input.py
   - ⚠️ **Need to test** - run console tests before continuing

## Remaining Dogfooding Tasks

### Priority 1: Complete Console Module Dogfooding
**Status**: In progress, nearly complete

**Tasks**:
1. Run code quality checks on console/input.py
2. Run console tests: `pytest tests/console/ -v`
3. If tests pass, mark console module as complete

**Files Modified**:
- `src/provide/foundation/console/output.py`
- `src/provide/foundation/console/input.py`

---

### Priority 2: Replace json Usage in Remaining Files
**Status**: Not started

**Files to update** (from earlier analysis):
1. `src/provide/foundation/cli/decorators.py`
2. `src/provide/foundation/integrations/openobserve/otlp.py`
3. Any other files found with `import json` that should use Foundation's serialization

**Pattern**:
```python
# Before:
import json
data = json.loads(string)
string = json.dumps(data)

# After:
from provide.foundation.serialization import json_loads, json_dumps
data = json_loads(string)
string = json_dumps(data)

# Exception handling:
# Replace: except json.JSONDecodeError
# With: except ValidationError
```

**Commands**:
```bash
# Find remaining files
grep -r "import json\b" src/ --include="*.py" -l

# For each file:
1. Add import: from provide.foundation.serialization import json_loads, json_dumps
2. Add import: from provide.foundation.errors import ValidationError (if needed)
3. Replace json.loads → json_loads
4. Replace json.dumps → json_dumps
5. Replace json.JSONDecodeError → ValidationError
6. Run ruff: .venv/bin/ruff check --fix --unsafe-fixes <file>
7. Run ruff format: .venv/bin/ruff format <file>
```

---

### Priority 3: Documentation Updates
**Status**: Not started

**Tasks**:
1. Update DOGFOODING.md with completed improvements:
   - Add section on logger name standardization
   - Add section on serialization function renaming
   - Add section on console module dogfooding

2. Update DOGFOODING_NEXT_STEPS.md:
   - Mark phases as complete
   - Update test counts
   - Add summary of improvements

3. Update developer docs (if any) with new naming conventions

**Template for DOGFOODING.md**:
```markdown
### 11. Standardized Logger Variable Names
**Status**: ✅ Completed
**Files Changed**: 18 files across crypto, platform, process, console, archive, docs, eventsets

- **Before**: Mixed usage of `plog`, `logger`, `log`
- **After**: Standardized on `log` for all module-level loggers
- **Exception**: `slog` reserved for system/bootstrap logging
- **Impact**: Consistent naming across entire codebase
- **Benefits**:
  - Easier to read and understand
  - Less cognitive overhead
  - Clear distinction between app logging (`log`) and bootstrap logging (`slog`)

### 12. Renamed Serialization Functions for Clarity
**Status**: ✅ Completed
**Files Changed**: 7 files (serialization core, config, CLI, tests)

- **Before**: `provide_dumps()`, `provide_loads()` (ambiguous naming)
- **After**: `json_dumps()`, `json_loads()` (clear JSON-specific naming)
- **Impact**: Makes it immediately clear these are JSON-specific utilities
- **Benefits**:
  - Follows Python stdlib naming convention
  - Room for future format-specific functions (yaml_dumps, toml_dumps)
  - Explicit is better than implicit

### 13. Console Module: Uses Foundation Utilities
**Status**: ✅ Completed
**Files Changed**: 2 files (console/output.py, console/input.py)

- **Changes**:
  - Replaced `os.environ.get()` → `get_str()`, `get_bool()`
  - Replaced `json.dumps()` → `json_dumps()`
  - Replaced `json.loads()` → `json_loads()`
- **Impact**: Console module now uses Foundation's own utilities
- **Benefits**:
  - Consistent environment variable access
  - Consistent serialization
  - Better error handling with ValidationError
```

---

### Priority 4: Create Environment Variable Constants (Optional)
**Status**: Not started (Nice to have)

**Rationale**: Tests have hardcoded "PROVIDE_*" strings scattered throughout

**Implementation**:
```python
# Create: src/provide/foundation/constants/env_vars.py
"""Environment variable name constants for Foundation."""

# Telemetry
SERVICE_NAME = "PROVIDE_SERVICE_NAME"
TELEMETRY_DISABLED = "PROVIDE_TELEMETRY_DISABLED"

# Logging
LOG_LEVEL = "PROVIDE_LOG_LEVEL"
LOG_CONSOLE_FORMATTER = "PROVIDE_LOG_CONSOLE_FORMATTER"
LOG_LOGGER_NAME_EMOJI_ENABLED = "PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"
LOG_DAS_EMOJI_ENABLED = "PROVIDE_LOG_DAS_EMOJI_ENABLED"
LOG_OMIT_TIMESTAMP = "PROVIDE_LOG_OMIT_TIMESTAMP"
LOG_MODULE_LEVELS = "PROVIDE_LOG_MODULE_LEVELS"
LOG_SANITIZATION_ENABLED = "PROVIDE_LOG_SANITIZATION_ENABLED"
LOG_SANITIZATION_MASK_PATTERNS = "PROVIDE_LOG_SANITIZATION_MASK_PATTERNS"
LOG_SANITIZATION_SANITIZE_DICTS = "PROVIDE_LOG_SANITIZATION_SANITIZE_DICTS"

# OpenTelemetry
OTLP_ENDPOINT = "PROVIDE_OTLP_ENDPOINT"
OTLP_TRACES_ENDPOINT = "PROVIDE_OTLP_TRACES_ENDPOINT"

# Foundation Internal
FOUNDATION_LOG_LEVEL = "FOUNDATION_LOG_LEVEL"
FOUNDATION_LOG_OUTPUT = "FOUNDATION_LOG_OUTPUT"
FORCE_COLOR = "FORCE_COLOR"
NO_COLOR = "NO_COLOR"

__all__ = [
    "SERVICE_NAME",
    "TELEMETRY_DISABLED",
    "LOG_LEVEL",
    # ... etc
]
```

**Usage**:
```python
# Before:
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

# After:
from provide.foundation.constants.env_vars import LOG_LEVEL
os.environ[LOG_LEVEL] = "DEBUG"
```

**Benefits**:
- Typo-proof (autocomplete + type checking)
- Single source of truth
- Easy to refactor if names change

---

### Priority 5: Run Full Test Suite
**Status**: Not started

**Commands**:
```bash
# Run all tests
.venv/bin/pytest tests/ -v --tb=short

# Or run specific test suites
.venv/bin/pytest tests/console tests/cli tests/serialization tests/logger -v
```

**Expected Results**:
- All tests should pass
- No regressions from naming changes
- Console module tests verify dogfooding improvements

---

## Future Dogfooding Opportunities (Lower Priority)

### 1. Use @resilient Decorator More Widely
**Files to consider**:
- Process execution modules
- File operations
- Network/HTTP operations

**Pattern**:
```python
from provide.foundation.errors.decorators import resilient

@resilient(
    fallback=None,
    suppress=(IOError, OSError),
    context_provider=lambda: {"operation": "file_read"}
)
def read_config_file(path):
    ...
```

### 2. Use Foundation's Validation Utilities
**Current state**: Manual type checking with `isinstance()` in many places

**Pattern**:
```python
# Before:
if not isinstance(value, str):
    raise TypeError("Expected string")

# After:
from provide.foundation.validation import ensure_type
value = ensure_type(value, str)
```

### 3. Use Foundation's Async Helpers
**Files**: Any with raw `asyncio.create_task()`, `asyncio.gather()`, etc.

**Pattern**: Create Foundation wrappers if they don't exist

### 4. Use Foundation's Path Utilities (If Needed)
**Consideration**: Only if there's value in standardizing path operations

---

## Testing Checklist

After completing all dogfooding improvements:

- [ ] Console tests pass: `pytest tests/console/ -v`
- [ ] Serialization tests pass: `pytest tests/serialization/ -v`
- [ ] CLI tests pass: `pytest tests/cli/ -v`
- [ ] Full test suite passes: `pytest tests/ -v`
- [ ] Code quality: `ruff check src/`
- [ ] Format: `ruff format src/`
- [ ] Type checks: `mypy src/` (if applicable)

---

## Summary of Naming Conventions

### Logger Variables
```python
# Standard module logger (everywhere)
log = get_logger(__name__)

# System/bootstrap logger (only in otel.py, coordinator.py)
slog = get_system_logger(__name__)
```

### Serialization Functions
```python
from provide.foundation.serialization import json_dumps, json_loads

# JSON serialization
data_str = json_dumps({"key": "value"})
data = json_loads(data_str)
```

### Environment Variables
```python
from provide.foundation.utils.environment import get_str, get_bool, get_int

# Get environment variables
level = get_str("LOG_LEVEL", "INFO")
enabled = get_bool("FEATURE_ENABLED", False)
port = get_int("PORT", 8080)
```

---

## Commands Reference

### Find files that need updates
```bash
# Find files with old logger names (should be none now)
grep -r "^plog = \|^logger = " src/ --include="*.py"

# Find files still using json module directly
grep -r "import json\b\|from json import" src/ --include="*.py" -l

# Find files using os.environ directly (excluding infrastructure files)
grep -r "os\.environ" src/ --include="*.py" -l | grep -v "config/env\|utils/environment"
```

### Code quality workflow
```bash
# Fix and format a file
.venv/bin/ruff check --fix --unsafe-fixes src/path/to/file.py
.venv/bin/ruff format src/path/to/file.py

# Run tests for a module
.venv/bin/pytest tests/module_name/ -v --tb=short
```

---

## Notes

- All test counts and file counts are approximate based on the current session
- The codebase is in a stable state with 992+ tests passing
- Focus on completing console module dogfooding first, then expand to other files
- Documentation updates can happen in parallel with technical work
- Environment variable constants are optional but would improve developer experience
