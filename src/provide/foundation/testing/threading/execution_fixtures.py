"""
Thread execution and testing helper fixtures.

Advanced fixtures for concurrent execution, synchronization testing, deadlock detection,
and exception handling in threaded code.
"""

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from typing import Any

import pytest


@pytest.fixture
def concurrent_executor():
    """
    Helper for executing functions concurrently in tests.

    Returns:
        Concurrent execution helper.
    """

    class ConcurrentExecutor:
        def __init__(self):
            self.results = []
            self.exceptions = []

        def run_concurrent(self, func: Callable, args_list: list[tuple], max_workers: int = 4) -> list[Any]:
            """
            Run function concurrently with different arguments.

            Args:
                func: Function to execute
                args_list: List of argument tuples
                max_workers: Maximum concurrent workers

            Returns:
                List of results in order
            """
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for args in args_list:
                    if isinstance(args, tuple):
                        future = executor.submit(func, *args)
                    else:
                        future = executor.submit(func, args)
                    futures.append(future)

                results = []
                for future in futures:
                    try:
                        result = future.result(timeout=10)
                        results.append(result)
                        self.results.append(result)
                    except Exception as e:
                        self.exceptions.append(e)
                        results.append(None)

                return results

        def run_parallel(self, funcs: list[Callable], timeout: float = 10) -> list[Any]:
            """
            Run different functions in parallel.

            Args:
                funcs: List of functions to execute
                timeout: Timeout for each function

            Returns:
                List of results
            """
            with ThreadPoolExecutor(max_workers=len(funcs)) as executor:
                futures = [executor.submit(func) for func in funcs]
                results = []

                for future in futures:
                    try:
                        result = future.result(timeout=timeout)
                        results.append(result)
                    except Exception as e:
                        self.exceptions.append(e)
                        results.append(None)

                return results

    return ConcurrentExecutor()


@pytest.fixture
def thread_synchronizer():
    """
    Helper for synchronizing test threads.

    Returns:
        Thread synchronization helper.
    """

    class ThreadSynchronizer:
        def __init__(self):
            self.checkpoints = {}

        def checkpoint(self, name: str, thread_id: int | None = None):
            """
            Record that a thread reached a checkpoint.

            Args:
                name: Checkpoint name
                thread_id: Optional thread ID (uses current if None)
            """
            thread_id = thread_id or threading.get_ident()
            if name not in self.checkpoints:
                self.checkpoints[name] = []
            self.checkpoints[name].append((thread_id, time.time()))

        def wait_for_checkpoint(self, name: str, count: int, timeout: float = 5.0) -> bool:
            """
            Wait for N threads to reach a checkpoint.

            Args:
                name: Checkpoint name
                count: Number of threads to wait for
                timeout: Maximum wait time

            Returns:
                True if checkpoint reached, False if timeout
            """
            start = time.time()
            while time.time() - start < timeout:
                if name in self.checkpoints and len(self.checkpoints[name]) >= count:
                    return True
                time.sleep(0.01)
            return False

        def get_order(self, checkpoint: str) -> list[int]:
            """
            Get order in which threads reached checkpoint.

            Args:
                checkpoint: Checkpoint name

            Returns:
                List of thread IDs in order
            """
            if checkpoint not in self.checkpoints:
                return []
            return [tid for tid, _ in sorted(self.checkpoints[checkpoint], key=lambda x: x[1])]

        def clear(self):
            """Clear all checkpoints."""
            self.checkpoints.clear()

    return ThreadSynchronizer()


@pytest.fixture
def deadlock_detector():
    """
    Helper for detecting potential deadlocks in tests.

    Returns:
        Deadlock detection helper.
    """

    class DeadlockDetector:
        def __init__(self):
            self.locks_held = {}  # thread_id -> set of locks
            self.lock = threading.Lock()

        def acquire(self, lock_name: str, thread_id: int | None = None):
            """Record lock acquisition."""
            thread_id = thread_id or threading.get_ident()
            with self.lock:
                if thread_id not in self.locks_held:
                    self.locks_held[thread_id] = set()
                self.locks_held[thread_id].add(lock_name)

        def release(self, lock_name: str, thread_id: int | None = None):
            """Record lock release."""
            thread_id = thread_id or threading.get_ident()
            with self.lock:
                if thread_id in self.locks_held:
                    self.locks_held[thread_id].discard(lock_name)

        def check_circular_wait(self) -> bool:
            """
            Check for potential circular wait conditions.

            Returns:
                True if potential deadlock detected
            """
            # Simplified check - in practice would need wait-for graph
            with self.lock:
                # Check if multiple threads hold multiple locks
                multi_lock_threads = [tid for tid, locks in self.locks_held.items() if len(locks) > 1]
                return len(multi_lock_threads) > 1

        def get_held_locks(self) -> dict[int, set[str]]:
            """Get current lock holdings."""
            with self.lock:
                return self.locks_held.copy()

    return DeadlockDetector()


@pytest.fixture
def thread_exception_handler():
    """
    Capture exceptions from threads for testing.

    Returns:
        Exception handler for threads.
    """

    class ThreadExceptionHandler:
        def __init__(self):
            self.exceptions = []
            self.lock = threading.Lock()

        def handle(self, func: Callable) -> Callable:
            """
            Wrap function to capture exceptions.

            Args:
                func: Function to wrap

            Returns:
                Wrapped function
            """

            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    with self.lock:
                        self.exceptions.append(
                            {
                                "thread": threading.current_thread().name,
                                "exception": e,
                                "time": time.time(),
                            }
                        )
                    raise

            return wrapper

        def get_exceptions(self) -> list[dict]:
            """Get all captured exceptions."""
            with self.lock:
                return self.exceptions.copy()

        def assert_no_exceptions(self):
            """Assert no exceptions were raised."""
            with self.lock:
                if self.exceptions:
                    raise AssertionError(f"Thread exceptions occurred: {self.exceptions}")

    return ThreadExceptionHandler()


__all__ = [
    "concurrent_executor",
    "deadlock_detector",
    "thread_exception_handler",
    "thread_synchronizer",
]
