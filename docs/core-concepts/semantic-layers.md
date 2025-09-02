# 🏛️ Core Concepts

## Semantic Layers: Logging with Meaning

Semantic Layers are the heart of `provide.foundation`'s advanced logging capabilities. They provide an extensible, schema-driven way to define structured logging conventions and their corresponding emoji representations for specific domains (like HTTP, Databases, or LLMs).

They allow you to move beyond generic `info` or `debug` messages to logging rich, domain-specific events with a shared, understood vocabulary.

### Why Use Semantic Layers?

1.  **Consistency**: Ensures that everyone on your team logs the same type of event (e.g., an incoming HTTP request) with the same structure and key names.
2.  **Automatic Context**: They can automatically add relevant emoji prefixes based on the content of the log, making your logs instantly scannable.
3.  **Discoverability**: They serve as documentation for the logging conventions within your application.
4.  **Extensibility**: You can easily create your own layers to fit the specific domain of your application.

### How They Work

When you enable a semantic layer, you are telling `provide.foundation` to watch for log events that contain specific keys. When a log call includes keys that match a field in an active semantic layer, the library automatically:

1.  **Adds a Semantic Emoji Prefix**: Based on the values of the keys you provided, a meaningful emoji prefix is constructed and prepended to your log message.
2.  **Namespaces the Context**: The keys are organized into a clear, namespaced structure in the final log output (especially when using the JSON formatter).

### Built-in Semantic Layers

`provide.foundation` comes with several pre-built layers for common use cases. To use them, you simply need to enable them in your configuration.

**Example: Enabling the `http` and `database` layers**

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    logging=LoggingConfig(enabled_semantic_layers=["http", "database"])
)
setup_telemetry(config)
```

#### The `http` Layer

Use this layer for logging HTTP server or client requests.

*   **Key Fields**: `http.method`, `http.status_code`, `http.url`, `http.response_time_ms`
*   **Example**:
    ```python
    from provide.foundation import logger

    logger.info(
        "API request processed",
        **{
            "http.method": "GET",
            "http.status_code": 200,
            "http.url": "/api/v1/users",
        }
    )
    ```
*   **Output**:
    ```
    [➡️][✅] API request processed http.url=/api/v1/users
    ```
    The `[➡️]` comes from the `http.method` (`GET`) and `[✅]` comes from the `http.status_code` (200-299 range).

#### The `database` Layer

Use this layer for logging database queries and operations.

*   **Key Fields**: `db.system`, `db.operation`, `db.statement`, `db.outcome`
*   **Example**:
    ```python
    logger.info(
        "User query executed",
        **{
            "db.system": "postgresql",
            "db.operation": "query",
            "db.outcome": "success",
        }
    )
    ```
*   **Output**:
    ```
    [🗄️][🔍][✅] User query executed
    ```

### The Domain-Action-Status (DAS) Fallback

What happens if a log event doesn't match any active semantic layer? It falls back to the classic **Domain-Action-Status (DAS)** pattern.

This is a simple yet powerful convention that allows you to add semantic meaning to any log message by providing up to three special keyword arguments:

*   `domain`: The area or component of the system the log belongs to.
*   `action`: The specific operation being performed.
*   `status`: The outcome of the operation.

**Example:**

```python
logger.info(
    "User authentication successful",
    domain="auth",      # Corresponds to the 🔑 emoji
    action="login",     # Corresponds to the ➡️ emoji
    status="success",   # Corresponds to the ✅ emoji
    user_id="usr_456"
)
```

**Output:**

```
[🔑][➡️][✅] User authentication successful user_id='usr_456'
```

The DAS pattern ensures that even without formal semantic layers, you can still produce richly annotated and visually parsable logs.

---

Next, learn more about the visual parsing system that powers all of this in [**The Emoji System**](./emoji-system.md).
