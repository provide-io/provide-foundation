#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for FoundationLogger bind() method."""

from __future__ import annotations

import json
from typing import Any, TextIO

from provide.testkit import FoundationTestCase

from provide.foundation import logger as global_logger
from provide.foundation.logger import LoggingConfig, TelemetryConfig


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


# 🧱🏗️🔚
