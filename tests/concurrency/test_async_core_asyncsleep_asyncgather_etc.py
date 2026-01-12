#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation concurrency utilities."""

import asyncio
import time
from typing import Never

from provide.testkit import MinimalTestCase
from provide.testkit.mocking import AsyncMock, patch
import pytest

from provide.foundation.concurrency import (
    async_gather,
    async_run,
    async_sleep,
    async_wait_for,
)
from provide.foundation.errors import ValidationError


class TestAsyncSleep(MinimalTestCase):
    """Test async_sleep function."""

    @pytest.mark.asyncio
    async def test_async_sleep_actually_sleeps(self) -> None:
        """Test async_sleep actually sleeps for the specified duration."""
        start = time.time()
        await async_sleep(0.1)
        end = time.time()

        # Allow some tolerance for timing
        elapsed = end - start
        assert 0.05 <= elapsed <= 0.2

    @pytest.mark.asyncio
    async def test_async_sleep_zero(self) -> None:
        """Test async_sleep with zero duration."""
        start = time.time()
        await async_sleep(0.0)
        end = time.time()

        # Should return immediately, with a small tolerance for the event loop.
        elapsed = end - start
        assert elapsed < 0.05

    @pytest.mark.asyncio
    async def test_async_sleep_negative_raises_error(self) -> None:
        """Test async_sleep raises error for negative duration."""
        with pytest.raises(ValidationError, match="Sleep delay must be non-negative"):
            await async_sleep(-1.0)

    @pytest.mark.asyncio
    @patch("provide.foundation.concurrency.core.asyncio")
    async def test_async_sleep_uses_asyncio_module(self, mock_asyncio) -> None:
        """Test async_sleep calls asyncio.sleep()."""
        mock_asyncio.sleep = AsyncMock()
        await async_sleep(0.5)
        mock_asyncio.sleep.assert_called_once_with(0.5)

    @pytest.mark.asyncio
    async def test_async_sleep_with_float_seconds(self) -> None:
        """Test async_sleep works with float values."""
        start = time.time()
        await async_sleep(0.05)
        end = time.time()

        elapsed = end - start
        assert 0.04 <= elapsed <= 0.1

    @pytest.mark.asyncio
    async def test_async_sleep_cancellation(self) -> None:
        """Test async_sleep can be cancelled."""

        async def cancel_sleep() -> str:
            task = asyncio.create_task(async_sleep(1.0))
            await asyncio.sleep(0.01)  # Let it start
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                return "cancelled"
            return "not cancelled"

        result = await cancel_sleep()
        assert result == "cancelled"


class TestAsyncGather(MinimalTestCase):
    """Test async_gather function."""

    @pytest.mark.asyncio
    async def test_async_gather_basic_multiple_tasks(self) -> None:
        """Test async_gather with multiple async tasks."""

        async def multiply(n, factor):
            await async_sleep(0.01)
            return n * factor

        results = await async_gather(multiply(2, 3), multiply(4, 5), multiply(6, 7))

        assert results == [6, 20, 42]

    @pytest.mark.asyncio
    async def test_async_gather_preserves_order(self) -> None:
        """Test async_gather preserves order of results."""

        async def delayed_return(value, delay):
            await async_sleep(delay)
            return value

        # Longer delays first - should still return in original order
        results = await async_gather(
            delayed_return("first", 0.1),
            delayed_return("second", 0.05),
            delayed_return("third", 0.01),
        )

        assert results == ["first", "second", "third"]

    @pytest.mark.asyncio
    async def test_async_gather_single_task(self) -> None:
        """Test async_gather with single task."""

        async def single_task() -> str:
            await async_sleep(0.01)
            return "done"

        results = await async_gather(single_task())
        assert results == ["done"]

    @pytest.mark.asyncio
    async def test_async_gather_no_tasks_raises_error(self) -> None:
        """Test async_gather raises error when no awaitables provided."""
        with pytest.raises(
            ValidationError,
            match="At least one awaitable must be provided",
        ):
            await async_gather()

    @pytest.mark.asyncio
    async def test_async_gather_with_exception_default(self) -> None:
        """Test async_gather propagates exceptions by default."""

        async def success_task() -> str:
            return "success"

        async def failing_task() -> Never:
            raise RuntimeError("Test error")

        with pytest.raises(RuntimeError, match="Test error"):
            await async_gather(success_task(), failing_task())

    @pytest.mark.asyncio
    async def test_async_gather_with_return_exceptions_true(self) -> None:
        """Test async_gather returns exceptions when return_exceptions=True."""

        async def success_task() -> str:
            return "success"

        async def failing_task() -> Never:
            raise RuntimeError("Test error")

        results = await async_gather(
            success_task(),
            failing_task(),
            return_exceptions=True,
        )

        assert len(results) == 2
        assert results[0] == "success"
        assert isinstance(results[1], RuntimeError)
        assert str(results[1]) == "Test error"

    @pytest.mark.asyncio
    async def test_async_gather_different_return_types(self) -> None:
        """Test async_gather with different return types."""

        async def return_int() -> int:
            return 42

        async def return_str() -> str:
            return "hello"

        async def return_list():
            return [1, 2, 3]

        async def return_dict():
            return {"key": "value"}

        results = await async_gather(
            return_int(),
            return_str(),
            return_list(),
            return_dict(),
        )

        assert results == [42, "hello", [1, 2, 3], {"key": "value"}]

    @pytest.mark.asyncio
    @patch("provide.foundation.concurrency.core.asyncio")
    async def test_async_gather_uses_asyncio_module(self, mock_asyncio) -> None:
        """Test async_gather calls asyncio.gather()."""
        mock_coro1 = AsyncMock(return_value="result1")
        mock_coro2 = AsyncMock(return_value="result2")
        mock_asyncio.gather = AsyncMock(return_value=["result1", "result2"])

        await async_gather(mock_coro1(), mock_coro2(), return_exceptions=True)

        mock_asyncio.gather.assert_called_once()
        args, kwargs = mock_asyncio.gather.call_args
        assert len(args) == 2
        assert kwargs["return_exceptions"] is True


class TestAsyncWaitFor(MinimalTestCase):
    """Test async_wait_for function."""

    @pytest.mark.asyncio
    async def test_async_wait_for_completes_within_timeout(self) -> None:
        """Test async_wait_for completes when task finishes within timeout."""

        async def quick_task() -> str:
            await async_sleep(0.01)
            return "completed"

        result = await async_wait_for(quick_task(), timeout=0.1)
        assert result == "completed"

    @pytest.mark.asyncio
    async def test_async_wait_for_raises_timeout_error(self) -> None:
        """Test async_wait_for raises TimeoutError when timeout exceeded."""

        async def slow_task() -> str:
            await async_sleep(0.2)
            return "too slow"

        with pytest.raises(asyncio.TimeoutError):
            await async_wait_for(slow_task(), timeout=0.05)

    @pytest.mark.asyncio
    async def test_async_wait_for_no_timeout(self) -> None:
        """Test async_wait_for works with no timeout."""

        async def task() -> str:
            await async_sleep(0.01)
            return "no timeout"

        result = await async_wait_for(task(), timeout=None)
        assert result == "no timeout"

    @pytest.mark.asyncio
    async def test_async_wait_for_negative_timeout_raises_error(self) -> None:
        """Test async_wait_for raises error for negative timeout."""

        async def task() -> str:
            return "test"

        # Create coroutine but properly handle it to avoid warning
        coro = task()
        try:
            with pytest.raises(ValidationError, match="Timeout must be non-negative"):
                await async_wait_for(coro, timeout=-1.0)
        finally:
            # Close coroutine if it wasn't consumed
            if coro.cr_frame is not None:
                coro.close()

    @pytest.mark.asyncio
    async def test_async_wait_for_zero_timeout(self) -> None:
        """Test async_wait_for with zero timeout raises TimeoutError."""

        async def instant_task() -> str:
            return "instant"

        # Zero timeout should raise TimeoutError even for immediate tasks
        # Create coroutine and properly handle it to avoid warning
        coro = instant_task()
        try:
            with pytest.raises(asyncio.TimeoutError):
                await async_wait_for(coro, timeout=0.0)
        finally:
            # Close coroutine if it wasn't consumed
            if coro.cr_frame is not None:
                coro.close()

    @pytest.mark.asyncio
    @patch("provide.foundation.concurrency.core.asyncio")
    async def test_async_wait_for_uses_asyncio_module(self, mock_asyncio) -> None:
        """Test async_wait_for calls asyncio.wait_for()."""
        mock_coro = AsyncMock(return_value="result")
        mock_asyncio.wait_for = AsyncMock(return_value="result")

        await async_wait_for(mock_coro(), timeout=1.0)

        mock_asyncio.wait_for.assert_called_once()
        args, kwargs = mock_asyncio.wait_for.call_args
        # Check that it was called with awaitable and timeout
        assert len(args) >= 1  # At least the awaitable
        assert kwargs.get("timeout") == 1.0 or (len(args) >= 2 and args[1] == 1.0)

    @pytest.mark.asyncio
    async def test_async_wait_for_propagates_exceptions(self) -> None:
        """Test async_wait_for propagates exceptions from awaitable."""

        async def failing_task() -> Never:
            raise ValueError("Task failed")

        with pytest.raises(ValueError, match="Task failed"):
            await async_wait_for(failing_task(), timeout=1.0)


class TestAsyncRun(MinimalTestCase):
    """Test async_run function."""

    def test_async_run_basic_async_function(self) -> None:
        """Test async_run executes basic async function."""

        async def main() -> str:
            await async_sleep(0.01)
            return "hello world"

        result = async_run(main)
        assert result == "hello world"

    def test_async_run_with_return_value(self) -> None:
        """Test async_run returns value from async function."""

        async def compute() -> int:
            return 2 + 2

        result = async_run(compute)
        assert result == 4

    def test_async_run_with_complex_return_value(self) -> None:
        """Test async_run handles complex return values."""

        async def complex_data():
            return {
                "numbers": [1, 2, 3],
                "nested": {"key": "value"},
                "result": await async_gather(
                    async_sleep(0.01),
                    async_sleep(0.01),
                ),
            }

        result = async_run(complex_data)
        assert result["numbers"] == [1, 2, 3]
        assert result["nested"]["key"] == "value"
        assert result["result"] == [None, None]  # sleep returns None

    def test_async_run_non_callable_raises_error(self) -> None:
        """Test async_run raises error for non-callable input."""
        with pytest.raises(ValidationError, match="Main must be callable"):
            async_run("not callable")

        with pytest.raises(ValidationError, match="Main must be callable"):
            async_run(123)

        with pytest.raises(ValidationError, match="Main must be callable"):
            async_run(None)

    def test_async_run_propagates_exceptions(self) -> None:
        """Test async_run propagates exceptions from async function."""

        async def failing_main() -> Never:
            raise RuntimeError("Main failed")

        with pytest.raises(RuntimeError, match="Main failed"):
            async_run(failing_main)

    @patch("provide.foundation.concurrency.core.asyncio")
    def test_async_run_uses_asyncio_module(self, mock_asyncio) -> None:
        """Test async_run calls asyncio.run()."""

        async def main() -> str:
            return "test"

        # Set up mock to properly handle the coroutine
        def mock_run(coro, **kwargs) -> str:
            # Close the coroutine to avoid warnings
            if hasattr(coro, "close"):
                coro.close()
            return "test"

        mock_asyncio.run.side_effect = mock_run

        result = async_run(main, debug=True)

        assert result == "test"
        mock_asyncio.run.assert_called_once()
        args, kwargs = mock_asyncio.run.call_args
        # Should be called with a coroutine object (main() returns a coroutine)
        import inspect

        assert inspect.iscoroutine(args[0])
        assert kwargs["debug"] is True

    def test_async_run_with_debug_false(self) -> None:
        """Test async_run with debug=False."""

        async def main() -> str:
            return "debug false"

        result = async_run(main, debug=False)
        assert result == "debug false"

    def test_async_run_with_async_generator(self) -> None:
        """Test async_run doesn't work with async generators (by design)."""

        async def async_gen():
            yield 1
            yield 2

        # This should raise an error because async_gen() returns an async generator,
        # not a coroutine that async_run expects
        with pytest.raises((TypeError, RuntimeError, ValueError)):
            async_run(async_gen)


# 🧱🏗️🔚
