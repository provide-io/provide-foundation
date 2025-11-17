#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Celery Integration - Task Definitions

This module contains example Celery tasks that demonstrate real-world patterns
with provide.foundation structured logging integration.

Part 3 of 4: Task Definitions
- Payment processing with retry logic
- Report generation with progress tracking
- Multi-channel notifications
- Batch data processing with error handling
- Data cleanup operations

Usage:
    from examples.integration.celery.tasks import process_payment, generate_report

    # Execute tasks
    result = process_payment.delay("order_123", 99.99, "credit_card")"""

from datetime import datetime, timedelta
from pathlib import Path
import random
import sys
import time
from typing import Any

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from examples.integration.celery.setup_and_config import CeleryTaskLogger, app


@app.task(bind=True, max_retries=3)
def process_payment(self, order_id: str, amount: float, payment_method: str) -> dict[str, Any]:
    """Process payment with retry logic and detailed logging."""
    task_logger = CeleryTaskLogger("process_payment")

    task_logger.logger.info(
        "processing_payment",
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        retry_count=self.request.retries,
    )

    try:
        # Simulate payment processing
        if random.random() < 0.3:  # 30% chance of transient failure
            raise ConnectionError("Payment gateway timeout")

        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))

        transaction_id = f"txn_{order_id}_{int(time.time())}"

        task_logger.logger.info(
            "payment_successful",
            order_id=order_id,
            transaction_id=transaction_id,
            amount=amount,
        )

        return {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except ConnectionError as exc:
        task_logger.logger.warning(
            "payment_gateway_error",
            order_id=order_id,
            error=str(exc),
            will_retry=self.request.retries < self.max_retries,
        )
        # Exponential backoff: 5, 10, 20 seconds
        countdown = 5 * (2**self.request.retries)
        raise self.retry(exc=exc, countdown=countdown) from exc


@app.task(bind=True)
def generate_report(self, report_type: str, date_range: dict[str, str], user_id: str) -> dict[str, Any]:
    """Generate report with progress tracking."""
    task_logger = CeleryTaskLogger("generate_report")

    task_logger.logger.info(
        "report_generation_started",
        report_type=report_type,
        date_range=date_range,
        user_id=user_id,
    )

    # Simulate report generation with progress updates
    total_steps = 5
    steps = [
        "Fetching data",
        "Processing records",
        "Calculating metrics",
        "Generating visualizations",
        "Creating PDF",
    ]

    for i, step in enumerate(steps, 1):
        task_logger.log_task_progress(self.request.id, i, total_steps, step)

        # Update task state for real-time monitoring
        self.update_state(
            state="PROGRESS",
            meta={"current": i, "total": total_steps, "status": step},
        )

        # Simulate work
        time.sleep(random.uniform(0.5, 1.5))

    report_url = f"https://reports.example.com/{report_type}_{self.request.id}.pdf"

    task_logger.logger.info(
        "report_generation_complete",
        report_type=report_type,
        report_url=report_url,
        user_id=user_id,
    )

    return {
        "status": "complete",
        "report_url": report_url,
        "generated_at": datetime.utcnow().isoformat(),
        "pages": random.randint(5, 20),
    }


@app.task
def send_notification(user_id: str, notification_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Send user notification with delivery tracking."""
    task_logger = CeleryTaskLogger("send_notification")

    task_logger.logger.info(
        "sending_notification",
        user_id=user_id,
        notification_type=notification_type,
        channels=["email", "push", "sms"],
    )

    results = {}

    # Simulate multi-channel delivery
    for channel in ["email", "push", "sms"]:
        success = random.random() > 0.1  # 90% success rate

        if success:
            task_logger.logger.info(
                f"{channel}_notification_sent",
                user_id=user_id,
                channel=channel,
                notification_type=notification_type,
            )
            results[channel] = {"status": "delivered", "timestamp": datetime.utcnow().isoformat()}
        else:
            task_logger.logger.warning(
                f"{channel}_notification_failed",
                user_id=user_id,
                channel=channel,
                notification_type=notification_type,
            )
            results[channel] = {"status": "failed", "error": "Delivery failed"}

    return {
        "user_id": user_id,
        "notification_type": notification_type,
        "delivery_results": results,
        "success_count": sum(1 for r in results.values() if r["status"] == "delivered"),
    }


@app.task
def process_batch_data(batch_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    """Process batch data with item-level error handling."""
    task_logger = CeleryTaskLogger("process_batch_data")

    task_logger.logger.info(
        "batch_processing_started",
        batch_id=batch_id,
        item_count=len(items),
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
                "batch_id": batch_id,
            }
            processed.append(processed_item)

        except Exception as e:
            task_logger.logger.warning(
                "batch_item_failed",
                batch_id=batch_id,
                item_index=i,
                error=str(e),
            )
            failed.append({"index": i, "error": str(e)})

    task_logger.logger.info(
        "batch_processing_complete",
        batch_id=batch_id,
        total_items=len(items),
        processed_count=len(processed),
        failed_count=len(failed),
        success_rate=round(len(processed) / len(items) * 100, 1),
    )

    return {
        "batch_id": batch_id,
        "processed": len(processed),
        "failed": len(failed),
        "failed_items": failed,
        "success_rate": round(len(processed) / len(items) * 100, 1),
    }


@app.task
def cleanup_old_data(days_to_keep: int = 30) -> dict[str, Any]:
    """Cleanup old data with detailed logging."""
    task_logger = CeleryTaskLogger("cleanup_old_data")

    task_logger.logger.info(
        "cleanup_started",
        days_to_keep=days_to_keep,
        cutoff_date=(datetime.utcnow() - timedelta(days=days_to_keep)).isoformat(),
    )

    # Simulate cleanup of different data types
    cleanup_results = {}
    data_types = ["logs", "temp_files", "cache_entries", "expired_sessions"]

    for data_type in data_types:
        # Simulate cleanup with random counts
        cleaned = random.randint(100, 10000)
        size_mb = random.uniform(10, 500)

        task_logger.logger.info(
            f"cleaned_{data_type}",
            data_type=data_type,
            items_removed=cleaned,
            space_freed_mb=round(size_mb, 2),
        )

        cleanup_results[data_type] = {
            "items_removed": cleaned,
            "space_freed_mb": round(size_mb, 2),
        }

    total_items = sum(r["items_removed"] for r in cleanup_results.values())
    total_space = sum(r["space_freed_mb"] for r in cleanup_results.values())

    task_logger.logger.info(
        "cleanup_complete",
        total_items_removed=total_items,
        total_space_freed_mb=round(total_space, 2),
        data_types_cleaned=len(data_types),
    )

    return {
        "status": "complete",
        "results": cleanup_results,
        "total_items_removed": total_items,
        "total_space_freed_mb": round(total_space, 2),
    }


if __name__ == "__main__":
    from provide.foundation import pout

    pout("🎯 Celery Tasks Available:")
    pout("• process_payment - Payment processing with retries")
    pout("• generate_report - Report generation with progress")
    pout("• send_notification - Multi-channel notifications")
    pout("• process_batch_data - Batch processing with error handling")
    pout("• cleanup_old_data - Data cleanup operations")

# 🧱🏗️🔚
