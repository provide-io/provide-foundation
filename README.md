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
    <img alt="Test Coverage" src="https://img.shields.io/badge/coverage-83.65%25-brightgreen.svg">
    <img alt="Test Count" src="https://img.shields.io/badge/tests-1000+-blue.svg">
    <img alt="Type Checking" src="https://img.shields.io/badge/typing-mypy-informational.svg">
    <a href="https://github.com/provide-io/provide-foundation/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/provide-io/provide-foundation.svg">
    </a>
</p>

---

**provide.foundation** is a comprehensive foundation library for Python applications, offering structured logging, CLI utilities, configuration management, error handling, and essential application building blocks. Built with modern Python practices, it provides the core infrastructure that production applications need.

> **Performance**: Benchmarked at >14,000 msg/sec under optimal conditions with minimal allocations. Actual performance varies based on configuration, system resources, and usage patterns.

## 🏆 Quality & Testing Achievements

**provide.foundation** maintains high standards for code quality, testing, and reliability:

- **83.65% Test Coverage** with 1000+ comprehensive tests
- **46 modules with 100% coverage** including core components
- **Comprehensive Security Testing** with path traversal, symlink validation, and input sanitization
- **Performance Benchmarked** logging, transport, and archive operations
- **Type-Safe Codebase** with comprehensive type annotations
- **Automated Quality Checks** with ruff, mypy, and bandit

### Recent Testing Improvements

| Component | Before | After | Tests Added |
|-----------|---------|--------|-------------|
| CLI Commands | 14-15% | 78-95% | 49 comprehensive tests |
| OTLP Integration | 0% | 86.75% | 21 integration tests |
| Archive Security | Basic | 100% | 15 security edge cases |
| Transport Layer | 74% | 91% | 22 edge case tests |

📊 **See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed roadmap and quality metrics**

---

## Prerequisites

> **Important:** This project uses `uv` for Python environment and package management.

### Install UV

Visit [UV Documentation](https://github.com/astral-sh/uv) for more information.

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pipx (if you prefer)
pipx install uv

# Update UV to latest version
uv self update
```

## Getting Started

### Development Setup

```bash
# Clone the repository
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Installing as a Package

```bash
# Install from PyPI
uv add provide-foundation

# Or install from source
uv add git+https://github.com/provide-io/provide-foundation.git

# Or using pip (if you prefer)
pip install provide-foundation
```

### Optional Dependencies

provide.foundation has optional feature sets that require additional dependencies:

| Feature | Install Command | Required For |
|---------|----------------|--------------|
| **Basic logging** | `pip install provide-foundation` | Core logging functionality |
| **CLI framework** | `pip install provide-foundation[cli]` | Command-line interface features |
| **Cryptography** | `pip install provide-foundation[crypto]` | Hash functions, digital signatures, certificates |
| **HTTP Transport** | `pip install provide-foundation[transport]` | HTTP client utilities and transport features |
| **OpenTelemetry** | `pip install provide-foundation[opentelemetry]` | Distributed tracing and metrics |
| **All features** | `pip install provide-foundation[all]` | Everything above |

> **Quick Start Tip**: For immediate use with just logging, install the base package. Add extras as needed.

---

## Testing with provide-foundation

### Required Testing Dependencies

When testing applications that use provide-foundation, **`provide-testkit` is mandatory**:

```bash
# Install testkit for development/testing
uv add provide-testkit --group dev

# Or with pip
pip install provide-testkit
```

### Essential Testing Pattern

```python
import pytest
from provide.testkit import (
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
)
from provide.foundation import logger

@pytest.fixture(autouse=True)
def reset_foundation():
    """Reset Foundation state before each test."""
    reset_foundation_setup_for_testing()

def test_foundation_logging():
    """Test Foundation logger functionality."""
    import sys

    # Capture Foundation logs for testing
    set_log_stream_for_testing(sys.stderr)

    # Use Foundation logger
    logger.info("Test message", component="test")
    # Your test assertions here...
```

### Key Testing Features

- **Automatic Context Detection**: TestKit detects testing environments automatically
- **Foundation Reset**: Clean state between tests via `reset_foundation_setup_for_testing()`
- **Log Capture**: Direct Foundation logs to streams for assertions
- **CLI Testing**: Comprehensive Click application testing utilities
- **Mock Integration**: Foundation-aware mocks and fixtures

> **Note**: If provide-testkit is not available, pause development and install it. Foundation-based applications require testkit fixtures for reliable testing.

---

## What's Included

### Core Components

#### **Structured Logging**
Beautiful, performant logging built on `structlog` with event-enriched structured logging and zero configuration required.

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
# From examples/cli/01_cli_application.py
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
# From examples/configuration/03_config_management.py
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
# From examples/telemetry/05_exception_handling.py
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
# From examples/cli/01_cli_application.py
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
# From examples/cli/01_cli_application.py
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
# From examples/configuration/03_config_management.py and examples/configuration/02_env_variables.py
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
# From examples/production/01_production_patterns.py
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
| `PROVIDE_LOG_LEVEL` | Minimum log level | `WARNING` |
| `PROVIDE_LOG_CONSOLE_FORMATTER` | Output format (`key_value` or `json`) | `key_value` |
| `PROVIDE_LOG_OMIT_TIMESTAMP` | Remove timestamps from console | `false` |
| `PROVIDE_LOG_FILE` | Log to file path | `None` |
| `PROVIDE_LOG_MODULE_LEVELS` | Per-module log levels (format: module1:LEVEL,module2:LEVEL) | `""` |
| `PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED` | Enable emoji prefixes based on logger names | `true` |
| `PROVIDE_LOG_DAS_EMOJI_ENABLED` | Enable Domain-Action-Status emoji prefixes | `true` |
| `PROVIDE_TELEMETRY_DISABLED` | Globally disable telemetry | `false` |
| `PROVIDE_SERVICE_VERSION` | Service version for telemetry | `None` |
| `FOUNDATION_LOG_LEVEL` | Log level for Foundation internal setup messages | `INFO` |
| `OTEL_SERVICE_NAME` | OpenTelemetry service name (takes precedence over PROVIDE_SERVICE_NAME) | `None` |
| `OTEL_TRACING_ENABLED` | Enable OpenTelemetry tracing | `true` |
| `OTEL_METRICS_ENABLED` | Enable OpenTelemetry metrics | `true` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint for traces and metrics | `None` |
| `OTEL_EXPORTER_OTLP_HEADERS` | Headers for OTLP requests (key1=value1,key2=value2) | `""` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (grpc, http/protobuf) | `http/protobuf` |
| `OTEL_TRACE_SAMPLE_RATE` | Sampling rate for traces (0.0 to 1.0) | `1.0` |

**Rate Limiting Configuration:**

| Variable | Description | Default |
|----------|-------------|---------|
| `PROVIDE_LOG_RATE_LIMIT_ENABLED` | Enable rate limiting for log output | `false` |
| `PROVIDE_LOG_RATE_LIMIT_GLOBAL` | Global rate limit (logs per second) | `None` |
| `PROVIDE_LOG_RATE_LIMIT_GLOBAL_CAPACITY` | Global rate limit burst capacity | `None` |
| `PROVIDE_LOG_RATE_LIMIT_PER_LOGGER` | Per-logger rate limits (format: logger1:rate:capacity,logger2:rate:capacity) | `""` |
| `PROVIDE_LOG_RATE_LIMIT_EMIT_WARNINGS` | Emit warnings when logs are rate limited | `true` |
| `PROVIDE_LOG_RATE_LIMIT_SUMMARY_INTERVAL` | Seconds between rate limit summary reports | `5.0` |
| `PROVIDE_LOG_RATE_LIMIT_MAX_QUEUE_SIZE` | Maximum number of logs to queue when rate limited | `1000` |
| `PROVIDE_LOG_RATE_LIMIT_MAX_MEMORY_MB` | Maximum memory (MB) for queued logs | `None` |
| `PROVIDE_LOG_RATE_LIMIT_OVERFLOW_POLICY` | Policy when queue is full: drop_oldest, drop_newest, or block | `drop_oldest` |

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

## OpenTelemetry Integration

provide.foundation includes built-in OpenTelemetry support for distributed tracing and metrics collection.

### Basic Setup

```python
from provide.foundation import setup_telemetry

# Basic setup with default OTLP exporter
setup_telemetry()

# With custom configuration
from provide.foundation import TelemetryConfig

config = TelemetryConfig(
    service_name="my-service",
    service_version="1.0.0",
    tracing_enabled=True,
    metrics_enabled=True,
    otlp_endpoint="http://localhost:4317"
)
setup_telemetry(config)
```

### Environment Configuration

Set these environment variables to configure OpenTelemetry:

```bash
# Service identification
export OTEL_SERVICE_NAME="my-service"
export PROVIDE_SERVICE_VERSION="1.0.0"

# OTLP endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"  # or "http/protobuf"

# Authentication (if required)
export OTEL_EXPORTER_OTLP_HEADERS="api-key=your-key,other-header=value"

# Sampling
export OTEL_TRACE_SAMPLE_RATE="1.0"  # Sample 100% of traces
```

### Usage with Jaeger

```bash
# Run Jaeger all-in-one for testing
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14250:14250 \
  jaegertracing/all-in-one:latest

# Configure your application
export OTEL_SERVICE_NAME="my-app"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:14250"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
```

### Usage with OTLP-compatible backends

```python
# Works with Honeycomb, Lightstep, New Relic, etc.
from provide.foundation import setup_telemetry

setup_telemetry()  # Uses environment variables
```

---

## Advanced Features

### Contextual Logging

```python
# From examples/telemetry/06_trace_logging.py
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

- `examples/telemetry/01_basic_logging.py` - Zero-setup logging (base install)
- `examples/telemetry/02_structured_logging.py` - Structured logging with context
- `examples/telemetry/03_named_loggers.py` - Module-specific loggers
- `examples/telemetry/04_das_pattern.py` - Domain-Action-Status pattern
- `examples/telemetry/05_exception_handling.py` - Error handling patterns
- `examples/telemetry/06_trace_logging.py` - Distributed tracing
- `examples/telemetry/07_module_filtering.py` - Log filtering by module
- `examples/configuration/02_env_variables.py` - Environment-based config
- `examples/async/01_async_usage.py` - Async logging patterns
- `examples/production/01_production_patterns.py` - Production best practices
- `examples/configuration/03_config_management.py` - Complete configuration system
- `examples/cli/01_cli_application.py` - Full CLI application example
- `examples/tracing/01_simple_tracing.py` - OpenTelemetry tracing setup
- `examples/tracing/02_distributed_tracing.py` - Distributed tracing patterns
- `examples/integration/celery/` - Celery task processing integration (requires `pip install celery`)

---

<p align="center">
  Built by <a href="https://provide.io">provide.io</a>
</p>
# Trigger CI pipeline test
