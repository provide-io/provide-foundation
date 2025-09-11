#!/usr/bin/env python3
"""
Celery Integration Example - Rich Task Processing Patterns

Demonstrates comprehensive integration of provide.foundation logging with Celery,
showing real-world task processing patterns including:
- Task lifecycle tracking with structured logging
- Worker pool monitoring and health metrics
- Task retry patterns with exponential backoff
- Error handling and dead letter queues
- Progress tracking for long-running tasks
- Task chains and workflows
- Priority queues and routing
- Memory-based broker for demo (no Redis required)

Installation:
    pip install celery  # Redis optional for this demo

Usage:
    # Option 1: Run with memory broker (no Redis needed):
    python 01_celery_integration.py --demo
    
    # Option 2: Run with Redis (production-like):
    # Start Redis:
    redis-server
    
    # Start Celery worker:
    celery -A 01_celery_integration worker --loglevel=info --pool=solo
    
    # Run tasks:
    python 01_celery_integration.py
"""

import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Any
from pathlib import Path
import sys
import json
import threading
from collections import defaultdict
import os

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Handle optional Celery dependency
try:
    from celery import Celery, Task, group, chain, chord
    from celery.signals import (
        task_prerun, task_postrun, task_failure, task_retry,
        worker_ready, worker_shutdown, worker_process_init,
        beat_init, celeryd_after_setup
    )
    from celery.result import AsyncResult
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

from provide.foundation import logger, setup_telemetry, pout, perr  # noqa: E402
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig  # noqa: E402
from provide.foundation.errors import error_boundary  # noqa: E402

# Setup telemetry for Celery
def setup_celery_logging(demo_mode: bool = False):
    """Configure comprehensive logging for Celery workers."""
    config = TelemetryConfig(
        service_name="celery-rich-demo" if demo_mode else "celery-worker",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            module_levels={
                "celery.worker": "INFO",
                "celery.task": "INFO", 
                "celery.beat": "INFO",
                "celery.app.trace": "INFO",
                "billiard": "WARNING",
                "kombu": "WARNING"
            }
        )
    )
    setup_telemetry(config)

if not CELERY_AVAILABLE:
    perr("❌ Celery is not installed!")
    perr("💡 Install with: pip install celery")
    perr("📝 Redis is optional for demo mode")
    exit(1)

# Check if running in demo mode
DEMO_MODE = '--demo' in sys.argv

setup_celery_logging(demo_mode=DEMO_MODE)

# Create Celery app with appropriate config
if DEMO_MODE:
    # Use memory broker for demo (no Redis needed)
    app = Celery('celery_rich_demo')
    app.conf.update(
        broker='memory://',
        result_backend='cache+memory://',
        task_always_eager=False,  # Still use worker pool
        task_eager_propagates=True,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        # Task execution limits
        task_soft_time_limit=60,
        task_time_limit=120,
        # Retry configuration
        task_default_retry_delay=5,
        task_max_retries=3,
        # Result expiration
        result_expires=3600,
        # Worker configuration
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,
    )
else:
    # Production-like Redis configuration
    app = Celery('celery_logging_example')
    app.conf.update(
        broker='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        # Task execution limits
        task_soft_time_limit=60,
        task_time_limit=120,
        # Retry configuration  
        task_default_retry_delay=5,
        task_max_retries=3,
        # Result expiration
        result_expires=3600,
        # Worker configuration
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,
    )

# Global metrics tracking
class TaskMetrics:
    """Track task execution metrics."""
    def __init__(self):
        self.task_counts = defaultdict(int)
        self.task_durations = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.retry_counts = defaultdict(int)
        self.lock = threading.Lock()
    
    def record_execution(self, task_name: str, duration: float, success: bool):
        with self.lock:
            self.task_counts[task_name] += 1
            self.task_durations[task_name].append(duration)
            if not success:
                self.error_counts[task_name] += 1
    
    def record_retry(self, task_name: str):
        with self.lock:
            self.retry_counts[task_name] += 1
    
    def get_stats(self) -> dict[str, Any]:
        with self.lock:
            stats = {}
            for task_name in self.task_counts:
                durations = self.task_durations[task_name]
                stats[task_name] = {
                    "count": self.task_counts[task_name],
                    "errors": self.error_counts[task_name],
                    "retries": self.retry_counts[task_name],
                    "avg_duration_ms": round(sum(durations) / len(durations) * 1000, 2) if durations else 0,
                    "success_rate": round((1 - self.error_counts[task_name] / self.task_counts[task_name]) * 100, 1)
                }
            return stats

metrics = TaskMetrics()

class CeleryTaskLogger:
    """Enhanced task-specific logging with metrics."""
    
    def __init__(self, task_name: str):
        self.logger = logger.get_logger(f"celery.task.{task_name}")
        self.task_name = task_name
    
    def log_task_start(self, task_id: str, args: tuple, kwargs: dict):
        """Log task execution start with context."""
        self.logger.info("task_started",
            task_id=task_id,
            task_name=self.task_name,
            args_count=len(args),
            kwargs_count=len(kwargs),
            args_preview=str(args)[:200] if args else None,
            kwargs_preview=str(kwargs)[:200] if kwargs else None,
            queue="default",
            worker_hostname=app.conf.get('worker_hostname', 'unknown')
        )
    
    def log_task_progress(self, task_id: str, current: int, total: int, message: str = ""):
        """Log task progress for long-running tasks."""
        progress_pct = round((current / total) * 100, 1) if total > 0 else 0
        self.logger.info("task_progress",
            task_id=task_id,
            task_name=self.task_name,
            current=current,
            total=total,
            progress_pct=progress_pct,
            message=message
        )
    
    def log_task_success(self, task_id: str, result: Any, duration: float):
        """Log successful task completion with metrics."""
        metrics.record_execution(self.task_name, duration, True)
        self.logger.info("task_completed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            result_type=type(result).__name__,
            success=True,
            total_executions=metrics.task_counts[self.task_name]
        )
    
    def log_task_failure(self, task_id: str, error: Exception, duration: float):
        """Log task failure with context."""
        metrics.record_execution(self.task_name, duration, False)
        self.logger.error("task_failed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            error_type=type(error).__name__,
            error_message=str(error),
            success=False,
            total_errors=metrics.error_counts[self.task_name]
        )
    
    def log_task_retry(self, task_id: str, exc: Exception, countdown: int, retry_count: int):
        """Log task retry attempt."""
        metrics.record_retry(self.task_name)
        self.logger.warning("task_retry",
            task_id=task_id,
            task_name=self.task_name,
            retry_count=retry_count,
            countdown_seconds=countdown,
            error_type=type(exc).__name__,
            error_message=str(exc),
            total_retries=metrics.retry_counts[self.task_name]
        )

# Global logger for worker events
worker_logger = logger.get_logger("celery.worker")

# Enhanced Celery signal handlers
@worker_ready.connect
def worker_ready_handler(sender, **kwargs):
    """Log when worker is ready with system info."""
    import platform
    worker_logger.info("worker_ready",
        worker_pid=sender.pid,
        hostname=sender.hostname,
        python_version=platform.python_version(),
        cpu_count=os.cpu_count(),
        demo_mode=DEMO_MODE
    )

@worker_process_init.connect
def worker_process_init_handler(sender, **kwargs):
    """Log worker process initialization."""
    worker_logger.info("worker_process_init",
        worker_pid=os.getpid(),
        parent_pid=os.getppid()
    )

@worker_shutdown.connect  
def worker_shutdown_handler(sender, **kwargs):
    """Log when worker shuts down with final metrics."""
    stats = metrics.get_stats()
    worker_logger.info("worker_shutdown",
        worker_pid=sender.pid,
        hostname=sender.hostname,
        final_metrics=stats
    )

@celeryd_after_setup.connect
def setup_periodic_monitoring(sender, instance, **kwargs):
    """Setup periodic health monitoring."""
    def monitor_health():
        while True:
            time.sleep(10)  # Check every 10 seconds
            stats = metrics.get_stats()
            if stats:
                worker_logger.info("worker_health",
                    task_metrics=stats,
                    total_tasks=sum(s['count'] for s in stats.values()),
                    total_errors=sum(s['errors'] for s in stats.values()),
                    total_retries=sum(s['retries'] for s in stats.values())
                )
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=monitor_health, daemon=True)
    monitor_thread.start()

# Task tracking dictionary
task_start_times = {}
task_contexts = {}  # Store additional context per task

@task_prerun.connect
def task_prerun_handler(sender, task_id, task, args, kwargs, **kwds):
    """Log before task execution with enhanced context."""
    task_start_times[task_id] = time.time()
    task_contexts[task_id] = {
        'start_time': datetime.utcnow().isoformat(),
        'retries': kwargs.get('__retry_count', 0)
    }
    task_logger = CeleryTaskLogger(task.name)
    task_logger.log_task_start(task_id, args, kwargs)

@task_postrun.connect
def task_postrun_handler(sender, task_id, task, args, kwargs, retval, state, **kwds):
    """Log after task execution with detailed metrics."""
    duration = time.time() - task_start_times.pop(task_id, time.time())
    context = task_contexts.pop(task_id, {})
    task_logger = CeleryTaskLogger(task.name)
    
    if state == 'SUCCESS':
        task_logger.log_task_success(task_id, retval, duration)
    else:
        # For non-success states, we might not have exception info here
        worker_logger.warning("task_completed_with_state",
            task_id=task_id,
            task_name=task.name,
            state=state,
            duration_ms=round(duration * 1000, 2),
            retry_count=context.get('retries', 0)
        )

@task_failure.connect
def task_failure_handler(sender, task_id, exception, args, kwargs, traceback, einfo, **kwds):
    """Log task failures with full context."""
    duration = time.time() - task_start_times.pop(task_id, time.time())
    context = task_contexts.get(task_id, {})
    task_logger = CeleryTaskLogger(sender.name)
    task_logger.log_task_failure(task_id, exception, duration)

@task_retry.connect
def task_retry_handler(sender, request, reason, einfo, **kwargs):
    """Log task retry attempts."""
    task_logger = CeleryTaskLogger(sender.name)
    task_logger.log_task_retry(
        request.id,
        reason,
        request.kwargs.get('countdown', 0),
        request.retries
    )

# Enhanced example tasks with real-world patterns

@app.task(bind=True, max_retries=3)
def process_payment(self, order_id: str, amount: float, payment_method: str) -> dict[str, Any]:
    """Process payment with retry logic and detailed logging."""
    task_logger = CeleryTaskLogger("process_payment")
    
    task_logger.logger.info("processing_payment",
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        retry_count=self.request.retries
    )
    
    try:
        # Simulate payment processing
        if random.random() < 0.3:  # 30% chance of transient failure
            raise ConnectionError("Payment gateway timeout")
        
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        transaction_id = f"txn_{order_id}_{int(time.time())}"
        
        task_logger.logger.info("payment_successful",
            order_id=order_id,
            transaction_id=transaction_id,
            amount=amount
        )
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except ConnectionError as exc:
        task_logger.logger.warning("payment_gateway_error",
            order_id=order_id,
            error=str(exc),
            will_retry=self.request.retries < self.max_retries
        )
        # Exponential backoff: 5, 10, 20 seconds
        countdown = 5 * (2 ** self.request.retries)
        raise self.retry(exc=exc, countdown=countdown)

@app.task(bind=True)
def generate_report(self, report_type: str, date_range: dict[str, str], user_id: str) -> dict[str, Any]:
    """Generate report with progress tracking."""
    task_logger = CeleryTaskLogger("generate_report")
    
    task_logger.logger.info("report_generation_started",
        report_type=report_type,
        date_range=date_range,
        user_id=user_id
    )
    
    # Simulate report generation with progress updates
    total_steps = 5
    steps = [
        "Fetching data",
        "Processing records",
        "Calculating metrics",
        "Generating visualizations",
        "Creating PDF"
    ]
    
    for i, step in enumerate(steps, 1):
        task_logger.log_task_progress(self.request.id, i, total_steps, step)
        
        # Update task state for real-time monitoring
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': total_steps, 'status': step}
        )
        
        # Simulate work
        time.sleep(random.uniform(0.5, 1.5))
    
    report_url = f"https://reports.example.com/{report_type}_{self.request.id}.pdf"
    
    task_logger.logger.info("report_generation_complete",
        report_type=report_type,
        report_url=report_url,
        user_id=user_id
    )
    
    return {
        "status": "complete",
        "report_url": report_url,
        "generated_at": datetime.utcnow().isoformat(),
        "pages": random.randint(5, 20)
    }

@app.task
def send_notification(user_id: str, notification_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Send user notification with delivery tracking."""
    task_logger = CeleryTaskLogger("send_notification")
    
    task_logger.logger.info("sending_notification",
        user_id=user_id,
        notification_type=notification_type,
        channels=["email", "push", "sms"]
    )
    
    results = {}
    
    # Simulate multi-channel delivery
    for channel in ["email", "push", "sms"]:
        success = random.random() > 0.1  # 90% success rate
        
        if success:
            task_logger.logger.info(f"{channel}_notification_sent",
                user_id=user_id,
                channel=channel,
                notification_type=notification_type
            )
            results[channel] = {"status": "delivered", "timestamp": datetime.utcnow().isoformat()}
        else:
            task_logger.logger.warning(f"{channel}_notification_failed",
                user_id=user_id,
                channel=channel,
                notification_type=notification_type
            )
            results[channel] = {"status": "failed", "error": "Delivery failed"}
    
    return {
        "user_id": user_id,
        "notification_type": notification_type,
        "delivery_results": results,
        "success_count": sum(1 for r in results.values() if r["status"] == "delivered")
    }

@app.task
def process_batch_data(batch_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    """Process batch data with item-level error handling."""
    task_logger = CeleryTaskLogger("process_batch_data")
    
    task_logger.logger.info("batch_processing_started",
        batch_id=batch_id,
        item_count=len(items)
    )
    
    processed = []
    failed = []
    
    for i, item in enumerate(items):
        try:
            # Simulate processing with occasional failures
            if random.random() < 0.05:  # 5% failure rate
                raise ValueError(f"Invalid data in item {item.get('id', i)}")
            
            # Process item
            processed_item = {
                **item,
                "processed_at": datetime.utcnow().isoformat(),
                "batch_id": batch_id
            }
            processed.append(processed_item)
            
        except Exception as e:
            task_logger.logger.warning("batch_item_failed",
                batch_id=batch_id,
                item_index=i,
                error=str(e)
            )
            failed.append({"index": i, "error": str(e)})
    
    task_logger.logger.info("batch_processing_complete",
        batch_id=batch_id,
        total_items=len(items),
        processed_count=len(processed),
        failed_count=len(failed),
        success_rate=round(len(processed) / len(items) * 100, 1)
    )
    
    return {
        "batch_id": batch_id,
        "processed": len(processed),
        "failed": len(failed),
        "failed_items": failed,
        "success_rate": round(len(processed) / len(items) * 100, 1)
    }

@app.task
def cleanup_old_data(days_to_keep: int = 30) -> dict[str, Any]:
    """Cleanup old data with detailed logging."""
    task_logger = CeleryTaskLogger("cleanup_old_data")
    
    task_logger.logger.info("cleanup_started",
        days_to_keep=days_to_keep,
        cutoff_date=(datetime.utcnow() - timedelta(days=days_to_keep)).isoformat()
    )
    
    # Simulate cleanup of different data types
    cleanup_results = {}
    data_types = ["logs", "temp_files", "cache_entries", "expired_sessions"]
    
    for data_type in data_types:
        # Simulate cleanup with random counts
        cleaned = random.randint(100, 10000)
        size_mb = random.uniform(10, 500)
        
        task_logger.logger.info(f"cleaned_{data_type}",
            data_type=data_type,
            items_removed=cleaned,
            space_freed_mb=round(size_mb, 2)
        )
        
        cleanup_results[data_type] = {
            "items_removed": cleaned,
            "space_freed_mb": round(size_mb, 2)
        }
    
    total_items = sum(r["items_removed"] for r in cleanup_results.values())
    total_space = sum(r["space_freed_mb"] for r in cleanup_results.values())
    
    task_logger.logger.info("cleanup_complete",
        total_items_removed=total_items,
        total_space_freed_mb=round(total_space, 2),
        data_types_cleaned=len(data_types)
    )
    
    return {
        "status": "complete",
        "results": cleanup_results,
        "total_items_removed": total_items,
        "total_space_freed_mb": round(total_space, 2)
    }

def run_demo_worker():
    """Run a demo worker in the same process for demonstration."""
    pout("\n🚀 Starting in-process demo worker...")
    
    # Start worker in a thread
    from celery.worker import WorkController
    
    def start_worker():
        worker = WorkController(app=app, loglevel='INFO')
        worker.start()
    
    worker_thread = threading.Thread(target=start_worker, daemon=True)
    worker_thread.start()
    
    # Give worker time to start
    time.sleep(2)
    pout("✅ Demo worker started!\n")

def demonstrate_task_workflows():
    """Demonstrate various task workflow patterns."""
    demo_logger = logger.get_logger("celery.demo")
    
    pout("\n" + "=" * 60)
    pout("🎯 Demonstrating Rich Celery Task Patterns")
    pout("=" * 60)
    
    # 1. Simple task execution with retries
    pout("\n1️⃣ Payment Processing with Automatic Retries")
    payment_task = process_payment.delay("order_123", 99.99, "credit_card")
    demo_logger.info("submitted_payment_task", task_id=payment_task.id)
    
    # 2. Long-running task with progress tracking
    pout("\n2️⃣ Report Generation with Progress Tracking")
    report_task = generate_report.delay(
        "analytics",
        {"start": "2024-01-01", "end": "2024-01-31"},
        "user_456"
    )
    demo_logger.info("submitted_report_task", task_id=report_task.id)
    
    # Monitor progress
    for _ in range(3):
        time.sleep(1)
        if report_task.state == 'PROGRESS':
            meta = report_task.info
            demo_logger.info("report_progress_update",
                task_id=report_task.id,
                current=meta.get('current', 0),
                total=meta.get('total', 0),
                status=meta.get('status', '')
            )
    
    # 3. Multi-channel notification
    pout("\n3️⃣ Multi-Channel Notification Delivery")
    notification_task = send_notification.delay(
        "user_789",
        "order_confirmation",
        {"order_id": "order_123", "amount": 99.99}
    )
    demo_logger.info("submitted_notification_task", task_id=notification_task.id)
    
    # 4. Batch processing with error handling
    pout("\n4️⃣ Batch Data Processing with Item-Level Error Handling")
    batch_items = [
        {"id": f"item_{i}", "value": random.randint(1, 100)}
        for i in range(50)
    ]
    batch_task = process_batch_data.delay("batch_001", batch_items)
    demo_logger.info("submitted_batch_task", 
        task_id=batch_task.id,
        item_count=len(batch_items)
    )
    
    # 5. Task chains and workflows
    pout("\n5️⃣ Task Chain: Payment → Notification → Cleanup")
    workflow = chain(
        process_payment.s("order_789", 149.99, "paypal"),
        send_notification.s("payment_success", {"amount": 149.99}),
        cleanup_old_data.s(days_to_keep=7)
    )
    workflow_result = workflow.apply_async()
    demo_logger.info("submitted_workflow", workflow_id=workflow_result.id)
    
    # 6. Parallel task group
    pout("\n6️⃣ Parallel Task Group: Multiple Payments")
    payment_group = group(
        process_payment.s(f"order_{i}", random.uniform(10, 200), "credit_card")
        for i in range(5)
    )
    group_result = payment_group.apply_async()
    demo_logger.info("submitted_parallel_group", 
        group_id=group_result.id,
        task_count=5
    )
    
    # Wait for some results
    pout("\n⏳ Waiting for task results...")
    time.sleep(3)
    
    # Collect results
    try:
        payment_result = payment_task.get(timeout=5)
        demo_logger.info("payment_task_completed", 
            task_id=payment_task.id,
            result=payment_result
        )
    except Exception as e:
        demo_logger.error("payment_task_error", 
            task_id=payment_task.id,
            error=str(e)
        )
    
    try:
        report_result = report_task.get(timeout=5)
        demo_logger.info("report_task_completed",
            task_id=report_task.id,
            pages=report_result.get('pages', 0)
        )
    except Exception as e:
        demo_logger.error("report_task_error",
            task_id=report_task.id,
            error=str(e)
        )
    
    try:
        notification_result = notification_task.get(timeout=5)
        demo_logger.info("notification_task_completed",
            task_id=notification_task.id,
            success_count=notification_result.get('success_count', 0)
        )
    except Exception as e:
        demo_logger.error("notification_task_error",
            task_id=notification_task.id,
            error=str(e)
        )
    
    try:
        batch_result = batch_task.get(timeout=5)
        demo_logger.info("batch_task_completed",
            task_id=batch_task.id,
            processed=batch_result.get('processed', 0),
            failed=batch_result.get('failed', 0),
            success_rate=batch_result.get('success_rate', 0)
        )
    except Exception as e:
        demo_logger.error("batch_task_error",
            task_id=batch_task.id,
            error=str(e)
        )
    
    # Display final metrics
    pout("\n📊 Task Execution Metrics")
    pout("=" * 40)
    stats = metrics.get_stats()
    for task_name, task_stats in stats.items():
        pout(f"\n📌 {task_name}:")
        pout(f"   Executions: {task_stats['count']}")
        pout(f"   Success Rate: {task_stats['success_rate']}%")
        pout(f"   Avg Duration: {task_stats['avg_duration_ms']}ms")
        pout(f"   Errors: {task_stats['errors']}")
        pout(f"   Retries: {task_stats['retries']}")
    
    demo_logger.info("demo_completed", final_metrics=stats)

if __name__ == '__main__':
    if DEMO_MODE:
        # Run in demo mode with in-process worker
        pout("🎮 Running in DEMO MODE - No Redis Required!")
        pout("   Using memory broker for demonstration")
        pout("")
        
        # Start demo worker
        run_demo_worker()
        
        # Run demonstrations
        demonstrate_task_workflows()
        
    else:
        # Production mode with Redis
        pout("🔄 Running Celery Integration Example (Production Mode)")
        pout("📝 Make sure you have:")
        pout("   1. Redis running: redis-server")
        pout("   2. Celery worker: celery -A 01_celery_integration worker --loglevel=info")
        pout("")
        pout("💡 Tip: Run with --demo flag to use memory broker without Redis")
        pout("")
        
        demonstrate_task_workflows()
    
    pout("\n✅ Rich Celery Integration Example Completed!")
    pout("\n🎯 Key Patterns Demonstrated:")
    pout("   • Payment processing with automatic retries")
    pout("   • Long-running tasks with progress tracking")
    pout("   • Multi-channel notification delivery")
    pout("   • Batch processing with item-level error handling")
    pout("   • Task chains and workflows")
    pout("   • Parallel task execution")
    pout("   • Comprehensive metrics tracking")
    pout("   • Worker health monitoring")
    pout("   • Structured logging with Foundation")
    pout("\n📊 Check the JSON logs above for detailed task telemetry!")