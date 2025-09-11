#!/usr/bin/env python3
"""
Celery Integration - Demo Runner and Workflow Examples

This module contains the demo runner and workflow examples that showcase
various Celery task patterns with provide.foundation logging integration.

Part 4 of 4: Demo Runner and Workflows
- In-process demo worker for testing without Redis
- Task workflow demonstrations (chains, groups, etc.)
- Result collection and metrics display
- Production vs demo mode examples

Usage:
    # Demo mode (no Redis required)
    python 04_demo_runner.py --demo
    
    # Production mode (requires Redis and separate worker)
    python 04_demo_runner.py
"""

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

from provide.foundation import logger, pout  # noqa: E402

# Import our setup and tasks
from examples.integration.celery.setup_and_config import app, DEMO_MODE  # noqa: E402
from examples.integration.celery.metrics_and_signals import metrics, setup_signal_handlers  # noqa: E402
from examples.integration.celery.tasks import (  # noqa: E402
    process_payment,
    generate_report,
    send_notification,
    process_batch_data,
    cleanup_old_data
)

# Try to import Celery workflow tools
try:
    from celery import chain, chord, group
    CELERY_WORKFLOWS_AVAILABLE = True
except ImportError:
    CELERY_WORKFLOWS_AVAILABLE = False

# Setup signal handlers
setup_signal_handlers(app, demo_mode=DEMO_MODE)


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

    if CELERY_WORKFLOWS_AVAILABLE:
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
    else:
        pout("\n5️⃣ Task Chains: Skipped (Celery workflows not available)")
        pout("\n6️⃣ Parallel Groups: Skipped (Celery workflows not available)")

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
    display_final_metrics(demo_logger)


def display_final_metrics(demo_logger):
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

    demo_logger.info("demo_completed", final_metrics=stats)


def main():
    """Main demo runner."""
    pout("""
╔══════════════════════════════════════════════════════════════════╗
║                   Celery Integration Example                     ║
║                Rich Task Processing Patterns                     ║
╚══════════════════════════════════════════════════════════════════╝

Demonstrates comprehensive integration of provide.foundation logging with Celery,
showing real-world task processing patterns including:
• Task lifecycle tracking with structured logging
• Worker pool monitoring and health metrics
• Task retry patterns with exponential backoff
• Error handling and dead letter queues
• Progress tracking for long-running tasks
• Task chains and workflows
• Priority queues and routing
""")

    if DEMO_MODE:
        # Run in demo mode with in-process worker
        pout("🎮 Running in DEMO MODE - No Redis Required!")
        pout("   Using filesystem broker for demonstration")
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
        pout("   2. Celery worker: celery -A examples.integration.celery.setup_and_config worker --loglevel=info")
        pout("")
        pout("💡 Tip: Run with --demo flag to use filesystem broker without Redis")
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


if __name__ == '__main__':
    main()