#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Setup and Configuration

This module contains the core Celery app setup, configuration, and
telemetry initialization for the provide.foundation Celery integration example.

Part 1 of 4: Setup and Configuration
- Celery app initialization with filesystem backend
- Telemetry configuration for structured logging
- Self-contained operation (no Redis required)

Usage:
    from examples.integration.celery.setup_and_config import app, setup_celery_logging"""

from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Handle optional Celery dependency
try:
    from celery import Celery

    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

from provide.foundation import logger, perr, pout, setup_telemetry
from provide.foundation.logger.config import (
    LoggingConfig,
    TelemetryConfig,
)


def setup_celery_logging() -> None:
    """Configure comprehensive logging for Celery workers."""
    config = TelemetryConfig(
        service_name="celery-foundation-example",
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            module_levels={
                "celery.worker": "INFO",
                "celery.task": "INFO",
                "celery.beat": "INFO",
                "celery.app.trace": "INFO",
                "billiard": "WARNING",
                "kombu": "WARNING",
            },
        ),
    )
    setup_telemetry(config)


if not CELERY_AVAILABLE:
    perr("❌ Celery is not installed!")
    perr("💡 Install with: uv add celery")
    perr("📝 This example uses filesystem backend (no Redis required)")
    exit(1)

# Configure telemetry for the example
setup_celery_logging()

# Create Celery app with filesystem backend
app = Celery("celery_foundation_example")

# Setup filesystem directories
temp_dir = Path("/tmp/celery_foundation")
temp_dir.mkdir(exist_ok=True)

# Create required directories for filesystem transport
(temp_dir / "out").mkdir(exist_ok=True)
(temp_dir / "processed").mkdir(exist_ok=True)
(temp_dir / "results").mkdir(exist_ok=True)

app.conf.update(
    broker_url="filesystem://",
    broker_transport_options={
        "data_folder_in": str(temp_dir / "out"),
        "data_folder_out": str(temp_dir / "out"),
        "data_folder_processed": str(temp_dir / "processed"),
    },
    result_backend=f"file://{temp_dir}/results",
    task_always_eager=False,  # Use actual worker pool
    task_eager_propagates=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
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


class CeleryTaskLogger:
    """Enhanced task-specific logging with metrics."""

    def __init__(self, task_name: str) -> None:
        self.logger = logger.get_logger(f"celery.task.{task_name}")
        self.task_name = task_name

    def log_task_start(self, task_id: str, args: tuple, kwargs: dict) -> None:
        """Log task execution start with context."""
        self.logger.info(
            "task_started",
            task_id=task_id,
            task_name=self.task_name,
            args_count=len(args),
            kwargs_count=len(kwargs),
            args_preview=str(args)[:200] if args else None,
            kwargs_preview=str(kwargs)[:200] if kwargs else None,
            queue="default",
            worker_hostname=app.conf.get("worker_hostname", "unknown"),
        )

    def log_task_progress(self, task_id: str, current: int, total: int, message: str = "") -> None:
        """Log task progress for long-running tasks."""
        progress_pct = round((current / total) * 100, 1) if total > 0 else 0
        self.logger.info(
            "task_progress",
            task_id=task_id,
            task_name=self.task_name,
            current=current,
            total=total,
            progress_pct=progress_pct,
            message=message,
        )

    def log_task_success(self, task_id: str, result, duration: float, metrics_tracker) -> None:
        """Log successful task completion with metrics."""
        metrics_tracker.record_execution(self.task_name, duration, True)
        self.logger.info(
            "task_completed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            result_type=type(result).__name__,
            success=True,
            total_executions=metrics_tracker.task_counts[self.task_name],
        )

    def log_task_failure(self, task_id: str, error: Exception, duration: float, metrics_tracker) -> None:
        """Log task failure with context."""
        metrics_tracker.record_execution(self.task_name, duration, False)
        self.logger.error(
            "task_failed",
            task_id=task_id,
            task_name=self.task_name,
            duration_ms=round(duration * 1000, 2),
            error_type=type(error).__name__,
            error_message=str(error),
            success=False,
            total_errors=metrics_tracker.error_counts[self.task_name],
        )

    def log_task_retry(
        self, task_id: str, exc: Exception, countdown: int, retry_count: int, metrics_tracker
    ) -> None:
        """Log task retry attempt."""
        metrics_tracker.record_retry(self.task_name)
        self.logger.warning(
            "task_retry",
            task_id=task_id,
            task_name=self.task_name,
            retry_count=retry_count,
            countdown_seconds=countdown,
            error_type=type(exc).__name__,
            error_message=str(exc),
            total_retries=metrics_tracker.retry_counts[self.task_name],
        )


if __name__ == "__main__":
    pout(f"📊 Broker: {app.conf.broker_url}")
    pout(f"💾 Result backend: {app.conf.result_backend}")

# 🧱🏗️🔚
