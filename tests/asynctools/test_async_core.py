"""Tests for Foundation async utilities."""

import asyncio
import time
from unittest.mock import AsyncMock, patch

import pytest

from provide.foundation.asynctools import (
    provide_gather,
    provide_run,
    provide_sleep_async,
    provide_wait_for,
)
from provide.foundation.errors import ValidationError


class TestProvideSleepAsync:
    """Test provide_sleep_async function."""

    @pytest.mark.asyncio
    async def test_provide_sleep_async_actually_sleeps(self):
        """Test provide_sleep_async actually sleeps for the specified duration."""
        start = time.time()
        await provide_sleep_async(0.1)
        end = time.time()

        # Allow some tolerance for timing
        elapsed = end - start
        assert 0.05 <= elapsed <= 0.2

    @pytest.mark.asyncio
    async def test_provide_sleep_async_zero(self):
        """Test provide_sleep_async with zero duration."""
        start = time.time()
        await provide_sleep_async(0.0)
        end = time.time()

        # Should return immediately
        elapsed = end - start
        assert elapsed < 0.01

    @pytest.mark.asyncio
    async def test_provide_sleep_async_negative_raises_error(self):
        """Test provide_sleep_async raises error for negative duration."""
        with pytest.raises(ValidationError, match="Sleep delay must be non-negative"):
            await provide_sleep_async(-1.0)

    @pytest.mark.asyncio
    @patch("provide.foundation.asynctools.core.asyncio")
    async def test_provide_sleep_async_uses_asyncio_module(self, mock_asyncio):
        """Test provide_sleep_async calls asyncio.sleep()."""
        mock_asyncio.sleep = AsyncMock()
        await provide_sleep_async(0.5)
        mock_asyncio.sleep.assert_called_once_with(0.5)

    @pytest.mark.asyncio
    async def test_provide_sleep_async_with_float_seconds(self):
        """Test provide_sleep_async works with float values."""
        start = time.time()
        await provide_sleep_async(0.05)
        end = time.time()

        elapsed = end - start
        assert 0.04 <= elapsed <= 0.1

    @pytest.mark.asyncio
    async def test_provide_sleep_async_cancellation(self):
        """Test provide_sleep_async can be cancelled."""

        async def cancel_sleep():
            task = asyncio.create_task(provide_sleep_async(1.0))
            await asyncio.sleep(0.01)  # Let it start
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                return "cancelled"
            return "not cancelled"

        result = await cancel_sleep()
        assert result == "cancelled"


class TestProvideGather:
    """Test provide_gather function."""

    @pytest.mark.asyncio
    async def test_provide_gather_basic_multiple_tasks(self):
        """Test provide_gather with multiple async tasks."""

        async def multiply(n, factor):
            await provide_sleep_async(0.01)
            return n * factor

        results = await provide_gather(multiply(2, 3), multiply(4, 5), multiply(6, 7))

        assert results == [6, 20, 42]

    @pytest.mark.asyncio
    async def test_provide_gather_preserves_order(self):
        """Test provide_gather preserves order of results."""

        async def delayed_return(value, delay):
            await provide_sleep_async(delay)
            return value

        # Longer delays first - should still return in original order
        results = await provide_gather(
            delayed_return("first", 0.1),
            delayed_return("second", 0.05),
            delayed_return("third", 0.01),
        )

        assert results == ["first", "second", "third"]

    @pytest.mark.asyncio
    async def test_provide_gather_single_task(self):
        """Test provide_gather with single task."""

        async def single_task():
            await provide_sleep_async(0.01)
            return "done"

        results = await provide_gather(single_task())
        assert results == ["done"]

    @pytest.mark.asyncio
    async def test_provide_gather_no_tasks_raises_error(self):
        """Test provide_gather raises error when no awaitables provided."""
        with pytest.raises(
            ValidationError, match="At least one awaitable must be provided"
        ):
            await provide_gather()

    @pytest.mark.asyncio
    async def test_provide_gather_with_exception_default(self):
        """Test provide_gather propagates exceptions by default."""

        async def success_task():
            return "success"

        async def failing_task():
            raise RuntimeError("Test error")

        with pytest.raises(RuntimeError, match="Test error"):
            await provide_gather(success_task(), failing_task())

    @pytest.mark.asyncio
    async def test_provide_gather_with_return_exceptions_true(self):
        """Test provide_gather returns exceptions when return_exceptions=True."""

        async def success_task():
            return "success"

        async def failing_task():
            raise RuntimeError("Test error")

        results = await provide_gather(
            success_task(), failing_task(), return_exceptions=True
        )

        assert len(results) == 2
        assert results[0] == "success"
        assert isinstance(results[1], RuntimeError)
        assert str(results[1]) == "Test error"

    @pytest.mark.asyncio
    async def test_provide_gather_different_return_types(self):
        """Test provide_gather with different return types."""

        async def return_int():
            return 42

        async def return_str():
            return "hello"

        async def return_list():
            return [1, 2, 3]

        async def return_dict():
            return {"key": "value"}

        results = await provide_gather(
            return_int(), return_str(), return_list(), return_dict()
        )

        assert results == [42, "hello", [1, 2, 3], {"key": "value"}]

    @pytest.mark.asyncio
    @patch("provide.foundation.asynctools.core.asyncio")
    async def test_provide_gather_uses_asyncio_module(self, mock_asyncio):
        """Test provide_gather calls asyncio.gather()."""
        mock_coro1 = AsyncMock(return_value="result1")
        mock_coro2 = AsyncMock(return_value="result2")
        mock_asyncio.gather = AsyncMock(return_value=["result1", "result2"])

        await provide_gather(mock_coro1(), mock_coro2(), return_exceptions=True)

        mock_asyncio.gather.assert_called_once()
        args, kwargs = mock_asyncio.gather.call_args
        assert len(args) == 2
        assert kwargs["return_exceptions"] is True


class TestProvideWaitFor:
    """Test provide_wait_for function."""

    @pytest.mark.asyncio
    async def test_provide_wait_for_completes_within_timeout(self):
        """Test provide_wait_for completes when task finishes within timeout."""

        async def quick_task():
            await provide_sleep_async(0.01)
            return "completed"

        result = await provide_wait_for(quick_task(), timeout=0.1)
        assert result == "completed"

    @pytest.mark.asyncio
    async def test_provide_wait_for_raises_timeout_error(self):
        """Test provide_wait_for raises TimeoutError when timeout exceeded."""

        async def slow_task():
            await provide_sleep_async(0.2)
            return "too slow"

        with pytest.raises(asyncio.TimeoutError):
            await provide_wait_for(slow_task(), timeout=0.05)

    @pytest.mark.asyncio
    async def test_provide_wait_for_no_timeout(self):
        """Test provide_wait_for works with no timeout."""

        async def task():
            await provide_sleep_async(0.01)
            return "no timeout"

        result = await provide_wait_for(task(), timeout=None)
        assert result == "no timeout"

    @pytest.mark.asyncio
    async def test_provide_wait_for_negative_timeout_raises_error(self):
        """Test provide_wait_for raises error for negative timeout."""

        async def task():
            return "test"

        # Create coroutine but properly handle it to avoid warning
        coro = task()
        try:
            with pytest.raises(ValidationError, match="Timeout must be non-negative"):
                await provide_wait_for(coro, timeout=-1.0)
        finally:
            # Close coroutine if it wasn't consumed
            if coro.cr_frame is not None:
                coro.close()

    @pytest.mark.asyncio
    async def test_provide_wait_for_zero_timeout(self):
        """Test provide_wait_for with zero timeout raises TimeoutError."""

        async def instant_task():
            return "instant"

        # Zero timeout should raise TimeoutError even for immediate tasks
        with pytest.raises(asyncio.TimeoutError):
            await provide_wait_for(instant_task(), timeout=0.0)

    @pytest.mark.asyncio
    @patch("provide.foundation.asynctools.core.asyncio")
    async def test_provide_wait_for_uses_asyncio_module(self, mock_asyncio):
        """Test provide_wait_for calls asyncio.wait_for()."""
        mock_coro = AsyncMock(return_value="result")
        mock_asyncio.wait_for = AsyncMock(return_value="result")

        await provide_wait_for(mock_coro(), timeout=1.0)

        mock_asyncio.wait_for.assert_called_once()
        args, kwargs = mock_asyncio.wait_for.call_args
        # Check that it was called with awaitable and timeout
        assert len(args) >= 1  # At least the awaitable
        assert kwargs.get("timeout") == 1.0 or (len(args) >= 2 and args[1] == 1.0)

    @pytest.mark.asyncio
    async def test_provide_wait_for_propagates_exceptions(self):
        """Test provide_wait_for propagates exceptions from awaitable."""

        async def failing_task():
            raise ValueError("Task failed")

        with pytest.raises(ValueError, match="Task failed"):
            await provide_wait_for(failing_task(), timeout=1.0)


class TestProvideRun:
    """Test provide_run function."""

    def test_provide_run_basic_async_function(self):
        """Test provide_run executes basic async function."""

        async def main():
            await provide_sleep_async(0.01)
            return "hello world"

        result = provide_run(main)
        assert result == "hello world"

    def test_provide_run_with_return_value(self):
        """Test provide_run returns value from async function."""

        async def compute():
            return 2 + 2

        result = provide_run(compute)
        assert result == 4

    def test_provide_run_with_complex_return_value(self):
        """Test provide_run handles complex return values."""

        async def complex_data():
            return {
                "numbers": [1, 2, 3],
                "nested": {"key": "value"},
                "result": await provide_gather(
                    provide_sleep_async(0.01), provide_sleep_async(0.01)
                ),
            }

        result = provide_run(complex_data)
        assert result["numbers"] == [1, 2, 3]
        assert result["nested"]["key"] == "value"
        assert result["result"] == [None, None]  # sleep returns None

    def test_provide_run_non_callable_raises_error(self):
        """Test provide_run raises error for non-callable input."""
        with pytest.raises(ValidationError, match="Main must be callable"):
            provide_run("not callable")

        with pytest.raises(ValidationError, match="Main must be callable"):
            provide_run(123)

        with pytest.raises(ValidationError, match="Main must be callable"):
            provide_run(None)

    def test_provide_run_propagates_exceptions(self):
        """Test provide_run propagates exceptions from async function."""

        async def failing_main():
            raise RuntimeError("Main failed")

        with pytest.raises(RuntimeError, match="Main failed"):
            provide_run(failing_main)

    @patch("provide.foundation.asynctools.core.asyncio")
    def test_provide_run_uses_asyncio_module(self, mock_asyncio):
        """Test provide_run calls asyncio.run()."""

        async def main():
            return "test"

        mock_asyncio.run.return_value = "test"

        result = provide_run(main, debug=True)

        assert result == "test"
        mock_asyncio.run.assert_called_once()
        args, kwargs = mock_asyncio.run.call_args
        # Should be called with a coroutine object (main() returns a coroutine)
        import inspect

        assert inspect.iscoroutine(args[0])
        assert kwargs["debug"] is True

    def test_provide_run_with_debug_false(self):
        """Test provide_run with debug=False."""

        async def main():
            return "debug false"

        result = provide_run(main, debug=False)
        assert result == "debug false"

    def test_provide_run_with_async_generator(self):
        """Test provide_run doesn't work with async generators (by design)."""

        async def async_gen():
            yield 1
            yield 2

        # This should raise an error because async_gen() returns an async generator,
        # not a coroutine that provide_run expects
        with pytest.raises((TypeError, RuntimeError, ValueError)):
            provide_run(async_gen)


class TestAsyncUtilitiesIntegration:
    """Integration tests for async utilities."""

    @pytest.mark.asyncio
    async def test_async_utilities_work_together(self):
        """Test async utilities work together in complex scenarios."""

        async def task_with_timeout(value, delay):
            await provide_sleep_async(delay)
            return value * 2

        async def main_workflow():
            # Use provide_gather to run multiple tasks
            tasks = await provide_gather(
                provide_wait_for(task_with_timeout(1, 0.01), timeout=0.1),
                provide_wait_for(task_with_timeout(2, 0.01), timeout=0.1),
                provide_wait_for(task_with_timeout(3, 0.01), timeout=0.1),
            )
            return sum(tasks)

        result = await main_workflow()
        assert result == 12  # (1*2) + (2*2) + (3*2)

    def test_provide_run_with_complex_async_workflow(self):
        """Test provide_run with complex async workflow."""

        async def complex_workflow():
            # Phase 1: Gather initial data
            initial_data = await provide_gather(
                provide_sleep_async(0.01),
                provide_sleep_async(0.01),
            )

            # Phase 2: Process data with timeout
            async def process_data():
                await provide_sleep_async(0.02)
                return [1, 2, 3]

            processed = await provide_wait_for(process_data(), timeout=0.1)

            # Phase 3: Final computation
            return sum(processed)

        result = provide_run(complex_workflow)
        assert result == 6

    @pytest.mark.asyncio
    async def test_error_handling_across_utilities(self):
        """Test error handling across multiple async utilities."""

        async def failing_task():
            await provide_sleep_async(0.01)
            raise ValueError("Task failed")

        async def success_task():
            await provide_sleep_async(0.01)
            return "success"

        # Test that provide_gather propagates errors
        with pytest.raises(ValueError):
            await provide_gather(success_task(), failing_task())

        # Test that provide_wait_for propagates errors
        with pytest.raises(ValueError):
            await provide_wait_for(failing_task(), timeout=1.0)

    @pytest.mark.asyncio
    async def test_cancellation_support(self):
        """Test cancellation support across utilities."""

        async def cancellable_workflow():
            try:
                # This should be cancellable
                await provide_gather(
                    provide_sleep_async(1.0),  # Long sleep
                    provide_sleep_async(1.0),
                )
                return "not cancelled"
            except asyncio.CancelledError:
                return "cancelled"

        # Start the task and cancel it
        task = asyncio.create_task(cancellable_workflow())
        await asyncio.sleep(0.01)  # Let it start
        task.cancel()

        try:
            result = await task
        except asyncio.CancelledError:
            result = "task cancelled"

        assert result in ["cancelled", "task cancelled"]

    @pytest.mark.asyncio
    async def test_performance_comparison(self):
        """Test performance characteristics of async utilities."""

        async def fast_task(n):
            await provide_sleep_async(0.001)
            return n

        # Sequential execution
        start = time.time()
        sequential_results = []
        for i in range(10):
            result = await fast_task(i)
            sequential_results.append(result)
        sequential_time = time.time() - start

        # Concurrent execution with provide_gather
        start = time.time()
        concurrent_results = await provide_gather(*[fast_task(i) for i in range(10)])
        concurrent_time = time.time() - start

        # Concurrent should be faster
        assert concurrent_time < sequential_time
        assert sequential_results == concurrent_results

    def test_async_utilities_error_messages(self):
        """Test that async utilities provide helpful error messages."""
        # Test provide_run error message
        try:
            provide_run("not callable")
        except ValidationError as e:
            assert "Main must be callable" in str(e)

        # Test provide_sleep_async error (need to run in event loop)
        async def test_sleep_error():
            try:
                await provide_sleep_async(-1)
            except ValidationError as e:
                return "Sleep delay must be non-negative" in str(e)
            return False

        result = provide_run(test_sleep_error)
        assert result is True
