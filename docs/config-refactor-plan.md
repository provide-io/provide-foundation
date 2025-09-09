# Configuration System Refactor Plan

## Current State Analysis

### Problem Summary
The codebase has a sophisticated configuration system (`BaseConfig`, `RuntimeConfig`, `field`, `env_field`) but most config classes bypass it by implementing manual `from_env()` methods with direct `os.getenv()` calls. This creates:
- Code duplication across config classes
- Inconsistent parsing and validation
- Unused field metadata (`env_var` declarations are ignored)
- No centralized environment variable handling

### Affected Files
- `src/provide/foundation/logger/config/logging.py` - 50+ manual `os.getenv()` calls
- `src/provide/foundation/logger/config/telemetry.py` - 20+ manual `os.getenv()` calls  
- `src/provide/foundation/transport/config.py` - 10+ manual `os.getenv()` calls
- `src/provide/foundation/streams/console.py` - Direct `os.getenv()` for flags
- `src/provide/foundation/streams/core.py` - Direct `os.getenv()` for testing

## Implementation Checklist

### Phase 1: Refactor Config Classes to Use RuntimeConfig
- [ ] Change `LoggingConfig` to inherit from `RuntimeConfig`
- [ ] Change `TelemetryConfig` to inherit from `RuntimeConfig`
- [ ] Change `TransportConfig` to inherit from `RuntimeConfig`
- [ ] Change `HTTPConfig` to inherit from `RuntimeConfig`
- [ ] Remove manual `from_env()` implementations from all config classes
- [ ] Update callers to use `RuntimeConfig.from_env()` method

### Phase 2: Enhance Field Declarations
- [ ] Add converter for `module_levels` field (parse "module1:LEVEL,module2:LEVEL")
- [ ] Add converter for `rate_limit_per_logger` field (parse "logger1:rate:capacity")
- [ ] Remove unused emoji sets fields (`enabled_emoji_sets`, `custom_emoji_sets`, `user_defined_emoji_sets`) - these are parsed but never used
- [ ] Add validators to fields instead of post-validation
- [ ] Remove manual parsing logic from `from_env()` methods

### Phase 3: Centralize Simple Environment Checks
- [ ] Create `StreamConfig` class for console settings
- [ ] Add fields for `NO_COLOR`, `FORCE_COLOR`, `CLICK_TESTING`
- [ ] Replace direct `os.getenv()` calls in streams modules
- [ ] Register `StreamConfig` with ConfigManager

### Phase 4: Leverage Config Manager
- [ ] Register all configs at application startup
- [ ] Replace direct config instantiation with manager-based loading
- [ ] Add config watching capabilities
- [ ] Enable hot-reloading for development

## Specific Changes for Phase 1 & 2

### 1. LoggingConfig Changes

**Current Structure:**
```python
@define(slots=True, repr=False)
class LoggingConfig(BaseConfig):
    default_level: LogLevelStr = field(
        default="WARNING",
        env_var="PROVIDE_LOG_LEVEL",
        description="Default logging level",
    )
    # ... more fields ...
    
    @classmethod
    def from_env(cls, strict: bool = True) -> "LoggingConfig":
        config_dict = {}
        if level := os.getenv("PROVIDE_LOG_LEVEL"):  # Manual parsing
            # ... validation logic ...
        # ... 200+ lines of manual env var reading ...
        return cls(**config_dict)
```

**New Structure:**
```python
@define(slots=True, repr=False)
class LoggingConfig(RuntimeConfig):
    default_level: LogLevelStr = field(
        default="WARNING",
        env_var="PROVIDE_LOG_LEVEL",
        converter=parse_log_level,  # Add converter
        validator=validate_log_level,  # Add validator
        description="Default logging level",
    )
    
    module_levels: dict[str, LogLevelStr] = field(
        factory=lambda: {},
        env_var="PROVIDE_LOG_MODULE_LEVELS",
        converter=parse_module_levels,  # Custom parser for "mod1:LEVEL,mod2:LEVEL"
        description="Per-module log levels",
    )
    
    # NOTE: The emoji sets fields (enabled_emoji_sets, custom_emoji_sets, 
    # user_defined_emoji_sets) have been REMOVED as they were parsed but
    # never actually used in the logger implementation - dead code cleanup
    # ... other fields with proper converters ...
    
    # No more from_env() method needed! RuntimeConfig handles it
```

### 2. TelemetryConfig Changes

**Current Structure:**
```python
@define(slots=True, repr=False)
class TelemetryConfig(BaseConfig):
    service_name: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_NAME",
        description="Service name for telemetry",
    )
    # ... more fields ...
    
    @classmethod
    def from_env(cls, strict: bool = True) -> "TelemetryConfig":
        config_dict = {}
        service_name = os.getenv("OTEL_SERVICE_NAME") or os.getenv("PROVIDE_SERVICE_NAME")
        # ... manual parsing ...
        return cls(**config_dict)
```

**New Structure:**
```python
@define(slots=True, repr=False)
class TelemetryConfig(RuntimeConfig):
    service_name: str | None = field(
        default=None,
        env_var="PROVIDE_SERVICE_NAME",
        converter=lambda v: v or os.getenv("OTEL_SERVICE_NAME"),  # Handle fallback
        description="Service name for telemetry",
    )
    
    logging: LoggingConfig = field(
        factory=lambda: LoggingConfig.from_env(),  # Nested config loading
        description="Logging configuration"
    )
    
    trace_sample_rate: float = field(
        default=1.0,
        env_var="OTEL_TRACE_SAMPLE_RATE",
        converter=parse_float_with_validation,  # Parse and validate 0.0-1.0
        validator=validate_sample_rate,
        description="Sampling rate for traces (0.0 to 1.0)",
    )
    # ... other fields with proper converters ...
```

### 3. New Converter Functions (to be added)

```python
# In src/provide/foundation/config/converters.py

def parse_log_level(value: str) -> LogLevelStr:
    """Parse and validate log level string."""
    level = value.upper()
    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(f"Invalid log level: {value}")
    return level

def parse_module_levels(value: str) -> dict[str, LogLevelStr]:
    """Parse module:LEVEL,module:LEVEL format."""
    result = {}
    for pair in value.split(","):
        if ":" in pair:
            module, level = pair.split(":", 1)
            result[module.strip()] = parse_log_level(level.strip())
    return result

# NOTE: Removed parse_comma_list and parse_json_emoji_sets as the emoji sets
# functionality is not actually implemented - these fields were dead code

def parse_rate_limits(value: str) -> dict[str, tuple[float, float]]:
    """Parse logger:rate:capacity format."""
    result = {}
    for item in value.split(","):
        parts = item.split(":")
        if len(parts) == 3:
            logger, rate, capacity = parts
            result[logger.strip()] = (float(rate), float(capacity))
    return result
```

### 4. Usage After Refactor

```python
# Old way (manual):
config = LoggingConfig.from_env()

# New way (automatic via RuntimeConfig):
config = LoggingConfig.from_env()  # Uses RuntimeConfig.from_env()
# or with prefix:
config = LoggingConfig.from_env(prefix="PROVIDE_LOG")

# The RuntimeConfig.from_env() automatically:
# 1. Reads env vars based on field metadata
# 2. Applies converters for type conversion
# 3. Runs validators
# 4. Tracks source as ConfigSource.ENV
# 5. Handles file:// secrets
```

## Benefits

1. **Code Reduction**: Removes ~500+ lines of manual env var parsing
2. **Consistency**: All configs use the same loading mechanism
3. **Type Safety**: Converters ensure proper types at field level
4. **Validation**: Validators run automatically during loading
5. **Maintainability**: Adding new env vars only requires field declaration
6. **Features**: Automatic support for file-based secrets, source tracking, etc.

## Testing Requirements

- [ ] Ensure all existing tests pass with new implementation
- [ ] Add tests for custom converters
- [ ] Test nested config loading (TelemetryConfig with LoggingConfig)
- [ ] Test validation error handling
- [ ] Test file-based secret loading
- [ ] Test precedence when multiple sources exist

## Migration Notes

- No breaking changes for users - `from_env()` calls still work
- Internal implementation becomes cleaner and more maintainable
- Field metadata is now actually used instead of being decorative
- Validation happens at parse time, not after object creation