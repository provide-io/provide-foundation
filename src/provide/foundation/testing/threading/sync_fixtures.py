"""
Thread synchronization test fixtures.

Fixtures for thread barriers, events, conditions, and other synchronization primitives.
"""

import threading

import pytest


@pytest.fixture
def thread_barrier():
    """
    Create a barrier for thread synchronization.

    Returns:
        Function to create barriers for N threads.
    """
    barriers = []

    def _create_barrier(n_threads: int, timeout: float | None = None) -> threading.Barrier:
        """
        Create a barrier for synchronizing threads.

        Args:
            n_threads: Number of threads to synchronize
            timeout: Optional timeout for barrier

        Returns:
            Barrier instance
        """
        barrier = threading.Barrier(n_threads, timeout=timeout)
        barriers.append(barrier)
        return barrier

    yield _create_barrier

    # Cleanup: abort all barriers
    for barrier in barriers:
        try:
            barrier.abort()
        except threading.BrokenBarrierError:
            pass


@pytest.fixture
def thread_event():
    """
    Create thread events for signaling.

    Returns:
        Function to create thread events.
    """
    events = []

    def _create_event() -> threading.Event:
        """Create a thread event."""
        event = threading.Event()
        events.append(event)
        return event

    yield _create_event

    # Cleanup: set all events to release waiting threads
    for event in events:
        event.set()


@pytest.fixture
def thread_condition():
    """
    Create condition variables for thread coordination.

    Returns:
        Function to create condition variables.
    """

    def _create_condition(lock: threading.Lock | None = None) -> threading.Condition:
        """
        Create a condition variable.

        Args:
            lock: Optional lock to use (creates new if None)

        Returns:
            Condition variable
        """
        return threading.Condition(lock)

    return _create_condition


__all__ = [
    "thread_barrier",
    "thread_condition",
    "thread_event",
]
