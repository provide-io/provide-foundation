#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Basic Task Queue Example (No External Dependencies)

Demonstrates Foundation logging for task queue patterns using Python's
built-in asyncio and queue modules. This shows the patterns without
requiring Celery or Redis.

This example simulates task queuing, processing, and monitoring that
would be used in production task queue systems.

Usage:
    python examples/integration/01a_basic_task_queue.py

Expected output:
    Structured logging showing task lifecycle, worker operations,
    and queue monitoring with Foundation's telemetry features."""

import asyncio
from pathlib import Path
import sys
from typing import Any
from uuid import uuid4

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import get_hub, logger, pout
from provide.foundation.errors import error_boundary
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)


class Task:
    """Represents a task to be processed."""

    def __init__(self, task_type: str, data: dict[str, Any], priority: int = 1) -> None:
        self.id = str(uuid4())
        self.type = task_type
        self.data = data
        self.priority = priority
        self.created_at = asyncio.get_event_loop().time()
        self.started_at: float | None = None
        self.completed_at: float | None = None
        self.status = "pending"
        self.result: dict[str, Any] | None = None
        self.error: str | None = None


class TaskQueue:
    """Simple async task queue implementation."""

    def __init__(self, name: str = "default") -> None:
        self.name = name
        self.queue: asyncio.Queue[Task] = asyncio.Queue()
        self.logger = logger.get_logger(f"task_queue.{name}")

    async def enqueue(self, task: Task) -> None:
        """Add a task to the queue."""
        await self.queue.put(task)
        self.logger.info(
            "task_enqueued",
            task_id=task.id,
            task_type=task.type,
            queue_name=self.name,
            priority=task.priority,
            queue_size=self.queue.qsize(),
        )

    async def dequeue(self) -> Task:
        """Get next task from queue."""
        task = await self.queue.get()
        self.logger.info(
            "task_dequeued",
            task_id=task.id,
            task_type=task.type,
            queue_name=self.name,
            wait_time_ms=round((asyncio.get_event_loop().time() - task.created_at) * 1000, 2),
        )
        return task

    def qsize(self) -> int:
        """Get current queue size."""
        return self.queue.qsize()


class TaskWorker:
    """Async worker to process tasks."""

    def __init__(self, worker_id: str, task_queue: TaskQueue) -> None:
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.logger = logger.get_logger(f"task_worker.{worker_id}")
        self.processed_count = 0
        self.failed_count = 0

    async def process_task(self, task: Task) -> None:
        """Process a single task."""
        task.started_at = asyncio.get_event_loop().time()
        task.status = "processing"

        self.logger.info("task_started", task_id=task.id, task_type=task.type, worker_id=self.worker_id)

        with error_boundary(Exception, reraise=False, log_errors=True):
            # Simulate different types of tasks
            if task.type == "email_send":
                await self._process_email_task(task)
            elif task.type == "data_processing":
                await self._process_data_task(task)
            elif task.type == "image_resize":
                await self._process_image_task(task)
            elif task.type == "report_generation":
                await self._process_report_task(task)
            else:
                raise ValueError(f"Unknown task type: {task.type}")

            # Mark as completed
            task.completed_at = asyncio.get_event_loop().time()
            task.status = "completed"
            duration_ms = round((task.completed_at - task.started_at) * 1000, 2)

            self.processed_count += 1
            self.logger.info(
                "task_completed",
                task_id=task.id,
                task_type=task.type,
                worker_id=self.worker_id,
                duration_ms=duration_ms,
                processed_count=self.processed_count,
            )
            return

        # If we get here, there was an error
        task.status = "failed"
        task.completed_at = asyncio.get_event_loop().time()
        duration_ms = round((task.completed_at - task.started_at) * 1000, 2)
        self.failed_count += 1

        self.logger.error(
            "task_failed",
            task_id=task.id,
            task_type=task.type,
            worker_id=self.worker_id,
            duration_ms=duration_ms,
            failed_count=self.failed_count,
        )

    async def _process_email_task(self, task: Task) -> None:
        """Simulate processing an email task."""
        recipient = task.data.get("recipient", "unknown")
        template = task.data.get("template", "default")

        self.logger.info("sending_email", task_id=task.id, recipient=recipient, template=template)

        # Simulate email processing time
        await asyncio.sleep(0.1)

        task.result = {
            "status": "sent",
            "message_id": f"msg_{task.id[:8]}",
            "recipient": recipient,
        }

    async def _process_data_task(self, task: Task) -> None:
        """Simulate processing a data task."""
        records = task.data.get("records", 100)
        operation = task.data.get("operation", "transform")

        self.logger.info("processing_data", task_id=task.id, records=records, operation=operation)

        # Simulate data processing time based on record count
        await asyncio.sleep(records * 0.001)

        task.result = {
            "records_processed": records,
            "operation": operation,
            "output_size": records * 1.2,
        }

    async def _process_image_task(self, task: Task) -> None:
        """Simulate processing an image task."""
        image_url = task.data.get("image_url", "image.jpg")
        target_size = task.data.get("target_size", "thumbnail")

        self.logger.info("resizing_image", task_id=task.id, image_url=image_url, target_size=target_size)

        # Simulate image processing time
        await asyncio.sleep(0.15)

        # Simulate occasional failures
        if "fail" in image_url:
            raise RuntimeError(f"Failed to process image: {image_url}")

        task.result = {
            "original_url": image_url,
            "resized_url": f"resized_{target_size}_{image_url}",
            "target_size": target_size,
        }

    async def _process_report_task(self, task: Task) -> None:
        """Simulate processing a report generation task."""
        report_type = task.data.get("report_type", "summary")
        date_range = task.data.get("date_range", "last_30_days")

        self.logger.info("generating_report", task_id=task.id, report_type=report_type, date_range=date_range)

        # Simulate report generation time
        await asyncio.sleep(0.2)

        task.result = {
            "report_type": report_type,
            "date_range": date_range,
            "file_path": f"reports/{report_type}_{date_range}.pdf",
            "size_bytes": 1024 * 250,
        }

    async def run(self) -> None:
        """Main worker loop."""
        self.logger.info("worker_started", worker_id=self.worker_id)

        try:
            while True:
                task = await self.task_queue.dequeue()
                await self.process_task(task)

        except asyncio.CancelledError:
            self.logger.info(
                "worker_shutdown",
                worker_id=self.worker_id,
                processed_count=self.processed_count,
                failed_count=self.failed_count,
            )
            raise


async def monitor_system(task_queue: TaskQueue, workers: list[TaskWorker]) -> None:
    """Monitor the task processing system."""
    monitor_logger = logger.get_logger("system.monitor")

    while True:
        await asyncio.sleep(1.0)  # Monitor every second

        total_processed = sum(w.processed_count for w in workers)
        total_failed = sum(w.failed_count for w in workers)
        queue_size = task_queue.qsize()

        monitor_logger.info(
            "system_status",
            queue_size=queue_size,
            active_workers=len(workers),
            total_processed=total_processed,
            total_failed=total_failed,
            success_rate=round((total_processed / max(total_processed + total_failed, 1)) * 100, 1),
        )


async def basic_task_queue_example() -> None:
    """Demonstrate basic task queue patterns with Foundation logging."""
    pout("\n" + "=" * 60)
    pout("🔄 Basic Task Queue Example")
    pout(" Demonstrates: Task queuing, processing, and monitoring patterns")
    pout("=" * 60)

    # Setup telemetry with JSON formatting for structured task logs
    get_hub().initialize_foundation(
        TelemetryConfig(
            service_name="task-queue-demo",
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
            ),
        ),
    )

    # Create task queue and workers
    task_queue = TaskQueue("main")
    workers = [
        TaskWorker("worker-1", task_queue),
        TaskWorker("worker-2", task_queue),
        TaskWorker("worker-3", task_queue),
    ]

    logger.info("system_startup", queue_name=task_queue.name, worker_count=len(workers))

    # Create various tasks
    tasks = [
        Task("email_send", {"recipient": "user@example.com", "template": "welcome"}, priority=1),
        Task("data_processing", {"records": 500, "operation": "transform"}, priority=2),
        Task("image_resize", {"image_url": "profile.jpg", "target_size": "thumbnail"}, priority=1),
        Task("report_generation", {"report_type": "analytics", "date_range": "last_7_days"}, priority=3),
        Task("email_send", {"recipient": "admin@example.com", "template": "notification"}, priority=1),
        Task("data_processing", {"records": 1000, "operation": "aggregate"}, priority=2),
        Task(
            "image_resize", {"image_url": "fail_image.jpg", "target_size": "large"}, priority=1
        ),  # This will fail
        Task("report_generation", {"report_type": "performance", "date_range": "last_30_days"}, priority=3),
    ]

    # Start workers
    worker_tasks = [asyncio.create_task(worker.run()) for worker in workers]

    # Start monitoring
    monitor_task = asyncio.create_task(monitor_system(task_queue, workers))

    # Enqueue tasks with some delay
    for i, task in enumerate(tasks):
        await task_queue.enqueue(task)
        if i < len(tasks) - 1:  # Don't sleep after last task
            await asyncio.sleep(0.2)  # Stagger task submissions

    logger.info("all_tasks_enqueued", task_count=len(tasks))

    # Let workers process for a few seconds
    await asyncio.sleep(3.0)

    # Shutdown
    logger.info("shutting_down_system")
    monitor_task.cancel()
    for task in worker_tasks:
        task.cancel()

    # Wait for clean shutdown
    await asyncio.gather(*worker_tasks, monitor_task, return_exceptions=True)

    # Final statistics
    total_processed = sum(w.processed_count for w in workers)
    total_failed = sum(w.failed_count for w in workers)

    logger.info(
        "system_shutdown_complete",
        tasks_submitted=len(tasks),
        tasks_processed=total_processed,
        tasks_failed=total_failed,
        final_queue_size=task_queue.qsize(),
    )


if __name__ == "__main__":
    asyncio.run(basic_task_queue_example())

# 🧱🏗️🔚
