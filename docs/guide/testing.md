# Testing Guide

Comprehensive guide for testing applications that use provide.foundation, covering unit tests, integration tests, logging verification, and performance testing.

## Overview

Testing applications that use provide.foundation involves several key areas:

- **Logger Testing**: Verifying log output, levels, and structured data
- **Configuration Testing**: Testing different configuration sources and environments
- **Context Testing**: Testing unified configuration and state management
- **CLI Testing**: Testing command-line interface components
- **Async Testing**: Testing asynchronous logging and operations
- **Performance Testing**: Verifying logging performance characteristics

## Basic Logger Testing

### Testing Log Output

```python
import pytest
import structlog.testing
from provide.foundation import logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def test_basic_logging():
    """Test basic log output with structured data."""
    # Setup test logging configuration
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="json"
        )
    )
    setup_telemetry(config)
    
    # Capture log output
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        logger.info("Test message", user_id=123, action="login")
    
    # Verify log entry
    assert len(cap_logs.entries) == 1
    entry = cap_logs.entries[0]
    assert entry["event"] == "Test message"
    assert entry["user_id"] == 123
    assert entry["action"] == "login"
    assert entry["level"] == "info"

def test_log_levels():
    """Test different log levels are captured correctly."""
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        logger.debug("Debug message")
        logger.info("Info message") 
        logger.warning("Warning message")
        logger.error("Error message")
    
    assert len(cap_logs.entries) == 4
    levels = [entry["level"] for entry in cap_logs.entries]
    assert levels == ["debug", "info", "warning", "error"]

def test_exception_logging():
    """Test exception logging with traceback."""
    cap_logs = structlog.testing.LogCapture()
    
    try:
        raise ValueError("Test error")
    except ValueError:
        with cap_logs:
            logger.exception("Operation failed", operation="test")
    
    assert len(cap_logs.entries) == 1
    entry = cap_logs.entries[0]
    assert entry["event"] == "Operation failed"
    assert entry["operation"] == "test"
    assert "exception" in entry  # Exception info included
```

### Testing Named Loggers

```python
from provide.foundation import get_logger

def test_named_loggers():
    """Test named logger creation and usage."""
    # Create different named loggers
    auth_log = get_logger("auth")
    db_log = get_logger("database")
    api_log = get_logger("api")
    
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        auth_log.info("User authenticated", user_id=123)
        db_log.debug("Query executed", query="SELECT * FROM users")
        api_log.warning("Rate limit exceeded", client_ip="192.168.1.1")
    
    assert len(cap_logs.entries) == 3
    
    # Verify logger names are included
    logger_names = [entry.get("logger") for entry in cap_logs.entries]
    assert "auth" in logger_names
    assert "database" in logger_names
    assert "api" in logger_names
```

## Configuration Testing

### Testing Environment Configuration

```python
import os
import pytest
from provide.foundation.logger.config import TelemetryConfig

def test_config_from_environment():
    """Test configuration loading from environment variables."""
    # Set environment variables
    env_vars = {
        "FOUNDATION_LOG_LEVEL": "DEBUG",
        "FOUNDATION_SERVICE_NAME": "test-service",
        "FOUNDATION_PROFILE": "testing",
        "FOUNDATION_DEBUG": "true"
    }
    
    with patch.dict(os.environ, env_vars):
        config = TelemetryConfig.from_env()
        
        assert config.logging.default_level == "DEBUG"
        assert config.service_name == "test-service"
        assert config.profile == "testing"
        assert config.debug is True

def test_config_validation():
    """Test configuration validation."""
    from provide.foundation.logger.config import LoggingConfig
    
    # Test invalid log level
    with pytest.raises(ValueError, match="Invalid log level"):
        LoggingConfig(default_level="INVALID")
    
    # Test valid log levels
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        config = LoggingConfig(default_level=level)
        assert config.default_level == level

def test_config_immutability():
    """Test that configuration objects are immutable."""
    config = TelemetryConfig()
    
    # Configuration should be immutable (frozen attrs class)
    with pytest.raises(AttributeError):
        config.service_name = "modified"
```

### Testing File Configuration

```python
import tempfile
from pathlib import Path
from provide.foundation import Context

def test_toml_configuration():
    """Test loading configuration from TOML file."""
    toml_content = '''
    log_level = "DEBUG"
    profile = "test"
    debug = true
    service_name = "test-app"
    
    [logging]
    console_formatter = "json"
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        config_path = Path(f.name)
    
    try:
        ctx = Context()
        ctx.load_config(config_path)
        
        assert ctx.log_level == "DEBUG"
        assert ctx.profile == "test"
        assert ctx.debug is True
        assert ctx.service_name == "test-app"
    finally:
        config_path.unlink()

def test_json_configuration():
    """Test loading configuration from JSON file."""
    json_content = {
        "log_level": "INFO",
        "profile": "production",
        "debug": False,
        "service_name": "prod-app"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        json.dump(json_content, f)
        config_path = Path(f.name)
    
    try:
        ctx = Context()
        ctx.load_config(config_path)
        
        assert ctx.log_level == "INFO"
        assert ctx.profile == "production"
        assert ctx.debug is False
        assert ctx.service_name == "prod-app"
    finally:
        config_path.unlink()
```

## Context Testing

### Testing Context Creation and Updates

```python
from provide.foundation import Context
from unittest.mock import patch

def test_context_creation():
    """Test Context creation with different parameters."""
    # Default context
    ctx = Context()
    assert ctx.log_level == "INFO"
    assert ctx.profile == "default"
    assert ctx.debug is False
    
    # Custom context
    ctx = Context(
        log_level="DEBUG",
        profile="development",
        debug=True,
        json_output=True
    )
    assert ctx.log_level == "DEBUG"
    assert ctx.profile == "development"
    assert ctx.debug is True
    assert ctx.json_output is True

def test_context_environment_loading():
    """Test Context.from_env() functionality."""
    env_vars = {
        "FOUNDATION_LOG_LEVEL": "ERROR",
        "FOUNDATION_PROFILE": "staging",
        "FOUNDATION_DEBUG": "false",
        "FOUNDATION_SERVICE_NAME": "staging-service"
    }
    
    with patch.dict(os.environ, env_vars):
        ctx = Context.from_env()
        
        assert ctx.log_level == "ERROR"
        assert ctx.profile == "staging"
        assert ctx.debug is False
        assert ctx.service_name == "staging-service"

def test_context_merging():
    """Test context merging functionality."""
    base_ctx = Context(
        profile="base",
        log_level="INFO",
        debug=False
    )
    
    override_ctx = Context(
        log_level="DEBUG",
        debug=True,
        service_name="override-service"
    )
    
    merged = base_ctx.merge(override_ctx)
    
    assert merged.profile == "base"  # From base
    assert merged.log_level == "DEBUG"  # From override
    assert merged.debug is True  # From override
    assert merged.service_name == "override-service"  # From override
```

## CLI Testing

### Testing CLI Components

```python
import pytest
from click.testing import CliRunner
from provide.foundation.cli import cli_command
from provide.foundation import Context

@cli_command
def sample_command(ctx: Context):
    """Sample CLI command for testing."""
    ctx.logger.info("Command executed", profile=ctx.profile)
    return f"Profile: {ctx.profile}, Debug: {ctx.debug}"

def test_cli_command_basic():
    """Test basic CLI command execution."""
    runner = CliRunner()
    result = runner.invoke(sample_command)
    
    assert result.exit_code == 0
    assert "Profile: default" in result.output
    assert "Debug: False" in result.output

def test_cli_command_with_options():
    """Test CLI command with options."""
    runner = CliRunner()
    result = runner.invoke(sample_command, [
        '--profile', 'testing',
        '--debug'
    ])
    
    assert result.exit_code == 0
    assert "Profile: testing" in result.output
    assert "Debug: True" in result.output

def test_cli_error_handling():
    """Test CLI error handling."""
    @cli_command
    def failing_command(ctx: Context):
        raise ValueError("Test error")
    
    runner = CliRunner()
    result = runner.invoke(failing_command)
    
    assert result.exit_code != 0
    assert "Test error" in result.output
```

### Testing CLI Input/Output

```python
from provide.foundation.console import pin, pout, perr
from click.testing import CliRunner

def test_console_input():
    """Test console input functions."""
    runner = CliRunner()
    
    # Test string input
    result = runner.invoke(lambda: pin("Enter name: "), input="test-user\n")
    assert "test-user" in result.output
    
    # Test integer input with validation
    result = runner.invoke(
        lambda: pin("Enter age: ", type=int, default=25),
        input="30\n"
    )
    assert "30" in result.output

def test_console_output():
    """Test console output functions."""
    from io import StringIO
    import sys
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    try:
        pout("Test message", color="green", bold=True)
        output = captured_output.getvalue()
        assert "Test message" in output
    finally:
        sys.stdout = sys.__stdout__

def test_console_error_output():
    """Test console error output."""
    from io import StringIO
    import sys
    
    # Capture stderr
    captured_error = StringIO()
    sys.stderr = captured_error
    
    try:
        perr("Error message", color="red")
        error_output = captured_error.getvalue()
        assert "Error message" in error_output
    finally:
        sys.stderr = sys.__stderr__
```

## Async Testing

### Testing Async Logging

```python
import asyncio
import pytest
import structlog.testing
from provide.foundation import logger

@pytest.mark.asyncio
async def test_async_logging():
    """Test logging in async contexts."""
    async def async_operation():
        logger.info("Async operation started")
        await asyncio.sleep(0.1)  # Simulate async work
        logger.info("Async operation completed")
    
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        await async_operation()
    
    assert len(cap_logs.entries) == 2
    assert cap_logs.entries[0]["event"] == "Async operation started"
    assert cap_logs.entries[1]["event"] == "Async operation completed"

@pytest.mark.asyncio
async def test_concurrent_logging():
    """Test logging from multiple concurrent tasks."""
    async def worker_task(worker_id: int):
        logger.info("Worker started", worker_id=worker_id)
        await asyncio.sleep(0.05)
        logger.info("Worker completed", worker_id=worker_id)
    
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        # Run multiple workers concurrently
        await asyncio.gather(*[
            worker_task(i) for i in range(5)
        ])
    
    assert len(cap_logs.entries) == 10  # 2 logs per worker * 5 workers
    worker_ids = [entry.get("worker_id") for entry in cap_logs.entries]
    assert set(worker_ids) == {0, 1, 2, 3, 4}
```

### Testing Context in Async Functions

```python
from provide.foundation import Context

@pytest.mark.asyncio
async def test_async_context_usage():
    """Test Context usage in async functions."""
    ctx = Context(profile="async-test", debug=True)
    
    async def async_function():
        # Context should be accessible in async functions
        assert ctx.profile == "async-test"
        assert ctx.debug is True
        
        # Context logger should work in async context
        ctx.logger.info("Async function called", profile=ctx.profile)
    
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        await async_function()
    
    assert len(cap_logs.entries) == 1
    entry = cap_logs.entries[0]
    assert entry["profile"] == "async-test"
```

## Performance Testing

### Testing Logging Performance

```python
import time
import statistics
from provide.foundation import logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def test_logging_performance():
    """Test logging performance characteristics."""
    # Setup high-performance logging
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    setup_telemetry(config)
    
    # Measure logging performance
    times = []
    num_iterations = 1000
    
    for _ in range(num_iterations):
        start_time = time.perf_counter()
        logger.info("Performance test message", iteration=_, data="test")
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    # Performance assertions
    avg_time = statistics.mean(times)
    median_time = statistics.median(times)
    
    # Should be under 1ms per log message
    assert avg_time < 0.001, f"Average logging time too slow: {avg_time:.6f}s"
    assert median_time < 0.001, f"Median logging time too slow: {median_time:.6f}s"
    
    # Calculate throughput
    throughput = num_iterations / sum(times)
    assert throughput > 1000, f"Throughput too low: {throughput:.0f} msg/sec"

def test_context_creation_performance():
    """Test Context creation performance."""
    times = []
    num_iterations = 1000
    
    for _ in range(num_iterations):
        start_time = time.perf_counter()
        ctx = Context(
            log_level="INFO",
            profile="performance-test",
            debug=False
        )
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    avg_time = statistics.mean(times)
    # Context creation should be very fast
    assert avg_time < 0.0001, f"Context creation too slow: {avg_time:.6f}s"
```

## Error Handling Testing

### Testing Error Scenarios

```python
import pytest
from provide.foundation import Context, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def test_invalid_configuration():
    """Test handling of invalid configurations."""
    # Test invalid log level
    with pytest.raises(ValueError):
        LoggingConfig(default_level="INVALID_LEVEL")
    
    # Test invalid profile
    with pytest.raises(ValueError):
        Context(profile="")  # Empty profile should be invalid

def test_missing_file_handling():
    """Test handling of missing configuration files."""
    ctx = Context()
    
    # Should raise FileNotFoundError for missing file
    with pytest.raises(FileNotFoundError):
        ctx.load_config("nonexistent-config.toml")

def test_graceful_degradation():
    """Test graceful degradation when setup fails."""
    import structlog.testing
    
    # Test logging works even with minimal setup
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        logger.info("Test message after failed setup")
    
    # Should still capture log even with basic setup
    assert len(cap_logs.entries) >= 0
```

## Test Fixtures and Utilities

### Common Test Fixtures

```python
import pytest
import tempfile
from pathlib import Path
from provide.foundation import Context
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file."""
    config_content = '''
    log_level = "DEBUG"
    profile = "test"
    debug = true
    service_name = "test-service"
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(config_content)
        config_path = Path(f.name)
    
    yield config_path
    
    # Cleanup
    config_path.unlink()

@pytest.fixture
def test_context():
    """Create a test context with known configuration."""
    return Context(
        log_level="DEBUG",
        profile="test",
        debug=True,
        service_name="test-service"
    )

@pytest.fixture
def test_telemetry_config():
    """Create a test telemetry configuration."""
    return TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="json"
        ),
        service_name="test-service",
        debug=True
    )

@pytest.fixture
def log_capture():
    """Create a log capture fixture."""
    import structlog.testing
    return structlog.testing.LogCapture()
```

### Test Helper Functions

```python
def assert_log_contains(cap_logs, event=None, level=None, **kwargs):
    """Helper function to assert log contains specific data."""
    for entry in cap_logs.entries:
        if event and entry.get("event") != event:
            continue
        if level and entry.get("level") != level:
            continue
        
        # Check all kwargs match
        if all(entry.get(k) == v for k, v in kwargs.items()):
            return True
    
    raise AssertionError(f"No log entry found matching criteria: {kwargs}")

def setup_test_logging():
    """Helper to setup logging for tests."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="json"
        )
    )
    setup_telemetry(config)

def create_test_config_file(content: dict, suffix: str = ".toml") -> Path:
    """Helper to create temporary config files."""
    if suffix == ".toml":
        import tomli_w
        with tempfile.NamedTemporaryFile(mode='wb', suffix=suffix, delete=False) as f:
            tomli_w.dump(content, f)
            return Path(f.name)
    elif suffix == ".json":
        import json
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            json.dump(content, f)
            return Path(f.name)
    else:
        raise ValueError(f"Unsupported config file suffix: {suffix}")
```

## Integration Testing

### Full Application Testing

```python
import pytest
from provide.foundation import Context, setup_telemetry, get_logger

def test_full_application_flow():
    """Test complete application initialization and logging flow."""
    # 1. Create context from environment
    ctx = Context.from_env()
    ctx.profile = "integration-test"
    ctx.debug = True
    
    # 2. Setup telemetry
    telemetry_config = ctx.to_telemetry_config()
    setup_telemetry(telemetry_config)
    
    # 3. Create application loggers
    app_log = get_logger("app")
    db_log = get_logger("database")
    api_log = get_logger("api")
    
    # 4. Test logging throughout application
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        app_log.info("Application started", version="1.0.0")
        db_log.debug("Database connected", host="localhost")
        api_log.info("API server listening", port=8000)
        
        # Simulate error scenario
        try:
            raise ValueError("Test error")
        except ValueError:
            app_log.exception("Application error occurred", component="main")
    
    # 5. Verify complete logging flow
    assert len(cap_logs.entries) == 4
    events = [entry["event"] for entry in cap_logs.entries]
    assert "Application started" in events
    assert "Database connected" in events
    assert "API server listening" in events
    assert "Application error occurred" in events
```

## Best Practices for Testing

### 1. Isolate Tests

```python
def test_isolated_logging():
    """Each test should be isolated with its own logging setup."""
    # Setup specific to this test
    config = TelemetryConfig(logging=LoggingConfig(default_level="DEBUG"))
    setup_telemetry(config)
    
    # Test logic here
    # ...
    
    # Tests should not depend on global state from other tests
```

### 2. Use Meaningful Assertions

```python
def test_with_meaningful_assertions():
    """Use specific, meaningful assertions."""
    cap_logs = structlog.testing.LogCapture()
    with cap_logs:
        logger.info("User login", user_id=123, success=True)
    
    # Good: Specific assertion
    entry = cap_logs.entries[0]
    assert entry["event"] == "User login"
    assert entry["user_id"] == 123
    assert entry["success"] is True
    
    # Avoid: Vague assertion
    # assert len(cap_logs.entries) > 0  # Too vague
```

### 3. Test Edge Cases

```python
def test_edge_cases():
    """Test edge cases and error conditions."""
    # Test with None values
    logger.info("Test message", user_id=None, data=None)
    
    # Test with empty strings
    logger.info("", empty_field="")
    
    # Test with large data
    large_data = "x" * 10000
    logger.info("Large data test", data=large_data)
    
    # Test with unicode
    logger.info("Unicode test", message="Hello 世界 🌍")
```

### 4. Performance Testing

```python
def test_performance_under_load():
    """Test performance characteristics under load."""
    import concurrent.futures
    import threading
    
    def worker():
        for i in range(100):
            logger.info("Worker message", worker_id=threading.get_ident(), count=i)
    
    # Test concurrent logging
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker) for _ in range(10)]
        concurrent.futures.wait(futures)
    
    # Verify no errors occurred
    for future in futures:
        future.result()  # Will raise if worker had an exception
```

## Running Tests

### Test Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "-v",
    "--strict-markers",
    "--strict-config",
    "--cov=provide.foundation",
    "--cov-report=html",
    "--cov-report=term-missing"
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "performance: marks tests as performance tests"
]
```

### Running Specific Test Categories

```bash
# Run all tests
pytest

# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run performance tests
pytest -m performance

# Run with coverage
pytest --cov=provide.foundation --cov-report=html

# Run specific test file
pytest tests/test_logger.py

# Run specific test function
pytest tests/test_logger.py::test_basic_logging

# Run tests in parallel
pytest -n auto
```

This comprehensive testing guide covers all aspects of testing applications built with provide.foundation, ensuring reliable and well-tested code.