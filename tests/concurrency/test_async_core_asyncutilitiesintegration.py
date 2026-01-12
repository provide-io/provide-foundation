#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation concurrency utilities."""

import asyncio
import time
from typing import Never

from provide.testkit import MinimalTestCase
import pytest

from provide.foundation.concurrency import (
    async_gather,
    async_run,
    async_sleep,
    async_wait_for,
)
from provide.foundation.errors import ValidationError


class TestAsyncUtilitiesIntegration(MinimalTestCase):
    """Integration tests for async utilities."""

    @pytest.mark.asyncio
    async def test_async_utilities_work_together(self) -> None:
        """Test async utilities work together in complex scenarios."""

        async def task_with_timeout(value, delay):
            await async_sleep(delay)
            return value * 2

        async def main_workflow():
            # Use async_gather to run multiple tasks
            tasks = await async_gather(
                async_wait_for(task_with_timeout(1, 0.01), timeout=0.1),
                async_wait_for(task_with_timeout(2, 0.01), timeout=0.1),
                async_wait_for(task_with_timeout(3, 0.01), timeout=0.1),
            )
            return sum(tasks)

        result = await main_workflow()
        assert result == 12  # (1*2) + (2*2) + (3*2)

    def test_async_run_with_complex_async_workflow(self) -> None:
        """Test async_run with complex async workflow."""

        async def complex_workflow():
            # Phase 1: Gather initial data
            await async_gather(
                async_sleep(0.01),
                async_sleep(0.01),
            )

            # Phase 2: Process data with timeout
            async def process_data():
                await async_sleep(0.02)
                return [1, 2, 3]

            processed = await async_wait_for(process_data(), timeout=0.1)

            # Phase 3: Final computation
            return sum(processed)

        result = async_run(complex_workflow)
        assert result == 6

    @pytest.mark.asyncio
    async def test_error_handling_across_utilities(self) -> None:
        """Test error handling across multiple async utilities."""

        async def failing_task() -> Never:
            await async_sleep(0.01)
            raise ValueError("Task failed")

        async def success_task() -> str:
            await async_sleep(0.01)
            return "success"

        # Test that async_gather propagates errors
        with pytest.raises(ValueError):
            await async_gather(success_task(), failing_task())

        # Test that async_wait_for propagates errors
        with pytest.raises(ValueError):
            await async_wait_for(failing_task(), timeout=1.0)

    @pytest.mark.asyncio
    async def test_cancellation_support(self) -> None:
        """Test cancellation support across utilities."""

        async def cancellable_workflow() -> str | None:
            try:
                # This should be cancellable
                await async_gather(
                    async_sleep(1.0),  # Long sleep
                    async_sleep(1.0),
                )
                return "not cancelled"
            except asyncio.CancelledError:
                return "cancelled"

        # Start the task and cancel it
        task = asyncio.create_task(cancellable_workflow())
        await asyncio.sleep(0.01)  # Let it start
        task.cancel()

        try:
            result = await task
        except asyncio.CancelledError:
            result = "task cancelled"

        assert result in ["cancelled", "task cancelled"]

    @pytest.mark.asyncio
    async def test_performance_comparison(self) -> None:
        """Test performance characteristics of async utilities."""

        async def fast_task(n):
            await async_sleep(0.001)
            return n

        # Sequential execution
        start = time.time()
        sequential_results = []
        for i in range(10):
            result = await fast_task(i)
            sequential_results.append(result)
        sequential_time = time.time() - start

        # Concurrent execution with async_gather
        start = time.time()
        concurrent_results = await async_gather(*[fast_task(i) for i in range(10)])
        concurrent_time = time.time() - start

        # Concurrent should be faster
        assert concurrent_time < sequential_time
        assert sequential_results == concurrent_results

    def test_async_utilities_error_messages(self) -> None:
        """Test that async utilities provide helpful error messages."""
        # Test async_run error message
        try:
            async_run("not callable")
        except ValidationError as e:
            assert "Main must be callable" in str(e)

        # Test async_sleep error (need to run in event loop)
        async def test_sleep_error():
            try:
                await async_sleep(-1)
            except ValidationError as e:
                return "Sleep delay must be non-negative" in str(e)
            return False

        result = async_run(test_sleep_error)
        assert result is True


# 🧱🏗️🔚
