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

from provide.foundation.core import (
    _resolve_active_emoji_config,
)
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)
from provide.foundation.logger.emoji.sets import BUILTIN_EMOJI_SETS

# env.py removed - use TelemetryConfig.from_env() directly
from provide.foundation.logger.processors import (
    _build_core_processors_list,
    _build_formatter_processors_list,
    _config_create_emoji_processors,
    _config_create_timestamp_processors,
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


class TestConfigTimestampProcessors:
    def test_timestamp_processors_default(self) -> None:
        processors = _config_create_timestamp_processors(omit_timestamp=False)
        assert len(processors) == 1 and get_proc_name(processors[0]) == "TimeStamper"

    def test_timestamp_processors_omitted(self) -> None:
        processors = _config_create_timestamp_processors(omit_timestamp=True)
        assert (
            len(processors) == 2
            and get_proc_name(processors[1]) == "pop_timestamp_processor"
        )


class TestConfigEmojiProcessors:
    def test_all_emojis_enabled(self) -> None:
        config = LoggingConfig(
            logger_name_emoji_prefix_enabled=True, das_emoji_prefix_enabled=True
        )
        resolved_config = _resolve_active_emoji_config(
            config, BUILTIN_EMOJI_SETS
        )
        processors = _config_create_emoji_processors(config, resolved_config)
        assert (
            len(processors) == 2
            and get_proc_name(processors[0]) == "add_logger_name_emoji_prefix"
            and callable(processors[1])
        )


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
        resolved_emoji_config = _resolve_active_emoji_config(
            config.logging, BUILTIN_EMOJI_SETS
        )
        processors = _build_core_processors_list(config, resolved_emoji_config)
        assert (
            len(processors) == 8
            and get_proc_name(processors[6]) == "add_logger_name_emoji_prefix"
        )


class TestTelemetryConfigFromEnvSemanticLayers:
    def test_from_env_parses_enabled_emoji_sets(self, monkeypatch) -> None:
        monkeypatch.setenv(
            "PROVIDE_LOG_ENABLED_EMOJI_SETS", "llm, http , database "
        )
        config = TelemetryConfig.from_env()
        assert config.logging.enabled_emoji_sets == ["llm", "http", "database"]

    def test_from_env_handles_malformed_custom_layers_json(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        monkeypatch.setenv(
            "PROVIDE_LOG_CUSTOM_EMOJI_SETS", "[{'name': 'badjson']"
        )
        # _ensure_config_logger_handler removed - warnings now handled by config system
        config = TelemetryConfig.from_env()
        assert config.logging.custom_emoji_sets == []
        captured = capsys.readouterr()
        assert "Invalid JSON in configuration" in captured.err
        assert "PROVIDE_LOG_CUSTOM_EMOJI_SETS" in captured.err

    def test_from_env_handles_type_error_in_custom_layer_data(
        self, monkeypatch, capsys: CaptureFixture
    ) -> None:
        custom_layers_json = json.dumps(
            [{"name": "my_layer", "priority": "not_an_int"}]
        )
        monkeypatch.setenv("PROVIDE_LOG_CUSTOM_EMOJI_SETS", custom_layers_json)
        # _ensure_config_logger_handler removed - warnings now handled by config system
        config = TelemetryConfig.from_env()
        assert config.logging.custom_emoji_sets == []
        captured = capsys.readouterr()
        assert "Error parsing custom emoji set configuration" in captured.err
        assert "PROVIDE_LOG_CUSTOM_EMOJI_SETS" in captured.err


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
