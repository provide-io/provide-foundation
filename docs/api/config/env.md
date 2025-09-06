# Environment Configuration API

Environment variable loading with async secret support, type coercion, and file-based secret handling.

## Overview

The environment configuration module provides utilities for loading configuration from environment variables with support for:

- Async file-based secrets (Docker secrets, Kubernetes secrets)
- Automatic type parsing and conversion
- Prefix-based variable grouping
- Custom parsers for complex types
- Both sync and async loading methods

## Functions

### get_env_async(var_name, default, required, secret_file)

Get environment variable value with async file-based secret support.

```python
async def get_env_async(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """
    Get environment variable value with optional file-based secret support (async).
    
    Args:
        var_name: Environment variable name
        default: Default value if not found
        required: Whether the variable is required
        secret_file: Whether to support file:// prefix for secrets
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required and not found
    """
```

**Example:**
```python
# Basic usage
value = await get_env_async("DATABASE_URL", default="sqlite:///app.db")

# Required variable
api_key = await get_env_async("API_KEY", required=True)

# File-based secret
# Set: DATABASE_PASSWORD=file:///run/secrets/db_password
password = await get_env_async("DATABASE_PASSWORD")
```

### get_env(var_name, default, required, secret_file)

Synchronous version of environment variable retrieval.

```python
def get_env(
    var_name: str,
    default: str | None = None,
    required: bool = False,
    secret_file: bool = True,
) -> str | None:
    """
    Get environment variable value with optional file-based secret support (sync).
    
    This is a compatibility function that uses sync I/O.
    Prefer get_env_async for new code.
    """
```

### env_field(**kwargs)

Create a field descriptor that can be loaded from environment variables.

```python
def env_field(
    env_var: str | None = None,
    env_prefix: str | None = None,
    parser: Callable[[str], Any] | None = None,
    **kwargs,
) -> Any:
    """
    Create a field that can be loaded from environment variables.
    
    Args:
        env_var: Explicit environment variable name
        env_prefix: Prefix for environment variable
        parser: Custom parser function
        **kwargs: Additional field arguments
        
    Returns:
        Field descriptor
    """
```

**Example:**
```python
from provide.foundation.config.env import env_field

@define(frozen=True)
class DatabaseConfig(BaseConfig):
    host: str = env_field(env_var="DB_HOST", default="localhost")
    port: int = env_field(default=5432)  # Uses DATABASE_CONFIG_PORT
    url: str = env_field(parser=parse_database_url)
    timeout: float = env_field(parser=float, default=30.0)
```

## Classes

### RuntimeConfig

Base configuration class that supports loading from environment variables.

```python
class RuntimeConfig(BaseConfig):
    """
    Configuration that can be loaded from environment variables.
    All methods are async to support async secret fetching and validation.
    """
```

#### Class Methods

##### from_env(prefix, delimiter, case_sensitive)

Load configuration from environment variables synchronously.

```python
@classmethod
def from_env(
    cls: type[T],
    prefix: str = "",
    delimiter: str = "_",
    case_sensitive: bool = False,
) -> T:
    """
    Load configuration from environment variables synchronously.
    
    Args:
        prefix: Prefix for all environment variables
        delimiter: Delimiter between prefix and field name
        case_sensitive: Whether variable names are case-sensitive
        
    Returns:
        Configuration instance
    """
```

**Example:**
```python
@define(frozen=True)
class DatabaseConfig(RuntimeConfig):
    host: str = field(default="localhost")
    port: int = field(default=5432)
    username: str = field()
    password: str = field(sensitive=True)

# Environment variables:
# DATABASE_HOST=postgres.example.com
# DATABASE_PORT=5432
# DATABASE_USERNAME=app_user
# DATABASE_PASSWORD=secret123

config = DatabaseConfig.from_env(prefix="DATABASE")
print(config.host)  # postgres.example.com
```

##### from_env_async(prefix, delimiter, case_sensitive, use_async_secrets)

Load configuration from environment variables asynchronously.

```python
@classmethod
async def from_env_async(
    cls: type[T],
    prefix: str = "",
    delimiter: str = "_",
    case_sensitive: bool = False,
    use_async_secrets: bool = True,
) -> T:
    """
    Load configuration from environment variables asynchronously.
    
    Args:
        prefix: Prefix for all environment variables
        delimiter: Delimiter between prefix and field name
        case_sensitive: Whether variable names are case-sensitive
        use_async_secrets: Whether to use async I/O for file-based secrets
        
    Returns:
        Configuration instance
    """
```

**Features:**
- Parallel loading of file-based secrets using asyncio.gather
- Async I/O for better performance with multiple secrets
- Automatic type parsing based on field types

**Example:**
```python
# Environment with file-based secrets:
# DATABASE_PASSWORD=file:///run/secrets/db_password
# API_KEY=file:///run/secrets/api_key

config = await DatabaseConfig.from_env_async(prefix="DATABASE")
```

#### Instance Methods

##### to_env_dict(prefix, delimiter)

Convert configuration back to environment variable format.

```python
def to_env_dict(self, prefix: str = "", delimiter: str = "_") -> dict[str, str]:
    """
    Convert configuration to environment variable dictionary.
    
    Args:
        prefix: Prefix for all environment variables
        delimiter: Delimiter between prefix and field name
        
    Returns:
        Dictionary of environment variables
    """
```

**Example:**
```python
config = DatabaseConfig(host="localhost", port=5432, username="user")
env_vars = config.to_env_dict(prefix="DATABASE")

print(env_vars)
# {
#     'DATABASE_HOST': 'localhost',
#     'DATABASE_PORT': '5432', 
#     'DATABASE_USERNAME': 'user'
# }
```

## File-based Secrets

The environment system supports file-based secrets using the `file://` prefix:

### Secret Sources

```bash
# Docker Secrets
export DATABASE_PASSWORD=file:///run/secrets/db_password

# Kubernetes Secrets  
export API_KEY=file:///var/secrets/api-key

# Local files
export CONFIG_JSON=file:///etc/myapp/config.json
```

### Async vs Sync Loading

```python
# Async loading (preferred) - parallel file reads
config = await DatabaseConfig.from_env_async(prefix="APP")

# Sync loading - sequential file reads
config = DatabaseConfig.from_env(prefix="APP")
```

## Type Parsing

The system automatically parses environment variable strings into appropriate types:

### Built-in Parsers

```python
# Boolean parsing
debug: bool = field()  # "true", "1", "yes" → True

# Numeric types
port: int = field()       # "8080" → 8080
timeout: float = field()  # "30.5" → 30.5

# Collections
tags: list[str] = field()  # "tag1,tag2,tag3" → ["tag1", "tag2", "tag3"]
settings: dict = field()   # "key1=val1,key2=val2" → {"key1": "val1", "key2": "val2"}
```

### Custom Parsers

```python
from urllib.parse import urlparse

def parse_database_url(value: str) -> dict:
    """Parse DATABASE_URL into components."""
    parsed = urlparse(value)
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "database": parsed.path.lstrip("/"),
        "username": parsed.username,
        "password": parsed.password,
    }

@define(frozen=True)
class DatabaseConfig(RuntimeConfig):
    connection: dict = env_field(
        env_var="DATABASE_URL", 
        parser=parse_database_url
    )
```

## Error Handling

Environment loading can raise several exceptions:

```python
from provide.foundation.errors.config import ConfigurationError

try:
    config = DatabaseConfig.from_env(prefix="DB")
except ValueError as e:
    # Required environment variable not found
    print(f"Missing required env var: {e}")

try:
    config = await DatabaseConfig.from_env_async(prefix="DB")
except ValueError as e:
    # File-based secret could not be read
    print(f"Secret loading failed: {e}")
```

## Usage Examples

### Basic Environment Configuration

```python
@define(frozen=True)
class AppConfig(RuntimeConfig):
    name: str = field(default="myapp")
    debug: bool = field(default=False)
    port: int = field(default=8000)
    database_url: str = field()

# Environment:
# APP_NAME=production-app
# APP_DEBUG=true
# APP_PORT=9000
# APP_DATABASE_URL=postgresql://user:pass@db:5432/app

config = AppConfig.from_env(prefix="APP")
```

### Complex Configuration with Custom Parsing

```python
import json

@define(frozen=True)
class ServiceConfig(RuntimeConfig):
    services: list[str] = env_field(parser=lambda x: x.split(","))
    features: dict = env_field(parser=json.loads, default_factory=dict)
    timeout: float = env_field(parser=float, default=30.0)

# Environment:
# SERVICE_SERVICES=auth,user,billing
# SERVICE_FEATURES={"feature1": true, "feature2": false}
# SERVICE_TIMEOUT=45.5

config = ServiceConfig.from_env(prefix="SERVICE")
```

### Docker Secrets Integration

```python
@define(frozen=True)
class SecureConfig(RuntimeConfig):
    database_password: str = field(sensitive=True)
    api_key: str = field(sensitive=True)
    jwt_secret: str = field(sensitive=True)

# Docker Compose or Kubernetes:
# DATABASE_PASSWORD=file:///run/secrets/db_password
# API_KEY=file:///run/secrets/api_key
# JWT_SECRET=file:///run/secrets/jwt_secret

config = await SecureConfig.from_env_async()
```

### Configuration Export for Testing

```python
# Export current config as environment variables
env_vars = config.to_env_dict(prefix="TEST")

# Use in subprocess or containerized testing
import subprocess
result = subprocess.run(
    ["python", "test_script.py"],
    env={**os.environ, **env_vars}
)
```

## Related Documentation

- [Configuration Manager API](manager.md) - Centralized configuration management
- [Configuration Loaders API](loader.md) - Multi-source loading
- [Environment Configuration Guide](../../guide/config/environment.md) - Setup and best practices
- [Configuration Best Practices](../../guide/config/best-practices.md) - Container and deployment patterns