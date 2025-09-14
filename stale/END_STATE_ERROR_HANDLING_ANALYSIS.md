# End-State Error Handling Decorator Analysis

## Current State vs End-State Design

This document analyzes what would change if we ignored backward compatibility and designed the `with_error_handling` decorator from scratch for the optimal end-state.

## Current Implementation (Backward Compatible)

The current implementation supports both Foundation and supsrc usage patterns:

```python
# Foundation pattern
@with_error_handling(
    context_provider=lambda: {"function": "load_config"},
    log_errors=True
)

# supsrc pattern  
@with_error_handling(
    reraise=True,
    context={"component": "orchestrator", "method": "run"}
)
```

## End-State Implementation (Clean Design)

If we removed backward compatibility constraints, the API would be much cleaner:

### 1. Unified Context Parameter

**Current:** Two ways to provide context
- `context_provider: Callable[[], dict]` - Foundation pattern
- `context: dict` - supsrc pattern

**End-state:** Single static context parameter
```python
@with_error_handling(
    context={"component": "orchestrator", "method": "run"}
)
```

### 2. Clearer Parameter Naming

**Current:** `reraise: bool = True` (confusing - implies it was already raised)

**End-state:** `suppress: bool = False` (clearer intent)
```python
@with_error_handling(suppress=True, fallback="default")  # Don't raise
@with_error_handling(suppress=False)  # Log and raise (default)
```

### 3. Simplified Error Control

**Current:** Complex interaction between multiple parameters:
- `suppress: tuple[type[Exception], ...]` - suppress specific exception types
- `reraise: bool` - control re-raising behavior
- `fallback: Any` - return value when not raising

**End-state:** Single boolean control:
```python
@with_error_handling(suppress=True, fallback="default")  # All errors suppressed
@with_error_handling(suppress=False)  # All errors re-raised after logging
```

### 4. Implementation Simplification

The end-state implementation would be ~30% smaller:
- Remove callable context provider logic
- Remove tuple-based exception filtering
- Single code path through error handling
- Better performance (no lambda calls on every error)

## Breaking Changes Required

### Foundation Codebase (8 usages)
Current `context_provider` usage would become static `context`:

```python
# Before
@with_error_handling(
    context_provider=lambda: {"function": "pout"}
)

# After  
@with_error_handling(
    context={"function": "pout"}
)
```

Files affected:
- `console/output.py`: 2 usages
- `config/loader.py`: 1 usage  
- `hub/config.py`: 1 usage
- `hub/manager.py`: 1 usage
- `hub/components.py`: 1 usage
- `hub/handlers.py`: 1 usage
- `process/lifecycle.py`: 1 usage

### supsrc Codebase (2 usages)
Change parameter name:

```python
# Before
@with_error_handling(reraise=False)

# After
@with_error_handling(suppress=True)
```

## Benefits of End-State Design

1. **Simpler API**: One context parameter, one suppress parameter
2. **Clearer semantics**: `suppress=True` vs confusing `reraise=False`
3. **Less complexity**: ~30% reduction in implementation code
4. **Better performance**: No callable overhead on every error
5. **Easier maintenance**: Single code path, fewer edge cases
6. **More intuitive**: Follows principle of least surprise

## Implementation Plan

If/when backward compatibility is not needed:

1. **Replace** all `context_provider` usage with static `context` 
2. **Replace** `reraise` parameter with `suppress` parameter (inverse logic)
3. **Remove** tuple-based `suppress` parameter entirely
4. **Update** supsrc to use new API  
5. **Simplify** decorator implementation
6. **Update** documentation and examples

## Estimated Impact

- **Foundation**: 8 decorator call sites to update
- **supsrc**: 2 decorator call sites to update  
- **Implementation**: ~40 lines of code reduction
- **Documentation**: 3 guide files to update
- **Tests**: ~15 test cases to update

## Current Status

For now, the backward-compatible implementation supports both patterns to maintain compatibility while supsrc adoption continues. The end-state refactor can be considered when all provide-ecosystem packages are stable.