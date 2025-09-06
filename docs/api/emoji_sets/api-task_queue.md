# Task Queue Emoji Set

Visual enhancements for asynchronous task queue operations, message processing, and background job management.

## Overview

The Task Queue emoji set provides visual context for asynchronous task processing, making it easy to identify different types of task queue activities at a glance. It covers popular task queue systems like Celery, RQ, Dramatiq, and message brokers like Kafka and RabbitMQ.

## Emoji Mappings

### Task Queue Systems
- **Celery**: 🥕 (celery vegetable)
- **RQ**: 🟥🇶 (red Q for Redis Queue)
- **Dramatiq**: 🎭 (drama/theater mask)
- **Kafka**: 🌊 (streaming data waves)
- **RabbitMQ**: 🐇 (rabbit for message broker)
- **Generic**: 📨 (message envelope)

### Task Status
- **Submitted**: ➡️📨 (arrow with message)
- **Received**: 📥 (inbox tray)
- **Started**: ▶️ (play button)
- **In Progress**: 🔄 (refresh/processing)
- **Retrying**: 🔁 (repeat/retry)
- **Success**: ✅🏁 (checkmark with finish flag)
- **Failure**: ❌🔥 (error with fire)
- **Revoked**: 🚫 (prohibited/cancelled)

## Usage Examples

### Basic Task Queue Logging

```python
from provide.foundation import get_logger

# Create task-specific logger
task_log = get_logger("task_queue")

# Task lifecycle logging
task_log.info("task_submitted", 
              task_name="process_payment", 
              task_id="abc-123",
              queue_name="payments")

task_log.info("task_started",
              task_name="process_payment",
              task_id="abc-123", 
              worker_id="worker-1")

task_log.info("task_completed",
              task_name="process_payment",
              task_id="abc-123",
              duration_ms=1500,
              status="success")
```

### Celery Integration

```python
from provide.foundation import get_logger
from celery import Celery
from celery.signals import (
    task_prerun, task_postrun, task_success, 
    task_failure, task_retry
)

app = Celery('myapp')
task_log = get_logger("task_queue.celery")

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kw):
    task_log.info("task_started",
                  task_system="celery",
                  task_name=task.name,
                  task_id=task_id,
                  queue_name=task.request.delivery_info.get('routing_key'))

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kw):
    task_log.info("task_completed", 
                  task_system="celery",
                  task_name=task.name,
                  task_id=task_id,
                  status=state.lower())

@task_success.connect
def task_success_handler(sender=None, result=None, **kw):
    task_log.info("task_success",
                  task_system="celery", 
                  task_name=sender.name,
                  task_status="success",
                  result_type=type(result).__name__)

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kw):
    task_log.error("task_failure",
                   task_system="celery",
                   task_name=sender.name if sender else "unknown",
                   task_id=task_id,
                   task_status="failure",
                   error=str(exception),
                   error_type=type(exception).__name__)

@task_retry.connect  
def task_retry_handler(sender=None, task_id=None, reason=None, einfo=None, **kw):
    task_log.warning("task_retry",
                     task_system="celery",
                     task_name=sender.name if sender else "unknown", 
                     task_id=task_id,
                     task_status="retrying",
                     retry_reason=str(reason))
```

### RQ (Redis Queue) Integration

```python
from provide.foundation import get_logger
from rq import Worker, Queue, Connection
import redis

redis_conn = redis.Redis()
task_log = get_logger("task_queue.rq")

class LoggingWorker(Worker):
    def execute_job(self, job, queue):
        task_log.info("task_started",
                      task_system="rq",
                      task_name=job.func_name,
                      task_id=job.id,
                      queue_name=queue.name)
        
        try:
            result = super().execute_job(job, queue)
            
            task_log.info("task_completed",
                          task_system="rq", 
                          task_name=job.func_name,
                          task_id=job.id,
                          task_status="success",
                          queue_name=queue.name)
            
            return result
            
        except Exception as e:
            task_log.error("task_failed",
                           task_system="rq",
                           task_name=job.func_name,
                           task_id=job.id,
                           task_status="failure", 
                           queue_name=queue.name,
                           error=str(e))
            raise

# Usage
queue = Queue('default', connection=redis_conn)
worker = LoggingWorker(['default'], connection=redis_conn)

@queue.enqueue
def process_data(data):
    # Your task logic here
    return f"Processed {len(data)} items"
```

### Dramatiq Integration

```python
from provide.foundation import get_logger
import dramatiq
from dramatiq.middleware import Middleware

task_log = get_logger("task_queue.dramatiq")

class LoggingMiddleware(Middleware):
    def before_process_message(self, broker, message):
        task_log.info("task_started",
                      task_system="dramatiq",
                      task_name=message.actor_name,
                      task_id=message.message_id,
                      queue_name=message.queue_name)

    def after_process_message(self, broker, message, *, result=None, exception=None):
        if exception:
            task_log.error("task_failed",
                           task_system="dramatiq",
                           task_name=message.actor_name,
                           task_id=message.message_id,
                           task_status="failure",
                           error=str(exception))
        else:
            task_log.info("task_completed", 
                          task_system="dramatiq",
                          task_name=message.actor_name,
                          task_id=message.message_id,
                          task_status="success")

    def before_delay_message(self, broker, message):
        task_log.info("task_submitted",
                      task_system="dramatiq",
                      task_name=message.actor_name, 
                      task_id=message.message_id,
                      queue_name=message.queue_name,
                      delay_ms=message.options.get('delay', 0))

# Configure broker with middleware
broker = dramatiq.get_broker()
broker.add_middleware(LoggingMiddleware())

@dramatiq.actor
def send_email(to, subject, body):
    # Email sending logic
    task_log.debug("email_sent", recipient=to, subject=subject)
```

### Batch Processing with Progress Tracking

```python
from provide.foundation import get_logger
import asyncio
from typing import Any

task_log = get_logger("task_queue.batch")

class BatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.log = task_log
    
    async def process_batch(self, task_name: str, items: list[Any], processor_func):
        total_items = len(items)
        batches = [items[i:i + self.batch_size] for i in range(0, total_items, self.batch_size)]
        
        self.log.info("batch_processing_started",
                      task_name=task_name,
                      total_items=total_items,
                      batch_count=len(batches),
                      batch_size=self.batch_size)
        
        completed = 0
        failed = 0
        
        for batch_num, batch in enumerate(batches, 1):
            batch_task_id = f"{task_name}-batch-{batch_num}"
            
            self.log.debug("batch_started",
                           task_name=task_name,
                           task_id=batch_task_id,
                           batch_number=batch_num,
                           batch_items=len(batch))
            
            try:
                results = await processor_func(batch)
                completed += len(batch)
                
                self.log.info("batch_completed",
                              task_name=task_name,
                              task_id=batch_task_id,
                              task_status="success",
                              batch_number=batch_num,
                              items_processed=len(batch),
                              progress_percent=round((completed / total_items) * 100, 1))
                
            except Exception as e:
                failed += len(batch)
                
                self.log.error("batch_failed",
                               task_name=task_name,
                               task_id=batch_task_id,
                               task_status="failure",
                               batch_number=batch_num,
                               error=str(e),
                               items_failed=len(batch))
        
        self.log.info("batch_processing_completed",
                      task_name=task_name,
                      total_items=total_items,
                      completed_items=completed,
                      failed_items=failed,
                      success_rate=round((completed / total_items) * 100, 1))

# Usage
processor = BatchProcessor(batch_size=50)

async def process_items(items):
    # Simulate processing
    await asyncio.sleep(0.1)
    return [f"processed_{item}" for item in items]

# Process a large dataset
large_dataset = list(range(1000))
await processor.process_batch("data_processing", large_dataset, process_items)
```

### Task Queue Health Monitoring

```python
from provide.foundation import get_logger
import asyncio
import time

class TaskQueueMonitor:
    def __init__(self, queue_name: str, system: str = "celery"):
        self.queue_name = queue_name
        self.system = system
        self.log = get_logger(f"task_queue.{system}.monitor")
    
    def log_queue_stats(self, pending: int, active: int, completed: int, failed: int):
        total_processed = completed + failed
        success_rate = (completed / total_processed * 100) if total_processed > 0 else 0
        
        self.log.info("queue_status",
                      task_system=self.system,
                      queue_name=self.queue_name,
                      pending_tasks=pending,
                      active_tasks=active,
                      completed_tasks=completed,
                      failed_tasks=failed,
                      success_rate_percent=round(success_rate, 1))
        
        # Alert on high failure rate
        if total_processed > 10 and success_rate < 90:
            self.log.warning("high_failure_rate",
                           task_system=self.system,
                           queue_name=self.queue_name,
                           success_rate_percent=round(success_rate, 1),
                           threshold_percent=90)
        
        # Alert on queue backup
        if pending > 1000:
            self.log.warning("queue_backlog",
                           task_system=self.system,
                           queue_name=self.queue_name,
                           pending_tasks=pending,
                           threshold_tasks=1000)
    
    def log_worker_stats(self, worker_id: str, tasks_processed: int, 
                        avg_duration_ms: float, last_seen: float):
        inactive_minutes = (time.time() - last_seen) / 60
        
        self.log.info("worker_status",
                      task_system=self.system,
                      worker_id=worker_id,
                      tasks_processed=tasks_processed,
                      avg_duration_ms=round(avg_duration_ms, 2),
                      inactive_minutes=round(inactive_minutes, 1))
        
        # Alert on inactive worker
        if inactive_minutes > 5:
            self.log.warning("worker_inactive",
                           task_system=self.system,
                           worker_id=worker_id,
                           inactive_minutes=round(inactive_minutes, 1),
                           threshold_minutes=5)

# Usage with periodic monitoring
monitor = TaskQueueMonitor("high_priority", "celery")

async def monitor_queue_health():
    while True:
        # Get stats from your queue system
        stats = get_celery_queue_stats("high_priority")
        monitor.log_queue_stats(
            pending=stats['pending'],
            active=stats['active'], 
            completed=stats['completed'],
            failed=stats['failed']
        )
        
        # Monitor workers
        for worker_id, worker_stats in get_worker_stats().items():
            monitor.log_worker_stats(
                worker_id=worker_id,
                tasks_processed=worker_stats['processed'],
                avg_duration_ms=worker_stats['avg_duration'],
                last_seen=worker_stats['last_seen']
            )
        
        await asyncio.sleep(60)  # Monitor every minute
```

## Performance Monitoring

### Task Duration Analysis

```python
from provide.foundation import get_logger
import time
from collections import defaultdict, deque

class TaskPerformanceAnalyzer:
    def __init__(self, window_size: int = 100):
        self.log = get_logger("task_queue.performance")
        self.window_size = window_size
        self.durations = defaultdict(lambda: deque(maxlen=window_size))
        self.counts = defaultdict(int)
        
    def record_task(self, task_name: str, duration_ms: float, status: str):
        self.durations[task_name].append(duration_ms)
        self.counts[task_name] += 1
        
        # Log performance metrics every 10 tasks
        if self.counts[task_name] % 10 == 0:
            self._analyze_performance(task_name)
    
    def _analyze_performance(self, task_name: str):
        durations = list(self.durations[task_name])
        if len(durations) < 5:  # Need some data
            return
            
        avg_duration = sum(durations) / len(durations)
        p50_duration = sorted(durations)[len(durations) // 2]
        p95_duration = sorted(durations)[int(len(durations) * 0.95)]
        
        self.log.info("task_performance_analysis",
                      task_name=task_name,
                      sample_size=len(durations),
                      avg_duration_ms=round(avg_duration, 2),
                      p50_duration_ms=round(p50_duration, 2),
                      p95_duration_ms=round(p95_duration, 2))
        
        # Alert on slow tasks
        if avg_duration > 5000:  # 5 seconds
            self.log.warning("slow_task_detected",
                           task_name=task_name,
                           avg_duration_ms=round(avg_duration, 2),
                           threshold_ms=5000)

# Usage
analyzer = TaskPerformanceAnalyzer()

def track_task_performance(task_name: str, duration_ms: float, status: str):
    analyzer.record_task(task_name, duration_ms, status)
```

## Configuration

### Enabling Task Queue Emoji Set

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        enabled_emoji_sets=["task_queue"]
    )
)
setup_telemetry(config)
```

### Custom Task Queue Emoji Set

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig

class CustomTaskQueueEmojiSet(EmojiSetConfig):
    """Custom task queue emoji set with additional system mappings."""
    
    domain = "task_queue"
    
    def get_emoji(self, action: str, status: str) -> str:
        # Custom mappings for specific task systems
        if "sidekiq" in action and status == "success":
            return "💎✅"  # Ruby gem + success
        elif "django_rq" in action:
            return "🐍🟥" if status == "success" else "🐍❌"
        elif action.startswith("cron"):
            return "⏰" if status == "success" else "⏰❌"
        elif action.startswith("priority"):
            return "🔥" if status == "high" else "📦"
        else:
            # Fallback to standard task queue emojis
            return super().get_emoji(action, status)

# Use custom emoji set
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[CustomTaskQueueEmojiSet()]
    )
)
```

## Best Practices

### 1. Log Levels for Task Operations

```python
# DEBUG: Detailed task parameters, internal state
task_log.debug("task_params", task_id="abc-123", args=args, kwargs=kwargs)

# INFO: Task lifecycle, completion, performance metrics
task_log.info("task_completed", task_id="abc-123", duration_ms=1250)

# WARNING: Retries, slow tasks, queue backlog
task_log.warning("task_retry", task_id="abc-123", attempt=3, max_retries=5)

# ERROR: Task failures, system errors
task_log.error("task_failed", task_id="abc-123", error="connection timeout")
```

### 2. Sensitive Data Handling

```python
# Good: Log metadata, not sensitive data
task_log.info("email_task_completed", 
              recipient_count=len(recipients),
              template_name="welcome")

# Avoid: Logging sensitive task data
# task_log.info("email_sent", recipients=email_list, content=email_body)
```

### 3. Structured Context

```python
# Use consistent field names for task operations
task_log.info("task_status_update",
              task_system="celery",
              task_name="process_payment",
              task_id="abc-123",
              task_status="success",
              queue_name="payments",
              duration_ms=1500,
              retries=0)
```

## Related Documentation

- [api-Base Emoji Types](api-base.md) - Core emoji system interfaces
- [api-Custom Emoji Sets](api-custom.md) - Creating custom emoji sets
- [api-HTTP Emoji Set](api-http.md) - Web request logging emojis
- [api-Database Emoji Set](api-database.md) - Database operation emojis
- [api-LLM Emoji Set](api-llm.md) - AI/ML model logging emojis
- [Testing Guide](../../guide/testing.md) - Testing task queue logging