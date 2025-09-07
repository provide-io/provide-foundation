# Optimization Techniques

Configuration and code patterns for maximum logging performance in high-throughput scenarios.

## High-Performance Configuration

### Optimal Settings

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

def setup_high_performance_logging():
    """Configure logging for maximum performance."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            # Use INFO level - avoid DEBUG in production
            default_level="INFO",
            
            # JSON formatter is faster than key_value
            console_formatter="json",
            
            # Disable emoji processing for speed
            das_emoji_prefix_enabled=False,
            logger_name_emoji_prefix_enabled=False,
            
            # Keep timestamps but optimize format
            omit_timestamp=False,
            
            # Reduce noise from verbose libraries
            module_levels={
                "urllib3": "WARNING",
                "requests": "WARNING", 
                "boto3": "WARNING",
                "botocore": "WARNING",
                "asyncio": "WARNING",
            }
        ),
        # Disable telemetry globally if not needed
        globally_disabled=False
    )
    setup_telemetry(config)

# Apply high-performance configuration
setup_high_performance_logging()
```

### Logger Binding Optimization

```python
from provide.foundation import get_logger

# Get base logger once
base_logger = get_logger(__name__)

# EFFICIENT: Create bound logger for request context
def process_request(request_id: str, user_id: int):
    # Bind context once at the start
    request_logger = base_logger.bind(
        request_id=request_id,
        user_id=user_id
    )
    
    # Reuse bound logger throughout request
    request_logger.info("Request started")
    request_logger.info("Validating input")
    request_logger.info("Processing data")
    request_logger.info("Request completed", status=200)

# LESS EFFICIENT: Repeat context in each call
def process_request_inefficient(request_id: str, user_id: int):
    base_logger.info("Request started", request_id=request_id, user_id=user_id)
    base_logger.info("Validating input", request_id=request_id, user_id=user_id) 
    base_logger.info("Processing data", request_id=request_id, user_id=user_id)
    base_logger.info("Request completed", request_id=request_id, user_id=user_id, status=200)
```

## Code-Level Optimizations

### Lazy Evaluation

```python
from provide.foundation import get_logger

logger = get_logger(__name__)

# EFFICIENT: Use lazy evaluation for expensive operations
def process_data(data_items):
    # Only compute expensive values if DEBUG is enabled
    if logger.isEnabledFor("DEBUG"):
        debug_info = {
            "item_count": len(data_items),
            "serialized_size": len(str(data_items)),
            "memory_usage": get_memory_usage(),  # Expensive call
        }
        logger.debug("Processing data", **debug_info)
    
    # Regular processing
    logger.info("Data processing started")
    result = expensive_processing(data_items)
    logger.info("Data processing completed", result_count=len(result))
    return result

# LESS EFFICIENT: Always compute expensive values
def process_data_inefficient(data_items):
    # These calculations happen even if DEBUG is disabled
    debug_info = {
        "item_count": len(data_items),
        "serialized_size": len(str(data_items)),
        "memory_usage": get_memory_usage(),
    }
    logger.debug("Processing data", **debug_info)
```

### Conditional Logging

```python
import os
from provide.foundation import get_logger

logger = get_logger(__name__)

# Check log level before expensive operations
DEBUG_ENABLED = logger.isEnabledFor("DEBUG")
TRACE_ENABLED = logger.isEnabledFor("TRACE")

def high_frequency_operation(item):
    """Operation called thousands of times per second."""
    
    # Fast path - no logging overhead for normal operations
    result = process_item(item)
    
    # Only log if DEBUG is actually enabled
    if DEBUG_ENABLED:
        logger.debug("Item processed", 
                    item_id=item.id,
                    processing_time=result.duration,
                    result_size=len(result.data))
    
    # Extremely detailed logging only when needed
    if TRACE_ENABLED:
        logger.trace("Detailed processing info",
                    item_details=item.to_dict(),
                    intermediate_steps=result.steps,
                    memory_allocated=result.memory_used)
    
    return result
```

### Batch Operations

```python
import asyncio
from collections import deque
from typing import List, Dict, Any
from provide.foundation import get_logger

class BatchLogger:
    """Logger that batches messages for high-volume scenarios."""
    
    def __init__(self, logger, batch_size: int = 100, flush_interval: float = 5.0):
        self.logger = logger
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch: deque = deque()
        self.last_flush = asyncio.get_event_loop().time()
        self._lock = asyncio.Lock()
        self._flush_task = None
        
    async def start(self):
        """Start the batch flush task."""
        self._flush_task = asyncio.create_task(self._periodic_flush())
    
    async def stop(self):
        """Stop and flush remaining messages."""
        if self._flush_task:
            self._flush_task.cancel()
        await self._flush()
    
    async def log(self, level: str, message: str, **kwargs):
        """Add log entry to batch."""
        entry = {
            "level": level,
            "message": message,
            "timestamp": asyncio.get_event_loop().time(),
            **kwargs
        }
        
        async with self._lock:
            self.batch.append(entry)
            
            # Flush if batch is full
            if len(self.batch) >= self.batch_size:
                await self._flush()
    
    async def _flush(self):
        """Flush the current batch."""
        if not self.batch:
            return
        
        # Get batch and clear
        async with self._lock:
            batch_copy = list(self.batch)
            self.batch.clear()
            self.last_flush = asyncio.get_event_loop().time()
        
        # Log batch summary first
        self.logger.info("Batch log flush", 
                        batch_size=len(batch_copy),
                        first_timestamp=batch_copy[0]["timestamp"],
                        last_timestamp=batch_copy[-1]["timestamp"])
        
        # Process batch entries
        for entry in batch_copy:
            log_method = getattr(self.logger, entry["level"], self.logger.info)
            entry_data = {k: v for k, v in entry.items() 
                         if k not in ("level", "message", "timestamp")}
            log_method(entry["message"], **entry_data)
    
    async def _periodic_flush(self):
        """Periodically flush batches."""
        while True:
            try:
                await asyncio.sleep(self.flush_interval)
                current_time = asyncio.get_event_loop().time()
                if (current_time - self.last_flush) >= self.flush_interval:
                    await self._flush()
            except asyncio.CancelledError:
                break

# Usage
async def high_volume_logging():
    logger = get_logger("batch_example")
    batch_logger = BatchLogger(logger, batch_size=50, flush_interval=2.0)
    
    await batch_logger.start()
    
    try:
        # High-volume logging
        for i in range(1000):
            await batch_logger.log("info", "High volume message", 
                                 iteration=i, 
                                 user_id=f"user_{i % 100}")
    finally:
        await batch_logger.stop()
```

## Memory Optimization

### Object Reuse

```python
from provide.foundation import get_logger
import threading
from typing import Dict, Any

class OptimizedLogger:
    """Logger with memory optimizations."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        # Thread-local storage for reusable objects
        self._local = threading.local()
    
    def _get_context_dict(self) -> Dict[str, Any]:
        """Get reusable context dictionary."""
        if not hasattr(self._local, 'context_dict'):
            self._local.context_dict = {}
        
        # Clear previous values
        self._local.context_dict.clear()
        return self._local.context_dict
    
    def log_request(self, request_id: str, user_id: int, action: str, **extra):
        """Optimized request logging."""
        # Reuse dictionary object
        context = self._get_context_dict()
        context.update({
            "request_id": request_id,
            "user_id": user_id,
            "action": action,
            **extra
        })
        
        self.logger.info("Request processed", **context)

# Usage
optimized_logger = OptimizedLogger()

# This reuses memory instead of creating new dicts each time
for i in range(10000):
    optimized_logger.log_request(f"req_{i}", i % 1000, "process_data")
```

### String Interning

```python
import sys
from provide.foundation import get_logger

# Intern commonly used strings to save memory
COMMON_ACTIONS = {
    sys.intern("create"),
    sys.intern("read"), 
    sys.intern("update"),
    sys.intern("delete"),
    sys.intern("list"),
    sys.intern("search")
}

COMMON_STATUSES = {
    sys.intern("success"),
    sys.intern("error"),
    sys.intern("pending"),
    sys.intern("cancelled")
}

logger = get_logger(__name__)

def optimized_crud_logging(action: str, status: str, **context):
    """Memory-optimized logging for CRUD operations."""
    # Use interned strings when possible
    action_str = action if action in COMMON_ACTIONS else action
    status_str = status if status in COMMON_STATUSES else status
    
    logger.info("CRUD operation", 
               action=action_str,
               status=status_str,
               **context)
```

## Processor Optimization

### Custom High-Performance Processors

```python
import structlog
from typing import Any, Dict
from provide.foundation.logger.custom_processors import StructlogProcessor

def create_high_performance_processor() -> StructlogProcessor:
    """Create optimized processor for high-throughput scenarios."""
    
    def optimized_processor(
        logger: Any, 
        method_name: str, 
        event_dict: structlog.types.EventDict
    ) -> structlog.types.EventDict:
        """Highly optimized processor."""
        
        # Fast path for common cases - avoid expensive operations
        if len(event_dict) < 10:  # Small event dict
            return event_dict
        
        # Only process if we have specific fields that need optimization
        if "sensitive_data" in event_dict:
            # Remove sensitive data without complex masking
            event_dict.pop("sensitive_data", None)
        
        # Batch common transformations
        transforms = []
        for key in ("password", "token", "secret", "key"):
            if key in event_dict:
                transforms.append(key)
        
        # Apply transforms in batch
        for key in transforms:
            event_dict[key] = "[REDACTED]"
        
        return event_dict
    
    return optimized_processor

# Register optimized processor
from provide.foundation.logger.processors import _build_core_processors_list

# Would integrate this into the processor chain
```

### Minimal Context Processors

```python
def create_minimal_context_processor():
    """Processor that adds only essential context."""
    
    import time
    import threading
    
    def minimal_processor(logger, method_name, event_dict):
        # Only add timestamp and thread ID for debugging
        event_dict["ts"] = int(time.time())
        event_dict["tid"] = threading.get_ident()
        return event_dict
    
    return minimal_processor
```

## I/O Optimization

### Async Logging Patterns

```python
import asyncio
import aiofiles
from provide.foundation import get_logger

class AsyncFileLogger:
    """Async file logger for high-performance scenarios."""
    
    def __init__(self, file_path: str, buffer_size: int = 8192):
        self.file_path = file_path
        self.buffer_size = buffer_size
        self.write_queue = asyncio.Queue()
        self.writer_task = None
        
    async def start(self):
        """Start the async writer task."""
        self.writer_task = asyncio.create_task(self._writer_loop())
    
    async def stop(self):
        """Stop the writer and flush remaining logs."""
        if self.writer_task:
            await self.write_queue.put(None)  # Sentinel to stop
            await self.writer_task
    
    async def write_log(self, log_entry: str):
        """Queue log entry for async writing."""
        await self.write_queue.put(log_entry)
    
    async def _writer_loop(self):
        """Async loop that writes logs to file."""
        async with aiofiles.open(self.file_path, 'a', buffering=self.buffer_size) as f:
            while True:
                entry = await self.write_queue.get()
                if entry is None:  # Shutdown signal
                    break
                
                await f.write(entry + '\n')
                
                # Batch writes for efficiency
                batch = [entry]
                while not self.write_queue.empty() and len(batch) < 100:
                    try:
                        next_entry = self.write_queue.get_nowait()
                        if next_entry is None:
                            await f.write('\n'.join(batch) + '\n')
                            return
                        batch.append(next_entry)
                    except asyncio.QueueEmpty:
                        break
                
                if len(batch) > 1:
                    await f.write('\n'.join(batch[1:]) + '\n')
                
                await f.flush()

# Usage in high-performance async applications
async def high_performance_async_app():
    logger = get_logger("async_app")
    file_logger = AsyncFileLogger("/tmp/high_perf.log")
    
    await file_logger.start()
    
    try:
        # High-frequency async operations
        tasks = []
        for i in range(1000):
            async def process_item(item_id):
                logger.info("Processing async item", item_id=item_id)
                await file_logger.write_log(f"ASYNC_LOG: item_{item_id} processed")
                return f"result_{item_id}"
            
            tasks.append(process_item(i))
        
        results = await asyncio.gather(*tasks)
        logger.info("All async items processed", count=len(results))
        
    finally:
        await file_logger.stop()
```

## Production Optimization Checklist

### Deployment Configuration

```python
import os
from provide.foundation import setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

def setup_production_logging():
    """Production-optimized logging configuration."""
    
    # Determine environment
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        config = TelemetryConfig(
            service_name=os.getenv("SERVICE_NAME", "unknown"),
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
                das_emoji_prefix_enabled=False,
                logger_name_emoji_prefix_enabled=False,
                omit_timestamp=False,
                module_levels={
                    # Reduce log noise from libraries
                    "urllib3.connectionpool": "WARNING",
                    "requests.packages.urllib3": "WARNING",
                    "boto3.resources": "WARNING",
                    "botocore": "WARNING",
                    "asyncio": "WARNING",
                    "aiohttp.access": "WARNING",
                }
            ),
            globally_disabled=False
        )
    elif environment == "development":
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="key_value",  # More readable for dev
                das_emoji_prefix_enabled=True,  # Visual aid
                logger_name_emoji_prefix_enabled=True,
            )
        )
    else:  # staging
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO", 
                console_formatter="json",
                das_emoji_prefix_enabled=False,
            )
        )
    
    setup_telemetry(config)

# Apply environment-specific configuration
setup_production_logging()
```

### Performance Monitoring

```python
import time
import psutil
from provide.foundation import get_logger

class PerformanceMonitor:
    """Monitor logging performance metrics."""
    
    def __init__(self):
        self.logger = get_logger("perf_monitor")
        self.start_time = time.time()
        self.message_count = 0
        self.last_report = time.time()
        
    def record_log_message(self):
        """Record that a log message was processed."""
        self.message_count += 1
        
        # Report performance every 10000 messages
        if self.message_count % 10000 == 0:
            self._report_performance()
    
    def _report_performance(self):
        """Report current performance metrics."""
        current_time = time.time()
        
        # Calculate rates
        time_since_start = current_time - self.start_time
        time_since_report = current_time - self.last_report
        
        overall_rate = self.message_count / time_since_start
        recent_rate = 10000 / time_since_report
        
        # Get system metrics
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        
        self.logger.info("Performance metrics",
                        messages_total=self.message_count,
                        overall_rate=round(overall_rate, 0),
                        recent_rate=round(recent_rate, 0),
                        memory_percent=memory_info.percent,
                        cpu_percent=cpu_percent,
                        uptime_seconds=round(time_since_start, 1))
        
        self.last_report = current_time

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Integrate into logging pipeline (would be done in processor)
def performance_aware_logging():
    perf_monitor.record_log_message()
```