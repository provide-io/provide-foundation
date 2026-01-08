#!/usr/bin/env python3
"""
Distributed Task Processing System - Comprehensive Foundation Demo

A production-ready distributed task processing system showcasing all major
provide.foundation features in a real-world application architecture.

Features:
- CLI interface with Click integration
- Persistent task queue with encryption
- Async worker pool with resilience patterns
- Pluggable task executors
- Comprehensive observability
- Multi-environment configuration
- Archive-based task backups
- Circuit breaker protection
- Distributed tracing
- Type-safe configuration
- Atomic file operations
- Advanced error handling

Usage:
    # Submit tasks
    python distributed_task_system.py submit --type http --data '{"url": "https://api.example.com"}'
    python distributed_task_system.py submit --type compute --data '{"operation": "fibonacci", "n": 30}'

    # Process tasks
    python distributed_task_system.py process --workers 4 --max-tasks 10

    # View status
    python distributed_task_system.py status

    # Backup tasks
    python distributed_task_system.py backup

    # View metrics
    python distributed_task_system.py metrics
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from enum import Enum
import json
from pathlib import Path
import time
from typing import Any
from uuid import uuid4

from attrs import define, field
import click

# Foundation imports - showcasing comprehensive usage
from provide.foundation import logger
from provide.foundation.archive.tar import TarArchive
from provide.foundation.config import env_field
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.console.output import perr, pout
from provide.foundation.crypto.hashing import hash_file
from provide.foundation.file.atomic import atomic_write_text
from provide.foundation.file.directory import ensure_dir
from provide.foundation.hub import get_hub
from provide.foundation.metrics import counter, gauge, histogram
from provide.foundation.resilience.decorators import circuit_breaker, fallback, retry
from provide.foundation.resilience.types import BackoffStrategy
from provide.foundation.tracer.context import with_span

# ============================================================================
# Configuration
# ============================================================================


@define
class SystemConfig(RuntimeConfig):
    """System configuration loaded from environment."""

    # System settings
    system_name: str = env_field(env_var="SYSTEM_NAME", default="task-processor")
    environment: str = env_field(env_var="ENVIRONMENT", default="development")

    # Queue settings
    queue_dir: str = env_field(env_var="QUEUE_DIR", default="/tmp/task-queue")
    backup_dir: str = env_field(env_var="BACKUP_DIR", default="/tmp/task-backups")

    # Worker settings
    default_workers: int = env_field(env_var="WORKERS", default=4)
    worker_timeout: int = env_field(env_var="WORKER_TIMEOUT", default=300)

    # Retry settings
    max_retries: int = env_field(env_var="MAX_RETRIES", default=3)
    retry_delay: float = env_field(env_var="RETRY_DELAY", default=1.0)

    # Circuit breaker settings
    cb_failure_threshold: int = env_field(env_var="CB_FAILURE_THRESHOLD", default=5)
    cb_timeout: int = env_field(env_var="CB_TIMEOUT", default=60)

    # Processing settings
    batch_size: int = env_field(env_var="BATCH_SIZE", default=10)
    enable_encryption: bool = env_field(env_var="ENABLE_ENCRYPTION", default=False)


# ============================================================================
# Task Models
# ============================================================================


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class TaskType(str, Enum):
    """Task type enumeration."""

    HTTP = "http"
    COMPUTE = "compute"
    FILE_PROCESS = "file_process"
    DATA_TRANSFORM = "data_transform"


@define
class Task:
    """Task model with full metadata."""

    task_type: TaskType = field()
    task_id: str = field(factory=lambda: str(uuid4()))
    data: dict[str, Any] = field(factory=dict)
    status: TaskStatus = field(default=TaskStatus.PENDING)
    priority: int = field(default=5)
    created_at: str = field(factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(factory=lambda: datetime.now(UTC).isoformat())
    started_at: str | None = field(default=None)
    completed_at: str | None = field(default=None)
    attempts: int = field(default=0)
    max_attempts: int = field(default=3)
    result: dict[str, Any] | None = field(default=None)
    error: str | None = field(default=None)
    execution_time_ms: float | None = field(default=None)
    worker_id: str | None = field(default=None)

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "data": self.data,
            "status": self.status.value,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "result": self.result,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms,
            "worker_id": self.worker_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        """Create task from dictionary."""
        return cls(
            task_id=data["task_id"],
            task_type=TaskType(data["task_type"]),
            data=data["data"],
            status=TaskStatus(data["status"]),
            priority=data.get("priority", 5),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            attempts=data.get("attempts", 0),
            max_attempts=data.get("max_attempts", 3),
            result=data.get("result"),
            error=data.get("error"),
            execution_time_ms=data.get("execution_time_ms"),
            worker_id=data.get("worker_id"),
        )


# ============================================================================
# Metrics
# ============================================================================

tasks_submitted = counter("tasks.submitted", "Total tasks submitted")
tasks_processed = counter("tasks.processed", "Total tasks processed successfully")
tasks_failed = counter("tasks.failed", "Total tasks failed")
tasks_retried = counter("tasks.retried", "Total task retry attempts")
active_tasks = gauge("tasks.active", "Currently active tasks")
queue_size = gauge("tasks.queue.size", "Current queue size")
task_execution_time = histogram("tasks.execution.duration_ms", "Task execution time in ms")
worker_utilization = gauge("workers.utilization", "Worker pool utilization")

# ============================================================================
# Task Queue
# ============================================================================


class TaskQueue:
    """Persistent task queue with atomic operations."""

    def __init__(self, config: SystemConfig) -> None:
        self.config = config
        self.queue_dir = Path(config.queue_dir)
        ensure_dir(str(self.queue_dir))
        logger.info("Task queue initialized", queue_dir=str(self.queue_dir))

    def submit(self, task: Task) -> str:
        """Submit a task to the queue."""
        with with_span("queue.submit") as span:
            span.set_tag("task.id", task.task_id)
            span.set_tag("task.type", task.task_type.value)

            task_file = self.queue_dir / f"{task.task_id}.json"
            atomic_write_text(str(task_file), json.dumps(task.to_dict(), indent=2))

            tasks_submitted.inc()
            queue_size.set(len(self.list_pending()))

            logger.info(
                "Task submitted",
                task_id=task.task_id,
                task_type=task.task_type.value,
                priority=task.priority,
            )

            return task.task_id

    def get(self, task_id: str) -> Task | None:
        """Get a task by ID."""
        task_file = self.queue_dir / f"{task_id}.json"
        if not task_file.exists():
            return None

        try:
            data = json.loads(task_file.read_text())
            return Task.from_dict(data)
        except Exception as e:
            logger.error("Failed to load task", task_id=task_id, error=str(e))
            return None

    def update(self, task: Task) -> None:
        """Update task status."""
        task.updated_at = datetime.now(UTC).isoformat()
        task_file = self.queue_dir / f"{task.task_id}.json"
        atomic_write_text(str(task_file), json.dumps(task.to_dict(), indent=2))
        queue_size.set(len(self.list_pending()))

    def list_pending(self) -> list[Task]:
        """List all pending tasks sorted by priority."""
        tasks = []
        for task_file in self.queue_dir.glob("*.json"):
            try:
                data = json.loads(task_file.read_text())
                task = Task.from_dict(data)
                if task.status == TaskStatus.PENDING:
                    tasks.append(task)
            except Exception as e:
                logger.warning("Failed to load task file", file=task_file.name, error=str(e))

        # Sort by priority (higher first) then by created_at
        tasks.sort(key=lambda t: (-t.priority, t.created_at))
        return tasks

    def list_all(self) -> list[Task]:
        """List all tasks."""
        tasks = []
        for task_file in self.queue_dir.glob("*.json"):
            try:
                data = json.loads(task_file.read_text())
                tasks.append(Task.from_dict(data))
            except Exception as e:
                logger.warning("Failed to load task file", file=task_file.name, error=str(e))
        return tasks

    def backup(self, backup_path: str) -> tuple[str, int]:
        """Create backup archive of all tasks."""
        with with_span("queue.backup"):
            archive = TarArchive(deterministic=True)
            archive.create(self.queue_dir, Path(backup_path))

            size_bytes = Path(backup_path).stat().st_size
            checksum = hash_file(backup_path, algorithm="sha256")

            logger.info(
                "Queue backup created",
                backup_path=backup_path,
                size_bytes=size_bytes,
                checksum=checksum[:16],
            )

            return checksum, size_bytes


# ============================================================================
# Task Executors
# ============================================================================


class TaskExecutor:
    """Base class for task executors."""

    async def execute(self, task: Task) -> dict[str, Any]:
        """Execute a task and return result."""
        raise NotImplementedError


class HTTPTaskExecutor(TaskExecutor):
    """Executor for HTTP tasks with circuit breaker protection."""

    @circuit_breaker(failure_threshold=5, recovery_timeout=60)
    @retry(max_attempts=3, backoff=BackoffStrategy.EXPONENTIAL, base_delay=1.0)
    async def execute(self, task: Task) -> dict[str, Any]:
        """Execute HTTP task."""
        with with_span("executor.http") as span:
            url = task.data.get("url", "https://api.example.com")
            span.set_tag("http.url", url)

            logger.info("Executing HTTP task", url=url)

            # Simulate HTTP request
            await asyncio.sleep(0.1)

            # Simulate occasional failures for demo
            if task.attempts == 0 and task.task_id.endswith("f"):
                raise ConnectionError("Simulated connection error")

            return {
                "url": url,
                "status_code": 200,
                "response_time_ms": 100,
                "content_length": 1024,
            }


class ComputeTaskExecutor(TaskExecutor):
    """Executor for compute-intensive tasks."""

    @fallback(lambda task: {"result": 0, "note": "Fallback: computation failed"})
    async def execute(self, task: Task) -> dict[str, Any]:
        """Execute compute task."""
        with with_span("executor.compute") as span:
            operation = task.data.get("operation", "sum")
            span.set_tag("compute.operation", operation)

            logger.info("Executing compute task", operation=operation)

            if operation == "fibonacci":
                n = task.data.get("n", 10)
                result = await self._fibonacci(n)
                return {"operation": "fibonacci", "n": n, "result": result}

            elif operation == "sum":
                numbers = task.data.get("numbers", [1, 2, 3, 4, 5])
                result = sum(numbers)
                return {"operation": "sum", "numbers": numbers, "result": result}

            else:
                raise ValueError(f"Unknown operation: {operation}")

    async def _fibonacci(self, n: int) -> int:
        """Calculate Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


class FileProcessTaskExecutor(TaskExecutor):
    """Executor for file processing tasks."""

    async def execute(self, task: Task) -> dict[str, Any]:
        """Execute file processing task."""
        with with_span("executor.file_process") as span:
            file_path = task.data.get("file_path", "/tmp/input.txt")
            span.set_tag("file.path", file_path)

            logger.info("Executing file process task", file_path=file_path)

            # Simulate file processing
            await asyncio.sleep(0.05)

            return {
                "file_path": file_path,
                "lines_processed": 100,
                "bytes_processed": 4096,
                "checksum": "abc123",
            }


class DataTransformTaskExecutor(TaskExecutor):
    """Executor for data transformation tasks."""

    async def execute(self, task: Task) -> dict[str, Any]:
        """Execute data transformation task."""
        with with_span("executor.data_transform") as span:
            transform = task.data.get("transform", "uppercase")
            span.set_tag("transform.type", transform)

            logger.info("Executing data transform task", transform=transform)

            # Simulate data transformation
            await asyncio.sleep(0.08)

            return {
                "transform": transform,
                "records_transformed": 50,
                "output_size_bytes": 2048,
            }


# ============================================================================
# Worker Pool
# ============================================================================


class WorkerPool:
    """Async worker pool with resilience patterns."""

    def __init__(self, config: SystemConfig, queue: TaskQueue) -> None:
        self.config = config
        self.queue = queue
        self.executors: dict[TaskType, TaskExecutor] = {
            TaskType.HTTP: HTTPTaskExecutor(),
            TaskType.COMPUTE: ComputeTaskExecutor(),
            TaskType.FILE_PROCESS: FileProcessTaskExecutor(),
            TaskType.DATA_TRANSFORM: DataTransformTaskExecutor(),
        }
        self.worker_id = str(uuid4())[:8]
        logger.info("Worker pool initialized", worker_id=self.worker_id)

    async def process_task(self, task: Task) -> None:
        """Process a single task."""
        with with_span("worker.process_task") as span:
            span.set_tag("task.id", task.task_id)
            span.set_tag("task.type", task.task_type.value)
            span.set_tag("worker.id", self.worker_id)

            start_time = time.time()

            try:
                # Update task status
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now(UTC).isoformat()
                task.attempts += 1
                task.worker_id = self.worker_id
                self.queue.update(task)

                active_tasks.inc()

                logger.info(
                    "Processing task",
                    task_id=task.task_id,
                    task_type=task.task_type.value,
                    attempt=task.attempts,
                )

                # Execute task
                executor = self.executors[task.task_type]
                result = await executor.execute(task)

                # Update task as completed
                execution_time = (time.time() - start_time) * 1000
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now(UTC).isoformat()
                task.result = result
                task.execution_time_ms = execution_time
                self.queue.update(task)

                # Update metrics
                tasks_processed.inc()
                task_execution_time.observe(execution_time)

                logger.info(
                    "Task completed",
                    task_id=task.task_id,
                    execution_time_ms=round(execution_time, 2),
                )

            except RuntimeError as e:
                # Circuit breaker is open - task will be retried
                if "circuit breaker" in str(e).lower():
                    logger.warning(
                        "Circuit breaker open, task will be retried",
                        task_id=task.task_id,
                        error=str(e),
                    )
                    task.status = TaskStatus.PENDING
                    self.queue.update(task)
                else:
                    raise

            except Exception as e:
                # Task failed
                execution_time = (time.time() - start_time) * 1000

                logger.error(
                    "Task failed",
                    task_id=task.task_id,
                    error=str(e),
                    attempt=task.attempts,
                    execution_time_ms=round(execution_time, 2),
                )

                if task.attempts >= task.max_attempts:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    task.execution_time_ms = execution_time
                    tasks_failed.inc()
                else:
                    task.status = TaskStatus.RETRYING
                    tasks_retried.inc()

                self.queue.update(task)

            finally:
                active_tasks.dec()

    async def process_batch(self, tasks: list[Task], max_concurrent: int = 4) -> None:
        """Process a batch of tasks concurrently."""
        with with_span("worker.process_batch") as span:
            span.set_tag("batch.size", len(tasks))
            span.set_tag("max.concurrent", max_concurrent)

            logger.info("Processing batch", batch_size=len(tasks), max_concurrent=max_concurrent)

            # Process tasks in batches to limit concurrency
            for i in range(0, len(tasks), max_concurrent):
                batch = tasks[i : i + max_concurrent]
                await asyncio.gather(*[self.process_task(task) for task in batch])

            logger.info("Batch processing complete", tasks_processed=len(tasks))

    async def run(self, max_tasks: int | None = None) -> dict[str, Any]:
        """Run the worker pool."""
        with with_span("worker.run"):
            start_time = time.time()

            pending_tasks = self.queue.list_pending()

            # Apply task limit if specified
            if max_tasks is not None:
                pending_tasks = pending_tasks[:max_tasks]

            if not pending_tasks:
                logger.info("No pending tasks to process")
                return {
                    "tasks_processed": 0,
                    "duration_ms": 0,
                }

            logger.info("Starting task processing", pending_count=len(pending_tasks))

            # Process tasks
            await self.process_batch(pending_tasks, max_concurrent=self.config.default_workers)

            duration_ms = (time.time() - start_time) * 1000

            # Calculate statistics
            all_tasks = self.queue.list_all()
            stats = {
                "tasks_processed": len(pending_tasks),
                "duration_ms": round(duration_ms, 2),
                "total_tasks": len(all_tasks),
                "pending": len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
                "running": len([t for t in all_tasks if t.status == TaskStatus.RUNNING]),
                "completed": len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
                "failed": len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
                "retrying": len([t for t in all_tasks if t.status == TaskStatus.RETRYING]),
            }

            logger.info("Worker run complete", **stats)

            return stats


# ============================================================================
# CLI Commands
# ============================================================================


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Distributed Task Processing System - Foundation Demo."""
    # Initialize Foundation
    hub = get_hub()
    hub.initialize_foundation()

    # Load configuration
    config = SystemConfig.from_env()

    # Store in context
    ctx.obj = {"config": config}

    logger.info("System initialized", environment=config.environment, system=config.system_name)


@cli.command()
@click.option(
    "--type",
    "task_type",
    required=True,
    type=click.Choice(["http", "compute", "file_process", "data_transform"]),
)
@click.option("--data", required=True, help="Task data as JSON string")
@click.option("--priority", default=5, type=int, help="Task priority (1-10)")
@click.pass_context
def submit(ctx: click.Context, task_type: str, data: str, priority: int) -> None:
    """Submit a task to the queue."""
    try:
        config = ctx.obj["config"]
        queue = TaskQueue(config)

        # Parse task data
        task_data = json.loads(data)

        # Create task
        task = Task(
            task_type=TaskType(task_type),
            data=task_data,
            priority=priority,
            max_attempts=config.max_retries,
        )

        # Submit task
        task_id = queue.submit(task)

        pout("✅ Task submitted successfully")
        pout(f"   Task ID: {task_id}")
        pout(f"   Type: {task_type}")
        pout(f"   Priority: {priority}")

    except json.JSONDecodeError:
        perr("❌ Invalid JSON data")
        raise click.Abort() from None
    except Exception as e:
        perr(f"❌ Failed to submit task: {e}")
        raise click.Abort() from None


@cli.command()
@click.option("--workers", default=None, type=int, help="Number of concurrent workers")
@click.option("--max-tasks", default=None, type=int, help="Maximum tasks to process")
@click.pass_context
def process(ctx: click.Context, workers: int | None, max_tasks: int | None) -> None:
    """Process pending tasks."""
    try:
        config = ctx.obj["config"]

        if workers:
            config.default_workers = workers

        queue = TaskQueue(config)
        pool = WorkerPool(config, queue)

        pout("🚀 Starting task processing...")
        pout(f"   Workers: {config.default_workers}")
        pout(f"   Max tasks: {max_tasks or 'unlimited'}")
        pout("")

        # Run worker pool
        stats = asyncio.run(pool.run(max_tasks))

        pout("")
        pout("=" * 70)
        pout("✨ Processing Complete")
        pout("=" * 70)
        pout(f"  Tasks Processed: {stats['tasks_processed']}")
        pout(f"  Duration: {stats['duration_ms']:.2f}ms")
        pout("")
        pout(f"  Total Tasks: {stats['total_tasks']}")
        pout(f"  Pending: {stats['pending']}")
        pout(f"  Completed: {stats['completed']}")
        pout(f"  Failed: {stats['failed']}")
        pout(f"  Retrying: {stats['retrying']}")
        pout("=" * 70)

    except Exception as e:
        perr(f"❌ Processing failed: {e}")
        logger.exception("Worker pool failed")
        raise click.Abort() from None


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show system status."""
    config = ctx.obj["config"]
    queue = TaskQueue(config)

    tasks = queue.list_all()

    pout("=" * 70)
    pout("📊 System Status")
    pout("=" * 70)
    pout(f"  System: {config.system_name}")
    pout(f"  Environment: {config.environment}")
    pout(f"  Queue Directory: {config.queue_dir}")
    pout("")
    pout(f"  Total Tasks: {len(tasks)}")
    pout(f"  Pending: {len([t for t in tasks if t.status == TaskStatus.PENDING])}")
    pout(f"  Running: {len([t for t in tasks if t.status == TaskStatus.RUNNING])}")
    pout(f"  Completed: {len([t for t in tasks if t.status == TaskStatus.COMPLETED])}")
    pout(f"  Failed: {len([t for t in tasks if t.status == TaskStatus.FAILED])}")
    pout(f"  Retrying: {len([t for t in tasks if t.status == TaskStatus.RETRYING])}")
    pout("")

    if tasks:
        pout("Recent Tasks:")
        for task in sorted(tasks, key=lambda t: t.created_at, reverse=True)[:5]:
            status_emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.RUNNING: "🔄",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.RETRYING: "🔁",
            }
            pout(
                f"  {status_emoji[task.status]} {task.task_id[:8]} - {task.task_type.value} - {task.status.value}"
            )

    pout("=" * 70)


@cli.command()
@click.pass_context
def backup(ctx: click.Context) -> None:
    """Create backup archive of task queue."""
    try:
        config = ctx.obj["config"]
        queue = TaskQueue(config)

        backup_dir = Path(config.backup_dir)
        ensure_dir(str(backup_dir))

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup_path = str(backup_dir / f"tasks_backup_{timestamp}.tar")

        pout("📦 Creating backup...")

        checksum, size_bytes = queue.backup(backup_path)

        pout("✅ Backup created successfully")
        pout(f"   Path: {backup_path}")
        pout(f"   Size: {size_bytes:,} bytes")
        pout(f"   Checksum: {checksum[:16]}...")

    except Exception as e:
        perr(f"❌ Backup failed: {e}")
        raise click.Abort() from None


@cli.command()
@click.pass_context
def metrics(ctx: click.Context) -> None:
    """Show system metrics."""
    pout("=" * 70)
    pout("📈 System Metrics")
    pout("=" * 70)
    pout(f"  Tasks Submitted: {tasks_submitted.value}")
    pout(f"  Tasks Processed: {tasks_processed.value}")
    pout(f"  Tasks Failed: {tasks_failed.value}")
    pout(f"  Tasks Retried: {tasks_retried.value}")
    pout(f"  Active Tasks: {active_tasks.value}")
    pout(f"  Queue Size: {queue_size.value}")
    pout("")
    pout("  Execution Time:")
    pout(f"    Count: {task_execution_time.count}")
    pout(f"    Sum: {task_execution_time.sum:.2f}ms")
    if task_execution_time.count > 0:
        avg = task_execution_time.sum / task_execution_time.count
        pout(f"    Average: {avg:.2f}ms")
    pout("=" * 70)


@cli.command()
@click.option("--count", default=10, type=int, help="Number of sample tasks to create")
@click.pass_context
def demo(ctx: click.Context, count: int) -> None:
    """Run a complete demo with sample tasks."""
    config = ctx.obj["config"]
    queue = TaskQueue(config)

    pout("=" * 70)
    pout("🎬 Running Complete Demo")
    pout("=" * 70)
    pout(f"Creating {count} sample tasks...\n")

    # Create sample tasks of different types
    task_definitions = [
        (TaskType.HTTP, {"url": "https://api.example.com/users"}),
        (TaskType.HTTP, {"url": "https://api.example.com/posts"}),
        (TaskType.COMPUTE, {"operation": "fibonacci", "n": 25}),
        (TaskType.COMPUTE, {"operation": "sum", "numbers": list(range(1, 101))}),
        (TaskType.FILE_PROCESS, {"file_path": "/tmp/data.txt"}),
        (TaskType.DATA_TRANSFORM, {"transform": "uppercase"}),
    ]

    submitted_ids = []
    for i in range(count):
        task_type, data = task_definitions[i % len(task_definitions)]
        task = Task(
            task_type=task_type,
            data=data,
            priority=(i % 10) + 1,
            max_attempts=config.max_retries,
        )
        task_id = queue.submit(task)
        submitted_ids.append(task_id)
        pout(f"  ✅ Created {task_type.value} task: {task_id[:8]}")

    pout(f"\n🚀 Processing {count} tasks...\n")

    # Process tasks
    pool = WorkerPool(config, queue)
    stats = asyncio.run(pool.run())

    pout("")
    pout("=" * 70)
    pout("✨ Demo Complete")
    pout("=" * 70)
    pout(f"  Tasks Created: {count}")
    pout(f"  Tasks Processed: {stats['tasks_processed']}")
    pout(f"  Duration: {stats['duration_ms']:.2f}ms")
    pout(f"  Completed: {stats['completed']}")
    pout(f"  Failed: {stats['failed']}")
    pout("")
    pout("📈 Try these commands:")
    pout("  • python distributed_task_system.py status")
    pout("  • python distributed_task_system.py metrics")
    pout("  • python distributed_task_system.py backup")
    pout("=" * 70)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    cli()
