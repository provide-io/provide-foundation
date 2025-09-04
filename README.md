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

---

## What's Included

### Core Components

#### **Structured Logging**
Beautiful, performant logging built on `structlog` with zero configuration required.

```python
from provide.foundation import logger

logger.info("Application started", version="1.0.0")
logger.error("Database connection failed", host="db.example.com", retry_count=3)
```

#### **CLI Framework**
Build command-line interfaces with automatic help generation, configuration loading, and output formatting.

```python
import click
from provide.foundation.cli import cli_command, setup_cli_logging

@cli_command()
@click.option("--name", help="Your name")
def greet(name):
    """A simple greeting command."""
    logger.info("Greeting user", name=name)
    print(f"Hello, {name}!")
```

#### **Configuration Management**
Flexible configuration system supporting environment variables, files, and runtime updates.

```python
from provide.foundation.config import ConfigManager, BaseConfig

class AppConfig(BaseConfig):
    api_key: str
    timeout: int = 30
    debug: bool = False

manager = ConfigManager()
manager.register("app", AppConfig)
config = manager.get_config("app")
```

#### **Error Handling**
Comprehensive error handling with retry logic, circuit breakers, and error boundaries.

```python
from provide.foundation import retry_on_error, with_error_handling

@retry_on_error(max_attempts=3, delay=1.0)
def flaky_network_call():
    return api.fetch_data()

@with_error_handling(fallback={"status": "error"})
def parse_response(data):
    return json.loads(data)
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

#### **Registry Pattern**
Flexible registry system for managing plugins, commands, and extensions.

```python
from provide.foundation.hub import Registry

registry = Registry("plugins")
registry.register("auth", AuthPlugin())
registry.register("cache", CachePlugin())

# Use registered items
auth = registry.get("auth")
all_plugins = registry.list_all()
```

#### **File Operations**
Safe file operations with atomic writes, file locking, and path utilities.

```python
from provide.foundation.file import atomic_write, FileLock, ensure_directory

# Atomic file writes
atomic_write("config.json", json.dumps(data))

# File locking
with FileLock("data.lock"):
    # Exclusive access to resource
    process_data()

# Path utilities
ensure_directory("logs", mode=0o755)
```

#### **Process Management**
Run and manage external processes with timeout, streaming output, and async support.

```python
from provide.foundation.process import run_command, AsyncCommandRunner

# Synchronous execution
result = run_command("git status", timeout=5.0)
print(result.stdout)

# Async execution with streaming
async def build_project():
    runner = AsyncCommandRunner()
    async for line in runner.run_streaming("npm build"):
        logger.info("Build output", line=line)
```

#### **Platform Detection**
Comprehensive platform and environment detection utilities.

```python
from provide.foundation.platform import PlatformInfo

info = PlatformInfo()
print(f"OS: {info.os_name}")
print(f"Python: {info.python_version}")
print(f"In Docker: {info.in_docker}")
print(f"In CI: {info.in_ci}")
```

---

## Quick Start Examples

### Building a CLI Application

```python
import click
from provide.foundation import logger
from provide.foundation.cli import cli_command, Context

@click.group()
@cli_command()
@click.pass_context
def cli(ctx):
    """My application CLI."""
    ctx.obj = Context()

@cli.command()
@cli_command()
def status():
    """Check application status."""
    logger.info("Checking status")
    # Your status logic here

@cli.command()
@cli_command()
@click.option("--input", required=True, help="Input file")
@click.option("--output", default="output.txt", help="Output file")
def process(input, output):
    """Process a file."""
    logger.info("Processing", input=input, output=output)
    # Your processing logic here

if __name__ == "__main__":
    cli()
```

### Configuration-Driven Application

```python
from provide.foundation import setup_telemetry, TelemetryConfig, LoggingConfig
from provide.foundation.config import ConfigManager, BaseConfig

# Define your configuration schema
class DatabaseConfig(BaseConfig):
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    
class AppConfig(BaseConfig):
    debug: bool = False
    workers: int = 4
    database: DatabaseConfig = DatabaseConfig()

# Setup logging
setup_telemetry(TelemetryConfig(
    service_name="my-app",
    logging=LoggingConfig(default_level="INFO")
))

# Load configuration
manager = ConfigManager()
manager.register("app", AppConfig)
config = manager.load_from_env()  # or load_from_file("config.yaml")
```

### Error-Resilient Service

```python
from provide.foundation import logger, circuit_breaker
from provide.foundation.errors import retry_on_error

class DataService:
    @circuit_breaker(failure_threshold=5, recovery_timeout=60)
    @retry_on_error(max_attempts=3, backoff="exponential")
    def fetch_data(self, endpoint):
        """Fetch data with automatic retry and circuit breaking."""
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def process_safely(self, data):
        """Process data with error boundaries."""
        with error_boundary(logger, "data_processing"):
            # Complex processing logic
            return transform_data(data)
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
from provide.foundation import logger

# Bind context to a logger
request_logger = logger.bind(
    request_id="req-123",
    user_id="user-456"
)

# All logs include the bound context
request_logger.info("Processing request")
request_logger.error("Request failed", error_code=500)
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
from provide.foundation import logger

async def process_items(items):
    for item in items:
        logger.info("Processing", item_id=item.id)
        await process_item(item)
        
# Thread-safe and async-safe logging
asyncio.run(process_items(items))
```

### Testing Utilities

```python
import pytest
from provide.foundation.testing import captured_logs, temp_config

def test_my_function():
    with captured_logs() as logs:
        my_function()
    
    assert "expected message" in logs.text
    assert logs.records[0]["level"] == "info"

def test_with_config():
    with temp_config({"debug": True}):
        assert config.debug is True
```

---

## Performance

- **Logging**: 14,000+ messages/second with full structured logging
- **Configuration**: Lazy loading with caching for optimal performance  
- **File Operations**: Atomic writes prevent corruption
- **Process Management**: Efficient streaming with backpressure support

---

## Contributing

We welcome contributions! Please see:
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development setup and guidelines
- [GitHub Issues](https://github.com/provide-io/provide-foundation/issues) - Bug reports and feature requests

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built by <a href="https://provide.io">Provide</a>
</p>