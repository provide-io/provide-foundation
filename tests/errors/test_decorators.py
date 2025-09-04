"""Tests for provide.foundation.errors.decorators module."""

import time
from typing import Never
from unittest.mock import ANY, MagicMock, patch

import pytest

from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.decorators import (
    CircuitBreaker,
    circuit_breaker,
    fallback_on_error,
    retry_on_error,
    suppress_and_log,
    with_error_handling,
)
from provide.foundation.errors.integration import NetworkError
from provide.foundation.errors.types import BackoffStrategy, RetryPolicy


class TestWithErrorHandling:
    """Test with_error_handling decorator."""

    def test_successful_function(self) -> None:
        """Test that successful functions work normally."""

        @with_error_handling(fallback="default")
        def successful_func() -> str:
            return "success"

        assert successful_func() == "success"

    def test_fallback_on_error(self) -> None:
        """Test that fallback is returned on error."""

        @with_error_handling(fallback="default")
        def failing_func() -> Never:
            raise ValueError("test error")

        with pytest.raises(ValueError):
            failing_func()

    def test_suppress_specific_errors(self) -> None:
        """Test suppressing specific error types."""

        @with_error_handling(fallback="default", suppress=(KeyError, ValueError))
        def func(error_type) -> Never:
            if error_type == "key":
                raise KeyError("key error")
            elif error_type == "value":
                raise ValueError("value error")
            else:
                raise TypeError("type error")

        assert func("key") == "default"
        assert func("value") == "default"

        with pytest.raises(TypeError):
            func("type")

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_enabled(self, mock_logger) -> None:
        """Test that errors are logged when log_errors=True."""

        @with_error_handling(fallback="default", log_errors=True)
        def failing_func() -> Never:
            raise ValueError("test error")

        with pytest.raises(ValueError):
            failing_func()

        mock_logger.return_value.error.assert_called_once()
        assert "Error in failing_func" in mock_logger.return_value.error.call_args[0][0]

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_disabled(self, mock_logger) -> None:
        """Test that errors are not logged when log_errors=False."""

        @with_error_handling(fallback="default", log_errors=False)
        def failing_func() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            failing_func()

        mock_logger.return_value.error.assert_not_called()

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_suppress_logging(self, mock_logger) -> None:
        """Test that suppressed errors are logged at info level."""

        @with_error_handling(fallback="default", suppress=(KeyError,), log_errors=True)
        def func() -> Never:
            raise KeyError("suppressed")

        result = func()

        assert result == "default"
        mock_logger.return_value.info.assert_called_once()
        assert "Suppressed KeyError" in mock_logger.return_value.info.call_args[0][0]

    def test_context_provider(self) -> None:
        """Test using context provider."""
        context_provider = MagicMock(return_value={"request_id": "123"})

        @with_error_handling(
            fallback="default", log_errors=True, context_provider=context_provider
        )
        def func() -> Never:
            raise ValueError("test")

        with patch("provide.foundation.errors.decorators._get_logger") as mock_logger:
            with pytest.raises(ValueError):
                func()

            context_provider.assert_called_once()
            call_args = mock_logger.return_value.error.call_args[1]
            assert call_args["request_id"] == "123"

    def test_error_mapper(self) -> None:
        """Test error mapping."""

        def mapper(e):
            if isinstance(e, ValueError):
                return FoundationError(f"Mapped: {e}")
            return e

        @with_error_handling(error_mapper=mapper)
        def func() -> Never:
            raise ValueError("original")

        with pytest.raises(FoundationError) as exc_info:
            func()

        assert "Mapped: original" in str(exc_info.value)

    def test_foundation_error_not_wrapped(self) -> None:
        """Test that FoundationErrors are not wrapped."""

        @with_error_handling(error_mapper=lambda e: ValueError("mapped"))
        def func() -> Never:
            raise FoundationError("foundation error")

        with pytest.raises(FoundationError) as exc_info:
            func()

        # Should not be mapped
        assert str(exc_info.value) == "foundation error"


class TestRetryOnError:
    """Test retry_on_error decorator."""

    def test_successful_on_first_try(self) -> None:
        """Test function that succeeds on first try."""
        attempt_count = 0

        @retry_on_error(max_attempts=3)
        def func() -> str:
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = func()

        assert result == "success"
        assert attempt_count == 1

    def test_retry_on_failure(self) -> None:
        """Test that function retries on failure."""
        attempt_count = 0

        @retry_on_error(max_attempts=3, delay=0.01)
        def func() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("fail")
            return "success"

        result = func()

        assert result == "success"
        assert attempt_count == 3

    def test_max_attempts_exceeded(self) -> None:
        """Test that error is raised after max attempts."""
        attempt_count = 0

        @retry_on_error(max_attempts=3, delay=0.01)
        def func() -> Never:
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        with pytest.raises(ValueError) as exc_info:
            func()

        assert "attempt 3" in str(exc_info.value)
        assert attempt_count == 3

    def test_specific_exception_types(self) -> None:
        """Test retrying only specific exception types."""

        @retry_on_error(NetworkError, max_attempts=3, delay=0.01)
        def func(error_type) -> Never:
            if error_type == "network":
                raise NetworkError("network error")
            else:
                raise ValueError("value error")

        # Should not retry ValueError
        with pytest.raises(ValueError):
            func("value")

        # Should retry NetworkError (but still fail)
        with pytest.raises(NetworkError):
            func("network")

    def test_with_retry_policy(self) -> None:
        """Test using RetryPolicy object."""
        policy = RetryPolicy(
            max_attempts=2, base_delay=0.01, backoff=BackoffStrategy.FIXED
        )

        attempt_count = 0

        @retry_on_error(policy=policy)
        def func() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("fail")
            return "success"

        result = func()

        assert result == "success"
        assert attempt_count == 2

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_retry_logging(self, mock_logger) -> None:
        """Test that retries are logged."""

        @retry_on_error(max_attempts=2, delay=0.01)
        def func() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func()

        # Should log warning for retry and error for final failure
        assert mock_logger.return_value.warning.call_count == 1
        assert mock_logger.return_value.error.call_count == 1

        warning_call = mock_logger.return_value.warning.call_args[0][0]
        assert "Retry 1/2" in warning_call

    def test_on_retry_callback(self) -> None:
        """Test on_retry callback."""
        callback = MagicMock()

        @retry_on_error(max_attempts=2, delay=0.01, on_retry=callback)
        def func() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func()

        callback.assert_called_once_with(1, ANY)

    def test_on_retry_callback_exception(self) -> None:
        """Test that exceptions in on_retry don't break retry."""

        def bad_callback(attempt, error) -> Never:
            raise RuntimeError("callback failed")

        attempt_count = 0

        @retry_on_error(max_attempts=3, delay=0.01, on_retry=bad_callback)
        def func() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("test")
            return "success"

        with patch("provide.foundation.errors.decorators._get_logger") as mock_logger:
            result = func()

        assert result == "success"
        assert attempt_count == 3
        # Should log callback failures
        assert any(
            "Retry callback failed" in str(call)
            for call in mock_logger.return_value.warning.call_args_list
        )

    @patch("time.sleep")
    def test_delay_between_retries(self, mock_sleep) -> None:
        """Test that delay is applied between retries."""

        @retry_on_error(max_attempts=3, delay=1.0)
        def func() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func()

        # Should sleep twice (between attempts 1-2 and 2-3)
        assert mock_sleep.call_count == 2

    def test_backoff_parameter(self) -> None:
        """Test backoff multiplier."""

        @retry_on_error(max_attempts=2, delay=0.01, backoff=2.0)
        def func() -> Never:
            raise ValueError("test")

        with patch("time.sleep") as mock_sleep:
            with pytest.raises(ValueError):
                func()

            # With backoff=2, delay should be calculated
            mock_sleep.assert_called()


class TestSuppressAndLog:
    """Test suppress_and_log decorator."""

    def test_suppress_specified_errors(self) -> None:
        """Test that specified errors are suppressed."""

        @suppress_and_log(KeyError, ValueError, fallback="default")
        def func(error_type) -> str:
            if error_type == "key":
                raise KeyError("key")
            elif error_type == "value":
                raise ValueError("value")
            return "success"

        assert func("key") == "default"
        assert func("value") == "default"
        assert func("none") == "success"

    def test_other_errors_not_suppressed(self) -> None:
        """Test that unspecified errors are not suppressed."""

        @suppress_and_log(KeyError, fallback="default")
        def func() -> Never:
            raise ValueError("not suppressed")

        with pytest.raises(ValueError):
            func()

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_at_warning_level(self, mock_logger) -> None:
        """Test that suppressed errors are logged at warning level."""

        @suppress_and_log(ValueError, fallback="default", log_level="warning")
        def func() -> Never:
            raise ValueError("test error")

        result = func()

        assert result == "default"
        mock_logger.return_value.warning.assert_called_once()
        assert "Suppressed ValueError" in mock_logger.return_value.warning.call_args[0][0]

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_at_custom_level(self, mock_logger) -> None:
        """Test logging at custom level."""

        @suppress_and_log(ValueError, fallback="default", log_level="error")
        def func() -> Never:
            raise ValueError("test")

        func()

        mock_logger.return_value.error.assert_called_once()

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_invalid_log_level_falls_back(self, mock_logger) -> None:
        """Test that invalid log level falls back to warning."""

        @suppress_and_log(ValueError, fallback="default", log_level="invalid")
        def func() -> Never:
            raise ValueError("test")

        func()

        # Should fall back to warning
        mock_logger.return_value.warning.assert_called_once()


class TestFallbackOnError:
    """Test fallback_on_error decorator."""

    def test_fallback_called_on_error(self) -> None:
        """Test that fallback function is called on error."""

        def fallback_func() -> str:
            return "fallback result"

        @fallback_on_error(fallback_func)
        def func() -> Never:
            raise ValueError("error")

        result = func()

        assert result == "fallback result"

    def test_fallback_with_same_arguments(self) -> None:
        """Test that fallback receives same arguments."""

        def fallback_func(a, b, c=None) -> str:
            return f"fallback: {a}, {b}, {c}"

        @fallback_on_error(fallback_func)
        def func(a, b, c=None) -> Never:
            raise ValueError("error")

        result = func(1, 2, c=3)

        assert result == "fallback: 1, 2, 3"

    def test_specific_exception_types(self) -> None:
        """Test fallback for specific exception types."""

        def fallback_func(error_type) -> str:
            return "fallback"

        @fallback_on_error(fallback_func, NetworkError)
        def func(error_type) -> Never:
            if error_type == "network":
                raise NetworkError("network")
            else:
                raise ValueError("value")

        assert func("network") == "fallback"

        with pytest.raises(ValueError):
            func("value")

    def test_successful_function_not_fallback(self) -> None:
        """Test that successful functions don't use fallback."""
        fallback_func = MagicMock(return_value="fallback")

        @fallback_on_error(fallback_func)
        def func() -> str:
            return "success"

        result = func()

        assert result == "success"
        fallback_func.assert_not_called()

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_enabled(self, mock_logger) -> None:
        """Test that fallback usage is logged."""

        def fallback_func() -> str:
            return "fallback"

        @fallback_on_error(fallback_func, log_errors=True)
        def func() -> Never:
            raise ValueError("test")

        func()

        mock_logger.return_value.warning.assert_called_once()
        assert "Using fallback" in mock_logger.return_value.warning.call_args[0][0]

    def test_fallback_error_propagates(self) -> None:
        """Test that errors in fallback function propagate."""

        def bad_fallback() -> Never:
            raise RuntimeError("fallback failed")

        @fallback_on_error(bad_fallback)
        def func() -> Never:
            raise ValueError("original")

        with pytest.raises(RuntimeError) as exc_info:
            func()

        assert str(exc_info.value) == "fallback failed"
        assert str(exc_info.value.__cause__) == "original"

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_fallback_error_logged(self, mock_logger) -> None:
        """Test that fallback errors are logged."""

        def bad_fallback() -> Never:
            raise RuntimeError("fallback failed")

        @fallback_on_error(bad_fallback, log_errors=True)
        def func() -> Never:
            raise ValueError("original")

        with pytest.raises(RuntimeError):
            func()

        # Should log both the fallback attempt and failure
        assert mock_logger.return_value.warning.call_count == 1
        assert mock_logger.return_value.error.call_count == 1


class TestCircuitBreaker:
    """Test CircuitBreaker class and decorator."""

    def test_circuit_breaker_creation(self) -> None:
        """Test creating CircuitBreaker."""
        breaker = CircuitBreaker(
            failure_threshold=3, recovery_timeout=10.0, expected_exception=(ValueError,)
        )

        assert breaker.failure_threshold == 3
        assert breaker.recovery_timeout == 10.0
        assert breaker.expected_exception == (ValueError,)

    def test_circuit_closes_on_success(self) -> None:
        """Test that circuit stays closed on success."""
        breaker = CircuitBreaker(failure_threshold=2)

        @breaker
        def func() -> str:
            return "success"

        # Multiple successful calls
        for _ in range(5):
            assert func() == "success"

        assert breaker._state == "closed"

    def test_circuit_opens_after_threshold(self) -> None:
        """Test that circuit opens after failure threshold."""
        breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=10.0)
        attempt_count = 0

        @breaker
        def func() -> Never:
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        # First failure
        with pytest.raises(ValueError):
            func()

        # Second failure - should open circuit
        with pytest.raises(ValueError):
            func()

        assert breaker._state == "open"

        # Next call should fail immediately
        with pytest.raises(RuntimeError) as exc_info:
            func()

        assert "Circuit breaker is open" in str(exc_info.value)

    def test_circuit_half_open_after_timeout(self) -> None:
        """Test that circuit goes to half-open after timeout."""
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.01)

        @breaker
        def func(should_fail) -> str:
            if should_fail:
                raise ValueError("fail")
            return "success"

        # Open the circuit
        with pytest.raises(ValueError):
            func(True)

        assert breaker._state == "open"

        # Wait for recovery timeout
        time.sleep(0.02)

        # Should try half-open
        result = func(False)

        assert result == "success"
        assert breaker._state == "closed"

    def test_circuit_reopens_on_half_open_failure(self) -> None:
        """Test that circuit reopens if half-open attempt fails."""
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.01)

        @breaker
        def func() -> Never:
            raise ValueError("always fails")

        # Open the circuit
        with pytest.raises(ValueError):
            func()

        # Wait for recovery timeout
        time.sleep(0.02)

        # Half-open attempt fails
        with pytest.raises(ValueError):
            func()

        # Should be open again
        assert breaker._state == "open"

    def test_failure_count_decreases_on_success(self) -> None:
        """Test that failure count decreases on success."""
        breaker = CircuitBreaker(failure_threshold=3)

        @breaker
        def func(should_fail) -> str:
            if should_fail:
                raise ValueError("fail")
            return "success"

        # Two failures
        for _ in range(2):
            with pytest.raises(ValueError):
                func(True)

        assert breaker._failure_count == 2

        # Success should reduce count
        func(False)
        assert breaker._failure_count == 1

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_circuit_open_logged(self, mock_logger) -> None:
        """Test that circuit opening is logged."""
        breaker = CircuitBreaker(failure_threshold=1)

        @breaker
        def func() -> Never:
            raise ValueError("fail")

        with pytest.raises(ValueError):
            func()

        mock_logger.return_value.error.assert_called()
        assert "Circuit breaker for func opened" in mock_logger.return_value.error.call_args[0][0]

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_recovery_logged(self, mock_logger) -> None:
        """Test that recovery is logged."""
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.01)

        @breaker
        def func(should_fail) -> str:
            if should_fail:
                raise ValueError("fail")
            return "success"

        # Open circuit
        with pytest.raises(ValueError):
            func(True)

        # Wait and recover
        time.sleep(0.02)
        func(False)

        # Check for recovery log
        info_calls = [call[0][0] for call in mock_logger.return_value.info.call_args_list]
        assert any("closed after successful recovery" in call for call in info_calls)

    def test_circuit_breaker_decorator(self) -> None:
        """Test circuit_breaker as a decorator function."""

        @circuit_breaker(failure_threshold=2, recovery_timeout=10.0)
        def func() -> Never:
            raise ValueError("fail")

        # Should work like CircuitBreaker class
        with pytest.raises(ValueError):
            func()

        with pytest.raises(ValueError):
            func()

        # Circuit should be open
        with pytest.raises(RuntimeError) as exc_info:
            func()

        assert "Circuit breaker is open" in str(exc_info.value)
