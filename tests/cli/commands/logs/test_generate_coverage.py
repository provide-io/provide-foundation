"""Comprehensive tests for CLI logs generate command."""

from __future__ import annotations

import random
import threading

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.cli.commands.logs.constants import (
    BURROUGHS_PHRASES,
    OPERATIONS,
    SERVICE_NAMES,
)
from provide.foundation.cli.commands.logs.generate import (
    generate_log_entry,
    generate_span_id,
    generate_trace_id,
)


class TestConstants(FoundationTestCase):
    """Test module constants."""

    def test_burroughs_phrases_exist(self) -> None:
        """Test that Burroughs phrases are defined."""
        assert isinstance(BURROUGHS_PHRASES, list)
        assert len(BURROUGHS_PHRASES) > 0
        assert all(isinstance(phrase, str) for phrase in BURROUGHS_PHRASES)

    def test_service_names_exist(self) -> None:
        """Test that service names are defined."""
        assert isinstance(SERVICE_NAMES, list)
        assert len(SERVICE_NAMES) > 0
        assert all(isinstance(name, str) for name in SERVICE_NAMES)

    def test_operations_exist(self) -> None:
        """Test that operations are defined."""
        assert isinstance(OPERATIONS, list)
        assert len(OPERATIONS) > 0
        assert all(isinstance(op, str) for op in OPERATIONS)

    def test_has_click_flag_exists(self) -> None:
        """Test that _HAS_CLICK flag is defined."""
        from provide.foundation.cli.deps import _HAS_CLICK

        assert isinstance(_HAS_CLICK, bool)


class TestTraceSpanGeneration(FoundationTestCase):
    """Test trace and span ID generation."""

    def setup_method(self) -> None:
        """Reset counters before each test."""
        super().setup_method()
        import provide.foundation.cli.commands.logs.generator as generator_module

        generator_module._default_generator._trace_counter = 0
        generator_module._default_generator._span_counter = 0

    def test_generate_trace_id(self) -> None:
        """Test trace ID generation."""
        trace_id = generate_trace_id()
        assert trace_id == "trace_00000000"

        # Second call should increment
        trace_id_2 = generate_trace_id()
        assert trace_id_2 == "trace_00000001"

    def test_generate_span_id(self) -> None:
        """Test span ID generation."""
        span_id = generate_span_id()
        assert span_id == "span_00000000"

        # Second call should increment
        span_id_2 = generate_span_id()
        assert span_id_2 == "span_00000001"

    def test_trace_id_thread_safety(self) -> None:
        """Test that trace ID generation is thread-safe."""
        trace_ids = []

        def generate_multiple() -> None:
            for _ in range(10):
                trace_ids.append(generate_trace_id())

        threads = [threading.Thread(daemon=True, target=generate_multiple) for _ in range(5)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10.0)

        # Should have 50 unique trace IDs
        assert len(trace_ids) == 50
        assert len(set(trace_ids)) == 50

    def test_span_id_thread_safety(self) -> None:
        """Test that span ID generation is thread-safe."""
        span_ids = []

        def generate_multiple() -> None:
            for _ in range(10):
                span_ids.append(generate_span_id())

        threads = [threading.Thread(daemon=True, target=generate_multiple) for _ in range(5)]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10.0)

        # Should have 50 unique span IDs
        assert len(span_ids) == 50
        assert len(set(span_ids)) == 50


class TestGenerateLogEntry(FoundationTestCase):
    """Test log entry generation."""

    def setup_method(self) -> None:
        """Reset counters and random seed before each test."""
        super().setup_method()
        import provide.foundation.cli.commands.logs.generator as generator_module

        generator_module._default_generator._trace_counter = 0
        generator_module._default_generator._span_counter = 0
        random.seed(42)  # For deterministic tests

    def test_generate_log_entry_basic(self) -> None:
        """Test basic log entry generation."""
        entry = generate_log_entry(0)

        assert isinstance(entry, dict)
        assert "message" in entry
        assert "service" in entry
        assert "operation" in entry
        assert "iteration" in entry
        assert "trace_id" in entry
        assert "span_id" in entry
        assert "duration_ms" in entry

        assert entry["iteration"] == 0
        assert entry["service"] in SERVICE_NAMES
        assert entry["operation"] in OPERATIONS
        assert isinstance(entry["duration_ms"], int)
        assert 10 <= entry["duration_ms"] <= 5000

    def test_generate_log_entry_normal_style(self) -> None:
        """Test log entry generation with normal style."""
        entry = generate_log_entry(0, style="normal")

        message = entry["message"]
        assert "Successfully" in message
        # Should contain one of the operations and objects
        operations = ["processed", "validated", "executed", "transformed", "cached", "synced"]
        objects = ["request", "query", "data", "event", "message", "transaction"]

        assert any(op in message for op in operations)
        assert any(obj in message for obj in objects)

    def test_generate_log_entry_burroughs_style(self) -> None:
        """Test log entry generation with Burroughs style."""
        entry = generate_log_entry(0, style="burroughs")

        message = entry["message"]
        assert message in BURROUGHS_PHRASES

    def test_generate_log_entry_error_rate_zero(self) -> None:
        """Test log entry generation with zero error rate."""
        # Generate multiple entries to ensure no errors
        for i in range(20):
            entry = generate_log_entry(i, error_rate=0.0)

            # Should not have error-specific fields
            assert "error_code" not in entry
            assert "error_type" not in entry
            assert entry["level"] in ["debug", "info", "warning"]
            assert entry["status"] in ["success", "pending", None]

    def test_generate_log_entry_error_rate_one(self) -> None:
        """Test log entry generation with 100% error rate."""
        entry = generate_log_entry(0, error_rate=1.0)

        # Should always be an error
        assert entry["level"] == "error"
        assert "error_code" in entry
        assert "error_type" in entry
        assert entry["error_code"] in [400, 404, 500, 503]
        assert entry["error_type"] in [
            "ValidationError",
            "ServiceUnavailable",
            "TimeoutError",
            "DatabaseError",
            "RateLimitExceeded",
        ]
        assert entry["status"] == "error"

    def test_generate_log_entry_domain_action_status(self) -> None:
        """Test DAS (Domain-Action-Status) fields."""
        entry = generate_log_entry(0)

        assert "domain" in entry
        assert "action" in entry
        assert "status" in entry

        if entry["domain"] is not None:
            assert entry["domain"] in ["user", "system", "data", "api"]
        if entry["action"] is not None:
            assert entry["action"] in ["create", "read", "update", "delete"]
        if entry["status"] is not None:
            assert entry["status"] in ["success", "pending", "error"]

    def test_generate_log_entry_trace_id_logic(self) -> None:
        """Test trace ID assignment logic."""
        # Index 0 should generate new trace ID
        entry_0 = generate_log_entry(0)
        assert entry_0["trace_id"] == "trace_00000000"

        # Indices 1-9 should reuse the same trace ID
        for i in range(1, 10):
            entry = generate_log_entry(i)
            assert entry["trace_id"] == "trace_00000000"

        # Index 10 should generate a new trace ID
        entry_10 = generate_log_entry(10)
        assert entry_10["trace_id"] == "trace_00000001"

    def test_generate_log_entry_unique_span_ids(self) -> None:
        """Test that each entry gets a unique span ID."""
        entries = [generate_log_entry(i) for i in range(5)]
        span_ids = [entry["span_id"] for entry in entries]

        assert len(set(span_ids)) == 5  # All unique
        for i, span_id in enumerate(span_ids):
            assert span_id == f"span_{i:08d}"


class TestHelperFunctions(FoundationTestCase):
    """Test helper functions from the generate module."""

    @patch("provide.foundation.cli.commands.logs.stats.click")
    def test_print_generation_config(self, mock_click: Mock) -> None:
        """Test print_generation_config function."""
        from provide.foundation.cli.commands.logs.stats import print_generation_config

        print_generation_config(
            count=100,
            rate=10.0,
            stream="test",
            style="normal",
            error_rate=0.1,
            enable_rate_limit=False,
            rate_limit=50.0,
        )

        # Should have called click.echo multiple times
        assert mock_click.echo.call_count >= 4

    @patch("provide.foundation.logger.ratelimit.GlobalRateLimiter")
    def test_configure_rate_limiter_enabled(self, mock_limiter_class: Mock) -> None:
        """Test _configure_rate_limiter with rate limiting enabled."""
        from provide.foundation.cli.commands.logs.generate import _configure_rate_limiter

        mock_limiter = Mock()
        mock_limiter_class.return_value = mock_limiter

        _configure_rate_limiter(enable_rate_limit=True, rate_limit=100.0)

        mock_limiter_class.assert_called_once()
        mock_limiter.configure.assert_called_once_with(
            global_rate=100.0,
            global_capacity=200.0,
        )

    def test_configure_rate_limiter_disabled(self) -> None:
        """Test _configure_rate_limiter with rate limiting disabled."""
        from provide.foundation.cli.commands.logs.generate import _configure_rate_limiter

        # Should not raise any errors
        _configure_rate_limiter(enable_rate_limit=False, rate_limit=100.0)

    @patch("provide.foundation.cli.commands.logs.generator.get_logger")
    def test_send_log_entry_success(self, mock_get_logger: Mock) -> None:
        """Test send_log_entry success case."""
        from provide.foundation.cli.commands.logs.generator import LogGenerator

        # Mock logger
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        entry = {
            "service": "test-service",
            "level": "info",
            "message": "test message",
            "extra_field": "value",
        }

        generator = LogGenerator()
        logs_sent, logs_failed, logs_rate_limited = generator.send_log_entry(
            entry,
            0,
            0,
            0,
        )

        assert logs_sent == 1
        assert logs_failed == 0
        assert logs_rate_limited == 0

        mock_get_logger.assert_called_once_with("generated.test-service")
        mock_logger.info.assert_called_once_with("test message", service="test-service", extra_field="value")

    @patch("provide.foundation.cli.commands.logs.generator.get_logger")
    def test_send_log_entry_failure(self, mock_get_logger: Mock) -> None:
        """Test send_log_entry failure case."""
        from provide.foundation.cli.commands.logs.generator import LogGenerator

        # Mock logger to raise exception
        mock_logger = Mock()
        mock_logger.info.side_effect = Exception("Logging failed")
        mock_get_logger.return_value = mock_logger

        entry = {
            "service": "test-service",
            "level": "info",
            "message": "test message",
        }

        generator = LogGenerator()
        logs_sent, logs_failed, logs_rate_limited = generator.send_log_entry(
            entry,
            0,
            0,
            0,
        )

        assert logs_sent == 0
        assert logs_failed == 1
        assert logs_rate_limited == 0

    @patch("provide.foundation.cli.commands.logs.generator.get_logger")
    def test_send_log_entry_rate_limited(self, mock_get_logger: Mock) -> None:
        """Test send_log_entry rate limit case."""
        from provide.foundation.cli.commands.logs.generator import LogGenerator
        from provide.foundation.errors import RateLimitExceededError

        # Mock logger to raise rate limit exception
        mock_logger = Mock()
        mock_logger.info.side_effect = RateLimitExceededError("Rate limit exceeded")
        mock_get_logger.return_value = mock_logger

        entry = {
            "service": "test-service",
            "level": "info",
            "message": "test message",
        }

        generator = LogGenerator()
        logs_sent, logs_failed, logs_rate_limited = generator.send_log_entry(
            entry,
            0,
            0,
            0,
        )

        assert logs_sent == 0
        assert logs_failed == 1
        assert logs_rate_limited == 1  # Should detect RateLimitExceededError

    @patch("provide.foundation.cli.commands.logs.stats.click")
    def test_print_stats(self, mock_click: Mock) -> None:
        """Test print_stats function."""
        from provide.foundation.cli.commands.logs.stats import print_stats

        last_stats_time, last_stats_sent = print_stats(
            current_time=10.0,
            last_stats_time=9.0,
            logs_sent=100,
            last_stats_sent=90,
            logs_failed=5,
            enable_rate_limit=True,
            logs_rate_limited=2,
        )

        assert last_stats_time == 10.0
        assert last_stats_sent == 100
        mock_click.echo.assert_called_once()

    @patch("provide.foundation.cli.commands.logs.stats.click")
    def test_print_final_stats(self, mock_click: Mock) -> None:
        """Test print_final_stats function."""
        from provide.foundation.cli.commands.logs.stats import print_final_stats

        print_final_stats(
            logs_sent=1000,
            logs_failed=50,
            logs_rate_limited=10,
            total_time=100.0,
            rate=10.0,
            enable_rate_limit=True,
        )

        # Should call click.echo multiple times for the final report
        assert mock_click.echo.call_count >= 5


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
        entry = generate_log_entry(5, style="normal", error_rate=0.5)

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
        # Generate entries until we get an error (with high error rate)
        for _ in range(50):  # Try up to 50 times
            entry = generate_log_entry(0, error_rate=0.8)
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
        normal_entries = [generate_log_entry(i, style="normal") for i in range(10)]
        for entry in normal_entries:
            assert "Successfully" in entry["message"]

        # Burroughs style messages
        burroughs_entries = [generate_log_entry(i, style="burroughs") for i in range(10)]
        for entry in burroughs_entries:
            assert entry["message"] in BURROUGHS_PHRASES
