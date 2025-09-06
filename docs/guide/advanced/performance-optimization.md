# Performance Optimization

Advanced performance tuning techniques for high-throughput logging scenarios.

## High-Performance Logging Configuration

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

def setup_high_performance_logging():
    """Setup logging optimized for high throughput."""
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",  # Avoid DEBUG in production
            console_formatter="json",  # JSON is faster than key_value
            das_emoji_prefix_enabled=False,  # Disable emoji for speed
            logger_name_emoji_prefix_enabled=False,
            omit_timestamp=False,  # Keep timestamps but optimize format
            module_levels={
                # Reduce noise from chatty libraries
                "urllib3": "WARNING",
                "requests": "WARNING", 
                "boto3": "WARNING",
                "botocore": "WARNING"
            }
        ),
        globally_disabled=False
    )
    setup_telemetry(config)

# Optimized logging patterns
from provide.foundation import get_logger

# Use logger binding for repeated context
log = get_logger(__name__)
request_log = log.bind(request_id="abc-123", user_id=456)

# Efficient: Reuse bound logger
request_log.info("Request started")
request_log.info("Database query completed", duration_ms=45)
request_log.info("Request completed", status=200)

# Less efficient: Repeat context in each call
# log.info("Request started", request_id="abc-123", user_id=456)
# log.info("Database query completed", request_id="abc-123", user_id=456, duration_ms=45)
```

## Batched Logging for High Volume

```python
import asyncio
import time
from collections import deque
from typing import Dict, Any, List

class BatchedLogger:
    """Logger that batches messages for high-volume scenarios."""
    
    def __init__(self, logger, batch_size=100, flush_interval=5.0):
        self.logger = logger
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch: deque = deque()
        self.last_flush = time.time()
        self._lock = asyncio.Lock()
    
    async def log(self, level: str, message: str, **kwargs):
        """Add log entry to batch."""
        entry = {
            "level": level,
            "message": message,
            "timestamp": time.time(),
            **kwargs
        }
        
        async with self._lock:
            self.batch.append(entry)
            
            # Flush if batch is full or interval exceeded
            if (len(self.batch) >= self.batch_size or 
                time.time() - self.last_flush >= self.flush_interval):
                await self._flush()
    
    async def _flush(self):
        """Flush the current batch."""
        if not self.batch:
            return
        
        batch_copy = list(self.batch)
        self.batch.clear()
        self.last_flush = time.time()
        
        # Log batch summary
        self.logger.info("Batch log flush", 
                        batch_size=len(batch_copy),
                        first_timestamp=batch_copy[0]["timestamp"],
                        last_timestamp=batch_copy[-1]["timestamp"])
        
        # Process batch (could write to file, send to service, etc.)
        for entry in batch_copy:
            getattr(self.logger, entry["level"])(
                entry["message"], 
                **{k: v for k, v in entry.items() 
                   if k not in ("level", "message", "timestamp")}
            )
    
    async def shutdown(self):
        """Flush any remaining logs on shutdown."""
        await self._flush()

# Usage
batched_logger = BatchedLogger(get_logger("batch"))

async def high_volume_task():
    for i in range(1000):
        await batched_logger.log("info", "Processing item", item_id=i, batch="high_volume")
    
    await batched_logger.shutdown()

# asyncio.run(high_volume_task())
```

## Custom Output Formatters

```python
import json
import time
from typing import Any, Dict
from provide.foundation.logger import add_processor

class PrometheusFormatter:
    """Format logs as Prometheus metrics."""
    
    def __init__(self):
        self.metrics = []
    
    def __call__(self, logger, method_name, event_dict):
        """Convert log to Prometheus metric format."""
        level = event_dict.get("level", "info")
        event = event_dict.get("event", "unknown")
        
        # Create metric
        metric_name = f"app_log_{level}_total"
        labels = {
            "event": event,
            "logger": event_dict.get("logger", "unknown")
        }
        
        # Add to metrics collection
        metric = f'{metric_name}{{{",".join([f"{k}=\"{v}\"" for k, v in labels.items()])}}} 1'
        self.metrics.append(metric)
        
        return event_dict
    
    def export_metrics(self) -> str:
        """Export collected metrics in Prometheus format."""
        return "\n".join(self.metrics)

class StructuredJSONFormatter:
    """Enhanced JSON formatter with additional metadata."""
    
    def __call__(self, logger, method_name, event_dict):
        """Add structured metadata to JSON logs."""
        # Add standard fields
        event_dict["@timestamp"] = time.isoformat()
        event_dict["@version"] = "1"
        event_dict["host"] = socket.gethostname()
        event_dict["service"] = os.getenv("SERVICE_NAME", "unknown")
        
        # Add log source information
        event_dict["source"] = {
            "file": event_dict.get("pathname", "unknown"),
            "line": event_dict.get("lineno", 0),
            "function": event_dict.get("funcName", "unknown")
        }
        
        return event_dict

# Register custom formatters
prometheus_formatter = PrometheusFormatter()
json_formatter = StructuredJSONFormatter()

add_processor(prometheus_formatter)
add_processor(json_formatter)
```

## Production Patterns

### Health Checks and Monitoring

```python
import asyncio
import time
from typing import Dict, Any, Optional
from provide.foundation import get_logger

class HealthChecker:
    """Application health checker with logging integration."""
    
    def __init__(self):
        self.logger = get_logger("health")
        self.checks: Dict[str, callable] = {}
        self.last_results: Dict[str, Any] = {}
    
    def register_check(self, name: str, check_func: callable):
        """Register a health check function."""
        self.checks[name] = check_func
        self.logger.info("Health check registered", check_name=name)
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all registered health checks."""
        results = {}
        overall_healthy = True
        
        self.logger.info("Running health checks", check_count=len(self.checks))
        
        for name, check_func in self.checks.items():
            start_time = time.time()
            
            try:
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()
                
                duration = time.time() - start_time
                
                results[name] = {
                    "status": "healthy",
                    "result": result,
                    "duration_seconds": duration,
                    "timestamp": time.time()
                }
                
                self.logger.info("Health check passed",
                               check_name=name,
                               duration_seconds=duration)
                
            except Exception as e:
                duration = time.time() - start_time
                overall_healthy = False
                
                results[name] = {
                    "status": "unhealthy", 
                    "error": str(e),
                    "duration_seconds": duration,
                    "timestamp": time.time()
                }
                
                self.logger.error("Health check failed",
                                check_name=name,
                                error=str(e),
                                duration_seconds=duration)
        
        results["overall"] = {
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": time.time()
        }
        
        self.last_results = results
        self.logger.info("Health check completed",
                        overall_status=results["overall"]["status"],
                        healthy_checks=sum(1 for r in results.values() if r.get("status") == "healthy"))
        
        return results
    
    def get_last_results(self) -> Dict[str, Any]:
        """Get results of last health check run."""
        return self.last_results

# Example health checks
def database_health_check():
    """Check database connectivity."""
    # Simulate database check
    time.sleep(0.01)
    return {"connections": 5, "query_time_ms": 10}

async def cache_health_check():
    """Check cache connectivity."""
    await asyncio.sleep(0.005)
    return {"hit_rate": 0.95, "memory_usage": "45MB"}

# Setup health checker
health_checker = HealthChecker()
health_checker.register_check("database", database_health_check)
health_checker.register_check("cache", cache_health_check)

# Run health checks periodically
async def health_check_loop():
    while True:
        await health_checker.run_checks()
        await asyncio.sleep(30)  # Check every 30 seconds
```

### Circuit Breaker Pattern

```python
import asyncio
import time
from enum import Enum
from provide.foundation import get_logger

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open" 
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker with comprehensive logging."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
        
        self.logger = get_logger("circuit_breaker")
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self._transition_to_half_open()
            else:
                self.logger.warning("Circuit breaker open, request blocked",
                                  failure_count=self.failure_count,
                                  time_since_failure=time.time() - self.last_failure_time)
                raise Exception("Circuit breaker is OPEN")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure(e)
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            self.logger.info("Circuit breaker half-open success",
                           success_count=self.success_count)
            
            if self.success_count >= self.success_threshold:
                self._transition_to_closed()
    
    def _on_failure(self, exception):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        self.logger.error("Circuit breaker failure",
                         failure_count=self.failure_count,
                         exception=str(exception),
                         current_state=self.state.value)
        
        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_open()
        elif self.failure_count >= self.failure_threshold:
            self._transition_to_open()
    
    def _transition_to_open(self):
        """Transition to OPEN state."""
        self.state = CircuitState.OPEN
        self.success_count = 0
        self.logger.error("Circuit breaker opened",
                         failure_count=self.failure_count,
                         recovery_timeout=self.recovery_timeout)
    
    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state."""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.logger.info("Circuit breaker half-open, testing recovery")
    
    def _transition_to_closed(self):
        """Transition to CLOSED state."""
        self.state = CircuitState.CLOSED
        self.logger.info("Circuit breaker closed, fully recovered")

# Usage
cb = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def unreliable_service():
    """Simulate unreliable external service."""
    import random
    if random.random() < 0.3:  # 30% failure rate
        raise Exception("Service unavailable")
    return "Success"

async def test_circuit_breaker():
    for i in range(10):
        try:
            result = await cb.call(unreliable_service)
            print(f"Call {i}: {result}")
        except Exception as e:
            print(f"Call {i}: Failed - {e}")
        
        await asyncio.sleep(1)

# asyncio.run(test_circuit_breaker())
```