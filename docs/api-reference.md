# 📚 Foundation Telemetry API Documentation

Complete API reference for Foundation Telemetry v1.0.0

## 🎯 Core API

### setup_telemetry()

```python
def setup_telemetry(config: TelemetryConfig | None = None) -> None
```

**Description**: Initializes and configures the Foundation Telemetry system.

**Parameters**:
- `config` (TelemetryConfig | None): Configuration instance. If None, loads from environment variables.

**Thread Safety**: ✅ Thread-safe with internal locking

**Example**:
```python
from provide.foundation import setup_telemetry, TelemetryConfig

# Use environment variables
setup_telemetry()

# Use programmatic config
config = TelemetryConfig(service_name="my-app")
setup_telemetry(config)
```

### shutdown_foundation_telemetry()

```python
async def shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None
```

**Description**: Performs graceful shutdown of telemetry system.

**Parameters**:
- `timeout_millis` (int): Timeout for shutdown operations (currently unused)

**Returns**: None

**Example**:
```python
import asyncio
from provide.foundation import shutdown_foundation_telemetry

# In async context
await shutdown_foundation_telemetry()

# In sync context
asyncio.run(shutdown_foundation_telemetry())
```

## 🏗️ Configuration Classes

### TelemetryConfig

```python
@define(kw_only=True, auto_attribs=True, frozen=True, slots=True)
class TelemetryConfig:
    service_name: str | None = field(default=None)
    logging: LoggingConfig = field(factory=LoggingConfig)
    globally_disabled: bool = field(default=False)
```

**Description**: Main configuration class for telemetry system.

**Attributes**:
- `service_name`: Service identifier included in all log entries
- `logging`: Logging-specific configuration 
- `globally_disabled`: If True, disables all telemetry output

**Methods**:

#### from_env()

```python
@classmethod
def from_env(cls) -> "TelemetryConfig"
```

**Description**: Creates configuration from environment variables.

**Environment Variables**:
- `OTEL_SERVICE_NAME` / `FOUNDATION_SERVICE_NAME`: Service name
- `FOUNDATION_TELEMETRY_DISABLED`: Global disable flag

**Example**:
```python
import os
from provide.foundation import TelemetryConfig

os.environ["FOUNDATION_SERVICE_NAME"] = "my-service"
config = TelemetryConfig.from_env()
print(config.service_name)  # "my-service"
```

### LoggingConfig

```python
@define(kw_only=True, auto_attribs=True, frozen=True, slots=True)
class LoggingConfig:
    default_level: LogLevelStr = field(default="DEBUG")
    module_levels: dict[str, LogLevelStr] = field(factory=dict)
    console_formatter: Literal["key_value", "json"] = field(default="key_value")
    logger_name_emoji_prefix_enabled: bool = field(default=True)
    das_emoji_prefix_enabled: bool = field(default=True)
    omit_timestamp: bool = field(default=False)
    # -- NEW ATTRIBUTES --
    enabled_semantic_layers: list[str] = field(factory=list)
    custom_semantic_layers: list[SemanticLayer] = field(factory=list)
    user_defined_emoji_sets: list[CustomDasEmojiSet] = field(factory=list)
```

**Description**: Logging-specific configuration options.

**Attributes**:
- `default_level`: Default log level for all loggers
- `module_levels`: Per-module log level overrides
- `console_formatter`: Output format ("key_value" or "json")
- `logger_name_emoji_prefix_enabled`: Enable logger name emoji prefixes
- `das_emoji_prefix_enabled`: Enable semantic emoji prefixes (from layers or legacy DAS).
- `omit_timestamp`: Remove timestamps from output
- **`enabled_semantic_layers` (new)**: A list of names of built-in or custom semantic layers to activate (e.g., `["llm", "http"]`).
- **`custom_semantic_layers` (new)**: A list of `SemanticLayer` objects to define custom logging schemas.
- **`user_defined_emoji_sets` (new)**: A list of `CustomDasEmojiSet` objects to add or override emoji mappings.

**Environment Variables**:
- `FOUNDATION_LOG_LEVEL`: Default log level
- `FOUNDATION_LOG_CONSOLE_FORMATTER`: Output formatter
- `FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED`: Logger emoji toggle
- `FOUNDATION_LOG_DAS_EMOJI_ENABLED`: DAS emoji toggle
- `FOUNDATION_LOG_OMIT_TIMESTAMP`: Timestamp toggle
- `FOUNDATION_LOG_MODULE_LEVELS`: Module level overrides
- **`FOUNDATION_LOG_ENABLED_SEMANTIC_LAYERS` (new)**: Comma-separated list of layer names to enable (e.g., `"llm,http"`).
- **`FOUNDATION_LOG_CUSTOM_SEMANTIC_LAYERS` (new)**: A JSON string representing a list of `SemanticLayer` objects.
- **`FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS` (new)**: A JSON string representing a list of `CustomDasEmojiSet` objects.

**Example**:
```python
from provide.foundation import LoggingConfig

config = LoggingConfig(
    default_level="INFO",
    module_levels={"auth": "DEBUG", "db": "ERROR"},
    console_formatter="json",
    enabled_semantic_layers=["http", "database"], # Enable built-in layers
    das_emoji_prefix_enabled=True
)
```

### LogLevelStr

```python
LogLevelStr = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]
```

**Description**: Type alias for valid log level strings.

**Valid Values**:
- `"CRITICAL"`: Critical system failures
- `"ERROR"`: Error conditions  
- `"WARNING"`: Warning conditions
- `"INFO"`: Informational messages
- `"DEBUG"`: Debug information
- `"TRACE"`: Ultra-verbose tracing (custom level)
- `"NOTSET"`: No level filtering

## 📝 Logger Interface

### logger (Global Instance)

```python
logger: FoundationLogger
```

**Description**: Global logger instance for immediate use.

**Example**:
```python
from provide.foundation import logger

logger.info("Application started")
logger.debug("Debug information", user_id=123)
logger.error("Error occurred", error_code="E001")
```

### FoundationLogger Class

#### get_logger()

```python
def get_logger(self, name: str | None = None) -> Any
```

**Description**: Creates a named logger instance.

**Parameters**:
- `name`: Logger name (defaults to "pyvider.default")

**Returns**: structlog BoundLogger instance

**Example**:
```python
from provide.foundation import logger

auth_logger = logger.get_logger("auth.service")
db_logger = logger.get_logger("database.connection")

auth_logger.info("User authenticated")
db_logger.error("Connection failed")
```

#### Logging Methods

All methods follow the same signature pattern:

```python
def info(self, event: str, *args: Any, **kwargs: Any) -> None
def debug(self, event: str, *args: Any, **kwargs: Any) -> None  
def warning(self, event: str, *args: Any, **kwargs: Any) -> None
def error(self, event: str, *args: Any, **kwargs: Any) -> None
def critical(self, event: str, *args: Any, **kwargs: Any) -> None
def exception(self, event: str, *args: Any, **kwargs: Any) -> None
```

**Parameters**:
- `event`: Log message (supports printf-style formatting)
- `*args`: Arguments for printf-style formatting
- `**kwargs`: Additional structured data

**Example**:
```python
# Simple message
logger.info("User login successful")

# With formatting
logger.info("User %s logged in from %s", "alice", "192.168.1.1")

# With structured data (using a semantic layer)
logger.info("HTTP Request", **{"http.method": "GET", "http.status_code": 200})

# Exception logging (includes traceback)
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed", operation="risky")
```

#### trace()

```python
def trace(
    self, 
    event: str, 
    *args: Any, 
    _foundation_logger_name: str | None = None, 
    **kwargs: Any
) -> None
```

**Description**: Logs with custom TRACE level (more verbose than DEBUG).

**Parameters**:
- `event`: Log message
- `*args`: Format arguments
- `_foundation_logger_name`: Override logger name for this call
- `**kwargs`: Additional structured data

**Example**:
```python
# Default trace
logger.trace("Detailed execution flow")

# With custom logger name
logger.trace("Database query details", 
            _foundation_logger_name="db.trace",
            query="SELECT * FROM users", 
            duration_ms=23)
```

<!-- NEW SECTION -->
## ⏱️ Utility Functions

### timed_block()

```python
def timed_block(
    logger_instance: "FoundationLogger",
    event_name: str,
    layer_keys: dict[str, Any] | None = None,
    **initial_kvs: Any
) -> Generator[None, None, None]
```

**Description**: A context manager to log the duration and outcome of a block of code. It automatically captures the start time, executes the wrapped code block, and then logs an event including the `duration_ms`, `outcome` (success/error), and any initial or error-specific key-value pairs. If an exception occurs, it is logged and then re-raised.

**Parameters**:
- `logger_instance`: The `provide.foundation.logger` instance to use for logging.
- `event_name`: A descriptive name for the event/operation being timed.
- `layer_keys`: Optional dictionary of pre-defined semantic keys relevant to active telemetry layers (e.g., `{"llm.task": "generation"}`). These are merged with `initial_kvs`.
- `**initial_kvs`: Additional key-value pairs to include in the log entry from the start of the block.

**Example**:
```python
from provide.foundation import logger, timed_block

# Example 1: Successful operation
with timed_block(logger, "database_query", db_table="users", query_type="select"):
    # ... code to execute database query ...
    pass
# Logs: [info] database_query db_table=users query_type=select outcome=success duration_ms=...

# Example 2: Failing operation
try:
    with timed_block(logger, "payment_processing", transaction_id="txn_123"):
        raise RuntimeError("Credit card declined")
except RuntimeError:
    # The exception is re-raised by timed_block
    logger.info("Handling payment failure.")

# Logs: [error] payment_processing transaction_id=txn_123 outcome=error error.message='Credit card declined' error.type=RuntimeError duration_ms=...
```
<!-- END NEW SECTION -->

## 🏛️ Semantic Layer API

Semantic layers provide an extensible, schema-driven way to define structured logging conventions and their corresponding emoji representations.

### SemanticLayer

```python
@define(frozen=True, slots=True)
class SemanticLayer:
    name: str
    description: str | None = None
    emoji_sets: list[CustomDasEmojiSet] = field(factory=list)
    field_definitions: list[SemanticFieldDefinition] = field(factory=list)
    priority: int = 0
```
**Description**: Defines a complete semantic logging convention for a domain.
- `name`: Unique name for the layer (e.g., "http", "database").
- `emoji_sets`: A list of `CustomDasEmojiSet` objects used by this layer.
- `field_definitions`: A list of `SemanticFieldDefinition` objects that define the log keys and their mapping to emoji sets. The order of this list determines the order of emojis in the prefix.
- `priority`: A number to resolve conflicts between layers. Layers with a higher priority will override field definitions from layers with a lower priority.

### SemanticFieldDefinition

```python
@define(frozen=True, slots=True)
class SemanticFieldDefinition:
    log_key: str
    description: str | None = None
    value_type: str | None = None
    emoji_set_name: str | None = None
    default_emoji_override_key: str | None = None
```
**Description**: Defines a single structured log key within a layer.
- `log_key`: The key to look for in the log event's `kwargs` (e.g., "http.method").
- `emoji_set_name`: The name of the `CustomDasEmojiSet` to use for finding an emoji for this key's value. If `None`, this key does not contribute to the emoji prefix.

### CustomDasEmojiSet

```python
@define(frozen=True, slots=True)
class CustomDasEmojiSet:
    name: str
    emojis: dict[str, str]
    default_emoji_key: str = "default"
```
**Description**: A named collection of emojis mapped to specific string values.
- `name`: A unique name for the set (e.g., "http_method", "llm_outcome").
- `emojis`: A dictionary mapping a value (e.g., "get", "success") to an emoji (e.g., "📥", "✅").
- `default_emoji_key`: The key within the `emojis` dict to use as a fallback.

### Example: Creating a Custom `file_io` Layer

This example shows how to define a completely custom layer for file operations.

```python
from provide.foundation import (
    setup_telemetry,
    logger,
    TelemetryConfig,
    LoggingConfig,
    SemanticLayer,
    SemanticFieldDefinition,
    CustomDasEmojiSet,
)

# 1. Define Emoji Sets for the layer
file_op_emojis = CustomDasEmojiSet(
    name="file_operation_emojis",
    emojis={"read": "📖", "write": "📝", "delete": "🗑️", "default": "⚙️"}
)

file_outcome_emojis = CustomDasEmojiSet(
    name="file_outcome_emojis",
    emojis={"success": "✅", "not_found": "❓", "permission_denied": "🚫", "default": "🔥"}
)

# 2. Define the Semantic Fields that use these emoji sets
file_io_fields = [
    SemanticFieldDefinition(log_key="file.operation", emoji_set_name="file_operation_emojis"),
    SemanticFieldDefinition(log_key="file.outcome", emoji_set_name="file_outcome_emojis"),
    SemanticFieldDefinition(log_key="file.path"), # Does not contribute to emoji prefix
    SemanticFieldDefinition(log_key="file.size_bytes"),
]

# 3. Create the Semantic Layer
file_io_layer = SemanticLayer(
    name="file_io",
    description="Semantic conventions for file input/output operations.",
    emoji_sets=[file_op_emojis, file_outcome_emojis],
    field_definitions=file_io_fields,
    priority=50
)

# 4. Configure telemetry to use the custom layer
config = TelemetryConfig(
    logging=LoggingConfig(
        # Note: We don't need to "enable" the custom layer, just provide it.
        custom_semantic_layers=[file_io_layer]
    )
)
setup_telemetry(config)

# 5. Log using the new semantic keys
logger.info(
    "File write operation complete",
    **{
        "file.operation": "write",
        "file.outcome": "success",
        "file.path": "/data/report.csv",
        "file.size_bytes": 10240,
    }
)
# Expected Output: [📝][✅] File write operation complete file.path=/data/report.csv file.size_bytes=10240

logger.error(
    "Failed to read file",
    **{
        "file.operation": "read",
        "file.outcome": "permission_denied",
        "file.path": "/etc/shadow",
    }
)
# Expected Output: [📖][🚫] Failed to read file file.path=/etc/shadow
```

## 🎨 Legacy Emoji System (Fallback)

When no semantic layers are active, the system falls back to the original Domain-Action-Status (DAS) pattern. Use `domain`, `action`, and `status` keyword arguments to trigger these emoji prefixes.

```python
logger.info("User authentication", 
           domain="auth", 
           action="login", 
           status="success")
# Output: [🔑][➡️][✅] User authentication
```

### Emoji Dictionaries

#### PRIMARY_EMOJI (Domains)

```python
PRIMARY_EMOJI: dict[str, str] = {
    "system": "⚙️", "server": "🛎️", "client": "🙋", "network": "🌐",
    "security": "🔐", "config": "🔩", "database": "🗄️", "cache": "💾",
    "task": "🔄", "plugin": "🔌", "telemetry": "🛰️", "di": "💉",
    "protocol": "📡", "file": "📄", "user": "👤", "test": "🧪",
    "utils": "🧰", "core": "🌟", "auth": "🔑", "entity": "🦎",
    "report": "📈", "default": "❓",
}
```

#### SECONDARY_EMOJI (Actions)

```python
SECONDARY_EMOJI: dict[str, str] = {
    "init": "🌱", "start": "🚀", "stop": "🛑", "connect": "🔗",
    "disconnect": "💔", "listen": "👂", "send": "📤", "receive": "📥",
    "read": "📖", "write": "📝", "process": "⚙️", "validate": "🛡️",
    "execute": "▶️", "query": "🔍", "update": "🔄", "delete": "🗑️",
    "login": "➡️", "logout": "⬅️", "auth": "🔑", "error": "🔥",
    "encrypt": "🛡️", "decrypt": "🔓", "parse": "🧩", "transmit": "📡",
    "build": "🏗️", "schedule": "📅", "emit": "📢", "load": "💡",
    "observe": "🧐", "request": "🗣️", "interrupt": "🚦",
    "default": "⚙️",
}
```

#### TERTIARY_EMOJI (Statuses)

```python
TERTIARY_EMOJI: dict[str, str] = {
    "success": "✅", "failure": "❌", "error": "🔥", "warning": "⚠️",
    "info": "ℹ️", "debug": "🐞", "trace": "👣", "attempt": "⏳",
    "retry": "🔁", "skip": "⏭️", "complete": "🏁", "timeout": "⏱️",
    "notfound": "❓", "unauthorized": "🚫", "invalid": "💢", "cached": "🎯",
    "ongoing": "🏃", "idle": "💤", "ready": "👍", "default": "➡️",
}
```

### show_emoji_matrix()

```python
def show_emoji_matrix() -> None
```

**Description**: Displays the complete emoji mapping contract for the **active configuration**. This is the best way to see which emojis are currently in use.

**Environment Variable**: `FOUNDATION_SHOW_EMOJI_MATRIX=true`

**Example**:
```python
import os
from provide.foundation.logger.emoji_matrix import show_emoji_matrix

os.environ["FOUNDATION_SHOW_EMOJI_MATRIX"] = "true"
show_emoji_matrix()  # Prints emoji reference
```

## 🚀 Performance Considerations

### **Benchmarked Performance Metrics**

The Foundation Telemetry system has been thoroughly benchmarked to ensure production-ready performance:

| Scenario          | Typical Performance | Notes                                   |
|-------------------|---------------------|-----------------------------------------|
| **Basic Logging** | ~40,000 msg/sec     | Key-value format, emoji enabled         |
| **JSON Formatting** | ~38,900 msg/sec     | Structured output with emojis           |
| **Multithreaded**   | ~39,800 msg/sec     | 10 threads, concurrent logging          |
| **Level Filtering** | ~68,100 msg/sec     | Efficient filtering                     |
| **Large Payloads**  | ~14,200 msg/sec     | ~1KB structured data per message        |
| **Async Logging**   | ~43,400 msg/sec     | Logging from async tasks                |

### **Optimization Guidelines**

#### **1. Log Level Management**
```python
# ✅ RECOMMENDED: Use appropriate levels for production
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",  # Avoid DEBUG/TRACE in production
        module_levels={
            "critical.component": "ERROR",    # Only errors for critical paths
            "auth": "DEBUG",                  # Verbose only where needed
            "performance.sensitive": "WARNING"  # Minimal logging for hot paths
        }
    )
)
```

#### **2. Module-Level Filtering**
```python
# ✅ RECOMMENDED: Use hierarchical filtering for fine control
module_levels = {
    "app": "INFO",                    # Default for application
    "app.auth": "DEBUG",              # Verbose authentication logs
    "app.auth.oauth": "TRACE",        # Ultra-verbose OAuth debugging
    "external.api": "ERROR",          # Minimal third-party noise
    "database.queries": "WARNING",    # Only slow/problematic queries
}
```

#### **3. High-Volume Applications**
```python
# ✅ RECOMMENDED: Configuration for high-throughput services
high_performance_config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="WARNING",  # Reduce log volume
        console_formatter="json",  # More efficient for log aggregation
        logger_name_emoji_prefix_enabled=False,  # Slight performance gain
        das_emoji_prefix_enabled=True,  # Keep semantic benefits
        omit_timestamp=True,  # If timestamps added by log aggregator
    )
)
```

#### **4. Memory Usage Optimization**
```python
# For long-running applications, monitor memory usage
from provide.foundation.logger.custom_processors import get_emoji_cache_stats

# Periodically check cache utilization
stats = get_emoji_cache_stats()
print(f"Emoji cache usage: {stats['cache_utilization']:.1f}%")

# Clear cache if needed (rare)
if stats['cache_size'] > 500:
    from provide.foundation.logger.custom_processors import clear_emoji_cache
    clear_emoji_cache()
```

### **Performance Best Practices**

#### **Efficient Logging Patterns**
```python
# ✅ GOOD: Structured logging with meaningful fields
logger.info("Request processed",
           request_id="req-123", 
           duration_ms=45, 
           status_code=200)

# ✅ GOOD: Use semantic layers for rich context
logger.info("Payment completed",
           **{"payment.status": "success", "payment.amount": 99.99})

# ❌ AVOID: Excessive string formatting in hot paths
logger.debug(f"Complex calculation: {expensive_computation()}")  # Computed even if filtered

# ✅ BETTER: Let level filtering avoid computation
logger.debug("Complex calculation", result=lambda: expensive_computation())
```

#### **Production Monitoring**
```python
# Monitor logging performance in production
import time

start_time = time.time()
for i in range(1000):
    logger.info("Performance test", iteration=i)
end_time = time.time()

throughput = 1000 / (end_time - start_time)
logger.info("Logging throughput measured", 
           **{"system.benchmark.messages_per_second": throughput})
```

### **Memory and CPU Considerations**

1. **Emoji Caching**: Logger name emoji lookups are cached for frequently used names (up to 1000 entries)
2. **Level Filtering**: Early filtering prevents expensive string operations for suppressed messages
3. **Processor Chain**: Optimized order minimizes work for filtered messages
4. **Thread Safety**: Lock-free logging operations after initial setup

### **Troubleshooting Performance Issues**

#### **Common Issues and Solutions**

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Slow Throughput** | <500 msg/sec | Check log level settings, disable unnecessary emojis |
| **High Memory Usage** | Growing RSS | Monitor emoji cache, check for log level misconfiguration |
| **Lock Contention** | Inconsistent performance | Verify proper setup, avoid repeated setup calls |
| **Formatting Overhead** | JSON slower than expected | Consider key-value format for high-volume scenarios |

#### **Performance Debugging**
```python
# Run built-in benchmarks
python scripts/benchmark_performance.py

# Check configuration impact
config_fast = TelemetryConfig(
    logging=LoggingConfig(
        default_level="ERROR",  # Minimal logging
        logger_name_emoji_prefix_enabled=False,
        das_emoji_prefix_enabled=False,
    )
)

config_full = TelemetryConfig(
    logging=LoggingConfig(
        default_level="DEBUG",  # Verbose logging
        logger_name_emoji_prefix_enabled=True,
        das_emoji_prefix_enabled=True,
    )
)

# Compare performance between configurations
```

## 🔧 Advanced Usage

### Module-Level Configuration

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        module_levels={
            "auth": "DEBUG",           # Verbose auth logging
            "auth.oauth": "TRACE",     # Ultra-verbose OAuth
            "database": "ERROR",       # Only DB errors
            "cache": "WARNING",        # Cache warnings+
            "api.handlers": "INFO",    # API info+
        }
    )
)
setup_telemetry(config)

# These loggers will use their configured levels
auth_logger = logger.get_logger("auth.service")        # DEBUG level
oauth_logger = logger.get_logger("auth.oauth.token")   # TRACE level  
db_logger = logger.get_logger("database.connection")   # ERROR level
cache_logger = logger.get_logger("cache.redis")        # WARNING level
api_logger = logger.get_logger("api.handlers.user")    # INFO level
```

### Custom Processor Development

```python
from typing import Any
import structlog

def custom_processor(
    logger: Any, 
    method_name: str, 
    event_dict: structlog.types.EventDict
) -> structlog.types.EventDict:
    """Example custom processor."""
    # Add custom field
    event_dict["custom_field"] = "custom_value"
    
    # Modify existing fields
    if "sensitive_data" in event_dict:
        event_dict["sensitive_data"] = "[REDACTED]"
    
    return event_dict

# Note: Adding custom processors requires modifying core.py
# This is for advanced users who want to extend functionality
```

### Testing Integration

```python
import pytest
from provide.foundation import setup_telemetry, TelemetryConfig

@pytest.fixture
def setup_logging():
    """Test fixture for logging setup."""
    config = TelemetryConfig(
        service_name="test-service",
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="json",
            omit_timestamp=True  # Easier test assertions
        )
    )
    setup_telemetry(config)

def test_feature_with_logging(setup_logging, caplog):
    """Example test using logging."""
    from provide.foundation import logger
    
    logger.info("Test operation", operation="test")
    
    # Verify log output
    assert "Test operation" in caplog.text
    assert "operation=test" in caplog.text
```

## 🔍 Troubleshooting

### Common Issues

#### Version Import Error
```python
# If dynamic versioning fails
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("provide-foundation")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"  # Development fallback
```

#### Thread Safety Concerns
```python
# The library is thread-safe, but for custom extensions:
import threading

_custom_lock = threading.Lock()

def thread_safe_operation():
    with _custom_lock:
        # Your thread-safe code here
        pass
```

#### Performance Optimization
```python
# For high-volume logging, consider level filtering
config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="WARNING",  # Reduce log volume
        module_levels={
            "critical.module": "ERROR"  # Only errors for critical modules
        }
    )
)
```
