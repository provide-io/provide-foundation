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
from provide.foundation import config, errors, platform, process
from provide.foundation._version import __version__

# Console I/O functions (always available - handles click dependency internally)
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import Context

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
    setup_logger,  # Setup function (consistent naming)
    setup_logging,  # Setup function (backward compatibility)
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
from provide.foundation.setup import (
    setup_telemetry,
    shutdown_foundation_telemetry,
)

# New type exports for emoji mapping
from provide.foundation.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)

# New utility exports
from provide.foundation.utils import (
    TokenBucketRateLimiter,
    check_optional_deps,
    timed_block,
)


# Lazy loading support for optional modules
def __getattr__(name: str):
    """Support lazy loading of optional modules."""
    if name == "cli":
        try:
            import provide.foundation.cli as cli

            return cli
        except ImportError as e:
            if "click" in str(e):
                raise ImportError(
                    "CLI features require optional dependencies. Install with: "
                    "pip install 'provide-foundation[cli]'"
                ) from e
            raise
    elif name == "metrics":
        import provide.foundation.metrics as metrics

        return metrics
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


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
    # Dependency checking utility
    "check_optional_deps",
    # Config module
    "config",
    "error_boundary",
    "errors",  # The errors module for detailed imports
    "get_logger",
    # Core setup and logger
    "logger",
    # Console functions (work with or without click)
    "perr",
    "pin",
    "pout",
    "platform",
    "process",
    "retry_on_error",
    "setup_logging",  # Backward compatibility
    "setup_logger",  # Consistent naming
    "setup_telemetry",
    # Utilities
    "show_emoji_matrix",
    "shutdown_foundation_telemetry",
    "timed_block",
    # Rate limiting utilities
    "TokenBucketRateLimiter",
    "with_error_handling",
]

# Import the logger instance after all other imports to avoid module shadowing
from provide.foundation.logger import logger

# 🐍📝
