"""
Async-specific test fixtures for process testing.

Provides fixtures for testing async operations, event loops, and 
async context management across the provide-io ecosystem.
"""

import asyncio
from unittest.mock import AsyncMock
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


@pytest.fixture
def async_gather_helper():
    """
    Helper for testing asyncio.gather operations.
    
    Returns:
        Function to gather async results with error handling.
    """
    async def _gather(*coroutines, return_exceptions: bool = False):
        """
        Gather results from multiple coroutines.
        
        Args:
            *coroutines: Coroutines to gather
            return_exceptions: Whether to return exceptions as results
            
        Returns:
            List of results from coroutines
        """
        return await asyncio.gather(*coroutines, return_exceptions=return_exceptions)
    
    return _gather


@pytest.fixture
def async_task_group():
    """
    Manage a group of async tasks with cleanup.
    
    Returns:
        AsyncTaskGroup instance for managing tasks.
    """
    class AsyncTaskGroup:
        def __init__(self):
            self.tasks = []
        
        def create_task(self, coro):
            """Create and track a task."""
            task = asyncio.create_task(coro)
            self.tasks.append(task)
            return task
        
        async def wait_all(self, timeout: float = None):
            """Wait for all tasks to complete."""
            if not self.tasks:
                return []
            
            done, pending = await asyncio.wait(
                self.tasks,
                timeout=timeout,
                return_when=asyncio.ALL_COMPLETED
            )
            
            if pending:
                for task in pending:
                    task.cancel()
            
            results = []
            for task in done:
                try:
                    results.append(task.result())
                except Exception as e:
                    results.append(e)
            
            return results
        
        async def cancel_all(self):
            """Cancel all tasks."""
            for task in self.tasks:
                if not task.done():
                    task.cancel()
            
            if self.tasks:
                await asyncio.gather(*self.tasks, return_exceptions=True)
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            await self.cancel_all()
    
    return AsyncTaskGroup()


@pytest.fixture
def async_condition_waiter():
    """
    Helper for waiting on async conditions in tests.
    
    Returns:
        Function to wait for conditions with timeout.
    """
    async def _wait_for(condition: Callable[[], bool], timeout: float = 5.0, interval: float = 0.1):
        """
        Wait for a condition to become true.
        
        Args:
            condition: Function that returns True when condition is met
            timeout: Maximum wait time
            interval: Check interval
            
        Returns:
            True if condition met, False if timeout
        """
        start = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start < timeout:
            if condition():
                return True
            await asyncio.sleep(interval)
        
        return False
    
    return _wait_for


@pytest.fixture
def async_pipeline():
    """
    Create an async pipeline for testing data flow.
    
    Returns:
        AsyncPipeline instance for chaining async operations.
    """
    class AsyncPipeline:
        def __init__(self):
            self.stages = []
            self.results = []
        
        def add_stage(self, func: Callable):
            """Add a processing stage."""
            self.stages.append(func)
            return self
        
        async def process(self, data):
            """Process data through all stages."""
            result = data
            for stage in self.stages:
                if asyncio.iscoroutinefunction(stage):
                    result = await stage(result)
                else:
                    result = stage(result)
                self.results.append(result)
            return result
        
        async def process_batch(self, items: list):
            """Process multiple items."""
            tasks = [self.process(item) for item in items]
            return await asyncio.gather(*tasks)
        
        def clear(self):
            """Clear stages and results."""
            self.stages.clear()
            self.results.clear()
    
    return AsyncPipeline()


@pytest.fixture
def async_rate_limiter():
    """
    Create an async rate limiter for testing.
    
    Returns:
        AsyncRateLimiter instance for controlling request rates.
    """
    class AsyncRateLimiter:
        def __init__(self, rate: int = 10, per: float = 1.0):
            self.rate = rate
            self.per = per
            self.allowance = rate
            self.last_check = asyncio.get_event_loop().time()
        
        async def acquire(self):
            """Acquire permission to proceed."""
            current = asyncio.get_event_loop().time()
            time_passed = current - self.last_check
            self.last_check = current
            
            self.allowance += time_passed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate
            
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0
        
        async def __aenter__(self):
            await self.acquire()
            return self
        
        async def __aexit__(self, *args):
            pass
    
    return AsyncRateLimiter()


__all__ = [
    "clean_event_loop",
    "async_timeout", 
    "event_loop_policy",
    "async_context_manager",
    "async_iterator",
    "async_queue",
    "async_lock",
    "mock_async_sleep",
    "async_gather_helper",
    "async_task_group", 
    "async_condition_waiter",
    "async_pipeline",
    "async_rate_limiter",
]