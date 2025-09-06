# provide.foundation

**A Comprehensive Python Foundation Library for Modern Applications**

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

---

**provide.foundation** is a comprehensive foundation library for Python applications, offering structured logging, CLI utilities, configuration management, error handling, and essential application building blocks. Built with modern Python practices, it provides the core infrastructure that production applications need.

---

## Installation

```bash
# Using uv (recommended)
uv pip install provide-foundation

# Using pip
pip install provide-foundation
```

### Optional Dependencies

provide.foundation has optional feature sets that require additional dependencies:

| Feature | Install Command | Required For |
|---------|----------------|--------------|
| **Basic logging** | `pip install provide-foundation` | Core logging functionality |
| **CLI framework** | `pip install provide-foundation[cli]` | Command-line interface features |
| **Cryptography** | `pip install provide-foundation[crypto]` | Hash functions, digital signatures, certificates |
| **OpenTelemetry** | `pip install provide-foundation[opentelemetry]` | Distributed tracing and metrics |
| **All features** | `pip install provide-foundation[all]` | Everything above |

> **Quick Start Tip**: For immediate use with just logging, install the base package. Add extras as needed.

---

## What's Included

### Core Components

#### **Structured Logging**
Beautiful, performant logging built on `structlog` with emoji-enhanced visual parsing and zero configuration required.

```python
# Simple usage - works immediately with base install
from provide.foundation import logger

logger.info("Application started", version="1.0.0")
logger.error("Database connection failed", host="db.example.com", retry_count=3)

# Full setup with tracing/metrics (requires [opentelemetry] extra)
from provide.foundation import setup_telemetry
setup_telemetry()  # Configures logging + optional tracing/metrics
```

#### **CLI Framework**
Build command-line interfaces with automatic help generation and component registration.

> **Requires**: `pip install provide-foundation[cli]`

```python
# From examples/12_cli_application.py
from provide.foundation.hub import register_command
from provide.foundation.cli import echo_success

@register_command("init", category="project")
def init_command(name: str = "myproject", template: str = "default"):
    """Initialize a new project."""
    echo_success(f"Initializing project '{name}' with template '{template}'")
```

#### **Configuration Management**
Flexible configuration system supporting environment variables, files, and runtime updates.

```python
# From examples/11_config_management.py
from provide.foundation.config import BaseConfig, ConfigManager, field
from attrs import define

@define
class AppConfig(BaseConfig):
    app_name: str = field(default="my-app", description="Application name")
    port: int = field(default=8080, description="Server port")
    debug: bool = field(default=False, description="Debug mode")

manager = ConfigManager()
manager.register("app", config=AppConfig())
config = manager.get("app")
```

#### **Error Handling**
Comprehensive error handling with retry logic and error boundaries.

```python
# From examples/05_exception_handling.py
from provide.foundation import logger, with_error_handling

@with_error_handling
def risky_operation():
    """Operation that might fail."""
    result = perform_calculation()
    logger.info("operation_succeeded", result=result)
    return result
```

#### **Cryptographic Utilities**
Comprehensive cryptographic operations with modern algorithms and secure defaults.

> **Requires**: `pip install provide-foundation[crypto]`

```python
from provide.foundation.crypto import hash_file, create_self_signed, sign_data

# File hashing and verification
hash_result = hash_file("document.pdf", algorithm="sha256")

# Digital signatures
signature = sign_data(data, private_key, algorithm="ed25519")

# Certificate generation
cert, key = create_self_signed("example.com", key_size=2048)
```

#### **File Operations**
Atomic file operations with format support and safety guarantees.

```python
from provide.foundation.file import atomic_write, read_json, safe_copy

# Atomic file operations
atomic_write("config.json", {"key": "value"})
data = read_json("config.json")

# Safe file operations
safe_copy("source.txt", "backup.txt")
```

#### **Console I/O**
Enhanced console input/output with color support, JSON mode, and interactive prompts.

```python
from provide.foundation import pin, pout, perr

# Colored output
pout("Success!", color="green")
perr("Error occurred", color="red")

# Interactive input
name = pin("What's your name?")
password = pin("Enter password:", password=True)

# JSON mode for scripts
pout({"status": "ok", "data": results}, json=True)
```

#### **Platform Utilities**
Cross-platform detection and system information gathering.

```python
from provide.foundation import platform

# Platform detection
if platform.is_linux():
    logger.info("Running on Linux")

system_info = platform.get_system_info()
logger.info("System info", **system_info.to_dict())
```

#### **Process Execution**
Safe subprocess execution with streaming and async support.

```python
from provide.foundation import process

# Synchronous execution
result = process.run_command(["git", "status"])
if result.returncode == 0:
    logger.info("Git status", output=result.stdout)

# Streaming output
for line in process.stream_command(["tail", "-f", "app.log"]):
    logger.info("Log line", line=line)
```

#### **Registry Pattern**
Flexible registry system for managing components and commands.

```python
# From examples/12_cli_application.py
from provide.foundation.hub import Hub

class DatabaseResource:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connected = False
    
    def __enter__(self):
        """Initialize database connection."""
        self.connected = True
        return self

hub = Hub()
hub.add_component(DatabaseResource, name="database", dimension="resource", version="1.0.0")
db_class = hub.get_component("database", dimension="resource")
```

See [examples/](examples/) for more comprehensive examples.

---

## Quick Start Examples

### Building a CLI Application

```python
# From examples/12_cli_application.py
from provide.foundation.hub import Hub, register_command
from provide.foundation.cli import echo_info, echo_success

@register_command("status", aliases=["st", "info"])
def status_command(verbose: bool = False):
    """Show system status."""
    hub = Hub()
    echo_info(f"Registered components: {len(hub.list_components())}")
    echo_info(f"Registered commands: {len(hub.list_commands())}")

if __name__ == "__main__":
    hub = Hub()
    cli = hub.create_cli(name="myapp", version="1.0.0")
    cli()
```

### Configuration-Driven Application

```python
# From examples/11_config_management.py and examples/08_env_variables_config.py
from provide.foundation import setup_telemetry, logger
from provide.foundation.config import RuntimeConfig, env_field, ConfigManager
from attrs import define

@define
class DatabaseConfig(RuntimeConfig):
    """Database configuration from environment."""
    host: str = env_field(default="localhost", env_var="DB_HOST")
    port: int = env_field(default=5432, env_var="DB_PORT", parser=int)
    database: str = env_field(default="mydb", env_var="DB_NAME")

# Setup logging from environment
setup_telemetry()  # Uses PROVIDE_* env vars automatically

# Load configuration
db_config = DatabaseConfig.from_env()
logger.info("Database configured", host=db_config.host, port=db_config.port)
```

### Production Patterns

```python
# From examples/10_production_patterns.py
from provide.foundation import logger, error_boundary
import asyncio

class ProductionService:
    def __init__(self):
        self.logger = logger.bind(component="production_service")
        
    async def process_batch(self, items):
        """Process items with error boundaries."""
        results = []
        for item in items:
            with error_boundary(self.logger, f"item_{item['id']}"):
                result = await self.process_item(item)
                results.append(result)
        return results
```

---

## Configuration

### Environment Variables

All configuration can be controlled through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDE_SERVICE_NAME` | Service identifier in logs | `None` |
| `PROVIDE_LOG_LEVEL` | Minimum log level | `DEBUG` |
| `PROVIDE_LOG_CONSOLE_FORMATTER` | Output format (`key_value` or `json`) | `key_value` |
| `PROVIDE_LOG_OMIT_TIMESTAMP` | Remove timestamps from console | `false` |
| `PROVIDE_LOG_FILE` | Log to file path | `None` |
| `PROVIDE_LOG_MODULE_LEVELS` | Per-module log levels | `""` |
| `PROVIDE_CONFIG_PATH` | Configuration file path | `None` |
| `PROVIDE_ENV` | Environment (dev/staging/prod) | `dev` |
| `PROVIDE_DEBUG` | Enable debug mode | `false` |
| `PROVIDE_JSON_OUTPUT` | Force JSON output | `false` |
| `PROVIDE_NO_COLOR` | Disable colored output | `false` |

### Configuration Files

Support for YAML, JSON, TOML, and .env files:

```yaml
# config.yaml
service_name: my-app
environment: production

logging:
  level: INFO
  formatter: json
  file: /var/log/myapp.log

database:
  host: db.example.com
  port: 5432
  pool_size: 20
```

---

## Advanced Features

### Contextual Logging

```python
# From examples/06_trace_logging.py
from provide.foundation import logger

# Add context via structured fields
logger.info("request_processing",
            request_id="req-123",
            user_id="user-456",
            method="GET",
            path="/api/users")
```

### Timing and Profiling

```python
from provide.foundation import timed_block

with timed_block(logger, "database_query"):
    results = db.query("SELECT * FROM users")
# Automatically logs: "database_query completed duration_seconds=0.123"
```

### Async Support

```python
import asyncio
from provide.foundation import logger, process

async def process_items(items):
    for item in items:
        logger.info("Processing", item_id=item.id)
        await process_item(item)

# Async process execution
result = await process.async_run_command(["curl", "-s", "api.example.com"])
logger.info("API response", status=result.returncode)

# Thread-safe and async-safe logging
asyncio.run(process_items(items))
```

### Example Files

Complete working examples are available in the [examples/](examples/) directory:

- `00_simple_start.py` - Zero-setup logging (base install)
- `01_quick_start.py` - Full telemetry setup (requires [opentelemetry])
- `02_custom_configuration.py` - Custom telemetry configuration
- `03_named_loggers.py` - Module-specific loggers
- `04_das_logging.py` - Domain-Action-Status pattern
- `05_exception_handling.py` - Error handling patterns
- `06_trace_logging.py` - Distributed tracing
- `07_module_filtering.py` - Log filtering by module
- `08_env_variables_config.py` - Environment-based config
- `09_async_usage.py` - Async logging patterns
- `10_production_patterns.py` - Production best practices
- `11_config_management.py` - Complete configuration system
- `12_cli_application.py` - Full CLI application example

---

<p align="center">
  Built by <a href="https://provide.io">provide.io</a>
</p>
