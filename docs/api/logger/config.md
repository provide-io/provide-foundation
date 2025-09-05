# Logger Configuration API

Configuration classes for the Foundation logging system, defining telemetry and logging behavior.

## Classes

### LoggingConfig

Configuration specific to logging behavior within Foundation Telemetry.

```python
@define(frozen=True, slots=True)
class LoggingConfig:
    """Configuration specific to logging behavior within Foundation Telemetry."""
```

#### Fields

##### default_level: LogLevelStr
Default log level for all loggers.

```python
default_level: LogLevelStr = field(default="DEBUG")
```

**Valid values:** `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`, `"TRACE"`, `"NOTSET"`

##### module_levels: dict[str, LogLevelStr]
Per-module log level overrides.

```python
module_levels: dict[str, LogLevelStr] = field(factory=lambda: {})
```

**Example:**
```python
module_levels = {
    "requests": "WARNING",
    "urllib3": "ERROR",
    "myapp.db": "DEBUG"
}
```

##### console_formatter: ConsoleFormatterStr
Console output format.

```python
console_formatter: ConsoleFormatterStr = field(default="key_value")
```

**Valid values:** `"key_value"`, `"json"`

##### logger_name_emoji_prefix_enabled: bool
Enable emoji prefixes for logger names.

```python
logger_name_emoji_prefix_enabled: bool = field(default=True)
```

##### das_emoji_prefix_enabled: bool
Enable Domain-Action-Status emoji prefixes.

```python
das_emoji_prefix_enabled: bool = field(default=True)
```

##### omit_timestamp: bool
Omit timestamps from log output.

```python
omit_timestamp: bool = field(default=False)
```

##### enabled_emoji_sets: list[str]
List of enabled emoji set names.

```python
enabled_emoji_sets: list[str] = field(factory=lambda: [])
```

##### custom_emoji_sets: list[EmojiSetConfig]
Custom emoji set definitions.

```python
custom_emoji_sets: list[EmojiSetConfig] = field(factory=lambda: [])
```

##### user_defined_emoji_sets: list[CustomDasEmojiSet]
User-defined emoji sets for emoji sets.

```python
user_defined_emoji_sets: list[CustomDasEmojiSet] = field(factory=lambda: [])
```

#### Usage Example

```python
from provide.foundation.logger.config import LoggingConfig

config = LoggingConfig(
    default_level="INFO",
    module_levels={
        "requests": "WARNING",
        "myapp.database": "DEBUG"
    },
    console_formatter="json",
    das_emoji_prefix_enabled=True,
    omit_timestamp=False
)
```

### TelemetryConfig

Main configuration object for the Foundation Telemetry system.

```python
@define(frozen=True, slots=True)
class TelemetryConfig:
    """Main configuration object for the Foundation Telemetry system."""
```

#### Fields

##### service_name: str | None
Name of the service for telemetry identification.

```python
service_name: str | None = field(default=None)
```

##### logging: LoggingConfig
Logging-specific configuration.

```python
logging: LoggingConfig = field(factory=LoggingConfig)
```

##### globally_disabled: bool
Globally disable all telemetry.

```python
globally_disabled: bool = field(default=False)
```

#### Class Methods

##### from_env() -> TelemetryConfig
Create configuration from environment variables.

```python
@classmethod
def from_env(cls) -> "TelemetryConfig":
    """Creates a TelemetryConfig instance by parsing relevant environment variables."""
```

**Environment Variables:**
- `PROVIDE_SERVICE_NAME`: Service name
- `PROVIDE_LOG_LEVEL`: Default log level
- `PROVIDE_LOG_FORMAT`: Console formatter
- `PROVIDE_DISABLE_EMOJI`: Disable emoji prefixes
- `PROVIDE_DISABLE_TIMESTAMPS`: Omit timestamps
- `PROVIDE_GLOBALLY_DISABLED`: Disable all telemetry

#### Usage Examples

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Manual configuration
logging_config = LoggingConfig(
    default_level="INFO",
    console_formatter="json",
    das_emoji_prefix_enabled=False
)

config = TelemetryConfig(
    service_name="myapp",
    logging=logging_config,
    globally_disabled=False
)

# From environment variables
config = TelemetryConfig.from_env()

# Using in setup
from provide.foundation.core import setup_telemetry
setup_telemetry(config)
```

## Type Definitions

### LogLevelStr
Valid log level strings.

```python
LogLevelStr = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "TRACE", "NOTSET"]
```

### ConsoleFormatterStr
Valid console formatter strings.

```python
ConsoleFormatterStr = Literal["key_value", "json"]
```

## Environment Configuration

The `from_env()` method reads the following environment variables:

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `PROVIDE_SERVICE_NAME` | string | Service identifier | None |
| `PROVIDE_LOG_LEVEL` | LogLevelStr | Default log level | "DEBUG" |
| `PROVIDE_LOG_FORMAT` | ConsoleFormatterStr | Output format | "key_value" |
| `PROVIDE_DISABLE_EMOJI` | bool | Disable emoji prefixes | False |
| `PROVIDE_DISABLE_TIMESTAMPS` | bool | Omit timestamps | False |
| `PROVIDE_GLOBALLY_DISABLED` | bool | Disable all logging | False |
| `PROVIDE_MODULE_LOG_LEVELS` | string | Module levels (JSON) | {} |

**Example environment setup:**
```bash
export PROVIDE_SERVICE_NAME="myapp"
export PROVIDE_LOG_LEVEL="INFO"
export PROVIDE_LOG_FORMAT="json"
export PROVIDE_DISABLE_EMOJI="false"
export PROVIDE_MODULE_LOG_LEVELS='{"requests": "WARNING", "urllib3": "ERROR"}'
```

## Immutability

Both configuration classes are frozen and use slots for memory efficiency. To modify configurations, create new instances:

```python
# Create new config with updated values
import attrs

new_config = attrs.evolve(
    existing_config,
    service_name="updated-service",
    globally_disabled=False
)
```

## Related Documentation

- [FoundationLogger API](base.md) - Main logger interface
- [Environment Configuration Guide](/guide/config/environment/) - Environment setup
- [Configuration Best Practices](/guide/config/best-practices/) - Usage patterns