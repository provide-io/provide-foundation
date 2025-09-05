#
# __init__.py
#
"""
Foundation Telemetry Library (structlog-based).
Primary public interface for the library, re-exporting common components.
"""

# Export config module for easy access
# New foundation components
# Make the errors module available for detailed imports
from provide.foundation import cli, config, errors, platform, process

# Console I/O functions
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import Context
from provide.foundation.core import (
    setup_telemetry,
    shutdown_foundation_telemetry,
)

# Error handling exports - only the essentials
from provide.foundation.errors import (
    # Base exception only
    FoundationError,
    # Most commonly used handlers
    error_boundary,
    retry_on_error,
    # Most commonly used decorators
    with_error_handling,
)

# Hub and Registry exports (public API)
from provide.foundation.hub.components import ComponentCategory, get_component_registry
from provide.foundation.hub.manager import Hub, clear_hub, get_hub
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,  # Factory function for creating loggers
    logger,  # Global logger instance
    setup_logging,  # Setup function
)

# Emoji exports
from provide.foundation.logger.emoji.matrix import (
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    show_emoji_matrix,
)
from provide.foundation.logger.emoji.types import (
    EmojiSet,
    EmojiSetConfig,
    FieldToEmojiMapping,
)

# New type exports for emoji mapping
from provide.foundation.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)

# New utility exports
from provide.foundation.utils import timed_block
from provide.foundation.version import __version__

__all__ = [
    # Core Emoji Dictionaries (available for direct use or reference)
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "ConsoleFormatterStr",
    # New foundation modules
    "Context",
    # Emoji Mapping classes
    "EmojiSet",
    # Error handling essentials
    "FoundationError",
    # Type aliases
    "LogLevelStr",
    "LoggingConfig",
    # Hub and Registry (public API)
    "Registry",
    "RegistryEntry",
    "Hub",
    "ComponentCategory",
    "get_component_registry",
    "get_hub",
    "clear_hub",
    "FieldToEmojiMapping",
    "EmojiSetConfig",
    # Configuration classes
    "TelemetryConfig",
    # Version
    "__version__",
    "cli",
    # Config module
    "config",
    "error_boundary",
    "errors",  # The errors module for detailed imports
    "get_logger",
    # Core setup and logger
    "logger",
    "perr",
    # Console input
    "pin",
    "platform",
    # Console output
    "pout",
    "process",
    "retry_on_error",
    "setup_logging",
    "setup_telemetry",
    # Utilities
    "show_emoji_matrix",
    "shutdown_foundation_telemetry",
    "timed_block",
    "with_error_handling",
]

# 🐍📝
