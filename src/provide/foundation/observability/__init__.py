"""
Observability module for Foundation.

Provides integration with observability platforms like OpenObserve.
Only available when OpenTelemetry dependencies are installed.
"""

# OpenTelemetry feature detection
try:
    from opentelemetry import trace as otel_trace

    _HAS_OTEL = True
except ImportError:
    otel_trace = None
    _HAS_OTEL = False

# Only import OpenObserve if OpenTelemetry is available
if _HAS_OTEL:
    try:
        from provide.foundation.integrations.openobserve import (
            OpenObserveClient,
            search_logs,
            stream_logs,
        )

        # Commands will auto-register if click is available
        try:
            from provide.foundation.integrations.openobserve.commands import (
                openobserve_group,
            )
        except ImportError:
            # Click not available, skip command registration
            pass

        __all__ = [
            "OpenObserveClient",
            "search_logs",
            "stream_logs",
        ]
    except ImportError:
        # OpenObserve module not fully available
        __all__ = []
else:
    __all__ = []


def is_openobserve_available() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available
    """
    return _HAS_OTEL and "OpenObserveClient" in globals()
