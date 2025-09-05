# Async Logging

Asynchronous logging support in provide.foundation applications.

## Overview

provide.foundation's logger is fully thread-safe and async-compatible, maintaining the same logging interface whether used in synchronous or asynchronous contexts. The logger handles async operations seamlessly without requiring special async methods.

## Basic Async Usage

### In Async Functions

Use the logger normally within async functions:

```python
import asyncio
from provide.foundation import logger

async def fetch_data(url: str):
    """Async function with logging."""
    logger.info("Starting fetch", url=url)
    
    try:
        # Simulate async operation
        await asyncio.sleep(1)
        result = {"data": "example"}
        
        logger.info("Fetch successful", 
                   url=url, 
                   size=len(str(result)))
        return result
        
    except Exception as e:
        logger.error("Fetch failed", 
                    url=url, 
                    error=str(e),
                    exc_info=True)
        raise
```

### Concurrent Logging

Logger is thread-safe for concurrent operations:

```python
async def process_items(items):
    """Process items concurrently with logging."""
    
    async def process_one(item):
        logger.info("Processing item", item_id=item.id)
        # Process...
        logger.info("Item complete", item_id=item.id)
        
    # Run concurrently - logger handles it safely
    tasks = [process_one(item) for item in items]
    results = await asyncio.gather(*tasks)
    
    logger.info("Batch complete", count=len(results))
    return results
```

## Context Management

### Async Context Variables

Use context variables for request-scoped logging:

```python
import contextvars
from provide.foundation import logger

request_id = contextvars.ContextVar("request_id", default=None)

async def handle_request(req_id: str):
    """Handle request with context."""
    # Set context for this async task
    token = request_id.set(req_id)
    
    try:
        # All logs in this context include request_id
        bound_logger = logger.bind(request_id=req_id)
        bound_logger.info("Request started")
        
        await process_request()
        
        bound_logger.info("Request completed")
    finally:
        request_id.reset(token)

async def process_request():
    """Logs automatically include request_id from context."""
    logger.info("Processing", 
               request_id=request_id.get())
```

### Structured Context

Bind context that persists across async calls:

```python
async def api_handler(user_id: str, session_id: str):
    """Handler with structured context."""
    # Create bound logger with context
    log = logger.bind(
        user_id=user_id,
        session_id=session_id,
        handler="api"
    )
    
    log.info("Handler started")
    
    # Pass bound logger to maintain context
    result = await fetch_user_data(log, user_id)
    processed = await process_data(log, result)
    
    log.info("Handler completed", result_size=len(processed))
    return processed

async def fetch_user_data(log, user_id: str):
    """Uses passed logger with context."""
    log.info("Fetching user data")
    # ... fetch logic
    return data
```

## Error Handling

### Async Exception Logging

Proper exception handling in async code:

```python
from provide.foundation import logger
from provide.foundation.errors import with_error_handling

@with_error_handling(
    fallback=None,
    log_errors=True
)
async def risky_operation():
    """Async function with automatic error logging."""
    logger.info("Starting risky operation")
    
    # If this fails, error is logged automatically
    result = await external_api_call()
    
    logger.info("Operation succeeded")
    return result

# Or manual exception logging
async def manual_error_handling():
    try:
        result = await risky_operation()
    except Exception as e:
        # Log with full traceback
        logger.exception("Operation failed",
                        error_type=type(e).__name__)
        # Or without traceback
        logger.error("Operation failed",
                    error=str(e),
                    exc_info=False)
        raise
```

### Async Retry with Logging

Implement retry logic with logging:

```python
from provide.foundation.errors import with_retry

@with_retry(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    log_retries=True
)
async def unstable_operation():
    """Retries with exponential backoff and logging."""
    response = await make_request()
    if not response.ok:
        raise ValueError(f"Request failed: {response.status}")
    return response.data
```

## Performance Considerations

### Non-Blocking Logging

The logger doesn't block the event loop:

```python
async def high_throughput_handler():
    """Logger won't block async operations."""
    
    # These complete immediately
    logger.info("Starting batch")
    
    tasks = []
    for i in range(1000):
        # Logging doesn't slow down task creation
        logger.debug("Creating task", task_id=i)
        tasks.append(process_item(i))
    
    results = await asyncio.gather(*tasks)
    logger.info("Batch complete", count=len(results))
```

### Batched Logging

For high-volume async operations:

```python
class BatchedLogger:
    """Batch log messages for efficiency."""
    
    def __init__(self, flush_interval=1.0, flush_size=100):
        self.messages = []
        self.flush_interval = flush_interval
        self.flush_size = flush_size
        self._task = None
    
    async def log(self, level, message, **kwargs):
        """Add message to batch."""
        self.messages.append({
            "level": level,
            "message": message,
            "kwargs": kwargs,
            "timestamp": time.time()
        })
        
        if len(self.messages) >= self.flush_size:
            await self.flush()
        elif not self._task:
            self._task = asyncio.create_task(self._auto_flush())
    
    async def flush(self):
        """Flush batched messages."""
        if not self.messages:
            return
        
        # Log all at once
        logger.info("Batch log flush", 
                   count=len(self.messages),
                   messages=self.messages)
        self.messages.clear()
    
    async def _auto_flush(self):
        """Auto-flush on interval."""
        await asyncio.sleep(self.flush_interval)
        await self.flush()
        self._task = None
```

## Integration Examples

### With aiohttp

Integration with async web frameworks:

```python
from aiohttp import web
from provide.foundation import logger

async def middleware_factory(app, handler):
    """Logging middleware for aiohttp."""
    
    async def middleware(request):
        # Log request
        log = logger.bind(
            method=request.method,
            path=request.path,
            request_id=request.headers.get("X-Request-ID")
        )
        log.info("Request received")
        
        try:
            # Process request
            response = await handler(request)
            
            # Log response
            log.info("Request completed",
                    status=response.status)
            return response
            
        except web.HTTPException as e:
            log.warning("HTTP exception",
                       status=e.status,
                       reason=e.reason)
            raise
        except Exception as e:
            log.exception("Unhandled error")
            raise

app = web.Application(middlewares=[middleware_factory])
```

### With asyncio Tasks

Track async task execution:

```python
async def task_manager():
    """Manage and log async tasks."""
    
    async def monitored_task(task_id: str, coro):
        """Wrap task with logging."""
        log = logger.bind(task_id=task_id)
        log.info("Task started")
        
        try:
            result = await coro
            log.info("Task completed successfully")
            return result
        except asyncio.CancelledError:
            log.warning("Task cancelled")
            raise
        except Exception as e:
            log.error("Task failed", error=str(e))
            raise
    
    # Create monitored tasks
    tasks = [
        asyncio.create_task(
            monitored_task(f"task-{i}", work_coroutine(i))
        )
        for i in range(10)
    ]
    
    # Wait with timeout
    done, pending = await asyncio.wait(
        tasks, 
        timeout=30.0,
        return_when=asyncio.ALL_COMPLETED
    )
    
    logger.info("Tasks completed",
               done=len(done),
               pending=len(pending))
```

## Best Practices

### 1. Use Bound Loggers

Create bound loggers for request/operation context:

```python
# Good: Bound logger maintains context
async def handle_user_request(user_id, request_id):
    log = logger.bind(user_id=user_id, request_id=request_id)
    log.info("Processing request")
    # Use log throughout this request
```

### 2. Log Task Lifecycle

Track async task start/completion:

```python
# Good: Clear task lifecycle logging
async def background_task(name):
    logger.info(f"Task {name} starting")
    try:
        result = await do_work()
        logger.info(f"Task {name} completed", result=result)
    except Exception as e:
        logger.error(f"Task {name} failed", error=str(e))
```

### 3. Avoid Blocking Operations

Don't block the event loop in logging:

```python
# Bad: Blocking I/O in async context
async def bad_example():
    with open("large_file.txt") as f:
        content = f.read()  # Blocks!
    logger.info("Read file", size=len(content))

# Good: Use async I/O
async def good_example():
    async with aiofiles.open("large_file.txt") as f:
        content = await f.read()
    logger.info("Read file", size=len(content))
```

### 4. Structure Concurrent Logs

Add correlation IDs for concurrent operations:

```python
# Good: Correlation IDs for concurrent work
async def process_batch(items):
    batch_id = str(uuid.uuid4())
    
    async def process_one(item):
        item_log = logger.bind(
            batch_id=batch_id,
            item_id=item.id
        )
        item_log.info("Processing item")
        # Work...
        item_log.info("Item done")
    
    await asyncio.gather(*[process_one(item) for item in items])
```

## Related Topics

- [Basic Usage](basic.md) - Core logging concepts
- [Configuration](config.md) - Logger configuration
- [Exceptions](exceptions.md) - Exception logging patterns