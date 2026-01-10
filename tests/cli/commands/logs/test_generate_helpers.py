#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for log generation helpers and integration."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.cli.commands.logs.constants import (
    BURROUGHS_PHRASES,
    OPERATIONS,
    SERVICE_NAMES,
)
from provide.foundation.cli.commands.logs.generator import LogGenerator


class TestClickIntegration(FoundationTestCase):
    """Test Click command integration when Click is available."""

    def test_generate_logs_command_exists(self) -> None:
        """Test that generate_logs_command exists."""
        try:
            from provide.foundation.cli.commands.logs.generate import generate_logs_command

            assert generate_logs_command is not None
            assert callable(generate_logs_command)
        except ImportError:
            pytest.skip("Click not available")

    def test_has_click_flag_consistency(self) -> None:
        """Test _HAS_CLICK flag matches actual click availability."""
        from provide.foundation.cli.deps import _HAS_CLICK

        try:
            import click  # noqa: F401

            expected = True
        except ImportError:
            expected = False

        assert expected == _HAS_CLICK

    def test_command_stub_when_click_missing(self) -> None:
        """Test command stub behavior when click is missing."""
        # This test verifies that the stub function exists
        # We can't easily test the actual ImportError behavior without mocking imports
        from provide.foundation.cli.deps import _HAS_CLICK

        if not _HAS_CLICK:
            # If click is not available, the command should be a stub
            from provide.foundation.cli.commands.logs.generate import generate_logs_command

            with pytest.raises(ImportError, match="CLI commands require optional dependencies"):
                generate_logs_command()


class TestLogEntryDataIntegrity(FoundationTestCase):
    """Test data integrity and consistency of generated log entries."""

    def test_log_entry_field_types(self) -> None:
        """Test that log entry fields have correct types."""
        generator = LogGenerator(style="normal", error_rate=0.5)
        entry = generator.generate_log_entry(5)

        # Required fields with expected types
        assert isinstance(entry["message"], str)
        assert isinstance(entry["service"], str) and entry["service"] in SERVICE_NAMES
        assert isinstance(entry["operation"], str) and entry["operation"] in OPERATIONS
        assert isinstance(entry["iteration"], int) and entry["iteration"] == 5
        assert isinstance(entry["trace_id"], str) and entry["trace_id"].startswith("trace_")
        assert isinstance(entry["span_id"], str) and entry["span_id"].startswith("span_")
        assert isinstance(entry["duration_ms"], int) and 10 <= entry["duration_ms"] <= 5000

        # DAS fields
        assert entry["domain"] is None or entry["domain"] in ["user", "system", "data", "api"]
        assert entry["action"] is None or entry["action"] in ["create", "read", "update", "delete"]
        assert entry["status"] is None or entry["status"] in ["success", "pending", "error"]

        # Level field
        assert entry["level"] in ["debug", "info", "warning", "error"]

    def test_error_entry_consistency(self) -> None:
        """Test that error entries have consistent fields."""
        generator = LogGenerator(error_rate=0.8)
        # Generate entries until we get an error (with high error rate)
        for _ in range(50):  # Try up to 50 times
            entry = generator.generate_log_entry(0)
            if entry["level"] == "error":
                assert "error_code" in entry
                assert "error_type" in entry
                assert entry["status"] == "error"
                assert entry["error_code"] in [400, 404, 500, 503]
                assert entry["error_type"] in [
                    "ValidationError",
                    "ServiceUnavailable",
                    "TimeoutError",
                    "DatabaseError",
                    "RateLimitExceeded",
                ]
                break
        else:
            pytest.fail("Could not generate error entry in 50 attempts")

    def test_message_generation_consistency(self) -> None:
        """Test message generation consistency across styles."""
        # Normal style messages
        normal_generator = LogGenerator(style="normal")
        normal_entries = [normal_generator.generate_log_entry(i) for i in range(10)]
        for entry in normal_entries:
            assert "Successfully" in entry["message"]

        # Burroughs style messages
        burroughs_generator = LogGenerator(style="burroughs")
        burroughs_entries = [burroughs_generator.generate_log_entry(i) for i in range(10)]
        for entry in burroughs_entries:
            assert entry["message"] in BURROUGHS_PHRASES


# 🧱🏗️🔚
