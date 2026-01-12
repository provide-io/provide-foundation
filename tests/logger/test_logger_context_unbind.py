#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for FoundationLogger unbind() and try_unbind() methods."""

from __future__ import annotations

import json
from typing import Any, TextIO

from provide.testkit import FoundationTestCase
import pytest

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


# 🧱🏗️🔚
