# Environment Variables

Learn how to configure Foundation using environment variables.

## Overview

Foundation can be configured entirely through environment variables, making it ideal for containerized deployments and twelve-factor apps.

## Quick Reference

| Variable | Purpose | Default |
|----------|---------|---------|
| `PROVIDE_LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `PROVIDE_SERVICE_NAME` | Service identifier | Auto-detected |
| `PROVIDE_LOG_FORMAT` | Output format (console, json) | `console` |
| `PROVIDE_LOG_MODULE_LEVELS` | Per-module log levels | None |

## Basic Configuration

```bash
# Set log level
export PROVIDE_LOG_LEVEL=DEBUG

# Set service name
export PROVIDE_SERVICE_NAME=my-app

# Use JSON logging
export PROVIDE_LOG_FORMAT=json
```

## Module-Specific Log Levels

Control logging for specific modules:

```bash
# Suppress asyncio debug logs, allow requests debug
export PROVIDE_LOG_MODULE_LEVELS="asyncio:WARNING,urllib3:ERROR,httpx:DEBUG"
```

## Using Environment Variables in Code

For simple one-off variable access:

```python
from provide.foundation.utils.environment import get_bool, get_int, get_str

# Simple access with type coercion
debug = get_bool("DEBUG", default=False)
port = get_int("PORT", default=8080)
api_key = get_str("API_KEY", required=True)
```

## Structured Configuration Classes

For application-wide configuration:

```python
from provide.foundation.config import BaseConfig, env_field
from attrs import define

@define
class AppConfig(BaseConfig):
    """Application configuration from environment."""

    database_url: str = env_field(
        env_var="DATABASE_URL",
        default="postgresql://localhost/myapp"
    )

    api_timeout: int = env_field(
        env_var="API_TIMEOUT",
        default=30
    )

    debug_mode: bool = env_field(
        env_var="DEBUG",
        default=False
    )

# Load from environment
config = AppConfig.from_env()
```

## Secret File Support

Read secrets from files (useful for Kubernetes secrets):

```bash
# Instead of exposing the secret directly
export DB_PASSWORD="file:///run/secrets/db_password"
```

```python
@define
class DatabaseConfig(BaseConfig):
    password: str = env_field(env_var="DB_PASSWORD")
    # Will read from /run/secrets/db_password if value starts with "file://"
```

## Development vs Production

Use `.env` files for development:

```bash
# .env.development
PROVIDE_LOG_LEVEL=DEBUG
PROVIDE_LOG_FORMAT=console
DATABASE_URL=postgresql://localhost/myapp_dev

# .env.production
PROVIDE_LOG_LEVEL=INFO
PROVIDE_LOG_FORMAT=json
DATABASE_URL=file:///run/secrets/database_url
```

## Next Steps

- **[File-Based Config](file-config.md)** - Load from YAML/JSON files
- **[Secret Management](secrets.md)** - Secure secret handling
- **[API Reference: Config](../../reference/provide/foundation/config/index.md)** - Complete config API

---

**See also:** [examples/configuration/02_env_variables.py](https://github.com/provide-io/provide-foundation/blob/main/examples/configuration/02_env_variables.py)
