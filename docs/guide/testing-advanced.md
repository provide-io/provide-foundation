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

