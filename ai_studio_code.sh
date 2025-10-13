#!/bin/bash
# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_update() { echo -e "🔄 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying non-breaking enhancements to provide.foundation..."

log_update "Updating: provide/foundation/__init__.py"
mkdir -p provide/foundation/
cat <<'EOF' > provide/foundation/__init__.py
from __future__ import annotations

import os
from typing import TYPE_CHECKING

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


# --- Eager Loading and Static Analysis Support ---

_EAGER_LOAD = os.environ.get("FOUNDATION_EAGER_LOAD", "false").lower() in ("true", "1", "yes")

# This block is ONLY for static analysis tools and IDEs. It is never executed at runtime
# unless FOUNDATION_EAGER_LOAD is enabled.
if TYPE_CHECKING or _EAGER_LOAD:
    from . import (
        archive,
        cli,
        concurrency,
        crypto,
        docs,
        env,
        file,
        formatting,
        integrations,
        metrics,
        observability,
        parsers,
        profiling,
        security,
        serialization,
        state,
        streams,
        testmode,
        time,
        transport,
    )
    from ._version import __version__


# Lazy loading support for optional modules and __version__
if not _EAGER_LOAD:

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
            from provide.foundation._version import __version__

            return __version__

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

# 🐍📝
EOF

log_update "Updating: provide/foundation/hub/core.py"
mkdir -p provide/foundation/hub/
cat <<'EOF' > provide/foundation/hub/core.py
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    import click

from provide.foundation.context import CLIContext
from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.decorators import resilient
from provide.foundation.errors.resources import AlreadyExistsError
from provide.foundation.hub.categories import ComponentCategory
from provide.foundation.hub.commands import CommandInfo
from provide.foundation.hub.components import ComponentInfo
from provide.foundation.hub.registry import Registry, get_command_registry

"""Core Hub class for component and command management.

This module provides the core Hub functionality for registering and
managing components and commands, without Foundation-specific features.
"""

# Lazy import to avoid circular dependency
_click_module: Any = None
_HAS_CLICK: bool | None = None

T = TypeVar("T")


def _get_click() -> tuple[Any, bool]:
    """Get click module and availability flag."""
    global _click_module, _HAS_CLICK
    if _HAS_CLICK is None:
        from provide.foundation.cli.deps import _HAS_CLICK as has_click, click

        _click_module = click
        _HAS_CLICK = has_click
    return _click_module, _HAS_CLICK


class CoreHub:
    """Core hub for managing components and commands.

    The CoreHub provides basic functionality for:
    - Registering components and commands
    - Managing component lifecycle
    - Creating Click CLI applications

    Does not include Foundation-specific initialization.
    """

    def __init__(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
    ) -> None:
        """Initialize the core hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
        """
        self.context = context or CLIContext()
        self._component_registry = component_registry or Registry()
        self._command_registry = command_registry or get_command_registry()
        self._cli_group: click.Group | None = None

    # Component Management

    @resilient(
        context_provider=lambda: {"hub": "add_component"},
        error_mapper=lambda e: ValidationError(
            f"Failed to add component: {e}",
            code="HUB_COMPONENT_ADD_ERROR",
            cause=e,
        )
        if not isinstance(e, AlreadyExistsError | ValidationError)
        else e,
    )
    def add_component(
        self,
        component_class: type[Any],
        name: str | None = None,
        dimension: str = ComponentCategory.COMPONENT.value,
        **metadata: Any,
    ) -> ComponentInfo:
        """Add a component to the hub.

        Args:
            component_class: Component class to register
            name: Optional name (defaults to class name)
            dimension: Registry dimension
            **metadata: Additional metadata

        Returns:
            ComponentInfo for the registered component

        Raises:
            AlreadyExistsError: If component is already registered
            ValidationError: If component class is invalid

        """
        if not isinstance(component_class, type):
            raise ValidationError(
                f"Component must be a class, got {type(component_class).__name__}",
                code="HUB_INVALID_COMPONENT",
                component_type=type(component_class).__name__,
            )

        component_name = name or component_class.__name__

        # Check if already exists
        if self._component_registry.get_entry(component_name, dimension=dimension):
            raise AlreadyExistsError(
                f"Component '{component_name}' already registered in dimension '{dimension}'",
                code="HUB_COMPONENT_EXISTS",
                component_name=component_name,
                dimension=dimension,
            )

        info = ComponentInfo(
            name=component_name,
            component_class=component_class,
            dimension=dimension,
            version=metadata.get("version"),
            description=metadata.get("description", component_class.__doc__),
            author=metadata.get("author"),
            tags=metadata.get("tags", []),
            metadata=metadata,
        )

        self._component_registry.register(
            name=component_name,
            value=component_class,
            dimension=dimension,
            metadata={"info": info, **metadata},
            replace=False,  # Don't allow replacement by default
        )

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added component to hub",
            name=component_name,
            dimension=dimension,
        )

        return info

    def get_component(
        self,
        name: str,
        dimension: str | None = None,
    ) -> type[Any] | None:
        """Get a component by name.

        Args:
            name: Component name
            dimension: Optional dimension filter

        Returns:
            Component class or None

        """
        return self._component_registry.get(name, dimension)

    def list_components(
        self,
        dimension: str | None = None,
    ) -> list[str]:
        """List component names.

        Args:
            dimension: Optional dimension filter

        Returns:
            List of component names

        """
        if dimension:
            return self._component_registry.list_dimension(dimension)

        # List all non-command dimensions
        all_items = self._component_registry.list_all()
        components = []
        for dim, names in all_items.items():
            if dim != ComponentCategory.COMMAND.value:
                components.extend(names)
        return components

    def discover_components(
        self,
        group: str,
        dimension: str = ComponentCategory.COMPONENT.value,
    ) -> dict[str, type[Any]]:
        """Discover and register components from entry points.

        Args:
            group: Entry point group name
            dimension: Dimension to register under

        Returns:
            Dictionary of discovered components

        """
        from provide.foundation.hub.components import discover_components as _discover_components

        return _discover_components(group, dimension, self._component_registry)

    def resolve(self, component_class: type[T]) -> T:
        """Resolve a component and its dependencies from the registry.

        This method uses introspection to automatically inject dependencies
        from the registry into a class's __init__ method, providing a
        Dependency Injection (DI) pattern as an alternative to the
        Service Locator pattern.

        Args:
            component_class: The class to instantiate and resolve.

        Returns:
            An instance of the component_class with dependencies injected.
        """
        import inspect

        if not inspect.isclass(component_class):
            raise TypeError("resolve() can only be used with classes.")

        sig = inspect.signature(component_class.__init__)
        dependencies = {}

        for name, param in sig.parameters.items():
            if name == "self":
                continue

            # Try to find dependency by type annotation first, then by name
            dependency = self.get_component(param.annotation) or self.get_component(name)

            if dependency:
                dependencies[name] = dependency
            elif param.default is inspect.Parameter.empty:
                # If no default is provided, we can't construct the object
                raise TypeError(
                    f"Could not resolve required dependency '{name}' "
                    f"with type hint '{param.annotation}' for {component_class.__name__}"
                )

        return component_class(**dependencies)

    # Command Management

    def add_command(
        self,
        func: Callable[..., Any] | click.Command,
        name: str | None = None,
        **kwargs: Any,
    ) -> CommandInfo:
        """Add a CLI command to the hub.

        Args:
            func: Command function or Click command
            name: Optional name (defaults to function name)
            **kwargs: Additional command options

        Returns:
            CommandInfo for the registered command

        """
        click_module, has_click = _get_click()
        if has_click and isinstance(func, click_module.Command):
            command_name = name or func.name
            command_func = func.callback
            click_command = func
        else:
            # func should be a callable with __name__
            if hasattr(func, "__name__"):
                command_name = name or func.__name__.replace("_", "-")
            else:
                command_name = name if name is not None else "unknown_command"
            command_func = func
            click_command = None

        info = CommandInfo(
            name=command_name,
            func=command_func,
            description=kwargs.get("description", getattr(func, "__doc__", None)),
            aliases=kwargs.get("aliases", []),
            hidden=kwargs.get("hidden", False),
            category=kwargs.get("category"),
            metadata=kwargs,
        )

        self._command_registry.register(
            name=command_name,
            value=func,
            dimension=ComponentCategory.COMMAND.value,
            metadata={
                "info": info,
                "click_command": click_command,
                **kwargs,
            },
            aliases=info.aliases,
        )

        # Add to CLI group if it exists
        if self._cli_group and click_command:
            self._cli_group.add_command(click_command)

        from provide.foundation.hub.foundation import get_foundation_logger

        get_foundation_logger().info(
            "Added command to hub",
            name=command_name,
            aliases=info.aliases,
        )

        return info

    def get_command(self, name: str) -> Callable[..., Any] | None:
        """Get a command by name.

        Args:
            name: Command name or alias

        Returns:
            Command function or None

        """
        return self._command_registry.get(name, dimension=ComponentCategory.COMMAND.value)

    def list_commands(self) -> list[str]:
        """List all command names.

        Returns:
            List of command names

        """
        return self._command_registry.list_dimension(ComponentCategory.COMMAND.value)

    # CLI Integration

    def create_cli(
        self,
        name: str = "cli",
        version: str | None = None,
        **kwargs: Any,
    ) -> click.Group:
        """Create a Click CLI with all registered commands.

        Requires click to be installed.

        Args:
            name: CLI name
            version: CLI version
            **kwargs: Additional Click Group options

        Returns:
            Click Group with registered commands

        """
        click_module, has_click = _get_click()
        if not has_click:
            raise ImportError("CLI creation requires: pip install 'provide-foundation[cli]'")

        from provide.foundation.hub.commands import create_command_group

        # Use create_command_group which handles nested groups
        cli = create_command_group(name=name, registry=self._command_registry, **kwargs)

        # Add version option if provided
        if version:
            cli = click_module.version_option(version=version)(cli)

        self._cli_group = cli
        return cli

    def add_cli_group(self, group: click.Group) -> None:
        """Add an existing Click group to the hub.

        This registers all commands from the group.

        Args:
            group: Click Group to add

        """
        for name, cmd in group.commands.items():
            self.add_command(cmd, name)

    # Lifecycle Management

    def initialize(self) -> None:
        """Initialize all components that support initialization."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "initialize"):
                try:
                    component_class.initialize()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Initialized component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to initialize {entry.name}: {e}")

    def cleanup(self) -> None:
        """Cleanup all components that support cleanup."""
        for entry in self._component_registry:
            if entry.dimension == ComponentCategory.COMMAND.value:
                continue

            component_class = entry.value
            if hasattr(component_class, "cleanup"):
                try:
                    component_class.cleanup()
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().debug(f"Cleaned up component: {entry.name}")
                except Exception as e:
                    from provide.foundation.hub.foundation import get_foundation_logger

                    get_foundation_logger().error(f"Failed to cleanup {entry.name}: {e}")

    def clear(self, dimension: str | None = None) -> None:
        """Clear registrations.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        if dimension == ComponentCategory.COMMAND.value or dimension is None:
            self._command_registry.clear(dimension=ComponentCategory.COMMAND.value if dimension else None)
            self._cli_group = None

        if dimension != ComponentCategory.COMMAND.value or dimension is None:
            self._component_registry.clear(dimension=dimension)

    def __enter__(self) -> CoreHub:
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.cleanup()
EOF

log_update "Updating: provide/foundation/testmode/__init__.py"
mkdir -p provide/foundation/testmode/
cat <<'EOF' > provide/foundation/testmode/__init__.py
from __future__ import annotations

#
# __init__.py
#
from provide.foundation.testmode.detection import (
    is_in_click_testing,
    is_in_test_mode,
    should_use_shared_registries,
)
from provide.foundation.testmode.internal import (
    reset_circuit_breaker_state,
    reset_global_coordinator,
    reset_hub_state,
    reset_logger_state,
    reset_streams_state,
    reset_structlog_state,
    reset_version_cache,
)
from provide.foundation.testmode.orchestration import (
    reset_foundation_for_testing,
    reset_foundation_state,
    test_scope,
)

"""Foundation Test Mode Support.

This module provides utilities for test mode detection and internal
reset APIs used by testing frameworks. It centralizes all test-related
functionality that Foundation needs for proper test isolation.
"""

__all__ = [
    # Test detection
    "is_in_click_testing",
    "is_in_test_mode",
    # Internal reset APIs (for testkit use)
    "reset_circuit_breaker_state",
    # Orchestrated reset functions
    "reset_foundation_for_testing",
    "reset_foundation_state",
    "reset_global_coordinator",
    "reset_hub_state",
    "reset_logger_state",
    "reset_streams_state",
    "reset_structlog_state",
    "reset_version_cache",
    "should_use_shared_registries",
    "test_scope",
]
EOF

log_update "Updating: provide/foundation/testmode/orchestration.py"
mkdir -p provide/foundation/testmode/
cat <<'EOF' > provide/foundation/testmode/orchestration.py
from __future__ import annotations

#
# orchestration.py
#
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any
from unittest.mock import patch

"""Foundation Test Reset Orchestration.

This module provides the complete reset orchestration for Foundation's
internal state. It knows the proper reset order and handles Foundation-specific
concerns like OpenTelemetry providers and environment variables.

This is Foundation-internal knowledge that should be owned by Foundation,
not by external testing frameworks.
"""

# Global flags to prevent recursive resets
_reset_in_progress = False
_reset_for_testing_in_progress = False


def _reset_otel_once_flag(once_obj: Any) -> None:
    """Reset OpenTelemetry Once flag to allow re-initialization."""
    if hasattr(once_obj, "_done"):
        once_obj._done = False
    if hasattr(once_obj, "_lock"):
        with once_obj._lock:
            once_obj._done = False


def _reset_tracer_provider() -> None:
    """Reset OpenTelemetry tracer provider."""
    try:
        import opentelemetry.trace as otel_trace

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_trace, "_TRACER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_trace._TRACER_PROVIDER_SET_ONCE)

        # Reset to NoOpTracerProvider
        from opentelemetry.trace import NoOpTracerProvider

        otel_trace.set_tracer_provider(NoOpTracerProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def _reset_meter_provider() -> None:
    """Reset OpenTelemetry meter provider."""
    try:
        import opentelemetry.metrics as otel_metrics
        import opentelemetry.metrics._internal as otel_metrics_internal

        # Reset the Once flag to allow re-initialization
        if hasattr(otel_metrics_internal, "_METER_PROVIDER_SET_ONCE"):
            _reset_otel_once_flag(otel_metrics_internal._METER_PROVIDER_SET_ONCE)

        # Reset to NoOpMeterProvider
        from opentelemetry.metrics import NoOpMeterProvider

        otel_metrics.set_meter_provider(NoOpMeterProvider())
    except (ImportError, Exception):
        # Ignore errors during reset - better to continue than fail
        pass


def _reset_opentelemetry_providers() -> None:
    """Reset OpenTelemetry providers to uninitialized state.

    This prevents "Overriding of current TracerProvider/MeterProvider" warnings
    and stream closure issues by properly resetting the global providers.
    """
    _reset_tracer_provider()
    _reset_meter_provider()


def _reset_foundation_environment_variables() -> None:
    """Reset Foundation environment variables that can affect test isolation.

    This resets Foundation-specific environment variables that tests may have set,
    ensuring clean state for subsequent tests while preserving active test configuration.

    Uses a conservative approach: only reset variables that are known to cause
    test isolation issues, and preserve any that might be set by current test.
    """
    import os

    # Always ensure these test defaults are set
    env_var_defaults = {
        "PROVIDE_LOG_LEVEL": "DEBUG",  # Default from conftest.py
        "FOUNDATION_SUPPRESS_TESTING_WARNINGS": "true",  # Default from conftest.py
    }

    # Only reset critical variables that commonly cause test interference
    # Be conservative - don't reset variables that might be intentionally set by tests
    env_vars_to_reset_conditionally = [
        "PROVIDE_PROFILE",
        "PROVIDE_DEBUG",
        "PROVIDE_JSON_OUTPUT",
    ]

    # Set test defaults (but don't override if already set by test)
    for env_var, default_value in env_var_defaults.items():
        if env_var not in os.environ:
            os.environ[env_var] = default_value

    # Only reset problematic variables that commonly cause cross-test contamination
    # Skip resetting variables that tests commonly use with patch.dict()
    for env_var in env_vars_to_reset_conditionally:
        if env_var in os.environ:
            # Only remove if it looks like leftover from previous test
            # This is conservative - when in doubt, preserve
            del os.environ[env_var]


def reset_foundation_state() -> None:
    """Reset Foundation's complete internal state using proper orchestration.

    This is the master reset function that knows the proper order and handles
    Foundation-specific concerns. It resets:
    - structlog configuration to defaults
    - Foundation Hub state (which manages all Foundation components)
    - Stream state back to defaults
    - Lazy setup state tracking (if available)
    - OpenTelemetry provider state (if available)
    - Foundation environment variables to defaults

    This function encapsulates Foundation-internal knowledge about proper
    reset ordering and component dependencies.
    """
    global _reset_in_progress

    # Prevent recursive resets that can cause infinite loops
    if _reset_in_progress:
        return

    _reset_in_progress = True
    try:
        # Import all the individual reset functions from internal module
        from provide.foundation.testmode.internal import (
            reset_circuit_breaker_state,
            reset_configuration_state,
            reset_coordinator_state,
            reset_event_loops,
            reset_eventsets_state,
            reset_hub_state,
            reset_logger_state,
            reset_state_managers,
            reset_streams_state,
            reset_structlog_state,
            reset_time_machine_state,
            reset_version_cache,
        )

        # Signal that reset is in progress to prevent event enrichment and Hub event logging
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(True)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(True)
        except ImportError:
            pass

        # Reset Foundation environment variables first to avoid affecting other resets
        _reset_foundation_environment_variables()

        # Reset in the proper order to avoid triggering reinitialization
        reset_structlog_state()
        reset_streams_state()
        reset_version_cache()

        # Reset event enrichment processor state to prevent re-initialization during cleanup
        try:
            from provide.foundation.logger.processors.main import (
                reset_event_enrichment_state,
            )

            reset_event_enrichment_state()
        except ImportError:
            # Processor module not available, skip
            pass

        # Reset OpenTelemetry providers to avoid "Overriding" warnings and stream closure
        # Note: OpenTelemetry providers are designed to prevent override for safety.
        # In parallel test environments (pytest-xdist), skip this reset to avoid deadlocks.
        # The OTel provider reset manipulates internal _ONCE flags which can deadlock
        # across multiple worker processes. The warnings are harmless in test context.
        import os

        if not os.environ.get("PYTEST_XDIST_WORKER"):
            _reset_opentelemetry_providers()

        # Reset lazy setup state FIRST to prevent hub operations from triggering setup
        reset_logger_state()

        # Clear Hub (this handles all Foundation state including logger instances)
        reset_hub_state()

        # Reset coordinator and event set state
        reset_coordinator_state()
        reset_eventsets_state()

        # Reset circuit breaker state to prevent test isolation issues
        reset_circuit_breaker_state()

        # Reset new state management systems
        reset_state_managers()
        reset_configuration_state()

        # Final reset of logger state (after all operations that might trigger setup)
        reset_logger_state()

        # Reset time_machine patches FIRST to unfreeze time
        # This must happen BEFORE creating a new event loop so the loop doesn't cache frozen time
        reset_time_machine_state()

        # Then clean up event loops to get a fresh loop with unfrozen time
        # The new loop will have correct time.monotonic references
        reset_event_loops()
    finally:
        # Always clear the reset-in-progress flags
        _reset_in_progress = False
        try:
            from provide.foundation.logger.processors.main import (
                set_reset_in_progress as set_processor_reset,
            )

            set_processor_reset(False)
        except ImportError:
            pass

        try:
            from provide.foundation.hub.event_handlers import (
                set_reset_in_progress as set_hub_reset,
            )

            set_hub_reset(False)
        except ImportError:
            pass


def reset_foundation_for_testing() -> None:
    """Complete Foundation reset for testing with transport re-registration.

    This is the full reset function that testing frameworks should call.
    It performs the complete state reset and handles test-specific concerns
    like transport re-registration and test stream preservation.
    """
    global _reset_for_testing_in_progress

    # Prevent recursive resets during test cleanup
    if _reset_for_testing_in_progress:
        return

    _reset_for_testing_in_progress = True
    try:
        # Save current stream if it's a test stream (not stderr/stdout)
        import sys

        preserve_stream = None
        try:
            from provide.foundation.streams.core import get_log_stream

            current_stream = get_log_stream()
            # Only preserve if it's not stderr/stdout (i.e., it's a test stream)
            if current_stream not in (sys.stderr, sys.stdout):
                preserve_stream = current_stream
        except Exception:
            # Error getting current stream, skip preservation
            pass

        # Full reset with Hub-based state management
        reset_foundation_state()

        # Reset transport registration flags so transports can be re-registered
        try:
            from provide.foundation.testmode.internal import reset_transport_registration_flags

            reset_transport_registration_flags()
        except ImportError:
            # Testmode module not available
            pass

        # Re-register HTTP transport for tests that need it
        try:
            from provide.foundation.transport.http import _register_http_transport

            _register_http_transport()
        except ImportError:
            # Transport module not available
            pass

        # Final reset of lazy setup state (after transport registration)
        try:
            from provide.foundation.logger.core import _LAZY_SETUP_STATE

            _LAZY_SETUP_STATE.update({"done": False, "error": None, "in_progress": False})
        except ImportError:
            pass

        # Restore test stream if there was one
        if preserve_stream:
            try:
                from provide.foundation.streams.core import set_log_stream_for_testing

                set_log_stream_for_testing(preserve_stream)
            except Exception:
                # Error restoring stream, continue without it
                pass
    finally:
        # Always clear the in-progress flag
        _reset_for_testing_in_progress = False


@contextmanager
def test_scope() -> Generator[Any, None, None]:
    """Provides an isolated Hub instance for the duration of a test.

    This context manager creates a temporary, isolated Hub instance and patches
    `provide.foundation.hub.manager.get_hub` to return it. This ensures that
    any code calling `get_hub()` within the `with` block receives the isolated
    instance, preventing state leakage between tests.

    Yields:
        A fresh, isolated Hub instance.

    Example:
        def test_my_component_in_isolation():
            with test_scope() as hub:
                # hub is a fresh, isolated instance
                hub.add_component(MockDb, 'db')
                component = MyComponent() # This component's call to get_hub() gets the isolated one
                component.do_work()
                # ... assertions ...
        # On exit from the 'with' block, all state is gone.
    """
    from provide.foundation.hub.manager import Hub

    # Create a new, non-shared Hub instance for this scope
    isolated_hub = Hub(use_shared_registries=False)

    with patch("provide.foundation.hub.manager.get_hub", return_value=isolated_hub):
        try:
            yield isolated_hub
        finally:
            # Cleanup resources held by the isolated hub
            isolated_hub.clear()
EOF

log_success "Project update complete."