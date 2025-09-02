# 🏛️ Core Concepts

## Configuring the Logger

`provide.foundation` is designed to work beautifully out of the box, but it also offers a powerful and flexible configuration system for when you need more control. You can configure the logger using environment variables or directly in your code.

### Zero-Configuration Default

If you provide no configuration, the logger will run with a sensible set of defaults:

*   **Log Level**: `DEBUG`
*   **Formatter**: `key_value` (human-readable console format)
*   **Emoji Prefixes**: All emoji systems (logger name and semantic) are enabled.
*   **Semantic Layers**: No layers are enabled by default; the system relies on the [DAS fallback](./semantic-layers.md#the-domain-action-status-das-fallback).

!!! info "Perfect for Development"
    The zero-configuration setup is perfect for local development and debugging, as it provides maximum information out of the box.

### Method 1: Configuration via Environment Variables

For production environments, and for making quick changes without altering code, environment variables are the recommended method of configuration.

!!! tip "Production Best Practice"
    Using environment variables allows you to change log levels or verbosity in your production environment without needing to redeploy your application.

Here is a complete list of the available environment variables:

| Variable | Description | Default | Example |
|---|---|---|---|
| `FOUNDATION_SERVICE_NAME` | A name for your service, included in all log entries. | `None` | `my-api-service` |
| `FOUNDATION_TELEMETRY_DISABLED` | Set to `true` to disable all logging output globally. | `false` | `true` |
| `FOUNDATION_LOG_LEVEL` | The default log level for all loggers. | `DEBUG` | `INFO` |
| `FOUNDATION_LOG_MODULE_LEVELS` | A comma-separated list of `module:level` pairs for fine-grained control. | `""` | `noisy_lib:WARNING,auth_service:DEBUG` |
| `FOUNDATION_LOG_CONSOLE_FORMATTER` | The output format for the console. | `key_value` | `json` |
| `FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED` | Set to `false` to disable the logger-name-based emoji prefix. | `true` | `false` |
| `FOUNDATION_LOG_DAS_EMOJI_ENABLED` | Set to `false` to disable the semantic (DAS or Layer-based) emoji prefix. | `true` | `false` |
| `FOUNDATION_LOG_OMIT_TIMESTAMP` | Set to `true` to remove the timestamp from the output. | `false` | `true` |
| `FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS` | A comma-separated list of built-in semantic layers to activate. | `""` | `http,database,llm` |
| `FOUNDATION_SHOW_EMOJI_MATRIX` | Set to `true` to print a reference of all active emoji mappings on startup. | `false` | `true` |

### Method 2: Programmatic Configuration

For the most control and for complex or dynamic configurations, you can configure the logger directly in your code. 

!!! warning "Call Once at Startup"
    Programmatic configuration should be done once, at the very beginning of your application's lifecycle, before any other modules start logging. This ensures all log messages are handled consistently.

This method uses two main data classes:

*   `TelemetryConfig`: The top-level configuration object.
*   `LoggingConfig`: A nested object specifically for logging-related settings.

**Example:**

```python
# In your application's main entry point (e.g., main.py or app.py)
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

# 1. Create a LoggingConfig instance
logging_config = LoggingConfig(
    default_level="INFO",
    console_formatter="json",
    module_levels={
        "noisy_library.utils": "WARNING",
        "critical_component.io": "DEBUG",
    },
    enabled_semantic_layers=["http", "database"],
)

# 2. Create the main TelemetryConfig instance
telemetry_config = TelemetryConfig(
    service_name="my-awesome-app",
    logging=logging_config,
)

# 3. Apply the configuration
setup_telemetry(telemetry_config)
```

### Configuration Precedence

1.  **`setup_telemetry(config)` is called**: The programmatic configuration provided in the `config` object takes precedence and is used exclusively.
2.  **`setup_telemetry()` is called with no arguments**: The system will attempt to load configuration from environment variables.
3.  **No setup is called (lazy initialization)**: The first time `logger` is used, it will initialize itself by loading configuration from environment variables.

---

Now that you understand the core concepts, explore the [**Guides**](../guides/async-usage.md) for practical, real-world use cases.