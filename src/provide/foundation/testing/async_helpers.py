"""
Async Test Helpers and Fixtures.

Utilities for testing async code, managing event loops, and handling
async subprocess mocking across the provide-io ecosystem.
"""

import asyncio
from unittest.mock import AsyncMock, Mock
from collections.abc import AsyncGenerator, Callable

import pytest


@pytest.fixture
async def clean_event_loop() -> AsyncGenerator[None, None]:
    """
    Ensure clean event loop for async tests.
    
    Cancels all pending tasks after the test to prevent event loop issues.
    
    Yields:
        None - fixture for test setup/teardown.
    """
    yield
    
    # Clean up any pending tasks
    loop = asyncio.get_event_loop()
    pending = asyncio.all_tasks(loop)
    
    for task in pending:
        if not task.done():
            task.cancel()
    
    # Wait for all tasks to complete cancellation
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)


@pytest.fixture
def async_timeout() -> Callable[[float], asyncio.Task]:
    """
    Provide configurable timeout wrapper for async operations.
    
    Returns:
        A function that wraps async operations with a timeout.
    """
    def _timeout_wrapper(coro, seconds: float = 5.0):
        """
        Wrap a coroutine with a timeout.
        
        Args:
            coro: Coroutine to wrap
            seconds: Timeout in seconds
            
        Returns:
            Result of the coroutine or raises asyncio.TimeoutError
        """
        return asyncio.wait_for(coro, timeout=seconds)
    
    return _timeout_wrapper


@pytest.fixture
def mock_async_process() -> AsyncMock:
    """
    Mock async subprocess for testing.
    
    Returns:
        AsyncMock configured as a subprocess with common attributes.
    """
    mock_process = AsyncMock()
    mock_process.communicate = AsyncMock(return_value=(b"output", b""))
    mock_process.returncode = 0
    mock_process.pid = 12345
    mock_process.stdin = AsyncMock()
    mock_process.stdout = AsyncMock()
    mock_process.stderr = AsyncMock()
    mock_process.wait = AsyncMock(return_value=0)
    mock_process.kill = Mock()
    mock_process.terminate = Mock()
    
    return mock_process


@pytest.fixture
async def async_stream_reader() -> AsyncMock:
    """
    Mock async stream reader for subprocess stdout/stderr.
    
    Returns:
        AsyncMock configured as a stream reader.
    """
    reader = AsyncMock()
    
    # Simulate reading lines
    async def readline_side_effect():
        for line in [b"line1\n", b"line2\n", b""]:
            yield line
    
    reader.readline = AsyncMock(side_effect=readline_side_effect().__anext__)
    reader.read = AsyncMock(return_value=b"full content")
    reader.at_eof = Mock(side_effect=[False, False, True])
    
    return reader


@pytest.fixture
def event_loop_policy():
    """
    Set event loop policy for tests to avoid conflicts.
    
    Returns:
        New event loop policy for isolated testing.
    """
    policy = asyncio.get_event_loop_policy()
    new_policy = asyncio.DefaultEventLoopPolicy()
    asyncio.set_event_loop_policy(new_policy)
    
    yield new_policy
    
    # Restore original policy
    asyncio.set_event_loop_policy(policy)


@pytest.fixture
async def async_context_manager():
    """
    Factory for creating mock async context managers.
    
    Returns:
        Function that creates configured async context manager mocks.
    """
    def _create_async_cm(enter_value=None, exit_value=None):
        """
        Create a mock async context manager.
        
        Args:
            enter_value: Value to return from __aenter__
            exit_value: Value to return from __aexit__
            
        Returns:
            AsyncMock configured as context manager
        """
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(return_value=enter_value)
        mock_cm.__aexit__ = AsyncMock(return_value=exit_value)
        return mock_cm
    
    return _create_async_cm


@pytest.fixture
async def async_iterator():
    """
    Factory for creating mock async iterators.
    
    Returns:
        Function that creates async iterator mocks with specified values.
    """
    def _create_async_iter(values):
        """
        Create a mock async iterator.
        
        Args:
            values: List of values to yield
            
        Returns:
            Async iterator that yields the specified values
        """
        class AsyncIterator:
            def __init__(self, vals):
                self.vals = vals
                self.index = 0
            
            def __aiter__(self):
                return self
            
            async def __anext__(self):
                if self.index >= len(self.vals):
                    raise StopAsyncIteration
                value = self.vals[self.index]
                self.index += 1
                return value
        
        return AsyncIterator(values)
    
    return _create_async_iter


@pytest.fixture
def async_queue():
    """
    Create an async queue for testing producer/consumer patterns.
    
    Returns:
        asyncio.Queue instance for testing.
    """
    return asyncio.Queue()


@pytest.fixture
async def async_lock():
    """
    Create an async lock for testing synchronization.
    
    Returns:
        asyncio.Lock instance for testing.
    """
    return asyncio.Lock()


@pytest.fixture
def mock_async_sleep():
    """
    Mock asyncio.sleep to speed up tests.
    
    Returns:
        Mock that replaces asyncio.sleep with instant return.
    """
    original_sleep = asyncio.sleep
    
    async def instant_sleep(seconds):
        """Sleep replacement that returns immediately."""
        return None
    
    asyncio.sleep = instant_sleep
    
    yield instant_sleep
    
    # Restore original
    asyncio.sleep = original_sleep