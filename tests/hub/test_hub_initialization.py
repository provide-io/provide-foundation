#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test Hub initialization and Foundation lifecycle management.

Tests for the unified initialization through Hub, replacing legacy setup functions."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading
import time
from typing import TextIO

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.hub.manager import Hub, clear_hub, get_hub
from provide.foundation.logger.config import LoggingConfig, TelemetryConfig


class TestHubInitialization(FoundationTestCase):
    """Test Hub-based Foundation initialization."""

    def setup_method(self) -> None:
        """Reset Hub state before each test."""
        super().setup_method()
        clear_hub()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        clear_hub()
        super().teardown_method()

    @pytest.fixture(autouse=True)
    def setup_test_output(self, captured_stderr_for_foundation: TextIO) -> None:
        """Setup output capture for all tests."""
        self.captured_output = captured_stderr_for_foundation

    def test_hub_lazy_initialization(self) -> None:
        """Test that Hub auto-initializes Foundation on first access."""
        # Getting shared hub should auto-initialize Foundation
        hub = get_hub()
        assert hub.is_foundation_initialized()

        # Should have logger and config registered
        logger_instance = hub._component_registry.get("foundation.logger.instance", "singleton")
        config = hub._component_registry.get("foundation.config", "singleton")

        assert logger_instance is not None
        assert config is not None

    def test_hub_idempotent_initialization(self) -> None:
        """Test that multiple initialization calls are safe."""
        hub = Hub()

        # Multiple initialization calls should be safe
        hub.initialize_foundation()
        hub.initialize_foundation()
        hub.initialize_foundation()

        assert hub.is_foundation_initialized()

        # Should only have one logger instance
        entries = [e for e in hub._component_registry if e.name == "foundation.logger.instance"]
        assert len(entries) == 1

    def test_hub_config_precedence(self) -> None:
        """Test that explicit config takes precedence over environment."""
        # Create custom config
        custom_config = TelemetryConfig(
            logging=LoggingConfig(default_level="DEBUG"),
        )

        hub = Hub()
        hub.initialize_foundation(custom_config)

        # Should use the custom config
        stored_config = hub.get_foundation_config()
        assert stored_config.logging.default_level == "DEBUG"

    def test_hub_environment_config_fallback(self) -> None:
        """Test fallback to environment configuration."""
        with patch.dict(os.environ, {"PROVIDE_LOG_LEVEL": "WARNING"}):
            hub = Hub()
            hub.initialize_foundation()  # No explicit config

            config = hub.get_foundation_config()
            assert config.logging.default_level == "WARNING"

    def test_hub_thread_safety(self) -> None:
        """Test thread-safe Hub initialization."""
        hubs = []
        errors = []

        def get_hub_thread() -> None:
            try:
                hub = get_hub()
                hubs.append(hub)
            except Exception as e:
                errors.append(e)

        # Start multiple threads simultaneously
        threads = [threading.Thread(daemon=True, target=get_hub_thread) for _ in range(10)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=10.0)

        # Should have no errors
        assert len(errors) == 0

        # All threads should get the same hub instance
        assert len(hubs) == 10
        assert all(hub is hubs[0] for hub in hubs)

    def test_hub_logger_access_with_output(self) -> None:
        """Test getting loggers through Hub and verify output."""
        hub = get_hub()

        # Should be able to get loggers
        logger1 = hub.get_foundation_logger("test.module1")
        logger2 = hub.get_foundation_logger("test.module2")

        assert logger1 is not None
        assert logger2 is not None

        # Test logging and verify output is captured
        test_message1 = "Test message from module1"
        test_message2 = "Test message from module2"

        logger1.warning(test_message1)
        logger2.warning(test_message2)

        # Check that messages were captured
        output = self.captured_output.getvalue()
        assert test_message1 in output
        assert test_message2 in output

    def test_hub_initialization_order_independence(self) -> None:
        """Test that initialization order doesn't matter."""
        # Get logger before explicit hub access
        from provide.foundation.logger.factories import get_logger

        logger1 = get_logger("test1")

        # Get shared hub
        hub = get_hub()

        # Get another logger through hub
        logger2 = hub.get_foundation_logger("test2")

        # Both should work
        assert logger1 is not None
        assert logger2 is not None

        # Should be able to log with both
        logger1.info("test message 1")
        logger2.info("test message 2")

    def test_hub_error_recovery(self) -> None:
        """Test graceful fallback on initialization errors."""
        hub = Hub()

        # Mock config loading to fail
        with patch("provide.foundation.logger.config.TelemetryConfig.from_env") as mock_from_env:
            mock_from_env.side_effect = Exception("Config loading failed")

            # Should still initialize with fallback
            hub.initialize_foundation()

            # Should still get working logger (fallback)
            logger = hub.get_foundation_logger("test")
            assert logger is not None

    def test_hub_deterministic_state(self) -> None:
        """Test that same config produces same state."""
        config = TelemetryConfig(
            logging=LoggingConfig(default_level="INFO"),
        )

        # Initialize two hubs with same config
        hub1 = Hub()
        hub1.initialize_foundation(config)

        hub2 = Hub()
        hub2.initialize_foundation(config)

        # Both should be initialized
        assert hub1.is_foundation_initialized()
        assert hub2.is_foundation_initialized()

        # Both should have same config
        config1 = hub1.get_foundation_config()
        config2 = hub2.get_foundation_config()

        assert config1.logging.default_level == config2.logging.default_level

    def test_hub_concurrent_logger_creation(self) -> None:
        """Test concurrent logger creation through Hub."""
        hub = get_hub()
        loggers = []
        errors = []

        def create_logger(name_suffix: int) -> None:
            try:
                logger = hub.get_foundation_logger(f"test.concurrent.{name_suffix}")
                loggers.append(logger)
                logger.info(f"Test message {name_suffix}")
            except Exception as e:
                errors.append(e)

        # Create loggers concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_logger, i) for i in range(50)]

            for future in as_completed(futures):
                future.result()  # Wait for completion

        # Should have no errors
        assert len(errors) == 0

        # Should have created all loggers
        assert len(loggers) == 50

        # All loggers should be functional
        assert all(logger is not None for logger in loggers)

    def test_hub_performance_requirements(self) -> None:
        """Test that Hub meets performance requirements."""
        # Test initialization speed
        start_time = time.time()
        hub = Hub()
        hub.initialize_foundation()
        init_time = time.time() - start_time

        # Should initialize in <100ms
        assert init_time < 0.1, f"Initialization took {init_time:.3f}s, expected <0.1s"

        # Test logger creation speed
        start_time = time.time()
        for i in range(1000):
            logger = hub.get_foundation_logger(f"performance.test.{i}")
            assert logger is not None

        create_time = time.time() - start_time
        avg_time = create_time / 1000

        # Should create logger in <1ms average
        assert avg_time < 0.001, f"Logger creation averaged {avg_time:.6f}s, expected <0.001s"


# 🧱🏗️🔚
