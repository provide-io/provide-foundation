# Examples

The Foundation repository includes a comprehensive collection of working examples demonstrating all major features. All examples are located in the `examples/` directory of the source repository.

## Running Examples

Clone the repository and run any example:

```bash
git clone https://github.com/provide-io/provide-foundation.git
cd provide-foundation
uv sync --all-extras

# Run an example
uv run python examples/telemetry/01_basic_logging.py
```

## Example Categories

### Getting Started

Perfect for learning the basics:

- **[telemetry/01_basic_logging.py](https://github.com/provide-io/provide-foundation/blob/main/examples/telemetry/01_basic_logging.py)** - Zero-setup logging introduction
- **[telemetry/02_structured_logging.py](https://github.com/provide-io/provide-foundation/blob/main/examples/telemetry/02_structured_logging.py)** - Structured logging with full Hub setup

### Telemetry & Logging

Core logging features and patterns:

- **01_basic_logging.py** - Simple start with zero configuration
- **02_structured_logging.py** - Hub-based initialization and configuration
- **03_named_loggers.py** - Component-specific named loggers
- **04_das_pattern.py** - Domain-Action-Status structured logging
- **05_exception_handling.py** - Exception logging with automatic tracebacks
- **06_trace_logging.py** - TRACE level logging for verbose output
- **07_module_filtering.py** - Module-specific log level configuration

**[View telemetry examples](https://github.com/provide-io/provide-foundation/tree/main/examples/telemetry)**

### Configuration Management

Environment and file-based configuration:

- **01_custom_config.py** - Custom TelemetryConfig and LoggingConfig
- **02_env_variables.py** - Environment variable configuration
- **03_config_management.py** - Complete configuration system with file loading

**[View configuration examples](https://github.com/provide-io/provide-foundation/tree/main/examples/configuration)**

### CLI Applications

Build command-line tools:

- **01_cli_application.py** - Complete CLI with Hub and command system
- **02_dogfooding_cli.py** - Foundation CLI using its own tools

**[View CLI examples](https://github.com/provide-io/provide-foundation/tree/main/examples/cli)**

### Async Programming

Using Foundation with asyncio:

- **01_async_usage.py** - Async application patterns with Foundation

**[View async examples](https://github.com/provide-io/provide-foundation/tree/main/examples/async)**

### HTTP Transport

HTTP client usage with middleware:

- **01_http_client.py** - HTTP requests with middleware and error handling

**[View transport examples](https://github.com/provide-io/provide-foundation/tree/main/examples/transport)**

### Distributed Tracing

OpenTelemetry integration:

- **01_simple_tracing.py** - Basic tracing with Foundation
- **02_distributed_tracing.py** - Distributed tracing across services

**[View tracing examples](https://github.com/provide-io/provide-foundation/tree/main/examples/tracing)**

### File Operations

Safe file handling and monitoring:

- **01_basic_usage.py** - Basic file operations
- **02_streaming_detection.py** - Detect streaming file changes
- **03_real_filesystem_monitoring.py** - Monitor filesystem events
- **04_quality_analysis.py** - File quality analysis

**[View file examples](https://github.com/provide-io/provide-foundation/tree/main/examples/file_operations)**

### Dependency Injection

Polyglot dependency injection patterns:

- **01_polyglot_di_pattern.py** - Dependency injection using the Hub system

**[View DI examples](https://github.com/provide-io/provide-foundation/tree/main/examples/di)**

### Production Patterns

Production-focused application patterns:

- **01_production_patterns.py** - Production logging and monitoring
- **02_error_handling.py** - Comprehensive error handling with resilience

**[View production examples](https://github.com/provide-io/provide-foundation/tree/main/examples/production)**

### Integration Examples

Third-party integrations:

#### Celery Integration
- **01_setup_and_config.py** - Celery setup and configuration
- **02_metrics_and_signals.py** - Metrics collection and signal handling
- **03_tasks.py** - Task definitions
- **04_runner.py** - Running Celery workers

**[View Celery examples](https://github.com/provide-io/provide-foundation/tree/main/examples/integration/celery)**

#### OpenObserve Integration
- **01_openobserve_integration.py** - Log aggregation with OpenObserve
- **02_metrics_integration.py** - Metrics integration with OpenObserve

**[View OpenObserve examples](https://github.com/provide-io/provide-foundation/tree/main/examples/openobserve)**

#### Task Queue Patterns
- **01a_basic_task_queue.py** - Task queue patterns with async workers (no external dependencies)

**[View all integration examples](https://github.com/provide-io/provide-foundation/tree/main/examples/integration)**

## Example Structure

Each example includes:

- **Complete working code** - Copy and run immediately
- **Inline documentation** - Explains what each section does
- **Expected output** - Shows what you should see
- **Usage instructions** - How to run and customize

## Common Patterns

All examples demonstrate these Foundation patterns:

### Structured Logging
```python
from provide.foundation import logger

logger.info(
    "user_action",
    user_id="123",
    action="login",
    source="web",
)
```

### Configuration
```python
from provide.foundation import get_hub
from provide.foundation.logger.config import TelemetryConfig

hub = get_hub()
hub.initialize_foundation(
    TelemetryConfig(service_name="my-service")
)
```

### Error Handling
```python
from provide.foundation import logger

try:
    # Operation that might fail
    process_data()
except Exception as e:
    logger.exception("operation_failed", operation="process_data")
    raise
```

### Output Separation
```python
from provide.foundation import logger, pout, perr

# System logs (for operators)
logger.info("processing_file", filename="data.csv")

# User output (for CLI users)
pout("✅ File processed successfully", color="green")
```

## Running All Examples

Test all examples at once:

```bash
# From the repository root
for example in examples/**/*.py; do
    echo "Running $example..."
    python "$example"
done
```

## Contributing Examples

Examples are always welcome! If you've built something useful:

1. Fork the repository
2. Add your example to the appropriate category
3. Include documentation and expected output
4. Submit a pull request

See [CONTRIBUTING.md](https://github.com/provide-io/provide-foundation/blob/main/CONTRIBUTING.md) for guidelines.

## Next Steps

After exploring examples:

- **[How-To Guides](../how-to-guides/logging/basic-logging.md)** - Solve specific problems
- **[API Reference](../reference/index.md)** - Detailed API documentation
- **[Explanation](../explanation/architecture.md)** - Understand architecture

---

**Browse all examples:** [github.com/provide-io/provide-foundation/tree/main/examples](https://github.com/provide-io/provide-foundation/tree/main/examples)
