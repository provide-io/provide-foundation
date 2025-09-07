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

