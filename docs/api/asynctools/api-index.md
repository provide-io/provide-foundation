# Async Tools API

Asynchronous utilities and helpers for building robust async applications with provide-foundation.

## Overview

The `asynctools` module provides utilities specifically designed for asynchronous programming patterns, including async context management, task coordination, and async-aware logging integration.

## Key Features

- **Async Context Management**: Context managers for async operations
- **Task Coordination**: Utilities for managing concurrent tasks
- **Async Logging Integration**: Seamless integration with structured logging
- **Resource Management**: Async resource lifecycle management
- **Error Handling**: Async-aware error handling patterns

## Basic Usage

### Async Context Managers

```python
import asyncio
from provide.foundation.asynctools import async_context, timeout_context

async def main():
    # Async context with automatic cleanup
    async with async_context("database_operation") as ctx:
        # Context automatically logs start/end and handles cleanup
        result = await perform_database_query()
        ctx.add_metadata(rows_processed=len(result))
    
    # Timeout context for operations
    async with timeout_context(30.0) as ctx:
        # Operation will be cancelled after 30 seconds
        await long_running_operation()
```

### Task Management

```python
from provide.foundation.asynctools import TaskManager, gather_with_concurrency

async def process_items():
    # Manage concurrent tasks with limits
    async with TaskManager(max_concurrent=10) as manager:
        tasks = []
        for item in items:
            task = manager.create_task(process_item(item))
            tasks.append(task)
        
        results = await manager.gather(*tasks)
    
    # Gather with concurrency limiting
    results = await gather_with_concurrency(
        *[process_item(item) for item in items],
        limit=5
    )
```

## Context Management

### Async Operation Context

```python
from provide.foundation.asynctools import AsyncOperationContext
from provide.foundation import logger

async def perform_operation():
    async with AsyncOperationContext("data_processing") as ctx:
        # Context automatically logs operation start
        logger.info("processing_data", operation_id=ctx.operation_id)
        
        try:
            result = await process_data()
            ctx.success(result_count=len(result))
            return result
        except Exception as e:
            ctx.error(error=str(e))
            raise
        # Context automatically logs operation completion/failure
```

### Resource Management

```python
from provide.foundation.asynctools import AsyncResourceManager

class DatabaseConnection:
    async def connect(self):
        # Async connection logic
        pass
    
    async def close(self):
        # Async cleanup logic
        pass

async def use_database():
    resource_manager = AsyncResourceManager()
    
    # Automatically managed async resource
    async with resource_manager.manage(DatabaseConnection()) as db:
        await db.connect()
        result = await db.query("SELECT * FROM users")
        # db.close() called automatically
        return result
```

## Task Coordination

### Concurrent Task Execution

```python
from provide.foundation.asynctools import ConcurrentExecutor

async def process_batch():
    executor = ConcurrentExecutor(max_workers=5)
    
    # Execute tasks concurrently with result tracking
    async with executor:
        results = await executor.map(
            process_item,
            items,
            progress_callback=lambda completed, total: 
                logger.info("batch_progress", completed=completed, total=total)
        )
    
    return results
```

### Task Pool Management

```python
from provide.foundation.asynctools import TaskPool

async def worker_pool_example():
    async with TaskPool(pool_size=10, queue_size=100) as pool:
        # Submit work to the pool
        for work_item in work_queue:
            await pool.submit(process_work_item, work_item)
        
        # Wait for all work to complete
        results = await pool.gather_results()
    
    return results
```

## Async Logging Integration

### Structured Async Logging

```python
from provide.foundation.asynctools import async_logger
from provide.foundation import logger

@async_logger("api_request")
async def handle_request(request_data):
    """Decorator automatically logs async function entry/exit."""
    # Function execution is automatically traced
    result = await process_request(request_data)
    return result

# Manual async logging context
async def manual_logging():
    async with logger.async_context("background_task") as log_ctx:
        log_ctx.info("task_started", task_id="task_123")
        
        await asyncio.sleep(1)
        
        log_ctx.info("task_progress", progress=0.5)
        
        await asyncio.sleep(1)
        
        log_ctx.info("task_completed", status="success")
```

### Async Event Tracking

```python
from provide.foundation.asynctools import AsyncEventTracker

async def track_events():
    tracker = AsyncEventTracker()
    
    # Track async events with timing
    async with tracker.track("data_download") as event:
        data = await download_large_file()
        event.add_metadata(size_bytes=len(data))
    
    # Get tracked events
    events = tracker.get_events()
    logger.info("event_summary", events=events)
```

## Error Handling

### Async Error Boundaries

```python
from provide.foundation.asynctools import async_error_boundary
from provide.foundation import logger

@async_error_boundary(
    fallback=lambda: "default_response",
    log_errors=True,
    retry_count=3
)
async def risky_operation():
    """Operation with automatic error handling and retries."""
    result = await external_api_call()
    return result

# Manual error boundary
async def manual_error_handling():
    async with async_error_boundary() as boundary:
        try:
            result = await risky_operation()
            boundary.success(result)
        except SpecificError as e:
            boundary.handle_error(e, recoverable=True)
            result = await fallback_operation()
        except Exception as e:
            boundary.handle_error(e, recoverable=False)
            raise
```

### Retry Mechanisms

```python
from provide.foundation.asynctools import async_retry

@async_retry(max_attempts=3, delay=1.0, backoff=2.0)
async def unreliable_operation():
    """Automatically retries on failure with exponential backoff."""
    result = await external_service_call()
    return result

# Manual retry with custom conditions
async def custom_retry():
    from provide.foundation.asynctools import AsyncRetryManager
    
    retry_manager = AsyncRetryManager(
        max_attempts=5,
        delay=0.5,
        should_retry=lambda e: isinstance(e, TemporaryError)
    )
    
    async with retry_manager:
        result = await potentially_failing_operation()
        return result
```

## Performance Utilities

### Async Batching

```python
from provide.foundation.asynctools import AsyncBatcher

async def batch_processing():
    batcher = AsyncBatcher(batch_size=100, flush_interval=5.0)
    
    # Automatically batches items for efficient processing
    async with batcher:
        for item in data_stream:
            await batcher.add(item)
            
        # Process any remaining items
        await batcher.flush()
```

### Async Caching

```python
from provide.foundation.asynctools import async_cache

@async_cache(ttl=300)  # 5-minute cache
async def expensive_operation(param: str):
    """Result is cached for subsequent calls."""
    result = await compute_expensive_result(param)
    return result

# Manual cache management
from provide.foundation.asynctools import AsyncCache

cache = AsyncCache(max_size=1000, ttl=600)

async def cached_lookup(key: str):
    result = await cache.get(key)
    if result is None:
        result = await fetch_data(key)
        await cache.set(key, result)
    return result
```

## Testing Support

### Async Test Utilities

```python
from provide.foundation.asynctools import AsyncTestCase, mock_async

class TestAsyncOperations(AsyncTestCase):
    async def test_async_operation(self):
        # Test async operations with proper setup/teardown
        result = await my_async_function()
        self.assertEqual(result, expected_value)
    
    async def test_with_mocks(self):
        with mock_async("external_service_call") as mock_call:
            mock_call.return_value = "mocked_response"
            
            result = await function_using_external_service()
            self.assertEqual(result, "expected_result")
```

### Async Context Testing

```python
from provide.foundation.asynctools import AsyncContextTester

async def test_context_behavior():
    tester = AsyncContextTester()
    
    # Test async context managers
    async with tester.test_context(my_async_context_manager()):
        # Verify context behavior
        assert tester.context_entered
        await perform_operations()
    
    # Verify cleanup occurred
    assert tester.context_exited
    assert tester.cleanup_performed
```

## Integration Patterns

### With FastAPI

```python
from fastapi import FastAPI
from provide.foundation.asynctools import async_middleware

app = FastAPI()

@async_middleware(app)
async def logging_middleware(request, call_next):
    async with async_context("http_request") as ctx:
        ctx.add_metadata(
            method=request.method,
            path=request.url.path
        )
        
        response = await call_next(request)
        
        ctx.add_metadata(status_code=response.status_code)
        return response
```

### With Background Tasks

```python
import asyncio
from provide.foundation.asynctools import BackgroundTaskManager

async def main():
    task_manager = BackgroundTaskManager()
    
    # Start background tasks
    await task_manager.start_task("data_sync", sync_data_periodically, interval=3600)
    await task_manager.start_task("cleanup", cleanup_old_files, interval=86400)
    
    # Run main application
    try:
        await run_main_application()
    finally:
        # Gracefully shutdown background tasks
        await task_manager.shutdown()
```

## Best Practices

### Context Management
```python
# Always use context managers for resource cleanup
async with async_context("operation") as ctx:
    # Operation code here
    pass

# Prefer context managers over manual resource management
async with AsyncResourceManager() as resources:
    db = await resources.get_database()
    cache = await resources.get_cache()
    # Automatic cleanup
```

### Error Handling
```python
# Use error boundaries for critical operations
@async_error_boundary(fallback=safe_fallback)
async def critical_operation():
    return await risky_external_call()

# Log errors with structured data
try:
    result = await operation()
except Exception as e:
    logger.error("operation_failed",
                error=str(e),
                error_type=type(e).__name__,
                operation="specific_operation")
    raise
```

### Performance
```python
# Use concurrency limiting to prevent resource exhaustion
async with TaskManager(max_concurrent=10) as manager:
    tasks = [manager.create_task(work(item)) for item in items]
    results = await manager.gather(*tasks)

# Cache expensive async operations
@async_cache(ttl=300)
async def expensive_computation(params):
    return await compute_result(params)
```

## API Reference

::: provide.foundation.asynctools

## Related Documentation

- [Logging Guide](../../guide/logging/async.md) - Async logging patterns
- [Performance Guide](../../guide/concepts/performance.md) - Async performance considerations
- [Error Handling](../errors/api-index.md) - Error handling utilities
- [Context API](../context/api-index.md) - Context management