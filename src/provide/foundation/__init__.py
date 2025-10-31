#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation import config, errors, hub, platform, process, resilience, tracer
from provide.foundation.console import perr, pin, pout
from provide.foundation.context import CLIContext
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
from provide.foundation.hub.manager import (
    Hub,
    clear_hub,
    get_hub,
)
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
    AsyncCircuitBreaker,
    BackoffStrategy,
    CircuitState,
    FallbackChain,
    RetryExecutor,
    RetryPolicy,
    SyncCircuitBreaker,
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

"""A foundational framework for building operationally excellent Python applications.

This is the primary public interface for the framework, re-exporting common
components for application development.
"""


# Lazy loading support for optional modules and __version__
def __getattr__(name: str) -> object:
    """Support lazy loading of modules and __version__.

    This reduces initial import overhead by deferring module imports
    and version loading until first access.

    Args:
        name: Attribute name to lazy-load

    Returns:
        The imported module or attribute

    Raises:
        AttributeError: If attribute doesn't exist
        ImportError: If module import fails
    """
    # Handle __version__ specially to avoid import-time I/O
    if name == "__version__":
        from provide.foundation.utils.versioning import get_version

        return get_version("provide-foundation", caller_file=__file__)

    # For all other attributes, try to import as a submodule
    try:
        from provide.foundation.utils.importer import lazy_import

        return lazy_import(__name__, name)
    except ModuleNotFoundError as e:
        # If the exact module doesn't exist, it's an invalid attribute
        module_name = f"{__name__}.{name}"
        if module_name in str(e):
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
        # Otherwise re-raise (it's a missing dependency)
        raise
    except AttributeError:
        # If it's not a valid submodule, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
    # Other ImportError is allowed to propagate for special error handling (e.g., missing click)


__all__ = [
    # Resilience - Circuit Breaker (async)
    "AsyncCircuitBreaker",
    "BackoffStrategy",
    # New foundation modules
    "CLIContext",
    "CircuitState",
    "ComponentCategory",
    "ConsoleFormatterStr",
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
    # Resilience - Circuit Breaker (sync)
    "SyncCircuitBreaker",
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

# 🧱🏗️🔚
