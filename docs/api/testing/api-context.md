# Context Detection API

Testing environment detection utilities for conditional behavior and test-aware functionality.

## Context Detection Function

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

**Return value**:
- `True` if running in testing context
- `False` if running in production/normal context

## Detection Scenarios

### pytest Detection

```python
def test_pytest_detection():
    """Test detection when running under pytest."""
    from provide.foundation.testing import _is_testing_context
    
    # Should be True when running under pytest
    assert _is_testing_context() is True
    
    def conditional_behavior():
        if _is_testing_context():
            return {"mode": "test", "database": "memory"}
        else:
            return {"mode": "production", "database": "postgresql"}
    
    result = conditional_behavior()
    assert result["mode"] == "test"
    assert result["database"] == "memory"
```

### Environment Variable Detection

```python
import os
from provide.foundation.testing import _is_testing_context

def test_environment_variable_detection():
    """Test detection via TESTING environment variable."""
    
    # Set testing environment variable
    original_value = os.environ.get("TESTING")
    try:
        os.environ["TESTING"] = "true"
        
        # Should detect testing context
        assert _is_testing_context() is True
        
        # Test different values
        os.environ["TESTING"] = "false"
        assert _is_testing_context() is False
        
        os.environ["TESTING"] = "1"
        assert _is_testing_context() is False  # Only "true" is recognized
        
    finally:
        # Restore original value
        if original_value is not None:
            os.environ["TESTING"] = original_value
        else:
            os.environ.pop("TESTING", None)
```

### unittest Detection

```python
import unittest
from provide.foundation.testing import _is_testing_context

class TestUnittestDetection(unittest.TestCase):
    """Test detection when running under unittest."""
    
    def test_unittest_context(self):
        """Test that unittest context is detected."""
        # Should be True when running under unittest
        self.assertTrue(_is_testing_context())
        
        def get_logger_config():
            if _is_testing_context():
                return {"level": "DEBUG", "output": "capture"}
            else:
                return {"level": "INFO", "output": "file"}
        
        config = get_logger_config()
        self.assertEqual(config["level"], "DEBUG")
        self.assertEqual(config["output"], "capture")
```

## Use Cases

### Database Configuration

```python
from provide.foundation.testing import _is_testing_context

def get_database_config():
    """Get database configuration based on context."""
    if _is_testing_context():
        return {
            "engine": "sqlite",
            "database": ":memory:",
            "echo": False
        }
    else:
        return {
            "engine": "postgresql",
            "host": os.getenv("DB_HOST", "localhost"),
            "database": os.getenv("DB_NAME", "myapp"),
            "echo": False
        }

def test_database_config():
    """Test database configuration in testing context."""
    config = get_database_config()
    
    assert config["engine"] == "sqlite"
    assert config["database"] == ":memory:"
```

### Feature Flags

```python
from provide.foundation.testing import _is_testing_context

class FeatureFlags:
    """Feature flag management with test-aware defaults."""
    
    def __init__(self):
        self.testing_mode = _is_testing_context()
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if feature is enabled."""
        # In testing, enable all features by default
        if self.testing_mode:
            test_disabled_features = ["slow_analytics", "external_apis"]
            return feature_name not in test_disabled_features
        
        # In production, use configuration/remote flags
        return self.get_production_flag(feature_name)
    
    def get_production_flag(self, feature_name: str) -> bool:
        """Get feature flag from production configuration."""
        # Implementation for production flag lookup
        return False

def test_feature_flags():
    """Test feature flag behavior in testing context."""
    flags = FeatureFlags()
    
    # Most features should be enabled in tests
    assert flags.is_enabled("new_ui") is True
    assert flags.is_enabled("enhanced_logging") is True
    
    # Except explicitly disabled ones
    assert flags.is_enabled("slow_analytics") is False
    assert flags.is_enabled("external_apis") is False
```

### Logging Configuration

```python
from provide.foundation.testing import _is_testing_context
from provide.foundation import TelemetryConfig, LoggingConfig

def create_telemetry_config() -> TelemetryConfig:
    """Create telemetry configuration based on context."""
    
    if _is_testing_context():
        # Testing configuration: capture output, disable external services
        return TelemetryConfig(
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="plain",  # Easier to parse in tests
                das_emoji_prefix_enabled=False  # Less visual noise
            ),
            otel_enabled=False,  # Disable telemetry in tests
            metrics_enabled=False
        )
    else:
        # Production configuration
        return TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
                das_emoji_prefix_enabled=True
            ),
            otel_enabled=True,
            metrics_enabled=True
        )

def test_telemetry_config():
    """Test telemetry configuration in testing context."""
    config = create_telemetry_config()
    
    # Should use test-friendly settings
    assert config.logging.default_level == "DEBUG"
    assert config.logging.console_formatter == "plain"
    assert config.logging.das_emoji_prefix_enabled is False
    assert config.otel_enabled is False
```

### External Service Mocking

```python
from provide.foundation.testing import _is_testing_context

class EmailService:
    """Email service with test-aware behavior."""
    
    def __init__(self):
        self.testing_mode = _is_testing_context()
        self.sent_emails = []  # For testing verification
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email with test-aware behavior."""
        
        if self.testing_mode:
            # In testing: capture email instead of sending
            self.sent_emails.append({
                "to": to,
                "subject": subject,
                "body": body,
                "timestamp": time.time()
            })
            return True
        else:
            # In production: actually send email
            return self.send_via_smtp(to, subject, body)
    
    def send_via_smtp(self, to: str, subject: str, body: str) -> bool:
        """Send email via SMTP (production only)."""
        # Implementation for real email sending
        pass

def test_email_service():
    """Test email service in testing context."""
    service = EmailService()
    
    result = service.send_email(
        to="test@example.com",
        subject="Test Email",
        body="This is a test email"
    )
    
    assert result is True
    assert len(service.sent_emails) == 1
    assert service.sent_emails[0]["to"] == "test@example.com"
    assert service.sent_emails[0]["subject"] == "Test Email"
```

## Performance Considerations

### Conditional Expensive Operations

```python
from provide.foundation.testing import _is_testing_context
import time

def expensive_computation():
    """Expensive operation with test shortcuts."""
    
    if _is_testing_context():
        # Return mock result in tests
        return {"result": "mocked", "computation_time": 0}
    
    # Real expensive computation in production
    start_time = time.time()
    
    # Simulate expensive work
    time.sleep(2)
    result = complex_calculation()
    
    return {
        "result": result,
        "computation_time": time.time() - start_time
    }

def test_expensive_computation():
    """Test that expensive computation is mocked."""
    result = expensive_computation()
    
    assert result["result"] == "mocked"
    assert result["computation_time"] == 0
```

### Resource Management

```python
from provide.foundation.testing import _is_testing_context

class ResourceManager:
    """Resource manager with test-aware resource allocation."""
    
    def __init__(self):
        self.testing_mode = _is_testing_context()
    
    def allocate_resources(self):
        """Allocate resources based on context."""
        if self.testing_mode:
            return {
                "memory_limit": "100MB",  # Small limit for tests
                "connection_pool_size": 2,  # Minimal pool
                "cache_size": 10  # Small cache
            }
        else:
            return {
                "memory_limit": "2GB",
                "connection_pool_size": 20,
                "cache_size": 1000
            }

def test_resource_allocation():
    """Test resource allocation in testing context."""
    manager = ResourceManager()
    resources = manager.allocate_resources()
    
    assert resources["memory_limit"] == "100MB"
    assert resources["connection_pool_size"] == 2
    assert resources["cache_size"] == 10
```

## Best Practices

### 1. Use for Infrastructure Decisions

```python
# ✅ Good - Infrastructure and configuration
def get_cache_backend():
    if _is_testing_context():
        return MemoryCache()  # Fast, isolated
    else:
        return RedisCache()   # Persistent, shared

# ❌ Bad - Business logic decisions
def calculate_tax(amount):
    if _is_testing_context():
        return amount * 0.1  # Wrong - tests should use real logic
    else:
        return amount * get_tax_rate()
```

### 2. Provide Override Mechanisms

```python
class APIClient:
    """API client with test override capability."""
    
    def __init__(self, force_real_api: bool = False):
        self.use_mock = _is_testing_context() and not force_real_api
    
    def make_request(self, endpoint: str) -> dict:
        if self.use_mock:
            return self.mock_response(endpoint)
        else:
            return self.real_request(endpoint)

# Allow forcing real API in tests when needed
def test_integration_with_real_api():
    """Test against real API when explicitly needed."""
    client = APIClient(force_real_api=True)
    response = client.make_request("/status")
    # Test against real API
```

### 3. Document Test Behavior

```python
def send_notification(message: str) -> bool:
    """
    Send notification to users.
    
    In testing context, notifications are captured in memory
    instead of being sent externally. Use NotificationService.sent
    to verify notifications in tests.
    """
    if _is_testing_context():
        NotificationService.sent.append(message)
        return True
    else:
        return NotificationService.send_external(message)
```

## Next Steps

- [Stream Testing](api-streams.md) - Stream redirection and output capture
- [Logger Management](api-logger.md) - Logger state management and isolation
- [CLI Testing](api-cli.md) - Command-line interface testing tools