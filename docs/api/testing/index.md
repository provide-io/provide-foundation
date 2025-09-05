# Testing API Reference

Comprehensive testing utilities for Foundation applications including fixtures, mocks, and testing helpers.

## Overview

The testing module provides Foundation's complete testing infrastructure with:
- **Stream Redirection** - Capture and control log output during tests  
- **Logger State Management** - Reset and isolate logger configurations
- **CLI Testing** - Mock contexts, isolated runners, and command testing
- **Crypto Fixtures** - Comprehensive certificate and key testing data
- **Test Fixtures** - Reusable pytest fixtures for common scenarios
- **Context Detection** - Automatic testing environment detection

## Quick Start

```python
import pytest
from provide.foundation.testing import (
    captured_stderr_for_foundation,
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
    isolated_cli_runner
)

# Capture log output
def test_with_captured_logs(captured_stderr_for_foundation):
    logger.info("test_message", key="value")
    output = captured_stderr_for_foundation.getvalue()
    assert "test_message" in output

# Reset logger state
def test_logger_isolation():
    reset_foundation_setup_for_testing()
    # Logger is in clean state

# CLI testing
def test_cli_command():
    with isolated_cli_runner() as runner:
        result = runner.invoke(cli, ["command", "--option"])
        assert result.exit_code == 0
```

## Stream Testing

### `set_log_stream_for_testing(stream: TextIO | None) -> None`

Redirect Foundation's log output to a custom stream for testing.

**Parameters**:
- `stream: TextIO | None` - Stream to redirect to, or None to reset to stderr

```python
import io
from provide.foundation.testing import set_log_stream_for_testing
from provide.foundation.logger import logger

# Capture output in StringIO
test_stream = io.StringIO()
set_log_stream_for_testing(test_stream)

logger.info("test_message", user_id=123)
output = test_stream.getvalue()
assert "test_message" in output

# Reset to stderr
set_log_stream_for_testing(None)
```

### `captured_stderr_for_foundation` (Fixture)

Pytest fixture that automatically captures Foundation's log output.

```python
def test_logging_output(captured_stderr_for_foundation):
    """Test that automatically captures log output."""
    logger.info("user_created", user_id="usr_123")
    logger.error("validation_failed", field="email")
    
    output = captured_stderr_for_foundation.getvalue()
    assert "user_created" in output
    assert "usr_123" in output
    assert "validation_failed" in output
    # Stream automatically reset after test
```

**Advanced Stream Testing**:
```python
import json
from provide.foundation.testing import captured_stderr_for_foundation

def test_structured_logging(captured_stderr_for_foundation):
    """Test structured log output format."""
    logger.info("api_request", 
                method="GET", 
                path="/users/123", 
                duration_ms=45.2)
    
    output = captured_stderr_for_foundation.getvalue()
    # Parse JSON log output
    for line in output.strip().split('\n'):
        if line:
            log_entry = json.loads(line)
            if log_entry.get('event') == 'api_request':
                assert log_entry['method'] == 'GET'
                assert log_entry['path'] == '/users/123'
                assert log_entry['duration_ms'] == 45.2
```

## Logger State Management

### `reset_foundation_setup_for_testing() -> None`

Reset Foundation's logger state for test isolation.

```python
from provide.foundation.testing import reset_foundation_setup_for_testing
from provide.foundation import setup_telemetry, TelemetryConfig

def test_logger_reconfiguration():
    """Test that logger can be reconfigured after reset."""
    # Set up initial configuration
    setup_telemetry(TelemetryConfig(
        logging=LoggingConfig(default_level="DEBUG")
    ))
    
    # Reset for clean test state
    reset_foundation_setup_for_testing()
    
    # Configure differently
    setup_telemetry(TelemetryConfig(
        logging=LoggingConfig(default_level="ERROR")
    ))
    
    # Verify new configuration is active
    logger.debug("debug_message")  # Should not appear
    logger.error("error_message")   # Should appear
```

### `reset_foundation_state() -> None`

Internal function for comprehensive state reset (used by reset_foundation_setup_for_testing).

**Resets**:
- structlog configuration to defaults
- Foundation logger state and configuration
- Stream state back to defaults  
- Lazy setup state tracking

```python
def test_complete_state_isolation():
    """Verify complete isolation between test runs."""
    from provide.foundation.testing.logger import reset_foundation_state
    
    # Modify state
    logger.info("setup_message")
    
    # Complete reset
    reset_foundation_state()
    
    # Verify clean state
    # All internal state should be reset
    assert not logger._is_configured_by_setup
    assert logger._active_config is None
```

## Common Fixtures

### `setup_foundation_telemetry_for_test` (Fixture)

Fixture that provides a function to set up Foundation Telemetry with custom configurations.

```python
from provide.foundation import TelemetryConfig, LoggingConfig

def test_custom_telemetry_config(setup_foundation_telemetry_for_test):
    """Test with custom telemetry configuration."""
    # Configure with specific settings
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",
            console_formatter="json",
            das_emoji_prefix_enabled=False
        )
    )
    
    setup_foundation_telemetry_for_test(config)
    
    # Test with this configuration
    logger.debug("debug_message", key="value")
    
def test_default_telemetry_config(setup_foundation_telemetry_for_test):
    """Test with default configuration."""
    # Use defaults
    setup_foundation_telemetry_for_test()
    
    # Test with default configuration
    logger.info("default_config_test")
```

## CLI Testing

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

## Crypto Testing Fixtures

### Certificate Fixtures

**Available fixtures**:
- `client_cert` - Client certificate for authentication testing
- `server_cert` - Server certificate for TLS testing  
- `ca_cert` - Certificate Authority for certificate chain testing

```python
def test_certificate_validation(client_cert, server_cert):
    """Test certificate validation logic."""
    # Client cert fixture provides Certificate object
    assert client_cert.is_valid()
    assert client_cert.common_name == "localhost"
    
    # Server cert for TLS scenarios
    assert server_cert.is_valid()
    assert not server_cert.is_expired()

def test_certificate_chain(ca_cert):
    """Test certificate chain validation."""
    # CA cert can be used to create signed certificates
    issued_cert = ca_cert.issue_certificate(
        common_name="service.example.com",
        validity_days=90
    )
    
    assert issued_cert.verify_chain([ca_cert])
```

### PEM Content Fixtures

**Available fixtures**:
- `valid_cert_pem` - Valid certificate PEM content
- `valid_key_pem` - Valid private key PEM content  
- `invalid_cert_pem` - Invalid certificate for error testing
- `invalid_key_pem` - Invalid key for error testing
- `malformed_cert_pem` - Malformed certificate data
- `empty_cert` - Empty certificate content

```python
def test_pem_parsing(valid_cert_pem, invalid_cert_pem):
    """Test PEM content parsing."""
    # Valid PEM should parse successfully
    cert = Certificate.from_pem(valid_cert_pem)
    assert cert.is_valid()
    
    # Invalid PEM should raise appropriate error
    with pytest.raises(CertificateError):
        Certificate.from_pem(invalid_cert_pem)

def test_key_validation(valid_key_pem, invalid_key_pem):
    """Test key validation."""
    # Valid key should be usable
    key = PrivateKey.from_pem(valid_key_pem)
    assert key.is_valid()
    
    # Invalid key should fail validation
    with pytest.raises(KeyError):
        PrivateKey.from_pem(invalid_key_pem)
```

### File-Based Fixtures

**Available fixtures**:
- `temporary_cert_file` - Temporary file with certificate
- `temporary_key_file` - Temporary file with private key
- `cert_with_windows_line_endings` - Certificate with Windows CRLF
- `cert_with_utf8_bom` - Certificate with UTF-8 BOM
- `cert_with_extra_whitespace` - Certificate with formatting issues

```python
def test_certificate_file_loading(temporary_cert_file, temporary_key_file):
    """Test loading certificates from files."""
    # Load from temporary files
    cert = Certificate.from_file(temporary_cert_file)
    key = PrivateKey.from_file(temporary_key_file)
    
    assert cert.is_valid()
    assert key.matches_certificate(cert)

def test_format_handling(cert_with_windows_line_endings, cert_with_utf8_bom):
    """Test handling various file formats."""
    # Should handle Windows line endings
    cert1 = Certificate.from_pem(cert_with_windows_line_endings)
    assert cert1.is_valid()
    
    # Should handle UTF-8 BOM
    cert2 = Certificate.from_pem(cert_with_utf8_bom) 
    assert cert2.is_valid()
```

## Context Detection

### `_is_testing_context() -> bool`

Detect if the code is running in a testing environment.

```python
from provide.foundation.testing import _is_testing_context

def production_only_feature():
    """Feature that should only run in production."""
    if _is_testing_context():
        return "test_mode_disabled"
    
    # Real production logic
    return perform_production_operation()

# In tests, this will be detected automatically
assert production_only_feature() == "test_mode_disabled"
```

**Detection methods**:
- `pytest` module is imported
- `PYTEST_CURRENT_TEST` environment variable is set
- `unittest` module is imported  
- `TESTING` environment variable equals "true"
- Command line arguments contain pytest/py.test

## Integration Examples

### Complete Test Suite Setup

```python
import pytest
from provide.foundation.testing import (
    captured_stderr_for_foundation,
    reset_foundation_setup_for_testing,
    setup_foundation_telemetry_for_test
)
from provide.foundation import TelemetryConfig, LoggingConfig

class TestUserService:
    """Complete test suite with proper setup/teardown."""
    
    def setup_method(self):
        """Set up each test with clean state."""
        reset_foundation_setup_for_testing()
    
    def test_user_creation_logging(
        self, 
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test
    ):
        """Test user creation with captured logging."""
        # Configure telemetry for test
        config = TelemetryConfig(
            logging=LoggingConfig(default_level="DEBUG")
        )
        setup_foundation_telemetry_for_test(config)
        
        # Test the service
        service = UserService()
        user = service.create_user({
            "name": "Alice",
            "email": "alice@example.com"
        })
        
        # Verify logging output
        output = captured_stderr_for_foundation.getvalue()
        assert "user_creation_started" in output
        assert "alice@example.com" in output
        assert "user_creation_completed" in output
        
        # Verify user creation
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
```

### API Testing with Error Handling

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

### Performance Testing

```python
import time
from provide.foundation.testing import captured_stderr_for_foundation

def test_logging_performance(captured_stderr_for_foundation):
    """Test logging performance under load."""
    message_count = 1000
    start_time = time.time()
    
    # Generate many log messages
    for i in range(message_count):
        logger.info("performance_test", 
                   iteration=i, 
                   timestamp=time.time())
    
    elapsed = time.time() - start_time
    messages_per_second = message_count / elapsed
    
    # Verify performance meets expectations
    assert messages_per_second > 5000, f"Only {messages_per_second:.0f} msg/sec"
    
    # Verify all messages were captured
    output = captured_stderr_for_foundation.getvalue()
    log_lines = output.strip().split('\n')
    assert len(log_lines) >= message_count
```

## Best Practices

### 1. Always Reset State Between Tests

```python
# ✅ Good - Clean state for each test
def setup_method(self):
    reset_foundation_setup_for_testing()

# ❌ Bad - State leaks between tests
def test_without_reset():
    # Previous test configuration still active
    pass
```

### 2. Use Appropriate Fixtures

```python
# ✅ Good - Use specific fixtures
def test_logging(captured_stderr_for_foundation):
    # Test-specific stream capture
    pass

def test_certificates(client_cert, server_cert):
    # Certificate-specific fixtures
    pass

# ❌ Bad - Manual setup
def test_logging():
    stream = io.StringIO()
    set_log_stream_for_testing(stream)
    # Manual teardown required
```

### 3. Isolate CLI Tests

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

### 4. Verify Both Success and Error Cases

```python
# ✅ Good - Test both paths
def test_user_service(captured_stderr_for_foundation):
    service = UserService()
    
    # Test success case
    user = service.create_user(valid_data)
    assert "user_created" in captured_stderr_for_foundation.getvalue()
    
    # Clear output buffer
    captured_stderr_for_foundation.truncate(0)
    captured_stderr_for_foundation.seek(0)
    
    # Test error case
    with pytest.raises(ValidationError):
        service.create_user(invalid_data)
    assert "validation_failed" in captured_stderr_for_foundation.getvalue()
```

## Thread Safety

All testing utilities are thread-safe and can be used in concurrent tests:

```python
import threading
from provide.foundation.testing import captured_stderr_for_foundation

def test_concurrent_logging(captured_stderr_for_foundation):
    """Test thread-safe logging capture."""
    
    def worker(worker_id):
        for i in range(100):
            logger.info("worker_message", 
                       worker_id=worker_id, 
                       iteration=i)
    
    # Run multiple worker threads
    threads = [
        threading.Thread(target=worker, args=(i,))
        for i in range(5)
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Verify all messages captured
    output = captured_stderr_for_foundation.getvalue()
    lines = output.strip().split('\n')
    assert len(lines) == 500  # 5 workers * 100 messages each
```

## See Also

- [Logger API](../logger/) - Foundation logging system
- [Streams API](../streams/) - Stream management and redirection
- [Errors API](../errors/) - Error handling and testing
- [CLI Guide](../../guide/cli/) - Command-line interface development
- [Testing Guide](../../guide/testing/) - Comprehensive testing practices