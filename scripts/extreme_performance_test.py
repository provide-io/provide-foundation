#!/usr/bin/env python3
# extreme_performance_test.py
#
"""
Extreme Performance Testing for Pyvider Telemetry.

This script pushes the logging system to its absolute limits to test:
- Maximum sustainable throughput
- Memory usage under extreme load
- Thread contention at high concurrency
- Performance degradation patterns
- System resource utilization
- Error handling under stress

Results help establish performance ceilings and identify breaking points.
"""
import asyncio
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import gc
from pathlib import Path
import sys
import threading
import time
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import io

from pyvider.telemetry import (
    LoggingConfig,
    TelemetryConfig,
    logger,
    setup_telemetry,
)
from pyvider.telemetry.core import (
    _set_log_stream_for_testing,
    reset_pyvider_setup_for_testing,
)


@contextmanager
def capture_logs() -> Generator[io.StringIO]:
    """Context manager for log capture during extreme testing."""
    captured = io.StringIO()
    _set_log_stream_for_testing(captured)
    try:
        yield captured
    finally:
        _set_log_stream_for_testing(None)


def get_memory_usage() -> float:
    """Get memory usage in MB, with fallback."""
    try:
        import psutil
        return psutil.Process().memory_info().rss / 1024 / 1024
    except ImportError:
        return 0.0


class PerformanceMonitor:
    """Real-time performance monitoring during tests."""

    def __init__(self) -> None:
        self.start_time = 0.0
        self.message_count = 0
        self.start_memory = 0.0
        self.max_memory = 0.0
        self.monitoring = False
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start monitoring."""
        self.start_time = time.perf_counter()
        self.start_memory = get_memory_usage()
        self.max_memory = self.start_memory
        self.message_count = 0
        self.monitoring = True

    def record_message(self) -> None:
        """Record a message and update stats."""
        if not self.monitoring:
            return
        with self._lock:
            self.message_count += 1
            current_memory = get_memory_usage()
            if current_memory > self.max_memory:
                self.max_memory = current_memory

    def get_stats(self) -> dict[str, Any]:
        """Get current performance statistics."""
        if not self.monitoring:
            return {}

        duration = time.perf_counter() - self.start_time
        current_memory = get_memory_usage()

        return {
            "duration_seconds": duration,
            "message_count": self.message_count,
            "messages_per_second": self.message_count / duration if duration > 0 else 0,
            "start_memory_mb": self.start_memory,
            "current_memory_mb": current_memory,
            "max_memory_mb": self.max_memory,
            "memory_delta_mb": current_memory - self.start_memory,
            "memory_peak_delta_mb": self.max_memory - self.start_memory,
        }


def extreme_throughput_test() -> dict[str, Any]:
    """Test absolute maximum throughput."""
    print("🔥 Running EXTREME Throughput Test...")

    reset_pyvider_setup_for_testing()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=False,  # Maximize speed
            das_emoji_prefix_enabled=False,
        )
    )

    monitor = PerformanceMonitor()

    with capture_logs():
        setup_telemetry(config)
        test_logger = logger.get_logger("extreme.throughput")

        monitor.start()

        # EXTREME: 100,000 messages as fast as possible
        message_count = 100000
        for i in range(message_count):
            test_logger.info(f"Extreme message {i}")
            if i % 10000 == 0:  # Periodic monitoring
                monitor.record_message()

        # Force final count
        monitor.message_count = message_count
        stats = monitor.get_stats()

    print(f"  🚀 Throughput: {stats['messages_per_second']:.0f} msg/sec")
    print(f"  ⏱️  Duration: {stats['duration_seconds']:.3f} seconds")
    print(f"  🧠 Memory Delta: {stats['memory_delta_mb']:.2f} MB")

    return stats


def extreme_concurrency_test() -> dict[str, Any]:
    """Test with extreme thread concurrency."""
    print("🧵 Running EXTREME Concurrency Test...")

    reset_pyvider_setup_for_testing()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )

    def worker_thread(thread_id: int, messages: int, monitor: PerformanceMonitor) -> None:
        """High-intensity worker thread."""
        thread_logger = logger.get_logger(f"extreme.thread.{thread_id}")
        for i in range(messages):
            thread_logger.info(f"Thread {thread_id} msg {i}", thread_id=thread_id)
            if i % 100 == 0:
                monitor.record_message()

    monitor = PerformanceMonitor()

    with capture_logs():
        setup_telemetry(config)
        monitor.start()

        # EXTREME: 50 threads, 2000 messages each = 100,000 total
        thread_count = 50
        messages_per_thread = 2000

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(worker_thread, tid, messages_per_thread, monitor)
                for tid in range(thread_count)
            ]

            for future in as_completed(futures):
                future.result()

        monitor.message_count = thread_count * messages_per_thread
        stats = monitor.get_stats()

    print(f"  🚀 Concurrent Throughput: {stats['messages_per_second']:.0f} msg/sec")
    print(f"  🧵 Threads: {thread_count}")
    print(f"  📨 Total Messages: {monitor.message_count}")
    print(f"  🧠 Memory Peak: {stats['memory_peak_delta_mb']:.2f} MB")

    return stats


def memory_stress_test() -> dict[str, Any]:
    """Test memory usage under sustained load."""
    print("🧠 Running Memory Stress Test...")

    reset_pyvider_setup_for_testing()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="DEBUG",  # More processing overhead
            console_formatter="json",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        )
    )

    monitor = PerformanceMonitor()
    memory_samples = []

    with capture_logs():
        setup_telemetry(config)
        test_logger = logger.get_logger("memory.stress")

        monitor.start()

        # Large payload logging over time
        large_data = {
            "large_string": "x" * 5000,  # 5KB string
            "large_list": list(range(1000)),
            "nested_data": {"level_%d" % i: f"data_{i}" * 100 for i in range(100)},
        }

        for i in range(10000):
            test_logger.info(
                f"Memory stress message {i}",
                iteration=i,
                domain="memory",
                action="stress",
                status="ongoing",
                **large_data
            )

            if i % 1000 == 0:
                gc.collect()  # Force garbage collection
                memory_samples.append(get_memory_usage())
                monitor.record_message()

        monitor.message_count = 10000
        stats = monitor.get_stats()
        stats["memory_samples"] = memory_samples
        stats["memory_growth_trend"] = (
            memory_samples[-1] - memory_samples[0] if len(memory_samples) > 1 else 0
        )

    print(f"  🚀 Throughput: {stats['messages_per_second']:.0f} msg/sec")
    print(f"  🧠 Memory Growth: {stats['memory_growth_trend']:.2f} MB")
    print(f"  📊 Peak Memory: {stats['max_memory_mb']:.2f} MB")

    return stats


async def async_extreme_test() -> dict[str, Any]:
    """Test extreme async performance."""
    print("⚡ Running EXTREME Async Test...")

    reset_pyvider_setup_for_testing()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )

    async def async_worker(worker_id: int, message_count: int) -> None:
        """High-speed async worker."""
        async_logger = logger.get_logger(f"extreme.async.{worker_id}")
        for i in range(message_count):
            async_logger.info(f"Async {worker_id} msg {i}", worker_id=worker_id)
            if i % 500 == 0:
                await asyncio.sleep(0)  # Yield occasionally

    with capture_logs():
        setup_telemetry(config)

        start_time = time.perf_counter()
        start_memory = get_memory_usage()

        # EXTREME: 20 async workers, 5000 messages each = 100,000 total
        worker_count = 20
        messages_per_worker = 5000

        tasks = [
            async_worker(worker_id, messages_per_worker)
            for worker_id in range(worker_count)
        ]

        await asyncio.gather(*tasks)

        end_time = time.perf_counter()
        end_memory = get_memory_usage()

        total_messages = worker_count * messages_per_worker
        duration = end_time - start_time

        stats = {
            "duration_seconds": duration,
            "total_messages": total_messages,
            "messages_per_second": total_messages / duration,
            "worker_count": worker_count,
            "memory_delta_mb": end_memory - start_memory,
        }

    print(f"  🚀 Async Throughput: {stats['messages_per_second']:.0f} msg/sec")
    print(f"  ⚡ Workers: {worker_count}")
    print(f"  📨 Total Messages: {total_messages}")

    return stats


def filtering_efficiency_test() -> dict[str, Any]:
    """Test filtering efficiency under extreme load."""
    print("🔍 Running Filtering Efficiency Test...")

    reset_pyvider_setup_for_testing()
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="CRITICAL",  # Filter almost everything
            module_levels={"extreme.allowed": "DEBUG"},  # Only one module allowed
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        allowed_logger = logger.get_logger("extreme.allowed")
        blocked_logger = logger.get_logger("extreme.blocked")

        start_time = time.perf_counter()

        # Generate massive number of messages, most filtered
        total_attempts = 100000
        for i in range(total_attempts // 2):
            # These should be logged
            allowed_logger.debug(f"Allowed message {i}")
            # These should be filtered
            blocked_logger.debug(f"Blocked message {i}")

        end_time = time.perf_counter()

        # Count actual output
        output_lines = len([
            line for line in captured.getvalue().split('\n')
            if line.strip() and not line.startswith("[Pyvider Setup]")
        ])

        duration = end_time - start_time
        stats = {
            "duration_seconds": duration,
            "total_attempts": total_attempts,
            "actual_output_lines": output_lines,
            "filtering_efficiency_percent": ((total_attempts - output_lines) / total_attempts) * 100,
            "messages_per_second": total_attempts / duration,
        }

    print(f"  🚀 Processing Rate: {stats['messages_per_second']:.0f} msg/sec")
    print(f"  🔍 Filtered: {stats['filtering_efficiency_percent']:.1f}%")
    print(f"  📊 Output Lines: {output_lines} / {total_attempts}")

    return stats


def main() -> None:
    """Run all extreme performance tests."""
    print("🚀 EXTREME PERFORMANCE TESTING")
    print("=" * 50)
    print("⚠️  WARNING: These tests push the system to its limits!")
    print("=" * 50)

    results = {}

    # Run all extreme tests
    try:
        results["extreme_throughput"] = extreme_throughput_test()
        print()

        results["extreme_concurrency"] = extreme_concurrency_test()
        print()

        results["memory_stress"] = memory_stress_test()
        print()

        results["async_extreme"] = asyncio.run(async_extreme_test())
        print()

        results["filtering_efficiency"] = filtering_efficiency_test()
        print()

    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        return
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        return

    # Summary
    print("=" * 50)
    print("🏁 EXTREME PERFORMANCE RESULTS")
    print("=" * 50)

    for test_name, stats in results.items():
        if "messages_per_second" in stats:
            throughput = stats["messages_per_second"]
            print(f"{test_name:20s}: {throughput:>10.0f} msg/sec")

    # Find peak performance
    peak_test = max(
        results.items(),
        key=lambda x: x[1].get("messages_per_second", 0)
    )
    peak_throughput = peak_test[1]["messages_per_second"]

    print(f"\n🚀 PEAK PERFORMANCE: {peak_throughput:.0f} msg/sec ({peak_test[0]})")

    # Performance targets
    print("\n🎯 EXTREME TARGETS:")
    print(f"  • >200K msg/sec: {'✅' if peak_throughput > 200000 else '❌'}")
    print(f"  • >500K msg/sec: {'✅' if peak_throughput > 500000 else '❌'}")
    print(f"  • >1M msg/sec:   {'✅' if peak_throughput > 1000000 else '❌'}")


if __name__ == "__main__":
    main()

# 🚀💥
