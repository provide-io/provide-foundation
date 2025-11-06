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

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
import importlib.util
import os
from pathlib import Path
import platform
import sys
import threading
import time
from types import ModuleType
from typing import Any

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import logger  # noqa: E402

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


def _load_module_from_file(name: str, filepath: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, filepath)
    if spec is None or spec.loader is None:
        msg = f"Unable to load module: {name}"
        raise ImportError(msg)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_celery_task_logger() -> type[Any]:
    current_dir = Path(__file__).parent
    setup_config = _load_module_from_file("setup_and_config", current_dir / "01_setup_and_config.py")
    return setup_config.CeleryTaskLogger


def _create_worker_ready_handler() -> Callable[[Any], None]:
    def worker_ready_handler(sender: Any, **kwargs: Any) -> None:
        """Log when worker is ready with system info."""
        worker_logger.info(
            "worker_ready",
            worker_pid=getattr(sender, "pid", None),
            hostname=getattr(sender, "hostname", None),
            python_version=platform.python_version(),
            cpu_count=os.cpu_count(),
            transport="filesystem",
            backend="file",
        )

    return worker_ready_handler


def _create_worker_process_init_handler() -> Callable[[Any], None]:
    def worker_process_init_handler(sender: Any, **kwargs: Any) -> None:
        """Log worker process initialization."""
        worker_logger.info(
            "worker_process_init",
            worker_pid=os.getpid(),
            parent_pid=os.getppid(),
        )

    return worker_process_init_handler


def _create_worker_shutdown_handler() -> Callable[[Any], None]:
    def worker_shutdown_handler(sender: Any, **kwargs: Any) -> None:
        """Log when worker shuts down with final metrics."""
        stats = metrics.get_stats()
        worker_logger.info(
            "worker_shutdown",
            worker_pid=getattr(sender, "pid", None),
            hostname=getattr(sender, "hostname", None),
            final_metrics=stats,
        )

    return worker_shutdown_handler


def _create_periodic_monitor_handler() -> Callable[[Any, Any], None]:
    def setup_periodic_monitoring(sender: Any, instance: Any, **kwargs: Any) -> None:
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

        monitor_thread = threading.Thread(target=monitor_health, daemon=True)
        monitor_thread.start()

    return setup_periodic_monitoring


def _create_task_prerun_handler(task_logger_cls: type[Any]) -> Callable[..., None]:
    def task_prerun_handler(
        sender: Any,
        task_id: str,
        task: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        **kwds: Any,
    ) -> None:
        """Log before task execution with enhanced context."""
        task_start_times[task_id] = time.time()
        task_contexts[task_id] = {
            "start_time": time.time(),
            "retries": kwargs.get("__retry_count", 0),
        }
        task_logger = task_logger_cls(task.name)
        task_logger.log_task_start(task_id, args, kwargs)

    return task_prerun_handler


def _create_task_postrun_handler(task_logger_cls: type[Any]) -> Callable[..., None]:
    def task_postrun_handler(
        sender: Any,
        task_id: str,
        task: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        retval: Any,
        state: str,
        **kwds: Any,
    ) -> None:
        """Log after task execution with detailed metrics."""
        duration = time.time() - task_start_times.pop(task_id, time.time())
        context = task_contexts.pop(task_id, {})
        task_logger = task_logger_cls(task.name)

        if state == "SUCCESS":
            task_logger.log_task_success(task_id, retval, duration, metrics)
        else:
            worker_logger.warning(
                "task_completed_with_state",
                task_id=task_id,
                task_name=task.name,
                state=state,
                duration_ms=round(duration * 1000, 2),
                retry_count=context.get("retries", 0),
            )

    return task_postrun_handler


def _create_task_failure_handler(task_logger_cls: type[Any]) -> Callable[..., None]:
    def task_failure_handler(
        sender: Any,
        task_id: str,
        exception: Exception,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        traceback: Any,
        einfo: Any,
        **kwds: Any,
    ) -> None:
        """Log task failures with full context."""
        duration = time.time() - task_start_times.pop(task_id, time.time())
        task_contexts.get(task_id, {})
        task_logger = task_logger_cls(getattr(sender, "name", "unknown"))
        task_logger.log_task_failure(task_id, exception, duration, metrics)

    return task_failure_handler


def _create_task_retry_handler(task_logger_cls: type[Any]) -> Callable[..., None]:
    def task_retry_handler(sender: Any, request: Any, reason: Any, einfo: Any, **kwargs: Any) -> None:
        """Log task retry attempts."""
        task_logger = task_logger_cls(getattr(sender, "name", "unknown"))
        task_logger.log_task_retry(
            request.id,
            reason,
            request.kwargs.get("countdown", 0),
            request.retries,
            metrics,
        )

    return task_retry_handler


def setup_signal_handlers(_app: Any) -> None:
    """Set up all Celery signal handlers."""
    CeleryTaskLogger = _load_celery_task_logger()

    worker_ready.connect(_create_worker_ready_handler())
    worker_process_init.connect(_create_worker_process_init_handler())
    worker_shutdown.connect(_create_worker_shutdown_handler())
    celeryd_after_setup.connect(_create_periodic_monitor_handler())
    task_prerun.connect(_create_task_prerun_handler(CeleryTaskLogger))
    task_postrun.connect(_create_task_postrun_handler(CeleryTaskLogger))
    task_failure.connect(_create_task_failure_handler(CeleryTaskLogger))
    task_retry.connect(_create_task_retry_handler(CeleryTaskLogger))


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
