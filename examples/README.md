# Foundation Examples

This directory contains practical examples demonstrating various features and usage patterns of provide-foundation. Examples are organized by feature area for easy discovery and learning.

## Directory Structure

### [telemetry/](telemetry/) - Core Logging and Telemetry
- `01_basic_logging.py` - Zero-setup logging with Foundation
- `02_structured_logging.py` - Structured logging with full telemetry setup
- `03_named_loggers.py` - Component-specific named loggers  
- `04_das_pattern.py` - Domain-Action-Status structured logging
- `05_exception_handling.py` - Exception logging with automatic tracebacks
- `06_trace_logging.py` - TRACE level logging for verbose output
- `07_module_filtering.py` - Module-specific log level configuration

### [configuration/](configuration/) - Configuration Management
- `01_custom_config.py` - Custom TelemetryConfig and LoggingConfig
- `02_env_variables.py` - Environment variable configuration
- `03_config_management.py` - Complete configuration system with file loading

### [async/](async/) - Asynchronous Programming
- `01_async_usage.py` - Using Foundation with asyncio applications

### [cli/](cli/) - Command Line Interface Development
- `01_cli_application.py` - Complete CLI with Hub and command system

### [transport/](transport/) - HTTP Client and Networking
- `01_http_client.py` - HTTP requests with middleware and error handling

### [tracing/](tracing/) - Distributed Tracing
- `01_simple_tracing.py` - Basic tracing with Foundation
- `02_distributed_tracing.py` - Distributed tracing across services

### [integration/](integration/) - Third-Party Integrations
- `01a_basic_task_queue.py` - Task queue patterns with async workers (no external deps)
- [celery/](integration/celery/) - Celery task queue integration
  - `01_setup_and_config.py` - Celery setup and configuration
  - `02_metrics_and_signals.py` - Metrics collection and signal handling
  - `03_tasks.py` - Task definitions and execution
  - `04_runner.py` - Running Celery workers
  - `05_cut_up_chuck_tasks.py` - Advanced task patterns
  - `06_cut_up_chuck_runner.py` - Advanced runner patterns

### [openobserve/](openobserve/) - OpenObserve Integration
- `01_openobserve_integration.py` - Log aggregation with OpenObserve
- `02_metrics_integration.py` - Metrics integration with OpenObserve

### [di/](di/) - Dependency Injection
- `01_polyglot_di_pattern.py` - Polyglot dependency injection patterns

### [production/](production/) - Production Patterns
- `01_production_patterns.py` - Production-focused logging and monitoring
- `02_error_handling.py` - Comprehensive error handling with resilience patterns

## Running Examples

Navigate to any directory and run the examples:

```bash
# Core telemetry features
cd telemetry
python 01_basic_logging.py

# Configuration management
cd configuration  
python 01_custom_config.py

# HTTP client usage
cd transport
python 01_http_client.py

# CLI development
cd cli
python 01_cli_application.py
```

## Example Categories

### Getting Started
Start with `telemetry/01_basic_logging.py` for the simplest introduction, then explore `telemetry/02_structured_logging.py` for a complete setup.

### Configuration
Learn how to configure Foundation through code (`configuration/01_custom_config.py`) or environment variables (`configuration/02_env_variables.py`).

### Production Use
See `production/01_production_patterns.py` for patterns suitable for production deployments with structured JSON logging and health metrics.

### Advanced Features
Explore tracing, transport clients, and integrations for building robust distributed systems.

## Common Patterns

All examples demonstrate these Foundation patterns:

- **Structured Logging**: Key-value logging with contextual information
- **Configuration**: Environment-based configuration without hardcoded defaults
- **Error Handling**: Comprehensive error logging with tracebacks
- **Performance**: Efficient logging suitable for high-throughput applications
- **Observability**: Built-in metrics and tracing capabilities

## Notes

- All examples use Foundation's native console utilities (`pout`, `perr`) instead of `print()`
- Examples demonstrate proper dogfooding by using only Foundation's own tools and dependencies
- No external network calls - transport examples use Foundation's mocking utilities

## Documentation

For complete API documentation, see:
- [Foundation Documentation](../docs/)
- [API Reference](../docs/reference/)
- [How-To Guides](../docs/how-to-guides/)