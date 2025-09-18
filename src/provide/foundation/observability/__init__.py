from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any

"""Observability module for Foundation.

Provides integration with observability platforms like OpenObserve.
Only available when OpenTelemetry dependencies are installed.
"""

if TYPE_CHECKING:
    pass  # OpenTelemetry imports are handled at runtime

# OpenTelemetry feature detection
_otel_trace_module: Any = None
try:
    from opentelemetry import trace as _otel_trace_module

    _HAS_OTEL = True
except ImportError:
    _otel_trace_module = None
    _HAS_OTEL = False

# Use consistent name throughout
otel_trace = _otel_trace_module

# Only import OpenObserve if OpenTelemetry is available
if _HAS_OTEL:
    try:
        from provide.foundation.integrations.openobserve import (
            OpenObserveClient,
            search_logs,
            stream_logs,
        )

        # Commands will auto-register if click is available
        with suppress(ImportError):
            from provide.foundation.integrations.openobserve.commands import (  # noqa: F401
                openobserve_group,
            )

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
