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

