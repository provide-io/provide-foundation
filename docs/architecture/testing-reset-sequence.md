# Foundation Testing Reset Sequence

This document describes the critical ordering requirements for resetting Foundation's internal state during testing.

## Overview

Foundation's testing infrastructure requires careful coordination of reset operations to ensure proper test isolation. The reset sequence must follow a specific order to avoid dependency conflicts and ensure complete state cleanup.

## Reset Sequence Order

The following functions must be called **in this exact order** for proper test isolation:

```python
# Required reset sequence (do not reorder)
reset_structlog_state()     # 1. Reset structlog configuration
reset_streams_state()       # 2. Reset file streams and output
reset_logger_state()        # 3. Reset Foundation logger state
reset_hub_state()           # 4. Reset Hub components and registry
reset_coordinator_state()   # 5. Reset setup coordinator cache
reset_eventsets_state()     # 6. Reset event set registry
reset_profiling_state()     # 7. Reset profiling metrics (if enabled)
clear_hub()                 # 8. Clear global Hub instance
```

## Why This Order Matters

### 1. Structlog First (`reset_structlog_state()`)
- **Why**: Structlog is the lowest-level logging infrastructure
- **Dependencies**: All other components depend on structlog
- **Effect**: Resets processor chains, logger factory, and configuration

### 2. Streams Second (`reset_streams_state()`)
- **Why**: Stream configuration affects where logs are written
- **Dependencies**: Must happen before logger reset to avoid writing to closed streams
- **Effect**: Closes file handles, resets output targets

### 3. Logger Third (`reset_logger_state()`)
- **Why**: Foundation logger depends on both structlog and streams
- **Dependencies**: Requires clean structlog and stream state
- **Effect**: Resets lazy setup flags, clears cached loggers

### 4. Hub Fourth (`reset_hub_state()`)
- **Why**: Hub manages component lifecycle and dependencies
- **Dependencies**: Must happen after logger to avoid component initialization issues
- **Effect**: Clears component registry, resets Hub components

### 5. Coordinator Fifth (`reset_coordinator_state()`)
- **Why**: Coordinator manages setup process and caches
- **Dependencies**: Requires clean logger and Hub state
- **Effect**: Clears setup caches, resets coordinator flags

### 6. Event Sets Sixth (`reset_eventsets_state()`)
- **Why**: Event sets provide emoji mapping for logging
- **Dependencies**: Must happen after logger reset
- **Effect**: Clears event set registry, resets discovery state

### 7. Profiling Seventh (`reset_profiling_state()`)
- **Why**: Profiling tracks metrics about other components
- **Dependencies**: Should be reset after all monitored components
- **Effect**: Clears metrics, resets profiling state

### 8. Clear Hub Last (`clear_hub()`)
- **Why**: Final cleanup of global Hub singleton
- **Dependencies**: Must happen after all component resets
- **Effect**: Sets global Hub instance to None

## Critical Dependency Graph

```
structlog (base layer)
  ↓
streams (output layer)
  ↓
logger (Foundation layer)
  ↓
hub (component layer)
  ↓
coordinator (setup layer)
  ↓
eventsets (enhancement layer)
  ↓
profiling (monitoring layer)
  ↓
clear_hub (cleanup)
```

## Usage in Tests

### Standard Test Setup

```python
import pytest
from provide.foundation.testmode import (
    reset_structlog_state,
    reset_streams_state,
    reset_logger_state,
    reset_hub_state,
    reset_coordinator_state,
    reset_eventsets_state,
    reset_profiling_state,
)
from provide.foundation.hub.manager import clear_hub

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    # CRITICAL: Maintain this exact order
    reset_structlog_state()
    reset_streams_state()
    reset_logger_state()
    reset_hub_state()
    reset_coordinator_state()
    reset_eventsets_state()
    reset_profiling_state()
    clear_hub()
```

### For Test Classes

```python
class TestMyFeature:
    def setup_method(self) -> None:
        """Reset Foundation state before each test method."""
        # Use the same sequence as above
        reset_structlog_state()
        reset_streams_state()
        reset_logger_state()
        reset_hub_state()
        reset_coordinator_state()
        reset_eventsets_state()
        reset_profiling_state()
        clear_hub()
```

## Troubleshooting

### Common Issues

1. **Tests hang during reset**
   - **Cause**: Reset functions called out of order
   - **Solution**: Verify exact sequence above

2. **Components not properly reset**
   - **Cause**: Missing reset function in sequence
   - **Solution**: Add missing reset function in correct position

3. **Import errors during testing**
   - **Cause**: Circular dependencies from incorrect reset order
   - **Solution**: Reset structlog first, Hub last

4. **State pollution between tests**
   - **Cause**: Incomplete reset sequence
   - **Solution**: Ensure all reset functions are called

### Debugging Reset Issues

Enable debug logging to trace reset sequence:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Each reset function will log its actions
```

## Adding New Components

When adding new Foundation components that require test reset:

1. **Add reset function** to appropriate module
2. **Update reset sequence** in this document
3. **Add to testmode exports** if needed
4. **Test the new sequence** thoroughly

### Reset Function Guidelines

```python
def reset_my_component_state() -> None:
    """Reset MyComponent state to defaults.

    This function should:
    - Clear all cached state
    - Reset configuration to defaults
    - Close any open resources
    - Be idempotent (safe to call multiple times)
    """
    try:
        # Reset implementation here
        pass
    except ImportError:
        # Component not available, skip gracefully
        pass
```

## Performance Considerations

- Reset sequence adds ~10-50ms per test
- Consider grouping tests that don't need full reset
- Use `pytest.mark.no_reset` for tests that don't modify Foundation state
- Reset functions are designed to be fast and idempotent

## Historical Changes

- **v1.0**: Initial reset sequence established
- **v1.1**: Added profiling reset support
- **v1.2**: Improved error handling in reset functions

---

**⚠️ WARNING**: Modifying this reset sequence can break test isolation and cause hard-to-debug test failures. Always validate changes against the full test suite.