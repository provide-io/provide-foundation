# Environment Variables

Complete reference for configuring provide.foundation through environment variables.

## Overview

provide.foundation uses environment variables with the **`PROVIDE_`** prefix for all user-facing configuration. This ensures:

- 🏷️ **Clear namespace ownership** - All provide.io tools use this prefix
- 🔍 **Easy discovery** - `env | grep PROVIDE_` shows all settings
- 🚀 **Container-friendly** - Perfect for Docker, Kubernetes, cloud platforms
- 🔒 **Security-first** - Secrets never touch config files

## Variable Reference

### Logging Configuration

Control how provide.foundation formats and outputs logs.

| Variable | Type | Default | Values | Description |
|----------|------|---------|---------|-------------|
| `PROVIDE_LOG_LEVEL` | string | `INFO` | `TRACE`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | Minimum log level to output |
| `PROVIDE_LOG_FORMAT` | string | `pretty` | `pretty`, `json`, `compact`, `plain` | Output format for logs |
| `PROVIDE_LOG_FILE` | path | None | Any valid file path | Write logs to this file |
| `PROVIDE_LOG_STDERR` | bool | `true` | `true`, `false` | Output to stderr (in addition to file if set) |
| `PROVIDE_LOG_COLORS` | bool | auto | `true`, `false`, `auto` | Enable colored output (auto detects TTY) |
| `PROVIDE_NO_COLOR` | bool | `false` | `true`, `false` | Disable all color output (overrides LOG_COLORS) |
| `PROVIDE_NO_EMOJI` | bool | `false` | `true`, `false` | Disable emoji in output |
| `PROVIDE_LOG_TIMESTAMP` | bool | `true` | `true`, `false` | Include timestamps in logs |
| `PROVIDE_LOG_TIMESTAMP_FORMAT` | string | `ISO8601` | `ISO8601`, `UNIX`, `RELATIVE` | Timestamp format |
| `PROVIDE_LOG_CALLER_INFO` | bool | `false` | `true`, `false` | Include file:line in logs |

#### Examples

```bash
# Development environment
export PROVIDE_LOG_LEVEL=DEBUG
export PROVIDE_LOG_FORMAT=pretty
export PROVIDE_NO_EMOJI=false
export PROVIDE_LOG_COLORS=true

# Production environment
export PROVIDE_LOG_LEVEL=INFO
export PROVIDE_LOG_FORMAT=json
export PROVIDE_NO_EMOJI=true
export PROVIDE_LOG_FILE=/var/log/app.log

# CI/CD environment
export PROVIDE_LOG_LEVEL=WARNING
export PROVIDE_LOG_FORMAT=compact
export PROVIDE_NO_COLOR=true
```

### Semantic Layers

Configure domain-specific telemetry interfaces.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_SEMANTIC_LAYERS` | bool | `true` | Enable semantic layer processing |
| `PROVIDE_ENABLED_LAYERS` | list | all | Comma-separated list of layers to enable |
| `PROVIDE_LAYER_TIMEOUT_MS` | int | `10` | Maximum processing time per layer |
| `PROVIDE_LAYER_EMOJI` | bool | `true` | Add emoji based on semantic context |
| `PROVIDE_LAYER_VALIDATION` | bool | `true` | Validate field types and values |
| `PROVIDE_LAYER_CACHE_SIZE` | int | `1024` | LRU cache size for emoji lookups |

#### Layer Names

- `http` - Web request/response telemetry
- `database` - Database query telemetry  
- `llm` - LLM/AI operations telemetry
- `task_queue` - Background task telemetry
- `cache` - Cache operations telemetry
- `messaging` - Message queue telemetry

#### Examples

```bash
# Enable only specific layers
export PROVIDE_ENABLED_LAYERS=http,database

# Disable emoji in production
export PROVIDE_LAYER_EMOJI=false

# Increase timeout for complex processing
export PROVIDE_LAYER_TIMEOUT_MS=50
```

### OpenTelemetry Integration

Seamlessly extend provide.foundation with OTEL.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_OTEL_ENDPOINT` | url | None | OTEL collector endpoint |
| `PROVIDE_OTEL_SERVICE_NAME` | string | app name | Service identifier |
| `PROVIDE_OTEL_TRACES` | bool | `true` | Export distributed traces |
| `PROVIDE_OTEL_METRICS` | bool | `true` | Export metrics |
| `PROVIDE_OTEL_LOGS` | bool | `false` | Export logs via OTEL |
| `PROVIDE_OTEL_HEADERS` | dict | None | Headers for OTEL exporter (JSON) |
| `PROVIDE_OTEL_TIMEOUT_MS` | int | `10000` | Export timeout |
| `PROVIDE_OTEL_BATCH_SIZE` | int | `512` | Batch size for exports |
| `PROVIDE_OTEL_COMPRESSION` | string | `gzip` | `none`, `gzip` |
| `PROVIDE_OTEL_SAMPLE_RATE` | float | `1.0` | Trace sampling rate (0.0-1.0) |

#### Examples

```bash
# Basic OTEL setup
export PROVIDE_OTEL_ENDPOINT=http://otel-collector:4317
export PROVIDE_OTEL_SERVICE_NAME=my-service

# Production with sampling
export PROVIDE_OTEL_ENDPOINT=https://otel.prod:4317
export PROVIDE_OTEL_SAMPLE_RATE=0.1
export PROVIDE_OTEL_COMPRESSION=gzip

# With authentication
export PROVIDE_OTEL_HEADERS='{"Authorization": "Bearer token123"}'
```

### Performance Tuning

Optimize provide.foundation for your workload.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_MAX_PROCESSORS` | int | CPU count | Number of processor threads |
| `PROVIDE_BUFFER_SIZE` | int | `1000` | Log buffer size |
| `PROVIDE_FLUSH_INTERVAL_MS` | int | `1000` | Buffer flush interval |
| `PROVIDE_ASYNC_LOGGING` | bool | `false` | Use async log processing |
| `PROVIDE_BATCH_SIZE` | int | `100` | Batch size for async processing |
| `PROVIDE_DROP_ON_OVERFLOW` | bool | `false` | Drop logs if buffer full |
| `PROVIDE_LAZY_INIT` | bool | `true` | Defer initialization until first use |

#### Examples

```bash
# High-throughput application
export PROVIDE_ASYNC_LOGGING=true
export PROVIDE_BUFFER_SIZE=10000
export PROVIDE_BATCH_SIZE=500

# Low-latency application
export PROVIDE_ASYNC_LOGGING=false
export PROVIDE_FLUSH_INTERVAL_MS=100

# Memory-constrained environment
export PROVIDE_BUFFER_SIZE=100
export PROVIDE_DROP_ON_OVERFLOW=true
```

### Application Context

Set application-wide context values.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_APP_NAME` | string | None | Application identifier |
| `PROVIDE_APP_VERSION` | string | None | Application version |
| `PROVIDE_APP_ENVIRONMENT` | string | `development` | Environment name |
| `PROVIDE_APP_REGION` | string | None | Deployment region |
| `PROVIDE_APP_INSTANCE_ID` | string | hostname | Instance identifier |
| `PROVIDE_APP_BUILD_ID` | string | None | Build/commit identifier |

#### Examples

```bash
# Kubernetes deployment
export PROVIDE_APP_NAME=payment-service
export PROVIDE_APP_VERSION=$(cat VERSION)
export PROVIDE_APP_ENVIRONMENT=production
export PROVIDE_APP_REGION=us-west-2
export PROVIDE_APP_INSTANCE_ID=$HOSTNAME
export PROVIDE_APP_BUILD_ID=$GIT_COMMIT

# Docker Compose
export PROVIDE_APP_NAME=web-api
export PROVIDE_APP_ENVIRONMENT=staging
export PROVIDE_APP_INSTANCE_ID=$(hostname)
```

### Configuration Management

Control how configuration is loaded and processed.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_CONFIG_FILE` | path | None | Primary config file location |
| `PROVIDE_CONFIG_DIR` | path | `./config` | Directory to search for configs |
| `PROVIDE_PROFILE` | string | `default` | Configuration profile to load |
| `PROVIDE_CONFIG_RELOAD` | bool | `false` | Watch for config file changes |
| `PROVIDE_CONFIG_VALIDATE` | bool | `true` | Validate configuration on load |
| `PROVIDE_CONFIG_STRICT` | bool | `false` | Fail on unknown config keys |

#### Examples

```bash
# Load specific config file
export PROVIDE_CONFIG_FILE=/etc/myapp/config.yaml

# Use profile-based configs
export PROVIDE_PROFILE=production

# Enable hot-reload in development
export PROVIDE_CONFIG_RELOAD=true
export PROVIDE_PROFILE=development
```

### CLI Configuration

Configure CLI-specific behavior.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PROVIDE_CLI_WIDTH` | int | auto | Terminal width for output |
| `PROVIDE_CLI_PAGER` | string | `less` | Pager for long output |
| `PROVIDE_CLI_EDITOR` | string | `$EDITOR` | Editor for interactive commands |
| `PROVIDE_JSON_OUTPUT` | bool | `false` | Force JSON output for all commands |
| `PROVIDE_TABLE_FORMAT` | string | `pretty` | `pretty`, `csv`, `json`, `plain` |
| `PROVIDE_CONFIRM_DESTRUCTIVE` | bool | `true` | Require confirmation for destructive operations |
| `PROVIDE_VERBOSE` | int | `0` | Verbosity level (0-3) |

#### Examples

```bash
# CI/CD automation
export PROVIDE_JSON_OUTPUT=true
export PROVIDE_CONFIRM_DESTRUCTIVE=false

# Interactive development
export PROVIDE_CLI_WIDTH=120
export PROVIDE_TABLE_FORMAT=pretty
export PROVIDE_VERBOSE=2
```

## Type Coercion

Environment variables are strings by default. provide.foundation automatically converts them to the appropriate type.

### Boolean Values

Any of these values are recognized (case-insensitive):

- **True**: `true`, `yes`, `on`, `1`, `enabled`, `enable`
- **False**: `false`, `no`, `off`, `0`, `disabled`, `disable`

```bash
export PROVIDE_NO_EMOJI=true     # Boolean: true
export PROVIDE_NO_EMOJI=YES      # Boolean: true
export PROVIDE_NO_EMOJI=1        # Boolean: true
export PROVIDE_NO_EMOJI=false    # Boolean: false
export PROVIDE_NO_EMOJI=0        # Boolean: false
```

### Numeric Values

Integers and floats are automatically parsed:

```bash
export PROVIDE_BUFFER_SIZE=5000           # Integer: 5000
export PROVIDE_SAMPLE_RATE=0.25          # Float: 0.25
export PROVIDE_LAYER_TIMEOUT_MS=50       # Integer: 50
```

### List Values

Comma-separated values become lists:

```bash
export PROVIDE_ENABLED_LAYERS=http,database,llm
# Parsed as: ["http", "database", "llm"]

export PROVIDE_OTEL_HEADERS='{"key": "value"}'
# Parsed as: {"key": "value"}
```

### Path Values

Paths are expanded and validated:

```bash
export PROVIDE_LOG_FILE=~/logs/app.log
# Expands to: /home/user/logs/app.log

export PROVIDE_CONFIG_FILE=$HOME/.config/app.yaml
# Expands to: /home/user/.config/app.yaml
```

## Precedence Rules

Configuration sources are applied in this order (highest to lowest priority):

1. **Runtime arguments** - Direct function parameters
2. **Environment variables** - `PROVIDE_*` variables
3. **Configuration files** - YAML/JSON/TOML files
4. **Defaults** - Built-in defaults

```python
from provide.foundation import logger
from provide.foundation.config import Config

# Environment variable takes precedence
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

# This is overridden by the env var above
config = Config(log_level="INFO")

# This overrides everything
logger.setup(level="ERROR")  # Runtime argument wins
```

## Platform-Specific Notes

### Docker

Use ENV or ARG directives:

```dockerfile
# Build-time configuration
ARG LOG_LEVEL=INFO
ENV PROVIDE_LOG_LEVEL=${LOG_LEVEL}

# Runtime configuration
ENV PROVIDE_LOG_FORMAT=json
ENV PROVIDE_NO_COLOR=true
ENV PROVIDE_APP_ENVIRONMENT=container
```

### Kubernetes

Use ConfigMaps and Secrets:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  PROVIDE_LOG_LEVEL: "INFO"
  PROVIDE_LOG_FORMAT: "json"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
data:
  PROVIDE_OTEL_HEADERS: <base64-encoded-json>
```

### AWS Lambda

Set in function configuration:

```python
# serverless.yml
functions:
  app:
    environment:
      PROVIDE_LOG_LEVEL: INFO
      PROVIDE_LOG_FORMAT: json
      PROVIDE_APP_ENVIRONMENT: lambda
      PROVIDE_APP_REGION: ${aws:region}
```

### GitHub Actions

```yaml
env:
  PROVIDE_LOG_LEVEL: DEBUG
  PROVIDE_NO_COLOR: true
  PROVIDE_JSON_OUTPUT: true
```

### Shell Scripts

```bash
#!/bin/bash
# Source environment
source .env

# Or inline
PROVIDE_LOG_LEVEL=DEBUG \
PROVIDE_LOG_FORMAT=pretty \
python app.py
```

## Security Considerations

### Secrets Management

Never put secrets in:
- Configuration files (tracked in git)
- Docker images (use runtime env)
- Log output (use redaction)

Always use:
- Environment variables for secrets
- Secret management systems (Vault, AWS Secrets Manager)
- Encrypted environment files (.env.encrypted)

```bash
# ❌ Bad: Secret in config file
# config.yaml
api_key: sk-1234567890abcdef

# ✅ Good: Secret in environment
export PROVIDE_API_KEY=${SECRET_API_KEY}
```

### Variable Validation

provide.foundation validates environment variables:

```python
# Automatic validation
try:
    config = Config.from_env()
except ValidationError as e:
    # PROVIDE_LOG_LEVEL=INVALID
    # Error: Invalid log level: INVALID
    print(f"Configuration error: {e}")
```

## Debugging Configuration

### Show Current Configuration

```bash
# Show all PROVIDE_ variables
env | grep ^PROVIDE_ | sort

# Show with values hidden
env | grep ^PROVIDE_ | sed 's/=.*/=***/' | sort
```

### Debug Loading

```bash
# Enable debug output for config loading
export FOUNDATION_DEBUG=true  # Internal debug flag
python -c "from provide.foundation.config import Config; Config.from_env()"
```

### Test Configuration

```python
from provide.foundation.config import validate_env

# Check all environment variables
errors = validate_env()
if errors:
    for error in errors:
        print(f"Config error: {error}")
```

## Internal/Debug Variables

For debugging provide.foundation itself (not for production use):

| Variable | Description | Use Case |
|----------|-------------|----------|
| `FOUNDATION_DEBUG` | Enable internal debug logging | Troubleshooting config loading |
| `FOUNDATION_SHOW_EMOJI_MATRIX` | Display emoji mapping table | Debug emoji assignments |
| `FOUNDATION_TRACE_PROCESSORS` | Trace log processor chain | Debug log pipeline |
| `FOUNDATION_PROFILE` | Enable profiling output | Performance analysis |

⚠️ **Warning**: Internal variables may change between versions.

## Best Practices

### 1. Use .env Files for Development

```bash
# .env.development
PROVIDE_LOG_LEVEL=DEBUG
PROVIDE_LOG_FORMAT=pretty
PROVIDE_NO_EMOJI=false

# Load in shell
source .env.development
```

### 2. Document Required Variables

```bash
# .env.example
# Required
PROVIDE_APP_NAME=       # Your app name
PROVIDE_OTEL_ENDPOINT=  # OTEL collector URL

# Optional
PROVIDE_LOG_LEVEL=INFO  # Default: INFO
```

### 3. Validate Early

```python
# app.py
from provide.foundation.config import Config

def main():
    # Fail fast on bad config
    try:
        config = Config.from_env()
    except Exception as e:
        print(f"Fatal: {e}")
        sys.exit(1)
```

### 4. Use Profiles for Environments

```bash
# Development
export PROVIDE_PROFILE=development

# Staging  
export PROVIDE_PROFILE=staging

# Production
export PROVIDE_PROFILE=production
```

## Migration from Other Systems

### From Python logging

```python
# Old (Python logging)
LOGLEVEL=DEBUG

# New (provide.foundation)
PROVIDE_LOG_LEVEL=DEBUG
```

### From structlog

```python
# Old (structlog)
STRUCTLOG_PROCESSORS=json

# New (provide.foundation)
PROVIDE_LOG_FORMAT=json
```

### From pyvider

```python
# Old (pyvider)
PYVIDER_DEBUG=true

# New (provide.foundation)
PROVIDE_LOG_LEVEL=DEBUG
```

## Next Steps

- 📁 [Configuration Files](files.md) - File-based configuration
- ⚙️ [Runtime Configuration](runtime.md) - Dynamic configuration
- 📚 [Best Practices](best-practices.md) - Production recommendations
- 🏠 [Back to Config Guide](index.md)