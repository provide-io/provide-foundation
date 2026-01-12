#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for @retry decorator."""

import asyncio
from typing import Any, Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import ANY, AsyncMock, MagicMock, patch
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.resilience.decorators import retry
from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy


class TestRetryDecoratorSync(FoundationTestCase):
    """Test @retry decorator with synchronous functions."""

    def test_successful_function(self) -> None:
        """Test decorated function that succeeds."""

        @retry(max_attempts=3)
        def successful_func() -> str:
            return "success"

        result = successful_func()
        assert result == "success"

    def test_retry_on_failure(self) -> None:
        """Test that decorated function retries on failure using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        attempt_count = 0

        @retry(max_attempts=3, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def failing_func() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError(f"attempt {attempt_count}")
            return "success"

        result = failing_func()

        assert result == "success"
        assert attempt_count == 3

    def test_max_attempts_exceeded(self) -> None:
        """Test that error is raised after max attempts using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        attempt_count = 0

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def always_fails() -> Never:
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        with pytest.raises(ValueError) as exc_info:
            always_fails()

        assert "attempt 2" in str(exc_info.value)
        assert attempt_count == 2

    def test_specific_exception_types(self) -> None:
        """Test retrying only specific exception types using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        @retry(
            ValueError, TypeError, max_attempts=3, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep
        )
        def selective_retry(error_type: str) -> Never:
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

    def test_with_retry_policy(self) -> None:
        """Test decorator with RetryPolicy object."""
        policy = RetryPolicy(
            max_attempts=2,
            base_delay=0.01,
            backoff=BackoffStrategy.FIXED,
        )

        attempt_count = 0

        @retry(policy=policy)
        def func_with_policy() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count == 1:
                raise ValueError("first")
            return "success"

        result = func_with_policy()

        assert result == "success"
        assert attempt_count == 2

    def test_function_with_arguments(self) -> None:
        """Test decorated function with arguments using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def func_with_args(a: str, b: str, c: str | None = None) -> str:
            if not hasattr(func_with_args, "called"):
                func_with_args.called = True
                raise ValueError("first")
            return f"{a}-{b}-{c}"

        result = func_with_args("x", "y", c="z")
        assert result == "x-y-z"

    def test_on_retry_callback(self) -> None:
        """Test on_retry callback with decorator using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        callback = MagicMock()

        @retry(max_attempts=2, base_delay=0.01, on_retry=callback, time_source=get_time, sleep_func=fake_sleep)
        def func_with_callback() -> str:
            if not hasattr(func_with_callback, "called"):
                func_with_callback.called = True
                raise ValueError("fail")
            return "success"

        result = func_with_callback()

        assert result == "success"
        callback.assert_called_once_with(1, ANY)

    def test_preserve_function_metadata(self) -> None:
        """Test that decorator preserves function metadata."""

        @retry(max_attempts=3)
        def documented_func() -> str:
            """This is a documented function."""
            return "result"

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "This is a documented function."

    @pytest.mark.slow
    def test_delay_between_retries(self) -> None:
        """Test delay between retry attempts using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        @retry(max_attempts=3, base_delay=0.1, jitter=False, time_source=get_time, sleep_func=fake_sleep)
        def failing_func() -> Never:
            raise ValueError("fail")

        with pytest.raises(ValueError):
            failing_func()

        # Function should fail after 3 attempts with controlled time

    def test_mixed_decorator_parameters(self) -> None:
        """Test decorator with mixed positional and keyword arguments using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        # Exceptions as positional, rest as kwargs
        @retry(
            ValueError, TypeError, max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep
        )
        def func1() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func1()

        # Policy as keyword
        @retry(policy=RetryPolicy(max_attempts=1))
        def func2() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func2()

        # Just kwargs
        @retry(max_attempts=1, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def func3() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            func3()


class TestRetryDecoratorAsync(FoundationTestCase):
    """Test @retry decorator with asynchronous functions."""

    @pytest.mark.asyncio
    async def test_successful_async_function(self) -> None:
        """Test decorated async function that succeeds."""

        @retry(max_attempts=3)
        async def successful_async() -> str:
            return "success"

        result = await successful_async()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_retry_on_async_failure(self) -> None:
        """Test that decorated async function retries on failure using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()
        attempt_count = 0

        @retry(max_attempts=3, base_delay=0.01, time_source=get_time, async_sleep_func=fake_async_sleep)
        async def failing_async() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError(f"attempt {attempt_count}")
            return "success"

        result = await failing_async()

        assert result == "success"
        assert attempt_count == 3

    @pytest.mark.asyncio
    async def test_async_max_attempts_exceeded(self) -> None:
        """Test that error is raised after max attempts in async using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()
        attempt_count = 0

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, async_sleep_func=fake_async_sleep)
        async def always_fails_async() -> Never:
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError(f"attempt {attempt_count}")

        with pytest.raises(ValueError) as exc_info:
            await always_fails_async()

        assert "attempt 2" in str(exc_info.value)
        assert attempt_count == 2

    @pytest.mark.asyncio
    async def test_async_with_arguments(self) -> None:
        """Test decorated async function with arguments using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, async_sleep_func=fake_async_sleep)
        async def async_with_args(a: str, b: str, *, c: str | None = None) -> str:
            await asyncio.sleep(0)  # Ensure it's async
            if not hasattr(async_with_args, "called"):
                async_with_args.called = True
                raise ValueError("first")
            return f"{a}-{b}-{c}"

        result = await async_with_args("x", "y", c="z")
        assert result == "x-y-z"

    @pytest.mark.asyncio
    async def test_async_on_retry_callback(self) -> None:
        """Test async on_retry callback using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()
        callback = AsyncMock()

        @retry(
            max_attempts=2,
            base_delay=0.01,
            on_retry=callback,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        async def async_with_callback() -> str:
            if not hasattr(async_with_callback, "called"):
                async_with_callback.called = True
                raise ValueError("fail")
            return "success"

        result = await async_with_callback()

        assert result == "success"
        callback.assert_called_once()

    @pytest.mark.asyncio
    async def test_sync_callback_with_async_function(self) -> None:
        """Test sync callback with async decorated function using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()
        callback = MagicMock()  # Sync callback

        @retry(
            max_attempts=2,
            base_delay=0.01,
            on_retry=callback,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        async def async_func() -> str:
            if not hasattr(async_func, "called"):
                async_func.called = True
                raise ValueError("fail")
            return "success"

        result = await async_func()

        assert result == "success"
        callback.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_async_delay_between_retries(self) -> None:
        """Test delay between async retry attempts using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()

        @retry(
            max_attempts=3,
            base_delay=0.1,
            jitter=False,
            time_source=get_time,
            async_sleep_func=fake_async_sleep,
        )
        async def failing_async() -> Never:
            raise ValueError("fail")

        with pytest.raises(ValueError):
            await failing_async()

        # Function should fail after 3 attempts with controlled time

    @pytest.mark.asyncio
    async def test_preserve_async_function_metadata(self) -> None:
        """Test that decorator preserves async function metadata."""

        @retry(max_attempts=3)
        async def documented_async() -> str:
            """This is a documented async function."""
            return "result"

        assert documented_async.__name__ == "documented_async"
        assert documented_async.__doc__ == "This is a documented async function."
        assert asyncio.iscoroutinefunction(documented_async)


class TestRetryDecoratorParameterValidation:
    """Test parameter validation for @retry decorator."""

    def test_conflicting_parameters(self) -> None:
        """Test that conflicting parameters raise errors."""
        from provide.foundation.errors.config import ConfigurationError

        # Can't specify both policy and individual params
        with pytest.raises(ConfigurationError) as exc_info:

            @retry(policy=RetryPolicy(), max_attempts=5)
            def func() -> None:
                pass

        assert "both policy and" in str(exc_info.value).lower()

    def test_invalid_max_attempts(self) -> None:
        """Test invalid max_attempts parameter."""
        with pytest.raises(ValueError):

            @retry(max_attempts=0)
            def func() -> None:
                pass

        with pytest.raises(ValueError):

            @retry(max_attempts=-1)
            def func() -> None:
                pass

    def test_invalid_delay(self) -> None:
        """Test invalid delay parameters."""
        with pytest.raises(ValueError):

            @retry(base_delay=-1.0)
            def func() -> None:
                pass

    def test_no_parentheses_decorator(self) -> None:
        """Test decorator used without parentheses."""

        # This should work
        @retry
        def func() -> str:
            if not hasattr(func, "called"):
                func.called = True
                raise ValueError("first")
            return "success"

        result = func()
        assert result == "success"

    def test_positional_exceptions_only(self) -> None:
        """Test decorator with only exception types as positional args."""

        @retry(ValueError, TypeError)
        def func(error_type: str) -> Never:
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
    def test_retry_logging(self, mock_get_logger: Any) -> None:
        """Test that retries are logged using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        mock_logger = mock_get_logger.return_value

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def func() -> str:
            if not hasattr(func, "called"):
                func.called = True
                raise ValueError("test")
            return "success"

        result = func()

        assert result == "success"
        # Should log the retry
        mock_logger.info.assert_called()

    @patch("provide.foundation.hub.foundation.get_foundation_logger")
    def test_failure_logging(self, mock_get_logger: Any) -> None:
        """Test that final failure is logged using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        mock_logger = mock_get_logger.return_value

        @retry(max_attempts=2, base_delay=0.01, time_source=get_time, sleep_func=fake_sleep)
        def always_fails() -> Never:
            raise ValueError("test")

        with pytest.raises(ValueError):
            always_fails()

        # Should log the final failure
        assert mock_logger.error.called


# 🧱🏗️🔚
