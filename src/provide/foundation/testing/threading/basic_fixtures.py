"""
Basic threading test fixtures.

Core fixtures for creating threads, thread pools, mocks, and thread-local storage.
"""

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
import threading
from unittest.mock import Mock

import pytest


@pytest.fixture
def test_thread():
    """
    Create a test thread with automatic cleanup.

    Returns:
        Function to create and manage test threads.
    """
    threads = []

    def _create_thread(
        target: Callable, args: tuple = (), kwargs: dict = None, daemon: bool = True
    ) -> threading.Thread:
        """
        Create a test thread.

        Args:
            target: Function to run in thread
            args: Positional arguments for target
            kwargs: Keyword arguments for target
            daemon: Whether thread should be daemon

        Returns:
            Started thread instance
        """
        kwargs = kwargs or {}
        thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        threads.append(thread)
        thread.start()
        return thread

    yield _create_thread

    # Cleanup: wait for all threads to complete
    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=1.0)


@pytest.fixture
def thread_pool():
    """
    Create a thread pool executor for testing.

    Returns:
        ThreadPoolExecutor instance with automatic cleanup.
    """
    executor = ThreadPoolExecutor(max_workers=4)
    yield executor
    executor.shutdown(wait=True, cancel_futures=True)


@pytest.fixture
def mock_thread():
    """
    Create a mock thread for testing without actual threading.

    Returns:
        Mock thread object.
    """
    mock = Mock(spec=threading.Thread)
    mock.is_alive.return_value = False
    mock.daemon = False
    mock.name = "MockThread"
    mock.ident = 12345
    mock.start = Mock()
    mock.join = Mock()
    mock.run = Mock()

    return mock


@pytest.fixture
def thread_local_storage():
    """
    Create thread-local storage for testing.

    Returns:
        Thread-local storage object.
    """
    return threading.local()


__all__ = [
    "mock_thread",
    "test_thread",
    "thread_local_storage",
    "thread_pool",
]
