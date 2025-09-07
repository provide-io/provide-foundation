#!/usr/bin/env python3
"""
Celery Integration Example

Demonstrates how to integrate provide.foundation logging with Celery
for comprehensive task tracking and monitoring.

Usage:
    # Start Celery worker in one terminal:
    celery -A 17_celery_integration worker --loglevel=info
    
    # Run tasks in another terminal:
    python 17_celery_integration.py
"""

import time
from typing import Any, Optional
from celery import Celery
from celery.signals import (
    task_prerun, task_postrun, task_failure, 
    worker_ready, worker_shutdown
)

from provide.foundation import get_logger, setup_telemetry
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig

# Setup telemetry for Celery
def setup_celery_logging():
    """Configure logging for Celery workers."""
    config = TelemetryConfig(
        service_name="celery-worker",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            module_levels={
                "celery.worker": "INFO",
                "celery.task": "INFO", 
                "celery.beat": "INFO",
                "billiard": "WARNING",
                "kombu": "WARNING"
            }
        )
    )
    setup_telemetry(config)

setup_celery_logging()

# Create Celery app with basic config
app = Celery('celery_logging_example')
app.conf.update(
    broker='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

class CeleryTaskLogger:
    """Helper for task-specific logging."""
    
    def __init__(self, task_name: str):
        self.logger = get_logger(f"celery.task.{task_name}")
        self.task_name = task_name
    
    def log_task_start(self, task_id: str, args: tuple, kwargs: dict):
        """Log task execution start."""
        self.logger.info("task_started",
            task_id=task_id,
            task_name=self.task_name,
            args_count=len(args),
            kwargs_count=len(kwargs),
            args_preview=str(args)[:200] if args else None,
            kwargs_preview=str(kwargs)[:200] if kwargs else None
        )
    
    def log_task_success(self, task_id: str, result: Any, duration: float):
        """Log successful task completion."""
        self.logger.info("task_completed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            result_type=type(result).__name__,
            success=True
        )
    
    def log_task_failure(self, task_id: str, error: Exception, duration: float):
        """Log task failure."""
        self.logger.error("task_failed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            error_type=type(error).__name__,
            error_message=str(error),
            success=False
        )

# Global logger for worker events
worker_logger = get_logger("celery.worker")

# Celery signal handlers
@worker_ready.connect
def worker_ready_handler(sender, **kwargs):
    """Log when worker is ready."""
    worker_logger.info("worker_ready",
        worker_pid=sender.pid,
        hostname=sender.hostname
    )

@worker_shutdown.connect  
def worker_shutdown_handler(sender, **kwargs):
    """Log when worker shuts down."""
    worker_logger.info("worker_shutdown",
        worker_pid=sender.pid,
        hostname=sender.hostname
    )

# Task tracking dictionary
task_start_times = {}

@task_prerun.connect
def task_prerun_handler(sender, task_id, task, args, kwargs, **kwds):
    """Log before task execution."""
    task_start_times[task_id] = time.time()
    task_logger = CeleryTaskLogger(task.name)
    task_logger.log_task_start(task_id, args, kwargs)

@task_postrun.connect
def task_postrun_handler(sender, task_id, task, args, kwargs, retval, state, **kwds):
    """Log after task execution."""
    duration = time.time() - task_start_times.pop(task_id, time.time())
    task_logger = CeleryTaskLogger(task.name)
    
    if state == 'SUCCESS':
        task_logger.log_task_success(task_id, retval, duration)
    else:
        # For non-success states, we might not have exception info here
        worker_logger.warning("task_completed_with_state",
            task_id=task_id,
            task_name=task.name,
            state=state,
            duration_ms=round(duration * 1000, 2)
        )

@task_failure.connect
def task_failure_handler(sender, task_id, exception, args, kwargs, traceback, einfo, **kwds):
    """Log task failures."""
    duration = time.time() - task_start_times.pop(task_id, time.time())
    task_logger = CeleryTaskLogger(sender.name)
    task_logger.log_task_failure(task_id, exception, duration)

# Example tasks
@app.task
def add_numbers(x: int, y: int) -> int:
    """Simple addition task."""
    task_logger = CeleryTaskLogger("add_numbers")
    task_logger.logger.debug("performing_addition", x=x, y=y)
    
    # Simulate some processing time
    time.sleep(0.1)
    
    result = x + y
    task_logger.logger.debug("addition_complete", result=result)
    return result

@app.task
def process_data(data: list) -> dict:
    """Process a list of data items."""
    task_logger = CeleryTaskLogger("process_data")
    task_logger.logger.info("processing_data", 
        item_count=len(data),
        data_size_bytes=len(str(data))
    )
    
    processed_items = []
    for i, item in enumerate(data):
        # Simulate processing
        time.sleep(0.01)
        processed_items.append(item.upper() if isinstance(item, str) else item)
        
        if i % 100 == 0:  # Log progress every 100 items
            task_logger.logger.debug("processing_progress",
                processed=i + 1,
                total=len(data),
                progress_percent=round((i + 1) / len(data) * 100, 1)
            )
    
    result = {
        "original_count": len(data),
        "processed_count": len(processed_items),
        "sample_results": processed_items[:5]
    }
    
    task_logger.logger.info("data_processing_complete",
        processed_items=len(processed_items)
    )
    
    return result

@app.task
def failing_task() -> str:
    """Task that demonstrates failure logging."""
    task_logger = CeleryTaskLogger("failing_task")
    task_logger.logger.info("about_to_fail")
    
    # Simulate some work before failing
    time.sleep(0.2)
    
    raise ValueError("This task always fails for demonstration purposes")

def run_example_tasks():
    """Run example tasks to demonstrate logging."""
    logger = get_logger("celery.example")
    
    logger.info("celery_example_started")
    
    try:
        # Simple task
        result1 = add_numbers.delay(4, 5)
        logger.info("submitted_add_task", task_id=result1.id)
        
        # Data processing task
        sample_data = [f"item_{i}" for i in range(20)]
        result2 = process_data.delay(sample_data)
        logger.info("submitted_process_task", task_id=result2.id)
        
        # Failing task
        result3 = failing_task.delay()
        logger.info("submitted_failing_task", task_id=result3.id)
        
        # Wait for results (in real apps, you might use callbacks or periodic checks)
        try:
            add_result = result1.get(timeout=10)
            logger.info("add_task_result", result=add_result, task_id=result1.id)
        except Exception as e:
            logger.error("add_task_error", error=str(e), task_id=result1.id)
        
        try:
            process_result = result2.get(timeout=10)
            logger.info("process_task_result", 
                processed_count=process_result["processed_count"],
                task_id=result2.id
            )
        except Exception as e:
            logger.error("process_task_error", error=str(e), task_id=result2.id)
        
        try:
            fail_result = result3.get(timeout=10)
            logger.info("failing_task_unexpectedly_succeeded", task_id=result3.id)
        except Exception as e:
            logger.info("failing_task_failed_as_expected", 
                error_type=type(e).__name__,
                task_id=result3.id
            )
        
    except Exception as e:
        logger.error("example_error", error=str(e), error_type=type(e).__name__)
    
    logger.info("celery_example_completed")

if __name__ == '__main__':
    # This will only run the client side - you need to start a Celery worker separately
    print("🔄 Running Celery integration example...")
    print("📝 Make sure you have a Celery worker running:")
    print("   celery -A 17_celery_integration worker --loglevel=info")
    print()
    
    run_example_tasks()
    
    print()
    print("✅ Example completed! Check the logs for structured Celery task tracking.")
    print("🔍 Key features demonstrated:")
    print("   • Task lifecycle logging (start, success, failure)")
    print("   • Worker event tracking")
    print("   • Progress logging for long tasks")
    print("   • Error handling with structured context")
    print("   • Task correlation with IDs")