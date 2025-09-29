"""Tests for FoundationLogger context binding methods (bind, unbind, try_unbind)."""

from __future__ import annotations

import json
from typing import Any, TextIO

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation import logger as global_logger
from provide.foundation.logger import LoggingConfig, TelemetryConfig, get_logger


def setup_json_logging(setup_func) -> None:
    """Helper to setup JSON logging for tests."""
    config = TelemetryConfig(
        logging=LoggingConfig(console_formatter="json", default_level="DEBUG"),
    )
    setup_func(config)


def get_log_entries(output: TextIO) -> list[dict[str, Any]]:
    """Parse JSON log entries from output."""
    output.seek(0)
    entries = []
    for line in output.getvalue().strip().split("\n"):
        if line and not line.startswith("[Foundation Setup]"):
            try:
                entry = json.loads(line)
                # Filter out Hub system logs (registration, setup, bootstrap logs)
                if "event" in entry and any(
                    hub_event in entry["event"]
                    for hub_event in [
                        "🗣️ Registered item",
                        "⚙️ Registered",
                        "🗣️ Foundation bootstrap",
                        "⚙️➡️🚀 Starting Foundation",
                        "⚙️➡️✅ Foundation",
                        "⚙️ Foundation initialized",
                    ]
                ):
                    continue
                entries.append(entry)
            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue
    return entries


class TestLoggerBind(FoundationTestCase):
    """Test the bind() method of FoundationLogger."""

    def test_bind_adds_context(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that bind() adds context to log messages."""
        setup_json_logging(setup_foundation_telemetry_for_test)

        # Create a bound logger with context
        bound_logger = global_logger.bind(request_id="req_123", user_id="usr_456")

        # Log with the bound logger
        bound_logger.info("test_event", custom_field="custom_value")

        # Check the output
        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if "test_event" in e.get("event", "")]
        assert len(test_entries) == 1

        entry = test_entries[0]
        # Event field may contain emoji/DAS pattern, so check if it contains the event name
        assert "test_event" in entry["event"]
        assert entry["request_id"] == "req_123"
        assert entry["user_id"] == "usr_456"
        assert entry["custom_field"] == "custom_value"

    def test_bind_returns_new_logger(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that bind() returns a new logger instance."""
        setup_json_logging(setup_foundation_telemetry_for_test)

        bound_logger1 = global_logger.bind(key1="value1")
        bound_logger2 = global_logger.bind(key2="value2")

        # They should be different instances
        assert bound_logger1 is not bound_logger2
        assert bound_logger1 is not global_logger

        # Log with each to verify they have different context
        bound_logger1.info("event1")
        bound_logger2.info("event2")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test messages
        test_entries = [e for e in entries if "event1" in e.get("event", "") or "event2" in e.get("event", "")]
        assert len(test_entries) == 2

        # Find the specific entries
        event1_entry = next(e for e in test_entries if "event1" in e.get("event", ""))
        event2_entry = next(e for e in test_entries if "event2" in e.get("event", ""))

        # First should have key1
        assert "key1" in event1_entry
        assert "key2" not in event1_entry

        # Second should have key2
        assert "key2" in event2_entry
        assert "key1" not in event2_entry

    def test_bind_preserves_original_logger(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that bind() doesn't modify the original logger."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        # Create a bound logger
        bound_logger = global_logger.bind(extra_context="test")

        # Log with original logger
        global_logger.info("original_event")

        # Log with bound logger
        bound_logger.info("bound_event")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test messages
        test_entries = [
            e for e in entries if "original_event" in e.get("event", "") or "bound_event" in e.get("event", "")
        ]
        assert len(test_entries) == 2

        # Find specific entries
        original_entry = next(e for e in test_entries if "original_event" in e.get("event", ""))
        bound_entry = next(e for e in test_entries if "bound_event" in e.get("event", ""))

        # Original logger shouldn't have the extra context
        assert "extra_context" not in original_entry

        # Bound logger should have it
        assert bound_entry["extra_context"] == "test"

    def test_bind_chaining(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that bind() can be chained for nested context."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound1 = global_logger.bind(level1="a")
        bound2 = bound1.bind(level2="b")
        bound3 = bound2.bind(level3="c")

        bound3.info("nested_event")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if "nested_event" in e.get("event", "")]
        assert len(test_entries) == 1

        entry = test_entries[0]
        assert entry["level1"] == "a"
        assert entry["level2"] == "b"
        assert entry["level3"] == "c"

    def test_bind_with_empty_context(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that bind() with no arguments still works."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind()
        bound_logger.info("test_event")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if "test_event" in e.get("event", "")]
        assert len(test_entries) == 1
        assert "test_event" in test_entries[0]["event"]


class TestLoggerUnbind(FoundationTestCase):
    """Test the unbind() method of FoundationLogger."""

    def test_unbind_removes_context(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that unbind() removes specified context keys."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        # Create logger with context
        bound_logger = global_logger.bind(key1="value1", key2="value2", key3="value3")

        # Unbind one key
        unbound_logger = bound_logger.unbind("key2")
        unbound_logger.info("after_unbind")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if "after_unbind" in e.get("event", "")]
        assert len(test_entries) == 1

        entry = test_entries[0]
        assert entry["key1"] == "value1"
        assert "key2" not in entry
        assert entry["key3"] == "value3"

    def test_unbind_multiple_keys(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test unbinding multiple keys at once."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(a="1", b="2", c="3", d="4")

        # Unbind multiple keys
        unbound_logger = bound_logger.unbind("a", "c")
        unbound_logger.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        assert len(test_entries) == 1
        entry = test_entries[0]

        assert "a" not in entry
        assert entry["b"] == "2"
        assert "c" not in entry
        assert entry["d"] == "4"

    def test_unbind_nonexistent_key_raises(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that unbind() raises error for non-existent keys."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(existing="value")

        # This should raise an error
        with pytest.raises(KeyError):
            bound_logger.unbind("nonexistent")

    def test_unbind_returns_new_logger(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that unbind() returns a new logger instance."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(key="value")
        unbound_logger = bound_logger.unbind("key")

        assert unbound_logger is not bound_logger
        assert unbound_logger is not global_logger


class TestLoggerTryUnbind(FoundationTestCase):
    """Test the try_unbind() method of FoundationLogger."""

    def test_try_unbind_removes_existing_keys(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that try_unbind() removes keys that exist."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(key1="value1", key2="value2")

        # Try to unbind existing key
        unbound_logger = bound_logger.try_unbind("key1")
        unbound_logger.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        assert len(test_entries) == 1
        entry = test_entries[0]

        assert "key1" not in entry
        assert entry["key2"] == "value2"

    def test_try_unbind_ignores_nonexistent_keys(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that try_unbind() doesn't fail for non-existent keys."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(existing="value")

        # This should NOT raise an error
        unbound_logger = bound_logger.try_unbind("nonexistent")
        unbound_logger.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        assert len(test_entries) == 1
        entry = test_entries[0]

        assert entry["existing"] == "value"

    def test_try_unbind_mixed_keys(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test try_unbind() with mix of existing and non-existing keys."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(a="1", b="2", c="3")

        # Try to unbind mix of existing and non-existing
        unbound_logger = bound_logger.try_unbind(
            "a",
            "nonexistent",
            "c",
            "another_missing",
        )
        unbound_logger.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        assert len(test_entries) == 1
        entry = test_entries[0]

        assert "a" not in entry
        assert entry["b"] == "2"
        assert "c" not in entry

    def test_try_unbind_returns_new_logger(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that try_unbind() returns a new logger instance."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound_logger = global_logger.bind(key="value")
        unbound_logger = bound_logger.try_unbind("key")

        assert unbound_logger is not bound_logger
        assert unbound_logger is not global_logger


class TestLoggerContextIntegration(FoundationTestCase):
    """Test integration scenarios with context binding."""

    def test_global_logger_bind_method_exists(self) -> None:
        """Test that global logger has bind method."""
        assert hasattr(global_logger, "bind")
        assert callable(global_logger.bind)

    def test_global_logger_unbind_method_exists(self) -> None:
        """Test that global logger has unbind method."""
        assert hasattr(global_logger, "unbind")
        assert callable(global_logger.unbind)

    def test_global_logger_try_unbind_method_exists(self) -> None:
        """Test that global logger has try_unbind method."""
        assert hasattr(global_logger, "try_unbind")
        assert callable(global_logger.try_unbind)

    def test_named_logger_also_supports_binding(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test that named loggers created with get_logger also support binding."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        named_logger = get_logger("test.module")

        # Should have the same binding methods
        assert hasattr(named_logger, "bind")
        assert hasattr(named_logger, "unbind")
        assert hasattr(named_logger, "try_unbind")

        # Test that they work
        bound_named = named_logger.bind(module_context="test")
        bound_named.info("named_logger_event")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test message
        test_entries = [e for e in entries if "named_logger_event" in e.get("event", "")]
        assert len(test_entries) == 1
        assert test_entries[0]["module_context"] == "test"

    def test_complex_workflow(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test a complex logging workflow with binding and unbinding."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        # Start with global logger
        global_logger.info("start", phase="initialization")

        # Create request-scoped logger
        request_logger = global_logger.bind(
            request_id="req_abc",
            user_id="user_123",
            ip="192.168.1.1",
        )
        request_logger.info("request_received")

        # Add more context for authentication
        auth_logger = request_logger.bind(auth_method="oauth", provider="google")
        auth_logger.info("auth_started")

        # Remove sensitive data before logging
        clean_logger = auth_logger.try_unbind("ip", "provider")
        clean_logger.info("auth_completed", success=True)

        # Back to request logger
        request_logger.info("request_processed", status_code=200)

        # And finally global logger
        global_logger.info("end", phase="shutdown")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter for our test messages
        test_keywords = [
            "start",
            "request_received",
            "auth_started",
            "auth_completed",
            "request_processed",
            "end",
        ]
        test_entries = [e for e in entries if any(kw in e.get("event", "") for kw in test_keywords)]
        assert len(test_entries) == 6

        # Sort by the order they appear to ensure consistency
        start_entry = next(e for e in test_entries if "start" in e.get("event", ""))
        request_received_entry = next(e for e in test_entries if "request_received" in e.get("event", ""))
        auth_started_entry = next(e for e in test_entries if "auth_started" in e.get("event", ""))
        auth_completed_entry = next(e for e in test_entries if "auth_completed" in e.get("event", ""))
        request_processed_entry = next(e for e in test_entries if "request_processed" in e.get("event", ""))
        end_entry = next(e for e in test_entries if "end" in e.get("event", ""))

        # Verify each entry has expected context
        assert "request_id" not in start_entry  # start
        assert request_received_entry["request_id"] == "req_abc"  # request_received
        assert auth_started_entry["auth_method"] == "oauth"  # auth_started
        assert "ip" not in auth_completed_entry  # auth_completed (unbound)
        assert request_processed_entry["request_id"] == "req_abc"  # request_processed
        assert "request_id" not in end_entry  # end


class TestLoggerBindingEdgeCases(FoundationTestCase):
    """Test edge cases and error conditions."""

    def test_bind_with_reserved_keys(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test binding with potentially reserved keys."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        # These shouldn't cause issues
        bound = global_logger.bind(
            event="custom_event",  # 'event' is used internally
            level="custom_level",  # 'level' might be reserved
            timestamp="custom_time",  # 'timestamp' might be reserved
        )
        bound.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter out Hub initialization logs, only look for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        # Should still work, though values might be overridden
        assert len(test_entries) == 1

    def test_bind_with_none_values(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test binding with None values."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound = global_logger.bind(key1=None, key2="value", key3=None)
        bound.info("test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter out Hub initialization logs, only look for our test message
        test_entries = [e for e in entries if e.get("event") == "🔹 test"]
        entry = test_entries[0]

        # None values should still be included
        assert entry["key1"] is None
        assert entry["key2"] == "value"
        assert entry["key3"] is None

    def test_bind_with_complex_values(
        self,
        captured_stderr_for_foundation,
        setup_foundation_telemetry_for_test,
    ) -> None:
        """Test binding with complex data types."""
        setup_json_logging(setup_foundation_telemetry_for_test)
        bound = global_logger.bind(
            list_val=[1, 2, 3],
            dict_val={"nested": "object"},
            tuple_val=(4, 5, 6),
            bool_val=True,
            float_val=3.14,
        )
        bound.info("complex_test")

        entries = get_log_entries(captured_stderr_for_foundation)
        # Filter out Hub initialization logs, only look for our test message
        test_entries = [e for e in entries if "complex_test" in e.get("event", "")]
        assert len(test_entries) == 1
        entry = test_entries[0]

        assert entry["list_val"] == [1, 2, 3]
        assert entry["dict_val"] == {"nested": "object"}
        assert entry["tuple_val"] == [4, 5, 6]  # JSON converts tuples to lists
        assert entry["bool_val"] is True
        assert entry["float_val"] == 3.14
