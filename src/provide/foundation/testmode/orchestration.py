#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# orchestration.py
#
from typing import Any

"""Foundation Test Reset Orchestration.

This module provides the complete reset orchestration for Foundation's
internal state. It knows the proper reset order and handles Foundation-specific
concerns like OpenTelemetry providers and environment variables.

This is Foundation-internal knowledge that should be owned by Foundation,
not by external testing frameworks.
"""

# Global flags to prevent recursive resets
_reset_in_progress = False
_reset_for_testing_in_progress = False


def _reset_otel_once_flag(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def _reset_tracer_provider() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def _reset_meter_provider() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def _reset_opentelemetry_providers() -> None:
    """Reset OpenTelemetry providers to uninitialized state.

    This prevents "Overriding of current TracerProvider/MeterProvider" warnings
    and stream closure issues by properly resetting the global providers.
    """
    _reset_tracer_provider()
    _reset_meter_provider()


def _reset_foundation_environment_variables() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def reset_foundation_state() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_test_mode_cache,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset test mode cache early so subsequent detection is fresh
        reset_test_mode_cache()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def reset_foundation_for_testing() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


# 🧱🏗️🔚
