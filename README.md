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

Install `provide.foundation` using `uv` (recommended) or `pip`:

```bash
uv pip install provide-foundation
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
    main()```

Run this script, and you'll see beautifully formatted, structured output right in your console:

```[▶️] Application starting up
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

`provide.foundation` is built around the principle of structured logging. Instead of embedding variables in log messages, you pass them as keyword arguments. This makes your logs machine-readable and consistent.

```python
# ❌ Anti-pattern: Unstructured logging
logger.info(f"User {user_id} completed checkout for order {order_id}.")

# ✅ Best practice: Structured logging
logger.info(
    "Checkout complete",
    user_id=user_id,
    order_id=order_id,
)
```

### 3. Semantic Layers

Semantic Layers provide a schema-driven way to define structured logging conventions for specific domains like HTTP, databases, or LLMs. When you log a message with keys that match a semantic layer, the library automatically adds contextual emoji prefixes.

**Example using the `http` layer:**

```python
from provide.foundation import logger, setup_telemetry, TelemetryConfig, LoggingConfig

# Enable the 'http' emoji set
config = TelemetryConfig(logging=LoggingConfig(enabled_emoji_sets=["http"]))
setup_telemetry(config)

# Log an HTTP request event
logger.info(
    "API request processed",
    **{
        "http.method": "GET",
        "http.status_code": 200,
        "http.url": "/api/v1/users",
    }
)
```

**Output:**
```
[➡️][✅] API request processed http.url=/api/v1/users
```
The `[➡️][✅]` prefix is automatically generated from the `http.method` ("GET") and `http.status_code` (200).

### 4. The Domain-Action-Status (DAS) Fallback

When no semantic layer matches, the system falls back to the classic DAS pattern. By providing `domain`, `action`, and `status` keys, you still get meaningful emoji prefixes.

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

While `provide.foundation` works out of the box, you can easily configure it via environment variables or code.

### Via Environment Variables

This is the recommended way to configure the logger in production.

#### Core Telemetry Variables (FOUNDATION_*)

These control the core logging behavior:

| Variable | Description | Default | Example |
|---|---|---|---|
| `FOUNDATION_SERVICE_NAME` | Sets the service name for all logs. | `None` | `my-api-service` |
| `FOUNDATION_LOG_LEVEL` | Default log level. | `DEBUG` | `INFO` |
| `FOUNDATION_LOG_CONSOLE_FORMATTER` | Output format. | `key_value` | `json` |
| `FOUNDATION_LOG_ENABLED_EMOJI_SETS` | Comma-separated list of emoji sets to enable. | `""` | `http,database` |

#### CLI Variables (PROVIDE_*)

When using the CLI decorators, these environment variables are also available:

| Variable | Description | Default | Example |
|---|---|---|---|
| `PROVIDE_LOG_LEVEL` | CLI log level override | - | `DEBUG` |
| `PROVIDE_LOG_FORMAT` | CLI output format | `key_value` | `json` |
| `PROVIDE_JSON_OUTPUT` | Force JSON output in CLI | `false` | `true` |
| `PROVIDE_NO_COLOR` | Disable colored output | `false` | `true` |
| `PROVIDE_NO_EMOJI` | Disable emoji in output | `false` | `true` |

### Programmatic Configuration

For more complex setups, configure the logger once at application startup.

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    service_name="my-awesome-app",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json",
        module_levels={
            "noisy_library": "WARNING",
        },
        enabled_emoji_sets=["http", "database", "llm"],
    )
)

setup_telemetry(config)
```

## 🧑‍💻 Advanced Usage

### Named Loggers

For better organization in larger applications, create named loggers. Each will have its own unique, consistent emoji prefix.

```python
from provide.foundation import logger

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

### `timed_block` Utility

The `timed_block` context manager is a powerful utility for logging the duration and outcome of a block of code.

```python
import time
from provide.foundation import logger, timed_block

# Time a successful operation
with timed_block(logger, "database_query", db_table="users"):
    time.sleep(0.5)

# Time a failing operation
try:
    with timed_block(logger, "payment_processing", transaction_id="txn_123"):
        raise RuntimeError("Credit card declined")
except RuntimeError:
    pass
```

**Output:**
```
[▶️] database_query completed db_table=users duration_seconds=0.501
[🔥] payment_processing failed transaction_id=txn_123 duration_seconds=0.0 error=...
```

## 🤝 Contribution

We welcome contributions! 
*   **For developers**: Please see `DEVELOPMENT.md` and `CLAUDE.md` for setup and convention guides.
*   **To report a bug or request a feature**: Please open an issue on our [GitHub repository](https://github.com/provide-io/provide-foundation).

---

<p align="center">
  Made with ❤️ by the team at <a href="https://provide.io">Provide</a>
</p>
