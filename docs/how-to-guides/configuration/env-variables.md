# How to Configure with Environment Variables

Foundation provides two complementary APIs for working with environment variables, each designed for different use cases. This guide shows you how to use both effectively.

## Quick Comparison

Foundation provides two complementary APIs for working with environment variables:

### When to Use Each API

| Use Case | API to Use | Why | Example |
|----------|-----------|-----|---------|
| **Simple scripts** | Direct Access (`utils.environment`) | Quick one-off reads, no class overhead | `get_bool("DEBUG")` |
| **Utility scripts** | Direct Access | Minimal boilerplate for throwaway code | `get_int("PORT")` |
| **Application config** | Structured Config (`config.env`) | Type safety, validation, IDE autocomplete | `BaseConfig.from_env()` |
| **Secret management** | Structured Config | Built-in `file://` prefix support | `password: str = env_field(...)` |
| **Complex validation** | Structured Config | Use attrs validators for constraints | Custom validators on fields |
| **Shared configuration** | Structured Config | Pass config objects between modules | Single source of truth |

### Decision Flow

```
Do you need configuration for the entire app?
├─ Yes → Use Structured Config (BaseConfig + env_field)
│   └─ Benefits: Type safety, validation, IDE support
│
└─ No → Is this a quick script or one-off read?
    ├─ Yes → Use Direct Access (get_bool, get_int, etc.)
    │   └─ Benefits: Less boilerplate, faster to write
    │
    └─ No → Use Structured Config anyway for consistency
        └─ Benefits: Easier to refactor later
```

## Direct Environment Variable Access

Use this for simple, one-off environment variable access with automatic type coercion.

### Basic Usage

```python
from provide.foundation.utils.environment import get_bool, get_int, get_str, get_list

# Boolean values
debug = get_bool("DEBUG", default=False)
# Accepts: "true", "1", "yes", "on" (case-insensitive)

# Integer values
port = get_int("PORT", default=8080)

# String values
api_key = get_str("API_KEY", required=True)
# Raises EnvironmentError if not set

# List values (comma-separated)
allowed_hosts = get_list("ALLOWED_HOSTS", default=["localhost"])
# "host1,host2,host3" → ["host1", "host2", "host3"]
```

### Available Functions

#### `get_bool(name, default=None, required=False)`

Parse boolean environment variables:

```python
from provide.foundation.utils.environment import get_bool

# Accepts various formats (case-insensitive):
# True:  "true", "1", "yes", "on", "y", "t"
# False: "false", "0", "no", "off", "n", "f", ""

enable_feature = get_bool("ENABLE_FEATURE", default=False)
debug_mode = get_bool("DEBUG")  # None if not set
strict_mode = get_bool("STRICT_MODE", required=True)  # Error if not set
```

#### `get_int(name, default=None, required=False)`

Parse integer environment variables:

```python
from provide.foundation.utils.environment import get_int

port = get_int("PORT", default=8080)
max_connections = get_int("MAX_CONNECTIONS", default=100)
timeout = get_int("TIMEOUT_SECONDS", required=True)
```

#### `get_float(name, default=None, required=False)`

Parse floating-point environment variables:

```python
from provide.foundation.utils.environment import get_float

timeout = get_float("TIMEOUT", default=30.0)
threshold = get_float("THRESHOLD", default=0.95)
```

#### `get_str(name, default=None, required=False)`

Get string environment variables:

```python
from provide.foundation.utils.environment import get_str

api_key = get_str("API_KEY", required=True)
app_name = get_str("APP_NAME", default="my-app")
database_url = get_str("DATABASE_URL")
```

#### `get_list(name, default=None, separator=",", required=False)`

Parse comma-separated lists:

```python
from provide.foundation.utils.environment import get_list

# Default comma separator
allowed_hosts = get_list("ALLOWED_HOSTS", default=["localhost"])
# "host1,host2,host3" → ["host1", "host2", "host3"]

# Custom separator
paths = get_list("SEARCH_PATHS", separator=":", default=["/usr/bin"])
# "/bin:/usr/bin:/usr/local/bin" → ["/bin", "/usr/bin", "/usr/local/bin"]
```

#### `get_dict(name, default=None, required=False)`

Parse key=value pairs:

```python
from provide.foundation.utils.environment import get_dict

# "key1=value1,key2=value2"
config = get_dict("CONFIG_PARAMS", default={})
# → {"key1": "value1", "key2": "value2"}
```

#### `get_path(name, default=None, required=False)`

Get filesystem paths:

```python
from provide.foundation.utils.environment import get_path

data_dir = get_path("DATA_DIR", default="/var/data")
config_file = get_path("CONFIG_FILE", required=True)
```

#### `require(name)`

Require an environment variable (raises if missing):

```python
from provide.foundation.utils.environment import require

# Shorthand for get_str(name, required=True)
api_key = require("API_KEY")
```

### Error Handling

```python
from provide.foundation.utils.environment import get_str, EnvironmentError

try:
    api_key = get_str("API_KEY", required=True)
except EnvironmentError as e:
    logger.error("missing_required_env_var", var_name="API_KEY")
    raise
```

## Structured Configuration Classes

Use this for building type-safe, validated configuration objects with file-based secret support.

### Understanding field() vs env_field()

Foundation provides two ways to declare fields in configuration classes. Both work identically - choose based on your preference and use case.

#### Quick Decision Guide

```
Are you building user-facing configuration classes?
├─ Yes → Use env_field() (clearer intent, less verbose)
│   └─ Example: AppConfig, DatabaseConfig, ServiceConfig
│
└─ No → Are you building internal Foundation-style configs?
    ├─ Yes → Use field() (matches Foundation's patterns)
    │   └─ Example: Custom LoggingConfig, TelemetryConfig extensions
    │
    └─ Either works → Choose based on code style preference
```

#### The Two Approaches

**1. `env_field()` - Convenience wrapper (recommended for user code):**
```python
from provide.foundation.config import env_field

api_key: str = env_field(env_var="API_KEY")
port: int = env_field(env_var="PORT", default=8080)
```

**2. `field()` - Direct approach (used in Foundation internals):**
```python
from provide.foundation.config.base import field

default_level: str = field(
    default="INFO",
    env_var="PROVIDE_LOG_LEVEL",
    description="Logging level"
)
```

**Key Points:**
- Both work identically - `env_field()` internally calls `field()`
- `env_field()` is more concise for simple use cases
- `field()` supports additional metadata like descriptions
- Foundation's own config classes use `field()` directly
- Use whichever feels more readable for your code

### Basic Example

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define

@define
class AppConfig(BaseConfig):
    # Required field
    api_key: str = env_field(env_var="API_KEY")

    # Optional with default
    debug: bool = env_field(env_var="DEBUG", default=False)

    # Port with default
    port: int = env_field(env_var="PORT", default=8080)

    # Optional string
    app_name: str = env_field(env_var="APP_NAME", default="my-app")

# Load from environment
config = AppConfig.from_env()

print(config.api_key)  # From API_KEY env var
print(config.port)     # From PORT env var or default 8080
```

### Type Validation

attrs automatically validates types:

```python
@define
class DatabaseConfig(BaseConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(env_var="DB_PORT", default=5432)
    ssl_enabled: bool = env_field(env_var="DB_SSL", default=False)
    timeout: float = env_field(env_var="DB_TIMEOUT", default=30.0)

# Load from environment
config = DatabaseConfig.from_env()

# Type errors are caught:
# export DB_PORT="not_a_number"
# config = DatabaseConfig.from_env()  # ← Raises validation error
```

### Secret Management with `file://` Prefix

Foundation supports reading secrets from files using the `file://` prefix:

```python
@define
class SecureConfig(BaseConfig):
    # Can be set directly or via file
    api_key: str = env_field(env_var="API_KEY")

    # Password from file
    database_password: str = env_field(env_var="DB_PASSWORD")

# Set via environment:
# export API_KEY="direct-key-value"
# export DB_PASSWORD="file:///run/secrets/db_password"

config = SecureConfig.from_env()
print(config.api_key)           # "direct-key-value"
print(config.database_password)  # Contents of /run/secrets/db_password
```

This is especially useful for:
- **Docker secrets**: `/run/secrets/secret_name`
- **Kubernetes secrets**: Mounted as files
- **AWS Secrets Manager**: Via file mounts
- **HashiCorp Vault**: Via file-based secret injection

### Complex Configuration

```python
from attrs import define, field
from provide.foundation.config import BaseConfig, env_field

@define
class ServerConfig(BaseConfig):
    # Server settings
    host: str = env_field(env_var="SERVER_HOST", default="0.0.0.0")
    port: int = env_field(env_var="SERVER_PORT", default=8000)
    workers: int = env_field(env_var="SERVER_WORKERS", default=4)

    # TLS settings
    tls_enabled: bool = env_field(env_var="TLS_ENABLED", default=False)
    tls_cert_file: str | None = env_field(env_var="TLS_CERT_FILE", default=None)
    tls_key_file: str | None = env_field(env_var="TLS_KEY_FILE", default=None)

    # Timeouts
    read_timeout: float = env_field(env_var="READ_TIMEOUT", default=30.0)
    write_timeout: float = env_field(env_var="WRITE_TIMEOUT", default=30.0)

    # Additional validation with attrs
    @port.validator
    def _validate_port(self, attribute, value):
        if not (1 <= value <= 65535):
            raise ValueError(f"Port must be between 1 and 65535, got {value}")

    @workers.validator
    def _validate_workers(self, attribute, value):
        if value < 1:
            raise ValueError(f"Workers must be at least 1, got {value}")

config = ServerConfig.from_env()
```

### Nested Configuration

```python
@define
class DatabaseConfig(BaseConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(env_var="DB_PORT", default=5432)
    name: str = env_field(env_var="DB_NAME", default="mydb")

@define
class RedisConfig(BaseConfig):
    host: str = env_field(env_var="REDIS_HOST", default="localhost")
    port: int = env_field(env_var="REDIS_PORT", default=6379)

@define
class ApplicationConfig(BaseConfig):
    app_name: str = env_field(env_var="APP_NAME", default="my-app")
    debug: bool = env_field(env_var="DEBUG", default=False)

    # Nested configs - loaded manually
    database: DatabaseConfig = field(factory=lambda: DatabaseConfig.from_env())
    redis: RedisConfig = field(factory=lambda: RedisConfig.from_env())

config = ApplicationConfig.from_env()
print(config.database.host)  # localhost
print(config.redis.port)     # 6379
```

## Common Patterns

### Script Configuration

For simple scripts, use direct access:

```python
#!/usr/bin/env python3
from provide.foundation.utils.environment import get_bool, get_int, get_str
from provide.foundation import logger

# Parse configuration
debug = get_bool("DEBUG", default=False)
batch_size = get_int("BATCH_SIZE", default=100)
data_dir = get_str("DATA_DIR", required=True)

# Configure logging
if debug:
    logger.info("debug_mode_enabled")

# Run script
logger.info("script_started", batch_size=batch_size, data_dir=data_dir)
# ... script logic ...
```

### Application Configuration

For applications, use structured config:

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define

@define
class AppConfig(BaseConfig):
    # Application settings
    environment: str = env_field(env_var="ENVIRONMENT", default="development")
    debug: bool = env_field(env_var="DEBUG", default=False)
    log_level: str = env_field(env_var="LOG_LEVEL", default="INFO")

    # Database
    database_url: str = env_field(env_var="DATABASE_URL", required=True)

    # API settings
    api_timeout: float = env_field(env_var="API_TIMEOUT", default=30.0)
    api_retries: int = env_field(env_var="API_RETRIES", default=3)

# Initialize application
config = AppConfig.from_env()

# Configure Foundation
from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

telemetry_config = TelemetryConfig(
    service_name="my-app",
    logging=LoggingConfig(
        default_level=config.log_level,
        logger_name_emoji_prefix_enabled=not config.environment == "production",
        das_emoji_prefix_enabled=not config.environment == "production"
    )
)

get_hub().initialize_foundation(telemetry_config)
```

### Production Secrets

```python
@define
class ProductionConfig(BaseConfig):
    # Public configuration
    app_name: str = env_field(env_var="APP_NAME", default="my-app")
    environment: str = env_field(env_var="ENVIRONMENT", default="production")

    # Secrets via files
    database_password: str = env_field(env_var="DB_PASSWORD")
    api_key: str = env_field(env_var="API_KEY")
    jwt_secret: str = env_field(env_var="JWT_SECRET")

# Docker/Kubernetes secrets mounted as files:
# export DB_PASSWORD="file:///run/secrets/db_password"
# export API_KEY="file:///run/secrets/api_key"
# export JWT_SECRET="file:///run/secrets/jwt_secret"

config = ProductionConfig.from_env()
```

### Environment-Specific Defaults

```python
@define
class EnvironmentAwareConfig(BaseConfig):
    environment: str = env_field(env_var="ENVIRONMENT", default="development")

    # Computed defaults based on environment
    @property
    def debug(self) -> bool:
        return self.environment != "production"

    @property
    def log_level(self) -> str:
        return "DEBUG" if self.debug else "INFO"

    @property
    def use_emoji(self) -> bool:
        return self.environment == "development"

from provide.foundation import get_hub, LoggingConfig, TelemetryConfig

config = EnvironmentAwareConfig.from_env()

# Configure based on environment
telemetry_config = TelemetryConfig(
    logging=LoggingConfig(
        default_level=config.log_level,
        logger_name_emoji_prefix_enabled=config.use_emoji,
        das_emoji_prefix_enabled=config.use_emoji
    )
)

get_hub().initialize_foundation(telemetry_config)
```

## Testing with Environment Variables

### Direct Access Testing

```python
import os
import pytest
from provide.foundation.utils.environment import get_bool, get_str

def test_environment_parsing(monkeypatch):
    # Set test environment variables
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_KEY", "test-key")

    assert get_bool("DEBUG") is True
    assert get_str("API_KEY") == "test-key"

def test_missing_required_var():
    from provide.foundation.utils.environment import get_str, EnvironmentError

    with pytest.raises(EnvironmentError):
        get_str("MISSING_VAR", required=True)
```

### Structured Config Testing

```python
import pytest
from provide.foundation.config import BaseConfig, env_field
from attrs import define

@define
class TestConfig(BaseConfig):
    api_key: str = env_field(env_var="API_KEY")
    debug: bool = env_field(env_var="DEBUG", default=False)

def test_config_loading(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("DEBUG", "true")

    config = TestConfig.from_env()

    assert config.api_key == "test-key"
    assert config.debug is True
```

## Best Practices

### ✅ DO: Use Descriptive Environment Variable Names

```python
# ✅ Good: Clear, descriptive names
DATABASE_URL = get_str("DATABASE_URL")
MAX_CONNECTIONS = get_int("MAX_CONNECTIONS")
ENABLE_FEATURE_X = get_bool("ENABLE_FEATURE_X")

# ❌ Bad: Ambiguous names
URL = get_str("URL")
MAX = get_int("MAX")
FEATURE = get_bool("FEATURE")
```

### ✅ DO: Use Structured Config for Applications

```python
# ✅ Good: Type-safe, validated configuration
@define
class AppConfig(BaseConfig):
    database_url: str = env_field(env_var="DATABASE_URL", required=True)
    port: int = env_field(env_var="PORT", default=8080)

# ❌ Bad: Direct access everywhere
database_url = get_str("DATABASE_URL", required=True)
port = get_int("PORT", default=8080)
```

### ✅ DO: Validate Configuration Early

```python
# ✅ Good: Load and validate config at startup
config = AppConfig.from_env()  # Validates immediately

# ❌ Bad: Lazy loading in critical paths
def handle_request():
    port = get_int("PORT")  # May fail during request handling
```

### ✅ DO: Use `file://` for Secrets

```python
# ✅ Good: Secrets from files
password: str = env_field(env_var="DB_PASSWORD")
# export DB_PASSWORD="file:///run/secrets/db_password"

# ❌ Bad: Secrets in environment directly (visible in process list)
# export DB_PASSWORD="my-secret-password"
```

### ❌ DON'T: Mix Configuration Methods

```python
# ❌ Bad: Mixing both approaches inconsistently
debug = get_bool("DEBUG")  # Direct access
config = AppConfig.from_env()  # Structured config

# ✅ Good: Choose one approach and stick with it
config = AppConfig.from_env()
debug = config.debug
```

## Next Steps

- **[File-Based Config](file-config.md)**: Load configuration from YAML/TOML files
- **[Secret Management](secrets.md)**: Advanced secret handling patterns
- **[Architecture](../../explanation/architecture.md)**: Understand the configuration system

---

**Tip**: Start with direct access for scripts, but migrate to structured config as your application grows. The type safety and validation are worth the small upfront cost.
