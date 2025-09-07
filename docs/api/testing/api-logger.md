# Logger Management API

Logger state management and isolation utilities for testing with clean, isolated logger configurations.

## State Reset Functions

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

**What it resets**:
- Logger configuration state
- Setup tracking flags
- Stream redirection state
- Lazy initialization state

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

## Test Fixtures

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

### Configuration Testing

```python
from provide.foundation.testing import (
    reset_foundation_setup_for_testing,
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
)

def test_log_level_configuration(
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
):
    """Test different log level configurations."""
    
    # Test DEBUG level
    debug_config = TelemetryConfig(
        logging=LoggingConfig(default_level="DEBUG")
    )
    setup_foundation_telemetry_for_test(debug_config)
    
    logger.debug("debug_message")
    logger.info("info_message")
    logger.error("error_message")
    
    debug_output = captured_stderr_for_foundation.getvalue()
    assert "debug_message" in debug_output
    assert "info_message" in debug_output
    assert "error_message" in debug_output
    
    # Reset and test ERROR level
    reset_foundation_setup_for_testing()
    captured_stderr_for_foundation.truncate(0)
    captured_stderr_for_foundation.seek(0)
    
    error_config = TelemetryConfig(
        logging=LoggingConfig(default_level="ERROR")
    )
    setup_foundation_telemetry_for_test(error_config)
    
    logger.debug("debug_message_2")
    logger.info("info_message_2")
    logger.error("error_message_2")
    
    error_output = captured_stderr_for_foundation.getvalue()
    assert "debug_message_2" not in error_output
    assert "info_message_2" not in error_output
    assert "error_message_2" in error_output
```

### Formatter Testing

```python
def test_json_formatter(
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
):
    """Test JSON formatter configuration."""
    import json
    
    config = TelemetryConfig(
        logging=LoggingConfig(
            console_formatter="json",
            default_level="INFO"
        )
    )
    setup_foundation_telemetry_for_test(config)
    
    logger.info("api_request", 
                method="POST",
                path="/users",
                status=201)
    
    output = captured_stderr_for_foundation.getvalue()
    
    # Parse JSON output
    for line in output.strip().split('\n'):
        if line:
            log_entry = json.loads(line)
            if log_entry.get('event') == 'api_request':
                assert log_entry['method'] == 'POST'
                assert log_entry['path'] == '/users'
                assert log_entry['status'] == 201
                break
    else:
        pytest.fail("Expected log entry not found")

def test_pretty_formatter(
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
):
    """Test pretty formatter configuration."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            console_formatter="pretty",
            das_emoji_prefix_enabled=True
        )
    )
    setup_foundation_telemetry_for_test(config)
    
    logger.info("user_created", user_id="usr_123")
    
    output = captured_stderr_for_foundation.getvalue()
    assert "user_created" in output
    assert "usr_123" in output
    # Should contain emoji and colors (when terminal supports it)
```

### Error Handling Tests

```python
from provide.foundation.errors import ValidationError

def test_error_logging_isolation(
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
):
    """Test error logging in isolation."""
    setup_foundation_telemetry_for_test()
    
    def risky_operation():
        try:
            raise ValidationError("Invalid data", field="email")
        except ValidationError as e:
            logger.error("validation_failed", 
                        error=str(e),
                        field=e.field)
            raise
    
    with pytest.raises(ValidationError):
        risky_operation()
    
    output = captured_stderr_for_foundation.getvalue()
    assert "validation_failed" in output
    assert "Invalid data" in output
    assert "email" in output
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

### 2. Use Setup Fixture for Configuration

```python
# ✅ Good - Use fixture for proper setup
def test_with_config(setup_foundation_telemetry_for_test):
    config = TelemetryConfig(logging=LoggingConfig(default_level="DEBUG"))
    setup_foundation_telemetry_for_test(config)
    # Test with clean configuration

# ❌ Bad - Direct setup without fixture
def test_without_fixture():
    setup_telemetry(config)  # May not be properly isolated
```

### 3. Verify Configuration Effects

```python
def test_configuration_effects(
    setup_foundation_telemetry_for_test,
    captured_stderr_for_foundation
):
    """Verify configuration actually affects logging behavior."""
    
    # Set strict ERROR-only configuration
    config = TelemetryConfig(
        logging=LoggingConfig(default_level="ERROR")
    )
    setup_foundation_telemetry_for_test(config)
    
    # Generate logs at different levels
    logger.debug("should_not_appear")
    logger.info("should_not_appear")
    logger.warning("should_not_appear")
    logger.error("should_appear")
    
    output = captured_stderr_for_foundation.getvalue()
    
    # Verify only ERROR level appears
    assert "should_not_appear" not in output
    assert "should_appear" in output
```

## Next Steps

- [Stream Testing](api-streams.md) - Stream redirection and output capture
- [CLI Testing](api-cli.md) - Command-line interface testing tools
- [Crypto Fixtures](api-crypto.md) - Certificate and key testing data