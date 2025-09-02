# `provide.foundation`: Beautiful, Performant, Structured Logging for Python

<p align="center">
  <img src="https://raw.githubusercontent.com/provide-io/provide-foundation/main/docs/assets/foundation-banner.png" alt="provide.foundation banner">
</p>

<p align="center">
    <a href="https://pypi.org/project/provide-foundation/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/provide-foundation.svg">
    </a>
    <a href="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml">
        <img alt="CI Status" src="https://github.com/provide-io/provide-foundation/actions/workflows/ci.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/provide-io/provide-foundation">
        <img src="https://codecov.io/gh/provide-io/provide-foundation/branch/main/graph/badge.svg"/>
    </a>
    <a href="https://github.com/provide-io/provide-foundation/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/provide-io/provide-foundation.svg">
    </a>
</p>

**`provide.foundation`** is a Python telemetry library, built on the robust `structlog`, that provides a beautiful, performant, and structured logging experience right out of the box. It is designed to make your logs not only machine-readable but also instantly scannable by human eyes, enhancing the developer experience in complex applications.

---

## ✨ Key Features

*   **🚀 Zero-Configuration Start**: Get beautiful, structured logs instantly without any setup.
*   **🎨 Emoji-Enhanced Visual Parsing**: Unique emoji prefixes based on logger names and semantic context make logs instantly scannable in a sea of text.
*   **🏛️ Semantic Logging**: Go beyond simple log levels with extensible Semantic Layers for domains like LLMs, HTTP, and Databases. Fall back to the classic Domain-Action-Status (DAS) pattern when needed.
*   **⚡ High Performance**: Benchmarked at over 14,000 messages per second with full semantic processing, ensuring it's ready for production loads.
*   **🔧 Flexible Configuration**: Configure via environment variables or programmatically for fine-grained control.
*   **🧑‍💻 Developer-Friendly**: Thread-safe, async-ready, and equipped with comprehensive type hints for a modern development workflow.

## 📦 Installation

Install `provide.foundation` using `pip` or your favorite package manager:

```bash
pip install provide-foundation
```

## 🚀 Quick Start

Getting started is as simple as importing the global `logger` and using it.

```python
# examples/01_quick_start.py
from provide.foundation import logger

def main():
    """A simple function to demonstrate logging."""
    logger.info("Application starting up")
    
    try:
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception(
            "An expected error occurred",
            error_details="Attempted to divide by zero",
            user_id="usr_123"
        )
    
    logger.info("Application shutting down")

if __name__ == "__main__":
    main()
```

Run this script, and you'll see beautifully formatted, structured output right in your console:

```
[▶️] Application starting up
[🔥] An expected error occurred error_details='Attempted to divide by zero' user_id='usr_123' exc_info=...
[▶️] Application shutting down
```

## 🏛️ Core Concepts

### 1. The Global Logger

For convenience, `provide.foundation` exposes a pre-configured, global logger instance named `logger`. You can import and use it anywhere in your application.

```python
from provide.foundation import logger

logger.debug("This is a debug message")
logger.info("User logged in", user_id=123, source="google_oauth")
logger.warning("Disk space is running low", free_space_gb=5)
logger.error("Failed to connect to database", db_host="prod.db.example.com")
```

### 2. Structured Logging

`provide.foundation` is built around the principle of structured logging. Instead of embedding variables in log messages, you pass them as keyword arguments. This makes your logs:
*   **Machine-readable**: Easily parsed, filtered, and indexed by log management systems (like Datadog, Splunk, or the ELK stack).
*   **Consistent**: Ensures the same event is always logged with the same structure.
*   **Rich with Context**: Carry detailed, queryable context with every event.

```python
# ❌ Anti-pattern: Unstructured logging
logger.info(f"User {user_id} from IP {ip_address} completed checkout for order {order_id}.")

# ✅ Best practice: Structured logging
logger.info(
    "Checkout complete",
    user_id=user_id,
    ip_address=ip_address,
    order_id=order_id,
)
```

### 3. Emoji-Enhanced Visual Parsing

A standout feature is the automatic inclusion of emoji prefixes. These aren't just for decoration; they provide instant visual cues about the log's origin and meaning, making it effortless to scan logs during development and debugging.

*   **Logger Name Prefix**: A unique emoji is generated based on the name of the logger, so you can instantly identify which part of your application a log is from.
*   **Semantic Prefix**: Emojis are added based on the *semantic content* of the log, using either the active Semantic Layers or the fallback DAS pattern.

### 4. Semantic Layers

Semantic Layers are the heart of `provide.foundation`'s advanced logging capabilities. They provide a schema-driven way to define structured logging conventions for specific domains.

When you log a message with keys that match a field in an active semantic layer, the library automatically:
1.  Validates the log structure (in a future release).
2.  Adds a semantic emoji prefix based on the log's content.
3.  Namespaces the context for cleaner, more organized output.

The library comes with built-in layers for common domains:
*   `http`: For logging HTTP requests and responses.
*   `database`: For database queries and operations.
*   `llm`: For interactions with Large Language Models.

**Example using the `http` layer:**

```python
from provide.foundation import logger, setup_telemetry, TelemetryConfig, LoggingConfig

# Enable the 'http' semantic layer
config = TelemetryConfig(logging=LoggingConfig(enabled_semantic_layers=["http"]))
setup_telemetry(config)

# Log an HTTP request event
logger.info(
    "API request processed",
    **{
        "http.method": "GET",
        "http.status_code": 200,
        "http.url": "/api/v1/users",
        "http.response_time_ms": 25,
    }
)
```

**Output:**
```
[➡️][✅] API request processed http.url=/api/v1/users http.response_time_ms=25
```
The `[➡️][✅]` prefix is automatically generated from the `http.method` ("GET") and `http.status_code` (200).

### 5. The Domain-Action-Status (DAS) Fallback

When no semantic layer matches a log event, the system falls back to the classic DAS pattern. By providing `domain`, `action`, and `status` keys in your log call, you can still get meaningful emoji prefixes.

```python
logger.info(
    "User authentication successful",
    domain="auth",      # 🔑
    action="login",     # ➡️
    status="success",   # ✅
    user_id="usr_456"
)
```

**Output:**
```
[🔑][➡️][✅] User authentication successful user_id='usr_456'
```

## 🔧 Configuration

While `provide.foundation` works out of the box, you can easily configure it to suit your needs.

### Via Environment Variables

This is the recommended way to configure the logger in production environments.

| Variable | Description | Default | Example |
|---|---|---|---|
| `FOUNDATION_SERVICE_NAME` | Sets the service name for all logs. | `None` | `my-api-service` |
| `FOUNDATION_LOG_LEVEL` | Default log level. | `DEBUG` | `INFO` |
| `FOUNDATION_LOG_CONSOLE_FORMATTER` | Output format. | `key_value` | `json` |
| `FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS` | Comma-separated list of layers to enable. | `""` | `http,database` |
| `FOUNDATION_SHOW_EMOJI_MATRIX` | Set to `true` to print the emoji reference on startup. | `false` | `true` |

### Programmatic Configuration

For more complex setups, you can configure the logger in your application's code. This is best done once at application startup.

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="my-awesome-app",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",
        # Set per-module log levels for fine-grained control
        module_levels={
            "noisy_library": "WARNING",
            "critical_component": "DEBUG",
        },
        # Enable built-in semantic layers
        enabled_semantic_layers=["http", "database", "llm"],
    )
)

setup_telemetry(config)
```

## 🧑‍💻 Advanced Usage

### Named Loggers

For better organization, especially in larger applications, you can create named loggers. Each named logger will have its own unique, consistent emoji prefix.

```python
from provide.foundation import logger

# Get a logger for a specific component
db_logger = logger.get_logger("database")
api_logger = logger.get_logger("api.v1.users")

db_logger.info("Connection pool initialized")
api_logger.info("User lookup request received")
```

**Output:**
```
[🗄️] Connection pool initialized
[🙋] User lookup request received
```

### Exception Handling

The `logger.exception()` method is the best way to log exceptions. It automatically captures and formats the traceback information.

```python
try:
    # Risky operation
    ...
except Exception as e:
    logger.exception(
        "Failed to process user data",
        user_id=123,
        cause=str(e)
    )
```

### Async Support

`provide.foundation` is fully compatible with `asyncio`. You can log from async functions without any special considerations.

```python
import asyncio
from provide.foundation import logger

async def fetch_data(url: str):
    logger.info("Fetching data", url=url)
    await asyncio.sleep(1) # Simulate network request
    logger.info("Data fetched successfully", url=url)

asyncio.run(fetch_data("https://example.com"))
```

### `timed_block` Utility

The `timed_block` context manager is a powerful utility for logging the duration and outcome of a block of code. It's perfect for monitoring performance of critical sections.

```python
from provide.foundation import logger, timed_block

# Time a successful operation
with timed_block(logger, "database_query", db_table="users"):
    # Simulate work
    time.sleep(0.5)

# Time a failing operation
try:
    with timed_block(logger, "payment_processing", transaction_id="txn_123"):
        raise RuntimeError("Credit card declined")
except RuntimeError:
    logger.info("Gracefully handling payment failure.")
```

**Output:**
```
[▶️] database_query db_table=users outcome=success duration_ms=501.23
[🔥] payment_processing transaction_id='txn_123' outcome=error error.message='Credit card declined' error.type=RuntimeError duration_ms=0.45
```

## 🎨 Customization

### Creating a Custom Semantic Layer

You can easily define your own semantic layers for your application's domain.

```python
from provide.foundation import (
    SemanticLayer,
    SemanticFieldDefinition,
    CustomDasEmojiSet,
    TelemetryConfig,
    LoggingConfig,
    setup_telemetry,
    logger,
)

# 1. Define emoji sets for the layer's fields
file_op_emojis = CustomDasEmojiSet(
    name="file_operation_emojis",
    emojis={"read": "📖", "write": "📝", "delete": "🗑️", "default": "⚙️"}
)
file_outcome_emojis = CustomDasEmojiSet(
    name="file_outcome_emojis",
    emojis={"success": "✅", "not_found": "❓", "permission_denied": "🚫", "default": "🔥"}
)

# 2. Define the semantic fields
file_io_fields = [
    SemanticFieldDefinition(log_key="file.operation", emoji_set_name="file_operation_emojis"),
    SemanticFieldDefinition(log_key="file.outcome", emoji_set_name="file_outcome_emojis"),
    SemanticFieldDefinition(log_key="file.path"), # This field adds context but not an emoji
]

# 3. Create the layer
file_io_layer = SemanticLayer(
    name="file_io",
    emoji_sets=[file_op_emojis, file_outcome_emojis],
    field_definitions=file_io_fields,
)

# 4. Configure telemetry to use the custom layer
config = TelemetryConfig(logging=LoggingConfig(custom_semantic_layers=[file_io_layer]))
setup_telemetry(config)

# 5. Log using your new semantic keys!
logger.info(
    "File write complete",
    **{
        "file.operation": "write",
        "file.outcome": "success",
        "file.path": "/data/report.csv",
    }
)
```

**Output:**
```
[📝][✅] File write complete file.path=/data/report.csv
```

## ⚡ Performance

`provide.foundation` is built for speed. However, for ultra-high-throughput applications, consider these tips:
*   **Set a higher log level in production**: `INFO` or `WARNING` is typical. This avoids the cost of processing and writing `DEBUG` logs.
*   **Use the `json` formatter**: It is slightly more performant than the `key_value` formatter and is better for ingestion by log aggregators.
*   **Disable logger name emojis if needed**: If you have thousands of dynamically named loggers, you can disable the name-based emoji for a performance boost.

## 🤝 Contribution

We welcome contributions! Whether it's bug reports, feature requests, or code contributions, please feel free to get involved.

*   **For developers contributing to this library**: Please see `DEVELOPMENT.md` and `CLAUDE.md` for detailed setup and convention guides.
*   **To report a bug or request a feature**: Please open an issue on our [GitHub repository](https://github.com/provide-io/provide-foundation).

---

<p align="center">
  Made with ❤️ by the team at <a href="https://provide.io">Provide</a>
</p>