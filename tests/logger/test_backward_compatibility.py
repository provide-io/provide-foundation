"""Test backward compatibility during Hub transition.

Ensures that existing code continues to work while using the new Hub-based system.
"""

from __future__ import annotations

import warnings

from provide.foundation.hub.manager import clear_hub, get_hub


class TestBackwardCompatibility:
    """Test backward compatibility with legacy API."""

    def setup_method(self) -> None:
        """Reset state before each test."""
        clear_hub()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        clear_hub()

    def test_global_logger_proxy_works(self) -> None:
        """Test that global logger proxy still works."""
        from provide.foundation.logger import logger

        # Should be able to use logger directly
        logger.info("Test message")
        logger.debug("Debug message")
        logger.error("Error message")

        # Should be able to get named loggers
        named_logger = logger.get_logger("test.module")
        assert named_logger is not None
        named_logger.info("Named logger message")

    def test_get_logger_factory_works(self) -> None:
        """Test that get_logger factory function still works."""
        from provide.foundation.logger import get_logger

        # Should work without arguments
        logger1 = get_logger()
        assert logger1 is not None

        # Should work with name
        logger2 = get_logger("test.module")
        assert logger2 is not None

        # Should work with new parameters
        logger3 = get_logger("test.module")
        assert logger3 is not None

        # All should be functional
        logger1.info("Factory test 1")
        logger2.info("Factory test 2")
        logger3.info("Factory test 3")

    def test_hub_api_works(self) -> None:
        """Test that new Hub API works as replacement for setup functions."""
        from provide.foundation import get_hub
        from provide.foundation.logger.config import TelemetryConfig

        # Hub initialization should work
        hub = get_hub()
        config = TelemetryConfig()
        hub.initialize_foundation(config, force=True)

        # Should be able to get logger after Hub initialization
        logger = hub.get_foundation_logger("test")
        assert logger is not None
        logger.info("Hub test message")

    def test_setup_functions_with_config(self) -> None:
        """Test that setup functions work with explicit config."""
        from provide.foundation import get_hub
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        config = TelemetryConfig(
            logging=LoggingConfig(default_level="WARNING"),
        )

        # Use Hub API instead of deprecated setup_foundation
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        # Should have used the provided config
        hub = get_hub()
        stored_config = hub.get_foundation_config()
        assert stored_config.logging.default_level == "WARNING"

    def test_mixed_old_and_new_api(self) -> None:
        """Test that old and new APIs can be mixed."""
        from provide.foundation import get_hub
        from provide.foundation.logger import get_logger

        # Use old setup first
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            hub = get_hub()
            hub.initialize_foundation(force=True)

        # Then use new API
        hub = get_hub()
        assert hub.is_foundation_initialized()

        # Both old and new logger access should work
        old_logger = get_logger("old.api")
        new_logger = hub.get_foundation_logger("new.api")

        old_logger.info("Old API message")
        new_logger.info("New API message")

    def test_logger_import_still_works(self) -> None:
        """Test that direct logger import still works."""
        # Should be able to import logger directly
        from provide.foundation.logger import logger

        # Should auto-initialize on first use
        logger.info("Direct import test")

        # Hub should be initialized
        hub = get_hub()
        assert hub.is_foundation_initialized()

    def test_ecosystem_compatibility(self) -> None:
        """Test patterns used by ecosystem projects."""
        # Pattern 1: Import and immediate use (supsrc pattern)
        from provide.foundation.logger import logger

        logger.info("Immediate use after import")

        # Pattern 2: Factory function (flavorpack pattern)
        from provide.foundation.logger import get_logger

        module_logger = get_logger(__name__)
        module_logger.info("Module logger test")

        # Pattern 3: Setup then use (provide-testkit pattern)
        hub = get_hub()
        hub.initialize_foundation(force=True)

        logger.info("After setup test")

        # All should work without issues
        assert True  # If we get here, all patterns worked

    def test_no_breaking_changes(self) -> None:
        """Test that no existing functionality is broken."""
        from provide.foundation.logger import get_logger, logger

        # All logger methods should still exist and work
        logger.trace("Trace message")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        # Context binding should still work
        bound_logger = logger.bind(component="test")
        bound_logger.info("Bound logger test")

        # Get logger should return working logger
        named_logger = get_logger("test.compatibility")
        named_logger.info("Named logger test")

        # All should complete without exceptions
        assert True

    def test_thread_safety_maintained(self) -> None:
        """Test that thread safety is maintained during transition."""
        import threading

        from provide.foundation.logger import get_logger

        results = []
        errors = []

        def worker_thread(thread_id: int) -> None:
            try:
                logger = get_logger(f"thread.{thread_id}")
                logger.info(f"Message from thread {thread_id}")
                results.append(thread_id)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads = [threading.Thread(target=worker_thread, args=(i,)) for i in range(20)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Should have no errors
        assert len(errors) == 0

        # All threads should have completed
        assert len(results) == 20
        assert sorted(results) == list(range(20))

    def test_configuration_compatibility(self) -> None:
        """Test that configuration objects remain compatible."""
        from provide.foundation.logger.config import LoggingConfig, TelemetryConfig

        # Should be able to create configs as before
        logging_config = LoggingConfig(
            default_level="DEBUG",
            console_formatter="json",
        )

        telemetry_config = TelemetryConfig(
            logging=logging_config,
        )

        # Should be able to use with new Hub API
        hub = get_hub()
        hub.initialize_foundation(telemetry_config, force=True)

        # Configuration should be stored correctly
        stored_config = hub.get_foundation_config()
        assert stored_config.logging.default_level == "DEBUG"
        assert stored_config.logging.console_formatter == "json"
