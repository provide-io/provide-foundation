# File-Based Configuration

Learn how to load configuration from YAML, JSON, and TOML files.

## Overview

Foundation supports loading configuration from files, making it easy to manage complex settings and environment-specific configurations.

## YAML Configuration

```yaml
# config.yaml
service:
  name: my-app
  version: 1.0.0

logging:
  level: INFO
  format: json

database:
  host: localhost
  port: 5432
  pool_size: 10
```

```python
from provide.foundation.config import ConfigManager

manager = ConfigManager()
config = await manager.load_yaml("config.yaml")

print(config["service"]["name"])  # "my-app"
```

## JSON Configuration

```json
{
  "service": {
    "name": "my-app",
    "version": "1.0.0"
  },
  "logging": {
    "level": "INFO",
    "format": "json"
  }
}
```

```python
config = await manager.load_json("config.json")
```

## TOML Configuration

```toml
[service]
name = "my-app"
version = "1.0.0"

[logging]
level = "INFO"
format = "json"

[database]
host = "localhost"
port = 5432
pool_size = 10
```

```python
config = await manager.load_toml("config.toml")
```

## Environment-Specific Files

```python
import os

environment = os.getenv("ENVIRONMENT", "development")
config_file = f"config.{environment}.yaml"

config = await manager.load_yaml(config_file)
```

## Merging Configurations

Combine multiple sources with environment variables taking precedence:

```python
# Load base config
base_config = await manager.load_yaml("config.base.yaml")

# Load environment-specific overrides
env_config = await manager.load_yaml(f"config.{environment}.yaml")

# Merge (env_config overrides base_config)
final_config = {**base_config, **env_config}
```

## Type-Safe Configuration

Use attrs classes for type safety:

```python
from attrs import define
from provide.foundation.config import BaseConfig, env_field

@define
class ServiceConfig(BaseConfig):
    name: str
    version: str
    port: int = 8000

# Load and validate
data = await manager.load_yaml("config.yaml")
service_config = ServiceConfig(**data["service"])
```

## Next Steps

- **[Environment Variables](env-variables.md)** - Environment-based config
- **[Secret Management](secrets.md)** - Secure configuration
- **[API Reference: Config](../../reference/provide/foundation/config/index.md)** - Complete config API

---

**See also:** [examples/configuration/03_config_management.py](https://github.com/provide-io/provide-foundation/blob/main/examples/configuration/03_config_management.py)
