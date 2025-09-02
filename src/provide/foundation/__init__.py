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

__all__ = [
    # Core setup and logger
    "logger",
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
]

# 🐍📝
