# Optional Dependency Patterns

This document defines the standard patterns for handling optional dependencies in Foundation.

## Overview

Foundation uses **four distinct patterns** for optional dependencies, each optimized for specific use cases. Using the right pattern ensures optimal performance, user experience, and maintainability.

## Pattern Decision Tree

```
Is this an optional dependency?
│
├─ YES → What's the primary use case?
│   │
│   ├─ Internal conditional logic (performance-critical)?
│   │   └─ ✅ Use Pattern 1: _HAS_* Flags
│   │
│   ├─ Public API feature (user-facing)?
│   │   └─ ✅ Use Pattern 2: __getattr__ Lazy Loading
│   │
│   ├─ Complete API surface (type checking needed)?
│   │   └─ ✅ Use Pattern 3: Stub Classes
│   │
│   └─ Module-level export control?
│       └─ ✅ Use Pattern 4: Dynamic __all__
│
└─ NO → Import normally
```

## Pattern 1: `_HAS_*` Flags

**When to Use**: Internal conditionals, performance-critical checks

**Characteristics**:
- Fast boolean flag check
- Used for internal logic branching
- Minimal performance overhead
- No user-facing error messages needed

**Example**:
```python
# At module top
try:
    import click
    _HAS_CLICK = True
except ImportError:
    click: Any = None
    _HAS_CLICK = False

# Later in code
def some_internal_function():
    if _HAS_CLICK:
        # Use click features
        return build_cli()
    else:
        # Fallback behavior
        return None
```

**Used In**:
- `hub/decorators.py` - Click availability
- `crypto/*` - Cryptography features (15 files)
- `cli/*` - Click-dependent CLI (8 files)
- `metrics/*` - OpenTelemetry metrics
- `tracer/*` - OpenTelemetry tracing

## Pattern 2: `__getattr__` Lazy Loading

**When to Use**: Public API features with helpful error messages

**Characteristics**:
- Lazy loads features on first access
- Provides helpful error messages to users
- Clear installation instructions
- Graceful AttributeError for unknown attributes

**Example** (Gold Standard from `hub/commands.py`):
```python
def __getattr__(name: str) -> Any:
    """Support lazy loading of CLI-dependent features."""
    if name in ("build_click_command", "create_command_group"):
        try:
            from provide.foundation.cli.click.builder import (
                build_click_command,
                create_command_group,
            )
            if name == "build_click_command":
                return build_click_command
            if name == "create_command_group":
                return create_command_group
        except ImportError as e:
            if "click" in str(e):
                raise ImportError(
                    f"CLI feature '{name}' requires: pip install 'provide-foundation[cli]'",
                ) from e
            raise
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "build_click_command",  # noqa: F822 - lazy loaded
    "create_command_group",  # noqa: F822 - lazy loaded
]
```

**Used In**:
- `hub/commands.py` ⭐ GOLD STANDARD
- `hub/__init__.py` - Click features
- `foundation/__init__.py` - Module lazy loading
- `utils/__init__.py` - Submodule loading
- `_version.py` - Version loading

## Pattern 3: Stub Classes

**When to Use**: Complete API surface for type checking + graceful degradation

**Characteristics**:
- Provides complete type information
- IDE autocomplete works correctly
- Graceful runtime errors with install instructions
- Type safety without runtime dependency

**Example** (using `create_dependency_stub`):
```python
try:
    from provide.foundation.transport.http import HTTPTransport
    _HAS_HTTPX = True
except ImportError:
    from provide.foundation.utils.stubs import create_dependency_stub
    _HAS_HTTPX = False
    HTTPTransport = create_dependency_stub("httpx", "transport")
```

**Manual Stub Example** (when more control needed):
```python
if not _HAS_CRYPTO:
    from provide.foundation.errors import DependencyError

    class Certificate:
        """Stub for Certificate when cryptography is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError("cryptography", feature="crypto")

        @classmethod
        def create_self_signed(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError("cryptography", feature="crypto")
```

**Used In**:
- `transport/__init__.py` - HTTPTransport (uses `create_dependency_stub`)
- `crypto/__init__.py` - Certificate classes (manual stubs, 337 lines)

## Pattern 4: Dynamic `__all__`

**When to Use**: Module-level export control based on availability

**Characteristics**:
- Controls what's exported from module
- Works with `from module import *`
- Clean module interface
- Prevents importing unavailable features

**Example**:
```python
if _HAS_OTEL:
    from provide.foundation.integrations.openobserve import (
        OpenObserveClient,
        search_logs,
        stream_logs,
    )
    __all__ = [
        "_HAS_OTEL",
        "OpenObserveClient",
        "search_logs",
        "stream_logs",
    ]
else:
    __all__ = ["_HAS_OTEL"]
```

**Used In**:
- `observability/__init__.py` - OpenObserve features

## Combining Patterns

Patterns can be combined when appropriate:

```python
# Pattern 1: Internal flag
try:
    import cryptography
    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False

# Pattern 3: Stub classes
if not _HAS_CRYPTO:
    Certificate = create_dependency_stub("cryptography", "crypto")

# Pattern 4: Dynamic exports
if _HAS_CRYPTO:
    __all__ = ["Certificate", "sign_data", "verify_signature"]
else:
    __all__ = ["Certificate"]  # Stub version exported
```

## Best Practices

### DO:
- ✅ Use `_HAS_*` for internal conditional logic
- ✅ Use `__getattr__` for public API features
- ✅ Use stub classes for type safety
- ✅ Provide clear install instructions in error messages
- ✅ Set `Any` type for missing imports: `click: Any = None`
- ✅ Add `# type: ignore` only when necessary for stubs

### DON'T:
- ❌ Mix patterns without clear rationale
- ❌ Create manual stubs when `create_dependency_stub()` suffices
- ❌ Raise unhelpful errors (always include install command)
- ❌ Use bare `except:` - catch `ImportError` specifically
- ❌ Complicate simple cases - use simplest pattern that works

## Migration Guide

### Simplifying Manual Stubs

If you have manual stub classes, consider migrating to `create_dependency_stub()`:

**Before** (337 lines in crypto/__init__.py):
```python
if not _HAS_CRYPTO:
    class Certificate:
        def __init__(self, *args, **kwargs):
            raise DependencyError("cryptography", feature="crypto")
        @classmethod
        def create_self_signed(cls, *args, **kwargs):
            raise DependencyError("cryptography", feature="crypto")
    # ... 300+ more lines
```

**After** (1 line):
```python
if not _HAS_CRYPTO:
    Certificate = create_dependency_stub("cryptography", "crypto")
```

**Trade-offs**:
- ✅ Much simpler (336 lines removed)
- ✅ Consistent with other modules
- ❌ Loses specific method stubs (but methods still fail with clear error)
- ❌ Loses custom error messages per method

## Examples by Use Case

### Use Case: Fast Internal Check
→ **Pattern 1**: `_HAS_CLICK` flag

### Use Case: User-Facing CLI Feature
→ **Pattern 2**: `__getattr__` with helpful error

### Use Case: Transport Implementation
→ **Pattern 3**: Stub class for type safety

### Use Case: Optional OpenObserve Integration
→ **Pattern 4**: Dynamic `__all__` exports

### Use Case: Both Type Safety AND Export Control
→ **Combine Pattern 3 + 4**: Stub classes + dynamic `__all__`

## Testing Optional Dependencies

Always test both with and without optional dependencies:

```python
def test_feature_with_dependency(monkeypatch):
    """Test when dependency is available."""
    # Normal test

def test_feature_without_dependency(monkeypatch):
    """Test graceful degradation."""
    monkeypatch.setattr("module._HAS_FEATURE", False)
    with pytest.raises(DependencyError):
        use_feature()
```

## Summary

| Pattern | Use Case | Performance | UX | Type Safety |
|---------|----------|-------------|----|----|
| 1. `_HAS_*` Flags | Internal logic | ⚡ Fastest | N/A | ⚠️ Manual typing |
| 2. `__getattr__` | Public API | ⚡ Fast (lazy) | ⭐ Best errors | ⚠️ Dynamic |
| 3. Stub Classes | Type checking | ⚡ Fast | ✅ Good errors | ⭐ Complete |
| 4. Dynamic `__all__` | Export control | ⚡ Fast | ✅ Clean imports | ✅ Good |

Choose the pattern that best fits your use case. When in doubt, follow existing examples in similar modules.
