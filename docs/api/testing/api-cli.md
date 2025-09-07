# CLI Testing API

Command-line interface testing tools including mock contexts, isolated runners, and configuration management.

## Mock Context Objects

### `MockContext`

Mock context class that tracks method calls for testing.

```python
from provide.foundation.testing import MockContext

def test_context_tracking():
    """Test that context tracks method calls."""
    ctx = MockContext(verbose=True, config_file="test.yaml")
    
    # Track save operations
    ctx.save_config("output.yaml")
    assert "output.yaml" in ctx.saved_configs
    
    # Track load operations  
    ctx.load_config("input.yaml")
    assert "input.yaml" in ctx.loaded_configs
    
    # Access tracking data
    assert len(ctx.calls) >= 0  # Tracks method calls
```

**Properties**:
- `saved_configs: list[str]` - List of config files saved
- `loaded_configs: list[str]` - List of config files loaded
- `calls: list[dict]` - Detailed method call tracking

## Isolated Test Runners

### `isolated_cli_runner()`

Context manager for isolated CLI testing with environment control.

```python
from provide.foundation.testing import isolated_cli_runner
import click

@click.command()
@click.option('--name', required=True)
def greet(name):
    """Test command."""
    click.echo(f"Hello, {name}!")

def test_cli_command():
    """Test CLI command in isolated environment."""
    with isolated_cli_runner(env={"TEST_MODE": "true"}) as runner:
        result = runner.invoke(greet, ['--name', 'World'])
        
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

def test_cli_with_config():
    """Test CLI with configuration file."""
    with isolated_cli_runner() as runner:
        # Create config file in isolated filesystem
        with open('config.yaml', 'w') as f:
            f.write("name: TestApp\nversion: 1.0.0\n")
        
        # Test command that uses config
        result = runner.invoke(my_cli, ['--config', 'config.yaml'])
        assert result.exit_code == 0
```

**Parameters**:
- `env: dict[str, str]` - Environment variables for isolated test
- Returns context manager with CliRunner instance

**Features**:
- Isolated filesystem for each test
- Custom environment variables
- Automatic cleanup after test

## Configuration Testing

### `temp_config_file()`

Context manager for creating temporary configuration files.

```python
from provide.foundation.testing import temp_config_file

def test_json_config():
    """Test with JSON configuration."""
    config_data = {
        "database": {"host": "localhost", "port": 5432},
        "logging": {"level": "DEBUG"}
    }
    
    with temp_config_file(config_data, format="json") as config_path:
        # Use the temporary config file
        result = load_config(config_path)
        assert result["database"]["host"] == "localhost"

def test_yaml_config():
    """Test with YAML configuration."""
    config_data = {
        "api": {"base_url": "https://api.example.com"},
        "features": ["auth", "analytics"]
    }
    
    with temp_config_file(config_data, format="yaml") as config_path:
        result = load_yaml_config(config_path)
        assert len(result["features"]) == 2

def test_string_config():
    """Test with raw string configuration."""
    config_content = """
    [database]
    host = "localhost"
    port = 5432
    """
    
    with temp_config_file(config_content, format="toml") as config_path:
        # Process raw TOML content
        result = load_toml_config(config_path)
        assert result["database"]["host"] == "localhost"
```

**Parameters**:
- `config_data: dict | str` - Configuration data or raw string content
- `format: str` - File format ("json", "yaml", "toml")

## CLI Structure Testing

### `create_test_cli()`

Create a test CLI group with standard options.

```python
from provide.foundation.testing import create_test_cli
import click

def test_cli_structure():
    """Test CLI structure creation."""
    @click.command()
    def test_command():
        click.echo("Test command executed")
    
    cli = create_test_cli(
        name="test-app",
        version="2.0.0", 
        commands=[test_command]
    )
    
    # Test CLI structure
    assert cli.name == "test-app"
    assert "test_command" in [cmd.name for cmd in cli.commands.values()]

def test_cli_execution():
    """Test CLI command execution."""
    @click.command()
    @click.option('--count', type=int, default=1)
    def repeat(count):
        for i in range(count):
            click.echo(f"Message {i+1}")
    
    cli = create_test_cli(commands=[repeat])
    
    with isolated_cli_runner() as runner:
        result = runner.invoke(cli, ['repeat', '--count', '3'])
        assert "Message 1" in result.output
        assert "Message 3" in result.output
```

**Parameters**:
- `name: str` - CLI application name
- `version: str` - CLI version string
- `commands: list[click.Command]` - Commands to add to CLI

## Mock Logger

### `mock_logger()`

Create a mock logger for testing without actual logging.

```python
from provide.foundation.testing import mock_logger

def test_with_mock_logger():
    """Test using mock logger."""
    mock = mock_logger()
    
    # Use mock in place of real logger
    service = UserService(logger=mock)
    service.create_user({"name": "John", "email": "john@example.com"})
    
    # Verify logging calls
    mock.info.assert_called_once()
    mock.debug.assert_called()
    
    # Check call arguments
    call_args = mock.info.call_args
    assert "user_created" in str(call_args)
```

**Returns**: Mock object with logger interface methods
- `debug()`, `info()`, `warning()`, `error()`, `critical()`
- All methods track calls for verification

## Base Test Classes

### `CliTestCase`

Base class for CLI test cases with common utilities.

```python
from provide.foundation.testing import CliTestCase
import json

class TestMyCliApp(CliTestCase):
    """Test cases for CLI application."""
    
    def test_command_output(self):
        """Test command produces expected output."""
        result = self.invoke(my_cli, ['status'])
        assert result.exit_code == 0
        assert "Status: OK" in result.output
    
    def test_json_output(self):
        """Test JSON output format."""
        result = self.invoke(my_cli, ['info', '--format', 'json'])
        
        expected = {"status": "running", "version": "1.0.0"}
        self.assert_json_output(result, expected)
    
    def test_with_config_file(self):
        """Test command with configuration file."""
        config_content = '{"timeout": 30, "retries": 3}'
        config_path = self.create_temp_file(config_content, '.json')
        
        result = self.invoke(my_cli, ['--config', str(config_path), 'run'])
        assert result.exit_code == 0
```

**Methods**:
- `invoke(cli, args)` - Invoke CLI command with arguments
- `assert_json_output(result, expected)` - Assert JSON output matches expected
- `create_temp_file(content, extension)` - Create temporary file with content

## Integration Examples

### API Testing with CLI

```python
from provide.foundation.testing import isolated_cli_runner, temp_config_file
from provide.foundation.errors import ValidationError

def test_api_error_handling():
    """Test API error handling and logging."""
    with isolated_cli_runner() as runner:
        # Create invalid config
        invalid_config = {
            "api": {"base_url": "not-a-url"},
            "timeout": -1  # Invalid timeout
        }
        
        with temp_config_file(invalid_config) as config_path:
            result = runner.invoke(
                api_cli, 
                ['--config', str(config_path), 'request', '/users']
            )
            
            # Should fail with validation error
            assert result.exit_code != 0
            assert "validation_failed" in result.output
            assert "not-a-url" in result.output

def test_api_success_flow(captured_stderr_for_foundation):
    """Test successful API request flow."""
    api = MockAPIClient()
    service = APIService(client=api)
    
    result = service.get_user("usr_123")
    
    # Verify success logging
    output = captured_stderr_for_foundation.getvalue()
    assert "api_request_started" in output
    assert "usr_123" in output
    assert "api_request_completed" in output
    
    assert result["user_id"] == "usr_123"
```

### Complex Command Testing

```python
from provide.foundation.testing import isolated_cli_runner, MockContext

def test_complex_command_flow():
    """Test complex command with multiple operations."""
    
    @click.command()
    @click.option('--config', type=click.Path())
    @click.option('--output', type=click.Path())
    @click.pass_context
    def process_data(ctx, config, output):
        """Process data with configuration."""
        if config:
            ctx.obj = MockContext()
            ctx.obj.load_config(config)
        
        # Simulate processing
        result = {"processed": True, "count": 100}
        
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(result, f)
            click.echo(f"Results written to {output}")
        else:
            click.echo(json.dumps(result))
    
    with isolated_cli_runner() as runner:
        # Create input config
        with temp_config_file({"source": "data.csv"}, format="json") as config_path:
            result = runner.invoke(process_data, [
                '--config', str(config_path),
                '--output', 'results.json'
            ])
            
            assert result.exit_code == 0
            assert "Results written to results.json" in result.output
            
            # Verify output file was created
            import json
            with open('results.json') as f:
                output_data = json.load(f)
            assert output_data["processed"] is True
            assert output_data["count"] == 100
```

## Best Practices

### 1. Use Isolated Runners

```python
# ✅ Good - Proper isolation
def test_cli_command():
    with isolated_cli_runner(env={"TEST": "true"}) as runner:
        result = runner.invoke(command, args)
        # Isolated environment, automatic cleanup

# ❌ Bad - No isolation
def test_cli_command():
    result = CliRunner().invoke(command, args)
    # May interfere with other tests
```

### 2. Test Both Success and Error Paths

```python
def test_command_scenarios():
    """Test both success and error scenarios."""
    with isolated_cli_runner() as runner:
        # Test success
        result = runner.invoke(my_command, ['--valid-arg', 'value'])
        assert result.exit_code == 0
        
        # Test validation error
        result = runner.invoke(my_command, ['--invalid-arg', 'bad'])
        assert result.exit_code != 0
        assert "validation error" in result.output.lower()
```

### 3. Verify Output and Side Effects

```python
def test_command_effects():
    """Test command output and side effects."""
    with isolated_cli_runner() as runner:
        result = runner.invoke(create_file_command, ['test.txt', 'content'])
        
        # Check command output
        assert result.exit_code == 0
        assert "File created: test.txt" in result.output
        
        # Check side effects
        assert os.path.exists('test.txt')
        with open('test.txt') as f:
            assert f.read() == 'content'
```

## Next Steps

- [Stream Testing](api-streams.md) - Stream redirection and output capture
- [Crypto Fixtures](api-crypto.md) - Certificate and key testing data
- [Context Detection](api-context.md) - Testing environment detection