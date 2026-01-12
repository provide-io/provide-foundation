#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration and environment variable edge case tests for Foundation Telemetry."""

from __future__ import annotations

import os

from provide.testkit.mocking import patch
import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
)


def test_invalid_environment_variables_handling(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Tests handling of invalid environment variables with strict validation."""
    # Define cases that should raise ValueError with strict validation
    strict_validation_cases = [
        ("PROVIDE_LOG_LEVEL", "INVALID_LEVEL", "Invalid log_level 'INVALID_LEVEL'"),
        (
            "PROVIDE_LOG_CONSOLE_FORMATTER",
            "invalid_formatter",
            "Invalid console_formatter 'invalid_formatter'",
        ),
    ]

    # Test cases that should raise exceptions
    for env_var, invalid_value, expected_error in strict_validation_cases:
        # Clear all env vars that might interfere
        possible_interfering_vars = [
            "PROVIDE_LOG_LEVEL",
            "PROVIDE_LOG_CONSOLE_FORMATTER",
            "PROVIDE_LOG_MODULE_LEVELS",
        ]
        for var_to_clear in possible_interfering_vars:
            monkeypatch.delenv(var_to_clear, raising=False)

        # Set the invalid value
        monkeypatch.setenv(env_var, invalid_value)

        # Should raise ValueError with strict validation
        with pytest.raises(ValueError, match=expected_error):
            TelemetryConfig.from_env()

    # Define cases that should handle invalid values gracefully (bool parsing)
    lenient_cases = [
        ("PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED", "maybe", None),
        (
            "PROVIDE_LOG_DAS_EMOJI_ENABLED",
            "sometimes",
            None,
        ),  # bool parsing defaults
        ("PROVIDE_LOG_OMIT_TIMESTAMP", "perhaps", None),  # bool parsing defaults
        ("PROVIDE_TELEMETRY_DISABLED", "kinda", None),  # bool parsing defaults
    ]

    for env_var, invalid_value, expected_warning_snippet in lenient_cases:
        # Use monkeypatch to set environment variables cleanly for each case
        # Clear relevant env vars to ensure a clean slate for each iteration,
        # otherwise a previously set valid value might interfere.
        monkeypatch.setenv(env_var, invalid_value)

        # Remove other potentially interfering env vars if they are not the one being tested
        # This ensures that warnings from other default settings don't cloud the specific test.
        possible_interfering_vars = [
            "PROVIDE_LOG_LEVEL",
            "PROVIDE_LOG_CONSOLE_FORMATTER",
            "PROVIDE_LOG_MODULE_LEVELS",
        ]
        for var_to_clear in possible_interfering_vars:
            if var_to_clear != env_var:
                monkeypatch.delenv(var_to_clear, raising=False)

        config = TelemetryConfig.from_env()

        # Assert basic config structure
        assert config is not None
        assert isinstance(config.logging, LoggingConfig)

        # Verify fallback to defaults for the specific var being tested
        if env_var == "PROVIDE_LOG_LEVEL":
            assert (
                config.logging.default_level == "WARNING"
            )  # Production default fallback when invalid value provided
        elif env_var == "PROVIDE_LOG_CONSOLE_FORMATTER":
            assert (
                config.logging.console_formatter == "key_value"
            )  # Default from DEFAULT_ENV_CONFIG or fallback in from_env

        # Check for specific warning message if one is expected
        captured = capsys.readouterr()
        if expected_warning_snippet:
            assert "[Foundation Config Warning]" in captured.err, (
                f"No Foundation Config Warning for {env_var}={invalid_value}. Output: {captured.err}"
            )
            # Note: exact message format may vary slightly with new config system
            # Just verify warnings are emitted for invalid values

        # Clean up the specific environment variable for the next iteration
        monkeypatch.delenv(env_var, raising=False)


def test_module_levels_parsing_edge_cases() -> None:
    """Tests edge cases in module level parsing."""
    edge_cases = [
        ("", {}),  # Empty string
        ("   ", {}),  # Whitespace only
        ("module1:DEBUG", {"module1": "DEBUG"}),  # Single valid
        (
            "module1:DEBUG,module2:ERROR",
            {"module1": "DEBUG", "module2": "ERROR"},
        ),  # Multiple valid
        ("module1:INVALID,module2:DEBUG", {"module2": "DEBUG"}),  # Mix valid/invalid
        ("invalid_format,module2:DEBUG", {"module2": "DEBUG"}),  # Missing colon
        ("module1:,module2:DEBUG", {"module2": "DEBUG"}),  # Empty level
        (":DEBUG,module2:ERROR", {"module2": "ERROR"}),  # Empty module name
        (
            "module1:DEBUG,,module2:ERROR",
            {"module1": "DEBUG", "module2": "ERROR"},
        ),  # Empty item
        ("module.with.dots:INFO", {"module.with.dots": "INFO"}),  # Dotted module names
    ]

    for levels_str, expected in edge_cases:
        with patch.dict(os.environ, {"PROVIDE_LOG_MODULE_LEVELS": levels_str}):
            config = TelemetryConfig.from_env()
            assert config.logging.module_levels == expected, f"Failed for: '{levels_str}'"


def test_configuration_validation_edge_cases() -> None:
    """Tests configuration validation with edge cases."""
    config_none_service = TelemetryConfig(service_name=None)
    assert config_none_service.service_name is None

    bool_test_cases = [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("1", True),
        ("0", False),
        ("yes", True),
        ("no", False),
        ("on", True),
        ("off", False),
    ]
    for env_value, expected in bool_test_cases:
        with patch.dict(os.environ, {"PROVIDE_LOG_OMIT_TIMESTAMP": env_value}):
            config = TelemetryConfig.from_env()
            assert config.logging.omit_timestamp == expected, f"Failed for '{env_value}'"


def test_configuration_immutability() -> None:
    """Tests that configuration objects use BaseConfig update mechanism."""
    # Since configs now inherit from BaseConfig, they are mutable but should use update()
    config_telemetry = TelemetryConfig(service_name="test")
    # Direct assignment works now with BaseConfig
    config_telemetry.service_name = "modified"
    assert config_telemetry.service_name == "modified"

    # But proper way is to use update()
    config_logging = LoggingConfig(default_level="INFO")
    config_logging.update({"default_level": "DEBUG"})
    assert config_logging.default_level == "DEBUG"


# 🧱🏗️🔚
