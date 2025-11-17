#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demonstrates using Foundation Telemetry in asynchronous applications."""

import asyncio
from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent  # Go up from examples to project root
# Line removed - project_root already set above
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import (
    logger,
    shutdown_foundation,
)
from provide.foundation.console.output import pout


async def example_9_async_usage() -> None:
    """Example 9: Demonstrates usage in asynchronous (`asyncio`) contexts.

    Covers logging from async functions and using the `shutdown_foundation`
    async function.
    """
    pout("\n" + "=" * 60)
    pout("⚡ Example 9: Async Usage")
    pout(" Demonstrates: Logging from asyncio tasks and async shutdown.")
    pout("=" * 60)

    async def async_task(task_id: int, task_type: str) -> dict[str, int]:
        """Simulate an async task with realistic operations."""
        task_logger = logger.get_logger(f"async_worker.{task_type}")
        task_logger.info("Async task started", task_id=task_id, task_type=task_type)

        # Simulate different types of async work
        if task_type == "data_processing":
            await asyncio.sleep(0.02)  # Simulate data processing
            task_logger.info("Processing data batch", task_id=task_id, records_processed=150)
            await asyncio.sleep(0.01)
            task_logger.info("Data validation completed", task_id=task_id, errors_found=0)
        elif task_type == "api_call":
            await asyncio.sleep(0.015)  # Simulate API call
            task_logger.info("API request sent", task_id=task_id, endpoint="/api/v1/users")
            await asyncio.sleep(0.01)
            task_logger.info("API response received", task_id=task_id, status_code=200, response_time_ms=25)

        result = {"duration_ms": 30 + task_id * 5}
        task_logger.info("Async task completed", task_id=task_id, **result)
        return result

    # Demonstrate concurrent async operations with different types
    logger.info("Starting batch of concurrent async tasks")
    results = await asyncio.gather(
        async_task(1, "data_processing"),
        async_task(2, "api_call"),
        async_task(3, "data_processing"),
        async_task(4, "api_call"),
    )

    # Process results
    total_duration = sum(r["duration_ms"] for r in results)
    logger.info(
        "All async tasks completed",
        tasks_completed=len(results),
        total_duration_ms=total_duration,
        avg_duration_ms=total_duration // len(results),
    )

    # Demonstrate async shutdown (currently logs a message)
    logger.info("Initiating telemetry shutdown...")
    await shutdown_foundation(timeout_millis=100)
    logger.info(
        "Message after shutdown call (may use fallback if shutdown was destructive)",
    )


if __name__ == "__main__":
    asyncio.run(example_9_async_usage())

# 🧱🏗️🔚
