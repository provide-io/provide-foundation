# Examples Gallery

Quick, copy-paste examples for common provide.foundation use cases.

## Logging Examples

### Basic Structured Logging

```python
from provide.foundation import logger

# Simple logging with context
logger.info("user_login", 
            user_id="user-123",
            ip="192.168.1.1",
            success=True)

# With error context
try:
    process_data()
except Exception as e:
    logger.exception("processing_failed",
                    error=str(e),
                    data_size=1024)
```

### Contextual Logging

```python
# From examples/06_trace_logging.py
from provide.foundation import logger

# Add context via structured fields
logger.info("request_started",
            request_id="req-456",
            user_id="user-123")
process_request()
logger.info("request_completed",
            request_id="req-456",
            user_id="user-123")
```

**See full example:** [examples/06_trace_logging.py](../../examples/06_trace_logging.py)

### Async Logging

```python
# From examples/09_async_usage.py
import asyncio
from provide.foundation import logger

async def async_operation():
    logger.info("task_started", operation="async_task")
    await asyncio.sleep(1)
    logger.info("task_completed", operation="async_task")

asyncio.run(async_operation())
```

**See full example:** [examples/09_async_usage.py](../../examples/09_async_usage.py)

## CLI Examples

### Simple Command

```python
# From examples/12_cli_application.py
from provide.foundation.hub import register_command, Hub
from provide.foundation.cli import echo_success

@register_command("init", category="project")
def init_command(name: str = "myproject", template: str = "default"):
    """Initialize a new project."""
    echo_success(f"Initializing project '{name}' with template '{template}'")

if __name__ == "__main__":
    hub = Hub()
    cli = hub.create_cli(name="myapp", version="1.0.0")
    cli()
```

**See full example:** [examples/12_cli_application.py](../../examples/12_cli_application.py)

### Nested Commands

```python
# From examples/12_cli_application.py
from provide.foundation.hub import register_command
from provide.foundation.cli import echo_info

@register_command("db.migrate")
def migrate():
    """Run database migrations."""
    echo_info("Running migrations...")

@register_command("db.seed")
def seed(count: int = 10):
    """Seed the database."""
    echo_info(f"Seeding {count} records...")

@register_command("db.reset")
def reset():
    """Reset the database."""
    echo_info("Resetting database...")

# Usage: python app.py db migrate
```

### Command with JSON Output

```python
# From examples/12_cli_application.py - status command
import json
from provide.foundation.hub import register_command, Hub
from provide.foundation.cli import echo_info, echo_json

@register_command("status")
def status_command(json_output: bool = False):
    """Show system status."""
    hub = Hub()
    data = {
        "components": len(hub.list_components()),
        "commands": len(hub.list_commands()),
        "status": "healthy"
    }
    
    if json_output:
        echo_json(data)
    else:
        for key, value in data.items():
            echo_info(f"{key}: {value}")
```

## Configuration Examples

### Environment Variables

```python
# From examples/08_env_variables_config.py
import os
from provide.foundation import TelemetryConfig

# Set environment variables
os.environ["PROVIDE_LOG_LEVEL"] = "DEBUG"
os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "json"

# Load configuration
config = TelemetryConfig.from_env()
print(f"Log level: {config.logging.default_level}")
print(f"Format: {config.logging.console_formatter}")
```

**See full example:** [examples/08_env_variables_config.py](../../examples/08_env_variables_config.py)

### Configuration File

```python
# From examples/11_config_management.py
from provide.foundation.config import FileConfigLoader, BaseConfig
from attrs import define

@define
class DatabaseConfig(BaseConfig):
    host: str = "localhost"
    port: int = 5432
    name: str = "myapp"

# Load from YAML/JSON/TOML file
loader = FileConfigLoader("config.yaml")
config = loader.load(DatabaseConfig)
print(f"Database: {config.host}:{config.port}/{config.name}")
```

**See full example:** [examples/11_config_management.py](../../examples/11_config_management.py)

### Runtime Configuration

```python
# From examples/02_custom_configuration.py
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig

# Configure telemetry at runtime
config = TelemetryConfig(
    service_name="my-service",
    environment="production",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json"
    )
)
setup_telemetry(config)
```

**See full example:** [examples/02_custom_configuration.py](../../examples/02_custom_configuration.py)

## Domain-Action-Status Pattern Examples

### DAS Pattern Logging

```python
# From examples/04_das_logging.py
from provide.foundation import logger

# Domain-Action-Status pattern for structured logging
logger.info("database_connection_established", 
            host="localhost", port=5432)

logger.info("api_request_started",
            method="GET", endpoint="/users")
            
logger.info("cache_hit_found",
            key="user:123", ttl=3600)

logger.error("payment_processing_failed",
             amount=99.99, currency="USD", error="Invalid card")
```

**See full example:** [examples/04_das_logging.py](../../examples/04_das_logging.py)

### Custom Emoji Patterns

```python
# From examples/04_das_logging.py
from provide.foundation import logger
from provide.foundation.logger.emoji.types import CustomDasEmojiSet

# Create custom emoji set
custom_emojis = CustomDasEmojiSet(
    enabled=True,
    das_mapping={
        "api_request_started": "🌐",
        "database_query_executed": "🗄️",
        "cache_hit_found": "⚡"
    }
)

# Logs will be prefixed with custom emojis
logger.info("api_request_started")  # 🌐 api_request_started
```

## Error Handling Examples

### Error Boundaries

```python
# From examples/05_exception_handling.py
from provide.foundation import logger, with_error_handling

@with_error_handling
def risky_operation():
    """Operation that might fail."""
    if random.random() > 0.5:
        raise ValueError("Random failure")
    return "success"

try:
    result = risky_operation()
    logger.info("operation_succeeded", result=result)
except Exception as e:
    logger.error("operation_failed", error=str(e))
```

**See full example:** [examples/05_exception_handling.py](../../examples/05_exception_handling.py)

### Exception Logging

```python
# From examples/05_exception_handling.py
from provide.foundation import logger

def process_data(data):
    try:
        # Process the data
        result = complex_operation(data)
        logger.info("data_processed", size=len(data), result=result)
    except ValueError as e:
        logger.exception("validation_error", data=data, error=str(e))
    except Exception as e:
        logger.exception("processing_error", data=data, error=str(e))
        raise
```

## Platform Detection Examples

```python
# From examples/10_production_patterns.py
from provide.foundation.platform import get_platform_info
from provide.foundation import logger

info = get_platform_info()
logger.info("system_info",
            platform=info["platform"],
            python_version=info["python_version"],
            hostname=info.get("hostname", "unknown"))

# Conditional logic based on platform
if info["platform"] == "darwin":
    # macOS specific code
    logger.debug("macos_specific_setup")
elif info["platform"] == "linux":
    # Linux specific code
    logger.debug("linux_specific_setup")
```

## Process Execution Examples

```python
from provide.foundation.process import run_shell_command
from provide.foundation import logger

# Simple command
result = run_shell_command("ls -la")
if result["returncode"] == 0:
    logger.info("command_succeeded", output=result["stdout"])
else:
    logger.error("command_failed", error=result["stderr"])

# With timeout and error handling
try:
    result = run_shell_command("slow_command", timeout=5.0)
except TimeoutError:
    logger.error("command_timeout", command="slow_command")
```

## Console Output Examples

```python
from provide.foundation import pout, perr

# Standard output with emoji
pout("✅ Operation successful")
pout("📊 Processing 1000 records...")
pout("🎉 All tests passed!")

# Error output
perr("❌ Connection failed")
perr("⚠️ Warning: Low memory")
perr("🔥 Critical error detected")

# Conditional output
if success:
    pout("✅ Task completed")
else:
    perr("❌ Task failed")
```

## Complete Working Examples

All examples shown above are extracted from fully working example files in the [examples/](../../examples/) directory:

| Example File | Description | Key Concepts |
|-------------|-------------|---------------|
| [01_quick_start.py](../../examples/01_quick_start.py) | Basic logging setup | Logger initialization, structured logging |
| [02_custom_configuration.py](../../examples/02_custom_configuration.py) | Custom telemetry config | TelemetryConfig, LoggingConfig |
| [03_named_loggers.py](../../examples/03_named_loggers.py) | Module-specific loggers | Named logger instances |
| [04_das_logging.py](../../examples/04_das_logging.py) | Domain-Action-Status pattern | Structured event naming, emoji prefixes |
| [05_exception_handling.py](../../examples/05_exception_handling.py) | Error handling patterns | Exception logging, error boundaries |
| [06_trace_logging.py](../../examples/06_trace_logging.py) | Distributed tracing | Request IDs, context propagation |
| [07_module_filtering.py](../../examples/07_module_filtering.py) | Log filtering by module | Module-level configuration |
| [08_env_variables_config.py](../../examples/08_env_variables_config.py) | Environment-based config | PROVIDE_* variables, env_field |
| [09_async_usage.py](../../examples/09_async_usage.py) | Async logging patterns | asyncio integration |
| [10_production_patterns.py](../../examples/10_production_patterns.py) | Production best practices | Performance, batching, monitoring |
| [11_config_management.py](../../examples/11_config_management.py) | Complete config system | ConfigManager, loaders, validation |
| [12_cli_application.py](../../examples/12_cli_application.py) | Full CLI application | Hub, commands, components |

To run any example:
```bash
python examples/01_quick_start.py
python examples/12_cli_application.py --help
PROVIDE_LOG_LEVEL=DEBUG python examples/08_env_variables_config.py
```

## Next Steps

- Explore the [User Guide](../guide/index.md) for in-depth coverage
- Check the [API Reference](../api/index.md) for complete documentation
- Browse the [Cookbook](../cookbook/index.md) for advanced patterns