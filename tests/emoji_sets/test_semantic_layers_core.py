# tests/test_emoji_sets.py
"""
Tests for Emoji Layer configuration, resolution, and processing.
"""

from collections.abc import Callable
import io

import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    logger as global_logger,
)
from provide.foundation.core import (
    _resolve_active_emoji_config,
    reset_foundation_setup_for_testing,
)
from provide.foundation.logger.emoji.sets import (
    BUILTIN_EMOJI_SETS,
    HTTP_EMOJI_SET,
    LEGACY_DAS_EMOJI_SETS,
    LLM_EMOJI_SET,
)
from provide.foundation.logger.emoji.types import (
    CustomDasEmojiSet,
    FieldToEmojiMapping,
    EmojiSetConfig,
)

ResolvedEmojiConfigForTest = tuple[
    list[FieldToEmojiMapping], dict[str]
]


@pytest.fixture(autouse=True)
def auto_reset_telemetry():
    reset_foundation_setup_for_testing()
    yield
    reset_foundation_setup_for_testing()


class TestResolveActiveEmojiConfig:
    def test_no_layers_enabled(self) -> None:
        lc = LoggingConfig()
        resolved_fields, resolved_emoji_sets = _resolve_active_emoji_config(
            lc, BUILTIN_EMOJI_SETS
        )
        assert resolved_fields == []
        for les in LEGACY_DAS_EMOJI_SETS:
            assert les.name in resolved_emoji_sets

    def test_enable_multiple_builtin_layers_no_conflict(self) -> None:
        lc = LoggingConfig(enabled_emoji_sets=["llm", "http"])
        resolved_fields, resolved_emoji_sets = _resolve_active_emoji_config(
            lc, BUILTIN_EMOJI_SETS
        )
        llm_field_keys = {f.log_key for f in LLM_EMOJI_SET.field_definitions}
        http_field_keys = {f.log_key for f in HTTP_EMOJI_SET.field_definitions}
        expected_field_count = len(llm_field_keys.union(http_field_keys))
        assert len(resolved_fields) == expected_field_count
        assert (
            "llm_provider" in resolved_emoji_sets
            and "http_method" in resolved_emoji_sets
        )

    def test_layer_priority_for_field_definitions(self) -> None:
        field1 = FieldToEmojiMapping(
            log_key="shared_key", description="from layer1"
        )
        layer1 = EmojiSetConfig(name="layer1", field_definitions=[field1], priority=10)
        field2 = FieldToEmojiMapping(
            log_key="shared_key", description="from layer2"
        )
        layer2 = EmojiSetConfig(name="layer2", field_definitions=[field2], priority=20)
        lc = LoggingConfig(custom_emoji_sets=[layer1, layer2])
        resolved_fields, _ = _resolve_active_emoji_config(lc, {})
        assert (
            len(resolved_fields) == 1
            and resolved_fields[0].description == "from layer2"
        )


class TestSetupWithLayers:
    def _filter_app_logs(self, output: str) -> str:
        return "\n".join(
            [
                line
                for line in output.splitlines()
                if not line.startswith("[Foundation Setup]")
            ]
        )

    def test_setup_with_enabled_llm_layer(
        self,
        setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
        captured_stderr_for_foundation: io.StringIO,
    ) -> None:
        config = TelemetryConfig(
            logging=LoggingConfig(
                enabled_emoji_sets=["llm"],
                console_formatter="key_value",
                das_emoji_prefix_enabled=True,
                logger_name_emoji_prefix_enabled=False,
            )
        )
        setup_foundation_telemetry_for_test(config)
        global_logger.info(
            "LLM Generation",
            **{
                "llm.provider": "openai",
                "llm.task": "generation",
                "llm.outcome": "success",
            },
        )
        captured = self._filter_app_logs(captured_stderr_for_foundation.getvalue())
        assert "[🤖][✍️][👍] LLM Generation" in captured

    def test_setup_with_custom_layer_overriding_builtin_emojis(
        self,
        setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
        captured_stderr_for_foundation: io.StringIO,
    ) -> None:
        my_llm_provider_emojis = CustomDasEmojiSet(
            name="llm_provider", emojis={"openai": "🧠MAX", "default": "💡CUST"}
        )
        config = TelemetryConfig(
            logging=LoggingConfig(
                enabled_emoji_sets=["llm"],
                user_defined_emoji_sets=[my_llm_provider_emojis],
                console_formatter="key_value",
                das_emoji_prefix_enabled=True,
                logger_name_emoji_prefix_enabled=False,
            )
        )
        setup_foundation_telemetry_for_test(config)
        global_logger.info(
            "LLM Call",
            **{"llm.provider": "openai", "llm.task": "chat", "llm.outcome": "error"},
        )
        captured = self._filter_app_logs(captured_stderr_for_foundation.getvalue())
        assert "[🧠MAX][💬][🔥] LLM Call" in captured

    def test_env_var_parsing_for_layers(
        self,
        monkeypatch: pytest.MonkeyPatch,
        setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
        captured_stderr_for_foundation: io.StringIO,
    ) -> None:
        monkeypatch.setenv("FOUNDATION_LOG_ENABLED_EMOJI_SETS", "http")
        monkeypatch.setenv(
            "FOUNDATION_LOG_USER_DEFINED_EMOJI_SETS",
            '[{"name": "http_method", "emojis": {"get": "🔽", "default": "🌐"}}]',
        )
        monkeypatch.setenv("FOUNDATION_LOG_LOGGER_NAME_EMOJI_ENABLED", "false")
        monkeypatch.setenv("FOUNDATION_LOG_CONSOLE_FORMATTER", "key_value")
        setup_foundation_telemetry_for_test(TelemetryConfig.from_env())
        global_logger.info(
            "HTTP GET", **{"http.method": "get", "http.status_class": "2xx"}
        )
        captured = self._filter_app_logs(captured_stderr_for_foundation.getvalue())
        assert "[🔽][✅] HTTP GET" in captured
