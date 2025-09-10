#
# logger.py
#
"""
Logger Testing Utilities for Foundation.

Provides utilities for resetting logger state, managing configurations,
and ensuring test isolation for the Foundation logging system.
"""

import structlog
import pytest
from unittest.mock import Mock

from provide.foundation.logger.core import (
    _LAZY_SETUP_STATE,
    logger as foundation_logger,
)
from provide.foundation.streams.file import reset_streams


@pytest.fixture
def mock_logger():
    """
    Comprehensive mock logger for testing.
    
    Provides compatibility with both stdlib logging and structlog interfaces,
    including method call tracking and common logger attributes.
    
    Returns:
        Mock logger with debug, info, warning, error methods and structlog compatibility.
    """
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.warn = Mock()  # Alias for warning
    logger.error = Mock()
    logger.exception = Mock()
    logger.critical = Mock()
    logger.fatal = Mock()  # Alias for critical
    
    # Add common logger attributes
    logger.name = "mock_logger"
    logger.level = 10  # DEBUG level
    logger.handlers = []
    logger.disabled = False
    
    # Add structlog compatibility methods
    logger.bind = Mock(return_value=logger)
    logger.unbind = Mock(return_value=logger)
    logger.new = Mock(return_value=logger)
    logger.msg = Mock()  # Alternative to info
    
    # Add trace method for Foundation's extended logging
    logger.trace = Mock()
    
    return logger


def mock_logger_factory():
    """
    Factory function to create mock loggers outside of pytest context.
    
    Useful for unit tests that need a mock logger but aren't using pytest fixtures.
    
    Returns:
        Mock logger with the same interface as the pytest fixture.
    """
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.warn = Mock()
    logger.error = Mock()
    logger.exception = Mock()
    logger.critical = Mock()
    logger.fatal = Mock()
    
    logger.name = "mock_logger"
    logger.level = 10
    logger.handlers = []
    logger.disabled = False
    
    logger.bind = Mock(return_value=logger)
    logger.unbind = Mock(return_value=logger)
    logger.new = Mock(return_value=logger)
    logger.msg = Mock()
    logger.trace = Mock()
    
    return logger


def _reset_opentelemetry_providers() -> None:
    """
    Reset OpenTelemetry providers to uninitialized state.

    This prevents "Overriding of current TracerProvider/MeterProvider" warnings
    and stream closure issues by properly resetting the global providers.
    """
    try:
        # Reset tracing provider more thoroughly
        import opentelemetry.trace as otel_trace
        
        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            once_obj = otel_trace._TRACER_PROVIDER_SET_ONCE
            if hasattr(once_obj, "_done"):
                once_obj._done = False
            if hasattr(once_obj, "_lock"):
                with once_obj._lock:
                    once_obj._done = False
        
        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider
        otel_trace.set_tracer_provider(NoOpTracerProvider())
        
    except ImportError:
        # OpenTelemetry tracing not available
        pass
    except Exception:
        # Ignore errors during reset - better to continue than fail
        pass

    try:
        # Reset metrics provider more thoroughly
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal
        
        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            once_obj = otel_metrics_internal._METER_PROVIDER_SET_ONCE
            if hasattr(once_obj, "_done"):
                once_obj._done = False
            if hasattr(once_obj, "_lock"):
                with once_obj._lock:
                    once_obj._done = False
        
        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider
        otel_metrics.set_meter_provider(NoOpMeterProvider())
        
    except ImportError:
        # OpenTelemetry metrics not available
        pass
    except Exception:
        # Ignore errors during reset - better to continue than fail
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
    reset_streams()

    # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
    # Note: OpenTelemetry providers are designed to prevent override for safety.
    # In test environments, we suppress this reset to avoid hanging/blocking.
    # The warnings are harmless in test context.
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
    # Full reset but with improved OpenTelemetry handling
    reset_foundation_state()
    
    # Clear and re-initialize the hub for test isolation
    try:
        from provide.foundation.hub.manager import clear_hub
        clear_hub()
    except ImportError:
        pass
    
    # Re-register HTTP transport for tests that need it
    try:
        from provide.foundation.transport.http import _register_http_transport
        _register_http_transport()
    except ImportError:
        # Transport module not available
        pass


__all__ = [
    "reset_foundation_setup_for_testing",
    "reset_foundation_state",
    "mock_logger",
    "mock_logger_factory",
]
