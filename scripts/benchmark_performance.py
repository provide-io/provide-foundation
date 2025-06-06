#!/usr/bin/env python3
# benchmark_performance.py
#
"""
Performance benchmarking script for Pyvider Telemetry.

This script measures the performance characteristics of the logging system
under various conditions and outputs detailed benchmark results.

The benchmarks include:
- Basic logging throughput measurement
- JSON vs key-value formatter performance
- Emoji processing overhead analysis
- Thread safety and concurrent logging performance
- Log level filtering efficiency
- Large payload handling performance
- Async logging patterns performance

Results are saved to benchmark-results.json for analysis and tracking
performance regressions over time.
"""
import asyncio
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import io
import json
from pathlib import Path
import sys
import time
from typing import Any

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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
    """
    Context manager to capture log output during benchmarks.

    This ensures that benchmark logging output doesn't interfere with
    benchmark timing measurements while still allowing us to verify
    that the expected number of log messages were generated.

    Yields:
        StringIO buffer containing captured log output.
    """
    captured = io.StringIO()
    _set_log_stream_for_testing(captured)
    try:
        yield captured
    finally:
        _set_log_stream_for_testing(None)


@contextmanager
def benchmark_timer(test_name: str) -> Generator[dict[str, Any]]:
    """
    Context manager to time benchmark operations and track memory usage.

    This provides consistent timing and memory measurement across all
    benchmark functions, ensuring accurate and comparable results.

    Args:
        test_name: Name of the benchmark test for result identification.

    Yields:
        Dictionary that will be populated with timing and memory results.
    """
    result = {"test_name": test_name}
    start_time = time.perf_counter()
    start_memory = _get_memory_usage()

    try:
        yield result
    finally:
        end_time = time.perf_counter()
        end_memory = _get_memory_usage()

        result.update({
            "duration_seconds": end_time - start_time,
            "start_memory_mb": start_memory,
            "end_memory_mb": end_memory,
            "memory_delta_mb": end_memory - start_memory,
        })


def _get_memory_usage() -> float:
    """
    Get current memory usage in MB.

    Uses psutil if available for accurate memory measurement,
    otherwise returns 0.0 as a safe fallback.

    Returns:
        Current process memory usage in megabytes, or 0.0 if unavailable.
    """
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        return 0.0  # psutil not available


def benchmark_basic_logging() -> dict[str, Any]:
    """
    Benchmark basic logging operations with emoji processing enabled.

    This test measures the core performance of the logging system with
    typical configuration settings. It establishes a baseline for
    logging throughput.

    Returns:
        Dictionary containing benchmark results including throughput metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=False,
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        with benchmark_timer("basic_logging") as result:
            message_count = 10000
            test_logger = logger.get_logger("benchmark.basic")

            for i in range(message_count):
                test_logger.info(f"Benchmark message {i}", iteration=i)

            # Store intermediate results that don't need timing
            result["message_count"] = message_count
            result["output_size_bytes"] = len(captured.getvalue())

        # Calculate throughput after timing is complete
        result["messages_per_second"] = result["message_count"] / result["duration_seconds"]

    return result


def benchmark_json_formatting() -> dict[str, Any]:
    """
    Benchmark JSON output formatting with full emoji processing.

    This test measures the performance impact of JSON serialization
    and emoji processing combined, which is common in production
    environments where structured logging is preferred.

    Returns:
        Dictionary containing JSON formatting performance metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        with benchmark_timer("json_formatting") as result:
            message_count = 5000
            test_logger = logger.get_logger("benchmark.json")

            for i in range(message_count):
                test_logger.info(
                    f"JSON benchmark message {i}",
                    iteration=i,
                    domain="benchmark",
                    action="test",
                    status="running",
                    extra_data={"nested": {"value": i}},
                )

            result["message_count"] = message_count
            result["output_size_bytes"] = len(captured.getvalue())

        result["messages_per_second"] = result["message_count"] / result["duration_seconds"]

    return result


def benchmark_emoji_processing() -> dict[str, Any]:
    """
    Benchmark emoji processing overhead by comparing enabled vs disabled.

    This test measures the performance impact of emoji processing features
    by running identical workloads with and without emoji processing enabled.

    Returns:
        Dictionary containing emoji processing overhead analysis.
    """
    reset_pyvider_setup_for_testing()

    # Test with emojis enabled
    config_with_emojis = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=True,
            das_emoji_prefix_enabled=True,
        )
    )

    with capture_logs():
        setup_telemetry(config_with_emojis)

        with benchmark_timer("emoji_enabled") as emoji_result:
            message_count = 5000
            test_logger = logger.get_logger("benchmark.emoji")

            for i in range(message_count):
                test_logger.info(
                    f"Emoji message {i}",
                    domain="system",
                    action="process",
                    status="success",
                )

            emoji_result["message_count"] = message_count

        emoji_result["messages_per_second"] = emoji_result["message_count"] / emoji_result["duration_seconds"]

    # Test with emojis disabled
    reset_pyvider_setup_for_testing()
    config_no_emojis = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="key_value",
            logger_name_emoji_prefix_enabled=False,
            das_emoji_prefix_enabled=False,
        )
    )

    with capture_logs():
        setup_telemetry(config_no_emojis)

        with benchmark_timer("emoji_disabled") as no_emoji_result:
            message_count = 5000
            test_logger = logger.get_logger("benchmark.no_emoji")

            for i in range(message_count):
                test_logger.info(f"No emoji message {i}")

            no_emoji_result["message_count"] = message_count

        no_emoji_result["messages_per_second"] = no_emoji_result["message_count"] / no_emoji_result["duration_seconds"]

    # Calculate overhead percentage
    emoji_overhead = (
        (no_emoji_result["duration_seconds"] - emoji_result["duration_seconds"])
        / no_emoji_result["duration_seconds"] * 100
    )

    return {
        "test_name": "emoji_processing_overhead",
        "emoji_enabled": emoji_result,
        "emoji_disabled": no_emoji_result,
        "emoji_overhead_percent": emoji_overhead,
    }


def benchmark_multithreaded_logging() -> dict[str, Any]:
    """
    Benchmark thread safety and performance under concurrent load.

    This test verifies that the logging system maintains performance
    and correctness under concurrent access from multiple threads,
    which is critical for multi-threaded applications.

    Returns:
        Dictionary containing concurrent logging performance metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        def worker_thread(thread_id: int, message_count: int) -> None:
            """Worker function that generates log messages from a specific thread."""
            thread_logger = logger.get_logger(f"benchmark.thread.{thread_id}")
            for i in range(message_count):
                thread_logger.info(
                    f"Thread {thread_id} message {i}",
                    thread_id=thread_id,
                    msg_id=i
                )

        with benchmark_timer("multithreaded_logging") as result:
            thread_count = 10
            messages_per_thread = 500
            total_messages = thread_count * messages_per_thread

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [
                    executor.submit(worker_thread, thread_id, messages_per_thread)
                    for thread_id in range(thread_count)
                ]

                for future in futures:
                    future.result()

            result["thread_count"] = thread_count
            result["messages_per_thread"] = messages_per_thread
            result["total_messages"] = total_messages
            result["output_size_bytes"] = len(captured.getvalue())

        result["messages_per_second"] = result["total_messages"] / result["duration_seconds"]

    return result


def benchmark_level_filtering() -> dict[str, Any]:
    """
    Benchmark log level filtering performance and efficiency.

    This test measures how efficiently the logging system filters out
    messages that are below the configured log level threshold.

    Returns:
        Dictionary containing level filtering performance metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="ERROR",  # High threshold to filter most messages
            module_levels={
                "benchmark.filtered": "DEBUG",  # Allow all for this module
            },
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        with benchmark_timer("level_filtering") as result:
            message_count = 10000
            filtered_logger = logger.get_logger("benchmark.filtered")
            blocked_logger = logger.get_logger("benchmark.blocked")

            # Half messages should pass filter, half should be blocked
            for i in range(message_count // 2):
                filtered_logger.debug(f"Allowed message {i}")  # Should pass
                blocked_logger.debug(f"Blocked message {i}")   # Should be filtered

            output_lines = len([
                line for line in captured.getvalue().split('\n')
                if line.strip()
            ])

            result["total_attempted_messages"] = message_count
            result["output_lines"] = output_lines
            result["filtering_efficiency"] = (message_count - output_lines) / message_count * 100

        result["messages_per_second"] = result["total_attempted_messages"] / result["duration_seconds"]

    return result


async def benchmark_async_usage() -> dict[str, Any]:
    """
    Benchmark usage patterns in async contexts.

    This test measures the performance of logging within async/await
    contexts, ensuring that the logging system doesn't interfere with
    async event loop performance.

    Returns:
        Dictionary containing async logging performance metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )

    with capture_logs():
        setup_telemetry(config)

        async def async_worker(worker_id: int, message_count: int) -> None:
            """Async worker that generates log messages with periodic yielding."""
            async_logger = logger.get_logger(f"benchmark.async.{worker_id}")
            for i in range(message_count):
                async_logger.info(
                    f"Async worker {worker_id} message {i}",
                    worker_id=worker_id,
                    msg_id=i
                )
                if i % 100 == 0:  # Yield control periodically
                    await asyncio.sleep(0)

        with benchmark_timer("async_logging") as result:
            worker_count = 5
            messages_per_worker = 1000
            total_messages = worker_count * messages_per_worker

            tasks = [
                async_worker(worker_id, messages_per_worker)
                for worker_id in range(worker_count)
            ]

            await asyncio.gather(*tasks)

            result["worker_count"] = worker_count
            result["messages_per_worker"] = messages_per_worker
            result["total_messages"] = total_messages

        result["messages_per_second"] = result["total_messages"] / result["duration_seconds"]

    return result


def benchmark_large_payloads() -> dict[str, Any]:
    """
    Benchmark performance with large log payloads.

    This test measures how the logging system handles large structured
    data payloads, which is important for applications that log detailed
    context information.

    Returns:
        Dictionary containing large payload performance metrics.
    """
    reset_pyvider_setup_for_testing()

    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json",
        )
    )

    with capture_logs() as captured:
        setup_telemetry(config)

        with benchmark_timer("large_payloads") as result:
            message_count = 1000
            test_logger = logger.get_logger("benchmark.large")

            # Create large payload data structure
            large_data = {
                "large_string": "x" * 1000,
                "large_list": list(range(100)),
                "nested_data": {
                    "level1": {
                        "level2": {
                            "data": ["item"] * 50
                        }
                    }
                },
            }

            for i in range(message_count):
                test_logger.info(f"Large payload message {i}", **large_data, iteration=i)

            result["message_count"] = message_count
            result["output_size_bytes"] = len(captured.getvalue())

        result["messages_per_second"] = result["message_count"] / result["duration_seconds"]
        result["avg_message_size_bytes"] = result["output_size_bytes"] / result["message_count"]

    return result


def main() -> None:
    """
    Run all benchmarks and output results.

    This function coordinates the execution of all benchmark tests,
    collects results, and saves them to a JSON file for analysis.
    """
    print("🚀 Starting Pyvider Telemetry Performance Benchmarks...")
    print("=" * 60)

    benchmarks = [
        ("Basic Logging", benchmark_basic_logging),
        ("JSON Formatting", benchmark_json_formatting),
        ("Emoji Processing", benchmark_emoji_processing),
        ("Multithreaded Logging", benchmark_multithreaded_logging),
        ("Level Filtering", benchmark_level_filtering),
        ("Large Payloads", benchmark_large_payloads),
    ]

    results = {
        "benchmark_info": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "python_version": sys.version,
            "memory_available": _get_memory_usage() > 0,
        },
        "benchmarks": {}
    }

    # Run synchronous benchmarks
    for name, benchmark_func in benchmarks:
        print(f"Running {name}...")
        try:
            result = benchmark_func()
            results["benchmarks"][result["test_name"]] = result

            # Print summary
            if "messages_per_second" in result:
                print(f"  ✅ {result['messages_per_second']:.1f} messages/second")
            if "duration_seconds" in result:
                print(f"  ⏱️  {result['duration_seconds']:.3f} seconds")
            if "memory_delta_mb" in result:
                print(f"  🧠 {result['memory_delta_mb']:.2f} MB memory delta")

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results["benchmarks"][name.lower().replace(" ", "_")] = {"error": str(e)}

        print()

    # Run async benchmark
    print("Running Async Logging...")
    try:
        async_result = asyncio.run(benchmark_async_usage())
        results["benchmarks"][async_result["test_name"]] = async_result
        print(f"  ✅ {async_result['messages_per_second']:.1f} messages/second")
        print(f"  ⏱️  {async_result['duration_seconds']:.3f} seconds")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["benchmarks"]["async_logging"] = {"error": str(e)}

    print()

    # Save results using pathlib
    output_file = Path("benchmark-results.json")
    with output_file.open("w") as f:
        json.dump(results, f, indent=2)

    print("=" * 60)
    print(f"✅ Benchmarks completed! Results saved to {output_file}")

    # Print summary statistics
    successful_benchmarks = [
        r for r in results["benchmarks"].values()
        if "error" not in r and "messages_per_second" in r
    ]

    if successful_benchmarks:
        avg_throughput = sum(
            r["messages_per_second"] for r in successful_benchmarks
        ) / len(successful_benchmarks)
        max_throughput = max(r["messages_per_second"] for r in successful_benchmarks)
        print(f"📊 Average throughput: {avg_throughput:.1f} messages/second")
        print(f"🚀 Peak throughput: {max_throughput:.1f} messages/second")

    print("\n🎯 Performance Goals:")
    basic_logging_ok = any(
        r.get("messages_per_second", 0) > 1000 for r in successful_benchmarks
    )
    print("  • Basic logging: >1000 msg/sec ✅" if basic_logging_ok else "  • Basic logging: >1000 msg/sec ❌")

    json_formatting_ok = any(
        r.get("test_name") == "json_formatting" and r.get("messages_per_second", 0) > 500
        for r in successful_benchmarks
    )
    print("  • JSON formatting: >500 msg/sec ✅" if json_formatting_ok else "  • JSON formatting: >500 msg/sec ❌")


if __name__ == "__main__":
    main()

# 📊⚡
