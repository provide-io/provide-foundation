#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for logger OTLP circuit breaker.

Tests all functionality in logger/otlp/circuit.py including state transitions,
exponential backoff, and threading safety."""

from __future__ import annotations

import time

from provide.foundation.logger.otlp.circuit import (
    OTLPCircuitBreaker,
    get_otlp_circuit_breaker,
    reset_otlp_circuit_breaker,
)


class TestOTLPCircuitBreakerBasics:
    """Tests for basic circuit breaker initialization and properties."""

    def test_initialization(self) -> None:
        """Test circuit breaker initialization with default values."""
        breaker = OTLPCircuitBreaker()

        assert breaker.failure_threshold == 5
        assert breaker.base_timeout == 60.0
        assert breaker.half_open_timeout == 10.0
        assert breaker.state == "closed"

    def test_initialization_with_custom_values(self) -> None:
        """Test circuit breaker initialization with custom parameters."""
        breaker = OTLPCircuitBreaker(
            failure_threshold=3,
            timeout=30.0,
            half_open_timeout=5.0,
        )

        assert breaker.failure_threshold == 3
        assert breaker.base_timeout == 30.0
        assert breaker.half_open_timeout == 5.0

    def test_state_property(self) -> None:
        """Test that state property returns current state."""
        breaker = OTLPCircuitBreaker()

        assert breaker.state == "closed"

    def test_state_property_thread_safe(self) -> None:
        """Test that state property uses locking."""
        breaker = OTLPCircuitBreaker()

        # Should work without raising
        state = breaker.state
        assert state in ["closed", "open", "half_open"]


class TestCanAttempt:
    """Tests for can_attempt() method."""

    def test_can_attempt_when_closed(self) -> None:
        """Test that attempts are allowed when circuit is closed."""
        breaker = OTLPCircuitBreaker()

        assert breaker.can_attempt() is True

    def test_can_attempt_when_open_without_enough_time(self) -> None:
        """Test that attempts are blocked when circuit is open."""
        breaker = OTLPCircuitBreaker(failure_threshold=1, timeout=10.0)

        # Record failure to open circuit
        breaker.record_failure()

        assert breaker.state == "open"
        assert breaker.can_attempt() is False

    def test_can_attempt_when_open_after_timeout(self) -> None:
        """Test that circuit transitions to half-open after timeout."""
        breaker = OTLPCircuitBreaker(failure_threshold=1, timeout=10.0)

        # Manually set to open state with a known failure time
        breaker._state = "open"
        breaker._last_failure_time = time.time() - 10.5  # Failed 10.5 seconds ago (>= timeout)
        breaker._open_count = 0  # First time opening, timeout = 10 * 2^0 = 10

        # Should transition to half-open since timeout (10s) has passed
        assert breaker.can_attempt() is True
        assert breaker.state == "half_open"

    def test_can_attempt_when_half_open_first_time(self) -> None:
        """Test that first attempt is allowed in half-open state."""
        breaker = OTLPCircuitBreaker()
        breaker._state = "half_open"
        breaker._last_attempt_time = None

        assert breaker.can_attempt() is True

    def test_can_attempt_when_half_open_within_timeout(self) -> None:
        """Test that rapid attempts are blocked in half-open state."""
        breaker = OTLPCircuitBreaker(half_open_timeout=5.0)
        breaker._state = "half_open"
        breaker._last_attempt_time = time.time() - 2.0  # Attempted 2 seconds ago

        # Second attempt within timeout should be blocked
        assert breaker.can_attempt() is False

    def test_can_attempt_when_half_open_after_timeout(self) -> None:
        """Test that attempts are allowed in half-open after timeout."""
        breaker = OTLPCircuitBreaker(half_open_timeout=5.0)
        breaker._state = "half_open"
        breaker._last_attempt_time = time.time() - 6.0  # Attempted 6 seconds ago

        # Second attempt after timeout should be allowed
        assert breaker.can_attempt() is True


class TestRecordSuccess:
    """Tests for record_success() method."""

    def test_record_success_from_closed(self) -> None:
        """Test recording success when circuit is closed."""
        breaker = OTLPCircuitBreaker()

        breaker.record_success()

        assert breaker.state == "closed"
        assert breaker.get_stats()["failure_count"] == 0

    def test_record_success_from_half_open(self) -> None:
        """Test that success in half-open closes the circuit."""
        breaker = OTLPCircuitBreaker(failure_threshold=1)

        # Open circuit
        breaker.record_failure()
        assert breaker.state == "open"

        # Transition to half-open
        breaker._state = "half_open"

        # Record success
        breaker.record_success()

        assert breaker.state == "closed"
        assert breaker.get_stats()["failure_count"] == 0

    def test_record_success_resets_counters(self) -> None:
        """Test that success resets failure counters."""
        breaker = OTLPCircuitBreaker(failure_threshold=5)

        # Record some failures
        breaker.record_failure()
        breaker.record_failure()

        assert breaker.get_stats()["failure_count"] == 2

        # Record success
        breaker.record_success()

        stats = breaker.get_stats()
        assert stats["failure_count"] == 0
        assert stats["last_failure_time"] is None
        assert stats["last_attempt_time"] is None

    def test_record_success_decays_open_count(self) -> None:
        """Test that success decays the open count."""
        breaker = OTLPCircuitBreaker(failure_threshold=1)

        # Open circuit multiple times
        breaker.record_failure()
        breaker._state = "closed"
        breaker.record_failure()

        assert breaker._open_count == 2

        # Record success
        breaker.record_success()

        assert breaker._open_count == 1


class TestRecordFailure:
    """Tests for record_failure() method."""

    def test_record_failure_increments_count(self) -> None:
        """Test that failure increments failure counter."""
        breaker = OTLPCircuitBreaker(failure_threshold=5)

        breaker.record_failure()

        assert breaker.get_stats()["failure_count"] == 1

    def test_record_failure_sets_timestamp(self) -> None:
        """Test that failure records timestamp."""
        breaker = OTLPCircuitBreaker()

        before = time.time()
        breaker.record_failure()
        after = time.time()

        stats = breaker.get_stats()
        assert stats["last_failure_time"] is not None
        assert before <= stats["last_failure_time"] <= after

    def test_record_failure_opens_circuit_at_threshold(self) -> None:
        """Test that circuit opens after threshold failures."""
        breaker = OTLPCircuitBreaker(failure_threshold=3)

        assert breaker.state == "closed"

        breaker.record_failure()
        breaker.record_failure()
        assert breaker.state == "closed"

        breaker.record_failure()
        assert breaker.state == "open"

    def test_record_failure_with_exception(self) -> None:
        """Test recording failure with exception information."""
        breaker = OTLPCircuitBreaker()

        error = Exception("Connection failed")
        breaker.record_failure(error)

        assert breaker.get_stats()["failure_count"] == 1

    def test_record_failure_from_half_open(self) -> None:
        """Test that failure in half-open returns to open."""
        breaker = OTLPCircuitBreaker(failure_threshold=1)

        # Open circuit
        breaker.record_failure()
        assert breaker.state == "open"

        # Transition to half-open
        breaker._state = "half_open"
        open_count_before = breaker._open_count

        # Record failure
        breaker.record_failure()

        assert breaker.state == "open"
        assert breaker._open_count == open_count_before + 1


class TestReset:
    """Tests for reset() method."""

    def test_reset_from_open(self) -> None:
        """Test that reset closes an open circuit."""
        breaker = OTLPCircuitBreaker(failure_threshold=1)

        # Open circuit
        breaker.record_failure()
        assert breaker.state == "open"

        # Reset
        breaker.reset()

        assert breaker.state == "closed"

    def test_reset_clears_all_state(self) -> None:
        """Test that reset clears all internal state."""
        breaker = OTLPCircuitBreaker(failure_threshold=1)

        # Create some state
        breaker.record_failure()
        breaker._open_count = 5

        # Reset
        breaker.reset()

        stats = breaker.get_stats()
        assert stats["state"] == "closed"
        assert stats["failure_count"] == 0
        assert stats["open_count"] == 0
        assert stats["last_failure_time"] is None
        assert stats["last_attempt_time"] is None


class TestGetStats:
    """Tests for get_stats() method."""

    def test_get_stats_initial_state(self) -> None:
        """Test stats for newly created circuit breaker."""
        breaker = OTLPCircuitBreaker()

        stats = breaker.get_stats()

        assert stats["state"] == "closed"
        assert stats["failure_count"] == 0
        assert stats["open_count"] == 0
        assert stats["last_failure_time"] is None
        assert stats["last_attempt_time"] is None
        assert "current_timeout" in stats

    def test_get_stats_after_failures(self) -> None:
        """Test stats after recording failures."""
        breaker = OTLPCircuitBreaker(failure_threshold=5)

        breaker.record_failure()
        breaker.record_failure()

        stats = breaker.get_stats()

        assert stats["failure_count"] == 2
        assert stats["last_failure_time"] is not None

    def test_get_stats_timeout_calculation(self) -> None:
        """Test that current timeout is calculated correctly."""
        breaker = OTLPCircuitBreaker(timeout=30.0)

        stats = breaker.get_stats()
        assert stats["current_timeout"] == 30.0

        # After opening once
        breaker._open_count = 1
        stats = breaker.get_stats()
        assert stats["current_timeout"] == 60.0  # 30 * 2^1

        # After opening twice
        breaker._open_count = 2
        stats = breaker.get_stats()
        assert stats["current_timeout"] == 120.0  # 30 * 2^2


class TestExponentialBackoff:
    """Tests for exponential backoff behavior."""

    def test_exponential_backoff_timeout_increases(self) -> None:
        """Test that timeout doubles with each circuit open."""
        breaker = OTLPCircuitBreaker(failure_threshold=1, timeout=10.0)

        # Manually set state after first failure  (open_count = 0)
        breaker._state = "open"
        breaker._open_count = 0  # First time, timeout = 10 * 2^0 = 10
        breaker._last_failure_time = time.time() - 10.5  # Failed 10.5 seconds ago

        # After 10 seconds, circuit should go half-open
        assert breaker.can_attempt() is True
        assert breaker.state == "half_open"

        # Record another failure (will increment open_count to 1)
        breaker.record_failure()

        # Now timeout should be 20 seconds (10 * 2^1)
        # Set last failure to 19 seconds ago (not enough)
        breaker._last_failure_time = time.time() - 19.5
        assert breaker.can_attempt() is False

        # Set last failure to 21 seconds ago (enough)
        breaker._last_failure_time = time.time() - 20.5
        assert breaker.can_attempt() is True

    def test_exponential_backoff_caps_at_10(self) -> None:
        """Test that exponential backoff caps at 2^10."""
        breaker = OTLPCircuitBreaker(timeout=1.0)

        # Set open count to 11 (should cap at 10)
        breaker._open_count = 11

        stats = breaker.get_stats()
        # Should be 1 * 2^10 = 1024, not 1 * 2^11 = 2048
        assert stats["current_timeout"] == 1024.0


class TestGlobalInstance:
    """Tests for global circuit breaker instance management."""

    def test_get_otlp_circuit_breaker_returns_instance(self) -> None:
        """Test that global getter returns a circuit breaker instance."""
        breaker = get_otlp_circuit_breaker()

        assert isinstance(breaker, OTLPCircuitBreaker)

    def test_get_otlp_circuit_breaker_returns_same_instance(self) -> None:
        """Test that global getter returns the same instance."""
        breaker1 = get_otlp_circuit_breaker()
        breaker2 = get_otlp_circuit_breaker()

        assert breaker1 is breaker2

    def test_get_otlp_circuit_breaker_default_config(self) -> None:
        """Test that global instance has correct default configuration."""
        # Reset first to ensure clean state
        reset_otlp_circuit_breaker()

        breaker = get_otlp_circuit_breaker()

        assert breaker.failure_threshold == 5
        assert breaker.base_timeout == 30.0
        assert breaker.half_open_timeout == 10.0

    def test_reset_otlp_circuit_breaker(self) -> None:
        """Test that global reset resets the circuit breaker."""
        breaker = get_otlp_circuit_breaker()

        # Make some changes
        breaker.record_failure()
        breaker.record_failure()

        assert breaker.get_stats()["failure_count"] > 0

        # Reset
        reset_otlp_circuit_breaker()

        assert breaker.get_stats()["failure_count"] == 0
        assert breaker.state == "closed"


class TestThreadSafety:
    """Tests for thread safety of circuit breaker."""

    def test_concurrent_record_failure(self) -> None:
        """Test that concurrent failures are counted correctly."""
        import concurrent.futures

        breaker = OTLPCircuitBreaker(failure_threshold=100)

        def record_failures() -> None:
            for _ in range(10):
                breaker.record_failure()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(record_failures) for _ in range(5)]
            for future in concurrent.futures.as_completed(futures):
                future.result()

        assert breaker.get_stats()["failure_count"] == 50

    def test_concurrent_can_attempt_and_record(self) -> None:
        """Test concurrent calls to can_attempt and record methods."""
        import concurrent.futures

        breaker = OTLPCircuitBreaker(failure_threshold=10)

        def worker() -> int:
            attempts = 0
            for _ in range(10):
                if breaker.can_attempt():
                    attempts += 1
                    if attempts % 2 == 0:
                        breaker.record_success()
                    else:
                        breaker.record_failure()
            return attempts

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(worker) for _ in range(3)]
            for future in concurrent.futures.as_completed(futures):
                # Should not raise any exceptions
                result = future.result()
                assert result >= 0


# 🧱🏗️🔚
