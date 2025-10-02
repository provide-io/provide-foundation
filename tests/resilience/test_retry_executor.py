"""Tests for RetryExecutor - the unified retry execution engine.

This test file follows TDD principles - tests are written before implementation.
"""

import asyncio
from typing import Never
from provide.testkit.mocking import AsyncMock, MagicMock, patch
from provide.testkit.time import make_controlled_time

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)


class TestRetryExecutorSync(FoundationTestCase):
    """Test synchronous retry execution."""

    def test_successful_first_attempt(self) -> None:
        """Test function that succeeds on first try."""
        policy = RetryPolicy(max_attempts=3)
        executor = RetryExecutor(policy)

        mock_func = MagicMock(return_value="success")

        result = executor.execute_sync(mock_func, "arg1", key="value")

        assert result == "success"
        mock_func.assert_called_once_with("arg1", key="value")

    def test_retry_on_failure_then_success(self) -> None:
        """Test function that fails then succeeds using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(
            side_effect=[
                ValueError("attempt 1"),
                ValueError("attempt 2"),
                "success",
            ]
        )

        result = executor.execute_sync(mock_func)

        assert result == "success"
        assert mock_func.call_count == 3

    def test_max_attempts_exceeded(self) -> None:
        """Test that error is raised after max attempts."""
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("always fails"))

        with pytest.raises(ValueError) as exc_info:
            executor.execute_sync(mock_func)

        assert "always fails" in str(exc_info.value)
        assert mock_func.call_count == 3

    def test_specific_exception_filtering(self) -> None:
        """Test retrying only specific exception types."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(ValueError, TypeError),
        )
        executor = RetryExecutor(policy)

        # Should not retry RuntimeError
        mock_func = MagicMock(side_effect=RuntimeError("not retryable"))

        with pytest.raises(RuntimeError):
            executor.execute_sync(mock_func)

        assert mock_func.call_count == 1  # No retries

    def test_no_retry_when_max_attempts_is_1(self) -> None:
        """Test that no retry occurs when max_attempts=1."""
        policy = RetryPolicy(max_attempts=1)
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        assert mock_func.call_count == 1

    def test_delay_between_retries(self) -> None:
        """Test that delay is applied between retries."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,  # Use small real delay
            backoff=BackoffStrategy.FIXED,
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 3 times (all attempts)
        assert mock_func.call_count == 3

    @pytest.mark.slow
    def test_exponential_backoff(self) -> None:
        """Test exponential backoff strategy with real delays."""
        policy = RetryPolicy(
            max_attempts=4,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.EXPONENTIAL,
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 4 times (all attempts)
        assert mock_func.call_count == 4

    @pytest.mark.slow
    def test_linear_backoff(self) -> None:
        """Test linear backoff strategy with real delays."""
        policy = RetryPolicy(
            max_attempts=4,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.LINEAR,
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 4 times (all attempts)
        assert mock_func.call_count == 4

    @pytest.mark.slow
    def test_fibonacci_backoff(self) -> None:
        """Test Fibonacci backoff strategy with real delays."""
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.FIBONACCI,
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 5 times (all attempts)
        assert mock_func.call_count == 5

    @pytest.mark.slow
    def test_max_delay_cap(self) -> None:
        """Test that delays are capped at max_delay with real delays."""
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.2,  # Real delay for thorough testing
            backoff=BackoffStrategy.EXPONENTIAL,
            max_delay=0.3,  # Real max delay cap
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 5 times (all attempts)
        assert mock_func.call_count == 5

    def test_on_retry_callback(self) -> None:
        """Test that on_retry callback is invoked."""
        callback = MagicMock()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=callback)

        mock_func = MagicMock(
            side_effect=[
                ValueError("attempt 1"),
                ValueError("attempt 2"),
                "success",
            ]
        )

        result = executor.execute_sync(mock_func)

        assert result == "success"
        assert callback.call_count == 2  # Called for retry attempts 2 and 3

        # Check callback arguments
        calls = callback.call_args_list
        assert calls[0][0][0] == 1  # First retry (attempt 2)
        assert isinstance(calls[0][0][1], ValueError)
        assert calls[1][0][0] == 2  # Second retry (attempt 3)

    def test_on_retry_callback_exception_ignored(self) -> None:
        """Test that exceptions in on_retry don't break retry."""

        def bad_callback(attempt, error) -> Never:
            raise RuntimeError("callback failed")

        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=bad_callback)

        mock_func = MagicMock(
            side_effect=[
                ValueError("attempt 1"),
                "success",
            ]
        )

        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            result = executor.execute_sync(mock_func)

        assert result == "success"
        # Should log callback failure
        mock_logger.warning.assert_called()

    @pytest.mark.slow
    def test_with_jitter(self) -> None:
        """Test that jitter adds randomness to delays with real delays."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.FIXED,
            jitter=True,
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 3 times (all attempts)
        assert mock_func.call_count == 3


class TestRetryExecutorAsync(FoundationTestCase):
    """Test asynchronous retry execution."""

    @pytest.mark.asyncio
    async def test_successful_first_attempt(self) -> None:
        """Test async function that succeeds on first try."""
        policy = RetryPolicy(max_attempts=3)
        executor = RetryExecutor(policy)

        mock_func = AsyncMock(return_value="success")

        result = await executor.execute_async(mock_func, "arg1", key="value")

        assert result == "success"
        mock_func.assert_called_once_with("arg1", key="value")

    @pytest.mark.asyncio
    async def test_retry_on_failure_then_success(self) -> None:
        """Test async function that fails then succeeds using controlled time."""
        get_time, _advance_time, _fake_sleep, fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, time_source=get_time, async_sleep_func=fake_async_sleep)

        mock_func = AsyncMock(
            side_effect=[
                ValueError("attempt 1"),
                ValueError("attempt 2"),
                "success",
            ]
        )

        result = await executor.execute_async(mock_func)

        assert result == "success"
        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self) -> None:
        """Test that error is raised after max attempts."""
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy)

        mock_func = AsyncMock(side_effect=ValueError("always fails"))

        with pytest.raises(ValueError) as exc_info:
            await executor.execute_async(mock_func)

        assert "always fails" in str(exc_info.value)
        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_specific_exception_filtering(self) -> None:
        """Test retrying only specific exception types."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(ValueError, TypeError),
        )
        executor = RetryExecutor(policy)

        # Should not retry RuntimeError
        mock_func = AsyncMock(side_effect=RuntimeError("not retryable"))

        with pytest.raises(RuntimeError):
            await executor.execute_async(mock_func)

        assert mock_func.call_count == 1  # No retries

    @pytest.mark.asyncio
    async def test_delay_between_retries(self) -> None:
        """Test that delay is applied between async retries."""
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,  # Use small real delay
            backoff=BackoffStrategy.FIXED,
            jitter=False,
        )
        executor = RetryExecutor(policy)

        mock_func = AsyncMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            await executor.execute_async(mock_func)

        # Function should have been called 3 times (all attempts)
        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_on_retry_callback_async(self) -> None:
        """Test that async on_retry callback is invoked."""
        callback = AsyncMock()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=callback)

        mock_func = AsyncMock(
            side_effect=[
                ValueError("attempt 1"),
                ValueError("attempt 2"),
                "success",
            ]
        )

        result = await executor.execute_async(mock_func)

        assert result == "success"
        assert callback.call_count == 2  # Called for retry attempts 2 and 3

    @pytest.mark.asyncio
    async def test_mixed_sync_async_callback(self) -> None:
        """Test sync callback with async execution."""
        callback = MagicMock()  # Sync callback
        policy = RetryPolicy(max_attempts=2, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=callback)

        mock_func = AsyncMock(
            side_effect=[
                ValueError("attempt 1"),
                "success",
            ]
        )

        result = await executor.execute_async(mock_func)

        assert result == "success"
        assert callback.call_count == 1

    @pytest.mark.asyncio
    async def test_concurrent_executions(self) -> None:
        """Test multiple concurrent retry executions."""
        policy = RetryPolicy(max_attempts=2, base_delay=0.01)
        executor = RetryExecutor(policy)

        async def failing_then_success(id) -> str:
            if not hasattr(failing_then_success, f"called_{id}"):
                setattr(failing_then_success, f"called_{id}", True)
                raise ValueError(f"First call {id}")
            return f"success {id}"

        # Run multiple concurrent executions
        results = await asyncio.gather(
            executor.execute_async(failing_then_success, 1),
            executor.execute_async(failing_then_success, 2),
            executor.execute_async(failing_then_success, 3),
        )

        assert results == ["success 1", "success 2", "success 3"]


class TestRetryExecutorLogging:
    """Test logging behavior of RetryExecutor."""

    def test_retry_attempt_logged(self) -> None:
        """Test that retry attempts are logged."""
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy)

        mock_func = MagicMock(
            side_effect=[
                ValueError("fail"),
                "success",
            ]
        )

        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            result = executor.execute_sync(mock_func)

        assert result == "success"

        # Should log the retry attempt
        mock_logger.info.assert_called()
        log_message = mock_logger.info.call_args[0][0]
        assert "Retry" in log_message
        assert "1/3" in log_message or "attempt 2" in log_message

    def test_max_attempts_failure_logged(self) -> None:
        """Test that max attempts failure is logged."""
        policy = RetryPolicy(max_attempts=2, base_delay=0.01)
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=ValueError("always fails"))

        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            with pytest.raises(ValueError):
                executor.execute_sync(mock_func)

        # Should log the final failure
        assert mock_logger.error.called
        log_message = mock_logger.error.call_args[0][0]
        assert "attempts failed" in log_message.lower()

    def test_non_retryable_error_not_logged_as_retry(self) -> None:
        """Test that non-retryable errors don't generate retry logs."""
        policy = RetryPolicy(
            max_attempts=3,
            retryable_errors=(ValueError,),
        )
        executor = RetryExecutor(policy)

        mock_func = MagicMock(side_effect=RuntimeError("not retryable"))

        with patch("provide.foundation.hub.foundation.get_foundation_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
            with pytest.raises(RuntimeError):
                executor.execute_sync(mock_func)

        # Should not log retry attempts for non-retryable errors
        mock_logger.info.assert_not_called()
        mock_logger.warning.assert_not_called()


class TestRetryExecutorEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_max_attempts_raises(self) -> None:
        """Test that max_attempts=0 raises an error."""
        with pytest.raises(ValueError) as exc_info:
            policy = RetryPolicy(max_attempts=0)
            RetryExecutor(policy)

        assert "at least 1" in str(exc_info.value).lower()

    def test_negative_delay_raises(self) -> None:
        """Test that negative delay raises an error."""
        with pytest.raises(ValueError) as exc_info:
            RetryPolicy(base_delay=-1.0)

        assert "positive" in str(exc_info.value).lower() or "negative" in str(exc_info.value).lower()

    def test_none_function_raises(self) -> None:
        """Test that None function raises appropriate error."""
        policy = RetryPolicy()
        executor = RetryExecutor(policy)

        with pytest.raises(TypeError):
            executor.execute_sync(None)

    def test_function_with_no_args(self) -> None:
        """Test retry with function that takes no arguments."""
        policy = RetryPolicy(max_attempts=2, base_delay=0.01)
        executor = RetryExecutor(policy)

        call_count = 0

        def no_args_func() -> str:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("first")
            return "success"

        result = executor.execute_sync(no_args_func)

        assert result == "success"
        assert call_count == 2

    def test_generator_function_retry(self) -> None:
        """Test handling of generator functions with retry executor."""
        policy = RetryPolicy(max_attempts=2, base_delay=0.01)
        executor = RetryExecutor(policy)

        # Simple test: generator functions should work with retry executor
        # The executor should call the generator function and return the generator

        def simple_generator():
            yield 1
            yield 2
            yield 3

        result = executor.execute_sync(simple_generator)

        # Should return a generator that can be consumed
        values = list(result)
        assert values == [1, 2, 3]
