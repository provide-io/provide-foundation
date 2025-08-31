#
# provide/foundation/__init__.py
#
"""
Provide Foundation - Core infrastructure for the provide.io ecosystem.

This package provides foundational components including telemetry, exceptions,
cryptography, hub, and configuration management.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("provide-foundation")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0-dev"

# Re-export telemetry components at foundation level
from provide.foundation.telemetry import (
    # Core setup and logger
    logger,
    setup_telemetry,
    shutdown_foundation_telemetry,
    # Configuration classes
    TelemetryConfig,
    LoggingConfig,
    # Type aliases
    LogLevelStr,
    ConsoleFormatterStr,
    # Emoji matrices
    PRIMARY_EMOJI,
    SECONDARY_EMOJI,
    TERTIARY_EMOJI,
    # Semantic Layering classes
    CustomDasEmojiSet,
    SemanticFieldDefinition,
    SemanticLayer,
    # Utilities
    show_emoji_matrix,
    timed_block,
)

# Make config, core, types, utils accessible at foundation level
# This allows both provide.foundation.telemetry.X and provide.foundation.X imports
from provide.foundation.telemetry import config
from provide.foundation.telemetry import core
from provide.foundation.telemetry import types
from provide.foundation.telemetry import utils

__all__ = [
    # Core components
    "logger",
    "setup_telemetry",
    "shutdown_foundation_telemetry",
    # Configuration
    "TelemetryConfig",
    "LoggingConfig",
    # Types
    "LogLevelStr",
    "ConsoleFormatterStr",
    # Emoji support
    "PRIMARY_EMOJI",
    "SECONDARY_EMOJI",
    "TERTIARY_EMOJI",
    "show_emoji_matrix",
    # Semantic layers
    "CustomDasEmojiSet",
    "SemanticFieldDefinition",
    "SemanticLayer",
    # Utilities
    "timed_block",
    # Modules
    "config",
    "core",
    "types",
    "utils",
    # Version
    "__version__",
]