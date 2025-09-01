# Migration Guide: pyvider to provide.foundation

This document outlines the migration from pyvider's internal telemetry/config/hub/cli modules to the new `provide.foundation` package.

## Overview

The `provide.foundation` package consolidates common functionality that was previously duplicated across multiple packages (pyvider, supsrc, etc.). This migration improves code reuse, consistency, and maintainability.

## Major Changes

### 1. Package Structure

**Old structure (pyvider-telemetry):**
```python
from pyvider.telemetry import get_logger, setup_telemetry, TelemetryConfig
from pyvider.hub import hub
from pyvider.cli import cli_main
from pyvider.common.config import PyviderConfig
```

**New structure (provide.foundation):**
```python
from provide.foundation import get_logger, setup_telemetry, TelemetryConfig
from provide.foundation.hub import hub, get_hub
from provide.foundation.cli import cli_main
from provide.foundation.config import BaseConfig
```

### 2. Import Path Updates

All imports have been changed from relative to absolute imports for better clarity and maintainability.

#### Logger/Telemetry
- `from pyvider.telemetry import ...` → `from provide.foundation import ...`
- `from pyvider.telemetry.logger import get_logger` → `from provide.foundation.logger import get_logger`

#### Hub/Registry
- `from pyvider.hub import hub` → `from provide.foundation.hub import get_hub`
- `from pyvider.hub.components import ComponentRegistry` → Uses `provide.foundation.registry.Registry` internally

#### CLI
- `from pyvider.cli.context import PyviderContext` → Extends `provide.foundation.context.Context`
- `from pyvider.cli.decorators import ...` → `from provide.foundation.cli.decorators import ...`

#### Configuration
- `from pyvider.common.config import PyviderConfig` → Extends `provide.foundation.config.BaseConfig`

### 3. Configuration Changes

#### PyviderConfig now extends BaseConfig
The `PyviderConfig` class now extends `provide.foundation.config.BaseConfig` for consistency:

```python
from provide.foundation.config import BaseConfig

class PyviderConfig(BaseConfig):
    """Pyvider-specific configuration."""
    # Inherits all BaseConfig functionality
```

#### Context is now attrs-based
The Context class uses attrs with best practices:

```python
from attrs import define, field

@define(slots=True)
class Context:
    log_level: str = field(default="INFO", validator=validators.in_(VALID_LOG_LEVELS))
    profile: str = field(default="default")
    # ...
```

### 4. New Utilities

#### Type Parsing Utilities
New utilities for parsing strings to typed values (useful for env vars, CLI args, config files):

```python
from provide.foundation.utils.parsing import (
    parse_bool,      # "true"/"false" → True/False
    parse_list,      # "a,b,c" → ["a", "b", "c"]
    parse_dict,      # "k1=v1,k2=v2" → {"k1": "v1", "k2": "v2"}
    parse_typed_value,  # Generic type-based parsing
    auto_parse,      # Auto-parse based on attrs field type
)
```

#### Timing Utilities
Context manager for timing operations:

```python
from provide.foundation.utils import timed_block

with timed_block(logger, "database_query") as ctx:
    ctx["query"] = "SELECT * FROM users"
    result = db.query(...)
    ctx["rows"] = len(result)
```

### 5. Thread Safety

All core components now have built-in thread safety:
- `Registry` uses `threading.RLock()` for all operations
- `Hub` singleton uses double-checked locking pattern
- Logger configuration is thread-safe

### 6. Dependencies

Add `provide-foundation` to your dependencies:

```toml
# pyproject.toml
dependencies = [
    "provide-foundation",  # Replaces pyvider-telemetry
    # ...
]

[tool.uv.sources]
provide-foundation = { path = "../provide-foundation", editable = true }
```

### 7. Breaking Changes

1. **No relative imports**: All imports must be absolute
2. **attrs everywhere**: All configuration and context classes use attrs, not dataclasses
3. **Python 3.11+ only**: No support for Python < 3.11
4. **TOML writing**: Requires `tomli_w` package for TOML file writing

### 8. Testing

Tests have been reorganized:
- Foundation-specific tests → `provide-foundation/tests/`
- Component-dependent tests → `pyvider-components/tests/`
- Hub-related tests → `provide-foundation/tests/hub/`

## Migration Steps

1. **Update dependencies**: Add `provide-foundation`, remove `pyvider-telemetry`
2. **Update imports**: Use the migration script or manually update all import statements
3. **Update configuration**: Ensure configs extend `BaseConfig` if creating custom configs
4. **Run tests**: Verify all tests pass with new foundation
5. **Update CI/CD**: Ensure build pipelines include `provide-foundation`

## Compatibility Notes

- The API is largely compatible, with most changes being import path updates
- Custom logger configurations should continue to work
- Existing hub registrations remain compatible
- CLI decorators and commands work the same way

## Support

For issues or questions about the migration:
- Check the test suite for usage examples
- Review the source code in `provide-foundation/src/provide/foundation/`
- File issues in the provide-foundation repository