"""
Tests for FoundationLogger context binding methods (bind, unbind, try_unbind).
"""

import io
import json
import sys
from typing import Any

import pytest
import structlog

from provide.foundation import logger as global_logger
from provide.foundation.core import setup_telemetry
from provide.foundation.logger import TelemetryConfig, LoggingConfig, get_logger


@pytest.fixture(autouse=True)
def reset_logger_state():
    """Reset logger state before each test."""
    # Clear any existing structlog configuration
    structlog.reset_defaults()
    yield
    # Clean up after test
    structlog.reset_defaults()


@pytest.fixture
def capture_logs():
    """Fixture to capture log output."""
    output = io.StringIO()
    
    # Setup with JSON format for easier parsing in tests
    config = TelemetryConfig(
        logging=LoggingConfig(
            console_formatter="json",
            default_level="DEBUG"
        )
    )
    setup_telemetry(config, log_stream=output)
    
    return output


def get_log_entries(output: io.StringIO) -> list[dict[str, Any]]:
    """Parse JSON log entries from output."""
    output.seek(0)
    entries = []
    for line in output.getvalue().strip().split('\n'):
        if line and not line.startswith('[Foundation Setup]'):
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue
    return entries


class TestLoggerBind:
    """Test the bind() method of FoundationLogger."""
    
    def test_bind_adds_context(self, capture_logs):
        """Test that bind() adds context to log messages."""
        # Create a bound logger with context
        bound_logger = global_logger.bind(request_id="req_123", user_id="usr_456")
        
        # Log with the bound logger
        bound_logger.info("test_event", status="success")
        
        # Check the output
        entries = get_log_entries(capture_logs)
        assert len(entries) == 1
        
        entry = entries[0]
        assert entry["event"] == "test_event"
        assert entry["request_id"] == "req_123"
        assert entry["user_id"] == "usr_456"
        assert entry["status"] == "success"
    
    def test_bind_returns_new_logger(self, capture_logs):
        """Test that bind() returns a new logger instance."""
        bound_logger1 = global_logger.bind(key1="value1")
        bound_logger2 = global_logger.bind(key2="value2")
        
        # They should be different instances
        assert bound_logger1 is not bound_logger2
        assert bound_logger1 is not global_logger
        
        # Log with each to verify they have different context
        bound_logger1.info("event1")
        bound_logger2.info("event2")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 2
        
        # First should have key1
        assert "key1" in entries[0]
        assert "key2" not in entries[0]
        
        # Second should have key2
        assert "key2" in entries[1]
        assert "key1" not in entries[1]
    
    def test_bind_preserves_original_logger(self, capture_logs):
        """Test that bind() doesn't modify the original logger."""
        # Create a bound logger
        bound_logger = global_logger.bind(extra_context="test")
        
        # Log with original logger
        global_logger.info("original_event")
        
        # Log with bound logger
        bound_logger.info("bound_event")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 2
        
        # Original logger shouldn't have the extra context
        assert "extra_context" not in entries[0]
        
        # Bound logger should have it
        assert entries[1]["extra_context"] == "test"
    
    def test_bind_chaining(self, capture_logs):
        """Test that bind() can be chained for nested context."""
        bound1 = global_logger.bind(level1="a")
        bound2 = bound1.bind(level2="b")
        bound3 = bound2.bind(level3="c")
        
        bound3.info("nested_event")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 1
        
        entry = entries[0]
        assert entry["level1"] == "a"
        assert entry["level2"] == "b"
        assert entry["level3"] == "c"
    
    def test_bind_with_empty_context(self, capture_logs):
        """Test that bind() with no arguments still works."""
        bound_logger = global_logger.bind()
        bound_logger.info("test_event")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 1
        assert entries[0]["event"] == "test_event"


class TestLoggerUnbind:
    """Test the unbind() method of FoundationLogger."""
    
    def test_unbind_removes_context(self, capture_logs):
        """Test that unbind() removes specified context keys."""
        # Create logger with context
        bound_logger = global_logger.bind(
            key1="value1",
            key2="value2",
            key3="value3"
        )
        
        # Unbind one key
        unbound_logger = bound_logger.unbind("key2")
        unbound_logger.info("after_unbind")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 1
        
        entry = entries[0]
        assert entry["key1"] == "value1"
        assert "key2" not in entry
        assert entry["key3"] == "value3"
    
    def test_unbind_multiple_keys(self, capture_logs):
        """Test unbinding multiple keys at once."""
        bound_logger = global_logger.bind(
            a="1", b="2", c="3", d="4"
        )
        
        # Unbind multiple keys
        unbound_logger = bound_logger.unbind("a", "c")
        unbound_logger.info("test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        assert "a" not in entry
        assert entry["b"] == "2"
        assert "c" not in entry
        assert entry["d"] == "4"
    
    def test_unbind_nonexistent_key_raises(self, capture_logs):
        """Test that unbind() raises error for non-existent keys."""
        bound_logger = global_logger.bind(existing="value")
        
        # This should raise an error
        with pytest.raises(KeyError):
            bound_logger.unbind("nonexistent")
    
    def test_unbind_returns_new_logger(self, capture_logs):
        """Test that unbind() returns a new logger instance."""
        bound_logger = global_logger.bind(key="value")
        unbound_logger = bound_logger.unbind("key")
        
        assert unbound_logger is not bound_logger
        assert unbound_logger is not global_logger


class TestLoggerTryUnbind:
    """Test the try_unbind() method of FoundationLogger."""
    
    def test_try_unbind_removes_existing_keys(self, capture_logs):
        """Test that try_unbind() removes keys that exist."""
        bound_logger = global_logger.bind(
            key1="value1",
            key2="value2"
        )
        
        # Try to unbind existing key
        unbound_logger = bound_logger.try_unbind("key1")
        unbound_logger.info("test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        assert "key1" not in entry
        assert entry["key2"] == "value2"
    
    def test_try_unbind_ignores_nonexistent_keys(self, capture_logs):
        """Test that try_unbind() doesn't fail for non-existent keys."""
        bound_logger = global_logger.bind(existing="value")
        
        # This should NOT raise an error
        unbound_logger = bound_logger.try_unbind("nonexistent")
        unbound_logger.info("test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        assert entry["existing"] == "value"
    
    def test_try_unbind_mixed_keys(self, capture_logs):
        """Test try_unbind() with mix of existing and non-existing keys."""
        bound_logger = global_logger.bind(a="1", b="2", c="3")
        
        # Try to unbind mix of existing and non-existing
        unbound_logger = bound_logger.try_unbind("a", "nonexistent", "c", "another_missing")
        unbound_logger.info("test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        assert "a" not in entry
        assert entry["b"] == "2"
        assert "c" not in entry
    
    def test_try_unbind_returns_new_logger(self, capture_logs):
        """Test that try_unbind() returns a new logger instance."""
        bound_logger = global_logger.bind(key="value")
        unbound_logger = bound_logger.try_unbind("key")
        
        assert unbound_logger is not bound_logger
        assert unbound_logger is not global_logger


class TestLoggerContextIntegration:
    """Test integration scenarios with context binding."""
    
    def test_global_logger_bind_method_exists(self):
        """Test that global logger has bind method."""
        assert hasattr(global_logger, 'bind')
        assert callable(global_logger.bind)
    
    def test_global_logger_unbind_method_exists(self):
        """Test that global logger has unbind method."""
        assert hasattr(global_logger, 'unbind')
        assert callable(global_logger.unbind)
    
    def test_global_logger_try_unbind_method_exists(self):
        """Test that global logger has try_unbind method."""
        assert hasattr(global_logger, 'try_unbind')
        assert callable(global_logger.try_unbind)
    
    def test_named_logger_also_supports_binding(self, capture_logs):
        """Test that named loggers created with get_logger also support binding."""
        named_logger = get_logger("test.module")
        
        # Should have the same binding methods
        assert hasattr(named_logger, 'bind')
        assert hasattr(named_logger, 'unbind')
        assert hasattr(named_logger, 'try_unbind')
        
        # Test that they work
        bound_named = named_logger.bind(module_context="test")
        bound_named.info("named_logger_event")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 1
        assert entries[0]["module_context"] == "test"
    
    def test_complex_workflow(self, capture_logs):
        """Test a complex logging workflow with binding and unbinding."""
        # Start with global logger
        global_logger.info("start", phase="initialization")
        
        # Create request-scoped logger
        request_logger = global_logger.bind(
            request_id="req_abc",
            user_id="user_123",
            ip="192.168.1.1"
        )
        request_logger.info("request_received")
        
        # Add more context for authentication
        auth_logger = request_logger.bind(
            auth_method="oauth",
            provider="google"
        )
        auth_logger.info("auth_started")
        
        # Remove sensitive data before logging
        clean_logger = auth_logger.try_unbind("ip", "provider")
        clean_logger.info("auth_completed", success=True)
        
        # Back to request logger
        request_logger.info("request_processed", status_code=200)
        
        # And finally global logger
        global_logger.info("end", phase="shutdown")
        
        entries = get_log_entries(capture_logs)
        assert len(entries) == 6
        
        # Verify each entry has expected context
        assert "request_id" not in entries[0]  # start
        assert entries[1]["request_id"] == "req_abc"  # request_received
        assert entries[2]["auth_method"] == "oauth"  # auth_started
        assert "ip" not in entries[3]  # auth_completed (unbound)
        assert entries[4]["request_id"] == "req_abc"  # request_processed
        assert "request_id" not in entries[5]  # end


class TestLoggerBindingEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_bind_with_reserved_keys(self, capture_logs):
        """Test binding with potentially reserved keys."""
        # These shouldn't cause issues
        bound = global_logger.bind(
            event="custom_event",  # 'event' is used internally
            level="custom_level",   # 'level' might be reserved
            timestamp="custom_time"  # 'timestamp' might be reserved
        )
        bound.info("test")
        
        entries = get_log_entries(capture_logs)
        # Should still work, though values might be overridden
        assert len(entries) == 1
    
    def test_bind_with_none_values(self, capture_logs):
        """Test binding with None values."""
        bound = global_logger.bind(
            key1=None,
            key2="value",
            key3=None
        )
        bound.info("test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        # None values should still be included
        assert entry["key1"] is None
        assert entry["key2"] == "value"
        assert entry["key3"] is None
    
    def test_bind_with_complex_values(self, capture_logs):
        """Test binding with complex data types."""
        bound = global_logger.bind(
            list_val=[1, 2, 3],
            dict_val={"nested": "object"},
            tuple_val=(4, 5, 6),
            bool_val=True,
            float_val=3.14
        )
        bound.info("complex_test")
        
        entries = get_log_entries(capture_logs)
        entry = entries[0]
        
        assert entry["list_val"] == [1, 2, 3]
        assert entry["dict_val"] == {"nested": "object"}
        assert entry["tuple_val"] == [4, 5, 6]  # JSON converts tuples to lists
        assert entry["bool_val"] is True
        assert entry["float_val"] == 3.14