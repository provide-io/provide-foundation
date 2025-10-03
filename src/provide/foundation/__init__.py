from __future__ import annotations

import sys
import threading

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
# Use thread-local storage for recursion guard to ensure thread safety
_thread_local = threading.local()

# Maximum depth for nested lazy imports to prevent stack overflow
_MAX_LAZY_IMPORT_DEPTH = 5

# Modules that are safe to lazy-load (do not trigger recursive lookups)
# These modules have been verified to not cause import cycles
_LAZY_LOADABLE_MODULES = frozenset(["cli", "crypto", "docs", "formatting", "metrics"])


def __getattr__(name: str) -> object:  # noqa: C901
    """Support lazy loading of optional modules.

    This lazy loading mechanism reduces initial import overhead by deferring
    module imports until first access. However, it can be fragile if modules
    have complex interdependencies.

    Safe lazy-loaded modules (verified no import cycles):
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection

    Args:
        name: Module name to lazy-load

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).
    """
    # Build the full module name
    module_name = f"provide.foundation.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= _MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({_MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{__name__}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Verify module is in the allowed lazy-load list
    if name not in _LAZY_LOADABLE_MODULES:
        available = ", ".join(sorted(_LAZY_LOADABLE_MODULES))
        raise AttributeError(
            f"module '{__name__}' has no attribute '{name}'. "
            f"Only these modules support lazy loading: {available}"
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        if name == "cli":
            try:
                mod = __import__(module_name, fromlist=[""])
                sys.modules[module_name] = mod
                return mod
            except ImportError as e:
                if "click" in str(e):
                    raise ImportError(
                        "CLI features require optional dependencies. Install with: "
                        "pip install 'provide-foundation[cli]'",
                    ) from e
                raise
        else:
            # Standard import for other allowed modules
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


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
