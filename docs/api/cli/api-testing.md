# CLI Testing API

Testing utilities specifically designed for CLI applications built with Click and provide.foundation.

## Overview

The CLI testing module provides:

- **Isolated test environments** - Filesystem and environment isolation
- **Configuration file helpers** - Temporary config files for testing
- **Mock contexts** - Trackable mock contexts for testing
- **Test CLI generators** - Quickly create test CLI applications
- **Assertion helpers** - Specialized assertions for CLI testing

## Classes

### MockContext

Mock context that tracks method calls for testing purposes.

```python
class MockContext(Context):
    """Mock context for testing that tracks method calls."""
    
    def __init__(self, **kwargs) -> None:
        """Initialize mock context with tracking."""
```

#### Attributes

- `calls: list` - List of tracked method calls
- `saved_configs: list` - List of saved configuration paths
- `loaded_configs: list` - List of loaded configuration paths

#### Usage Example

```python
from provide.foundation.cli.testing import MockContext

def test_config_operations():
    ctx = MockContext()
    
    # Perform operations
    ctx.load_config("config.yaml")
    ctx.save_config("output.yaml")
    
    # Assert operations were tracked
    assert "config.yaml" in ctx.loaded_configs
    assert "output.yaml" in ctx.saved_configs
```

### CliTestCase

Base class for CLI test cases with common utilities.

```python
class CliTestCase:
    """Base class for CLI test cases with common utilities."""
    
    def setup_method(self) -> None:
        """Set up test case."""
        
    def teardown_method(self) -> None:
        """Clean up test case."""
```

#### Methods

##### invoke(*args, **kwargs)

Invoke CLI command using the test runner.

```python
def invoke(self, *args, **kwargs):
    """Invoke CLI command."""
```

##### create_temp_file(content, suffix)

Create a temporary file that will be cleaned up automatically.

```python
def create_temp_file(self, content: str = "", suffix: str = "") -> Path:
    """Create a temporary file that will be cleaned up."""
```

##### assert_json_output(result, expected)

Assert that CLI output is valid JSON matching expected structure.

```python
def assert_json_output(self, result, expected: dict[str, Any]) -> None:
    """Assert that output is valid JSON matching expected."""
```

#### Usage Example

```python
from provide.foundation.cli.testing import CliTestCase

class TestMyCLI(CliTestCase):
    def test_command_output(self):
        result = self.invoke(my_cli, ["--json", "status"])
        
        self.assert_json_output(result, {
            "status": "running",
            "version": "1.0.0"
        })
        
        assert result.exit_code == 0
```

## Context Managers

### isolated_cli_runner(env, mix_stderr)

Create an isolated test environment for CLI testing.

```python
@contextmanager
def isolated_cli_runner(
    env: dict[str, str] | None = None,
    mix_stderr: bool = False,
):
    """
    Create an isolated test environment for CLI testing.
    
    Args:
        env: Environment variables to set
        mix_stderr: Whether to mix stderr with stdout
        
    Yields:
        CliRunner instance in isolated filesystem
    """
```

**Features:**
- Isolated filesystem (temporary directory)
- Environment variable management
- Automatic cleanup
- stderr/stdout handling

**Usage Example:**
```python
from provide.foundation.cli.testing import isolated_cli_runner

def test_cli_with_env():
    with isolated_cli_runner(env={"DEBUG": "true"}) as runner:
        result = runner.invoke(my_cli, ["status"])
        assert result.exit_code == 0
        assert "Debug mode enabled" in result.output
```

### temp_config_file(content, format)

Create a temporary configuration file for testing.

```python
@contextmanager
def temp_config_file(
    content: dict[str, Any] | str,
    format: str = "json",
) -> Path:
    """
    Create a temporary configuration file for testing.
    
    Args:
        content: Configuration content (dict or string)
        format: File format (json, toml, yaml)
        
    Yields:
        Path to temporary config file
    """
```

**Supported formats:**
- `json` - JSON format
- `toml` - TOML format (requires tomli_w)
- `yaml` - YAML format (requires PyYAML)

**Usage Examples:**
```python
from provide.foundation.cli.testing import temp_config_file

# JSON configuration
def test_json_config():
    config_data = {"host": "localhost", "port": 8080}
    
    with temp_config_file(config_data, format="json") as config_path:
        result = runner.invoke(my_cli, ["--config", str(config_path), "start"])
        assert result.exit_code == 0

# YAML configuration  
def test_yaml_config():
    yaml_content = """
    database:
      host: postgres.example.com
      port: 5432
    """
    
    with temp_config_file(yaml_content, format="yaml") as config_path:
        result = runner.invoke(my_cli, ["--config", str(config_path), "db", "connect"])
        assert "Connected to postgres.example.com" in result.output

# TOML configuration
def test_toml_config():
    config_data = {
        "app": {"name": "myapp", "debug": True},
        "server": {"port": 8000}
    }
    
    with temp_config_file(config_data, format="toml") as config_path:
        result = runner.invoke(my_cli, ["--config", str(config_path)])
        assert result.exit_code == 0
```

## Test Utilities

### create_test_cli(name, version, commands)

Create a test CLI group with standard options.

```python
def create_test_cli(
    name: str = "test-cli",
    version: str = "1.0.0", 
    commands: list[click.Command] | None = None,
) -> click.Group:
    """
    Create a test CLI group with standard options.
    
    Args:
        name: CLI name
        version: CLI version
        commands: Optional list of commands to add
        
    Returns:
        Click Group configured for testing
    """
```

**Usage Example:**
```python
from provide.foundation.cli.testing import create_test_cli
import click

@click.command()
def hello():
    """Say hello."""
    click.echo("Hello, World!")

@click.command()  
def status():
    """Show status."""
    click.echo("All systems operational")

def test_custom_cli():
    cli = create_test_cli(
        name="myapp",
        version="2.0.0",
        commands=[hello, status]
    )
    
    with isolated_cli_runner() as runner:
        # Test hello command
        result = runner.invoke(cli, ["hello"])
        assert "Hello, World!" in result.output
        
        # Test status command
        result = runner.invoke(cli, ["status"])
        assert "All systems operational" in result.output
        
        # Test version
        result = runner.invoke(cli, ["--version"])
        assert "2.0.0" in result.output
```

### mock_logger()

Create a mock logger for testing.

```python
def mock_logger():
    """
    Create a mock logger for testing.
    
    Returns:
        MagicMock with common logger methods
    """
```

**Usage Example:**
```python
from provide.foundation.cli.testing import mock_logger
from unittest.mock import patch

def test_logging():
    logger_mock = mock_logger()
    
    with patch('my_module.log', logger_mock):
        my_function()
        
        # Assert logging calls
        logger_mock.info.assert_called_once_with("Operation completed")
        logger_mock.error.assert_not_called()
```

## Integration Testing Patterns

### Full CLI Application Testing

```python
import pytest
from provide.foundation.cli.testing import isolated_cli_runner, temp_config_file
from myapp.cli import cli

class TestMyAppCLI:
    def test_start_command_with_config(self):
        config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8080
            },
            "database": {
                "url": "sqlite:///test.db"
            }
        }
        
        with temp_config_file(config) as config_path:
            with isolated_cli_runner() as runner:
                result = runner.invoke(cli, [
                    "--config", str(config_path),
                    "start"
                ])
                
                assert result.exit_code == 0
                assert "Server starting on 0.0.0.0:8080" in result.output
    
    def test_status_command_json_output(self):
        with isolated_cli_runner() as runner:
            result = runner.invoke(cli, ["--json", "status"])
            
            assert result.exit_code == 0
            
            # Parse and validate JSON output
            import json
            output_data = json.loads(result.output)
            assert "status" in output_data
            assert "uptime" in output_data
    
    def test_error_handling(self):
        with isolated_cli_runner() as runner:
            result = runner.invoke(cli, ["nonexistent-command"])
            
            assert result.exit_code != 0
            assert "No such command" in result.output

    def test_environment_variables(self):
        env = {
            "MYAPP_DEBUG": "true",
            "MYAPP_LOG_LEVEL": "DEBUG"
        }
        
        with isolated_cli_runner(env=env) as runner:
            result = runner.invoke(cli, ["status"])
            
            assert result.exit_code == 0
            # Should see debug output due to env vars
```

### Testing with Mock Dependencies

```python
from unittest.mock import patch, MagicMock
from provide.foundation.cli.testing import isolated_cli_runner

def test_cli_with_external_service():
    mock_service = MagicMock()
    mock_service.connect.return_value = True
    mock_service.status.return_value = "healthy"
    
    with patch('myapp.services.external_service', mock_service):
        with isolated_cli_runner() as runner:
            result = runner.invoke(cli, ["check", "external"])
            
            assert result.exit_code == 0
            assert "External service: healthy" in result.output
            
            # Verify service was called
            mock_service.connect.assert_called_once()
            mock_service.status.assert_called_once()
```

### Configuration Testing

```python
def test_configuration_loading():
    # Test with missing config
    with isolated_cli_runner() as runner:
        result = runner.invoke(cli, ["--config", "missing.yaml", "start"])
        assert result.exit_code != 0
        assert "Configuration file not found" in result.output
    
    # Test with invalid config
    invalid_config = "invalid: yaml: content"
    with temp_config_file(invalid_config, format="yaml") as config_path:
        with isolated_cli_runner() as runner:
            result = runner.invoke(cli, ["--config", str(config_path), "start"])
            assert result.exit_code != 0
            assert "Configuration error" in result.output
```

## Async CLI Testing

For CLI commands that use async operations:

```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_async_cli_command():
    from provide.foundation.cli.testing import isolated_cli_runner
    
    with isolated_cli_runner() as runner:
        # For async CLI commands, you may need to run them in the event loop
        result = runner.invoke(cli, ["async-command"])
        
        assert result.exit_code == 0
        assert "Async operation completed" in result.output
```

## Performance Testing

```python
import time
from provide.foundation.cli.testing import isolated_cli_runner

def test_command_performance():
    with isolated_cli_runner() as runner:
        start_time = time.time()
        
        result = runner.invoke(cli, ["heavy-operation"])
        
        duration = time.time() - start_time
        
        assert result.exit_code == 0
        assert duration < 5.0  # Should complete in under 5 seconds
```

## Related Documentation

- [api-CLI Decorators API](decorators.md) - Standard CLI decorators
- [api-CLI Utils API](utils.md) - CLI utilities and helpers
- [Hub Commands API](../hub/commands.md) - Hub-based command system
- [CLI Guide](../../guide/cli/index.md) - CLI development guide