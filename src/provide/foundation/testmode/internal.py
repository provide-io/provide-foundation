from __future__ import annotations

#
# internal.py
#
import structlog

"""Internal Reset APIs for Foundation Testing.

This module provides low-level reset functions that testing frameworks
can use to reset Foundation's internal state. These are internal APIs
designed to be called by testkit for proper test isolation.
"""


def reset_structlog_state() -> None:
    """Reset structlog configuration to defaults.

    This is the most fundamental reset - it clears all structlog
    configuration and returns it to an unconfigured state.
    """
    structlog.reset_defaults()


def reset_logger_state() -> None:
    """Reset Foundation logger state to defaults.

    This resets the lazy setup state and logger configuration flags
    without importing the full logger module to avoid circular dependencies.
    """
    try:
        from provide.foundation.logger.core import _LAZY_SETUP_STATE

        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except ImportError:
        # Logger state not available, skip
        pass

    try:
        from provide.foundation.logger.core import logger as foundation_logger

        # Reset foundation logger state by bypassing the proxy to avoid circular initialization
        # Access the proxy's __dict__ directly to avoid triggering __setattr__
        foundation_logger.__dict__["_is_configured_by_setup"] = False
        foundation_logger.__dict__["_active_config"] = None
        foundation_logger.__dict__["_active_resolved_emoji_config"] = None
    except (ImportError, AttributeError, TypeError):
        # Skip if foundation_logger is a proxy without direct attribute access
        pass


def reset_hub_state() -> None:
    """Reset Hub state to defaults.

    This clears the Hub registry and resets all Hub components
    to their initial state.
    """
    try:
        from provide.foundation.hub.manager import clear_hub

        clear_hub()
    except ImportError:
        # Hub module not available, skip
        pass


def reset_streams_state() -> None:
    """Reset stream state to defaults.

    This resets file streams and other stream-related state
    managed by the streams module.
    """
    try:
        from provide.foundation.streams.file import reset_streams

        reset_streams()
    except ImportError:
        # Streams module not available, skip
        pass


def reset_eventsets_state() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass


def reset_coordinator_state() -> None:
    """Reset setup coordinator state.

    This clears cached coordinator state including setup logger
    cache and other coordinator-managed state.
    """
    try:
        from provide.foundation.logger.setup.coordinator import reset_coordinator_state

        reset_coordinator_state()
    except ImportError:
        # Coordinator module not available, skip
        pass

    try:
        from provide.foundation.logger.setup.coordinator import reset_setup_logger_cache

        reset_setup_logger_cache()
    except ImportError:
        # Setup logger cache not available, skip
        pass


def reset_profiling_state() -> None:
    """Reset profiling state to defaults.

    This clears profiling metrics and resets profiling components
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        profiler = hub.get_component("profiler")
        if profiler:
            profiler.reset()
    except ImportError:
        # Profiling module or Hub not available, skip
        pass


def reset_global_coordinator() -> None:
    """Reset the global initialization coordinator state for testing.

    This function resets the singleton InitializationCoordinator state
    to ensure proper test isolation between test runs.

    WARNING: This should only be called from test code or test fixtures.
    Production code should not reset the global coordinator state.
    """
    try:
        from provide.foundation.hub.initialization import _coordinator

        _coordinator.reset_state()
    except ImportError:
        # Initialization module not available, skip
        pass


def reset_circuit_breaker_state() -> None:
    """Reset all circuit breaker instances to ensure test isolation.

    This function resets all circuit breaker instances that were created
    by the @circuit_breaker decorator to ensure their state doesn't leak
    between tests.
    """
    try:
        from provide.foundation.resilience.decorators import (
            reset_circuit_breakers_for_testing,
            reset_test_circuit_breakers,
        )

        # Reset both production and test circuit breakers
        reset_circuit_breakers_for_testing()
        reset_test_circuit_breakers()
    except ImportError:
        # Resilience module not available, skip
        pass
