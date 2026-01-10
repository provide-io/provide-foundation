#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for config defaults - logging, telemetry, process, file, resilience, integration, testing, and exit codes."""

from provide.testkit import FoundationTestCase

from provide.foundation.config.defaults import (
    DEFAULT_FILE_LOCK_TIMEOUT,
    DEFAULT_TEST_CHECKPOINT_TIMEOUT,
    DEFAULT_TEST_PARALLEL_TIMEOUT,
    DEFAULT_TEST_WAIT_TIMEOUT,
    EXIT_ERROR,
    EXIT_SIGINT,
    EXIT_SUCCESS,
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
        assert DEFAULT_FOUNDATION_SETUP_LOG_LEVEL == "WARNING"
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


# 🧱🏗️🔚
