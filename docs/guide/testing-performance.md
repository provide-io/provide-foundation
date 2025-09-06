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