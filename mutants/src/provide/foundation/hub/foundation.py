# provide/foundation/hub/foundation.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class FoundationManager:
    """Manages Foundation system initialization and lifecycle."""

    def xǁFoundationManagerǁ__init____mutmut_orig(self, hub: Hub, registry: Registry) -> None:
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

    def xǁFoundationManagerǁ__init____mutmut_1(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = None
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_2(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = None
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_3(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = None
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_4(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = True
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_5(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = ""
        self._logger_instance: FoundationLogger | None = None
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_6(self, hub: Hub, registry: Registry) -> None:
        """Initialize Foundation manager.

        Args:
            hub: The parent Hub instance for context
            registry: Component registry for storing Foundation state
        """
        self._hub = hub
        self._registry = registry
        self._initialized = False
        self._config: TelemetryConfig | None = None
        self._logger_instance: FoundationLogger | None = ""
        self._init_lock = threading.Lock()

    def xǁFoundationManagerǁ__init____mutmut_7(self, hub: Hub, registry: Registry) -> None:
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
        self._init_lock = None

    xǁFoundationManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁ__init____mutmut_1": xǁFoundationManagerǁ__init____mutmut_1,
        "xǁFoundationManagerǁ__init____mutmut_2": xǁFoundationManagerǁ__init____mutmut_2,
        "xǁFoundationManagerǁ__init____mutmut_3": xǁFoundationManagerǁ__init____mutmut_3,
        "xǁFoundationManagerǁ__init____mutmut_4": xǁFoundationManagerǁ__init____mutmut_4,
        "xǁFoundationManagerǁ__init____mutmut_5": xǁFoundationManagerǁ__init____mutmut_5,
        "xǁFoundationManagerǁ__init____mutmut_6": xǁFoundationManagerǁ__init____mutmut_6,
        "xǁFoundationManagerǁ__init____mutmut_7": xǁFoundationManagerǁ__init____mutmut_7,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁFoundationManagerǁ__init____mutmut_orig)
    xǁFoundationManagerǁ__init____mutmut_orig.__name__ = "xǁFoundationManagerǁ__init__"

    def xǁFoundationManagerǁinitialize_foundation__mutmut_orig(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_1(
        self, config: Any = None, force: bool = True
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_2(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and self._config is not None
            or getattr(self._config, "service_name", "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_3(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and not force
            or self._config is not None  # Have existing config to check
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_4(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and self._initialized
            or not force  # User didn't explicitly set force
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_5(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            config is not None
            or self._initialized  # Already initialized (likely auto-init)
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_6(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            config is None  # Explicit config provided
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_7(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and force  # User didn't explicitly set force
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_8(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and self._config is None  # Have existing config to check
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_9(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(None, "service_name", "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_10(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, None, "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_11(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "service_name", None) is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_12(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr("service_name", "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_13(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_14(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(
                self._config,
                "service_name",
            )
            is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_15(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "XXservice_nameXX", "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_16(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "SERVICE_NAME", "not-none") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_17(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "service_name", "XXnot-noneXX") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_18(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "service_name", "NOT-NONE") is None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_19(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            and getattr(self._config, "service_name", "not-none") is not None  # Auto-init indicator
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_20(
        self, config: Any = None, force: bool = False
    ) -> None:
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
            otlp_configured = None

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_21(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                and getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_22(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(None, "otlp_endpoint", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_23(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, None, None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_24(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr("otlp_endpoint", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_25(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, None) is not None or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_26(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(
                    self._config,
                    "otlp_endpoint",
                )
                is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_27(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, "XXotlp_endpointXX", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_28(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, "OTLP_ENDPOINT", None) is not None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_29(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, "otlp_endpoint", None) is None
                or getattr(config, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_30(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(None, "otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_31(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(config, None, None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_32(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr("otlp_endpoint", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_33(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                getattr(self._config, "otlp_endpoint", None) is not None or getattr(config, None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_34(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(
                    config,
                    "otlp_endpoint",
                )
                is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_35(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(config, "XXotlp_endpointXX", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_36(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(config, "OTLP_ENDPOINT", None) is not None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_37(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                or getattr(config, "otlp_endpoint", None) is None
            )

            # Use system logger for init-time logging (safe during Foundation setup)
            from provide.foundation.logger.setup.coordinator import get_system_logger

            setup_log = get_system_logger("provide.foundation.hub.init")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_38(
        self, config: Any = None, force: bool = False
    ) -> None:
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

            setup_log = None

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_39(
        self, config: Any = None, force: bool = False
    ) -> None:
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

            setup_log = get_system_logger(None)

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_40(
        self, config: Any = None, force: bool = False
    ) -> None:
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

            setup_log = get_system_logger("XXprovide.foundation.hub.initXX")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_41(
        self, config: Any = None, force: bool = False
    ) -> None:
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

            setup_log = get_system_logger("PROVIDE.FOUNDATION.HUB.INIT")

            if otlp_configured:
                # Force full re-initialization to recreate LoggerProvider with new service_name
                force = True
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_42(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                force = None
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_43(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                force = False
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_44(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    None
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_45(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "XXFoundation: Re-initializing with OTLP (explicit service_name overriding auto-init)XX"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_46(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "foundation: re-initializing with otlp (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_47(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "FOUNDATION: RE-INITIALIZING WITH OTLP (EXPLICIT SERVICE_NAME OVERRIDING AUTO-INIT)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_48(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = None

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_49(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(None, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_50(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, None):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_51(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_52(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(
                    self._registry,
                ):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_53(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = None
                    setup_log.info(  # type: ignore[attr-defined]
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_54(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        None
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_55(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "XXFoundation: Updated config (explicit service_name overriding auto-init default)XX"
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_56(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "foundation: updated config (explicit service_name overriding auto-init default)"
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_57(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "FOUNDATION: UPDATED CONFIG (EXPLICIT SERVICE_NAME OVERRIDING AUTO-INIT DEFAULT)"
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_58(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = None

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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_59(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = None

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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_60(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=None, config=config, force=force
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_61(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry, config=None, force=force
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_62(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry, config=config, force=None
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_63(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(config=config, force=force)

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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_64(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry, force=force
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_65(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
                        "Foundation: Updated config (explicit service_name overriding auto-init default)"
                    )
                    return
                # If lightweight update failed, fall through to normal initialization

        # Use the new simplified coordinator
        from provide.foundation.hub.initialization import get_initialization_coordinator

        coordinator = get_initialization_coordinator()

        actual_config, logger_instance = coordinator.initialize_foundation(
            registry=self._registry,
            config=config,
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_66(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
        self._config = None
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_67(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
        self._logger_instance = None
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

    def xǁFoundationManagerǁinitialize_foundation__mutmut_68(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
        self._initialized = None

        # Log initialization success (avoid test interference)
        import os

        if not os.environ.get("PYTEST_CURRENT_TEST"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_69(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
        self._initialized = False

        # Log initialization success (avoid test interference)
        import os

        if not os.environ.get("PYTEST_CURRENT_TEST"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_70(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

        if os.environ.get("PYTEST_CURRENT_TEST"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_71(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

        if not os.environ.get(None):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_72(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

        if not os.environ.get("XXPYTEST_CURRENT_TESTXX"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_73(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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

        if not os.environ.get("pytest_current_test"):
            logger = self._get_logger()
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_74(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
            logger = None
            if logger:
                logger.info(
                    "Foundation initialized through Hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_75(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    None,
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_76(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source=None,
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_77(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_78(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_79(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    "XXFoundation initialized through HubXX",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_80(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    "foundation initialized through hub",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_81(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    "FOUNDATION INITIALIZED THROUGH HUB",
                    config_source="explicit" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_82(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source="XXexplicitXX" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_83(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source="EXPLICIT" if config else "environment",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_84(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source="explicit" if config else "XXenvironmentXX",
                )

    def xǁFoundationManagerǁinitialize_foundation__mutmut_85(
        self, config: Any = None, force: bool = False
    ) -> None:
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
                setup_log.info(  # type: ignore[attr-defined]
                    "Foundation: Re-initializing with OTLP (explicit service_name overriding auto-init)"
                )
            else:
                # Try lightweight config update (avoids expensive re-initialization)
                from provide.foundation.hub.initialization import get_initialization_coordinator

                coordinator = get_initialization_coordinator()

                if coordinator.update_config_if_default(self._registry, config):
                    # Config updated successfully - no need to re-initialize
                    self._config = config
                    setup_log.info(  # type: ignore[attr-defined]
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
                    config_source="explicit" if config else "ENVIRONMENT",
                )

    xǁFoundationManagerǁinitialize_foundation__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁinitialize_foundation__mutmut_1": xǁFoundationManagerǁinitialize_foundation__mutmut_1,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_2": xǁFoundationManagerǁinitialize_foundation__mutmut_2,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_3": xǁFoundationManagerǁinitialize_foundation__mutmut_3,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_4": xǁFoundationManagerǁinitialize_foundation__mutmut_4,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_5": xǁFoundationManagerǁinitialize_foundation__mutmut_5,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_6": xǁFoundationManagerǁinitialize_foundation__mutmut_6,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_7": xǁFoundationManagerǁinitialize_foundation__mutmut_7,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_8": xǁFoundationManagerǁinitialize_foundation__mutmut_8,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_9": xǁFoundationManagerǁinitialize_foundation__mutmut_9,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_10": xǁFoundationManagerǁinitialize_foundation__mutmut_10,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_11": xǁFoundationManagerǁinitialize_foundation__mutmut_11,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_12": xǁFoundationManagerǁinitialize_foundation__mutmut_12,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_13": xǁFoundationManagerǁinitialize_foundation__mutmut_13,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_14": xǁFoundationManagerǁinitialize_foundation__mutmut_14,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_15": xǁFoundationManagerǁinitialize_foundation__mutmut_15,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_16": xǁFoundationManagerǁinitialize_foundation__mutmut_16,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_17": xǁFoundationManagerǁinitialize_foundation__mutmut_17,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_18": xǁFoundationManagerǁinitialize_foundation__mutmut_18,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_19": xǁFoundationManagerǁinitialize_foundation__mutmut_19,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_20": xǁFoundationManagerǁinitialize_foundation__mutmut_20,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_21": xǁFoundationManagerǁinitialize_foundation__mutmut_21,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_22": xǁFoundationManagerǁinitialize_foundation__mutmut_22,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_23": xǁFoundationManagerǁinitialize_foundation__mutmut_23,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_24": xǁFoundationManagerǁinitialize_foundation__mutmut_24,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_25": xǁFoundationManagerǁinitialize_foundation__mutmut_25,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_26": xǁFoundationManagerǁinitialize_foundation__mutmut_26,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_27": xǁFoundationManagerǁinitialize_foundation__mutmut_27,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_28": xǁFoundationManagerǁinitialize_foundation__mutmut_28,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_29": xǁFoundationManagerǁinitialize_foundation__mutmut_29,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_30": xǁFoundationManagerǁinitialize_foundation__mutmut_30,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_31": xǁFoundationManagerǁinitialize_foundation__mutmut_31,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_32": xǁFoundationManagerǁinitialize_foundation__mutmut_32,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_33": xǁFoundationManagerǁinitialize_foundation__mutmut_33,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_34": xǁFoundationManagerǁinitialize_foundation__mutmut_34,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_35": xǁFoundationManagerǁinitialize_foundation__mutmut_35,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_36": xǁFoundationManagerǁinitialize_foundation__mutmut_36,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_37": xǁFoundationManagerǁinitialize_foundation__mutmut_37,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_38": xǁFoundationManagerǁinitialize_foundation__mutmut_38,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_39": xǁFoundationManagerǁinitialize_foundation__mutmut_39,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_40": xǁFoundationManagerǁinitialize_foundation__mutmut_40,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_41": xǁFoundationManagerǁinitialize_foundation__mutmut_41,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_42": xǁFoundationManagerǁinitialize_foundation__mutmut_42,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_43": xǁFoundationManagerǁinitialize_foundation__mutmut_43,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_44": xǁFoundationManagerǁinitialize_foundation__mutmut_44,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_45": xǁFoundationManagerǁinitialize_foundation__mutmut_45,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_46": xǁFoundationManagerǁinitialize_foundation__mutmut_46,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_47": xǁFoundationManagerǁinitialize_foundation__mutmut_47,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_48": xǁFoundationManagerǁinitialize_foundation__mutmut_48,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_49": xǁFoundationManagerǁinitialize_foundation__mutmut_49,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_50": xǁFoundationManagerǁinitialize_foundation__mutmut_50,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_51": xǁFoundationManagerǁinitialize_foundation__mutmut_51,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_52": xǁFoundationManagerǁinitialize_foundation__mutmut_52,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_53": xǁFoundationManagerǁinitialize_foundation__mutmut_53,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_54": xǁFoundationManagerǁinitialize_foundation__mutmut_54,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_55": xǁFoundationManagerǁinitialize_foundation__mutmut_55,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_56": xǁFoundationManagerǁinitialize_foundation__mutmut_56,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_57": xǁFoundationManagerǁinitialize_foundation__mutmut_57,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_58": xǁFoundationManagerǁinitialize_foundation__mutmut_58,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_59": xǁFoundationManagerǁinitialize_foundation__mutmut_59,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_60": xǁFoundationManagerǁinitialize_foundation__mutmut_60,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_61": xǁFoundationManagerǁinitialize_foundation__mutmut_61,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_62": xǁFoundationManagerǁinitialize_foundation__mutmut_62,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_63": xǁFoundationManagerǁinitialize_foundation__mutmut_63,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_64": xǁFoundationManagerǁinitialize_foundation__mutmut_64,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_65": xǁFoundationManagerǁinitialize_foundation__mutmut_65,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_66": xǁFoundationManagerǁinitialize_foundation__mutmut_66,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_67": xǁFoundationManagerǁinitialize_foundation__mutmut_67,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_68": xǁFoundationManagerǁinitialize_foundation__mutmut_68,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_69": xǁFoundationManagerǁinitialize_foundation__mutmut_69,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_70": xǁFoundationManagerǁinitialize_foundation__mutmut_70,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_71": xǁFoundationManagerǁinitialize_foundation__mutmut_71,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_72": xǁFoundationManagerǁinitialize_foundation__mutmut_72,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_73": xǁFoundationManagerǁinitialize_foundation__mutmut_73,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_74": xǁFoundationManagerǁinitialize_foundation__mutmut_74,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_75": xǁFoundationManagerǁinitialize_foundation__mutmut_75,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_76": xǁFoundationManagerǁinitialize_foundation__mutmut_76,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_77": xǁFoundationManagerǁinitialize_foundation__mutmut_77,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_78": xǁFoundationManagerǁinitialize_foundation__mutmut_78,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_79": xǁFoundationManagerǁinitialize_foundation__mutmut_79,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_80": xǁFoundationManagerǁinitialize_foundation__mutmut_80,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_81": xǁFoundationManagerǁinitialize_foundation__mutmut_81,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_82": xǁFoundationManagerǁinitialize_foundation__mutmut_82,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_83": xǁFoundationManagerǁinitialize_foundation__mutmut_83,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_84": xǁFoundationManagerǁinitialize_foundation__mutmut_84,
        "xǁFoundationManagerǁinitialize_foundation__mutmut_85": xǁFoundationManagerǁinitialize_foundation__mutmut_85,
    }

    def initialize_foundation(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁinitialize_foundation__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁinitialize_foundation__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    initialize_foundation.__signature__ = _mutmut_signature(
        xǁFoundationManagerǁinitialize_foundation__mutmut_orig
    )
    xǁFoundationManagerǁinitialize_foundation__mutmut_orig.__name__ = (
        "xǁFoundationManagerǁinitialize_foundation"
    )

    def xǁFoundationManagerǁget_foundation_logger__mutmut_orig(self, name: str | None = None) -> Any:
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

    def xǁFoundationManagerǁget_foundation_logger__mutmut_1(self, name: str | None = None) -> Any:
        """Get Foundation logger instance through Hub.

        Auto-initializes Foundation if not already done.
        Thread-safe with fallback behavior.

        Args:
            name: Logger name (e.g., module name)

        Returns:
            Configured logger instance

        """
        # Ensure Foundation is initialized
        if self._initialized:
            self.initialize_foundation()

        # Get logger instance from registry
        logger_instance = self._registry.get("foundation.logger.instance", "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_2(self, name: str | None = None) -> Any:
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
        logger_instance = None

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_3(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get(None, "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_4(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("foundation.logger.instance", None)

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_5(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_6(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get(
            "foundation.logger.instance",
        )

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_7(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("XXfoundation.logger.instanceXX", "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_8(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("FOUNDATION.LOGGER.INSTANCE", "singleton")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_9(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("foundation.logger.instance", "XXsingletonXX")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_10(self, name: str | None = None) -> Any:
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
        logger_instance = self._registry.get("foundation.logger.instance", "SINGLETON")

        if logger_instance:
            return logger_instance.get_logger(name)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_11(self, name: str | None = None) -> Any:
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
            return logger_instance.get_logger(None)

        # Emergency fallback if logger instance not available
        import structlog

        return structlog.get_logger(name or "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_12(self, name: str | None = None) -> Any:
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

        return structlog.get_logger(None)

    def xǁFoundationManagerǁget_foundation_logger__mutmut_13(self, name: str | None = None) -> Any:
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

        return structlog.get_logger(name and "fallback")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_14(self, name: str | None = None) -> Any:
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

        return structlog.get_logger(name or "XXfallbackXX")

    def xǁFoundationManagerǁget_foundation_logger__mutmut_15(self, name: str | None = None) -> Any:
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

        return structlog.get_logger(name or "FALLBACK")

    xǁFoundationManagerǁget_foundation_logger__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁget_foundation_logger__mutmut_1": xǁFoundationManagerǁget_foundation_logger__mutmut_1,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_2": xǁFoundationManagerǁget_foundation_logger__mutmut_2,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_3": xǁFoundationManagerǁget_foundation_logger__mutmut_3,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_4": xǁFoundationManagerǁget_foundation_logger__mutmut_4,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_5": xǁFoundationManagerǁget_foundation_logger__mutmut_5,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_6": xǁFoundationManagerǁget_foundation_logger__mutmut_6,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_7": xǁFoundationManagerǁget_foundation_logger__mutmut_7,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_8": xǁFoundationManagerǁget_foundation_logger__mutmut_8,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_9": xǁFoundationManagerǁget_foundation_logger__mutmut_9,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_10": xǁFoundationManagerǁget_foundation_logger__mutmut_10,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_11": xǁFoundationManagerǁget_foundation_logger__mutmut_11,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_12": xǁFoundationManagerǁget_foundation_logger__mutmut_12,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_13": xǁFoundationManagerǁget_foundation_logger__mutmut_13,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_14": xǁFoundationManagerǁget_foundation_logger__mutmut_14,
        "xǁFoundationManagerǁget_foundation_logger__mutmut_15": xǁFoundationManagerǁget_foundation_logger__mutmut_15,
    }

    def get_foundation_logger(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁget_foundation_logger__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁget_foundation_logger__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_foundation_logger.__signature__ = _mutmut_signature(
        xǁFoundationManagerǁget_foundation_logger__mutmut_orig
    )
    xǁFoundationManagerǁget_foundation_logger__mutmut_orig.__name__ = (
        "xǁFoundationManagerǁget_foundation_logger"
    )

    def is_foundation_initialized(self) -> bool:
        """Check if Foundation system is initialized."""
        return self._initialized

    def xǁFoundationManagerǁget_foundation_config__mutmut_orig(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_1(self) -> Any | None:
        """Get the current Foundation configuration."""
        if self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_2(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get(None, "singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_3(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", None)

    def xǁFoundationManagerǁget_foundation_config__mutmut_4(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_5(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get(
            "foundation.config",
        )

    def xǁFoundationManagerǁget_foundation_config__mutmut_6(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("XXfoundation.configXX", "singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_7(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("FOUNDATION.CONFIG", "singleton")

    def xǁFoundationManagerǁget_foundation_config__mutmut_8(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "XXsingletonXX")

    def xǁFoundationManagerǁget_foundation_config__mutmut_9(self) -> Any | None:
        """Get the current Foundation configuration."""
        if not self._initialized:
            self.initialize_foundation()

        # Return the local config if available
        if self._config:
            return self._config

        # Otherwise get from registry
        return self._registry.get("foundation.config", "SINGLETON")

    xǁFoundationManagerǁget_foundation_config__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁget_foundation_config__mutmut_1": xǁFoundationManagerǁget_foundation_config__mutmut_1,
        "xǁFoundationManagerǁget_foundation_config__mutmut_2": xǁFoundationManagerǁget_foundation_config__mutmut_2,
        "xǁFoundationManagerǁget_foundation_config__mutmut_3": xǁFoundationManagerǁget_foundation_config__mutmut_3,
        "xǁFoundationManagerǁget_foundation_config__mutmut_4": xǁFoundationManagerǁget_foundation_config__mutmut_4,
        "xǁFoundationManagerǁget_foundation_config__mutmut_5": xǁFoundationManagerǁget_foundation_config__mutmut_5,
        "xǁFoundationManagerǁget_foundation_config__mutmut_6": xǁFoundationManagerǁget_foundation_config__mutmut_6,
        "xǁFoundationManagerǁget_foundation_config__mutmut_7": xǁFoundationManagerǁget_foundation_config__mutmut_7,
        "xǁFoundationManagerǁget_foundation_config__mutmut_8": xǁFoundationManagerǁget_foundation_config__mutmut_8,
        "xǁFoundationManagerǁget_foundation_config__mutmut_9": xǁFoundationManagerǁget_foundation_config__mutmut_9,
    }

    def get_foundation_config(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁget_foundation_config__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁget_foundation_config__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_foundation_config.__signature__ = _mutmut_signature(
        xǁFoundationManagerǁget_foundation_config__mutmut_orig
    )
    xǁFoundationManagerǁget_foundation_config__mutmut_orig.__name__ = (
        "xǁFoundationManagerǁget_foundation_config"
    )

    def xǁFoundationManagerǁclear_foundation_state__mutmut_orig(self) -> None:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_1(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = None
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_2(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = True
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_3(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = ""
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_4(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = ""

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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_5(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") or self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_6(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(None, "_registry") and self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_7(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, None) and self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_8(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr("_registry") and self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_9(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if (
            hasattr(
                self,
            )
            and self._registry
        ):
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_10(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "XX_registryXX") and self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_11(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_REGISTRY") and self._registry:
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

    def xǁFoundationManagerǁclear_foundation_state__mutmut_12(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(None):
                self._registry.remove("foundation.config", "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_13(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove(None, "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_14(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", None)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_15(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_16(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove(
                    "foundation.config",
                )
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_17(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("XXfoundation.configXX", "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_18(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("FOUNDATION.CONFIG", "singleton")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_19(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", "XXsingletonXX")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_20(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", "SINGLETON")
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_21(self) -> None:
        """Clear Foundation initialization state."""
        self._initialized = False
        self._config = None
        self._logger_instance = None

        # Clear Foundation config from registry to prevent stale state
        if hasattr(self, "_registry") and self._registry:
            # Remove foundation config entries that might have stale state (entry might not exist)
            with contextlib.suppress(Exception):
                self._registry.remove("foundation.config", "singleton")
            with contextlib.suppress(None):
                self._registry.remove("foundation.logger.instance", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_22(self) -> None:
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
                self._registry.remove(None, "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_23(self) -> None:
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
                self._registry.remove("foundation.logger.instance", None)

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_24(self) -> None:
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
                self._registry.remove("singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_25(self) -> None:
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
                self._registry.remove(
                    "foundation.logger.instance",
                )

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_26(self) -> None:
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
                self._registry.remove("XXfoundation.logger.instanceXX", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_27(self) -> None:
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
                self._registry.remove("FOUNDATION.LOGGER.INSTANCE", "singleton")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_28(self) -> None:
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
                self._registry.remove("foundation.logger.instance", "XXsingletonXX")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    def xǁFoundationManagerǁclear_foundation_state__mutmut_29(self) -> None:
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
                self._registry.remove("foundation.logger.instance", "SINGLETON")

        # Reset global coordinator state only in test mode
        from provide.foundation.testmode.detection import is_in_test_mode

        if is_in_test_mode():
            from provide.foundation.testmode.internal import reset_global_coordinator

            reset_global_coordinator()

    xǁFoundationManagerǁclear_foundation_state__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁclear_foundation_state__mutmut_1": xǁFoundationManagerǁclear_foundation_state__mutmut_1,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_2": xǁFoundationManagerǁclear_foundation_state__mutmut_2,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_3": xǁFoundationManagerǁclear_foundation_state__mutmut_3,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_4": xǁFoundationManagerǁclear_foundation_state__mutmut_4,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_5": xǁFoundationManagerǁclear_foundation_state__mutmut_5,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_6": xǁFoundationManagerǁclear_foundation_state__mutmut_6,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_7": xǁFoundationManagerǁclear_foundation_state__mutmut_7,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_8": xǁFoundationManagerǁclear_foundation_state__mutmut_8,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_9": xǁFoundationManagerǁclear_foundation_state__mutmut_9,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_10": xǁFoundationManagerǁclear_foundation_state__mutmut_10,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_11": xǁFoundationManagerǁclear_foundation_state__mutmut_11,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_12": xǁFoundationManagerǁclear_foundation_state__mutmut_12,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_13": xǁFoundationManagerǁclear_foundation_state__mutmut_13,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_14": xǁFoundationManagerǁclear_foundation_state__mutmut_14,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_15": xǁFoundationManagerǁclear_foundation_state__mutmut_15,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_16": xǁFoundationManagerǁclear_foundation_state__mutmut_16,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_17": xǁFoundationManagerǁclear_foundation_state__mutmut_17,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_18": xǁFoundationManagerǁclear_foundation_state__mutmut_18,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_19": xǁFoundationManagerǁclear_foundation_state__mutmut_19,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_20": xǁFoundationManagerǁclear_foundation_state__mutmut_20,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_21": xǁFoundationManagerǁclear_foundation_state__mutmut_21,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_22": xǁFoundationManagerǁclear_foundation_state__mutmut_22,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_23": xǁFoundationManagerǁclear_foundation_state__mutmut_23,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_24": xǁFoundationManagerǁclear_foundation_state__mutmut_24,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_25": xǁFoundationManagerǁclear_foundation_state__mutmut_25,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_26": xǁFoundationManagerǁclear_foundation_state__mutmut_26,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_27": xǁFoundationManagerǁclear_foundation_state__mutmut_27,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_28": xǁFoundationManagerǁclear_foundation_state__mutmut_28,
        "xǁFoundationManagerǁclear_foundation_state__mutmut_29": xǁFoundationManagerǁclear_foundation_state__mutmut_29,
    }

    def clear_foundation_state(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁclear_foundation_state__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁclear_foundation_state__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    clear_foundation_state.__signature__ = _mutmut_signature(
        xǁFoundationManagerǁclear_foundation_state__mutmut_orig
    )
    xǁFoundationManagerǁclear_foundation_state__mutmut_orig.__name__ = (
        "xǁFoundationManagerǁclear_foundation_state"
    )

    def xǁFoundationManagerǁ_get_logger__mutmut_orig(self) -> Any | None:
        """Get logger for internal use."""
        if self._logger_instance:
            return self._logger_instance.get_logger(__name__)

        # Fallback during initialization
        import structlog

        return structlog.get_logger(__name__)

    def xǁFoundationManagerǁ_get_logger__mutmut_1(self) -> Any | None:
        """Get logger for internal use."""
        if self._logger_instance:
            return self._logger_instance.get_logger(None)

        # Fallback during initialization
        import structlog

        return structlog.get_logger(__name__)

    def xǁFoundationManagerǁ_get_logger__mutmut_2(self) -> Any | None:
        """Get logger for internal use."""
        if self._logger_instance:
            return self._logger_instance.get_logger(__name__)

        # Fallback during initialization
        import structlog

        return structlog.get_logger(None)

    xǁFoundationManagerǁ_get_logger__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationManagerǁ_get_logger__mutmut_1": xǁFoundationManagerǁ_get_logger__mutmut_1,
        "xǁFoundationManagerǁ_get_logger__mutmut_2": xǁFoundationManagerǁ_get_logger__mutmut_2,
    }

    def _get_logger(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationManagerǁ_get_logger__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationManagerǁ_get_logger__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _get_logger.__signature__ = _mutmut_signature(xǁFoundationManagerǁ_get_logger__mutmut_orig)
    xǁFoundationManagerǁ_get_logger__mutmut_orig.__name__ = "xǁFoundationManagerǁ_get_logger"


def x_get_foundation_logger__mutmut_orig(name: str | None = None) -> Any:
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


def x_get_foundation_logger__mutmut_1(name: str | None = None) -> Any:
    """Get a logger from the Foundation system.

    This is the preferred way to get loggers instead of using _get_logger()
    patterns that create circular import issues.

    Args:
        name: Logger name (defaults to calling module)

    Returns:
        Logger instance
    """
    from provide.foundation.hub.manager import get_hub

    hub = None
    if hasattr(hub, "_foundation") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_2(name: str | None = None) -> Any:
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
    if hasattr(hub, "_foundation") or hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_3(name: str | None = None) -> Any:
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
    if hasattr(None, "_foundation") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_4(name: str | None = None) -> Any:
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
    if hasattr(hub, None) and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_5(name: str | None = None) -> Any:
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
    if hasattr("_foundation") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_6(name: str | None = None) -> Any:
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
    if (
        hasattr(
            hub,
        )
        and hub._foundation._logger_instance
    ):
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_7(name: str | None = None) -> Any:
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
    if hasattr(hub, "XX_foundationXX") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_8(name: str | None = None) -> Any:
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
    if hasattr(hub, "_FOUNDATION") and hub._foundation._logger_instance:
        return hub._foundation._logger_instance.get_logger(name)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_9(name: str | None = None) -> Any:
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
        return hub._foundation._logger_instance.get_logger(None)

    # Fallback to direct logger import during bootstrap
    from provide.foundation.logger import logger

    if name:
        return logger.get_logger(name)
    return logger


def x_get_foundation_logger__mutmut_10(name: str | None = None) -> Any:
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
        return logger.get_logger(None)
    return logger


x_get_foundation_logger__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_foundation_logger__mutmut_1": x_get_foundation_logger__mutmut_1,
    "x_get_foundation_logger__mutmut_2": x_get_foundation_logger__mutmut_2,
    "x_get_foundation_logger__mutmut_3": x_get_foundation_logger__mutmut_3,
    "x_get_foundation_logger__mutmut_4": x_get_foundation_logger__mutmut_4,
    "x_get_foundation_logger__mutmut_5": x_get_foundation_logger__mutmut_5,
    "x_get_foundation_logger__mutmut_6": x_get_foundation_logger__mutmut_6,
    "x_get_foundation_logger__mutmut_7": x_get_foundation_logger__mutmut_7,
    "x_get_foundation_logger__mutmut_8": x_get_foundation_logger__mutmut_8,
    "x_get_foundation_logger__mutmut_9": x_get_foundation_logger__mutmut_9,
    "x_get_foundation_logger__mutmut_10": x_get_foundation_logger__mutmut_10,
}


def get_foundation_logger(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_foundation_logger__mutmut_orig, x_get_foundation_logger__mutmut_mutants, args, kwargs
    )
    return result


get_foundation_logger.__signature__ = _mutmut_signature(x_get_foundation_logger__mutmut_orig)
x_get_foundation_logger__mutmut_orig.__name__ = "x_get_foundation_logger"


# <3 🧱🤝🌐🪄
