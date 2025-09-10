# Examples

Practical examples demonstrating provide-foundation features and patterns.

## Available Examples

### Basic Application
[Basic Application](basic-app.md) - Simple application setup with logging

### CLI Tool  
[CLI Tool](cli-tool.md) - Command-line interface with argument handling

### Web Service
[Web Service](web-service.md) - HTTP service with structured logging

### Data Pipeline
[Data Pipeline](data-pipeline.md) - Data processing with error handling

### Transport Client
HTTP client usage with middleware, error handling, and streaming

## Running Examples

All examples are available in the project's `examples/` directory:

```bash
cd examples
python 01_quick_start.py         # Basic logging and telemetry
python 02_basic_app.py           # Application structure
python 03_cli_tool.py            # CLI development  
python 04_web_service.py         # HTTP service
python 05_data_pipeline.py       # Data processing
python 06_transport_client.py    # HTTP client
```

Each example is self-contained and demonstrates specific features:

- **Structured logging** with contextual information
- **Configuration management** from environment and files  
- **Error handling** with resilience patterns
- **CLI development** with automatic help generation
- **HTTP client operations** with middleware and retries
- **Performance monitoring** with metrics collection

## Example Patterns

### Basic Setup

```python
from provide.foundation import logger, setup_telemetry

# Setup telemetry
setup_telemetry()

# Use structured logging
logger.info("application_started", version="1.0.0")
```

### CLI Application

```python
from provide.foundation.hub import register_command
from provide.foundation.console import pout

@register_command("hello")
def hello_command(name: str = "World"):
    """Say hello to someone."""
    pout(f"Hello, {name}!")
```

### Configuration

```python
from provide.foundation.config import BaseConfig
from attrs import define

@define
class AppConfig(BaseConfig):
    debug: bool = False
    port: int = 8080

config = AppConfig.from_env()
```

## Next Steps

- Browse the [API Reference](../api/api-index.md) for detailed documentation
- Check the [User Guide](../guide/index.md) for comprehensive patterns
- Explore the source code in the `examples/` directory