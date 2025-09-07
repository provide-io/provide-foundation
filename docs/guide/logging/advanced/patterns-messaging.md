# Message Queue Integration

Integration patterns for message queues and event-driven systems.

### Celery Integration

```python
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

# Create Celery app
app = Celery('myapp')
app.config_from_object('celeryconfig')

class CeleryTaskLogger:
    """Helper for task-specific logging."""
    
    def __init__(self, task_name: str):
        self.logger = get_logger(f"celery.task.{task_name}")
        self.task_name = task_name
    
    def log_task_start(self, task_id: str, args: tuple, kwargs: dict):
        """Log task execution start."""
        self.logger.info("Task started",
            domain="celery",
            action="task", 
            status="started",
            task_id=task_id,
            task_name=self.task_name,
            args_count=len(args),
            kwargs_count=len(kwargs),
            args_preview=str(args)[:200] if args else None,
            kwargs_preview=str(kwargs)[:200] if kwargs else None
        )
    
    def log_task_success(self, task_id: str, result: Any, duration: float):
        """Log successful task completion."""
        self.logger.info("Task completed successfully",
            domain="celery",
            action="task",
            status="success", 
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            result_type=type(result).__name__,
            result_preview=str(result)[:200] if result is not None else None
        )
    
    def log_task_failure(self, task_id: str, error: Exception, traceback: str, duration: float):
        """Log task failure."""
        self.logger.error("Task failed",
            domain="celery", 
            action="task",
            status="error",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            error_type=type(error).__name__,
            error_message=str(error),
            traceback=traceback[:1000]  # Truncate long tracebacks
        )
    
    def log_task_retry(self, task_id: str, error: Exception, retry_count: int, eta: Optional[str]):
        """Log task retry."""
        self.logger.warning("Task retry scheduled",
            domain="celery",
            action="task",
            status="retry",
            task_id=task_id,
            task_name=self.task_name,
            retry_count=retry_count,
            error_type=type(error).__name__,
            error_message=str(error),
            retry_eta=eta
        )

# Global task tracking
task_start_times: dict[str, float] = {}
task_loggers: dict[str, CeleryTaskLogger] = {}

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, **kwds):
    """Handle task pre-run signal."""
    task_start_times[task_id] = time.time()
    
    # Get or create task logger
    task_name = task.name if task else sender
    if task_name not in task_loggers:
        task_loggers[task_name] = CeleryTaskLogger(task_name)
    
    # Log task start
    task_loggers[task_name].log_task_start(task_id, args or (), kwargs or {})

@task_postrun.connect  
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, 
                        kwargs=None, retval=None, state=None, **kwds):
    """Handle task post-run signal."""
    start_time = task_start_times.pop(task_id, time.time())
    duration = time.time() - start_time
    
    task_name = task.name if task else sender
    if task_name in task_loggers:
        if state == 'SUCCESS':
            task_loggers[task_name].log_task_success(task_id, retval, duration)
        # Note: Failures are handled by task_failure signal

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwds):
    """Handle task failure signal."""
    start_time = task_start_times.pop(task_id, time.time())
    duration = time.time() - start_time
    
    task_name = sender.name if sender else "unknown"
    if task_name not in task_loggers:
        task_loggers[task_name] = CeleryTaskLogger(task_name)
    
    task_loggers[task_name].log_task_failure(
        task_id, exception, str(traceback), duration
    )

@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    """Handle worker ready signal."""
    logger = get_logger("celery.worker")
    logger.info("Celery worker ready",
        domain="celery",
        action="worker", 
        status="ready",
        hostname=sender.hostname if sender else "unknown"
    )

@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    """Handle worker shutdown signal."""
    logger = get_logger("celery.worker")  
    logger.info("Celery worker shutting down",
        domain="celery",
        action="worker",
        status="shutdown",
        hostname=sender.hostname if sender else "unknown"
    )

# Example task with comprehensive logging
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_user_data(self, user_id: int, data: dict):
    """Example Celery task with integrated logging."""
    
    # Task-specific logger (automatically configured by signals)
    logger = get_logger(f"celery.task.{self.name}")
    
    try:
        # Log processing steps
        logger.info("Processing user data",
            domain="users",
            action="process",
            status="started", 
            user_id=user_id,
            data_size=len(data),
            task_id=self.request.id
        )
        
        # Simulate processing steps
        validation_result = validate_user_data(user_id, data, logger)
        
        if not validation_result.valid:
            logger.warning("User data validation failed",
                domain="users",
                action="validate",
                status="failed",
                user_id=user_id,
                validation_errors=validation_result.errors
            )
            return {"success": False, "errors": validation_result.errors}
        
        # Process the data
        result = perform_data_processing(user_id, data, logger)
        
        logger.info("User data processed successfully",
            domain="users", 
            action="process",
            status="success",
            user_id=user_id,
            processed_records=result.get("record_count", 0)
        )
        
        return {"success": True, "result": result}
        
    except TemporaryProcessingError as e:
        # Retry for temporary errors
        logger.warning("Temporary processing error, retrying",
            domain="users",
            action="process", 
            status="retry",
            user_id=user_id,
            error_message=str(e),
            retry_count=self.request.retries,
            max_retries=self.max_retries
        )
        
        task_loggers[self.name].log_task_retry(
            self.request.id, e, self.request.retries, 
            str(self.retry(countdown=60))
        )
        
        raise self.retry(exc=e, countdown=60)
        
    except Exception as e:
        # Log and re-raise for permanent errors
        logger.error("Permanent processing error",
            domain="users",
            action="process",
            status="error", 
            user_id=user_id,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise

def validate_user_data(user_id: int, data: dict, logger) -> Any:
    """Validate user data with logging."""
    logger.debug("Validating user data",
        domain="users",
        action="validate",
        status="started",
        user_id=user_id
    )
    
    # Mock validation
    class ValidationResult:
        def __init__(self, valid: bool, errors: list = None):
            self.valid = valid
            self.errors = errors or []
    
    return ValidationResult(True, [])

def perform_data_processing(user_id: int, data: dict, logger) -> dict:
    """Process user data with logging."""
    logger.debug("Processing user data",
        domain="users",
        action="transform",
        status="started", 
        user_id=user_id
    )
    
    # Mock processing
    return {"record_count": 42, "status": "processed"}

class TemporaryProcessingError(Exception):
    """Temporary processing error that should trigger retry."""
    pass
```

