# Advanced Usage Guide

Advanced patterns and techniques for power users of provide.foundation, including custom emoji sets, processors, performance optimization, and architectural patterns.

## Overview

This guide covers advanced usage patterns for experienced developers who want to extend and customize provide.foundation:

- **Custom Emoji Sets**: Create domain-specific logging emoji sets
- **Custom Processors**: Extend the logging pipeline with custom processing
- **Performance Optimization**: Advanced performance tuning techniques
- **Thread Safety & Concurrency**: Advanced concurrent usage patterns
- **Integration Patterns**: Advanced integration with frameworks and services
- **Extension Points**: How to extend and customize the system

## Custom Emoji Sets

### Creating Domain-Specific Emoji Sets

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig, EmojiSet
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

class KubernetesEmojiSet(EmojiSetConfig):
    """Emoji set for Kubernetes operations."""
    
    domain = "k8s"
    
    def get_emoji(self, action: str, status: str) -> str:
        """Get emoji for Kubernetes operations."""
        if action.startswith("deploy"):
            return "🚀" if status == "success" else "💥"
        elif action.startswith("scale"):
            return "📏" if status == "success" else "⚠️"
        elif action.startswith("rollback"):
            return "⏪" if status == "success" else "🔄"
        elif action.startswith("pod"):
            return "📦" if status == "running" else "⏹️"
        elif action.startswith("service"):
            return "🔗" if status == "ready" else "🔌"
        else:
            return "⚙️"  # Default for unknown k8s operations

# Register and use the custom emoji set
k8s_emoji_set = KubernetesEmojiSet()

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="key_value",
        custom_emoji_sets=[k8s_emoji_set]
    )
)
setup_telemetry(config)

# Usage with domain-specific logger
from provide.foundation import get_logger
k8s_log = get_logger("k8s")

k8s_log.info("deploy_started", application="web-app", namespace="production")
k8s_log.info("deploy_success", application="web-app", replicas=3, namespace="production")
k8s_log.error("pod_failed", pod="web-app-abc123", reason="ImagePullBackOff")
```

### Multi-Domain Emoji Sets

```python
class WebEmojiSet(EmojiSetConfig):
    """Emoji set for web operations."""
    
    domain = "web"
    
    def get_emoji(self, action: str, status: str) -> str:
        if action.startswith("request"):
            if status.startswith("2"):  # 2xx status codes
                return "✅"
            elif status.startswith("4"):  # 4xx status codes
                return "❌"
            elif status.startswith("5"):  # 5xx status codes
                return "💥"
            else:
                return "🌐"
        elif action.startswith("cache"):
            return "⚡" if status == "hit" else "💾"
        elif action.startswith("auth"):
            return "🔐" if status == "success" else "🚫"
        else:
            return "🌐"

class DatabaseEmojiSet(EmojiSetConfig):
    """Emoji set for database operations."""
    
    domain = "db"
    
    def get_emoji(self, action: str, status: str) -> str:
        if action.startswith("query"):
            return "🔍" if status == "success" else "❗"
        elif action.startswith("connection"):
            return "🔗" if status == "connected" else "🔌"
        elif action.startswith("migration"):
            return "🔄" if status == "success" else "⚠️"
        elif action.startswith("backup"):
            return "💾" if status == "success" else "❌"
        else:
            return "🗄️"

# Use multiple emoji sets
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[
            WebEmojiSet(),
            DatabaseEmojiSet(),
            KubernetesEmojiSet()
        ]
    )
)
setup_telemetry(config)

# Use with different domain loggers
web_log = get_logger("web")
db_log = get_logger("db")
k8s_log = get_logger("k8s")

web_log.info("request_completed", method="GET", status="200", path="/api/users")
db_log.debug("query_executed", table="users", duration_ms=45)
k8s_log.info("pod_ready", pod="api-server-xyz789", node="worker-1")
```

## Custom Log Processors

### Creating Custom Processors

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

### Advanced Processor Patterns

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

## Performance Optimization

### High-Performance Logging Configuration

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

### Batched Logging for High Volume

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

## Integration Patterns

### FastAPI Integration

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import time
import uuid
from provide.foundation import get_logger, Context, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class LoggingMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for request logging."""
    
    def __init__(self, app, logger_name: str = "api"):
        super().__init__(app)
        self.logger = get_logger(logger_name)
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request start
        self.logger.info("Request started",
                        request_id=request_id,
                        method=request.method,
                        url=str(request.url),
                        headers=dict(request.headers),
                        client_ip=request.client.host)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log successful response
            duration = time.time() - start_time
            self.logger.info("Request completed",
                           request_id=request_id,
                           status_code=response.status_code,
                           duration_seconds=duration)
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            self.logger.error("Request failed",
                            request_id=request_id,
                            exception=str(e),
                            duration_seconds=duration)
            raise

# Setup FastAPI with logging
def create_app():
    # Configure logging
    config = TelemetryConfig(
        service_name="my-api",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    setup_telemetry(config)
    
    # Create app with middleware
    app = FastAPI(title="My API")
    app.add_middleware(LoggingMiddleware)
    
    return app

app = create_app()
api_log = get_logger("api")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    api_log.info("Fetching user", user_id=user_id)
    
    # Simulate database lookup
    await asyncio.sleep(0.05)
    
    user = {"id": user_id, "name": f"User {user_id}"}
    api_log.info("User fetched successfully", user_id=user_id, user=user)
    
    return user
```

### Django Integration

```python
import logging
import time
from django.utils.deprecation import MiddlewareMixin
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

class DjangoFoundationLoggingMiddleware(MiddlewareMixin):
    """Django middleware for provide.foundation logging."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = get_logger("django")
        
    def process_request(self, request):
        request.start_time = time.time()
        request.logger = self.logger.bind(
            request_id=getattr(request, 'id', 'unknown'),
            path=request.path,
            method=request.method
        )
        
        request.logger.info("Request started",
                          user=getattr(request.user, 'username', 'anonymous') if hasattr(request, 'user') else 'unknown',
                          ip=request.META.get('REMOTE_ADDR'))
        
    def process_response(self, request, response):
        if hasattr(request, 'start_time') and hasattr(request, 'logger'):
            duration = time.time() - request.start_time
            request.logger.info("Request completed",
                              status_code=response.status_code,
                              duration_seconds=duration)
        return response
    
    def process_exception(self, request, exception):
        if hasattr(request, 'logger'):
            request.logger.error("Request failed",
                                exception=str(exception),
                                exception_type=type(exception).__name__)

# Django settings integration
class FoundationLoggingConfig:
    """Django settings for provide.foundation."""
    
    @classmethod
    def setup(cls, debug=False, log_level="INFO"):
        """Setup provide.foundation for Django."""
        config = TelemetryConfig(
            service_name="django-app",
            debug=debug,
            logging=LoggingConfig(
                default_level=log_level,
                console_formatter="json" if not debug else "key_value",
                module_levels={
                    "django.db.backends": "WARNING",  # Reduce SQL query logs
                    "django.request": "INFO"
                }
            )
        )
        setup_telemetry(config)

# In Django views
from django.http import JsonResponse
from provide.foundation import get_logger

def user_view(request, user_id):
    log = get_logger("views.user")
    
    log.info("Fetching user", user_id=user_id)
    
    try:
        # Simulate user lookup
        user_data = {"id": user_id, "name": f"User {user_id}"}
        
        log.info("User retrieved successfully", user_id=user_id)
        return JsonResponse(user_data)
        
    except Exception as e:
        log.error("Failed to retrieve user", user_id=user_id, error=str(e))
        return JsonResponse({"error": "User not found"}, status=404)
```

### Celery Integration

```python
from celery import Celery
from celery.signals import task_prerun, task_postrun, task_failure
from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
import time

# Configure logging for Celery
config = TelemetryConfig(
    service_name="celery-worker",
    logging=LoggingConfig(
        default_level="INFO",
        console_formatter="json"
    )
)
setup_telemetry(config)

app = Celery('myapp')
celery_log = get_logger("celery")

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Log task start."""
    celery_log.info("Task started",
                   task_id=task_id,
                   task_name=task.name,
                   args=args,
                   kwargs=kwargs)

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, 
                        retval=None, state=None, **kwds):
    """Log task completion."""
    celery_log.info("Task completed",
                   task_id=task_id,
                   task_name=task.name,
                   state=state,
                   result_type=type(retval).__name__)

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Log task failure."""
    celery_log.error("Task failed",
                    task_id=task_id,
                    task_name=sender.name,
                    exception=str(exception),
                    exception_type=type(exception).__name__)

@app.task
def process_data(data_id: int):
    """Example Celery task with logging."""
    task_log = get_logger("tasks.process_data")
    
    task_log.info("Processing data", data_id=data_id)
    
    try:
        # Simulate data processing
        time.sleep(2)
        
        result = {"data_id": data_id, "processed": True, "timestamp": time.time()}
        
        task_log.info("Data processing completed", 
                     data_id=data_id,
                     result=result)
        
        return result
        
    except Exception as e:
        task_log.error("Data processing failed", 
                      data_id=data_id,
                      error=str(e))
        raise
```

## Extension Points and Customization

### Custom Configuration Sources

```python
from provide.foundation import Context
from typing import Dict, Any
import requests
import json

class RemoteConfigSource:
    """Load configuration from remote service."""
    
    def __init__(self, config_url: str, api_key: str):
        self.config_url = config_url
        self.api_key = api_key
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from remote service."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(self.config_url, headers=headers)
        response.raise_for_status()
        return response.json()

class VaultConfigSource:
    """Load secrets from HashiCorp Vault."""
    
    def __init__(self, vault_url: str, vault_token: str):
        self.vault_url = vault_url
        self.vault_token = vault_token
    
    def load_secrets(self, path: str) -> Dict[str, Any]:
        """Load secrets from Vault."""
        headers = {"X-Vault-Token": self.vault_token}
        response = requests.get(f"{self.vault_url}/v1/{path}", headers=headers)
        response.raise_for_status()
        return response.json()["data"]

class AdvancedContext(Context):
    """Extended Context with remote configuration support."""
    
    def load_remote_config(self, config_source: RemoteConfigSource):
        """Load configuration from remote source."""
        try:
            config_data = config_source.load_config()
            
            # Update context with remote configuration
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
        except Exception as e:
            # Log error but don't fail initialization
            print(f"Failed to load remote config: {e}")
    
    def load_vault_secrets(self, vault_source: VaultConfigSource, secret_path: str):
        """Load secrets from Vault."""
        try:
            secrets = vault_source.load_secrets(secret_path)
            
            # Apply secrets to context
            for key, value in secrets.items():
                setattr(self, f"secret_{key}", value)
                
        except Exception as e:
            print(f"Failed to load vault secrets: {e}")

# Usage
remote_source = RemoteConfigSource("https://config.example.com/api/config", "api-key")
vault_source = VaultConfigSource("https://vault.example.com", "vault-token")

ctx = AdvancedContext()
ctx.load_remote_config(remote_source)
ctx.load_vault_secrets(vault_source, "secret/myapp/config")
```

### Custom Output Formatters

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

This advanced usage guide provides comprehensive patterns for extending and optimizing provide.foundation in production environments, covering custom extensions, performance optimization, and enterprise integration patterns.