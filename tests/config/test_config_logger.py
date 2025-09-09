#
# tests/test_config.py
#
"""
Unit tests for processor assembly helper functions in provide.foundation.config.
"""

import io
import json
from typing import Any

from pytest import CaptureFixture
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, TimeStamper

from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.eventsets.registry import discover_event_sets, get_registry

# env.py removed - use TelemetryConfig.from_env() directly
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
)


def get_proc_name(proc: Any) -> str:
    if hasattr(proc, "__name__"):
        return proc.__name__
    if isinstance(proc, TimeStamper):
        return "TimeStamper"
    if isinstance(proc, JSONRenderer):
        return "JSONRenderer"
    if isinstance(proc, ConsoleRenderer):
        return "ConsoleRenderer"
    return proc.__class__.__name__ if hasattr(proc, "__class__") else str(type(proc))


class TestBuildFormatterProcessorsList:
    def test_build_json_formatter(self) -> None:
        processors = _build_formatter_processors_list(
            LoggingConfig(console_formatter="json"), io.StringIO()
        )
        assert [get_proc_name(p) for p in processors] == [
            "ExceptionRenderer",
            "JSONRenderer",
        ]

    def test_build_keyvalue_formatter(self) -> None:
        processors = _build_formatter_processors_list(
            LoggingConfig(console_formatter="key_value"), io.StringIO()
        )
        assert [get_proc_name(p) for p in processors] == [
            "pop_logger_name_processor",
            "ConsoleRenderer",
        ]


class TestBuildCoreProcessorsList:
    def test_default_config(self) -> None:
        config = TelemetryConfig()
        # Event sets auto-discovered now
        discover_event_sets()
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]
        assert len(processors) == 9
        # Check that inject_trace_context and add_logger_name_emoji_prefix are present
        assert "inject_trace_context" in proc_names
        assert "add_logger_name_emoji_prefix" in proc_names


class TestTelemetryConfigFromEnvEventSets:
    """Tests for deprecated emoji sets - now replaced by event sets."""
    
    def test_event_sets_replaced_emoji_sets(self) -> None:
        """Verify that event sets have replaced emoji sets."""
        # Event sets are now handled through the eventsets module
        from provide.foundation.eventsets.registry import get_registry
        registry = get_registry()
        
        # Check that event sets are registered
        assert ("eventset", "llm") in registry
        assert ("eventset", "http") in registry
        assert ("eventset", "database") in registry
    
    def test_logging_config_no_emoji_sets(self) -> None:
        """Verify LoggingConfig doesn't have deprecated emoji_sets fields."""
        config = TelemetryConfig.from_env()
        # These fields should not exist anymore
        assert not hasattr(config.logging, 'enabled_emoji_sets')
        assert not hasattr(config.logging, 'custom_emoji_sets')


class TestFoundationLogOutputConfigIntegration:
    """Test FOUNDATION_LOG_OUTPUT integration with config warnings."""

    def test_config_warnings_respect_foundation_log_output_stdout(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        """Test that config warnings go to stdout when FOUNDATION_LOG_OUTPUT=stdout."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "stdout")
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")

        config = LoggingConfig.from_env()
        captured = capsys.readouterr()

        # Warning should go to stdout, not stderr
        assert "[Foundation Config Warning]" in captured.out
        assert "[Foundation Config Warning]" not in captured.err

    def test_config_warnings_respect_foundation_log_output_stderr_default(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        """Test that config warnings go to stderr by default."""
        # Ensure no FOUNDATION_LOG_OUTPUT is set (should default to stderr)
        monkeypatch.delenv("FOUNDATION_LOG_OUTPUT", raising=False)
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")

        config = LoggingConfig.from_env()
        captured = capsys.readouterr()

        # Warning should go to stderr (default behavior)
        assert "[Foundation Config Warning]" in captured.err
        assert "[Foundation Config Warning]" not in captured.out

    def test_config_warnings_with_invalid_foundation_log_output(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        """Test config warnings when FOUNDATION_LOG_OUTPUT has invalid value."""
        monkeypatch.setenv("FOUNDATION_LOG_OUTPUT", "invalid_value")
        monkeypatch.setenv("PROVIDE_LOG_LEVEL", "INVALID_LEVEL")

        config = LoggingConfig.from_env()
        captured = capsys.readouterr()

        # Both warnings should go to stderr (fallback)
        assert "[Foundation Config Warning]" in captured.err
        # Should have warning about invalid FOUNDATION_LOG_OUTPUT
        assert "FOUNDATION_LOG_OUTPUT" in captured.err
        # Should also have warning about invalid PROVIDE_LOG_LEVEL
        assert "PROVIDE_LOG_LEVEL" in captured.err
