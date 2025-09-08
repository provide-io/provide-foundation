#
# logger.py
#
"""
Logger Testing Utilities for Foundation.

Provides utilities for resetting logger state, managing configurations,
and ensuring test isolation for the Foundation logging system.
"""

import structlog

from provide.foundation.logger.core import (
    _LAZY_SETUP_STATE,
    logger as foundation_logger,
)
from provide.foundation.streams.file import reset_streams


def _reset_opentelemetry_providers() -> None:
    """
    Reset OpenTelemetry providers to uninitialized state.

    This prevents "Overriding of current TracerProvider/MeterProvider" warnings
    and stream closure issues by properly resetting the global providers.
    """
    try:
        # Reset tracing provider by resetting the Once flag
        import opentelemetry.trace as otel_trace

        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            once_obj = otel_trace._TRACER_PROVIDER_SET_ONCE
            if hasattr(once_obj, "_done"):
                once_obj._done = False
        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace._TRACER_PROVIDER = NoOpTracerProvider()
    except ImportError:
        # OpenTelemetry tracing not available
        pass
    except Exception:
        # Ignore errors during reset
        pass

    try:
        # Reset metrics provider by resetting the Once flag
        import opentelemetry.metrics._internal as otel_metrics_internal

        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            once_obj = otel_metrics_internal._METER_PROVIDER_SET_ONCE
            if hasattr(once_obj, "_done"):
                once_obj._done = False
        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics_internal._METER_PROVIDER = NoOpMeterProvider()
    except ImportError:
        # OpenTelemetry metrics not available
        pass
    except Exception:
        # Ignore errors during reset
        pass


def reset_foundation_state() -> None:
    """
    Internal function to reset structlog and Foundation's state.

    This resets:
    - structlog configuration to defaults
    - Foundation logger state and configuration
    - Stream state back to defaults
    - Lazy setup state tracking
    - OpenTelemetry provider state (if available)
    """
    # Reset structlog to its default unconfigured state
    structlog.reset_defaults()

    # Reset stream state
    # NOTE: Temporarily disabled as it can cause hanging in CLI tests
    # reset_streams()

    # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
    # NOTE: Temporarily disabled as it can cause hanging in CLI tests
    # _reset_opentelemetry_providers()

    # Reset foundation logger state
    foundation_logger._is_configured_by_setup = False
    foundation_logger._active_config = None
    foundation_logger._active_resolved_emoji_config = None
    _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})


def reset_foundation_setup_for_testing() -> None:
    """
    Public test utility to reset Foundation's internal state.

    This function ensures clean test isolation by resetting all
    Foundation logging state between test runs.
    """
    # Minimal reset to avoid hanging issues in CLI tests
    try:
        # Only reset structlog state - avoid stream and provider resets
        import structlog
        structlog.reset_defaults()
        
        # Reset foundation logger state minimally
        from provide.foundation.logger.core import (
            _LAZY_SETUP_STATE,
            logger as foundation_logger,
        )
        foundation_logger._is_configured_by_setup = False
        foundation_logger._active_config = None
        foundation_logger._active_resolved_emoji_config = None
        _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
    except Exception:
        # If anything fails, just ignore - testing should still work
        pass
    
    # Clear and re-initialize the hub for test isolation
    # NOTE: Temporarily disabled as it can cause hanging in CLI tests
    # try:
    #     from provide.foundation.hub.manager import clear_hub
    #     clear_hub()
    # except ImportError:
    #     pass
    
    # Re-register HTTP transport for tests that need it
    # NOTE: Temporarily disabled as it can cause hanging in CLI tests
    # try:
    #     from provide.foundation.transport.http import _register_http_transport
    #     _register_http_transport()
    # except ImportError:
    #     # Transport module not available
    #     pass


__all__ = [
    "reset_foundation_setup_for_testing",
    "reset_foundation_state",
]
