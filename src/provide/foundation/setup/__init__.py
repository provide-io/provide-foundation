#
# __init__.py
#
"""Foundation Setup Module.

This module provides the main setup API for Foundation,
orchestrating logging, tracing, and other subsystems.
"""

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.setup import internal_setup
from provide.foundation.logger.setup.coordinator import _PROVIDE_SETUP_LOCK

# Import reset function from testkit (will be called by testkit internally)
# from provide.testkit.logger import reset_foundation_setup_for_testing
from provide.foundation.metrics.otel import (
    setup_opentelemetry_metrics,
    shutdown_opentelemetry_metrics,
)
from provide.foundation.streams.file import configure_file_logging, flush_log_streams
from provide.foundation.tracer.otel import (
    setup_opentelemetry_tracing,
    shutdown_opentelemetry,
)

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
