#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Task Workflow Runner

This module demonstrates comprehensive Celery task patterns with provide.foundation
logging integration using filesystem backend (no Redis required).

Part 4 of 4: Task Workflow Runner
- In-process worker with filesystem transport
- Task workflow demonstrations (chains, groups, etc.)
- Result collection and metrics display
- Comprehensive logging patterns

Usage:
    python 04_runner.py"""

from pathlib import Path
import random
import sys
import threading
import time

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Add current directory to path for local imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import our setup and tasks
import importlib.util

from provide.foundation import logger, pout


# Load modules by file path to handle hyphenated names
def load_module_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load local modules
current_dir = Path(__file__).parent
setup_config = load_module_from_file("setup_and_config", current_dir / "01_setup_and_config.py")
metrics_signals = load_module_from_file("metrics_and_signals", current_dir / "02_metrics_and_signals.py")
tasks_module = load_module_from_file("tasks", current_dir / "03_tasks.py")

# Extract needed objects
app = setup_config.app
metrics = metrics_signals.metrics
setup_signal_handlers = metrics_signals.setup_signal_handlers
process_payment = tasks_module.process_payment
generate_report = tasks_module.generate_report
send_notification = tasks_module.send_notification
process_batch_data = tasks_module.process_batch_data
cleanup_old_data = tasks_module.cleanup_old_data

# Try to import Celery workflow tools
try:
    from celery import chain, group

    CELERY_WORKFLOWS_AVAILABLE = True
except ImportError:
    CELERY_WORKFLOWS_AVAILABLE = False

# Setup signal handlers
setup_signal_handlers(app)


def run_worker() -> None:
    """Run a worker in the same process for demonstration."""
    pout("\n🚀 Starting in-process worker...")

    # Start worker in a thread
    from celery.worker import WorkController

    def start_worker() -> None:
        worker = WorkController(app=app, loglevel="INFO")
        worker.start()

    worker_thread = threading.Thread(target=start_worker, daemon=True)
    worker_thread.start()

    # Give worker time to start
    time.sleep(2)


def demonstrate_task_workflows() -> None:
    """Demonstrate various task workflow patterns."""
    example_logger = logger.get_logger("celery.example")

    pout("\n" + "=" * 60)
    pout("🎯 Demonstrating Rich Celery Task Patterns")
    pout("=" * 60)

    # 1. Simple task execution with retries
    pout("\n1️⃣ Payment Processing with Automatic Retries")
    payment_task = process_payment.delay("order_123", 99.99, "credit_card")
    example_logger.info("submitted_payment_task", task_id=payment_task.id)

    # 2. Long-running task with progress tracking
    pout("\n2️⃣ Report Generation with Progress Tracking")
    report_task = generate_report.delay(
        "analytics",
        {"start": "2024-01-01", "end": "2024-01-31"},
        "user_456",
    )
    example_logger.info("submitted_report_task", task_id=report_task.id)

    # Monitor progress
    for _ in range(3):
        time.sleep(1)
        if report_task.state == "PROGRESS":
            meta = report_task.info
            example_logger.info(
                "report_progress_update",
                task_id=report_task.id,
                current=meta.get("current", 0),
                total=meta.get("total", 0),
                status=meta.get("status", ""),
            )

    # 3. Multi-channel notification
    pout("\n3️⃣ Multi-Channel Notification Delivery")
    notification_task = send_notification.delay(
        "user_789",
        "order_confirmation",
        {"order_id": "order_123", "amount": 99.99},
    )
    example_logger.info("submitted_notification_task", task_id=notification_task.id)

    # 4. Batch processing with error handling
    pout("\n4️⃣ Batch Data Processing with Item-Level Error Handling")
    batch_items = [{"id": f"item_{i}", "value": random.randint(1, 100)} for i in range(50)]
    batch_task = process_batch_data.delay("batch_001", batch_items)
    example_logger.info(
        "submitted_batch_task",
        task_id=batch_task.id,
        item_count=len(batch_items),
    )

    if CELERY_WORKFLOWS_AVAILABLE:
        # 5. Task chains and workflows
        pout("\n5️⃣ Task Chain: Payment → Notification → Cleanup")
        workflow = chain(
            process_payment.s("order_789", 149.99, "paypal"),
            send_notification.s("payment_success", {"amount": 149.99}),
            cleanup_old_data.s(days_to_keep=7),
        )
        workflow_result = workflow.apply_async()
        example_logger.info("submitted_workflow", workflow_id=workflow_result.id)

        # 6. Parallel task group
        pout("\n6️⃣ Parallel Task Group: Multiple Payments")
        payment_group = group(
            process_payment.s(f"order_{i}", random.uniform(10, 200), "credit_card") for i in range(5)
        )
        group_result = payment_group.apply_async()
        example_logger.info(
            "submitted_parallel_group",
            group_id=group_result.id,
            task_count=5,
        )
    else:
        pout("\n5️⃣ Task Chains: Skipped (Celery workflows not available)")
        pout("\n6️⃣ Parallel Groups: Skipped (Celery workflows not available)")

    # Wait for some results
    pout("\n⏳ Waiting for task results...")
    time.sleep(3)

    # Collect results
    try:
        payment_result = payment_task.get(timeout=5)
        example_logger.info(
            "payment_task_completed",
            task_id=payment_task.id,
            result=payment_result,
        )
    except Exception as e:
        example_logger.error(
            "payment_task_error",
            task_id=payment_task.id,
            error=str(e),
        )

    try:
        report_result = report_task.get(timeout=5)
        example_logger.info(
            "report_task_completed",
            task_id=report_task.id,
            pages=report_result.get("pages", 0),
        )
    except Exception as e:
        example_logger.error(
            "report_task_error",
            task_id=report_task.id,
            error=str(e),
        )

    try:
        notification_result = notification_task.get(timeout=5)
        example_logger.info(
            "notification_task_completed",
            task_id=notification_task.id,
            success_count=notification_result.get("success_count", 0),
        )
    except Exception as e:
        example_logger.error(
            "notification_task_error",
            task_id=notification_task.id,
            error=str(e),
        )

    try:
        batch_result = batch_task.get(timeout=5)
        example_logger.info(
            "batch_task_completed",
            task_id=batch_task.id,
            processed=batch_result.get("processed", 0),
            failed=batch_result.get("failed", 0),
            success_rate=batch_result.get("success_rate", 0),
        )
    except Exception as e:
        example_logger.error(
            "batch_task_error",
            task_id=batch_task.id,
            error=str(e),
        )

    # Display final metrics
    display_final_metrics(example_logger)


def display_final_metrics(example_logger) -> None:
    """Display final execution metrics."""
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

    example_logger.info("example_completed", final_metrics=stats)


def main() -> None:
    """Main example runner."""
    pout("""
╔══════════════════════════════════════════════════════════════════╗
║                   Celery Integration Example                     ║
║              Comprehensive Task Processing Patterns              ║
╚══════════════════════════════════════════════════════════════════╝

Demonstrates provide.foundation's structured logging with Celery using filesystem
transport (no Redis required). Real-world patterns include:
• Task lifecycle tracking with structured logging
• Worker pool monitoring and health metrics
• Task retry patterns with exponential backoff
• Error handling and recovery patterns
• Progress tracking for long-running tasks
• Task chains and workflows
• Parallel task execution
""")

    pout("🚀 Running Celery Foundation Example")
    pout("   Using filesystem transport (self-contained)")
    pout("")

    # Start worker
    run_worker()

    # Run demonstrations
    demonstrate_task_workflows()

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


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
