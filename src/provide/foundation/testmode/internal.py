#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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

# Global flags to prevent recursive resets in individual functions
_eventsets_reset_in_progress = False
_hub_reset_in_progress = False


def reset_event_loops() -> None:
    """Close any running event loops to prevent worker shutdown hangs.

    This is critical for pytest-xdist workers to shut down cleanly after
    async tests complete.

    IMPORTANT: This MUST be called AFTER reset_time_machine_state() to ensure
    time patches are stopped before creating a new event loop. Otherwise the
    new loop may cache frozen time.monotonic references.
    """
    try:
        import asyncio

        # Close the current event loop if it's not running
        try:
            loop = asyncio.get_event_loop()
            # Don't close if it's running (we're inside an async context)
            if not loop.is_running() and not loop.is_closed():
                loop.close()
        except RuntimeError:
            # No event loop in this thread, that's fine
            pass

        # DON'T create a new event loop - let pytest-asyncio manage it
        # If we create one here while time patches are still active (fixture cleanup
        # hasn't run yet), the new loop will cache frozen time.monotonic references
    except Exception:
        # If anything fails, continue - better to leak a loop than crash
        pass


def reset_time_machine_state() -> None:
    """Reset time_machine state to ensure time is not frozen.

    NOTE: The actual cleanup is now handled by the _force_time_machine_cleanup
    fixture in tests/conftest.py, which runs BEFORE Foundation teardown.

    This ensures time patches are stopped before pytest-asyncio creates event loops
    for the next test. This function remains as a no-op safety fallback.
    """
    # Cleanup is now handled by conftest fixture which runs earlier
    pass


def reset_test_mode_cache() -> None:
    """Reset test mode detection cache.

    This clears the cached test mode detection result, allowing fresh
    detection on the next call. This is important for test isolation
    when tests manipulate environment variables or sys.modules.
    """
    from provide.foundation.testmode.detection import _clear_test_mode_cache

    _clear_test_mode_cache()


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
    global _hub_reset_in_progress

    # Prevent recursive resets that can trigger re-initialization
    if _hub_reset_in_progress:
        return

    _hub_reset_in_progress = True
    try:
        try:
            from provide.foundation.hub.manager import clear_hub

            clear_hub()
        except ImportError:
            # Hub module not available, skip
            pass

        try:
            # Also reset the initialized components cache
            from provide.foundation.hub.components import _initialized_components

            _initialized_components.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global component registry (where bootstrap_foundation registers components)
            from provide.foundation.hub.components import _component_registry

            _component_registry.clear()
        except ImportError:
            # Components module not available, skip
            pass

        try:
            # Clear the global command registry (where @register_command decorator registers commands)
            from provide.foundation.hub.registry import _command_registry

            _command_registry.clear()
        except ImportError:
            # Registry module not available, skip
            pass
    finally:
        _hub_reset_in_progress = False

    # NOTE: Event bus clearing removed - it was causing infinite recursion
    # during Foundation reinitialization. Event handlers use weak references
    # and will be garbage collected naturally. The event bus has built-in
    # "already registered" checks to prevent duplicate registrations.


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


def reset_transport_registration_flags() -> None:
    """Reset transport auto-registration flags.

    This resets the module-level flags that prevent duplicate transport
    registration, allowing transports to be re-registered after the
    registry is cleared during test cleanup.
    """
    try:
        import sys

        # Reset HTTP transport registration flag if module is loaded
        if "provide.foundation.transport.http" in sys.modules:
            http_module = sys.modules["provide.foundation.transport.http"]
            if hasattr(http_module, "_http_transport_registered"):
                http_module._http_transport_registered = False  # type: ignore[attr-defined]
    except Exception:
        # If reset fails, skip - the guard will be bypassed on next import
        pass


def reset_eventsets_state() -> None:
    """Reset event set registry and discovery state.

    This clears the event set registry to ensure clean state
    between tests.
    """
    global _eventsets_reset_in_progress

    # Prevent recursive resets that trigger event processor initialization
    if _eventsets_reset_in_progress:
        return

    _eventsets_reset_in_progress = True
    try:
        from provide.foundation.eventsets.registry import clear_registry

        clear_registry()
    except ImportError:
        # Event sets may not be available in all test environments
        pass
    finally:
        _eventsets_reset_in_progress = False


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


def _reset_direct_circuit_breaker_instances() -> None:
    """Reset ONLY CircuitBreaker instances created directly (not via decorator) in tests.

    This function uses introspection to find CircuitBreaker instances
    that exist in memory but are NOT tracked by the decorator registries.
    This ensures we only reset orphaned instances created directly, while
    preserving the state of decorator-created instances within a test.
    """
    import gc

    try:
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
        from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker

        registry = get_hub()._component_registry

        # Get all decorator-tracked instances from registry
        decorator_tracked_ids = set()
        for dimension in ["circuit_breaker", "circuit_breaker_test"]:
            for name in registry.list_dimension(dimension):
                breaker = registry.get(name, dimension=dimension)
                if breaker:
                    decorator_tracked_ids.add(id(breaker))

        # Find all CircuitBreaker instances in memory using garbage collector
        # Only reset those NOT tracked by decorators (i.e., created directly)
        instances_found = 0
        for obj in gc.get_objects():
            if (
                isinstance(obj, (SyncCircuitBreaker, AsyncCircuitBreaker))
                and id(obj) not in decorator_tracked_ids
            ):
                try:
                    # Only reset instances that are still alive and not tracked by decorators
                    if obj is not None:
                        # Reset each circuit breaker instance to clean state
                        obj.reset()
                        instances_found += 1
                except Exception:
                    # Skip instances that can't be reset (might be in an inconsistent state)
                    pass

        # Force garbage collection to clean up any dead references
        if instances_found > 0:
            gc.collect()

    except ImportError:
        # Circuit breaker module not available, skip
        pass


def reset_circuit_breaker_state() -> None:
    """Reset all circuit breaker instances to ensure test isolation.

    This function resets all circuit breaker instances that were created
    by the @circuit_breaker decorator and direct instantiation to ensure
    their state doesn't leak between tests.
    """
    # Reset all CircuitBreaker instances created directly (not via decorator)
    # Do this FIRST to catch all instances before decorator reset
    _reset_direct_circuit_breaker_instances()

    try:
        import asyncio

        from provide.foundation.resilience.decorators import (
            reset_circuit_breakers_for_testing,
            reset_test_circuit_breakers,
        )

        # Reset both production and test circuit breakers
        # These are now async functions, so we need to run them in an event loop

        # Check if we're in an async context (running event loop)
        try:
            asyncio.get_running_loop()
            # We're in an async context - skip reset to avoid blocking
            # This shouldn't happen in practice since reset is called from sync fixtures
            return
        except RuntimeError:
            # No running loop - we're in sync context, safe to proceed
            pass

        # Use asyncio.run() to create fresh event loop for each call
        # This is more reliable than trying to reuse get_event_loop()
        asyncio.run(reset_circuit_breakers_for_testing())
        asyncio.run(reset_test_circuit_breakers())
    except ImportError:
        # Resilience decorators module not available, skip
        pass


def reset_state_managers() -> None:
    """Reset all state managers to default state.

    This resets logger state managers and other state management
    components to ensure clean test isolation.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset logger state manager if available
        try:
            logger_state_manager = hub.get_component("logger_state_manager")
            if logger_state_manager and hasattr(logger_state_manager, "reset_to_default"):
                logger_state_manager.reset_to_default()
        except Exception:
            # Logger state manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def reset_configuration_state() -> None:
    """Reset configuration state to defaults.

    This resets all versioned configurations and their managers
    to ensure clean state between tests.
    """
    try:
        from provide.foundation.hub.manager import get_hub

        hub = get_hub()

        # Reset config manager if available
        try:
            config_manager = hub.get_component("config_manager")
            if config_manager and hasattr(config_manager, "clear_all"):
                config_manager.clear_all()
        except Exception:
            # Config manager not available or reset failed, skip
            pass

    except ImportError:
        # Hub not available, skip
        pass


def reset_version_cache() -> None:
    """Reset version cache to defaults.

    This clears the cached version to ensure clean state
    between tests, allowing each test to verify different
    version resolution scenarios.
    """
    try:
        from provide.foundation._version import (  # type: ignore[import-untyped]
            reset_version_cache as _reset_cache,
        )

        _reset_cache()
    except ImportError:
        # Version module not available, skip
        pass


# 🧱🏗️🔚
