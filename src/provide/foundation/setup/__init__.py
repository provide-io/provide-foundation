#
# __init__.py
#
"""
Foundation Telemetry Setup Module.

This module provides the main setup API for Foundation Telemetry,
centralizing all setup-related functionality in focused sub-modules.
"""

from provide.foundation.logger.config import TelemetryConfig
from provide.foundation.setup.coordinator import internal_setup, _PROVIDE_SETUP_LOCK
from provide.foundation.setup.streams import configure_file_logging, flush_log_streams
from provide.foundation.setup.testing import reset_foundation_setup_for_testing

_EXPLICIT_SETUP_DONE = False


def setup_telemetry(config: TelemetryConfig | None = None) -> None:
    """
    Initializes or reconfigures the Foundation Telemetry system.
    
    Args:
        config: Optional configuration to use. If None, loads from environment.
    """
    global _EXPLICIT_SETUP_DONE
    
    with _PROVIDE_SETUP_LOCK:
        current_config = config if config is not None else TelemetryConfig.from_env()
        
        # Configure file logging if specified
        log_file_path = getattr(current_config.logging, "log_file", None)
        configure_file_logging(log_file_path)
        
        # Run the main setup
        internal_setup(current_config, is_explicit_call=True)
        _EXPLICIT_SETUP_DONE = True


async def shutdown_foundation_telemetry(timeout_millis: int = 5000) -> None:
    """
    Gracefully flushes any buffered telemetry, especially for file logging.
    This does NOT perform a full reset, allowing test runners to clean up streams.
    
    Args:
        timeout_millis: Timeout for shutdown (currently unused)
    """
    with _PROVIDE_SETUP_LOCK:
        flush_log_streams()


__all__ = [
    "setup_telemetry",
    "shutdown_foundation_telemetry", 
    "reset_foundation_setup_for_testing",
]