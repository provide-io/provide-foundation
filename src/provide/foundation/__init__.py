#
# __init__.py
#
"""
Foundation Telemetry Library (structlog-based).
Primary public interface for the library, re-exporting common components.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("provide-foundation")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0-dev"

# Export config module for easy access
from provide.foundation import config
from provide.foundation.core import (
    setup_telemetry,
    shutdown_foundation_telemetry,
)
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    logger,  # Global logger instance
    logger as plog,  # Alias for console logging
    get_logger,  # Factory function for creating loggers
    setup_logging,  # Setup function
)

# New type exports for semantic layering
from provide.foundation.types import (
    ConsoleFormatterStr,
    CustomDasEmojiSet,
    LogLevelStr,
    SemanticFieldDefinition,
    SemanticLayer,
)

# New utility exports
from provide.foundation.utils import timed_block

# Emoji exports
from provide.foundation.logger.emoji_matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    show_emoji_matrix,
)

# New foundation components
from provide.foundation import cli
from provide.foundation.context import Context
from provide.foundation.registry import Registry, RegistryEntry

# Console output functions
from provide.foundation.console import pout, perr

__all__ = [
    # Core setup and logger
    "logger",
    "plog",  # Alias for logger
    "get_logger",
    "setup_logging",
    "setup_telemetry",
    "shutdown_foundation_telemetry",
    # Configuration classes
    "TelemetryConfig",
    "LoggingConfig",
    # Type aliases
    "LogLevelStr",
    "ConsoleFormatterStr",
    # Legacy Emoji Dictionaries (still available for direct use or reference)
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    # Semantic Layering classes
    "CustomDasEmojiSet",
    "SemanticFieldDefinition",
    "SemanticLayer",
    # Utilities
    "show_emoji_matrix",
    "timed_block",
    # Version
    "__version__",
    # Config module
    "config",
    # New foundation modules
    "Context",
    "Registry",
    "RegistryEntry",
    "cli",
    # Console output
    "pout",
    "perr",
]

# 🐍📝
