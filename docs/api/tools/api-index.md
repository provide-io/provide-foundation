# Tools API

Development and utility tools for working with provide-foundation applications.

## Overview

The `tools` module provides a collection of development utilities, debugging aids, and operational tools to help with building, testing, and maintaining provide-foundation applications.

## Key Features

- **Code Generation**: Automatic code generation utilities
- **Development Server**: Built-in development server with hot reload
- **Debugging Tools**: Advanced debugging and profiling utilities
- **Migration Tools**: Database and configuration migration utilities
- **Validation Tools**: Configuration and data validation utilities
- **Performance Tools**: Benchmarking and performance analysis

## Code Generation

### Configuration Class Generation

```python
from provide.foundation.tools import codegen

# Generate configuration classes from schema
schema_definition = {
    "database": {
        "host": {"type": "string", "default": "localhost"},
        "port": {"type": "integer", "default": 5432},
        "name": {"type": "string", "required": True}
    },
    "cache": {
        "enabled": {"type": "boolean", "default": True},
        "ttl": {"type": "integer", "default": 300}
    }
}

# Generate Python dataclass
config_code = codegen.generate_config_class(
    schema_definition,
    class_name="AppConfig",
    output_file="config.py"
)

print(config_code)
# Output:
# @dataclass
# class AppConfig(BaseConfig):
#     database_host: str = "localhost"
#     database_port: int = 5432
#     database_name: str
#     cache_enabled: bool = True
#     cache_ttl: int = 300
```

### CLI Command Generation

```python
# Generate CLI commands from functions
@codegen.cli_command
def process_data(input_file: str, output_dir: str = "./output", verbose: bool = False):
    """Process data from input file and save to output directory."""
    # Function implementation
    pass

# Generates CLI interface automatically
generated_cli = codegen.generate_cli_module([process_data], module_name="data_cli")
```

## Development Server

### Built-in Dev Server

```python
from provide.foundation.tools import dev_server

# Create development server
server = dev_server.DevServer(
    app_module="myapp.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    reload_dirs=["src", "config"],
    log_level="DEBUG"
)

# Start with hot reload
await server.start()

# Server features:
# - Automatic reload on file changes
# - Enhanced error pages with stack traces
# - Request/response logging
# - Performance profiling
# - Configuration validation
```

### Hot Reload Configuration

```python
# Configure hot reload behavior
reload_config = dev_server.ReloadConfig(
    watch_directories=["src", "templates", "config"],
    ignore_patterns=["*.pyc", "*.log", "__pycache__/*"],
    reload_delay=0.5,  # Debounce file changes
    auto_restart=True
)

server = dev_server.DevServer(
    app_module="myapp.main:app",
    reload_config=reload_config
)
```

## Debugging Tools

### Interactive Debugger

```python
from provide.foundation.tools import debugger

# Drop into interactive debugger
@debugger.breakpoint
def problematic_function():
    # When called, opens interactive debugger
    result = complex_calculation()
    return result

# Conditional debugging
@debugger.breakpoint_if(lambda: os.getenv("DEBUG") == "true")
def debug_only_function():
    pass

# Remote debugging
@debugger.remote_breakpoint(host="localhost", port=5678)
def remote_debug_function():
    pass
```

### Performance Profiler

```python
from provide.foundation.tools import profiler

# Profile function execution
@profiler.profile
def expensive_function():
    # Function is automatically profiled
    time.sleep(1)
    return "result"

# Get profiling results
results = profiler.get_results()
profiler.print_stats()

# Line-by-line profiling
@profiler.line_profile
def detailed_function():
    # Each line is profiled individually
    x = expensive_operation()  # Line timing recorded
    y = another_operation(x)   # Line timing recorded
    return y

# Memory profiling
@profiler.memory_profile
def memory_intensive_function():
    # Memory usage tracked throughout execution
    data = load_large_dataset()
    processed = process_data(data)
    return processed
```

### Request Tracing

```python
from provide.foundation.tools import request_tracer

# Trace HTTP requests in development
tracer = request_tracer.RequestTracer()

@tracer.trace_requests
async def traced_handler(request):
    # All downstream requests are traced
    response = await external_api.call()
    return response

# View traced requests
traces = tracer.get_traces()
tracer.export_traces("traces.json")
```

## Migration Tools

### Database Migration

```python
from provide.foundation.tools import migration

# Create migration
migration_tool = migration.MigrationTool(database_url="postgresql://localhost/mydb")

# Generate migration from schema changes
migration_tool.create_migration(
    name="add_user_table",
    description="Add user table with indexes"
)

# Apply migrations
await migration_tool.migrate()

# Rollback migrations
await migration_tool.rollback(steps=1)
```

### Configuration Migration

```python
# Migrate configuration formats
config_migrator = migration.ConfigMigration()

# Convert YAML to TOML
await config_migrator.convert_format(
    source="config.yaml",
    target="config.toml",
    format_target="toml"
)

# Migrate configuration schema
await config_migrator.migrate_schema(
    config_file="config.yaml",
    from_version="1.0",
    to_version="2.0"
)
```

## Validation Tools

### Configuration Validator

```python
from provide.foundation.tools import validator

# Validate configuration files
config_validator = validator.ConfigValidator()

# Validate single file
validation_result = await config_validator.validate_file("config.yaml")
if not validation_result.is_valid:
    for error in validation_result.errors:
        print(f"Error: {error.message} at {error.path}")

# Validate directory of configs
results = await config_validator.validate_directory("config/")
```

### Data Validator

```python
# Validate data against schema
data_validator = validator.DataValidator(schema_file="user_schema.json")

# Validate single record
user_data = {"name": "John", "age": 30, "email": "john@example.com"}
result = data_validator.validate(user_data)

# Batch validation
validation_results = await data_validator.validate_batch(user_records)

# Generate validation report
report = data_validator.generate_report(validation_results)
```

## Performance Tools

### Benchmarking Suite

```python
from provide.foundation.tools import benchmark

# Benchmark functions
@benchmark.benchmark
def function_to_benchmark():
    # Function execution is timed
    return expensive_operation()

# Run benchmark suite
suite = benchmark.BenchmarkSuite()
suite.add_benchmark("json_serialization", test_json_serialization)
suite.add_benchmark("msgpack_serialization", test_msgpack_serialization)

results = await suite.run()
suite.generate_report(results, output="benchmark_report.html")
```

### Load Testing

```python
from provide.foundation.tools import load_test

# Create load test
load_tester = load_test.LoadTester()

# Define test scenarios
@load_tester.scenario(users=100, duration="5m")
async def api_load_test():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/users")
        assert response.status_code == 200

# Run load test
results = await load_tester.run()
load_tester.generate_report(results)
```

## Build Tools

### Project Builder

```python
from provide.foundation.tools import builder

# Build project
project_builder = builder.ProjectBuilder()

# Build for different environments
await project_builder.build(
    environment="production",
    optimize=True,
    include_tests=False
)

# Package application
await project_builder.package(
    format="docker",
    output_path="./dist/"
)
```

### Dependency Analyzer

```python
# Analyze project dependencies
analyzer = builder.DependencyAnalyzer()

# Find unused dependencies
unused_deps = await analyzer.find_unused()

# Check for security vulnerabilities
vulnerabilities = await analyzer.security_scan()

# Generate dependency report
report = await analyzer.generate_report()
```

## Testing Tools

### Test Generator

```python
from provide.foundation.tools import test_generator

# Generate tests from function signatures
@test_generator.generate_tests
def calculate_tax(income: float, rate: float = 0.2) -> float:
    """Calculate tax based on income and rate."""
    return income * rate

# Generates test cases automatically:
# - Test with valid inputs
# - Test with edge cases (0, negative numbers)
# - Test with invalid types
# - Test default parameter behavior
```

### Mock Data Generator

```python
# Generate mock data for testing
mock_generator = test_generator.MockDataGenerator()

# Generate from schema
user_schema = {
    "name": {"type": "string", "faker": "name"},
    "email": {"type": "string", "faker": "email"},
    "age": {"type": "integer", "min": 18, "max": 80},
    "active": {"type": "boolean", "probability": 0.8}
}

mock_users = mock_generator.generate(user_schema, count=100)
```

## Monitoring Tools

### Health Check Generator

```python
from provide.foundation.tools import monitoring

# Generate health checks
health_generator = monitoring.HealthCheckGenerator()

# Auto-generate from configuration
health_checks = health_generator.generate_from_config("config.yaml")

# Generate monitoring dashboard
dashboard_generator = monitoring.DashboardGenerator()
dashboard = dashboard_generator.generate(
    service_name="my-service",
    metrics_endpoint="http://localhost:9090",
    health_checks=health_checks
)
```

## CLI Tools

### Foundation CLI

```python
# Command-line interface for foundation tools
from provide.foundation.tools import cli

# Main CLI entry point
@cli.main
def foundation_cli():
    """Foundation development tools."""
    pass

@foundation_cli.command()
def init_project(name: str, template: str = "basic"):
    """Initialize new foundation project."""
    # Project initialization logic
    pass

@foundation_cli.command()
def validate_config(config_file: str):
    """Validate configuration file."""
    # Configuration validation logic
    pass

# Run CLI
if __name__ == "__main__":
    foundation_cli()
```

### Project Templates

```python
# Generate project from template
template_generator = cli.TemplateGenerator()

# Create new project
await template_generator.create_project(
    template="web-api",
    name="my-api",
    output_dir="./projects/",
    variables={
        "author": "John Doe",
        "database": "postgresql"
    }
)

# Available templates:
# - web-api: FastAPI-based web API
# - cli-app: Command-line application
# - worker: Background worker service
# - microservice: Containerized microservice
```

## Integration with IDEs

### VS Code Integration

```python
# Generate VS Code configuration
from provide.foundation.tools import ide_integration

vscode_config = ide_integration.VSCodeIntegration()

# Generate launch configurations
launch_configs = vscode_config.generate_launch_configs(
    main_module="myapp.main:app",
    debug_port=5678
)

# Generate settings
settings = vscode_config.generate_settings(
    python_path="./venv/bin/python",
    test_framework="pytest"
)

# Generate recommended extensions
extensions = vscode_config.generate_extensions()
```

## Best Practices

### Development Workflow
```python
# Use development server for local development
dev_server.start(hot_reload=True, debug=True)

# Profile performance-critical code
@profiler.profile
def critical_function():
    pass

# Validate configuration in CI
validator.validate_all_configs(exit_on_error=True)
```

### Testing Strategy
```python
# Generate comprehensive test suites
test_generator.generate_from_modules(["myapp.models", "myapp.services"])

# Use mock data for consistent testing
mock_data = mock_generator.generate_dataset("user_data", count=1000)
```

### Performance Monitoring
```python
# Continuous benchmarking
benchmark_suite.run_on_schedule(interval="daily")

# Load testing in staging
load_tester.run_on_deploy(environment="staging")
```

## API Reference

::: provide.foundation.tools

## Related Documentation

- [Development Guide](../../development/index.md) - Development workflow with tools
- [CLI Framework](../../guide/cli/index.md) - Building CLI applications
- [Testing Guide](../../guide/testing.md) - Testing with foundation tools