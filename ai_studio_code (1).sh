#!/bin/bash
# 🛠️ Project Update Script
set -eo pipefail

# --- Logging ---
log_info() { echo -e "ℹ️  $1"; }
log_update() { echo -e "🔄 $1"; }
log_success() { echo -e "✅ $1"; }

# --- Operations ---
log_info "Applying Phase 1 & 2 of internal state refactoring..."

log_update "Updating: provide/foundation/file/operations/detectors/orchestrator.py"
mkdir -p provide/foundation/file/operations/detectors/
cat <<'EOF' > provide/foundation/file/operations/detectors/orchestrator.py
"""File operation detector orchestrator.

Coordinates detector functions via registry to identify the best match for file events.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from provide.foundation.file.operations.detectors.auto_flush import AutoFlushHandler
from provide.foundation.file.operations.detectors.helpers import (
    extract_base_name,
    is_temp_file,
)
from provide.foundation.file.operations.detectors.registry import get_detector_registry
from provide.foundation.file.operations.types import (
    DetectorConfig,
    FileEvent,
    FileOperation,
)
from provide.foundation.hub.registry import Registry
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class OperationDetector:
    """Detects and classifies file operations from events."""

    def __init__(
        self,
        config: DetectorConfig | None = None,
        on_operation_complete: Any = None,
        registry: Registry | None = None,
    ) -> None:
        """Initialize with optional configuration and callback.

        Args:
            config: Detector configuration
            on_operation_complete: Callback function(operation: FileOperation) called
                                 when an operation is detected. Used for streaming mode.
            registry: Optional registry for detectors (defaults to global)
        """
        self.config = config or DetectorConfig()
        self.on_operation_complete = on_operation_complete
        self.registry = registry or get_detector_registry()
        self._pending_events: list[FileEvent] = []
        self._last_flush = datetime.now()

        # Create auto-flush handler for streaming mode
        self._auto_flush_handler = AutoFlushHandler(
            time_window_ms=self.config.time_window_ms,
            on_operation_complete=on_operation_complete,
            analyze_func=self._analyze_event_group,
        )

    def detect(self, events: list[FileEvent]) -> list[FileOperation]:
        """Detect all operations from a list of events.

        Args:
            events: List of file events to analyze

        Returns:
            List of detected operations, ordered by start time
        """
        if not events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)

        # Group events by time windows
        event_groups = self._group_events_by_time(sorted_events)

        operations = []
        for group in event_groups:
            operation = self._analyze_event_group(group)
            if operation:
                operations.append(operation)

        return operations

    def detect_streaming(self, event: FileEvent) -> FileOperation | None:
        """Process events in streaming fashion.

        Args:
            event: Single file event

        Returns:
            Completed operation if detected, None otherwise
        """
        self._pending_events.append(event)

        # Check if we should flush based on time window
        now = datetime.now()
        time_since_last = (now - self._last_flush).total_seconds() * 1000

        if time_since_last >= self.config.time_window_ms:
            return self._flush_pending()

        return None

    def add_event(self, event: FileEvent) -> None:
        """Add event with auto-flush and callback support.

        This is the recommended method for streaming detection with automatic
        temp file hiding and callback-based operation reporting.

        Args:
            event: File event to process

        Behavior:
            - Hides temp files automatically (no callback until operation completes)
            - Schedules auto-flush timer for pending operations
            - Calls on_operation_complete(operation) when pattern detected
            - Emits non-temp files immediately if no operation pattern found
        """
        # Delegate to auto-flush handler
        self._auto_flush_handler.add_event(event)

    def flush(self) -> list[FileOperation]:
        """Get any pending operations and clear buffer."""
        operations = []
        if self._pending_events:
            operation = self._flush_pending()
            if operation:
                operations.append(operation)
        return operations

    def _flush_pending(self) -> FileOperation | None:
        """Analyze pending events and clear buffer."""
        if not self._pending_events:
            return None

        operation = self._analyze_event_group(self._pending_events)
        self._pending_events.clear()
        self._last_flush = datetime.now()
        return operation

    def _group_events_by_time(self, events: list[FileEvent]) -> list[list[FileEvent]]:
        """Group events that occur within time windows.

        Uses a fixed time window from the first event in each group to ensure
        all related events are captured together, even if they span longer than
        the window between consecutive events.
        """
        if not events:
            return []

        groups = []
        current_group = [events[0]]
        group_start_time = events[0].timestamp  # Track first event in group

        for event in events[1:]:
            # Compare to FIRST event in group, not last (fixes bundling bug)
            time_diff = (event.timestamp - group_start_time).total_seconds() * 1000

            if time_diff <= self.config.time_window_ms:
                current_group.append(event)
            else:
                groups.append(current_group)
                current_group = [event]
                group_start_time = event.timestamp  # Reset for new group

        if current_group:
            groups.append(current_group)

        return groups

    def _analyze_event_group(self, events: list[FileEvent]) -> FileOperation | None:
        """Analyze a group of events to detect an operation using registry-based detectors.

        Performance optimizations:
        - Registry-based detector lookup (extensible)
        - Priority-ordered execution (highest priority first)
        - Early termination on high-confidence matches (>=0.95)
        """
        if not events:
            return None

        # Get all registered detectors from the instance's registry, sorted by priority
        all_entries = [entry for entry in self.registry if entry.dimension == "file_operation_detector"]
        sorted_entries = sorted(all_entries, key=lambda e: e.metadata.get("priority", 0), reverse=True)
        detectors = [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]

        best_operation = None
        best_confidence = 0.0
        # Early termination threshold - stop searching if we find a very high confidence match
        HIGH_CONFIDENCE_THRESHOLD = 0.95

        for detector_name, detect_func, priority in detectors:
            try:
                operation = detect_func(events)
                if operation and operation.confidence > best_confidence:
                    best_operation = operation
                    best_confidence = operation.confidence
                    log.debug(
                        "Found better operation match",
                        detector=detector_name,
                        priority=priority,
                        confidence=operation.confidence,
                        operation_type=operation.operation_type.value,
                        primary_path=str(operation.primary_path),
                    )

                    # Early termination: if we found a very high confidence match, stop searching
                    if best_confidence >= HIGH_CONFIDENCE_THRESHOLD:
                        log.debug(
                            "Early termination on high confidence match",
                            confidence=best_confidence,
                            detector=detector_name,
                        )
                        break

            except Exception as e:
                log.warning(
                    "Detector failed",
                    detector=detector_name,
                    priority=priority,
                    error=str(e),
                )

        if best_operation and best_confidence >= self.config.min_confidence:
            # Validate that primary_path is not a temp file
            if is_temp_file(best_operation.primary_path):
                log.warning(
                    "Detector returned temp file as primary_path, attempting to fix",
                    temp_path=str(best_operation.primary_path),
                    operation_type=best_operation.operation_type.value,
                )
                # Try to find the real file from the events
                real_file = self._find_real_file_from_events(best_operation.events)
                if real_file:
                    # Create a new operation with the corrected path
                    # (FileOperation is frozen, so we need attrs.evolve or recreate)
                    from attrs import evolve

                    best_operation = evolve(best_operation, primary_path=real_file)
                    log.info(
                        "Corrected primary_path from temp to real file",
                        corrected_path=str(real_file),
                    )
                else:
                    log.error(
                        "Could not find real file, rejecting operation",
                        temp_path=str(best_operation.primary_path),
                    )
                    return None

            log.debug(
                "Selected operation",
                operation_type=best_operation.operation_type.value,
                primary_path=str(best_operation.primary_path),
                confidence=best_confidence,
                is_temp=is_temp_file(best_operation.primary_path),
            )
            return best_operation

        return None

    def _find_real_file_from_events(self, events: list[FileEvent]) -> Path | None:
        """Find the real (non-temp) file path from a list of events."""
        # Look for non-temp files in the events
        for event in reversed(events):  # Start from most recent
            # Check dest_path first (for move/rename operations)
            if event.dest_path and not is_temp_file(event.dest_path):
                return event.dest_path
            # Then check regular path
            if not is_temp_file(event.path):
                return event.path

        # If all files are temp files, try to extract the base name
        for event in events:
            if event.dest_path:
                base_name = extract_base_name(event.dest_path)
                if base_name:
                    # Try to construct real path from base name
                    real_path = event.dest_path.parent / base_name
                    if real_path != event.dest_path:
                        return real_path

            base_name = extract_base_name(event.path)
            if base_name:
                real_path = event.path.parent / base_name
                if real_path != event.path:
                    return real_path

        return None
EOF

log_update "Updating: provide/foundation/hub/foundation.py"
mkdir -p provide/foundation/hub/
cat <<'EOF' > provide/foundation/hub/foundation.py
from __future__ import annotations

import contextlib
import threading
from typing import TYPE_CHECKING, Any

from provide.foundation.hub.registry import Registry

"""Foundation system initialization and lifecycle management.

This module provides Foundation-specific functionality for the Hub,
including telemetry configuration and logger initialization.
"""

if TYPE_CHECKING:
    from provide.foundation.hub.manager import Hub
    from provide.foundation.logger.base import FoundationLogger
    from provide.foundation.logger.config import TelemetryConfig


class FoundationManager:
    """Manages Foundation system initialization and lifecycle."""

    def __init__(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Smart initialization: If explicit config is provided and Foundation
        was auto-initialized with defaults, automatically upgrades to force=True
        to ensure explicit config takes precedence.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        # Smart initialization: Try lightweight config update OR force re-init when explicit
        # config is provided but Foundation is already auto-initialized with defaults
        if (
            config is not None  # Explicit config provided
            and self._initialized  # Already initialized (likely auto-init)
            and not force  # User didn't explicitly set force
            and self._config is not None  # Have existing config to check
            and getattr(self._config, "service_name", "not-none") is None  # Auto-init indicator
        ):
            # Check if OTLP is configured - if so, we MUST do full re-init to recreate LoggerProvider
            # The LoggerProvider bakes service_name into its Resource during creation, so we can't
            # just update the config - we need to recreate it
            otlp_configured = (
                getattr(self._config, "otlp_endpoint", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry, config=config, force=force
        )

        # Update our local state
        self._config = actual_config
        self._logger_instance = logger_instance
        self._initialized = True

        # Log initialization success (avoid test interference)
        import os

        if not os.environ.get("PYTEST_CURRENT_TEST"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def get_foundation_logger(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        # Ensure Foundation is initialized
        if not self._initialized:
            self.initialize_foundation()

        # Get logger instance from registry
        logger_instance = self._registry.get("foundation.logger.instance", "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._initialized

    def get_foundation_config(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "singleton")

    def clear_foundation_state(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def _get_logger(self) -> Any | None:
        """Get logger for internal use."""
        if self._logger_instance:
            return self._logger_instance.get_logger(__name__)

        # Fallback during initialization
        import structlog

        return structlog.get_logger(__name__)


def get_foundation_logger(name: str | None = None) -> Any:
    """Get a logger from the Foundation system.

    This is the preferred way to get loggers instead of using _get_logger()
    patterns that create circular import issues.

    Args:
        name: Logger name (defaults to calling module)

    Returns:
        Logger instance
    """
    from provide.foundation.hub.manager import get_hub

    hub = get_hub()
    if hasattr(hub, "_foundation") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger
EOF

log_update "Updating: provide/foundation/hub/manager.py"
mkdir -p provide/foundation/hub/
cat <<'EOF' > provide/foundation/hub/manager.py
from __future__ import annotations

from typing import Any

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.context import CLIContext
from provide.foundation.hub.commands import get_command_registry
from provide.foundation.hub.components import get_component_registry
from provide.foundation.hub.core import CoreHub
from provide.foundation.hub.foundation import FoundationManager
from provide.foundation.hub.registry import Registry
from provide.foundation.testmode.detection import should_use_shared_registries

"""Hub manager - the main coordinator for components and commands.

This module provides the Hub class that coordinates component and command
registration, discovery, and access, with Foundation system integration.
"""


class Hub(CoreHub):
    """Central hub for managing components, commands, and Foundation integration.

    The Hub provides a unified interface for:
    - Registering components and commands
    - Discovering plugins via entry points
    - Creating Click CLI applications
    - Managing component lifecycle
    - Foundation system initialization

    Example:
        >>> hub = Hub()
        >>> hub.add_component(MyResource, "resource")
        >>> hub.add_command(init_cmd, "init")
        >>> hub.initialize_foundation()
        >>>
        >>> # Create CLI with all commands
        >>> cli = hub.create_cli()
        >>> cli()

    """

    def __init__(
        self,
        context: CLIContext | None = None,
        component_registry: Registry | None = None,
        command_registry: Registry | None = None,
        use_shared_registries: bool = False,
    ) -> None:
        """Initialize the hub.

        Args:
            context: Foundation CLIContext for configuration
            component_registry: Custom component registry
            command_registry: Custom command registry
            use_shared_registries: If True, use global shared registries

        """
        # Determine if we should use shared registries
        use_shared = should_use_shared_registries(use_shared_registries, component_registry, command_registry)

        # Setup registries
        if component_registry:
            comp_registry = component_registry
        elif use_shared:
            comp_registry = get_component_registry()
        else:
            comp_registry = Registry()

        if command_registry:
            cmd_registry = command_registry
        elif use_shared:
            cmd_registry = get_command_registry()
        else:
            cmd_registry = Registry()

        # Initialize core hub functionality
        super().__init__(context, comp_registry, cmd_registry)

        # Initialize Foundation management, injecting self
        self._foundation = FoundationManager(hub=self, registry=self._component_registry)

    # Foundation Integration Methods

    def initialize_foundation(self, config: Any = None, force: bool = False) -> None:
        """Initialize Foundation system through Hub.

        Single initialization method replacing all setup_* functions.
        Thread-safe and idempotent, unless force=True.

        Args:
            config: Optional TelemetryConfig (defaults to from_env)
            force: If True, force re-initialization even if already initialized

        """
        self._foundation.initialize_foundation(config, force)

    def get_foundation_logger(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        return self._foundation.get_foundation_logger(name)

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._foundation.is_foundation_initialized()

    def get_foundation_config(self) -> Any | None:
        """Get the current Foundation configuration."""
        return self._foundation.get_foundation_config()

    def clear(self, dimension: str | None = None) -> None:
        """Clear registrations and dispose of resources properly.

        Args:
            dimension: Optional dimension to clear (None = all)

        """
        # Clear core hub registrations (this will now dispose resources)
        super().clear(dimension)

        # Reset Foundation state when clearing all or foundation-specific dimensions
        if dimension is None or dimension in ("singleton", "foundation"):
            self._foundation.clear_foundation_state()

    def dispose_all(self) -> None:
        """Dispose of all managed resources without clearing registrations."""
        self._component_registry.dispose_all()
        if hasattr(self._command_registry, "dispose_all"):
            self._command_registry.dispose_all()


# Global hub instance for thread-safe singleton initialization
_global_hub: Hub | None = None


def get_hub() -> Hub:
    """Get the global shared hub instance (singleton pattern).

    This function acts as the Composition Root for the global singleton instance.
    It is maintained for backward compatibility and convenience.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to use a `Container` or `Hub` instance created at your application's
    entry point for explicit dependency management. This global accessor should be
    avoided in application code.

    Thread-safe: Uses double-checked locking pattern for efficient lazy initialization.

    **Auto-Initialization Behavior:**
    This function automatically initializes the Foundation system on first access.
    The initialization is:
    - **Idempotent**: Safe to call multiple times
    - **Thread-safe**: Uses lock manager for coordination
    - **Lazy**: Only happens on first access

    Returns:
        Global Hub instance (created and initialized if needed)

    Example:
        >>> hub = get_hub()
        >>> hub.register_command("my_command", my_function)

    Note:
        For isolated Hub instances (testing, advanced use cases), use:
        >>> hub = Hub(use_shared_registries=False)

    """
    global _global_hub

    # Fast path: hub already initialized
    if _global_hub is not None:
        return _global_hub

    # Slow path: need to initialize hub
    with get_lock_manager().acquire("foundation.hub.init"):
        # Double-check after acquiring lock
        if _global_hub is None:
            # Global hub uses shared registries by default
            _global_hub = Hub(use_shared_registries=True)

            # Auto-initialize Foundation on first hub access
            _global_hub.initialize_foundation()

            # Bootstrap foundation components now that hub is ready (skip in test mode)
            from provide.foundation.testmode.detection import is_in_test_mode

            if not is_in_test_mode():
                try:
                    from provide.foundation.hub.components import bootstrap_foundation

                    bootstrap_foundation()
                except ImportError:
                    # Bootstrap function might not exist yet, that's okay
                    pass

    return _global_hub


def clear_hub() -> None:
    """Clear the global hub instance.

    This is primarily used for testing to reset Foundation state
    between test runs.

    """
    global _global_hub
    if _global_hub:
        _global_hub.clear()
    _global_hub = None
EOF

log_update "Updating: provide/foundation/logger/core.py"
mkdir -p provide/foundation/logger/
cat <<'EOF' > provide/foundation/logger/core.py
from __future__ import annotations

#
# core.py
#
import contextlib
from typing import TYPE_CHECKING, Any

import structlog

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.logger.types import TRACE_LEVEL_NAME, TRACE_LEVEL_NUM

"""Core FoundationLogger implementation.
Contains the main logging class with all logging methods.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig

_LAZY_SETUP_STATE: dict[str, Any] = {"done": False, "error": None, "in_progress": False}


class FoundationLogger:
    """A `structlog`-based logger providing a standardized logging interface."""

    def __init__(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def setup(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def _check_structlog_already_disabled(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def _try_hub_configuration(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return False

        try:
            # Use the injected hub instance to get config
            config = self._hub.get_foundation_config()
            if config and not self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def _should_use_emergency_fallback(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"]

    def _perform_locked_setup(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def _ensure_configured(self) -> None:
        """Ensures the logger is configured, performing lazy setup if necessary.
        Uses Hub for configuration when available, falls back to lazy setup.
        This method is thread-safe and handles setup failures gracefully.
        """
        # Fast path for already configured loggers.
        if self._is_configured_by_setup:
            return

        # If we have a Hub, try to get configuration from it
        if self._try_hub_configuration():
            return

        # Check if setup is already done
        if _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]:
            return

        # If setup is in progress by another thread, or failed previously, use fallback.
        if self._should_use_emergency_fallback():
            self._setup_emergency_fallback()
            return

        # If structlog is already configured to be a no-op, we're done.
        if self._check_structlog_already_disabled():
            return

        # Acquire lock to perform setup.
        try:
            with get_lock_manager().acquire("foundation.logger.lazy"):
                self._perform_locked_setup()
        except Exception:
            # If lock acquisition fails (e.g., due to ordering violations), use emergency fallback
            self._setup_emergency_fallback()

    def _perform_lazy_setup(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def _setup_emergency_fallback(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def get_logger(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "foundation.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def _log_with_level(self, level_method_name: str, event: str, **kwargs: Any) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def _format_message_with_args(self, event: str | Any, args: tuple[Any, ...]) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(event) % args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(event)

    def trace(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def bind(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def unbind(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def try_unbind(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, "_logger") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to prevent accidental modification of logger state."""
        if hasattr(self, name) and name.startswith("_"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


# Global logger function - gets logger through Hub
def get_global_logger() -> FoundationLogger:
    """Get the global FoundationLogger instance through Hub.

    This function acts as the Composition Root for the global logger instance,
    maintained for backward compatibility.

    **Note:** For building testable and maintainable applications, the recommended
    approach is to inject a logger instance via a `Container`. This global
    accessor should be avoided in new application code.

    Returns:
        FoundationLogger instance from Hub

    """
    from provide.foundation.hub.manager import get_hub

    hub = get_hub()
    logger_instance = hub._component_registry.get("foundation.logger.instance", "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


class GlobalLoggerProxy:
    """Proxy object that forwards all attribute access to Hub-based logger."""

    def __getattr__(self, name: str) -> Any:
        return getattr(get_global_logger(), name)

    # Forward common logger methods to help mypy
    def debug(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(event, *args, **kwargs)

    def info(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(event, *args, **kwargs)

    def warning(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(event, *args, **kwargs)

    def error(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(event, *args, **kwargs)

    def critical(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(event, *args, **kwargs)

    def exception(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(event, *args, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow tests to set internal state on the underlying logger."""
        if name.startswith("_"):
            # For internal attributes, set them on the actual logger instance
            logger = get_global_logger()
            setattr(logger, name, value)
        else:
            super().__setattr__(name, value)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return get_global_logger()(*args, **kwargs)


# Global logger instance (now a proxy)
logger = GlobalLoggerProxy()
EOF

log_update "Updating: provide/foundation/resilience/decorators.py"
mkdir -p provide/foundation/resilience/
cat <<'EOF' > provide/foundation/resilience/decorators.py
from __future__ import annotations

import asyncio
from collections.abc import Callable
import functools
import inspect
import threading
from typing import TYPE_CHECKING, Any, TypeVar

from provide.foundation.errors.config import ConfigurationError
from provide.foundation.resilience.circuit_async import AsyncCircuitBreaker
from provide.foundation.resilience.circuit_sync import SyncCircuitBreaker
from provide.foundation.resilience.defaults import DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)

if TYPE_CHECKING:
    from provide.foundation.hub.registry import Registry

"""Resilience decorators for retry, circuit breaker, and fallback patterns."""

# Circuit breaker registry dimensions
CIRCUIT_BREAKER_DIMENSION = "circuit_breaker"
CIRCUIT_BREAKER_TEST_DIMENSION = "circuit_breaker_test"

# Counter for generating unique circuit breaker names (protected by lock)
_circuit_breaker_counter = 0
_circuit_breaker_counter_lock = threading.Lock()


def _get_circuit_breaker_registry() -> Registry:
    """Get the Hub registry for circuit breakers."""
    from provide.foundation.hub.manager import get_hub

    return get_hub()._component_registry  # type: ignore[attr-defined]


def _should_register_for_global_reset() -> bool:
    """Determine if a circuit breaker should be registered for global reset.

    Circuit breakers created in test files should not be registered for global
    reset to ensure proper test isolation in parallel execution.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return True

        # Walk up the call stack to find where the decorator is being applied
        while frame:
            frame = frame.f_back
            if frame is None:
                break

            filename = frame.f_code.co_filename

            # If we're in a test file, don't register for global reset
            # This catches both runtime and import-time circuit breaker creation
            if "/tests/" in filename or "test_" in filename or "conftest" in filename:
                return False

        return True
    except Exception:
        # If inspection fails, assume we should register (safer default)
        return True


F = TypeVar("F", bound=Callable[..., Any])


def _handle_no_parentheses_retry(func: F) -> F:
    """Handle @retry decorator used without parentheses."""
    executor = RetryExecutor(RetryPolicy())

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper


def _validate_retry_parameters(
    policy: RetryPolicy | None,
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> None:
    """Validate that policy and individual parameters are not both specified."""
    if policy is not None and any(
        p is not None for p in [max_attempts, base_delay, backoff, max_delay, jitter]
    ):
        raise ConfigurationError(
            "Cannot specify both policy and individual retry parameters",
            code="CONFLICTING_RETRY_CONFIG",
            has_policy=policy is not None,
            individual_params=[
                name
                for name, value in [
                    ("max_attempts", max_attempts),
                    ("base_delay", base_delay),
                    ("backoff", backoff),
                    ("max_delay", max_delay),
                    ("jitter", jitter),
                ]
                if value is not None
            ],
        )


def _build_retry_policy(
    exceptions: tuple[type[Exception], ...],
    max_attempts: int | None,
    base_delay: float | None,
    backoff: BackoffStrategy | None,
    max_delay: float | None,
    jitter: bool | None,
) -> RetryPolicy:
    """Build a retry policy from individual parameters."""
    policy_kwargs: dict[str, Any] = {}

    if max_attempts is not None:
        policy_kwargs["max_attempts"] = max_attempts
    if base_delay is not None:
        policy_kwargs["base_delay"] = base_delay
    if backoff is not None:
        policy_kwargs["backoff"] = backoff
    if max_delay is not None:
        policy_kwargs["max_delay"] = max_delay
    if jitter is not None:
        policy_kwargs["jitter"] = jitter
    if exceptions:
        policy_kwargs["retryable_errors"] = exceptions

    return RetryPolicy(**policy_kwargs)


def _create_retry_wrapper(
    func: F,
    policy: RetryPolicy,
    on_retry: Callable[[int, Exception], None] | None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> F:
    """Create the retry wrapper for a function."""
    executor = RetryExecutor(
        policy,
        on_retry=on_retry,
        time_source=time_source,
        sleep_func=sleep_func,
        async_sleep_func=async_sleep_func,
    )

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            return await executor.execute_async(func, *args, **kwargs)

        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return executor.execute_sync(func, *args, **kwargs)

    return sync_wrapper


def retry(
    *exceptions: type[Exception],
    policy: RetryPolicy | None = None,
    max_attempts: int | None = None,
    base_delay: float | None = None,
    backoff: BackoffStrategy | None = None,
    max_delay: float | None = None,
    jitter: bool | None = None,
    on_retry: Callable[[int, Exception], None] | None = None,
    time_source: Callable[[], float] | None = None,
    sleep_func: Callable[[float], None] | None = None,
    async_sleep_func: Callable[[float], Any] | None = None,
) -> Callable[[F], F]:
    """Decorator for retrying operations on errors.

    Can be used in multiple ways:

    1. With a policy object:
        @retry(policy=RetryPolicy(max_attempts=5))

    2. With individual parameters:
        @retry(max_attempts=3, base_delay=1.0)

    3. With specific exceptions:
        @retry(ConnectionError, TimeoutError, max_attempts=3)

    4. Without parentheses (uses defaults):
        @retry
        def my_func(): ...

    Args:
        *exceptions: Exception types to retry (all if empty)
        policy: Complete retry policy (overrides other params)
        max_attempts: Maximum retry attempts
        base_delay: Base delay between retries
        backoff: Backoff strategy
        max_delay: Maximum delay cap
        jitter: Whether to add jitter
        on_retry: Callback for retry events
        time_source: Optional callable that returns current time (for testing)
        sleep_func: Optional synchronous sleep function (for testing)
        async_sleep_func: Optional asynchronous sleep function (for testing)

    Returns:
        Decorated function with retry logic

    Examples:
        >>> @retry(max_attempts=3)
        ... def flaky_operation():
        ...     # May fail occasionally
        ...     pass

        >>> @retry(ConnectionError, max_attempts=5, base_delay=2.0)
        ... async def connect_to_service():
        ...     # Async function with specific error handling
        ...     pass

    """
    # Handle decorator without parentheses
    if len(exceptions) == 1 and callable(exceptions[0]) and not isinstance(exceptions[0], type):
        # Called as @retry without parentheses
        func = exceptions[0]
        return _handle_no_parentheses_retry(func)

    # Validate parameters
    _validate_retry_parameters(policy, max_attempts, base_delay, backoff, max_delay, jitter)

    # Build policy if not provided
    if policy is None:
        policy = _build_retry_policy(exceptions, max_attempts, base_delay, backoff, max_delay, jitter)

    def decorator(func: F) -> F:
        return _create_retry_wrapper(
            func,
            policy,
            on_retry,
            time_source=time_source,
            sleep_func=sleep_func,
            async_sleep_func=async_sleep_func,
        )

    return decorator


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = DEFAULT_CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
    expected_exception: type[Exception] | tuple[type[Exception], ...] = Exception,
    time_source: Callable[[], float] | None = None,
    registry: Registry | None = None,
) -> Callable[[F], F]:
    """Create a circuit breaker decorator.

    Creates a SyncCircuitBreaker for synchronous functions and an
    AsyncCircuitBreaker for asynchronous functions to avoid locking issues.

    Args:
        failure_threshold: Number of failures before opening circuit.
        recovery_timeout: Seconds to wait before attempting recovery.
        expected_exception: Exception type(s) that trigger the breaker.
            Can be a single exception type or a tuple of exception types.
        time_source: Optional callable that returns current time (for testing).
        registry: Optional registry to register the breaker with (for DI).

    Returns:
        Circuit breaker decorator.

    Examples:
        >>> @circuit_breaker(failure_threshold=3, recovery_timeout=30)
        ... def unreliable_service():
        ...     return external_api_call()

        >>> @circuit_breaker(expected_exception=ValueError)
        ... def parse_data():
        ...     return risky_parse()

        >>> @circuit_breaker(expected_exception=(ValueError, TypeError))
        ... async def async_unreliable_service():
        ...     return await async_api_call()

    """
    # Normalize expected_exception to tuple
    if not isinstance(expected_exception, tuple):
        expected_exception_tuple = (expected_exception,)
    else:
        expected_exception_tuple = expected_exception

    def decorator(func: F) -> F:
        global _circuit_breaker_counter

        # Use provided registry or fall back to global
        reg = registry or _get_circuit_breaker_registry()

        # Create appropriate breaker type based on function type
        if asyncio.iscoroutinefunction(func):
            breaker = AsyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await breaker.call(func, *args, **kwargs)

            # Register async circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return async_wrapper  # type: ignore
        else:
            breaker = SyncCircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                expected_exception=expected_exception_tuple,
                time_source=time_source,
            )

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return breaker.call(func, *args, **kwargs)

            # Register sync circuit breaker (thread-safe)
            with _circuit_breaker_counter_lock:
                _circuit_breaker_counter += 1
                breaker_name = f"cb_{_circuit_breaker_counter}"

            if _should_register_for_global_reset():
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_DIMENSION)
            else:
                reg.register(breaker_name, breaker, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)

            return sync_wrapper  # type: ignore

    return decorator


async def reset_circuit_breakers_for_testing() -> None:
    """Reset all circuit breaker instances for test isolation.

    This function is called by the test framework to ensure
    circuit breaker state doesn't leak between tests.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


async def reset_test_circuit_breakers() -> None:
    """Reset circuit breaker instances created in test files.

    This function resets circuit breakers that were created within test files
    to ensure proper test isolation without affecting production circuit breakers.

    Note: This is an async function because AsyncCircuitBreaker has async methods.
    Both sync and async circuit breakers are reset using their reset() method.
    """
    registry = _get_circuit_breaker_registry()
    for name in registry.list_dimension(CIRCUIT_BREAKER_TEST_DIMENSION):
        breaker = registry.get(name, dimension=CIRCUIT_BREAKER_TEST_DIMENSION)
        if breaker:
            if isinstance(breaker, AsyncCircuitBreaker):
                await breaker.reset()
            else:
                breaker.reset()


def fallback(*fallback_funcs: Callable[..., Any]) -> Callable[[F], F]:
    """Fallback decorator using FallbackChain.

    Args:
        *fallback_funcs: Functions to use as fallbacks, in order of preference

    Returns:
        Decorated function with fallback chain

    Examples:
        >>> def backup_api():
        ...     return "backup result"
        ...
        >>> @fallback(backup_api)
        ... def primary_api():
        ...     return external_api_call()

    """
    from provide.foundation.resilience.fallback import FallbackChain

    def decorator(func: F) -> F:
        chain = FallbackChain()
        for fallback_func in fallback_funcs:
            chain.add_fallback(fallback_func)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await chain.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            return chain.execute(func, *args, **kwargs)

        return sync_wrapper  # type: ignore

    return decorator
EOF

log_update "Updating: provide/foundation/transport/client.py"
mkdir -p provide/foundation/transport/
cat <<'EOF' > provide/foundation/transport/client.py
from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from attrs import define, field

from provide.foundation.hub import Hub, get_hub
from provide.foundation.logger import get_logger
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.cache import TransportCache
from provide.foundation.transport.errors import TransportError
from provide.foundation.transport.middleware import (
    MiddlewarePipeline,
    create_default_pipeline,
)
from provide.foundation.transport.registry import get_transport
from provide.foundation.transport.types import Data, Headers, HTTPMethod, Params

"""Universal transport client with middleware support."""

log = get_logger(__name__)


@define(slots=True)
class UniversalClient:
    """Universal client that works with any transport via Hub registry.

    The client uses a TransportCache that automatically evicts transports
    that exceed the failure threshold (default: 3 consecutive failures).
    """

    hub: Hub = field()
    middleware: MiddlewarePipeline = field(factory=create_default_pipeline)
    default_headers: Headers = field(factory=dict)
    default_timeout: float | None = field(default=None)
    _cache: TransportCache = field(factory=TransportCache, init=False)

    async def request(
        self,
        uri: str,
        method: str | HTTPMethod = HTTPMethod.GET,
        *,
        headers: Headers | None = None,
        params: Params | None = None,
        body: Data = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> Response:
        """Make a request using appropriate transport.

        Args:
            uri: Full URI to make request to
            method: HTTP method or protocol-specific method
            headers: Request headers
            params: Query parameters
            body: Request body (dict for JSON, str/bytes for raw)
            timeout: Request timeout override
            **kwargs: Additional request metadata

        Returns:
            Response from the transport

        """
        # Normalize method
        if isinstance(method, HTTPMethod):
            method = method.value

        # Merge headers
        request_headers = dict(self.default_headers)
        if headers:
            request_headers.update(headers)

        # Create request object
        request = Request(
            uri=uri,
            method=method,
            headers=request_headers,
            params=params or {},
            body=body,
            timeout=timeout or self.default_timeout,
            metadata=kwargs,
        )

        # Process through middleware
        request = await self.middleware.process_request(request)

        try:
            # Get transport for this URI
            transport = await self._get_transport(request.transport_type.value)

            # Execute request
            response = await transport.execute(request)

            # Mark success in cache
            self._cache.mark_success(request.transport_type.value)

            # Process response through middleware
            response = await self.middleware.process_response(response)

            return response

        except Exception as e:
            # Mark failure if it's a transport error
            if isinstance(e, TransportError):
                self._cache.mark_failure(request.transport_type.value, e)

            # Process error through middleware
            e = await self.middleware.process_error(e, request)
            raise e

    async def stream(
        self,
        uri: str,
        method: str | HTTPMethod = HTTPMethod.GET,
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """Stream data from URI.

        Args:
            uri: URI to stream from
            method: HTTP method or protocol-specific method
            **kwargs: Additional request parameters

        Yields:
            Chunks of response data

        """
        # Normalize method
        if isinstance(method, HTTPMethod):
            method = method.value

        # Create request
        request = Request(uri=uri, method=method, headers=dict(self.default_headers), **kwargs)

        # Get transport
        transport = await self._get_transport(request.transport_type.value)

        # Stream response
        log.info(f"🌊 Streaming {method} {uri}")
        async for chunk in transport.stream(request):
            yield chunk

    async def get(self, uri: str, **kwargs: Any) -> Response:
        """GET request."""
        return await self.request(uri, HTTPMethod.GET, **kwargs)

    async def post(self, uri: str, **kwargs: Any) -> Response:
        """POST request."""
        return await self.request(uri, HTTPMethod.POST, **kwargs)

    async def put(self, uri: str, **kwargs: Any) -> Response:
        """PUT request."""
        return await self.request(uri, HTTPMethod.PUT, **kwargs)

    async def patch(self, uri: str, **kwargs: Any) -> Response:
        """PATCH request."""
        return await self.request(uri, HTTPMethod.PATCH, **kwargs)

    async def delete(self, uri: str, **kwargs: Any) -> Response:
        """DELETE request."""
        return await self.request(uri, HTTPMethod.DELETE, **kwargs)

    async def head(self, uri: str, **kwargs: Any) -> Response:
        """HEAD request."""
        return await self.request(uri, HTTPMethod.HEAD, **kwargs)

    async def options(self, uri: str, **kwargs: Any) -> Response:
        """OPTIONS request."""
        return await self.request(uri, HTTPMethod.OPTIONS, **kwargs)

    async def _get_transport(self, scheme: str) -> Any:
        """Get or create transport for scheme.

        Raises:
            TransportCacheEvictedError: If transport was evicted due to failures
        """

        def _factory(s: str) -> Any:
            """Factory to create transport from registry."""
            return get_transport(f"{s}://example.com")

        return await self._cache.get_or_create(scheme, _factory)

    async def __aenter__(self) -> UniversalClient:
        """Context manager entry."""
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Context manager exit - cleanup all transports."""
        transports = self._cache.clear()
        for transport in transports.values():
            try:
                await transport.disconnect()
            except Exception as e:
                log.error(f"Error disconnecting transport: {e}")

    def reset_transport_cache(self) -> None:
        """Reset the transport cache.

        Useful for testing or forcing reconnection after configuration changes.
        """
        log.info("🔄 Resetting transport cache")
        self._cache.clear()


# Global client instance for convenience functions
_default_client: UniversalClient | None = None


def get_default_client() -> UniversalClient:
    """Get or create the default client instance.

    This function acts as the composition root for the default client,
    preserving backward compatibility for public convenience functions.
    """
    global _default_client
    if _default_client is None:
        _default_client = UniversalClient(hub=get_hub())
    return _default_client


async def request(uri: str, method: str | HTTPMethod = HTTPMethod.GET, **kwargs: Any) -> Response:
    """Make a request using the default client."""
    client = get_default_client()
    return await client.request(uri, method, **kwargs)


async def get(uri: str, **kwargs: Any) -> Response:
    """GET request using default client."""
    client = get_default_client()
    return await client.get(uri, **kwargs)


async def post(uri: str, **kwargs: Any) -> Response:
    """POST request using default client."""
    client = get_default_client()
    return await client.post(uri, **kwargs)


async def put(uri: str, **kwargs: Any) -> Response:
    """PUT request using default client."""
    client = get_default_client()
    return await client.put(uri, **kwargs)


async def patch(uri: str, **kwargs: Any) -> Response:
    """PATCH request using default client."""
    client = get_default_client()
    return await client.patch(uri, **kwargs)


async def delete(uri: str, **kwargs: Any) -> Response:
    """DELETE request using default client."""
    client = get_default_client()
    return await client.delete(uri, **kwargs)


async def head(uri: str, **kwargs: Any) -> Response:
    """HEAD request using default client."""
    client = get_default_client()
    return await client.head(uri, **kwargs)


async def options(uri: str, **kwargs: Any) -> Response:
    """OPTIONS request using default client."""
    client = get_default_client()
    return await client.options(uri, **kwargs)


async def stream(uri: str, **kwargs: Any) -> AsyncIterator[bytes]:
    """Stream data using default client."""
    client = get_default_client()
    async for chunk in client.stream(uri, **kwargs):
        yield chunk


__all__ = [
    "UniversalClient",
    "delete",
    "get",
    "get_default_client",
    "head",
    "options",
    "patch",
    "post",
    "put",
    "request",
    "stream",
]
EOF

log_update "Updating: provide/foundation/transport/middleware.py"
mkdir -p provide/foundation/transport/
cat <<'EOF' > provide/foundation/transport/middleware.py
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
import time
from typing import Any

from attrs import define, field

from provide.foundation.hub import get_component_registry
from provide.foundation.logger import get_logger
from provide.foundation.metrics import counter, histogram
from provide.foundation.resilience.retry import (
    BackoffStrategy,
    RetryExecutor,
    RetryPolicy,
)
from provide.foundation.security import sanitize_headers, sanitize_uri
from provide.foundation.transport.base import Request, Response
from provide.foundation.transport.defaults import (
    DEFAULT_TRANSPORT_LOG_BODIES,
    DEFAULT_TRANSPORT_LOG_REQUESTS,
    DEFAULT_TRANSPORT_LOG_RESPONSES,
)
from provide.foundation.transport.errors import TransportError

"""Transport middleware system with Hub registration."""

log = get_logger(__name__)


class Middleware(ABC):
    """Abstract base class for transport middleware."""

    @abstractmethod
    async def process_request(self, request: Request) -> Request:
        """Process request before sending."""

    @abstractmethod
    async def process_response(self, response: Response) -> Response:
        """Process response after receiving."""

    @abstractmethod
    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Process errors during request."""


@define(slots=True)
class LoggingMiddleware(Middleware):
    """Built-in telemetry middleware using foundation.logger."""

    log_requests: bool = field(default=DEFAULT_TRANSPORT_LOG_REQUESTS)
    log_responses: bool = field(default=DEFAULT_TRANSPORT_LOG_RESPONSES)
    log_bodies: bool = field(default=DEFAULT_TRANSPORT_LOG_BODIES)
    sanitize_logs: bool = field(default=True)

    async def process_request(self, request: Request) -> Request:
        """Log outgoing request."""
        if self.log_requests:
            # Sanitize URI and headers if enabled
            uri_str = str(request.uri)
            if self.sanitize_logs:
                uri_str = sanitize_uri(uri_str)
                headers = sanitize_headers(dict(request.headers)) if hasattr(request, "headers") else {}
            else:
                headers = dict(request.headers) if hasattr(request, "headers") else {}

            log.info(
                f"🚀 {request.method} {uri_str}",
                method=request.method,
                uri=uri_str,
                headers=headers,
            )

            if self.log_bodies and request.body:
                # Truncate request body to prevent logging secrets/PII
                body_str = str(request.body) if not isinstance(request.body, str) else request.body
                log.trace(
                    "Request body",
                    body=body_str[:500],  # Truncate large bodies (matches response behavior)
                    method=request.method,
                    uri=uri_str,
                )

        return request

    async def process_response(self, response: Response) -> Response:
        """Log incoming response."""
        if self.log_responses:
            # Sanitize URI and headers if enabled
            uri_str = str(response.request.uri) if response.request else None
            if self.sanitize_logs and uri_str:
                uri_str = sanitize_uri(uri_str)
                headers = sanitize_headers(dict(response.headers)) if hasattr(response, "headers") else {}
            else:
                headers = dict(response.headers) if hasattr(response, "headers") else {}

            status_emoji = self._get_status_emoji(response.status)
            log.info(
                f"{status_emoji} {response.status} ({response.elapsed_ms:.0f}ms)",
                status_code=response.status,
                elapsed_ms=response.elapsed_ms,
                method=response.request.method if response.request else None,
                uri=uri_str,
                headers=headers,
            )

            if self.log_bodies and response.body:
                log.trace(
                    "Response body",
                    body=response.text[:500],  # Truncate large bodies
                    status_code=response.status,
                    method=response.request.method if response.request else None,
                    uri=uri_str,
                )

        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Log errors."""
        # Sanitize URI if enabled
        uri_str = str(request.uri)
        if self.sanitize_logs:
            uri_str = sanitize_uri(uri_str)

        log.error(
            f"❌ {request.method} {uri_str} failed: {error}",
            method=request.method,
            uri=uri_str,
            error_type=error.__class__.__name__,
            error_message=str(error),
        )
        return error

    def _get_status_emoji(self, status_code: int) -> str:
        """Get emoji for status code."""
        if 200 <= status_code < 300:
            return "✅"
        if 300 <= status_code < 400:
            return "↩️"
        if 400 <= status_code < 500:
            return "⚠️"
        if 500 <= status_code < 600:
            return "❌"
        return "❓"


@define(slots=True)
class RetryMiddleware(Middleware):
    """Automatic retry middleware using unified retry logic."""

    policy: RetryPolicy = field(
        factory=lambda: RetryPolicy(
            max_attempts=3,
            base_delay=0.5,
            backoff=BackoffStrategy.EXPONENTIAL,
            retryable_errors=(TransportError,),
            retryable_status_codes={500, 502, 503, 504},
        ),
    )
    time_source: Callable[[], float] | None = field(default=None)
    async_sleep_func: Callable[[float], Awaitable[None]] | None = field(default=None)

    async def process_request(self, request: Request) -> Request:
        """No request processing needed."""
        return request

    async def process_response(self, response: Response) -> Response:
        """No response processing needed (retries handled in execute)."""
        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Handle error, potentially with retries (this is called by client)."""
        return error

    async def execute_with_retry(
        self, execute_func: Callable[[Request], Awaitable[Response]], request: Request
    ) -> Response:
        """Execute request with retry logic using unified RetryExecutor."""
        executor = RetryExecutor(
            self.policy,
            time_source=self.time_source,
            async_sleep_func=self.async_sleep_func,
        )

        async def wrapped() -> Response:
            response = await execute_func(request)

            # Check if status code is retryable
            if self.policy.should_retry_response(response, attempt=1):
                # Convert to exception for executor to handle
                raise TransportError(f"Retryable HTTP status: {response.status}")

            return response

        try:
            return await executor.execute_async(wrapped)
        except TransportError as e:
            # If it's our synthetic error, extract the response
            if "Retryable HTTP status" in str(e):
                # The last response will be returned
                # For now, re-raise as this needs more sophisticated handling
                raise
            raise


@define(slots=True)
class MetricsMiddleware(Middleware):
    """Middleware for collecting transport metrics using foundation.metrics."""

    _counter_func: Callable = field(default=counter)
    _histogram_func: Callable = field(default=histogram)

    # Create metrics instances
    _request_counter: Any = field(init=False)
    _request_duration: Any = field(init=False)
    _error_counter: Any = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Initialize metrics after creation."""
        self._request_counter = self._counter_func(
            "transport_requests_total",
            description="Total number of transport requests",
            unit="requests",
        )
        self._request_duration = self._histogram_func(
            "transport_request_duration_seconds",
            description="Duration of transport requests",
            unit="seconds",
        )
        self._error_counter = self._counter_func(
            "transport_errors_total",
            description="Total number of transport errors",
            unit="errors",
        )

    async def process_request(self, request: Request) -> Request:
        """Record request start time."""
        request.metadata["start_time"] = time.perf_counter()
        return request

    async def process_response(self, response: Response) -> Response:
        """Record response metrics."""
        if response.request and "start_time" in response.request.metadata:
            start_time = response.request.metadata["start_time"]
            duration = time.perf_counter() - start_time

            method = response.request.method
            status_class = f"{response.status // 100}xx"

            # Record metrics with labels
            self._request_counter.inc(
                1,
                method=method,
                status_code=str(response.status),
                status_class=status_class,
            )

            self._request_duration.observe(duration, method=method, status_class=status_class)

        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Record error metrics."""
        method = request.method
        error_type = error.__class__.__name__

        self._error_counter.inc(1, method=method, error_type=error_type)

        return error


@define(slots=True)
class MiddlewarePipeline:
    """Pipeline for executing middleware in order."""

    middleware: list[Middleware] = field(factory=list)

    def add(self, middleware: Middleware) -> None:
        """Add middleware to the pipeline."""
        self.middleware.append(middleware)
        log.trace(f"Added middleware: {middleware.__class__.__name__}")

    def remove(self, middleware_class: type[Middleware]) -> bool:
        """Remove middleware by class type."""
        for i, mw in enumerate(self.middleware):
            if isinstance(mw, middleware_class):
                del self.middleware[i]
                log.trace(f"Removed middleware: {middleware_class.__name__}")
                return True
        return False

    async def process_request(self, request: Request) -> Request:
        """Process request through all middleware."""
        for mw in self.middleware:
            request = await mw.process_request(request)
        return request

    async def process_response(self, response: Response) -> Response:
        """Process response through all middleware (in reverse order)."""
        for mw in reversed(self.middleware):
            response = await mw.process_response(response)
        return response

    async def process_error(self, error: Exception, request: Request) -> Exception:
        """Process error through all middleware."""
        for mw in self.middleware:
            error = await mw.process_error(error, request)
        return error


def register_middleware(
    name: str,
    middleware_class: type[Middleware],
    category: str = "transport.middleware",
    **metadata: str | int | bool | None,
) -> None:
    """Register middleware in the Hub."""
    registry = get_component_registry()

    registry.register(
        name=name,
        value=middleware_class,
        dimension=category,
        metadata={
            "category": category,
            "priority": metadata.get("priority", 100),
            "class_name": middleware_class.__name__,
            **metadata,
        },
        replace=True,
    )

    # Defer logging to avoid stderr output during module import
    # which breaks Terraform's go-plugin handshake protocol
    # The registry.register() call above already handles the registration
    # Logging can be enabled later if needed via trace level


def get_middleware_by_category(
    category: str = "transport.middleware",
) -> list[type[Middleware]]:
    """Get all middleware for a category, sorted by priority."""
    registry = get_component_registry()
    middleware = []

    for entry in registry:
        if entry.dimension == category:
            priority = entry.metadata.get("priority", 100)
            middleware.append((entry.value, priority))

    # Sort by priority (lower numbers = higher priority)
    middleware.sort(key=lambda x: x[1])
    return [mw[0] for mw in middleware]


def create_default_pipeline(
    enable_retry: bool = True,
    enable_logging: bool = True,
    enable_metrics: bool = True,
) -> MiddlewarePipeline:
    """Create pipeline with default middleware.

    Args:
        enable_retry: Enable automatic retry middleware (default: True)
        enable_logging: Enable request/response logging middleware (default: True)
        enable_metrics: Enable metrics collection middleware (default: True)

    Returns:
        Configured middleware pipeline

    """
    pipeline = MiddlewarePipeline()

    # Add retry middleware first (so retries happen before logging each attempt)
    if enable_retry:
        # Use sensible retry defaults
        retry_policy = RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.EXPONENTIAL,
            base_delay=1.0,
            max_delay=10.0,
            # Retry on common transient failures
            retryable_status_codes={408, 429, 500, 502, 503, 504},
        )
        pipeline.add(RetryMiddleware(policy=retry_policy))

    # Add built-in middleware
    if enable_logging:
        pipeline.add(LoggingMiddleware())

    if enable_metrics:
        pipeline.add(MetricsMiddleware())

    return pipeline


# Auto-register built-in middleware
def _register_builtin_middleware() -> None:
    """Register built-in middleware with the Hub."""
    try:
        register_middleware(
            "logging",
            LoggingMiddleware,
            description="Built-in request/response logging",
            priority=10,
        )

        register_middleware(
            "retry",
            RetryMiddleware,
            description="Automatic retry with exponential backoff",
            priority=20,
        )

        register_middleware(
            "metrics",
            MetricsMiddleware,
            description="Request/response metrics collection",
            priority=30,
        )

    except ImportError:
        # Registry not available yet
        pass


# Register when module is imported
_register_builtin_middleware()


__all__ = [
    "LoggingMiddleware",
    "MetricsMiddleware",
    "Middleware",
    "MiddlewarePipeline",
    "RetryMiddleware",
    "create_default_pipeline",
    "get_middleware_by_category",
    "register_middleware",
]
EOF

log_success "Project update complete."