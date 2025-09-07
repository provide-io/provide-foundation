#
# __init__.py
#
"""
Foundation Setup Module.

This module provides the main setup API for Foundation,
orchestrating logging, tracing, and other subsystems.
"""

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.logger.setup import internal_setup
from provide.foundation.logger.setup.coordinator import _PROVIDE_SETUP_LOCK
from provide.foundation.logger.setup.testing import reset_foundation_setup_for_testing
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


def setup_foundation(config: TelemetryConfig | None = None) -> None:
    """
    Initialize the Foundation system with all its subsystems.

    This orchestrates:
    - Logging system setup
    - Stream configuration
    - Future: Tracer initialization

    Args:
        config: Optional configuration to use. If None, loads from environment.
    """
    global _EXPLICIT_SETUP_DONE

    with _PROVIDE_SETUP_LOCK:
        current_config = config if config is not None else TelemetryConfig.from_env()

        # Configure file logging if specified
        log_file_path = getattr(current_config.logging, "log_file", None)
        configure_file_logging(log_file_path)

        # Run the main logging setup
        internal_setup(current_config, is_explicit_call=True)

        # Initialize OpenTelemetry tracing and metrics if available and enabled
        setup_opentelemetry_tracing(current_config)
        setup_opentelemetry_metrics(current_config)

        _EXPLICIT_SETUP_DONE = True


def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Legacy alias for setup_foundation.

    Args:
        config: Optional configuration to use. If None, loads from environment.
    """
    setup_foundation(config)


async def shutdown_foundation(timeout_millis: int = 5000) -> None:
    """
    Gracefully shutdown all Foundation subsystems.

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
    """
    Legacy alias for shutdown_foundation.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)
    """
    await shutdown_foundation(timeout_millis)


__all__ = [
    "reset_foundation_setup_for_testing",
    "setup_foundation",
    "setup_telemetry",  # Legacy alias
    "shutdown_foundation",
    "shutdown_foundation_telemetry",  # Legacy alias
]
