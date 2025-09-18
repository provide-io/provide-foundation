from __future__ import annotations

from provide.foundation import config, errors, hub, platform, process, resilience, tracer
from provide.foundation._version import __version__
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import CLIContext, Context
from provide.foundation.errors import (
    FoundationError,
    error_boundary,
    resilient,
    retry_on_error,
)
from provide.foundation.eventsets.display import show_event_matrix
from provide.foundation.eventsets.types import (
    EventMapping,
    EventSet,
    FieldMapping,
)
from provide.foundation.hub.components import ComponentCategory, get_component_registry
from provide.foundation.hub.manager import Hub, clear_hub, get_hub
from provide.foundation.hub.registry import Registry, RegistryEntry
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,
    logger,
)
from provide.foundation.logger.types import (
    ConsoleFormatterStr,
    LogLevelStr,
)
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
    shutdown_foundation_telemetry,
)
from provide.foundation.utils import (
    TokenBucketRateLimiter,
    check_optional_deps,
    timed_block,
)

"""Foundation Telemetry Library (structlog-based).
Primary public interface for the library, re-exporting common components.
"""


# Lazy loading support for optional modules
def __getattr__(name: str) -> object:
    """Support lazy loading of optional modules."""
    match name:
        case "cli":
            try:
                import provide.foundation.cli as cli

                return cli
            except ImportError as e:
                if "click" in str(e):
                    raise ImportError(
                        "CLI features require optional dependencies. Install with: "
                        "pip install 'provide-foundation[cli]'",
                    ) from e
                raise
        case "crypto":
            import provide.foundation.crypto as crypto

            return crypto
        case "formatting":
            import provide.foundation.formatting as formatting

            return formatting
        case "metrics":
            import provide.foundation.metrics as metrics

            return metrics
        case _:
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
    # Crypto module (lazy loaded)
    "crypto",
    "error_boundary",
    "errors",  # The errors module for detailed imports
    "fallback",
    # Formatting module (lazy loaded)
    "formatting",
    "get_component_registry",
    "get_hub",
    "get_logger",
    "hub",
    # Core setup and logger
    "logger",
    # Console functions (work with or without click)
    "perr",
    "pin",
    "platform",
    "pout",
    "process",
    "resilience",  # The resilience module for detailed imports
    "resilient",
    # Resilience patterns
    "retry",
    # Legacy patterns
    "retry_on_error",
    # Event enrichment utilities
    "show_event_matrix",
    # Utilities
    "shutdown_foundation_telemetry",
    "timed_block",
    "tracer",  # The tracer module for distributed tracing
]

# Logger instance is imported above with other logger imports

# 🐍📝
