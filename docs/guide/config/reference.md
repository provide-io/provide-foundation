# Configuration Reference

Complete reference for all Foundation configuration options via environment variables, configuration objects, and files.

## Environment Variables

Foundation uses the `PROVIDE_*` prefix for all environment variables. OpenTelemetry-compatible variables (`OTEL_*`) are also supported where applicable.

### Core Service Configuration

#### `PROVIDE_SERVICE_NAME` / `OTEL_SERVICE_NAME`
**Type:** `string`  
**Default:** `None`  
**Description:** Service name for telemetry and logging identification.

```bash
export PROVIDE_SERVICE_NAME="my-api-service"
# Or OpenTelemetry compatible
export OTEL_SERVICE_NAME="my-api-service"
```

#### `PROVIDE_TELEMETRY_DISABLED`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Globally disable all telemetry features.

```bash
export PROVIDE_TELEMETRY_DISABLED=true
```

### Logging Configuration

#### `PROVIDE_LOG_LEVEL`
**Type:** `LogLevel`  
**Default:** `"DEBUG"`  
**Valid Values:** `"TRACE"`, `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`  
**Description:** Default logging level for all loggers.

```bash
export PROVIDE_LOG_LEVEL=INFO
```

#### `PROVIDE_LOG_MODULE_LEVELS`
**Type:** `string` (comma-separated key:value pairs)  
**Default:** `{}` (empty)  
**Format:** `module1:LEVEL,module2:LEVEL`  
**Description:** Per-module log level overrides.

```bash
export PROVIDE_LOG_MODULE_LEVELS="database:DEBUG,auth:WARNING,external:ERROR"
```

#### `PROVIDE_LOG_CONSOLE_FORMATTER`
**Type:** `ConsoleFormatter`  
**Default:** `"key_value"`  
**Valid Values:** `"key_value"`, `"json"`, `"compact"`, `"plain"`  
**Description:** Console output format.

```bash
# Pretty format with emojis (development)
export PROVIDE_LOG_CONSOLE_FORMATTER=key_value

# JSON format (production)  
export PROVIDE_LOG_CONSOLE_FORMATTER=json

# Compact format (CI/CD)
export PROVIDE_LOG_CONSOLE_FORMATTER=compact

# Plain format (debugging)
export PROVIDE_LOG_CONSOLE_FORMATTER=plain
```

#### `PROVIDE_LOG_OMIT_TIMESTAMP`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Omit timestamps from console output.

```bash
export PROVIDE_LOG_OMIT_TIMESTAMP=true
```

#### `PROVIDE_LOG_FILE`
**Type:** `string` (file path)  
**Default:** `None`  
**Description:** Path to log file for file-based logging.

```bash
export PROVIDE_LOG_FILE=/var/log/myapp.log
```

### Event Enrichment Configuration

#### `PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED`
**Type:** `boolean`  
**Default:** `true`  
**Description:** Enable visual markers based on logger names.

```bash
export PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED=false
```

#### `PROVIDE_LOG_DAS_EMOJI_ENABLED`
**Type:** `boolean`  
**Default:** `true`  
**Description:** Enable Domain-Action-Status visual markers.

```bash
export PROVIDE_LOG_DAS_EMOJI_ENABLED=false
```

#### `PROVIDE_LOG_ENABLED_EVENT_SETS`
**Type:** `string` (comma-separated list)  
**Default:** `[]` (empty)  
**Valid Values:** `"http"`, `"database"`, `"system"`  
**Description:** Event sets to enable for enrichment.

```bash
export PROVIDE_LOG_ENABLED_EVENT_SETS="http,database,system"
```

### Internal Configuration

#### `FOUNDATION_LOG_LEVEL`
**Type:** `LogLevel`  
**Default:** `"INFO"`  
**Description:** Log level for Foundation's internal setup logging.

```bash
export FOUNDATION_LOG_LEVEL=DEBUG
```

## Configuration Objects

### TelemetryConfig

Main configuration class for the telemetry system.

```python
from provide.foundation import TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="my-service",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json"
    ),
    globally_disabled=False
)
```

#### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `service_name` | `str \| None` | `None` | Service name for telemetry |
| `logging` | `LoggingConfig` | `LoggingConfig()` | Logging configuration |
| `globally_disabled` | `bool` | `False` | Disable all telemetry |

#### Methods

##### `from_env(strict: bool = True) -> TelemetryConfig`
Load configuration from environment variables.

```python
config = TelemetryConfig.from_env()
```

### LoggingConfig

Configuration specific to logging behavior.

```python
from provide.foundation import LoggingConfig

config = LoggingConfig(
    default_level="INFO",
    console_formatter="json",
    das_emoji_prefix_enabled=True,
    module_levels={"database": "DEBUG", "auth": "WARNING"}
)
```

#### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_level` | `LogLevelStr` | `"DEBUG"` | Default logging level |
| `module_levels` | `dict[str, LogLevelStr]` | `{}` | Per-module log levels |
| `console_formatter` | `ConsoleFormatterStr` | `"key_value"` | Console formatter |
| `logger_name_emoji_prefix_enabled` | `bool` | `True` | Logger name emoji prefixes |
| `das_emoji_prefix_enabled` | `bool` | `True` | DAS emoji prefixes |
| `omit_timestamp` | `bool` | `False` | Omit timestamps |
| `enabled_event_sets` | `list[str]` | `[]` | Enabled event sets |
| `log_file` | `Path \| None` | `None` | Log file path |

#### Methods

##### `from_env(strict: bool = True) -> LoggingConfig`
Load configuration from environment variables.

```python
config = LoggingConfig.from_env()
```

## Configuration Files

Foundation supports loading configuration from YAML, JSON, and TOML files.

### YAML Configuration

```yaml
# config.yaml
service_name: "my-service"
logging:
  default_level: "INFO"
  console_formatter: "json"
  module_levels:
    database: "DEBUG"
    auth: "WARNING"
  das_emoji_prefix_enabled: true
  enabled_event_sets:
    - "http"
    - "database"
```

### JSON Configuration

```json
{
  "service_name": "my-service",
  "logging": {
    "default_level": "INFO",
    "console_formatter": "json",
    "module_levels": {
      "database": "DEBUG",
      "auth": "WARNING"
    },
    "das_emoji_prefix_enabled": true,
    "enabled_event_sets": ["http", "database"]
  }
}
```

### TOML Configuration

```toml
service_name = "my-service"

[logging]
default_level = "INFO"
console_formatter = "json"
das_emoji_prefix_enabled = true
enabled_event_sets = ["http", "database"]

[logging.module_levels]
database = "DEBUG"
auth = "WARNING"
```

### Loading from Files

```python
from provide.foundation.config import FileConfigLoader

# Load YAML
loader = FileConfigLoader("config.yaml")
config = loader.load(TelemetryConfig)

# Load JSON
loader = FileConfigLoader("config.json")
config = loader.load(TelemetryConfig)

# Load TOML
loader = FileConfigLoader("config.toml")
config = loader.load(TelemetryConfig)
```

## Configuration Examples

### Development Environment

```bash
# Development configuration
export PROVIDE_SERVICE_NAME="myapp-dev"
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_CONSOLE_FORMATTER=key_value
export PROVIDE_LOG_DAS_EMOJI_ENABLED=true
export PROVIDE_LOG_ENABLED_EVENT_SETS="http,database"
```

### Production Environment

```bash
# Production configuration
export PROVIDE_SERVICE_NAME="myapp"
export PROVIDE_LOG_LEVEL=INFO
export PROVIDE_LOG_CONSOLE_FORMATTER=json
export PROVIDE_LOG_OMIT_TIMESTAMP=false
export PROVIDE_LOG_FILE=/var/log/myapp.log
export PROVIDE_LOG_DAS_EMOJI_ENABLED=false
```

### CI/CD Environment

```bash
# CI/CD configuration
export PROVIDE_SERVICE_NAME="myapp-ci"
export PROVIDE_LOG_LEVEL=WARNING
export PROVIDE_LOG_CONSOLE_FORMATTER=compact
export PROVIDE_LOG_DAS_EMOJI_ENABLED=false
export PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED=false
```

### Testing Environment

```bash
# Testing configuration
export PROVIDE_LOG_LEVEL=ERROR
export PROVIDE_LOG_CONSOLE_FORMATTER=plain
export PROVIDE_LOG_DAS_EMOJI_ENABLED=false
export PROVIDE_TELEMETRY_DISABLED=true  # Disable for unit tests
```

## Configuration Priority

Foundation loads configuration in the following order (later sources override earlier ones):

1. **Default values** - Built-in defaults
2. **Configuration files** - YAML/JSON/TOML files
3. **Environment variables** - `PROVIDE_*` and `OTEL_*` variables
4. **Runtime configuration** - Programmatically set values

### Example Priority

```python
# 1. Default: default_level="DEBUG"
# 2. File: default_level="INFO" (overrides default)
# 3. Environment: PROVIDE_LOG_LEVEL=WARNING (overrides file)
# 4. Runtime: LoggingConfig(default_level="ERROR") (overrides env)

# Final result: default_level="ERROR"
```

## Type Definitions

### LogLevelStr

Valid log level values:
- `"TRACE"` (5) - Most verbose
- `"DEBUG"` (10) - Diagnostic information
- `"INFO"` (20) - General information
- `"WARNING"` (30) - Warning messages
- `"ERROR"` (40) - Error messages  
- `"CRITICAL"` (50) - Critical failures

### ConsoleFormatterStr

Valid console formatter values:
- `"key_value"` - Pretty format with emojis (development)
- `"json"` - JSON format (production/analysis)
- `"compact"` - Compact format (CI/CD)
- `"plain"` - Plain format (debugging)

## Validation

Foundation validates all configuration values and provides clear error messages:

```python
from provide.foundation import LoggingConfig
from provide.foundation.errors import ConfigValidationError

try:
    config = LoggingConfig(default_level="INVALID")
except ConfigValidationError as e:
    print(f"Configuration error: {e}")
    # Configuration error: 'INVALID' is not a valid log level
```

## Environment Variable Parsing

Foundation provides intelligent parsing for environment variables:

### Boolean Values
Accepts: `"true"`, `"false"`, `"1"`, `"0"`, `"yes"`, `"no"` (case-insensitive)

```bash
export PROVIDE_LOG_DAS_EMOJI_ENABLED=True   # → true
export PROVIDE_LOG_DAS_EMOJI_ENABLED=FALSE  # → false  
export PROVIDE_LOG_DAS_EMOJI_ENABLED=1      # → true
export PROVIDE_LOG_DAS_EMOJI_ENABLED=no     # → false
```

### List Values
Comma-separated values:

```bash
export PROVIDE_LOG_ENABLED_EMOJI_SETS="http, database, llm"
# → ["http", "database", "llm"]
```

### Dictionary Values
Key-value pairs separated by commas:

```bash
export PROVIDE_LOG_MODULE_LEVELS="db:DEBUG,auth:WARNING,api:INFO"
# → {"db": "DEBUG", "auth": "WARNING", "api": "INFO"}
```

### JSON Values
Complex structures as JSON:

```bash
export PROVIDE_LOG_CUSTOM_EMOJI_SETS='[{"enabled": true, "das_mapping": {"test": "🧪"}}]'
```

## Best Practices

### 1. Environment-Specific Configuration

Use different configurations for each environment:

```bash
# .env.development
PROVIDE_LOG_LEVEL=DEBUG
PROVIDE_LOG_CONSOLE_FORMATTER=key_value
PROVIDE_LOG_DAS_EMOJI_ENABLED=true

# .env.production  
PROVIDE_LOG_LEVEL=INFO
PROVIDE_LOG_CONSOLE_FORMATTER=json
PROVIDE_LOG_FILE=/var/log/app.log
```

### 2. Service-Specific Settings

Configure per-service logging levels:

```bash
export PROVIDE_LOG_MODULE_LEVELS="database:DEBUG,http:INFO,auth:WARNING"
```

### 3. Container Deployment

Use environment variables for containerized deployments:

```dockerfile
# Dockerfile
ENV PROVIDE_SERVICE_NAME=myapp
ENV PROVIDE_LOG_LEVEL=INFO
ENV PROVIDE_LOG_CONSOLE_FORMATTER=json
```

### 4. Configuration Validation

Always validate configuration in startup code:

```python
from provide.foundation import setup_telemetry, TelemetryConfig

try:
    config = TelemetryConfig.from_env()
    setup_telemetry(config)
except Exception as e:
    logger.critical("Failed to initialize telemetry", error=str(e))
    raise
```

## Troubleshooting

### Common Issues

#### Invalid Log Level
```bash
# ❌ Invalid
export PROVIDE_LOG_LEVEL=VERBOSE

# ✅ Correct
export PROVIDE_LOG_LEVEL=DEBUG
```

#### Invalid Formatter
```bash
# ❌ Invalid
export PROVIDE_LOG_CONSOLE_FORMATTER=pretty

# ✅ Correct  
export PROVIDE_LOG_CONSOLE_FORMATTER=key_value
```

#### Module Level Format
```bash
# ❌ Invalid
export PROVIDE_LOG_MODULE_LEVELS="database=DEBUG"

# ✅ Correct
export PROVIDE_LOG_MODULE_LEVELS="database:DEBUG"
```

### Debugging Configuration

Enable Foundation's internal logging to debug configuration issues:

```bash
export FOUNDATION_LOG_LEVEL=DEBUG
```

## See Also

- [Configuration Best Practices](best-practices.md) - Configuration patterns and recommendations
- [Environment Setup](environment.md) - Environment-specific configuration guide
- [API Reference](../../api/config/api-index.md) - Complete configuration API documentation
- [Examples](../../getting-started/examples.md) - Working configuration examples