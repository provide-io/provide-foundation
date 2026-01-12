#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Examples demonstrating the new architectural improvements in provide-foundation.

This file showcases the new features added in the comprehensive refactoring:
- Resource cleanup protocols
- Thread-safe circuit breaker
- Bulkhead pattern for resource isolation
- Event-driven architecture
- Memory management with weak references"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from provide.foundation.hub import (
    AsyncDisposable,
    Disposable,
    get_bulkhead_manager,
    get_hub,
)
from provide.foundation.hub.events import get_event_bus
from provide.foundation.resilience import SyncCircuitBreaker


class ExampleResource(Disposable):
    """Example resource that implements the Disposable protocol."""

    def __init__(self, name: str) -> None:
        """Initialize the resource."""
        self.name = name
        self.is_disposed = False

    def do_work(self) -> str:
        """Perform some work."""
        if self.is_disposed:
            raise RuntimeError(f"Resource {self.name} has been disposed")
        return f"Work completed by {self.name}"

    def dispose(self) -> None:
        """Clean up the resource."""
        if not self.is_disposed:
            self.is_disposed = True
            print(f"🗑️  Disposed resource: {self.name}")


class AsyncExampleResource(AsyncDisposable):
    """Example async resource that implements the AsyncDisposable protocol."""

    def __init__(self, name: str) -> None:
        """Initialize the async resource."""
        self.name = name
        self.is_disposed = False

    async def do_async_work(self) -> str:
        """Perform some async work."""
        if self.is_disposed:
            raise RuntimeError(f"Async resource {self.name} has been disposed")
        await asyncio.sleep(0.1)  # Simulate async work
        return f"Async work completed by {self.name}"

    async def dispose_async(self) -> None:
        """Clean up the async resource."""
        if not self.is_disposed:
            self.is_disposed = True
            print(f"🗑️  Disposed async resource: {self.name}")


def example_event_system() -> None:
    """Demonstrate the event-driven architecture."""
    print("\n🎯 Event System Example")
    print("=" * 50)

    # Get the global event bus
    event_bus = get_event_bus()

    # Create event handlers
    def handle_test_event(event: Any) -> None:
        print(f"📢 Received event: {event.name} with data: {event.data}")

    # Subscribe to events
    event_bus.subscribe("test.event", handle_test_event)

    # Emit some events
    from provide.foundation.hub.events import Event

    event_bus.emit(Event(name="test.event", data={"message": "Hello from event system!"}, source="example"))

    # Get memory statistics
    stats = event_bus.get_memory_stats()
    print(f"📊 Event bus stats: {stats}")

    # Force cleanup of dead references
    event_bus.force_cleanup()
    print("🧹 Cleaned up event bus")


def example_resource_cleanup() -> None:
    """Demonstrate resource cleanup protocols."""
    print("\n🧹 Resource Cleanup Example")
    print("=" * 50)

    # Get the hub and create resources
    hub = get_hub()

    # Register a disposable resource
    resource1 = ExampleResource("Resource-1")
    hub.register(name="example.resource1", value=resource1, dimension="singleton")

    resource2 = ExampleResource("Resource-2")
    hub.register(name="example.resource2", value=resource2, dimension="singleton")

    # Use the resources
    print(f"🔨 {resource1.do_work()}")
    print(f"🔨 {resource2.do_work()}")

    # Clear the singleton dimension - this will automatically dispose resources
    print("\n🧹 Clearing hub dimension (will auto-dispose resources)...")
    hub.clear(dimension="singleton")


def example_circuit_breaker() -> None:
    """Demonstrate thread-safe circuit breaker."""
    print("\n⚡ Circuit Breaker Example")
    print("=" * 50)

    # Create a circuit breaker
    circuit_breaker = SyncCircuitBreaker(failure_threshold=3, recovery_timeout=5.0)

    # Function that sometimes fails
    call_count = 0

    def unreliable_service() -> str:
        nonlocal call_count
        call_count += 1
        if call_count <= 4:  # Fail first 4 calls
            raise RuntimeError(f"Service failure #{call_count}")
        return f"Success on call #{call_count}"

    # Try to call the unreliable service
    for i in range(7):
        try:
            circuit_breaker.call(unreliable_service)
        except Exception as e:
            print(f"❌ Call {i + 1}: {e}")

        print(f"   Circuit state: {circuit_breaker.state.value}, failures: {circuit_breaker.failure_count}")

    # Reset the circuit breaker
    circuit_breaker.reset()
    print("\n🔄 Circuit breaker manually reset")
    print(f"   Circuit state: {circuit_breaker.state.value}, failures: {circuit_breaker.failure_count}")


def example_bulkhead_pattern() -> None:
    """Demonstrate bulkhead pattern for resource isolation."""
    print("\n🚢 Bulkhead Pattern Example")
    print("=" * 50)

    # Get the bulkhead manager
    manager = get_bulkhead_manager()

    # Create bulkheads for different services
    db_bulkhead = manager.create_bulkhead("database", max_concurrent=3, timeout=2.0)
    api_bulkhead = manager.create_bulkhead("external_api", max_concurrent=2, timeout=1.0)

    # Simulate database operations
    def database_operation(query_id: int) -> str:
        time.sleep(0.5)  # Simulate DB operation
        return f"Database query {query_id} completed"

    # Simulate API calls
    def api_call(request_id: int) -> str:
        time.sleep(0.3)  # Simulate API call
        return f"API request {request_id} completed"

    # Execute operations through bulkheads
    try:
        # Database operations
        for i in range(5):
            try:
                result = db_bulkhead.execute(database_operation, i + 1)
                print(f"📊 {result}")
            except RuntimeError as e:
                print(f"❌ DB operation failed: {e}")

        # API operations
        for i in range(3):
            try:
                result = api_bulkhead.execute(api_call, i + 1)
                print(f"🌐 {result}")
            except RuntimeError as e:
                print(f"❌ API operation failed: {e}")

    finally:
        # Get status of all bulkheads
        status = manager.get_all_status()
        print(f"\n📈 Bulkhead status: {status}")


async def example_async_bulkhead() -> None:
    """Demonstrate async bulkhead pattern."""
    print("\n🚢 Async Bulkhead Example")
    print("=" * 50)

    manager = get_bulkhead_manager()
    async_bulkhead = manager.create_bulkhead("async_service", max_concurrent=2, timeout=1.0)

    async def async_service_call(request_id: int) -> str:
        await asyncio.sleep(0.2)  # Simulate async work
        return f"Async service request {request_id} completed"

    # Execute async operations through bulkhead
    tasks = []
    for i in range(4):

        async def wrapped_call(req_id: int = i + 1) -> None:
            try:
                result = await async_bulkhead.execute_async(async_service_call, req_id)
                print(f"⚡ {result}")
            except RuntimeError as e:
                print(f"❌ Async operation failed: {e}")

        tasks.append(wrapped_call())

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
    print(f"📊 Final bulkhead status: {async_bulkhead.get_status()}")


async def example_async_resource_cleanup() -> None:
    """Demonstrate async resource cleanup."""
    print("\n🧹 Async Resource Cleanup Example")
    print("=" * 50)

    # Create async resources
    resource1 = AsyncExampleResource("AsyncResource-1")
    resource2 = AsyncExampleResource("AsyncResource-2")

    # Use the async resources
    print(f"🔨 {await resource1.do_async_work()}")
    print(f"🔨 {await resource2.do_async_work()}")

    # Clean up async resources
    print("\n🧹 Cleaning up async resources...")
    await resource1.dispose_async()
    await resource2.dispose_async()


def main() -> None:
    """Run all examples."""
    print("=" * 60)

    # Run synchronous examples
    example_event_system()
    example_resource_cleanup()
    example_circuit_breaker()
    example_bulkhead_pattern()

    # Run async examples
    print("\n🔄 Running async examples...")
    asyncio.run(example_async_examples())


async def example_async_examples() -> None:
    """Run all async examples."""
    await example_async_bulkhead()
    await example_async_resource_cleanup()


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
