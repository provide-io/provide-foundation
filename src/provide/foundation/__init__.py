#
# __init__.py
#
"""Foundation Telemetry Library (structlog-based).
Primary public interface for the library, re-exporting common components.
"""

# Export config module for easy access
# New foundation components
# Make the errors module available for detailed imports
from provide.foundation import config, errors, platform, process, resilience, tracer
from provide.foundation._version import __version__

# Console I/O functions (always available - handles click dependency internally)
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import CLIContext, Context

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

# Event set exports
from provide.foundation.eventsets.display import show_event_matrix
from provide.foundation.eventsets.types import (
    EventMapping,
    EventSet,
    FieldMapping,
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
    setup_logging,  # Setup function
)

# Logger type exports
from provide.foundation.logger.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)

# Resilience exports
from provide.foundation.resilience import (
    BackoffStrategy,
    CircuitBreaker,
    CircuitState,
    FallbackChain,
    RetryExecutor,
    RetryPolicy,
    circuit_breaker,
    fallback,
    retry,
)
from provide.foundation.setup import (
    setup_telemetry,
    shutdown_foundation_telemetry,
)

# New utility exports
from provide.foundation.utils import (
    TokenBucketRateLimiter,
    check_optional_deps,
    timed_block,
)


# Lazy loading support for optional modules
def __getattr__(name: str) -> object:
    """Support lazy loading of optional modules."""
    if name == "cli":
        try:
            from provide.foundation import cli

            return cli
        except ImportError as e:
            if "click" in str(e):
                raise ImportError(
                    "CLI features require optional dependencies. Install with: "
                    "pip install 'provide-foundation[cli]'",
                ) from e
            raise
    elif name == "metrics":
        from provide.foundation import metrics

        return metrics
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "BackoffStrategy",
    # New foundation modules
    "CLIContext",
    "CircuitBreaker",
    "CircuitState",
    "ComponentCategory",
    "ConsoleFormatterStr",
    "Context",  # Legacy context support
    # Event set types
    "EventMapping",
    "EventSet",
    "FallbackChain",
    "FieldMapping",
    # Error handling essentials
    "FoundationError",
    "Hub",
    # Type aliases
    "LogLevelStr",
    "LoggingConfig",
    # Hub and Registry (public API)
    "Registry",
    "RegistryEntry",
    "RetryExecutor",
    "RetryPolicy",
    # Configuration classes
    "TelemetryConfig",
    # Rate limiting utilities
    "TokenBucketRateLimiter",
    # Version
    "__version__",
    # Dependency checking utility
    "check_optional_deps",
    "circuit_breaker",
    "clear_hub",
    # Config module
    "config",
    "error_boundary",
    "errors",  # The errors module for detailed imports
    "fallback",
    "get_component_registry",
    "get_hub",
    "get_logger",
    # Core setup and logger
    "logger",
    # Console functions (work with or without click)
    "perr",
    "pin",
    "platform",
    "pout",
    "process",
    "resilience",  # The resilience module for detailed imports
    # Resilience patterns
    "retry",
    # Legacy patterns
    "retry_on_error",
    "setup_logger",  # Consistent naming
    "setup_logging",  # Legacy setup function
    "setup_telemetry",
    # Event enrichment utilities
    "show_event_matrix",
    # Utilities
    "shutdown_foundation_telemetry",
    "timed_block",
    "tracer",  # The tracer module for distributed tracing
    "with_error_handling",
]

# Import the logger instance after all other imports to avoid module shadowing
from provide.foundation.logger import logger

# 🐍📝
