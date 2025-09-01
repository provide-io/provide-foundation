# 📚 API Reference

## Configuration API

This document provides a detailed reference for the data classes used in the programmatic configuration of `provide.foundation`.

### Core Functions

#### `setup_telemetry(config: TelemetryConfig | None = None)`

This is the main function for applying configuration to the telemetry system. It should be called once at application startup.

*   **Parameters**:
    *   `config` (`TelemetryConfig` | `None`): A `TelemetryConfig` instance containing your desired configuration. If `None`, the system will initialize from environment variables.

*   **Behavior**:
    *   If called with a `config` object, that configuration is used exclusively.
    *   If called with `None`, or if not called at all (lazy initialization), the system will build its configuration from environment variables.
    *   The function is thread-safe and ensures that initialization happens only once.

### `TelemetryConfig`

This is the top-level data class for all telemetry configuration.

```python
@define(kw_only=True, auto_attribs=True, frozen=True, slots=True)
class TelemetryConfig:
    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)
```

*   **`service_name`** (`str` | `None`)
    *   **Description**: A name for your application or service, which will be included as a `service.name` field in all log records.
    *   **Default**: `None`
    *   **Environment Variable**: `FOUNDATION_SERVICE_NAME` or `OTEL_SERVICE_NAME`

*   **`logging`** (`LoggingConfig`)
    *   **Description**: A nested `LoggingConfig` object containing all logging-specific settings.
    *   **Default**: A default `LoggingConfig` instance.

*   **`globally_disabled`** (`bool`)
    *   **Description**: If `True`, completely disables all telemetry output. This provides a global kill-switch.
    *   **Default**: `False`
    *   **Environment Variable**: `FOUNDATION_TELEMETRY_DISABLED` (set to `"true"`)

### `LoggingConfig`

This data class holds all configuration options related to the logging system.

```python
@define(kw_only=True, auto_attribs=True, frozen=True, slots=True)
class LoggingConfig:
    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=dict)
    console_formatter: Literal["key_value", "json"] = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)
    enabled_semantic_layers: list[str] = field(factory=list)
    custom_semantic_layers: list[SemanticLayer] = field(factory=list)
```

*   **`default_level`** (`LogLevelStr`)
    *   **Description**: The default log level for all loggers. Messages below this level will be discarded.
    *   **Type**: `Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]`
    *   **Default**: `"DEBUG"`
    *   **Environment Variable**: `FOUNDATION_LOG_LEVEL`

*   **`module_levels`** (`dict[str, LogLevelStr]`)
    *   **Description**: A dictionary to set different log levels for specific modules. The keys are dot-separated module names, and the values are the desired log level.
    *   **Default**: `{}`
    *   **Environment Variable**: `FOUNDATION_LOG_MODULE_LEVELS` (e.g., `"noisy_lib:WARNING,app.db:INFO"`)

*   **`console_formatter`** (`Literal["key_value", "json"]`)
    *   **Description**: The output format for the console.
        *   `key_value`: A human-readable format (e.g., `message key=value`).
        *   `json`: A machine-readable format where each log is a JSON object.
    *   **Default**: `"key_value"`
    *   **Environment Variable**: `FOUNDATION_LOG_CONSOLE_FORMATTER`

*   **`logger_name_emoji_prefix_enabled`** (`bool`)
    *   **Description**: If `True`, prepends a unique emoji based on the logger's name.
    *   **Default**: `True`
    *   **Environment Variable**: `FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED` (set to `"false"` to disable)

*   **`das_emoji_prefix_enabled`** (`bool`)
    *   **Description**: If `True`, prepends emojis based on active Semantic Layers or the DAS fallback (`domain`, `action`, `status`).
    *   **Default**: `True`
    *   **Environment Variable**: `FOUNDATION_LOG_DAS_EMOJI_ENABLED` (set to `"false"` to disable)

*   **`omit_timestamp`** (`bool`)
    *   **Description**: If `True`, removes the timestamp from the log output. This can be useful if the log aggregator adds its own timestamp.
    *   **Default**: `False`
    *   **Environment Variable**: `FOUNDATION_LOG_OMIT_TIMESTAMP` (set to `"true"`)

*   **`enabled_semantic_layers`** (`list[str]`)
    *   **Description**: A list of strings containing the names of built-in semantic layers to activate (e.g., `"http"`, `"database"`).
    *   **Default**: `[]`
    *   **Environment Variable**: `FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS` (e.g., `"http,database"`)

*   **`custom_semantic_layers`** (`list[SemanticLayer]`)
    *   **Description**: A list of custom `SemanticLayer` objects to activate. This is how you enable your own application-specific layers.
    *   **Default**: `[]`
    *   **Environment Variable**: Not recommended. This is best handled programmatically.

---

Next, learn about the data classes used to define semantic layers in the [**Semantic Layers API**](./semantic-layers.md).
