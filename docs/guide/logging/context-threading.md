## Thread-Local Context

### Thread Context Manager

```python
import threading
from contextvars import ContextVar
from typing import Any

# Context variables are thread-safe
request_context: ContextVar[dict[str, Any]] = ContextVar(
    "request_context",
    default={}
)

class ThreadLocalLogger:
    """Logger with thread-local context."""
    
    @staticmethod
    def bind(**kwargs) -> None:
        """Add to thread-local context."""
        current = request_context.get()
        updated = {**current, **kwargs}
        request_context.set(updated)
    
    @staticmethod
    def unbind(*keys) -> None:
        """Remove from thread-local context."""
        current = request_context.get()
        updated = {k: v for k, v in current.items() if k not in keys}
        request_context.set(updated)
    
    @staticmethod
    def log(level: str, event: str, **kwargs):
        """Log with thread-local context."""
        context = request_context.get()
        merged = {**context, **kwargs}
        getattr(logger, level)(event, **merged)

# Usage in threaded application
def worker_thread(worker_id: int):
    """Worker with its own context."""
    ThreadLocalLogger.bind(worker_id=worker_id)
    
    for task in get_tasks():
        ThreadLocalLogger.bind(task_id=task.id)
        ThreadLocalLogger.log("info", "task_started")
        
        process_task(task)
        
        ThreadLocalLogger.log("info", "task_completed")
        ThreadLocalLogger.unbind("task_id")

# Start workers
threads = [
    threading.Thread(target=worker_thread, args=(i,))
    for i in range(4)
]
for t in threads:
    t.start()
```

### Async Context Variables

```python
import asyncio
from contextvars import ContextVar

# Context variables work across async boundaries
trace_context: ContextVar[str] = ContextVar("trace_id")

async def process_with_context(trace_id: str):
    """Process with trace context."""
    trace_context.set(trace_id)
    
    # Context is preserved across await
    await logger.ainfo("processing_started", 
                      trace_id=trace_context.get())
    
    # Even across task boundaries
    await asyncio.gather(
        subtask_a(),
        subtask_b(),
        subtask_c()
    )

async def subtask_a():
    """Subtask automatically has trace context."""
    trace_id = trace_context.get()
    await logger.ainfo("subtask_a_executed", trace_id=trace_id)
```

