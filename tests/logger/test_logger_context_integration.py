#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for FoundationLogger context binding integration and edge cases."""

from __future__ import annotations

import json
from typing import Any, TextIO

from provide.testkit import FoundationTestCase

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
                        "🗣️ Foundation bootstrap",
                    ]
                ):
                    continue
                entries.append(entry)
            except json.JSONDecodeError:
                # Skip non-JSON lines
                continue
    return entries


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


# 🧱🏗️🔚
