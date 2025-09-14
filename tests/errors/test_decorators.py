"""Tests for provide.foundation.errors.decorators module."""

from typing import Never
from unittest.mock import patch

import pytest

from provide.foundation.errors.base import FoundationError
from provide.foundation.errors.decorators import (
    fallback_on_error,
    suppress_and_log,
    with_error_handling,
)


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
            if error_type == "value":
                raise ValueError("value error")
            raise RuntimeError("runtime error")

        # Should suppress KeyError and ValueError
        assert func("key") == "default"
        assert func("value") == "default"

        # Should not suppress RuntimeError
        with pytest.raises(RuntimeError):
            func("runtime")

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_error_logging(self, mock_logger) -> None:
        """Test that errors are logged."""

        @with_error_handling(log_errors=True)
        def failing_func() -> Never:
            raise ValueError("test error")

        with pytest.raises(ValueError):
            failing_func()

        mock_logger.return_value.error.assert_called_once()
        error_message = mock_logger.return_value.error.call_args[0][0]
        assert "failing_func" in error_message
        assert "test error" in error_message

    def test_context_provider(self) -> None:
        """Test context provider for logging."""

        def get_context() -> dict[str, str]:
            return {"request_id": "123", "user_id": "456"}

        @with_error_handling(context_provider=get_context, log_errors=True)
        def failing_func() -> Never:
            raise ValueError("test error")

        with patch("provide.foundation.errors.decorators._get_logger") as mock_logger:
            with pytest.raises(ValueError):
                failing_func()

            mock_logger.return_value.error.assert_called_once()
            kwargs = mock_logger.return_value.error.call_args[1]
            assert kwargs["request_id"] == "123"
            assert kwargs["user_id"] == "456"

    def test_error_mapper(self) -> None:
        """Test error mapping functionality."""

        def map_error(e: Exception) -> Exception:
            if isinstance(e, ValueError):
                return RuntimeError(f"Mapped: {e}")
            return e

        @with_error_handling(error_mapper=map_error)
        def func(error_type: str) -> Never:
            if error_type == "value":
                raise ValueError("value error")
            raise KeyError("key error")

        # ValueError should be mapped to RuntimeError
        with pytest.raises(RuntimeError, match="Mapped: value error"):
            func("value")

        # KeyError should not be mapped
        with pytest.raises(KeyError, match="key error"):
            func("key")

    @pytest.mark.asyncio
    async def test_async_function(self) -> None:
        """Test with async functions."""

        @with_error_handling(fallback="default", suppress=(ValueError,))
        async def async_func(should_fail: bool) -> str:
            if should_fail:
                raise ValueError("async error")
            return "async success"

        # Successful call
        result = await async_func(False)
        assert result == "async success"

        # Suppressed error
        result = await async_func(True)
        assert result == "default"

    def test_foundation_error_not_mapped(self) -> None:
        """Test that FoundationError is not mapped."""

        def map_error(e: Exception) -> Exception:
            return RuntimeError(f"Mapped: {e}")

        @with_error_handling(error_mapper=map_error)
        def func() -> Never:
            raise FoundationError("foundation error")

        # FoundationError should not be mapped
        with pytest.raises(FoundationError) as exc_info:
            func()
        assert str(exc_info.value) == "foundation error"


class TestSuppressAndLog:
    """Test suppress_and_log decorator."""

    def test_suppress_specified_errors(self) -> None:
        """Test that specified errors are suppressed."""

        @suppress_and_log(KeyError, ValueError, fallback="default")
        def func(error_type: str) -> Never:
            if error_type == "key":
                raise KeyError("key error")
            if error_type == "value":
                raise ValueError("value error")
            raise RuntimeError("runtime error")

        # Should suppress KeyError and ValueError
        assert func("key") == "default"
        assert func("value") == "default"

        # Should not suppress RuntimeError
        with pytest.raises(RuntimeError):
            func("runtime")

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_logging_levels(self, mock_logger) -> None:
        """Test different logging levels."""

        @suppress_and_log(ValueError, fallback=None, log_level="debug")
        def debug_func() -> Never:
            raise ValueError("debug error")

        @suppress_and_log(ValueError, fallback=None, log_level="warning")
        def warning_func() -> Never:
            raise ValueError("warning error")

        debug_func()
        warning_func()

        mock_logger.return_value.debug.assert_called_once()
        mock_logger.return_value.warning.assert_called_once()

    def test_fallback_value(self) -> None:
        """Test different fallback values."""

        @suppress_and_log(ValueError, fallback=42)
        def int_fallback() -> Never:
            raise ValueError("error")

        @suppress_and_log(ValueError, fallback={"key": "value"})
        def dict_fallback() -> Never:
            raise ValueError("error")

        assert int_fallback() == 42
        assert dict_fallback() == {"key": "value"}

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_log_message_format(self, mock_logger) -> None:
        """Test log message formatting."""

        @suppress_and_log(ValueError, fallback="fallback")
        def test_func() -> Never:
            raise ValueError("test error")

        result = test_func()
        assert result == "fallback"

        mock_logger.return_value.warning.assert_called_once()
        log_message = mock_logger.return_value.warning.call_args[0][0]
        assert "Suppressed ValueError" in log_message
        assert "test_func" in log_message
        assert "test error" in log_message


class TestFallbackOnError:
    """Test fallback_on_error decorator."""

    def test_successful_function(self) -> None:
        """Test that successful functions work normally."""

        def fallback() -> str:
            return "fallback"

        @fallback_on_error(fallback)
        def successful_func() -> str:
            return "success"

        assert successful_func() == "success"

    def test_fallback_on_error(self) -> None:
        """Test fallback is called on error."""

        def fallback() -> str:
            return "fallback"

        @fallback_on_error(fallback)
        def failing_func() -> Never:
            raise ValueError("error")

        assert failing_func() == "fallback"

    def test_fallback_with_arguments(self) -> None:
        """Test fallback receives same arguments."""

        def fallback(x: int, y: int) -> int:
            return x + y

        @fallback_on_error(fallback)
        def divide(x: int, y: int) -> float:
            return x / y

        # Normal operation
        assert divide(10, 2) == 5.0

        # Fallback on error
        assert divide(10, 0) == 10  # 10 + 0

    def test_specific_exception_types(self) -> None:
        """Test fallback for specific exception types."""

        def fallback(error_type: str) -> str:
            return "fallback"

        @fallback_on_error(fallback, ValueError, KeyError)
        def func(error_type: str) -> Never:
            if error_type == "value":
                raise ValueError("value error")
            if error_type == "key":
                raise KeyError("key error")
            raise RuntimeError("runtime error")

        # Should use fallback for ValueError and KeyError
        assert func("value") == "fallback"
        assert func("key") == "fallback"

        # Should not use fallback for RuntimeError
        with pytest.raises(RuntimeError):
            func("runtime")

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_error_logging(self, mock_logger) -> None:
        """Test that errors are logged before fallback."""

        def fallback() -> str:
            return "fallback"

        @fallback_on_error(fallback, log_errors=True)
        def failing_func() -> Never:
            raise ValueError("test error")

        result = failing_func()
        assert result == "fallback"

        mock_logger.return_value.warning.assert_called_once()
        log_message = mock_logger.return_value.warning.call_args[0][0]
        assert "Using fallback" in log_message
        assert "failing_func" in log_message
        assert "ValueError" in log_message

    def test_fallback_function_error(self) -> None:
        """Test when fallback function also fails."""

        def bad_fallback() -> Never:
            raise RuntimeError("fallback error")

        @fallback_on_error(bad_fallback)
        def failing_func() -> Never:
            raise ValueError("original error")

        # Should raise the fallback error with original as cause
        with pytest.raises(RuntimeError, match="fallback error") as exc_info:
            failing_func()
        assert exc_info.value.__cause__.__class__ == ValueError

    @patch("provide.foundation.errors.decorators._get_logger")
    def test_fallback_error_logging(self, mock_logger) -> None:
        """Test logging when fallback also fails."""

        def bad_fallback() -> Never:
            raise RuntimeError("fallback error")

        @fallback_on_error(bad_fallback, log_errors=True)
        def failing_func() -> Never:
            raise ValueError("original error")

        with pytest.raises(RuntimeError):
            failing_func()

        # Should log both original error and fallback failure
        assert mock_logger.return_value.warning.call_count >= 1
        assert mock_logger.return_value.error.call_count >= 1
