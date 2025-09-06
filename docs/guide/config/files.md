# Configuration Files

Load provide.foundation configuration from YAML, JSON, or TOML files.

## Overview

Configuration files provide a structured way to manage settings across environments. provide.foundation supports:

- 📄 **YAML** - Human-friendly, perfect for hand-editing
- 📊 **JSON** - Machine-readable, ideal for automation
- ⚙️ **TOML** - Clean syntax, great for simple configs
- 🎯 **Profile-based** - Environment-specific settings
- 🔄 **Hot-reload** - Dynamic configuration updates

## File Formats

### YAML Configuration

Most human-friendly format with comments support:

```yaml
# config.yaml - Main application configuration
logging:
  level: INFO           # Minimum log level
  format: pretty        # Output format
  no_emoji: false      # Enable emoji
  no_color: false      # Enable colors
  file: /var/log/app.log

emoji_sets:
  enabled: true
  layers:
    - http
    - database
    - llm
  timeout_ms: 10
  cache_size: 1024

otel:
  endpoint: http://otel-collector:4317
  service_name: my-service
  traces: true
  metrics: true
  sample_rate: 0.1

app:
  name: payment-service
  version: 1.2.3
  environment: production
  region: us-west-2
```

### JSON Configuration

Best for programmatic generation and CI/CD:

```json
{
  "logging": {
    "level": "INFO",
    "format": "json",
    "no_emoji": true,
    "no_color": true,
    "file": "/var/log/app.log"
  },
  "emoji_sets": {
    "enabled": true,
    "layers": ["http", "database"],
    "timeout_ms": 10
  },
  "otel": {
    "endpoint": "http://otel-collector:4317",
    "service_name": "my-service",
    "traces": true,
    "metrics": true
  },
  "app": {
    "name": "payment-service",
    "version": "1.2.3",
    "environment": "production"
  }
}
```

### TOML Configuration

Clean, minimal syntax:

```toml
# config.toml
[logging]
level = "INFO"
format = "pretty"
no_emoji = false
no_color = false

[emoji_sets]
enabled = true
layers = ["http", "database", "llm"]
timeout_ms = 10

[otel]
endpoint = "http://otel-collector:4317"
service_name = "my-service"
traces = true
metrics = true
sample_rate = 0.1

[app]
name = "payment-service"
version = "1.2.3"
environment = "production"
```

## Loading Configuration

### Basic Loading

```python
from provide.foundation.config import Config

# Auto-detect format from extension
config = Config.from_file("config.yaml")
config = Config.from_file("config.json")
config = Config.from_file("config.toml")

# Or specify format explicitly
config = Config.from_file("settings.conf", format="yaml")
```

### With Environment Override

Environment variables override file settings:

```python
import os
from provide.foundation.config import Config

# File sets level to INFO
config = Config.from_file("config.yaml")

# Environment overrides to DEBUG
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

# Final level is DEBUG (env wins)
final_config = config.merge_env()
```

### Multiple Config Files

Load and merge multiple configuration sources:

```python
from provide.foundation.config import Config

# Load base configuration
base = Config.from_file("config/base.yaml")

# Load environment-specific
env = Config.from_file("config/production.yaml")

# Merge (env overrides base)
config = base.merge(env)

# Apply environment variables last
config = config.merge_env()
```

## Profile-Based Configuration

### Single File with Profiles

```yaml
# config.yaml with multiple profiles
default:
  logging:
    level: INFO
    format: pretty

profiles:
  development:
    logging:
      level: DEBUG
      format: pretty
      no_emoji: false
    app:
      environment: development
      debug: true

  staging:
    logging:
      level: INFO
      format: json
    app:
      environment: staging
    otel:
      endpoint: http://staging-otel:4317

  production:
    logging:
      level: WARNING
      format: json
      no_emoji: true
    app:
      environment: production
    otel:
      endpoint: https://prod-otel:4317
      sample_rate: 0.1
```

Load specific profile:

```python
from provide.foundation.config import Config

# Via environment variable
os.environ["PROVIDE_PROFILE"] = "production"
config = Config.from_file("config.yaml")

# Or programmatically
config = Config.from_file("config.yaml", profile="production")
```

### Separate Files per Environment

```
config/
├── base.yaml           # Shared settings
├── development.yaml    # Dev overrides
├── staging.yaml        # Staging overrides
└── production.yaml     # Prod overrides
```

```python
from provide.foundation.config import Config
import os

# Determine environment
env = os.getenv("PROVIDE_APP_ENVIRONMENT", "development")

# Load base + environment
base = Config.from_file("config/base.yaml")
env_config = Config.from_file(f"config/{env}.yaml")

# Merge
config = base.merge(env_config)
```

## Configuration Schema

### Root Structure

```yaml
# Full configuration schema
logging:          # Logging configuration
  level: string   # Log level
  format: string  # Output format
  # ... more logging options

emoji_sets:  # Emoji set settings
  enabled: bool
  layers: list
  # ... more layer options

otel:            # OpenTelemetry settings
  endpoint: string
  service_name: string
  # ... more OTEL options

app:             # Application metadata
  name: string
  version: string
  # ... more app options

performance:     # Performance tuning
  buffer_size: int
  async_logging: bool
  # ... more performance options

cli:             # CLI-specific settings
  output_format: string
  confirm_destructive: bool
  # ... more CLI options
```

### Logging Section

```yaml
logging:
  # Core settings
  level: INFO              # TRACE|DEBUG|INFO|WARNING|ERROR|CRITICAL
  format: pretty           # pretty|json|compact|plain
  
  # Output control
  file: /var/log/app.log   # Log file path
  stderr: true             # Also log to stderr
  
  # Visual settings
  no_color: false          # Disable colors
  no_emoji: false          # Disable emoji
  
  # Timestamps
  timestamp: true          # Include timestamps
  timestamp_format: ISO8601 # ISO8601|UNIX|RELATIVE
  
  # Debug info
  caller_info: false       # Include file:line
  
  # Structured data
  extra_fields:            # Additional fields for all logs
    service: my-app
    datacenter: us-west-2
```

### Emoji Sets Section

```yaml
emoji_sets:
  enabled: true            # Enable layer processing
  
  layers:                  # Active layers
    - http
    - database
    - llm
    
  # Performance
  timeout_ms: 10           # Processing timeout
  cache_size: 1024         # Emoji cache size
  
  # Behavior
  emoji: true              # Add emoji prefixes
  validation: true         # Validate field types
  
  # Custom layers
  custom:
    - name: payment
      priority: 75
      fields:
        payment.method: string
        payment.amount: float
```

### OpenTelemetry Section

```yaml
otel:
  # Connection
  endpoint: http://otel-collector:4317
  headers:
    Authorization: Bearer token123
    
  # Service info
  service_name: my-service
  service_version: 1.2.3
  service_namespace: production
  
  # Export settings
  traces: true
  metrics: true
  logs: false
  
  # Performance
  timeout_ms: 10000
  batch_size: 512
  compression: gzip
  
  # Sampling
  sample_rate: 0.1         # 10% sampling
  sample_errors: 1.0       # Always sample errors
```

## Advanced Features

### Environment Variable Expansion

Use environment variables in config files:

```yaml
# config.yaml with env var expansion
logging:
  level: ${LOG_LEVEL:-INFO}           # Default to INFO
  file: ${LOG_PATH}/app.log           # Use LOG_PATH env var

otel:
  endpoint: ${OTEL_ENDPOINT}          # Required env var
  headers:
    Authorization: Bearer ${OTEL_TOKEN}

app:
  name: ${APP_NAME:-my-app}
  version: ${VERSION:-unknown}
  build_id: ${GIT_COMMIT}
```

### Include Files

Split configuration across multiple files:

```yaml
# main.yaml
!include logging.yaml
!include otel.yaml

app:
  name: my-service
```

```yaml
# logging.yaml
logging:
  level: INFO
  format: json
```

```yaml
# otel.yaml
otel:
  endpoint: http://otel-collector:4317
  service_name: my-service
```

### Conditional Configuration

```yaml
# config.yaml with conditionals
logging:
  level: !env
    production: WARNING
    staging: INFO
    default: DEBUG
    
  format: !env
    production: json
    default: pretty

otel: !if ${ENABLE_OTEL}
  endpoint: ${OTEL_ENDPOINT}
  service_name: ${SERVICE_NAME}
```

### Secret Management

```yaml
# config.yaml - references to secrets
database:
  host: ${DB_HOST}
  port: 5432
  username: ${DB_USER}
  password: !secret database/password  # From secret manager
  
api:
  key: !vault secret/api/key          # From HashiCorp Vault
  
aws:
  access_key: !aws-secret api-keys/access
  secret_key: !aws-secret api-keys/secret
```

Load with secret resolution:

```python
from provide.foundation.config import Config
from provide.foundation.secrets import SecretResolver

# Setup secret resolver
resolver = SecretResolver()
resolver.add_provider("vault", VaultProvider())
resolver.add_provider("aws-secret", AWSSecretsProvider())

# Load config with secret resolution
config = Config.from_file("config.yaml", secret_resolver=resolver)
```

## Hot Reload

Watch for configuration changes:

```python
from provide.foundation.config import Config, watch_config
from provide.foundation import logger

@watch_config("config.yaml")
def on_config_change(new_config: Config):
    """Handle configuration changes."""
    logger.info("config_reloaded", 
                level=new_config.logging.level)
    
    # Apply new configuration
    logger.set_level(new_config.logging.level)
    logger.set_format(new_config.logging.format)

# Or manually
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigReloader(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("config.yaml"):
            reload_config()

observer = Observer()
observer.schedule(ConfigReloader(), path=".", recursive=False)
observer.start()
```

## Validation

### Schema Validation

Define and validate configuration schema:

```python
from provide.foundation.config import Config, ConfigSchema
from pydantic import BaseModel, Field

class LoggingSchema(BaseModel):
    level: str = Field(regex="^(DEBUG|INFO|WARNING|ERROR)$")
    format: str = Field(regex="^(pretty|json|compact)$")
    file: str | None = None

class AppSchema(BaseModel):
    name: str = Field(min_length=1)
    version: str = Field(regex=r"^\d+\.\d+\.\d+$")

class ConfigSchema(BaseModel):
    logging: LoggingSchema
    app: AppSchema

# Validate on load
config = Config.from_file("config.yaml", schema=ConfigSchema)
```

### Custom Validators

```python
from provide.foundation.config import Config, validator

@validator("logging.level")
def validate_log_level(value: str) -> str:
    valid_levels = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]
    if value.upper() not in valid_levels:
        raise ValueError(f"Invalid log level: {value}")
    return value.upper()

@validator("otel.sample_rate")
def validate_sample_rate(value: float) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError("Sample rate must be between 0.0 and 1.0")
    return value

# Apply validators
config = Config.from_file("config.yaml", validators=[
    validate_log_level,
    validate_sample_rate
])
```

## Best Practices

### 1. Layer Configuration

```yaml
# base.yaml - Shared across all environments
logging:
  timestamp: true
  timestamp_format: ISO8601

app:
  name: my-service

# production.yaml - Production-specific
logging:
  level: WARNING
  format: json
  no_emoji: true

otel:
  endpoint: https://prod-otel:4317
  sample_rate: 0.1
```

### 2. Use Profiles for Environments

```yaml
# Single file with clear profile separation
profiles:
  development:
    logging:
      level: DEBUG
      format: pretty
    debug:
      enabled: true
      
  production:
    logging:
      level: WARNING
      format: json
    debug:
      enabled: false
```

### 3. Validate Early and Strictly

```python
# startup.py
from provide.foundation.config import Config, ValidationError

def load_config() -> Config:
    try:
        config = Config.from_file("config.yaml", strict=True)
        config.validate()
        return config
    except ValidationError as e:
        logger.error("config_invalid", error=str(e))
        sys.exit(1)
```

### 4. Document Configuration

```yaml
# config.yaml with inline documentation
logging:
  # Minimum log level to output
  # Options: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
  level: INFO
  
  # Output format for logs
  # Options: pretty (dev), json (prod), compact (CI)
  format: pretty
  
  # Log file path (optional)
  # Leave empty to disable file logging
  file: null
```

### 5. Secure Sensitive Data

```yaml
# Never commit secrets
database:
  host: localhost
  port: 5432
  username: ${DB_USER}        # From environment
  password: !secret db/pass   # From secret manager
  
# Use .gitignore
# config.local.yaml
# config.*.secret.yaml
```

## Migration Examples

### From Python logging

```ini
# Old: logging.ini
[loggers]
keys=root

[handlers]
keys=console

[formatters]
keys=simple

[logger_root]
level=INFO
handlers=console
```

```yaml
# New: config.yaml
logging:
  level: INFO
  format: pretty
  handlers:
    - console
```

### From Django Settings

```python
# Old: settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

```yaml
# New: config.yaml
logging:
  level: INFO
  format: pretty
  disable_existing: false
  handlers:
    - type: console
      stream: stderr
```

## Troubleshooting

### Config Not Loading

```python
from provide.foundation.config import Config
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Check file path
import os
print(f"Looking for: {os.path.abspath('config.yaml')}")
print(f"File exists: {os.path.exists('config.yaml')}")

# Load with verbose error handling
try:
    config = Config.from_file("config.yaml", verbose=True)
except Exception as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### Environment Variables Not Overriding

```python
# Check precedence
import os
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"

config = Config.from_file("config.yaml")
print(f"File level: {config.logging.level}")

config = config.merge_env()
print(f"After env merge: {config.logging.level}")
```

### Validation Errors

```python
from provide.foundation.config import Config, ValidationError

try:
    config = Config.from_file("config.yaml")
    config.validate()
except ValidationError as e:
    for error in e.errors:
        print(f"Field: {error.field}")
        print(f"Value: {error.value}")
        print(f"Error: {error.message}")
```

## Next Steps

- 🔧 [Runtime Configuration](runtime.md) - Dynamic configuration changes
- 🌍 [Environment Variables](environment.md) - Environment-based config
- 📚 [Best Practices](best-practices.md) - Production recommendations
- 🏠 [Back to Config Guide](index.md)