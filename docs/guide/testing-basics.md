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

