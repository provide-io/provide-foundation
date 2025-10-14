"""Tests for config.defaults module."""

from pathlib import Path

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

from provide.foundation.config.defaults import (
    DEFAULT_ATOMIC_ENCODING,
    DEFAULT_ATOMIC_MODE,
    DEFAULT_DIR_MODE,
    DEFAULT_DIR_PARENTS,
    DEFAULT_FILE_LOCK_TIMEOUT,
    DEFAULT_MISSING_OK,
    DEFAULT_TEMP_CLEANUP,
    DEFAULT_TEMP_PREFIX,
    DEFAULT_TEMP_SUFFIX,
    DEFAULT_TEMP_TEXT_MODE,
    DEFAULT_TEST_CHECKPOINT_TIMEOUT,
    DEFAULT_TEST_PARALLEL_TIMEOUT,
    DEFAULT_TEST_WAIT_TIMEOUT,
    EXIT_ERROR,
    EXIT_SIGINT,
    EXIT_SUCCESS,
    default_empty_dict,
    path_converter,
)
from provide.foundation.crypto.defaults import (
    default_supported_ec_curves,
    default_supported_key_types,
    default_supported_rsa_sizes,
)
from provide.foundation.integrations.openobserve.defaults import (
    DEFAULT_OPENOBSERVE_MAX_RETRIES,
    DEFAULT_OPENOBSERVE_TIMEOUT,
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
    DEFAULT_RATE_LIMIT_GLOBAL,
    DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY,
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
    DEFAULT_TRACE_SAMPLE_RATE,
    DEFAULT_TRACING_ENABLED,
    default_otlp_headers,
)


class TestLoggingDefaults(FoundationTestCase):
    """Test logging-related defaults."""

    def test_log_level_default(self) -> None:
        """Test default log level."""
        assert DEFAULT_LOG_LEVEL == "WARNING"
        assert isinstance(DEFAULT_LOG_LEVEL, str)

    def test_console_formatter_default(self) -> None:
        """Test default console formatter."""
        assert DEFAULT_CONSOLE_FORMATTER == "key_value"
        assert isinstance(DEFAULT_CONSOLE_FORMATTER, str)

    def test_emoji_defaults(self) -> None:
        """Test emoji-related defaults."""
        assert DEFAULT_LOGGER_NAME_EMOJI_ENABLED is True
        assert DEFAULT_DAS_EMOJI_ENABLED is True
        assert isinstance(DEFAULT_LOGGER_NAME_EMOJI_ENABLED, bool)
        assert isinstance(DEFAULT_DAS_EMOJI_ENABLED, bool)

    def test_timestamp_default(self) -> None:
        """Test timestamp omission default."""
        assert DEFAULT_OMIT_TIMESTAMP is False
        assert isinstance(DEFAULT_OMIT_TIMESTAMP, bool)

    def test_foundation_logging_defaults(self) -> None:
        """Test Foundation internal logging defaults."""
        assert DEFAULT_FOUNDATION_SETUP_LOG_LEVEL == "INFO"
        assert DEFAULT_FOUNDATION_LOG_OUTPUT == "stderr"
        assert isinstance(DEFAULT_FOUNDATION_SETUP_LOG_LEVEL, str)
        assert isinstance(DEFAULT_FOUNDATION_LOG_OUTPUT, str)

    def test_rate_limiting_defaults(self) -> None:
        """Test rate limiting defaults."""
        assert DEFAULT_RATE_LIMIT_ENABLED is False
        assert DEFAULT_RATE_LIMIT_EMIT_WARNINGS is True
        assert DEFAULT_RATE_LIMIT_GLOBAL == 5.0
        assert DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY == 1000
        assert DEFAULT_RATE_LIMIT_OVERFLOW_POLICY == "drop_oldest"

        assert isinstance(DEFAULT_RATE_LIMIT_ENABLED, bool)
        assert isinstance(DEFAULT_RATE_LIMIT_EMIT_WARNINGS, bool)
        assert isinstance(DEFAULT_RATE_LIMIT_GLOBAL, float)
        assert isinstance(DEFAULT_RATE_LIMIT_GLOBAL_CAPACITY, int)
        assert isinstance(DEFAULT_RATE_LIMIT_OVERFLOW_POLICY, str)


class TestTelemetryDefaults(FoundationTestCase):
    """Test telemetry-related defaults."""

    def test_global_telemetry_default(self) -> None:
        """Test global telemetry disabled default."""
        assert DEFAULT_TELEMETRY_GLOBALLY_DISABLED is False
        assert isinstance(DEFAULT_TELEMETRY_GLOBALLY_DISABLED, bool)

    def test_tracing_default(self) -> None:
        """Test tracing enabled default."""
        assert DEFAULT_TRACING_ENABLED is True
        assert isinstance(DEFAULT_TRACING_ENABLED, bool)

    def test_metrics_default(self) -> None:
        """Test metrics enabled default."""
        assert DEFAULT_METRICS_ENABLED is True
        assert isinstance(DEFAULT_METRICS_ENABLED, bool)

    def test_otlp_protocol_default(self) -> None:
        """Test OTLP protocol default."""
        assert DEFAULT_OTLP_PROTOCOL == "http/protobuf"
        assert isinstance(DEFAULT_OTLP_PROTOCOL, str)

    def test_trace_sample_rate_default(self) -> None:
        """Test trace sample rate default."""
        assert DEFAULT_TRACE_SAMPLE_RATE == 1.0
        assert isinstance(DEFAULT_TRACE_SAMPLE_RATE, float)
        assert 0.0 <= DEFAULT_TRACE_SAMPLE_RATE <= 1.0


class TestProcessDefaults(FoundationTestCase):
    """Test process-related defaults."""

    def test_process_timeout_defaults(self) -> None:
        """Test process timeout defaults."""
        assert DEFAULT_PROCESS_READLINE_TIMEOUT == 2.0
        assert DEFAULT_PROCESS_READCHAR_TIMEOUT == 1.0
        assert DEFAULT_PROCESS_TERMINATE_TIMEOUT == 7.0
        assert DEFAULT_PROCESS_WAIT_TIMEOUT == 10.0

        assert isinstance(DEFAULT_PROCESS_READLINE_TIMEOUT, float)
        assert isinstance(DEFAULT_PROCESS_READCHAR_TIMEOUT, float)
        assert isinstance(DEFAULT_PROCESS_TERMINATE_TIMEOUT, float)
        assert isinstance(DEFAULT_PROCESS_WAIT_TIMEOUT, float)

        # All timeouts should be positive
        assert DEFAULT_PROCESS_READLINE_TIMEOUT > 0
        assert DEFAULT_PROCESS_READCHAR_TIMEOUT > 0
        assert DEFAULT_PROCESS_TERMINATE_TIMEOUT > 0
        assert DEFAULT_PROCESS_WAIT_TIMEOUT > 0


class TestFileDefaults(FoundationTestCase):
    """Test file and lock-related defaults."""

    def test_file_lock_timeout_default(self) -> None:
        """Test file lock timeout default."""
        assert DEFAULT_FILE_LOCK_TIMEOUT == 10.0
        assert isinstance(DEFAULT_FILE_LOCK_TIMEOUT, float)
        assert DEFAULT_FILE_LOCK_TIMEOUT > 0


class TestResilienceDefaults(FoundationTestCase):
    """Test resilience-related defaults."""

    def test_circuit_breaker_timeout_default(self) -> None:
        """Test circuit breaker recovery timeout default."""
        assert DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT == 60.0
        assert isinstance(DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT, float)
        assert DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT > 0


class TestIntegrationDefaults(FoundationTestCase):
    """Test integration-related defaults."""

    def test_openobserve_defaults(self) -> None:
        """Test OpenObserve integration defaults."""
        assert DEFAULT_OPENOBSERVE_TIMEOUT == 30
        assert DEFAULT_OPENOBSERVE_MAX_RETRIES == 3

        assert isinstance(DEFAULT_OPENOBSERVE_TIMEOUT, int)
        assert isinstance(DEFAULT_OPENOBSERVE_MAX_RETRIES, int)
        assert DEFAULT_OPENOBSERVE_TIMEOUT > 0
        assert DEFAULT_OPENOBSERVE_MAX_RETRIES >= 0


class TestTestingDefaults(FoundationTestCase):
    """Test testing-related defaults."""

    def test_testing_timeout_defaults(self) -> None:
        """Test testing timeout defaults."""
        assert DEFAULT_TEST_WAIT_TIMEOUT == 5.0
        assert DEFAULT_TEST_PARALLEL_TIMEOUT == 10.0
        assert DEFAULT_TEST_CHECKPOINT_TIMEOUT == 5.0

        assert isinstance(DEFAULT_TEST_WAIT_TIMEOUT, float)
        assert isinstance(DEFAULT_TEST_PARALLEL_TIMEOUT, float)
        assert isinstance(DEFAULT_TEST_CHECKPOINT_TIMEOUT, float)

        # All timeouts should be positive
        assert DEFAULT_TEST_WAIT_TIMEOUT > 0
        assert DEFAULT_TEST_PARALLEL_TIMEOUT > 0
        assert DEFAULT_TEST_CHECKPOINT_TIMEOUT > 0


class TestExitCodes(FoundationTestCase):
    """Test exit code constants."""

    def test_exit_code_values(self) -> None:
        """Test exit code constant values."""
        assert EXIT_SUCCESS == 0
        assert EXIT_ERROR == 1
        assert EXIT_SIGINT == 130

        assert isinstance(EXIT_SUCCESS, int)
        assert isinstance(EXIT_ERROR, int)
        assert isinstance(EXIT_SIGINT, int)

    def test_exit_code_uniqueness(self) -> None:
        """Test that exit codes are unique."""
        codes = [EXIT_SUCCESS, EXIT_ERROR, EXIT_SIGINT]
        assert len(set(codes)) == len(codes)


class TestTempFileDefaults(FoundationTestCase):
    """Test temporary file/directory defaults."""

    def test_temp_file_defaults(self) -> None:
        """Test temporary file defaults."""
        assert DEFAULT_TEMP_PREFIX == "provide_"
        assert DEFAULT_TEMP_SUFFIX == ""
        assert DEFAULT_TEMP_CLEANUP is True
        assert DEFAULT_TEMP_TEXT_MODE is False

        assert isinstance(DEFAULT_TEMP_PREFIX, str)
        assert isinstance(DEFAULT_TEMP_SUFFIX, str)
        assert isinstance(DEFAULT_TEMP_CLEANUP, bool)
        assert isinstance(DEFAULT_TEMP_TEXT_MODE, bool)


class TestDirectoryDefaults(FoundationTestCase):
    """Test directory operation defaults."""

    def test_directory_defaults(self) -> None:
        """Test directory operation defaults."""
        assert DEFAULT_DIR_MODE == 0o755
        assert DEFAULT_DIR_PARENTS is True
        assert DEFAULT_MISSING_OK is True

        assert isinstance(DEFAULT_DIR_MODE, int)
        assert isinstance(DEFAULT_DIR_PARENTS, bool)
        assert isinstance(DEFAULT_MISSING_OK, bool)

    def test_directory_mode_validity(self) -> None:
        """Test directory mode is valid octal."""
        # Should be a valid file mode
        assert 0o000 <= DEFAULT_DIR_MODE <= 0o777


class TestAtomicWriteDefaults(FoundationTestCase):
    """Test atomic write defaults."""

    def test_atomic_write_defaults(self) -> None:
        """Test atomic write defaults."""
        assert DEFAULT_ATOMIC_MODE == 0o644
        assert DEFAULT_ATOMIC_ENCODING == "utf-8"

        assert isinstance(DEFAULT_ATOMIC_MODE, int)
        assert isinstance(DEFAULT_ATOMIC_ENCODING, str)

    def test_atomic_mode_validity(self) -> None:
        """Test atomic write mode is valid octal."""
        # Should be a valid file mode
        assert 0o000 <= DEFAULT_ATOMIC_MODE <= 0o777

    def test_atomic_encoding_validity(self) -> None:
        """Test atomic write encoding is valid."""
        # Should be a valid Python encoding
        "test".encode(DEFAULT_ATOMIC_ENCODING)


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
