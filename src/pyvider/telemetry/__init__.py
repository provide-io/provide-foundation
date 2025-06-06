#
# __init__.py
#
"""
Pyvider Telemetry Library (structlog-based).

This top-level `pyvider.telemetry` package module serves as the primary public interface
for the library. It conveniently re-exports the most commonly used components,
allowing users to import them directly from `pyvider.telemetry` without needing
to delve into the submodule structure.

Key Exports:
- `logger`: The pre-configured global logger instance for immediate use.
- `setup_telemetry`: Function to explicitly initialize or reconfigure telemetry settings.
- `shutdown_pyvider_telemetry`: Async function to perform graceful shutdown procedures.
- `TelemetryConfig`, `LoggingConfig`: Configuration objects for telemetry and logging behavior.
- `LogLevelStr`: Type alias for valid log level strings.
- `PRIMARY_EMOJI`, `SECONDARY_EMOJI`, `TERTIARY_EMOJI`: Dictionaries defining the
  Domain-Action-Status (DAS) emoji mappings.
- `__version__`: The package version string.

Usage Example:
    ```python
    from pyvider.telemetry import logger, setup_telemetry, TelemetryConfig

    # Optionally configure telemetry (or rely on defaults/environment variables)
    # config = TelemetryConfig(service_name="my-app")
    # setup_telemetry(config)

    logger.info("Application started", domain="app", action="start", status="success")
    ```

This module aims to simplify the integration of Pyvider Telemetry into other applications
by providing a flat and accessible API for essential functionalities.
"""

from importlib.metadata import PackageNotFoundError, version

# Dynamic version loading from package metadata
try:
    __version__ = version("pyvider-telemetry")
except PackageNotFoundError:  # pragma: no cover
    # Fallback for development/editable installs
    __version__ = "0.0.0-dev"

from pyvider.telemetry.config import (
    LoggingConfig,
    LogLevelStr,
    TelemetryConfig,
)
from pyvider.telemetry.core import (
    setup_telemetry,
    shutdown_pyvider_telemetry,
)
from pyvider.telemetry.logger import logger
from pyvider.telemetry.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
)

__all__ = [
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "LogLevelStr",
    "LoggingConfig",
    "TelemetryConfig",
    "__version__",
    "logger",
    "setup_telemetry",
    "shutdown_pyvider_telemetry",
]

# 🐍📝
