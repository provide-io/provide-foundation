#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for factory functions, converters, consistency checks, and crypto defaults."""

from pathlib import Path

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

from provide.foundation.config.defaults import (
    DEFAULT_ATOMIC_ENCODING,
    DEFAULT_DIR_PARENTS,
    DEFAULT_FILE_LOCK_TIMEOUT,
    DEFAULT_MISSING_OK,
    DEFAULT_TEMP_CLEANUP,
    DEFAULT_TEMP_TEXT_MODE,
    DEFAULT_TEST_CHECKPOINT_TIMEOUT,
    DEFAULT_TEST_PARALLEL_TIMEOUT,
    DEFAULT_TEST_WAIT_TIMEOUT,
    default_empty_dict,
    path_converter,
)
from provide.foundation.crypto.defaults import (
    default_supported_ec_curves,
    default_supported_key_types,
    default_supported_rsa_sizes,
)
from provide.foundation.logger.defaults import (
    DEFAULT_CONSOLE_FORMATTER,
    DEFAULT_DAS_EMOJI_ENABLED,
    DEFAULT_FOUNDATION_LOG_OUTPUT,
    DEFAULT_FOUNDATION_SETUP_LOG_LEVEL,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOGGER_NAME_EMOJI_ENABLED,
    DEFAULT_OMIT_TIMESTAMP,
    DEFAULT_RATE_LIMIT_EMIT_WARNINGS,
    DEFAULT_RATE_LIMIT_ENABLED,
    DEFAULT_RATE_LIMIT_OVERFLOW_POLICY,
    default_logging_config,
    default_module_levels,
    default_rate_limits,
)
from provide.foundation.process.defaults import (
    DEFAULT_PROCESS_READCHAR_TIMEOUT,
    DEFAULT_PROCESS_READLINE_TIMEOUT,
    DEFAULT_PROCESS_TERMINATE_TIMEOUT,
    DEFAULT_PROCESS_WAIT_TIMEOUT,
)
from provide.foundation.resilience.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.telemetry.defaults import (
    DEFAULT_METRICS_ENABLED,
    DEFAULT_OTLP_PROTOCOL,
    DEFAULT_TELEMETRY_GLOBALLY_DISABLED,
    DEFAULT_TRACING_ENABLED,
    default_otlp_headers,
)


class TestFactoryFunctions(FoundationTestCase):
    """Test factory functions for mutable defaults."""

    def test_default_empty_dict(self) -> None:
        """Test default_empty_dict factory."""
        result = default_empty_dict()
        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

        # Each call should return a new instance
        result1 = default_empty_dict()
        result2 = default_empty_dict()
        assert result1 is not result2

    def test_default_module_levels(self) -> None:
        """Test default_module_levels factory."""
        result = default_module_levels()
        assert isinstance(result, dict)

        # Should include asyncio suppression by default
        assert "asyncio" in result
        assert result["asyncio"] == "INFO"

        # Each call should return a new instance
        result1 = default_module_levels()
        result2 = default_module_levels()
        assert result1 is not result2

        # Should be string keys and string values
        result1["test.module"] = "DEBUG"
        assert isinstance(next(iter(result1.keys())), str)
        assert isinstance(next(iter(result1.values())), str)

    def test_default_rate_limits(self) -> None:
        """Test default_rate_limits factory."""
        result = default_rate_limits()
        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

        # Each call should return a new instance
        result1 = default_rate_limits()
        result2 = default_rate_limits()
        assert result1 is not result2

        # Should accept string keys and tuple[float, float] values
        result1["test.logger"] = (10.0, 100.0)
        assert isinstance(next(iter(result1.keys())), str)
        assert isinstance(next(iter(result1.values())), tuple)
        assert len(next(iter(result1.values()))) == 2
        assert isinstance(next(iter(result1.values()))[0], float)
        assert isinstance(next(iter(result1.values()))[1], float)

    def test_default_otlp_headers(self) -> None:
        """Test default_otlp_headers factory."""
        result = default_otlp_headers()
        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

        # Each call should return a new instance
        result1 = default_otlp_headers()
        result2 = default_otlp_headers()
        assert result1 is not result2

        # Should accept string keys and string values
        result1["X-Custom-Header"] = "value"
        assert isinstance(next(iter(result1.keys())), str)
        assert isinstance(next(iter(result1.values())), str)

    @patch("provide.foundation.logger.config.logging.LoggingConfig.from_env")
    def test_default_logging_config(self, mock_from_env) -> None:
        """Test default_logging_config factory."""
        mock_config = "mock_logging_config"
        mock_from_env.return_value = mock_config

        result = default_logging_config()

        assert result == mock_config
        mock_from_env.assert_called_once()

    @patch("provide.foundation.logger.config.logging.LoggingConfig.from_env")
    def test_default_logging_config_import_location(self, mock_from_env) -> None:
        """Test that default_logging_config imports from correct location."""
        mock_config = "mock_logging_config"
        mock_from_env.return_value = mock_config

        result = default_logging_config()

        # Verify the import is working (no ImportError)
        assert result is not None
        mock_from_env.assert_called_once()


class TestConverterFunctions(FoundationTestCase):
    """Test converter functions."""

    def test_path_converter_with_string(self) -> None:
        """Test path_converter with valid string."""
        result = path_converter("/path/to/file")
        assert isinstance(result, Path)
        assert str(result) == "/path/to/file"

    def test_path_converter_with_none(self) -> None:
        """Test path_converter with None."""
        result = path_converter(None)
        assert result is None

    def test_path_converter_with_empty_string(self) -> None:
        """Test path_converter with empty string."""
        result = path_converter("")
        assert result is None

    def test_path_converter_with_relative_path(self) -> None:
        """Test path_converter with relative path."""
        result = path_converter("relative/path")
        assert isinstance(result, Path)
        assert str(result) == "relative/path"

    def test_path_converter_with_home_directory(self) -> None:
        """Test path_converter with home directory."""
        result = path_converter("~/config.yaml")
        assert isinstance(result, Path)
        assert str(result) == "~/config.yaml"

    def test_path_converter_type_annotations(self) -> None:
        """Test path_converter handles type annotations correctly."""
        # This test ensures the function signature is correct
        from typing import get_type_hints

        hints = get_type_hints(path_converter)

        assert hints["x"] == str | None
        assert hints["return"] == Path | None


class TestDefaultConsistency(FoundationTestCase):
    """Test consistency across different default categories."""

    def test_timeout_consistency(self) -> None:
        """Test that timeout defaults are reasonable and consistent."""
        timeouts = [
            DEFAULT_PROCESS_READLINE_TIMEOUT,
            DEFAULT_PROCESS_READCHAR_TIMEOUT,
            DEFAULT_PROCESS_TERMINATE_TIMEOUT,
            DEFAULT_PROCESS_WAIT_TIMEOUT,
            DEFAULT_FILE_LOCK_TIMEOUT,
            DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
            DEFAULT_TEST_WAIT_TIMEOUT,
            DEFAULT_TEST_PARALLEL_TIMEOUT,
            DEFAULT_TEST_CHECKPOINT_TIMEOUT,
        ]

        # All timeouts should be positive floats
        for timeout in timeouts:
            assert isinstance(timeout, float)
            assert timeout > 0

        # Some logical ordering expectations
        assert DEFAULT_PROCESS_READCHAR_TIMEOUT <= DEFAULT_PROCESS_READLINE_TIMEOUT
        assert DEFAULT_PROCESS_READLINE_TIMEOUT <= DEFAULT_PROCESS_WAIT_TIMEOUT
        assert DEFAULT_TEST_WAIT_TIMEOUT <= DEFAULT_TEST_PARALLEL_TIMEOUT

    def test_boolean_defaults_consistency(self) -> None:
        """Test boolean defaults are properly set."""
        boolean_defaults = [
            DEFAULT_LOGGER_NAME_EMOJI_ENABLED,
            DEFAULT_DAS_EMOJI_ENABLED,
            DEFAULT_OMIT_TIMESTAMP,
            DEFAULT_RATE_LIMIT_ENABLED,
            DEFAULT_RATE_LIMIT_EMIT_WARNINGS,
            DEFAULT_TELEMETRY_GLOBALLY_DISABLED,
            DEFAULT_TRACING_ENABLED,
            DEFAULT_METRICS_ENABLED,
            DEFAULT_TEMP_CLEANUP,
            DEFAULT_TEMP_TEXT_MODE,
            DEFAULT_DIR_PARENTS,
            DEFAULT_MISSING_OK,
        ]

        for default in boolean_defaults:
            assert isinstance(default, bool)

    def test_string_defaults_not_empty(self) -> None:
        """Test that required string defaults are not empty."""
        required_strings = [
            DEFAULT_LOG_LEVEL,
            DEFAULT_CONSOLE_FORMATTER,
            DEFAULT_FOUNDATION_SETUP_LOG_LEVEL,
            DEFAULT_FOUNDATION_LOG_OUTPUT,
            DEFAULT_RATE_LIMIT_OVERFLOW_POLICY,
            DEFAULT_OTLP_PROTOCOL,
            DEFAULT_ATOMIC_ENCODING,
        ]

        for string_default in required_strings:
            assert isinstance(string_default, str)
            assert len(string_default) > 0


class TestCryptoFactoryFunctions(FoundationTestCase):
    """Test crypto-related factory functions."""

    def test_default_supported_ec_curves(self) -> None:
        """Test default_supported_ec_curves factory."""
        result = default_supported_ec_curves()
        assert isinstance(result, set)
        assert len(result) == 3
        assert result == {"secp256r1", "secp384r1", "secp521r1"}

        # Each call should return a new instance
        result1 = default_supported_ec_curves()
        result2 = default_supported_ec_curves()
        assert result1 is not result2

    def test_default_supported_key_types(self) -> None:
        """Test default_supported_key_types factory."""
        result = default_supported_key_types()
        assert isinstance(result, set)
        assert len(result) == 3
        assert result == {"rsa", "ecdsa", "ed25519"}

        # Each call should return a new instance
        result1 = default_supported_key_types()
        result2 = default_supported_key_types()
        assert result1 is not result2

    def test_default_supported_rsa_sizes(self) -> None:
        """Test default_supported_rsa_sizes factory."""
        result = default_supported_rsa_sizes()
        assert isinstance(result, set)
        assert len(result) == 3
        assert result == {2048, 3072, 4096}

        # Each call should return a new instance
        result1 = default_supported_rsa_sizes()
        result2 = default_supported_rsa_sizes()
        assert result1 is not result2


# 🧱🏗️🔚
