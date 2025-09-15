"""Tests for @retry decorator.
"""

import asyncio
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest

from provide.foundation.resilience.decorators import retry
from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy


class TestRetryDecoratorSync:
    """Test @retry decorator with synchronous functions."""

    def test_successful_function(self):
        """Test decorated function that succeeds."""

        @retry(max_attempts=3)
        def successful_func():
            return "success"

        result = successful_func()
        assert result == "success"

    def test_retry_on_failure(self):
        """Test that decorated function retries on failure."""
        attempt_count = 0

        @retry(max_attempts=3, base_delay=0.01)
        def failing_func():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError(f"attempt {attempt_count}")
            return "success"

        result = failing_func()

        assert result == "success"
        assert attempt_count == 3

    def test_max_attempts_exceeded(self):
        """Test that error is raised after max attempts."""
        attempt_count = 0

        @retry(max_attempts=2, base_delay=0.01)
        def always_fails():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        with pytest.raises(ValueError) as exc_info:
            always_fails()

        assert "attempt 2" in str(exc_info.value)
        assert attempt_count == 2

    def test_specific_exception_types(self):
        """Test retrying only specific exception types."""

        @retry(ValueError, TypeError, max_attempts=3, base_delay=0.01)
        def selective_retry(error_type):
            if error_type == "value":
                raise ValueError("value error")
            if error_type == "type":
                raise TypeError("type error")
            raise RuntimeError("runtime error")

        # Should retry ValueError
        with pytest.raises(ValueError):
            selective_retry("value")

        # Should retry TypeError
        with pytest.raises(TypeError):
            selective_retry("type")

        # Should NOT retry RuntimeError (fails immediately)
        with pytest.raises(RuntimeError):
            selective_retry("runtime")

    def test_with_retry_policy(self):
        """Test decorator with RetryPolicy object."""
        policy = RetryPolicy(
            max_attempts=2,
            base_delay=0.01,
            backoff=BackoffStrategy.FIXED,
        )

        attempt_count = 0

        @retry(policy=policy)
        def func_with_policy():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count == 1:
                raise ValueError("first")
            return "success"

        result = func_with_policy()

        assert result == "success"
        assert attempt_count == 2

    def test_function_with_arguments(self):
        """Test decorated function with arguments."""

        @retry(max_attempts=2, base_delay=0.01)
        def func_with_args(a, b, c=None):
            if not hasattr(func_with_args, "called"):
                func_with_args.called = True
                raise ValueError("first")
            return f"{a}-{b}-{c}"

        result = func_with_args("x", "y", c="z")
        assert result == "x-y-z"

    def test_on_retry_callback(self):
        """Test on_retry callback with decorator."""
        callback = MagicMock()

        @retry(max_attempts=2, base_delay=0.01, on_retry=callback)
        def func_with_callback():
            if not hasattr(func_with_callback, "called"):
                func_with_callback.called = True
                raise ValueError("fail")
            return "success"

        result = func_with_callback()

        assert result == "success"
        callback.assert_called_once_with(1, ANY)

    def test_preserve_function_metadata(self):
        """Test that decorator preserves function metadata."""

        @retry(max_attempts=3)
        def documented_func():
            """This is a documented function."""
            return "result"

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a documented function."

    @patch("time.sleep")
    def test_delay_between_retries(self, mock_sleep):
        """Test delay between retry attempts."""

        @retry(max_attempts=3, base_delay=1.0, jitter=False)
        def failing_func():
            raise ValueError("fail")

        with pytest.raises(ValueError):
            failing_func()

        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)

    def test_mixed_decorator_parameters(self):
        """Test decorator with mixed positional and keyword arguments."""

        # Exceptions as positional, rest as kwargs
        @retry(ValueError, TypeError, max_attempts=2, base_delay=0.01)
        def func1():
            raise ValueError("test")

        with pytest.raises(ValueError):
            func1()

        # Policy as keyword
        @retry(policy=RetryPolicy(max_attempts=1))
        def func2():
            raise ValueError("test")

        with pytest.raises(ValueError):
            func2()

        # Just kwargs
        @retry(max_attempts=1, base_delay=0.01)
        def func3():
            raise ValueError("test")

        with pytest.raises(ValueError):
            func3()


class TestRetryDecoratorAsync:
    """Test @retry decorator with asynchronous functions."""

    @pytest.mark.asyncio
    async def test_successful_async_function(self):
        """Test decorated async function that succeeds."""

        @retry(max_attempts=3)
        async def successful_async():
            return "success"

        result = await successful_async()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_retry_on_async_failure(self):
        """Test that decorated async function retries on failure."""
        attempt_count = 0

        @retry(max_attempts=3, base_delay=0.01)
        async def failing_async():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError(f"attempt {attempt_count}")
            return "success"

        result = await failing_async()

        assert result == "success"
        assert attempt_count == 3

    @pytest.mark.asyncio
    async def test_async_max_attempts_exceeded(self):
        """Test that error is raised after max attempts in async."""
        attempt_count = 0

        @retry(max_attempts=2, base_delay=0.01)
        async def always_fails_async():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        with pytest.raises(ValueError) as exc_info:
            await always_fails_async()

        assert "attempt 2" in str(exc_info.value)
        assert attempt_count == 2

    @pytest.mark.asyncio
    async def test_async_with_arguments(self):
        """Test decorated async function with arguments."""

        @retry(max_attempts=2, base_delay=0.01)
        async def async_with_args(a, b, *, c=None):
            await asyncio.sleep(0)  # Ensure it's async
            if not hasattr(async_with_args, "called"):
                async_with_args.called = True
                raise ValueError("first")
            return f"{a}-{b}-{c}"

        result = await async_with_args("x", "y", c="z")
        assert result == "x-y-z"

    @pytest.mark.asyncio
    async def test_async_on_retry_callback(self):
        """Test async on_retry callback."""
        callback = AsyncMock()

        @retry(max_attempts=2, base_delay=0.01, on_retry=callback)
        async def async_with_callback():
            if not hasattr(async_with_callback, "called"):
                async_with_callback.called = True
                raise ValueError("fail")
            return "success"

        result = await async_with_callback()

        assert result == "success"
        callback.assert_called_once()

    @pytest.mark.asyncio
    async def test_sync_callback_with_async_function(self):
        """Test sync callback with async decorated function."""
        callback = MagicMock()  # Sync callback

        @retry(max_attempts=2, base_delay=0.01, on_retry=callback)
        async def async_func():
            if not hasattr(async_func, "called"):
                async_func.called = True
                raise ValueError("fail")
            return "success"

        result = await async_func()

        assert result == "success"
        callback.assert_called_once()

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_async_delay_between_retries(self, mock_sleep):
        """Test delay between async retry attempts."""
        mock_sleep.return_value = None

        @retry(max_attempts=3, base_delay=1.0, jitter=False)
        async def failing_async():
            raise ValueError("fail")

        with pytest.raises(ValueError):
            await failing_async()

        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)

    @pytest.mark.asyncio
    async def test_preserve_async_function_metadata(self):
        """Test that decorator preserves async function metadata."""

        @retry(max_attempts=3)
        async def documented_async():
            """This is a documented async function."""
            return "result"

        assert documented_async.__name__ == "documented_async"
        assert documented_async.__doc__ == "This is a documented async function."
        assert asyncio.iscoroutinefunction(documented_async)


class TestRetryDecoratorParameterValidation:
    """Test parameter validation for @retry decorator."""

    def test_conflicting_parameters(self):
        """Test that conflicting parameters raise errors."""
        # Can't specify both policy and individual params
        with pytest.raises(ValueError) as exc_info:
            @retry(policy=RetryPolicy(), max_attempts=5)
            def func():
                pass

        assert "both policy and" in str(exc_info.value).lower()

    def test_invalid_max_attempts(self):
        """Test invalid max_attempts parameter."""
        with pytest.raises(ValueError):
            @retry(max_attempts=0)
            def func():
                pass

        with pytest.raises(ValueError):
            @retry(max_attempts=-1)
            def func():
                pass

    def test_invalid_delay(self):
        """Test invalid delay parameters."""
        with pytest.raises(ValueError):
            @retry(base_delay=-1.0)
            def func():
                pass

    def test_no_parentheses_decorator(self):
        """Test decorator used without parentheses."""

        # This should work
        @retry
        def func():
            if not hasattr(func, "called"):
                func.called = True
                raise ValueError("first")
            return "success"

        result = func()
        assert result == "success"

    def test_positional_exceptions_only(self):
        """Test decorator with only exception types as positional args."""

        @retry(ValueError, TypeError)
        def func(error_type):
            if error_type == "value":
                raise ValueError("test")
            if error_type == "type":
                raise TypeError("test")
            raise RuntimeError("test")

        # Should retry these
        with pytest.raises(ValueError):
            func("value")

        with pytest.raises(TypeError):
            func("type")

        # Should not retry this
        with pytest.raises(RuntimeError):
            func("runtime")


class TestRetryDecoratorLogging:
    """Test logging behavior of @retry decorator."""

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_retry_logging(self, mock_get_logger):
        """Test that retries are logged."""
        mock_logger = mock_get_logger.return_value

        @retry(max_attempts=2, base_delay=0.01)
        def func():
            if not hasattr(func, "called"):
                func.called = True
                raise ValueError("test")
            return "success"

        result = func()

        assert result == "success"
        # Should log the retry
        mock_logger.info.assert_called()

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_failure_logging(self, mock_get_logger):
        """Test that final failure is logged."""
        mock_logger = mock_get_logger.return_value

        @retry(max_attempts=2, base_delay=0.01)
        def always_fails():
            raise ValueError("test")

        with pytest.raises(ValueError):
            always_fails()

        # Should log the final failure
        assert mock_logger.error.called
