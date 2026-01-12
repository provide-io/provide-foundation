#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for processor assembly helper functions in provide.foundation.config."""

import io
from typing import Any

from provide.testkit import FoundationTestCase
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, TimeStamper

from provide.foundation.eventsets.registry import discover_event_sets
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)

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


class TestBuildFormatterProcessorsList(FoundationTestCase):
    def test_build_json_formatter(self) -> None:
        processors = _build_formatter_processors_list(
            LoggingConfig(console_formatter="json"),
            io.StringIO(),
        )
        assert [get_proc_name(p) for p in processors] == [
            "ExceptionRenderer",
            "JSONRenderer",
        ]

    def test_build_keyvalue_formatter(self) -> None:
        processors = _build_formatter_processors_list(
            LoggingConfig(console_formatter="key_value"),
            io.StringIO(),
        )
        assert [get_proc_name(p) for p in processors] == [
            "pop_logger_name_processor",
            "ConsoleRenderer",
        ]


class TestBuildCoreProcessorsList(FoundationTestCase):
    def test_default_config(self) -> None:
        config = TelemetryConfig()
        # Event sets auto-discovered now
        discover_event_sets()
        processors = _build_core_processors_list(config)
        proc_names = [get_proc_name(p) for p in processors]
        assert len(processors) == 11  # Added strip_foundation_context processor
        # Check that inject_trace_context and add_logger_name_emoji_prefix are present
        assert "inject_trace_context" in proc_names
        assert "add_logger_name_emoji_prefix" in proc_names
        # Check that sanitization processor is present
        assert "sanitization_processor" in proc_names
        # Check that strip_foundation_context is present
        assert "strip_foundation_context" in proc_names


class TestTelemetryConfigFromEnvEventSets(FoundationTestCase):
    """Tests for deprecated emoji sets - now replaced by event sets."""

    def test_logging_config_no_emoji_sets(self) -> None:
        """Verify LoggingConfig doesn't have deprecated emoji_sets fields."""
        config = TelemetryConfig.from_env()
        # These fields should not exist anymore
        assert not hasattr(config.logging, "enabled_emoji_sets")
        assert not hasattr(config.logging, "custom_emoji_sets")


# 🧱🏗️🔚
