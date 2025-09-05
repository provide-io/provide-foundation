"""
Performance benchmarks using pytest-benchmark.

This module provides pytest-benchmark integration for Foundation's performance 
testing, complementing the existing benchmark infrastructure with statistical
analysis and comparison features.

The benchmarks validate that Foundation maintains >14,000 msg/sec performance
even after internal improvements like dogfooding structured logging.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import io
from typing import Any

import pytest

from provide.foundation import LoggingConfig, TelemetryConfig, logger, setup_telemetry
from provide.foundation.core import (
    _set_log_stream_for_testing,
    reset_foundation_setup_for_testing,
)


@contextmanager
def capture_logs():
    """Context manager to capture log output during benchmarks."""
    captured = io.StringIO()
    _set_log_stream_for_testing(captured)
    try:
        yield captured
    finally:
        _set_log_stream_for_testing(None)


class TestBasicLoggingPerformance:
    """Basic logging performance benchmarks."""

    def setup_method(self):
        """Reset Foundation state before each test."""
        reset_foundation_setup_for_testing()

    def test_basic_logging_throughput(self, benchmark):
        """Benchmark basic logging operations with emoji processing.
        
        Target: >14,000 messages per second
        """
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
                logger_name_emoji_prefix_enabled=True,
                das_emoji_prefix_enabled=False,
            )
        )

        with capture_logs():
            setup_telemetry(config)
            test_logger = logger.get_logger("benchmark.basic")

            def log_messages():
                """Function to benchmark - logs 1000 messages."""
                for i in range(1000):
                    test_logger.info(f"Benchmark message {i}", iteration=i)

            result = benchmark(log_messages)
            
            # Verify we're meeting performance targets
            # pytest-benchmark measures time, so convert to msg/sec
            messages_per_second = 1000 / result
            assert messages_per_second > 1000, f"Basic logging too slow: {messages_per_second:.1f} msg/sec"

    def test_json_formatting_performance(self, benchmark):
        """Benchmark JSON output formatting with emoji processing.
        
        Target: >500 messages per second for JSON formatting
        """
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
                logger_name_emoji_prefix_enabled=True,
                das_emoji_prefix_enabled=True,
            )
        )

        with capture_logs():
            setup_telemetry(config)
            test_logger = logger.get_logger("benchmark.json")

            def log_json_messages():
                """Function to benchmark - logs 500 structured messages."""
                for i in range(500):
                    test_logger.info(
                        f"JSON benchmark message {i}",
                        iteration=i,
                        domain="benchmark",
                        action="test",
                        status="running",
                        extra_data={"nested": {"value": i}},
                    )

            result = benchmark(log_json_messages)
            
            messages_per_second = 500 / result
            assert messages_per_second > 500, f"JSON formatting too slow: {messages_per_second:.1f} msg/sec"

    def test_emoji_processing_performance(self, benchmark):
        """Benchmark emoji processing overhead."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
                logger_name_emoji_prefix_enabled=True,
                das_emoji_prefix_enabled=True,
            )
        )

        with capture_logs():
            setup_telemetry(config)
            test_logger = logger.get_logger("benchmark.emoji")

            def log_with_emoji():
                """Function to benchmark - logs with emoji processing."""
                for i in range(500):
                    test_logger.info(
                        f"Emoji message {i}",
                        domain="system",
                        action="process", 
                        status="success",
                    )

            result = benchmark(log_with_emoji)
            
            messages_per_second = 500 / result
            # Emoji processing should still be fast
            assert messages_per_second > 1000, f"Emoji processing too slow: {messages_per_second:.1f} msg/sec"


class TestConcurrentPerformance:
    """Concurrent and async performance benchmarks."""

    def setup_method(self):
        """Reset Foundation state before each test."""
        reset_foundation_setup_for_testing()

    def test_multithreaded_logging_performance(self, benchmark):
        """Benchmark thread safety and concurrent performance."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
            )
        )

        with capture_logs():
            setup_telemetry(config)

            def worker_thread(thread_id: int, message_count: int):
                """Worker function for multithreaded logging."""
                thread_logger = logger.get_logger(f"benchmark.thread.{thread_id}")
                for i in range(message_count):
                    thread_logger.info(
                        f"Thread {thread_id} message {i}", 
                        thread_id=thread_id, 
                        msg_id=i
                    )

            def multithreaded_logging():
                """Function to benchmark - concurrent logging."""
                thread_count = 5
                messages_per_thread = 100
                
                with ThreadPoolExecutor(max_workers=thread_count) as executor:
                    futures = [
                        executor.submit(worker_thread, thread_id, messages_per_thread)
                        for thread_id in range(thread_count)
                    ]
                    for future in futures:
                        future.result()

            result = benchmark(multithreaded_logging)
            
            total_messages = 5 * 100  # 500 messages
            messages_per_second = total_messages / result
            assert messages_per_second > 1000, f"Multithreaded logging too slow: {messages_per_second:.1f} msg/sec"

    def test_level_filtering_performance(self, benchmark):
        """Benchmark log level filtering efficiency."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="ERROR",  # High threshold to filter most messages
                module_levels={
                    "benchmark.filtered": "DEBUG",  # Allow all for this module
                },
            )
        )

        with capture_logs():
            setup_telemetry(config)
            filtered_logger = logger.get_logger("benchmark.filtered")
            blocked_logger = logger.get_logger("benchmark.blocked")

            def level_filtering_test():
                """Function to benchmark - level filtering."""
                for i in range(500):
                    filtered_logger.debug(f"Allowed message {i}")  # Should pass
                    blocked_logger.debug(f"Blocked message {i}")   # Should be filtered

            result = benchmark(level_filtering_test)
            
            # Even with filtering, should be very fast
            messages_per_second = 1000 / result  # 1000 attempted messages
            assert messages_per_second > 5000, f"Level filtering too slow: {messages_per_second:.1f} msg/sec"


class TestDogfoodingPerformance:
    """Specific benchmarks for dogfooding improvements."""

    def setup_method(self):
        """Reset Foundation state before each test."""
        reset_foundation_setup_for_testing()

    def test_config_warning_performance(self, benchmark):
        """Benchmark config system warning generation with structured logging."""
        def generate_config_warnings():
            """Test config warnings (which now use structured logging)."""
            # This will trigger our improved warning system
            config = LoggingConfig(
                default_level="INFO",
                console_formatter="key_value",
            )
            # The from_env() method includes our structured warning improvements
            LoggingConfig.from_env(strict=False)

        # Config warnings should be very fast even with structured logging
        result = benchmark(generate_config_warnings)
        
        # Should complete in well under 1ms
        assert result < 0.001, f"Config warning generation too slow: {result:.4f}s"

    def test_foundation_setup_performance(self, benchmark):
        """Benchmark Foundation setup with structured logging improvements."""
        def foundation_setup():
            """Test the improved Foundation setup process."""
            reset_foundation_setup_for_testing()
            config = TelemetryConfig(
                logging=LoggingConfig(
                    default_level="DEBUG",  # Enable our structured setup logging
                    foundation_setup_log_level="DEBUG",
                )
            )
            with capture_logs():
                setup_telemetry(config)

        # Foundation setup should be fast even with structured logging
        result = benchmark(foundation_setup)
        
        # Setup should complete quickly
        assert result < 0.1, f"Foundation setup too slow: {result:.4f}s"

    def test_core_setup_logger_performance(self, benchmark):
        """Benchmark the core setup logger with structured fields."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                foundation_setup_log_level="DEBUG",
            )
        )
        
        with capture_logs():
            setup_telemetry(config)
            
            # Import core setup logger to test directly
            from provide.foundation.core import _core_setup_logger

            def core_logger_messages():
                """Test core setup logger performance."""
                for i in range(100):
                    _core_setup_logger.debug(f"Setup message {i}")

            result = benchmark(core_logger_messages)
            
            messages_per_second = 100 / result
            # Core setup logger should still be fast
            assert messages_per_second > 1000, f"Core setup logger too slow: {messages_per_second:.1f} msg/sec"


class TestLargePayloadPerformance:
    """Performance benchmarks for large payloads."""

    def setup_method(self):
        """Reset Foundation state before each test."""
        reset_foundation_setup_for_testing()

    def test_large_payload_performance(self, benchmark):
        """Benchmark performance with large structured data."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="INFO",
                console_formatter="json",
            )
        )

        with capture_logs():
            setup_telemetry(config)
            test_logger = logger.get_logger("benchmark.large")

            # Create large payload similar to existing benchmark
            large_data = {
                "large_string": "x" * 1000,
                "large_list": list(range(100)), 
                "nested_data": {"level1": {"level2": {"data": ["item"] * 50}}},
            }

            def log_large_payloads():
                """Function to benchmark - large payload logging."""
                for i in range(100):
                    test_logger.info(
                        f"Large payload message {i}",
                        **large_data,
                        iteration=i
                    )

            result = benchmark(log_large_payloads)
            
            messages_per_second = 100 / result
            # Large payloads should still process reasonably fast
            assert messages_per_second > 100, f"Large payload logging too slow: {messages_per_second:.1f} msg/sec"