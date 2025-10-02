from __future__ import annotations

from provide.foundation import config, errors, hub, platform, process, resilience, tracer
from provide.foundation._version import __version__
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import CLIContext, Context
from provide.foundation.errors import (
    FoundationError,
    error_boundary,
    resilient,
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
from provide.foundation.setup import shutdown_foundation
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
    import sys

    # Build the full module name
    module_name = f"provide.foundation.{name}"

    # Check if we've already entered recursion for this module
    # This prevents infinite recursion when a module has been corrupted
    recursion_key = f"_getattr_recursion_{name}"
    if recursion_key in globals():
        raise AttributeError(
            f"module '{__name__}' has no attribute '{name}' "
            f"(recursion detected, module may be corrupted in sys.modules)"
        )

    # Set recursion guard
    globals()[recursion_key] = True

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

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
            case "docs":
                import provide.foundation.docs as docs

                return docs
            case "formatting":
                import provide.foundation.formatting as formatting

                return formatting
            case "metrics":
                import provide.foundation.metrics as metrics

                return metrics
            case _:
                raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
    finally:
        # Always clear recursion guard
        globals().pop(recursion_key, None)


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
    # Docs module (lazy loaded)
    "docs",
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
    # Event enrichment utilities
    "show_event_matrix",
    # Utilities
    "shutdown_foundation",
    "timed_block",
    "tracer",  # The tracer module for distributed tracing
]

# Logger instance is imported above with other logger imports

# 🐍📝
