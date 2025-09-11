"""
Thread-safe data structure test fixtures.

Fixtures for thread-safe lists, counters, and other data structures for testing.
"""

import threading
from typing import Any

import pytest


@pytest.fixture
def thread_safe_list():
    """
    Create a thread-safe list for collecting results.

    Returns:
        Thread-safe list implementation.
    """

    class ThreadSafeList:
        def __init__(self):
            self._list = []
            self._lock = threading.Lock()

        def append(self, item: Any):
            """Thread-safe append."""
            with self._lock:
                self._list.append(item)

        def extend(self, items):
            """Thread-safe extend."""
            with self._lock:
                self._list.extend(items)

        def get_all(self) -> list:
            """Get copy of all items."""
            with self._lock:
                return self._list.copy()

        def clear(self):
            """Clear the list."""
            with self._lock:
                self._list.clear()

        def __len__(self) -> int:
            with self._lock:
                return len(self._list)

        def __getitem__(self, index):
            with self._lock:
                return self._list[index]

    return ThreadSafeList()


@pytest.fixture
def thread_safe_counter():
    """
    Create a thread-safe counter.

    Returns:
        Thread-safe counter implementation.
    """

    class ThreadSafeCounter:
        def __init__(self, initial: int = 0):
            self._value = initial
            self._lock = threading.Lock()

        def increment(self, amount: int = 1) -> int:
            """Thread-safe increment."""
            with self._lock:
                self._value += amount
                return self._value

        def decrement(self, amount: int = 1) -> int:
            """Thread-safe decrement."""
            with self._lock:
                self._value -= amount
                return self._value

        @property
        def value(self) -> int:
            """Get current value."""
            with self._lock:
                return self._value

        def reset(self, value: int = 0):
            """Reset counter."""
            with self._lock:
                self._value = value

    return ThreadSafeCounter()


__all__ = [
    "thread_safe_counter",
    "thread_safe_list",
]
