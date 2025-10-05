# Circular Dependency Management in Foundation

## Overview

Foundation uses several patterns to manage circular dependencies between modules. This document describes the current approaches and provides guidelines for future development.

## Current State

Foundation has **no active circular import errors** but uses multiple defensive patterns to prevent them. As of the last audit, there are:

- **34 files** using `TYPE_CHECKING` guards for type-only imports
- **~27 locations** using lazy imports (import inside functions)
- **1 event system** (hub/events.py) for decoupled communication
- **1 thread-local recursion detector** (logger/factories.py) for logger access

## Circular Dependency Patterns

### Pattern 1: TYPE_CHECKING Guards (Type-Only Imports)

**Use when:** You need a type hint but not the actual runtime object.

**Example:**
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig

def setup(config: TelemetryConfig) -> None:
    # config is only used for type checking
    # Actual import happens at runtime when called
    from provide.foundation.logger.config import TelemetryConfig
    ...
```

**Files using this pattern:** 34 (see grep output below)

**Pros:**
- Zero runtime overhead
- Prevents import cycles at module load time
- Works well with type checkers (mypy, pyright)

**Cons:**
- Requires duplicate imports if runtime access needed
- Can be confusing for new developers

---

### Pattern 2: Lazy Imports (Deferred Loading)

**Use when:** You need the actual object but only in specific code paths.

**Example:**
```python
def get_logger():
    # Import only when function is called
    from provide.foundation.hub.manager import get_hub
    return get_hub().get_foundation_logger()
```

**Locations:** ~27 throughout codebase

**Common use cases:**
- `streams/file.py` (lines 41, 98, 116) - Import logger only when needed
- `crypto/certificates/factory.py` (lines 42, 82, 141, 187) - Import crypto modules on demand
- `hub/decorators.py` (line 21) - Defer click_builder import
- `errors/context.py` (line 228) - Import context utilities late

**Pros:**
- Breaks import cycles effectively
- Reduces startup time (deferred loading)
- Clear intent with "Import here to avoid circular dependency" comments

**Cons:**
- Slightly slower function calls (first invocation)
- Can hide import errors until runtime
- Makes static analysis harder

---

### Pattern 3: Event System (Decoupled Communication)

**Use when:** Multiple systems need to communicate but shouldn't depend on each other.

**Location:** `hub/events.py` + `hub/event_handlers.py`

**Purpose:** "Provides a lightweight event system to break circular dependencies between hub and logger systems"

**Example:**
```python
# In hub/registry.py (lines 99, 204, 224)
# Emit event instead of direct logging to break circular dependency
self._hub._events.emit("component.registered", data={"name": name})

# In hub/event_handlers.py
def handle_component_registered(data: dict):
    logger = get_safe_logger()  # Safe logger getter
    logger.debug("Component registered", **data)
```

**Pros:**
- Complete decoupling between emitter and handler
- Can add handlers without modifying emitters
- Scalable for complex systems

**Cons:**
- Adds complexity
- Harder to trace code flow
- Event contracts must be documented

---

### Pattern 4: Thread-Local Recursion Detection (Most Sophisticated)

**Use when:** You have unavoidable circular dependencies during initialization.

**Location:** `logger/factories.py`

**How it works:**
```python
_is_initializing = threading.local()
_MAX_RECURSION_DEPTH = 3

def get_logger(name: str | None = None) -> Any:
    depth = getattr(_is_initializing, "depth", 0)

    if depth > 0:
        # Already initializing - use fallback
        import structlog
        return structlog.get_logger(name)

    try:
        _is_initializing.depth = depth + 1
        from provide.foundation.hub.manager import get_hub
        return get_hub().get_foundation_logger(name)
    except (ImportError, RecursionError):
        import structlog
        return structlog.get_logger(name)
    finally:
        _is_initializing.depth = max(0, depth)
```

**Key features:**
- Tracks recursion depth per thread
- Falls back to basic structlog if cycle detected
- Always cleans up state in `finally` block
- Maximum depth limit prevents infinite loops

**Pros:**
- Robust handling of complex initialization
- Graceful fallback behavior
- Thread-safe
- Self-documenting code

**Cons:**
- Most complex pattern
- Slight performance overhead
- Only works for specific use cases

---

### Pattern 5: Avoid Dependencies (Print to Stderr)

**Use when:** Module is so low-level it can't depend on anything.

**Location:** `streams/file.py`, `streams/core.py`

**Example:**
```python
def _error_to_stderr(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies."""
    print(f"ERROR: {message}", file=sys.stderr, flush=True)
```

**Rationale:** Stream modules are used by the logger, so they cannot use the logger themselves.

**Pros:**
- Simple and foolproof
- Zero dependencies
- Always works

**Cons:**
- No structured logging
- No log levels
- Hard to test

---

## Guidelines for New Code

### When adding imports, follow this decision tree:

1. **Can the import be at module level without creating a cycle?**
   - YES → Use normal import
   - NO → Go to step 2

2. **Do you only need the import for type hints?**
   - YES → Use `TYPE_CHECKING` guard (Pattern 1)
   - NO → Go to step 3

3. **Is the import only needed in specific functions/methods?**
   - YES → Use lazy import (Pattern 2) with explanatory comment
   - NO → Go to step 4

4. **Is this for logging/observability in hub/registry code?**
   - YES → Use event system (Pattern 3)
   - NO → Go to step 5

5. **Is this a logger access pattern during initialization?**
   - YES → Use `get_logger()` from factories (Pattern 4)
   - NO → **STOP - Reconsider your architecture**

### If none of these patterns work:

- Your modules might be too tightly coupled
- Consider introducing an interface/protocol
- Consider splitting modules
- Consider dependency injection

---

## Known Circular Dependencies (Managed)

### 1. Logger ↔ Hub
- **Pattern used:** Thread-local recursion detection (Pattern 4)
- **Files:** `logger/factories.py`, `hub/manager.py`
- **Status:** ✅ Working

### 2. Hub ↔ Registry Logging
- **Pattern used:** Event system (Pattern 3)
- **Files:** `hub/registry.py`, `hub/event_handlers.py`
- **Status:** ✅ Working

### 3. Streams ↔ Logger
- **Pattern used:** Avoid dependencies (Pattern 5)
- **Files:** `streams/file.py`, `streams/core.py`
- **Status:** ✅ Working

### 4. Config Parsers ↔ Logger
- **Pattern used:** Lazy imports (Pattern 2)
- **Files:** Various config/parsers/* files
- **Status:** ✅ Working

---

## Future Improvements

### Short Term (Next Release)

1. **Standardize lazy import comments**
   - Current: Mix of "Import here to avoid circular dependency", "Lazy import to avoid circular dependency", "Defer import"
   - Target: Use consistent format: `# Import deferred to avoid circular dependency with <module>`

2. **Add TYPE_CHECKING to more type-only imports**
   - Audit all `from X import Y` where Y is only used in type hints
   - Convert to TYPE_CHECKING guards
   - Estimated: 10-15 additional conversions

3. **Document event contracts**
   - Create `hub/events_contracts.md` documenting all event types
   - Include payload schemas
   - Add type hints for event data

### Medium Term (Post-Release)

1. **Dependency Injection for Logger**
   - Instead of `get_logger()` accessing global hub, inject logger instances
   - Example: `class MyClass: def __init__(self, logger: FoundationLogger = None)`
   - Benefits: Testability, explicit dependencies, no hidden globals

2. **Protocol/Interface Layer**
   - Create `provide.foundation.interfaces` package
   - Define protocols for `Logger`, `Config`, `Hub`, etc.
   - Allow modules to depend on interfaces, not concrete implementations

3. **Lazy Module Loading**
   - Use `importlib.util.LazyLoader` for heavy modules
   - Defer loading of crypto, profiling, CLI until actually used
   - Faster startup time

### Long Term (Major Version)

1. **Module Restructuring**
   - Split `hub` into smaller, focused modules
   - Separate "hub core" from "hub registry" from "hub events"
   - Clearer dependency graph

2. **Replace Event System with Hooks**
   - More explicit than events
   - Better type safety
   - Easier to discover (IDE autocomplete)
   - Example: `hub.on_component_registered.add(handler)`

3. **Consider Async-First Initialization**
   - Use `async def initialize()` to handle complex init sequences
   - Allows proper ordering without circular workarounds
   - Better error handling

---

## Testing for Circular Dependencies

### Manual Check
```bash
cd src
python3 -c "import provide.foundation" 2>&1 | grep -i "circular\|import.*error"
```

### Automated Check (pytest)
```python
def test_no_circular_imports():
    """Ensure foundation can be imported without circular dependency errors."""
    try:
        import provide.foundation
        assert True
    except ImportError as e:
        if "circular" in str(e).lower():
            pytest.fail(f"Circular import detected: {e}")
        raise
```

### Find TYPE_CHECKING Usage
```bash
grep -r "TYPE_CHECKING" src/provide/foundation/ --include="*.py" | wc -l
```

### Find Lazy Imports
```bash
grep -r "avoid circular" src/provide/foundation/ --include="*.py" -i
```

---

## References

- Python Import System: https://docs.python.org/3/reference/import.html
- PEP 484 (Type Hints): https://peps.python.org/pep-0484/
- PEP 563 (Postponed Annotations): https://peps.python.org/pep-0563/
- Thread-Local Storage: https://docs.python.org/3/library/threading.html#thread-local-data

---

## Appendix: Files Using TYPE_CHECKING

Current count: **34 files**

<details>
<summary>Full list (click to expand)</summary>

```
src/provide/foundation/cli/decorators.py
src/provide/foundation/crypto/certificates/generator.py
src/provide/foundation/config/defaults.py
src/provide/foundation/logger/core.py
src/provide/foundation/crypto/__init__.py
src/provide/foundation/cli/commands/logs/tail.py
src/provide/foundation/observability/__init__.py
src/provide/foundation/tracer/spans.py
src/provide/foundation/hub/foundation.py
src/provide/foundation/crypto/certificates/certificate.py
src/provide/foundation/cli/commands/logs/send.py
src/provide/foundation/logger/processors/trace.py
src/provide/foundation/profiling/component.py
src/provide/foundation/profiling/cli.py
src/provide/foundation/crypto/certificates/loader.py
src/provide/foundation/crypto/certificates/trust.py
src/provide/foundation/crypto/certificates/operations.py
src/provide/foundation/crypto/certificates/factory.py
src/provide/foundation/console/input.py
src/provide/foundation/eventsets/display.py
src/provide/foundation/hub/info.py
src/provide/foundation/cli/main.py
src/provide/foundation/cli/commands/logs/__init__.py
src/provide/foundation/cli/commands/logs/generate.py
src/provide/foundation/cli/commands/deps.py
src/provide/foundation/utils/timing.py
src/provide/foundation/config/parsers/base.py
src/provide/foundation/config/parsers/structured.py
src/provide/foundation/config/parsers/telemetry.py
src/provide/foundation/transport/errors.py
src/provide/foundation/crypto/signatures.py
src/provide/foundation/crypto/certificates/base.py
src/provide/foundation/tracer/otel.py
src/provide/foundation/tracer/__init__.py
```

</details>

---

**Last Updated:** 2025-10-03
**Status:** ✅ No active circular import errors
**Next Review:** After major refactoring or before next major release
