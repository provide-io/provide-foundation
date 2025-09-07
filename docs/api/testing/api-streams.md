# Stream Testing API

Stream redirection and output capture utilities for testing log output and stream behavior.

## Stream Control Functions

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

**Use Cases**:
- Manual stream control in complex test scenarios
- Custom stream implementations for specialized testing
- Integration with non-pytest test frameworks

## Pytest Fixtures

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

**Features**:
- Automatic setup and teardown
- Thread-safe capture
- Works with all Foundation logging formats

## Advanced Stream Testing

### Structured Log Parsing

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

### Thread Safety Testing

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

## Error Handling Tests

### Stream Isolation

```python
def test_stream_isolation(captured_stderr_for_foundation):
    """Verify streams are properly isolated between tests."""
    logger.info("first_test_message")
    
    # Clear the buffer mid-test
    captured_stderr_for_foundation.truncate(0)
    captured_stderr_for_foundation.seek(0)
    
    logger.info("second_test_message")
    
    output = captured_stderr_for_foundation.getvalue()
    assert "first_test_message" not in output
    assert "second_test_message" in output
```

### Exception Logging

```python
from provide.foundation.testing import captured_stderr_for_foundation
from provide.foundation.errors import ValidationError

def test_exception_logging(captured_stderr_for_foundation):
    """Test exception logging capture."""
    try:
        raise ValidationError("Invalid email format", field="email")
    except ValidationError as e:
        logger.error("validation_exception", 
                    error=str(e), 
                    field=e.field)
    
    output = captured_stderr_for_foundation.getvalue()
    assert "validation_exception" in output
    assert "Invalid email format" in output
    assert "email" in output
```

## Best Practices

### 1. Use Appropriate Fixtures

```python
# ✅ Good - Use fixture for automatic cleanup
def test_logging(captured_stderr_for_foundation):
    logger.info("test_message")
    output = captured_stderr_for_foundation.getvalue()
    assert "test_message" in output

# ❌ Bad - Manual setup requires cleanup
def test_logging():
    import io
    stream = io.StringIO()
    set_log_stream_for_testing(stream)
    logger.info("test_message")
    # Forgot to reset stream - affects other tests
```

### 2. Clear Buffers When Needed

```python
def test_multiple_operations(captured_stderr_for_foundation):
    """Test multiple operations with clean separation."""
    
    # First operation
    service.create_user({"name": "Alice"})
    output1 = captured_stderr_for_foundation.getvalue()
    assert "user_created" in output1
    
    # Clear buffer for next test
    captured_stderr_for_foundation.truncate(0)
    captured_stderr_for_foundation.seek(0)
    
    # Second operation
    service.delete_user("alice")
    output2 = captured_stderr_for_foundation.getvalue()
    assert "user_deleted" in output2
    assert "user_created" not in output2  # Previous logs cleared
```

### 3. Test Both Success and Error Cases

```python
def test_service_operations(captured_stderr_for_foundation):
    """Test both success and error logging."""
    service = UserService()
    
    # Test success case
    user = service.create_user({"name": "Alice", "email": "alice@example.com"})
    success_output = captured_stderr_for_foundation.getvalue()
    assert "user_created" in success_output
    
    # Clear for error test
    captured_stderr_for_foundation.truncate(0)
    captured_stderr_for_foundation.seek(0)
    
    # Test error case
    with pytest.raises(ValidationError):
        service.create_user({"name": ""})  # Invalid data
    
    error_output = captured_stderr_for_foundation.getvalue()
    assert "validation_failed" in error_output
```

## Next Steps

- [Logger Management](api-logger.md) - Logger state management and isolation
- [CLI Testing](api-cli.md) - Command-line interface testing tools
- [Context Detection](api-context.md) - Testing environment detection