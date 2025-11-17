#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Metrics Tracking and Signal Handlers

This module contains the metrics tracking system and Celery signal handlers
for comprehensive monitoring and logging of Celery operations.

Part 2 of 4: Metrics and Signal Handlers
- TaskMetrics class for execution tracking
- Celery signal handlers for worker lifecycle events
- Task execution monitoring with detailed metrics
- Periodic health monitoring

Usage:
    from examples.integration.celery.metrics_and_signals import metrics, setup_signal_handlers"""

from collections import defaultdict
import os
from pathlib import Path
import platform
import sys
import threading
import time
from typing import Any

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import logger

# Import Celery signal types
try:
    from celery.signals import (
        celeryd_after_setup,
        task_failure,
        task_postrun,
        task_prerun,
        task_retry,
        worker_process_init,
        worker_ready,
        worker_shutdown,
    )

    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False


class TaskMetrics:
    """Track task execution metrics."""

    def __init__(self) -> None:
        self.task_counts = defaultdict(int)
        self.task_durations = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.retry_counts = defaultdict(int)
        self.lock = threading.Lock()

    def record_execution(self, task_name: str, duration: float, success: bool) -> None:
        with self.lock:
            self.task_counts[task_name] += 1
            self.task_durations[task_name].append(duration)
            if not success:
                self.error_counts[task_name] += 1

    def record_retry(self, task_name: str) -> None:
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
                    "success_rate": round(
                        (1 - self.error_counts[task_name] / self.task_counts[task_name]) * 100, 1
                    ),
                }
            return stats


# Global metrics instance
metrics = TaskMetrics()

# Global logger for worker events
worker_logger = logger.get_logger("celery.worker")

# Task tracking dictionaries
task_start_times = {}
task_contexts = {}  # Store additional context per task


def setup_signal_handlers(app) -> None:
    """Set up all Celery signal handlers."""
    # Import task logger after app setup
    import importlib.util
    from pathlib import Path

    def load_module_from_file(name, filepath):
        spec = importlib.util.spec_from_file_location(name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    current_dir = Path(__file__).parent
    setup_config = load_module_from_file("setup_and_config", current_dir / "01_setup_and_config.py")
    CeleryTaskLogger = setup_config.CeleryTaskLogger

    @worker_ready.connect
    def worker_ready_handler(sender, **kwargs) -> None:
        """Log when worker is ready with system info."""
        worker_logger.info(
            "worker_ready",
            worker_pid=sender.pid,
            hostname=sender.hostname,
            python_version=platform.python_version(),
            cpu_count=os.cpu_count(),
            transport="filesystem",
            backend="file",
        )

    @worker_process_init.connect
    def worker_process_init_handler(sender, **kwargs) -> None:
        """Log worker process initialization."""
        worker_logger.info(
            "worker_process_init",
            worker_pid=os.getpid(),
            parent_pid=os.getppid(),
        )

    @worker_shutdown.connect
    def worker_shutdown_handler(sender, **kwargs) -> None:
        """Log when worker shuts down with final metrics."""
        stats = metrics.get_stats()
        worker_logger.info(
            "worker_shutdown",
            worker_pid=sender.pid,
            hostname=sender.hostname,
            final_metrics=stats,
        )

    @celeryd_after_setup.connect
    def setup_periodic_monitoring(sender, instance, **kwargs) -> None:
        """Setup periodic health monitoring."""

        def monitor_health() -> None:
            while True:
                time.sleep(10)  # Check every 10 seconds
                stats = metrics.get_stats()
                if stats:
                    worker_logger.info(
                        "worker_health",
                        task_metrics=stats,
                        total_tasks=sum(s["count"] for s in stats.values()),
                        total_errors=sum(s["errors"] for s in stats.values()),
                        total_retries=sum(s["retries"] for s in stats.values()),
                    )

        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_health, daemon=True)
        monitor_thread.start()

    @task_prerun.connect
    def task_prerun_handler(sender, task_id, task, args, kwargs, **kwds) -> None:
        """Log before task execution with enhanced context."""
        task_start_times[task_id] = time.time()
        task_contexts[task_id] = {
            "start_time": time.time(),
            "retries": kwargs.get("__retry_count", 0),
        }
        task_logger = CeleryTaskLogger(task.name)
        task_logger.log_task_start(task_id, args, kwargs)

    @task_postrun.connect
    def task_postrun_handler(sender, task_id, task, args, kwargs, retval, state, **kwds) -> None:
        """Log after task execution with detailed metrics."""
        duration = time.time() - task_start_times.pop(task_id, time.time())
        context = task_contexts.pop(task_id, {})
        task_logger = CeleryTaskLogger(task.name)

        if state == "SUCCESS":
            task_logger.log_task_success(task_id, retval, duration, metrics)
        else:
            # For non-success states, we might not have exception info here
            worker_logger.warning(
                "task_completed_with_state",
                task_id=task_id,
                task_name=task.name,
                state=state,
                duration_ms=round(duration * 1000, 2),
                retry_count=context.get("retries", 0),
            )

    @task_failure.connect
    def task_failure_handler(sender, task_id, exception, args, kwargs, traceback, einfo, **kwds) -> None:
        """Log task failures with full context."""
        duration = time.time() - task_start_times.pop(task_id, time.time())
        task_contexts.get(task_id, {})
        task_logger = CeleryTaskLogger(sender.name)
        task_logger.log_task_failure(task_id, exception, duration, metrics)

    @task_retry.connect
    def task_retry_handler(sender, request, reason, einfo, **kwargs) -> None:
        """Log task retry attempts."""
        task_logger = CeleryTaskLogger(sender.name)
        task_logger.log_task_retry(
            request.id,
            reason,
            request.kwargs.get("countdown", 0),
            request.retries,
            metrics,
        )


if __name__ == "__main__":
    from provide.foundation import pout

    pout("📊 Task Metrics System")
    pout("=" * 30)

    # Demo the metrics system
    metrics.record_execution("test_task", 1.5, True)
    metrics.record_execution("test_task", 2.1, False)
    metrics.record_retry("test_task")

    stats = metrics.get_stats()
    pout(f"Demo stats: {stats}")

# 🧱🏗️🔚
