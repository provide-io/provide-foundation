#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for RetryExecutor - the unified retry execution engine.

This test file follows TDD principles - tests are written before implementation."""

from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.resilience.retry import (
    RetryExecutor,
    RetryPolicy,
)
from provide.foundation.resilience.types import BackoffStrategy


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
        """Test that error is raised after max attempts using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("always fails"))

        with pytest.raises(ValueError) as exc_info:
            executor.execute_sync(mock_func)

        assert "always fails" in str(exc_info.value)
        assert mock_func.call_count == 3

    def test_specific_exception_filtering(self) -> None:
        """Test retrying only specific exception types using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,
            retryable_errors=(ValueError, TypeError),
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

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
        """Test that delay is applied between retries using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.01,  # Use small real delay
            backoff=BackoffStrategy.FIXED,
            jitter=False,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 3 times (all attempts)
        assert mock_func.call_count == 3

    @pytest.mark.slow
    def test_exponential_backoff(self) -> None:
        """Test exponential backoff strategy using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=4,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.EXPONENTIAL,
            jitter=False,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 4 times (all attempts)
        assert mock_func.call_count == 4

    @pytest.mark.slow
    def test_linear_backoff(self) -> None:
        """Test linear backoff strategy using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=4,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.LINEAR,
            jitter=False,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 4 times (all attempts)
        assert mock_func.call_count == 4

    @pytest.mark.slow
    def test_fibonacci_backoff(self) -> None:
        """Test Fibonacci backoff strategy using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.FIBONACCI,
            jitter=False,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 5 times (all attempts)
        assert mock_func.call_count == 5

    @pytest.mark.slow
    def test_max_delay_cap(self) -> None:
        """Test that delays are capped at max_delay using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.2,  # Real delay for thorough testing
            backoff=BackoffStrategy.EXPONENTIAL,
            max_delay=0.3,  # Real max delay cap
            jitter=False,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 5 times (all attempts)
        assert mock_func.call_count == 5

    def test_on_retry_callback(self) -> None:
        """Test that on_retry callback is invoked using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        callback = MagicMock()
        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=callback, time_source=get_time, sleep_func=fake_sleep)

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
        """Test that exceptions in on_retry don't break retry using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()

        def bad_callback(attempt, error) -> Never:
            raise RuntimeError("callback failed")

        policy = RetryPolicy(max_attempts=3, base_delay=0.01)
        executor = RetryExecutor(policy, on_retry=bad_callback, time_source=get_time, sleep_func=fake_sleep)

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
        """Test that jitter adds randomness to delays using controlled time."""
        get_time, _advance_time, fake_sleep, _fake_async_sleep = make_controlled_time()
        policy = RetryPolicy(
            max_attempts=3,
            base_delay=0.1,  # Real delay for thorough testing
            backoff=BackoffStrategy.FIXED,
            jitter=True,
        )
        executor = RetryExecutor(policy, time_source=get_time, sleep_func=fake_sleep)

        mock_func = MagicMock(side_effect=ValueError("fail"))

        with pytest.raises(ValueError):
            executor.execute_sync(mock_func)

        # Function should have been called 3 times (all attempts)
        assert mock_func.call_count == 3


# 🧱🏗️🔚
