# Custom Log Processors

Extend the logging pipeline with custom processing to add metadata, filter data, collect statistics, and trigger actions.

## Creating Custom Processors

```python
import time
import threading
from typing import Any
from provide.foundation.logger import add_processor

def performance_processor(logger, method_name, event_dict):
    """Add performance timing information to logs."""
    # Add processing timestamp
    event_dict["processed_at"] = time.time()
    
    # Add thread information
    event_dict["thread_id"] = threading.get_ident()
    event_dict["thread_name"] = threading.current_thread().name
    
    # Calculate processing time if available
    if "start_time" in event_dict:
        duration = time.time() - event_dict["start_time"]
        event_dict["duration_seconds"] = round(duration, 6)
        del event_dict["start_time"]  # Remove intermediate timing
    
    return event_dict

def request_correlation_processor(logger, method_name, event_dict):
    """Add request correlation ID to logs."""
    import contextvars
    
    # Get correlation ID from context (set by middleware)
    correlation_id = getattr(contextvars.copy_context(), 'correlation_id', None)
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    
    return event_dict

def sensitive_data_processor(logger, method_name, event_dict):
    """Remove or mask sensitive data from logs."""
    sensitive_fields = [
        "password", "token", "secret", "key", "authorization",
        "cookie", "session", "credit_card", "ssn", "email"
    ]
    
    def mask_sensitive(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if any(sensitive in key.lower() for sensitive in sensitive_fields):
                    obj[key] = "[REDACTED]"
                elif isinstance(value, (dict, list)):
                    mask_sensitive(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    mask_sensitive(item, f"{path}[{i}]")
        return obj
    
    return mask_sensitive(event_dict)

# Register processors
add_processor(performance_processor)
add_processor(request_correlation_processor)
add_processor(sensitive_data_processor)

# Usage example
from provide.foundation import get_logger
log = get_logger(__name__)

log.info("Processing request", 
         start_time=time.time(),
         user_data={"username": "john", "password": "secret123"},
         request_id="abc-123")
```

## Advanced Processor Patterns

```python
class StatisticsProcessor:
    """Processor that collects logging statistics."""
    
    def __init__(self):
        self.stats = {
            "total_logs": 0,
            "by_level": {},
            "by_logger": {},
            "errors": 0
        }
    
    def __call__(self, logger, method_name, event_dict):
        """Process log entry and collect statistics."""
        self.stats["total_logs"] += 1
        
        level = event_dict.get("level", "unknown")
        self.stats["by_level"][level] = self.stats["by_level"].get(level, 0) + 1
        
        logger_name = event_dict.get("logger", "unknown")
        self.stats["by_logger"][logger_name] = self.stats["by_logger"].get(logger_name, 0) + 1
        
        if level in ("error", "critical"):
            self.stats["errors"] += 1
        
        return event_dict
    
    def get_stats(self):
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            "total_logs": 0,
            "by_level": {},
            "by_logger": {},
            "errors": 0
        }

class AlertingProcessor:
    """Processor that triggers alerts for critical logs."""
    
    def __init__(self, alert_callback=None, alert_levels=None):
        self.alert_callback = alert_callback or self.default_alert
        self.alert_levels = alert_levels or {"critical", "error"}
        self.alert_count = 0
    
    def __call__(self, logger, method_name, event_dict):
        level = event_dict.get("level", "").lower()
        
        if level in self.alert_levels:
            self.alert_count += 1
            try:
                self.alert_callback(event_dict)
            except Exception as e:
                # Don't fail logging if alerting fails
                print(f"Alert failed: {e}")
        
        return event_dict
    
    def default_alert(self, event_dict):
        """Default alert implementation."""
        print(f"🚨 ALERT: {event_dict.get('event', 'Unknown error')}")

# Usage
stats_processor = StatisticsProcessor()
alert_processor = AlertingProcessor()

add_processor(stats_processor)
add_processor(alert_processor)

# Later, check statistics
stats = stats_processor.get_stats()
print(f"Total logs: {stats['total_logs']}")
print(f"Errors: {stats['errors']}")
```

## Thread Safety and Concurrency

### Advanced Concurrent Patterns

```python
import asyncio
import threading
import concurrent.futures
from contextlib import contextmanager
from provide.foundation import get_logger

class ThreadSafeLoggerPool:
    """Pool of thread-local loggers for high-concurrency scenarios."""
    
    def __init__(self, base_name: str):
        self.base_name = base_name
        self.local = threading.local()
    
    def get_logger(self):
        """Get thread-local logger."""
        if not hasattr(self.local, 'logger'):
            thread_id = threading.get_ident()
            self.local.logger = get_logger(f"{self.base_name}.thread_{thread_id}")
        return self.local.logger

# Usage with thread pool
logger_pool = ThreadSafeLoggerPool("worker")

def worker_function(task_id: int):
    """Worker function that uses thread-local logger."""
    log = logger_pool.get_logger()
    
    log.info("Task started", task_id=task_id, thread_id=threading.get_ident())
    
    # Simulate work
    time.sleep(0.1)
    
    log.info("Task completed", task_id=task_id)
    return f"Task {task_id} completed"

# Run tasks concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(worker_function, i) for i in range(50)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

@contextmanager
def logging_context(**kwargs):
    """Context manager for adding context to all logs in a block."""
    log = get_logger(__name__)
    bound_logger = log.bind(**kwargs)
    
    # Store in thread-local storage
    if not hasattr(threading.current_thread(), 'context_logger'):
        threading.current_thread().context_logger = []
    
    threading.current_thread().context_logger.append(bound_logger)
    
    try:
        yield bound_logger
    finally:
        threading.current_thread().context_logger.pop()

def get_context_logger():
    """Get the current context logger."""
    if (hasattr(threading.current_thread(), 'context_logger') and 
        threading.current_thread().context_logger):
        return threading.current_thread().context_logger[-1]
    return get_logger(__name__)

# Usage
with logging_context(request_id="abc-123", user_id=456):
    log = get_context_logger()
    log.info("Processing request")  # Includes request_id and user_id
    
    with logging_context(operation="database"):
        log = get_context_logger()
        log.info("Executing query")  # Includes all context
```

### Async Logging Patterns

```python
import asyncio
from typing import AsyncContextManager
from provide.foundation import get_logger

class AsyncLoggingContext:
    """Async context manager for structured logging contexts."""
    
    def __init__(self, logger_name: str, **context):
        self.logger = get_logger(logger_name)
        self.context = context
        self.start_time = None
    
    async def __aenter__(self):
        self.start_time = time.time()
        self.logger.info("Context started", **self.context)
        return self.logger.bind(**self.context)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        
        if exc_type:
            self.logger.error("Context failed", 
                            exception=str(exc_val),
                            duration_seconds=duration,
                            **self.context)
        else:
            self.logger.info("Context completed",
                           duration_seconds=duration,
                           **self.context)

async def async_operation_with_logging():
    """Example async operation with structured logging."""
    async with AsyncLoggingContext("async_ops", operation="data_processing", batch_id="batch_123") as log:
        
        # Simulate async work with logging
        await asyncio.sleep(0.1)
        log.info("Phase 1 completed", phase="validation")
        
        await asyncio.sleep(0.1) 
        log.info("Phase 2 completed", phase="transformation")
        
        await asyncio.sleep(0.1)
        log.info("Phase 3 completed", phase="persistence")

# Run multiple operations concurrently
async def run_concurrent_operations():
    tasks = [
        async_operation_with_logging() 
        for _ in range(10)
    ]
    await asyncio.gather(*tasks)

# asyncio.run(run_concurrent_operations())
```