from __future__ import annotations

#
# __init__.py
#
from provide.foundation.logger.setup import internal_setup
from provide.foundation.logger.setup.coordinator import _PROVIDE_SETUP_LOCK
from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics
from provide.foundation.streams.file import flush_log_streams
from provide.foundation.tracer.otel import shutdown_opentelemetry

"""Foundation Setup Module.

This module provides the main setup API for Foundation,
orchestrating logging, tracing, and other subsystems.
"""

_EXPLICIT_SETUP_DONE = False


async def shutdown_foundation(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with _PROVIDE_SETUP_LOCK:
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


async def shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None:
    """Legacy alias for shutdown_foundation.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    await shutdown_foundation(timeout_millis)


__all__ = [
    "internal_setup",
    "shutdown_foundation",
    "shutdown_foundation_telemetry",  # Legacy alias
]
