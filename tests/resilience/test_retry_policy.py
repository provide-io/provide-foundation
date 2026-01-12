#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for RetryPolicy configuration and behavior."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.resilience.retry import BackoffStrategy, RetryPolicy


class TestRetryPolicyConfiguration(FoundationTestCase):
    """Test RetryPolicy configuration and validation."""

    def test_default_configuration(self) -> None:
        """Test default policy configuration."""
        policy = RetryPolicy()

        assert policy.max_attempts == 3
        assert policy.backoff == BackoffStrategy.EXPONENTIAL
        assert policy.base_delay == 1.0
        assert policy.max_delay == 60.0
        assert policy.jitter is True
        assert policy.retryable_errors is None
        assert policy.retryable_status_codes is None

    def test_custom_configuration(self) -> None:
        """Test custom policy configuration."""
        policy = RetryPolicy(
            max_attempts=5,
            backoff=BackoffStrategy.LINEAR,
            base_delay=2.0,
            max_delay=30.0,
            jitter=False,
            retryable_errors=(ValueError, TypeError),
            retryable_status_codes={500, 503},
        )

        assert policy.max_attempts == 5
        assert policy.backoff == BackoffStrategy.LINEAR
        assert policy.base_delay == 2.0
        assert policy.max_delay == 30.0
        assert policy.jitter is False
        assert policy.retryable_errors == (ValueError, TypeError)
        assert policy.retryable_status_codes == {500, 503}

    def test_invalid_max_attempts(self) -> None:
        """Test that invalid max_attempts raises error."""
        with pytest.raises(ValueError) as exc_info:
            RetryPolicy(max_attempts=0)

        assert "at least 1" in str(exc_info.value).lower()

        with pytest.raises(ValueError):
            RetryPolicy(max_attempts=-1)

    def test_invalid_delays(self) -> None:
        """Test that invalid delays raise errors."""
        with pytest.raises(ValueError) as exc_info:
            RetryPolicy(base_delay=-1.0)

        assert "positive" in str(exc_info.value).lower()

        with pytest.raises(ValueError):
            RetryPolicy(max_delay=-1.0)

        with pytest.raises(ValueError):
            RetryPolicy(base_delay=10.0, max_delay=5.0)  # max < base


class TestRetryPolicyDelayCalculation(FoundationTestCase):
    """Test delay calculation for different backoff strategies."""

    def test_fixed_backoff(self) -> None:
        """Test fixed backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIXED,
            base_delay=2.0,
            jitter=False,
        )

        assert policy.calculate_delay(1) == 2.0
        assert policy.calculate_delay(2) == 2.0
        assert policy.calculate_delay(3) == 2.0
        assert policy.calculate_delay(10) == 2.0

    def test_linear_backoff(self) -> None:
        """Test linear backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.LINEAR,
            base_delay=2.0,
            jitter=False,
        )

        assert policy.calculate_delay(1) == 2.0
        assert policy.calculate_delay(2) == 4.0
        assert policy.calculate_delay(3) == 6.0
        assert policy.calculate_delay(4) == 8.0

    def test_exponential_backoff(self) -> None:
        """Test exponential backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=2.0,
            jitter=False,
        )

        assert policy.calculate_delay(1) == 2.0  # 2 * 2^0
        assert policy.calculate_delay(2) == 4.0  # 2 * 2^1
        assert policy.calculate_delay(3) == 8.0  # 2 * 2^2
        assert policy.calculate_delay(4) == 16.0  # 2 * 2^3

    def test_fibonacci_backoff(self) -> None:
        """Test Fibonacci backoff strategy."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIBONACCI,
            base_delay=1.0,
            jitter=False,
        )

        assert policy.calculate_delay(1) == 1.0  # fib(1) = 1
        assert policy.calculate_delay(2) == 1.0  # fib(2) = 1
        assert policy.calculate_delay(3) == 2.0  # fib(3) = 2
        assert policy.calculate_delay(4) == 3.0  # fib(4) = 3
        assert policy.calculate_delay(5) == 5.0  # fib(5) = 5
        assert policy.calculate_delay(6) == 8.0  # fib(6) = 8

    def test_max_delay_cap(self) -> None:
        """Test that delays are capped at max_delay."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=10.0,
            max_delay=50.0,
            jitter=False,
        )

        assert policy.calculate_delay(1) == 10.0
        assert policy.calculate_delay(2) == 20.0
        assert policy.calculate_delay(3) == 40.0
        assert policy.calculate_delay(4) == 50.0  # Capped
        assert policy.calculate_delay(10) == 50.0  # Still capped

    def test_zero_attempt_returns_zero(self) -> None:
        """Test that attempt 0 returns 0 delay."""
        policy = RetryPolicy(base_delay=5.0, jitter=False)

        assert policy.calculate_delay(0) == 0
        assert policy.calculate_delay(-1) == 0

    def test_jitter_adds_randomness(self) -> None:
        """Test that jitter adds randomness to delays."""
        policy = RetryPolicy(
            backoff=BackoffStrategy.FIXED,
            base_delay=10.0,
            jitter=True,
        )

        # Collect multiple delay calculations
        delays = [policy.calculate_delay(1) for _ in range(100)]

        # All should be within ±25% of base delay
        assert all(7.5 <= d <= 12.5 for d in delays)

        # Should have variation (not all the same)
        assert len(set(delays)) > 1

        # Mean should be close to base delay
        mean_delay = sum(delays) / len(delays)
        assert 9.5 <= mean_delay <= 10.5


class TestRetryPolicyShouldRetry(FoundationTestCase):
    """Test should_retry decision logic."""

    def test_should_retry_within_attempts(self) -> None:
        """Test should_retry returns True within max attempts."""
        policy = RetryPolicy(max_attempts=3)

        error = ValueError("test")
        assert policy.should_retry(error, 1) is True
        assert policy.should_retry(error, 2) is True
        assert policy.should_retry(error, 3) is False  # Exceeds max
        assert policy.should_retry(error, 4) is False

    def test_should_retry_with_retryable_errors(self) -> None:
        """Test should_retry with specific error types."""
        policy = RetryPolicy(
            max_attempts=5,
            retryable_errors=(ValueError, TypeError),
        )

        # Retryable errors
        assert policy.should_retry(ValueError("test"), 1) is True
        assert policy.should_retry(TypeError("test"), 1) is True

        # Non-retryable errors
        assert policy.should_retry(RuntimeError("test"), 1) is False
        assert policy.should_retry(KeyError("test"), 1) is False

        # Even retryable errors stop at max attempts
        assert policy.should_retry(ValueError("test"), 5) is False

    def test_should_retry_none_errors_means_retry_all(self) -> None:
        """Test that None retryable_errors means retry all errors."""
        policy = RetryPolicy(
            max_attempts=3,
            retryable_errors=None,
        )

        assert policy.should_retry(ValueError("test"), 1) is True
        assert policy.should_retry(RuntimeError("test"), 1) is True
        assert policy.should_retry(Exception("test"), 1) is True
        assert policy.should_retry(KeyError("test"), 1) is True

    def test_should_retry_response_with_status_codes(self) -> None:
        """Test should_retry_response for HTTP responses."""
        policy = RetryPolicy(
            max_attempts=3,
            retryable_status_codes={500, 502, 503},
        )

        # Mock response objects
        class MockResponse:
            def __init__(self, status: int) -> None:
                self.status = status

        # Retryable status codes
        assert policy.should_retry_response(MockResponse(500), 1) is True
        assert policy.should_retry_response(MockResponse(502), 1) is True
        assert policy.should_retry_response(MockResponse(503), 1) is True

        # Non-retryable status codes
        assert policy.should_retry_response(MockResponse(200), 1) is False
        assert policy.should_retry_response(MockResponse(404), 1) is False
        assert policy.should_retry_response(MockResponse(400), 1) is False

        # Respects max attempts
        assert policy.should_retry_response(MockResponse(500), 3) is False

    def test_should_retry_response_none_codes_means_no_retry(self) -> None:
        """Test that None retryable_status_codes means don't retry responses."""
        policy = RetryPolicy(
            max_attempts=3,
            retryable_status_codes=None,
        )

        class MockResponse:
            def __init__(self, status: int) -> None:
                self.status = status

        assert policy.should_retry_response(MockResponse(500), 1) is False
        assert policy.should_retry_response(MockResponse(200), 1) is False


class TestRetryPolicyComparison(FoundationTestCase):
    """Test RetryPolicy comparison and hashing."""

    def test_equality(self) -> None:
        """Test policy equality comparison."""
        policy1 = RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
        )

        policy2 = RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
        )

        policy3 = RetryPolicy(
            max_attempts=5,  # Different
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
        )

        assert policy1 == policy2
        assert policy1 != policy3
        assert policy2 != policy3

    def test_hashable(self) -> None:
        """Test that policies are hashable."""
        policy1 = RetryPolicy(max_attempts=3)
        policy2 = RetryPolicy(max_attempts=3)
        policy3 = RetryPolicy(max_attempts=5)

        # Should be hashable
        policy_set = {policy1, policy2, policy3}

        # policy1 and policy2 are equal, so set should have 2 items
        assert len(policy_set) == 2

    def test_immutable(self) -> None:
        """Test that policy is immutable (frozen)."""
        policy = RetryPolicy(max_attempts=3)

        with pytest.raises(AttributeError):
            policy.max_attempts = 5

        with pytest.raises(AttributeError):
            policy.base_delay = 10.0


class TestRetryPolicyStringRepresentation(FoundationTestCase):
    """Test string representation of RetryPolicy."""

    def test_repr(self) -> None:
        """Test __repr__ output."""
        policy = RetryPolicy(
            max_attempts=5,
            backoff=BackoffStrategy.LINEAR,
            base_delay=2.0,
        )

        repr_str = repr(policy)
        assert "RetryPolicy" in repr_str
        assert "max_attempts=5" in repr_str
        assert "LINEAR" in repr_str
        assert "base_delay=2.0" in repr_str

    def test_str(self) -> None:
        """Test __str__ output."""
        policy = RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.EXPONENTIAL,
        )

        str_repr = str(policy)
        assert "3 attempts" in str_repr.lower() or "max_attempts=3" in str_repr
        assert "exponential" in str_repr.lower()


# 🧱🏗️🔚
