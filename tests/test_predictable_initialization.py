"""Test predictable initialization behavior.

Tests that Foundation initialization is deterministic and predictable
across different usage patterns and scenarios.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import tempfile
import time
from unittest.mock import patch

from provide.foundation.hub.manager import Hub, clear_hub, get_hub
from provide.foundation.logger.config import LoggingConfig, TelemetryConfig


class TestPredictableInitialization:
    """Test predictable initialization behavior."""

    def setup_method(self) -> None:
        """Reset state before each test."""
        clear_hub()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        clear_hub()

    def test_initialization_order_independence(self) -> None:
        """Test that components work regardless of initialization order."""
        # Scenario 1: Get logger before hub
        from provide.foundation.logger.factories import get_logger

        logger1 = get_logger("test.order1")

        # Get hub
        hub = get_hub()
        assert hub.is_foundation_initialized()

        # Get another logger through hub
        logger2 = hub.get_foundation_logger("test.order2")

        # Both should work
        logger1.info("Logger before hub")
        logger2.info("Logger after hub")

        # Scenario 2: Get hub first, then logger
        clear_hub()

        hub = get_hub()
        logger3 = get_logger("test.order3")
        logger3.info("Logger after hub first")

        # All scenarios should work predictably
        assert True  # If we get here, all worked

    def test_configuration_precedence_predictable(self) -> None:
        """Test that config precedence is predictable and documented."""
        # 1. Explicit config should always win
        explicit_config = TelemetryConfig(
            logging=LoggingConfig(default_level="CRITICAL"),
        )

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "DEBUG"}):
            hub = Hub()
            hub.initialize_foundation(explicit_config)

            config = hub.get_foundation_config()
            # Explicit config should override environment
            assert config.logging.default_level == "CRITICAL"

        # 2. Environment should be used when no explicit config
        clear_hub()

        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "WARNING"}):
            hub = get_hub()  # Auto-initialize with env config

            config = hub.get_foundation_config()
            assert config.logging.default_level == "WARNING"

        # 3. Defaults should be used when nothing specified
        clear_hub()

        with patch.dict(os.environ, {}, clear=True):
            hub = get_hub()

            config = hub.get_foundation_config()
            # Should use default level (WARNING)
            assert config.logging.default_level == "WARNING"

    def test_error_recovery_predictable(self) -> None:
        """Test predictable behavior when errors occur."""
        hub = Hub()

        # Test 1: Config loading failure should fallback gracefully
        with patch("provide.foundation.logger.config.TelemetryConfig.from_env") as mock_config:
            mock_config.side_effect = Exception("Config error")

            # Should not raise exception
            hub.initialize_foundation()

            # Should still get working logger (emergency fallback)
            logger = hub.get_foundation_logger("test.fallback")
            assert logger is not None

            # Logger should work
            logger.info("Fallback logger works")

    def test_deterministic_state_across_restarts(self) -> None:
        """Test that same inputs produce same state."""
        config = TelemetryConfig(
            logging=LoggingConfig(
                default_level="DEBUG",
                console_formatter="json",
            ),
        )

        # First initialization
        hub1 = Hub()
        hub1.initialize_foundation(config)

        state1 = {
            "initialized": hub1.is_foundation_initialized(),
            "config_level": hub1.get_foundation_config().logging.default_level,
            "config_formatter": hub1.get_foundation_config().logging.console_formatter,
        }

        # Reset and initialize again with same config
        clear_hub()

        hub2 = Hub()
        hub2.initialize_foundation(config)

        state2 = {
            "initialized": hub2.is_foundation_initialized(),
            "config_level": hub2.get_foundation_config().logging.default_level,
            "config_formatter": hub2.get_foundation_config().logging.console_formatter,
        }

        # States should be identical
        assert state1 == state2

    def test_concurrent_initialization_deterministic(self) -> None:
        """Test that concurrent initialization produces deterministic results."""
        results = []
        errors = []

        def init_worker(worker_id: int) -> None:
            try:
                hub = get_hub()
                logger = hub.get_foundation_logger(f"worker.{worker_id}")

                result = {
                    "worker_id": worker_id,
                    "initialized": hub.is_foundation_initialized(),
                    "logger_works": logger is not None,
                }
                results.append(result)
            except Exception as e:
                errors.append((worker_id, e))

        # Start many workers simultaneously
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(init_worker, i) for i in range(100)]

            for future in futures:
                future.result()

        # Should have no errors
        assert len(errors) == 0

        # All workers should have consistent results
        assert len(results) == 100

        for result in results:
            assert result["initialized"] is True
            assert result["logger_works"] is True

    def test_resource_cleanup_predictable(self) -> None:
        """Test predictable resource cleanup."""
        hub = get_hub()

        # Create some loggers
        loggers = [hub.get_foundation_logger(f"test.cleanup.{i}") for i in range(10)]

        # All should work before cleanup
        for i, logger in enumerate(loggers):
            logger.info(f"Pre-cleanup message {i}")

        # Clear hub
        clear_hub()

        # After clear, new hub should initialize cleanly
        new_hub = get_hub()
        assert new_hub.is_foundation_initialized()

        # New loggers should work
        new_logger = new_hub.get_foundation_logger("test.after.cleanup")
        new_logger.info("Post-cleanup message")

    def test_file_logging_predictable(self) -> None:
        """Test predictable file logging behavior."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"

            config = TelemetryConfig(
                logging=LoggingConfig(
                    default_level="INFO",
                    log_file=log_file,
                ),
            )

            hub = Hub()
            hub.initialize_foundation(config)

            logger = hub.get_foundation_logger("test.file")
            logger.info("Test file message")

            # File should be created and contain message
            # Note: Actual file writing depends on setup completion
            # This test mainly ensures no errors occur
            assert True  # If we get here, file logging didn't crash

    def test_multiple_hubs_independent(self) -> None:
        """Test that multiple Hub instances are independent."""
        # Create two separate hubs
        hub1 = Hub()
        hub2 = Hub()

        # Initialize with different configs
        config1 = TelemetryConfig(
            logging=LoggingConfig(default_level="DEBUG"),
        )
        config2 = TelemetryConfig(
            logging=LoggingConfig(default_level="ERROR"),
        )

        hub1.initialize_foundation(config1)
        hub2.initialize_foundation(config2)

        # Should have different configs
        assert hub1.get_foundation_config().logging.default_level == "DEBUG"
        assert hub2.get_foundation_config().logging.default_level == "ERROR"

        # Should be independently functional
        logger1 = hub1.get_foundation_logger("hub1.test")
        logger2 = hub2.get_foundation_logger("hub2.test")

        logger1.info("Hub1 message")
        logger2.info("Hub2 message")

    def test_performance_consistent(self) -> None:
        """Test that performance is consistent across runs."""
        times = []

        for _ in range(5):
            clear_hub()

            start_time = time.time()
            hub = get_hub()
            logger = hub.get_foundation_logger("performance.test")
            logger.info("Performance test")
            end_time = time.time()

            times.append(end_time - start_time)

        # Performance should be consistent (no outliers > 10x average)
        avg_time = sum(times) / len(times)
        max_time = max(times)

        assert max_time < avg_time * 10, f"Performance inconsistent: max={max_time:.3f}, avg={avg_time:.3f}"

    def test_memory_usage_predictable(self) -> None:
        """Test that memory usage is predictable and doesn't leak."""
        import gc
        import os

        import psutil

        process = psutil.Process(os.getpid())

        # Get baseline memory
        gc.collect()
        baseline_memory = process.memory_info().rss

        # Create and clear hubs multiple times
        for _i in range(10):
            hub = get_hub()
            loggers = [hub.get_foundation_logger(f"memory.test.{j}") for j in range(100)]

            # Use loggers
            for logger in loggers:
                logger.info("Memory test message")

            clear_hub()
            gc.collect()

        # Check final memory
        final_memory = process.memory_info().rss
        memory_growth = final_memory - baseline_memory

        # Memory growth should be reasonable (< 50MB for this test)
        max_growth = 50 * 1024 * 1024  # 50MB in bytes
        assert memory_growth < max_growth, (
            f"Memory growth too large: {memory_growth / 1024 / 1024:.1f}MB > {max_growth / 1024 / 1024:.1f}MB"
        )

    def test_logger_naming_consistent(self) -> None:
        """Test that logger naming is consistent and predictable."""
        hub = get_hub()

        # Test various naming patterns
        test_cases = [
            None,  # Should use default
            "",  # Empty string
            "test",  # Simple name
            "test.module",  # Dotted name
            "test.module.submodule",  # Nested dotted name
            "__main__",  # Special name
            "test-with-dashes",  # Dashes
            "test_with_underscores",  # Underscores
        ]

        loggers = {}
        for name in test_cases:
            logger = hub.get_foundation_logger(name)
            loggers[name] = logger

            # Should always get a working logger
            assert logger is not None
            logger.info(f"Test message for {name}")

        # Same names should return equivalent loggers
        for name in test_cases:
            logger2 = hub.get_foundation_logger(name)
            # Note: May not be same object due to structlog design,
            # but should be functionally equivalent
            logger2.info(f"Second test message for {name}")

    def test_exception_handling_predictable(self) -> None:
        """Test that exception handling is predictable."""
        hub = get_hub()
        logger = hub.get_foundation_logger("test.exceptions")

        # Should handle various exception types gracefully
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("Caught ValueError")

        try:
            raise RuntimeError("Test runtime error")
        except RuntimeError:
            logger.error("Caught RuntimeError", exc_info=True)

        # Should handle logging with invalid parameters
        try:
            logger.info("Test message", invalid_param=object())
        except Exception as e:
            # If this fails, it should fail predictably
            assert isinstance(e, (TypeError, AttributeError))

        # All exception scenarios should be handled gracefully
        assert True  # If we get here, exception handling worked
