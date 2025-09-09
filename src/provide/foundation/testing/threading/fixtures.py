"""
Threading Test Fixtures and Utilities.

Fixtures for testing multi-threaded code, thread synchronization,
and concurrent operations across the provide-io ecosystem.
"""

import threading
import time
import queue
from typing import Any, Callable, Optional
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
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
    
    def _create_thread(target: Callable, args: tuple = (), kwargs: dict = None, daemon: bool = True) -> threading.Thread:
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
def thread_barrier():
    """
    Create a barrier for thread synchronization.
    
    Returns:
        Function to create barriers for N threads.
    """
    barriers = []
    
    def _create_barrier(n_threads: int, timeout: Optional[float] = None) -> threading.Barrier:
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
    def _create_condition(lock: Optional[threading.Lock] = None) -> threading.Condition:
        """
        Create a condition variable.
        
        Args:
            lock: Optional lock to use (creates new if None)
            
        Returns:
            Condition variable
        """
        return threading.Condition(lock)
    
    return _create_condition


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
        
        def checkpoint(self, name: str, thread_id: Optional[int] = None):
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
        
        def acquire(self, lock_name: str, thread_id: Optional[int] = None):
            """Record lock acquisition."""
            thread_id = thread_id or threading.get_ident()
            with self.lock:
                if thread_id not in self.locks_held:
                    self.locks_held[thread_id] = set()
                self.locks_held[thread_id].add(lock_name)
        
        def release(self, lock_name: str, thread_id: Optional[int] = None):
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
                multi_lock_threads = [
                    tid for tid, locks in self.locks_held.items()
                    if len(locks) > 1
                ]
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
                        self.exceptions.append({
                            'thread': threading.current_thread().name,
                            'exception': e,
                            'time': time.time()
                        })
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
    "test_thread",
    "thread_pool",
    "thread_barrier",
    "thread_safe_list",
    "thread_safe_counter",
    "thread_event",
    "thread_condition",
    "mock_thread",
    "thread_local_storage",
    "concurrent_executor",
    "thread_synchronizer",
    "deadlock_detector",
    "thread_exception_handler",
]