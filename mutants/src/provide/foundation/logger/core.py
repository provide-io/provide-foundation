# provide/foundation/logger/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# core.py
#
import contextlib
from typing import TYPE_CHECKING, Any

import structlog

from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.logger.types import TRACE_LEVEL_NAME

"""Core FoundationLogger implementation.
Contains the main logging class with all logging methods.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.config import TelemetryConfig

_LAZY_SETUP_STATE: dict[str, Any] = {"done": False, "error": None, "in_progress": False}
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


class FoundationLogger:
    """A `structlog`-based logger providing a standardized logging interface."""

    def xǁFoundationLoggerǁ__init____mutmut_orig(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_1(self, hub: Any = None) -> None:
        self._internal_logger = None
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_2(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=None,
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_3(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = None
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_4(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = True
        self._active_config: TelemetryConfig | None = None
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_5(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = ""
        self._hub = hub  # Hub dependency for DI pattern

    def xǁFoundationLoggerǁ__init____mutmut_6(self, hub: Any = None) -> None:
        self._internal_logger = structlog.get_logger().bind(
            logger_name=f"{self.__class__.__module__}.{self.__class__.__name__}",
        )
        self._is_configured_by_setup: bool = False
        self._active_config: TelemetryConfig | None = None
        self._hub = None  # Hub dependency for DI pattern

    xǁFoundationLoggerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ__init____mutmut_1": xǁFoundationLoggerǁ__init____mutmut_1,
        "xǁFoundationLoggerǁ__init____mutmut_2": xǁFoundationLoggerǁ__init____mutmut_2,
        "xǁFoundationLoggerǁ__init____mutmut_3": xǁFoundationLoggerǁ__init____mutmut_3,
        "xǁFoundationLoggerǁ__init____mutmut_4": xǁFoundationLoggerǁ__init____mutmut_4,
        "xǁFoundationLoggerǁ__init____mutmut_5": xǁFoundationLoggerǁ__init____mutmut_5,
        "xǁFoundationLoggerǁ__init____mutmut_6": xǁFoundationLoggerǁ__init____mutmut_6,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁFoundationLoggerǁ__init____mutmut_orig)
    xǁFoundationLoggerǁ__init____mutmut_orig.__name__ = "xǁFoundationLoggerǁ__init__"

    def xǁFoundationLoggerǁsetup__mutmut_orig(self, config: TelemetryConfig) -> None:
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

    def xǁFoundationLoggerǁsetup__mutmut_1(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = None
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_2(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = None

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_3(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = False

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_4(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(None, is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_5(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=None)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_6(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(is_explicit_call=True)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_7(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(
                config,
            )
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    def xǁFoundationLoggerǁsetup__mutmut_8(self, config: TelemetryConfig) -> None:
        """Setup the logger with configuration from Hub.

        Args:
            config: TelemetryConfig to use for setup

        """
        self._active_config = config
        self._is_configured_by_setup = True

        # Run the internal setup process
        try:
            from provide.foundation.logger.setup.coordinator import internal_setup

            internal_setup(config, is_explicit_call=False)
        except Exception as e:
            # Fallback to emergency setup if regular setup fails
            self._setup_emergency_fallback()
            raise e

    xǁFoundationLoggerǁsetup__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁsetup__mutmut_1": xǁFoundationLoggerǁsetup__mutmut_1,
        "xǁFoundationLoggerǁsetup__mutmut_2": xǁFoundationLoggerǁsetup__mutmut_2,
        "xǁFoundationLoggerǁsetup__mutmut_3": xǁFoundationLoggerǁsetup__mutmut_3,
        "xǁFoundationLoggerǁsetup__mutmut_4": xǁFoundationLoggerǁsetup__mutmut_4,
        "xǁFoundationLoggerǁsetup__mutmut_5": xǁFoundationLoggerǁsetup__mutmut_5,
        "xǁFoundationLoggerǁsetup__mutmut_6": xǁFoundationLoggerǁsetup__mutmut_6,
        "xǁFoundationLoggerǁsetup__mutmut_7": xǁFoundationLoggerǁsetup__mutmut_7,
        "xǁFoundationLoggerǁsetup__mutmut_8": xǁFoundationLoggerǁsetup__mutmut_8,
    }

    def setup(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁsetup__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁsetup__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    setup.__signature__ = _mutmut_signature(xǁFoundationLoggerǁsetup__mutmut_orig)
    xǁFoundationLoggerǁsetup__mutmut_orig.__name__ = "xǁFoundationLoggerǁsetup"

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_orig(self) -> bool:
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

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_1(self) -> bool:
        try:
            current_config = None
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

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_2(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config or isinstance(
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

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_3(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire(None):
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_4(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("XXfoundation.logger.lazyXX"):
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_5(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("FOUNDATION.LOGGER.LAZY"):
                    _LAZY_SETUP_STATE["done"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_6(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["done"] = None
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_7(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["XXdoneXX"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_8(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["DONE"] = True
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_9(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["done"] = False
                return True
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_10(self) -> bool:
        try:
            current_config = structlog.get_config()
            if current_config and isinstance(
                current_config.get("logger_factory"),
                structlog.ReturnLoggerFactory,
            ):
                with get_lock_manager().acquire("foundation.logger.lazy"):
                    _LAZY_SETUP_STATE["done"] = True
                return False
        except Exception:
            # Broad catch intentional: structlog config check may fail for various reasons
            # Return False to indicate we should continue with standard setup
            pass
        return False

    def xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_11(self) -> bool:
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
        return True

    xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_1": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_1,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_2": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_2,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_3": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_3,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_4": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_4,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_5": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_5,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_6": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_6,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_7": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_7,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_8": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_8,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_9": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_9,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_10": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_10,
        "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_11": xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_11,
    }

    def _check_structlog_already_disabled(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_orig"),
            object.__getattribute__(
                self, "xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    _check_structlog_already_disabled.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_orig
    )
    xǁFoundationLoggerǁ_check_structlog_already_disabled__mutmut_orig.__name__ = (
        "xǁFoundationLoggerǁ_check_structlog_already_disabled"
    )

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_orig(self) -> bool:
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

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_1(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is not None:
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

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_2(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return True

        try:
            # Use the injected hub instance to get config
            config = self._hub.get_foundation_config()
            if config and not self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_3(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return False

        try:
            # Use the injected hub instance to get config
            config = None
            if config and not self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_4(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return False

        try:
            # Use the injected hub instance to get config
            config = self._hub.get_foundation_config()
            if config or not self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_5(self) -> bool:
        """Try to configure using Hub if available.

        Returns:
            True if Hub configuration was successful
        """
        if self._hub is None:
            return False

        try:
            # Use the injected hub instance to get config
            config = self._hub.get_foundation_config()
            if config and self._is_configured_by_setup:
                self.setup(config)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_6(self) -> bool:
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
                self.setup(None)
            return True
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_7(self) -> bool:
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
            return False
        except Exception:
            # If Hub setup fails, fall through to lazy setup
            return False

    def xǁFoundationLoggerǁ_try_hub_configuration__mutmut_8(self) -> bool:
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
            return True

    xǁFoundationLoggerǁ_try_hub_configuration__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_1": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_1,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_2": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_2,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_3": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_3,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_4": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_4,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_5": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_5,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_6": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_6,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_7": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_7,
        "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_8": xǁFoundationLoggerǁ_try_hub_configuration__mutmut_8,
    }

    def _try_hub_configuration(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_try_hub_configuration__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _try_hub_configuration.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_try_hub_configuration__mutmut_orig
    )
    xǁFoundationLoggerǁ_try_hub_configuration__mutmut_orig.__name__ = (
        "xǁFoundationLoggerǁ_try_hub_configuration"
    )

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_orig(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["error"]

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_1(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] and _LAZY_SETUP_STATE["error"]

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_2(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["XXin_progressXX"] or _LAZY_SETUP_STATE["error"]

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_3(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["IN_PROGRESS"] or _LAZY_SETUP_STATE["error"]

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_4(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["XXerrorXX"]

    def xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_5(self) -> bool:
        """Check if emergency fallback should be used.

        Returns:
            True if emergency fallback should be used
        """
        return _LAZY_SETUP_STATE["in_progress"] or _LAZY_SETUP_STATE["ERROR"]

    xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_1": xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_1,
        "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_2": xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_2,
        "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_3": xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_3,
        "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_4": xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_4,
        "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_5": xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_5,
    }

    def _should_use_emergency_fallback(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _should_use_emergency_fallback.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_orig
    )
    xǁFoundationLoggerǁ_should_use_emergency_fallback__mutmut_orig.__name__ = (
        "xǁFoundationLoggerǁ_should_use_emergency_fallback"
    )

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_orig(self) -> None:
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

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_1(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup and (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_2(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] or not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_3(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["XXdoneXX"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_4(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["DONE"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_5(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_6(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["XXerrorXX"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_7(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["ERROR"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_8(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["XXerrorXX"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_9(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["ERROR"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_10(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if _LAZY_SETUP_STATE["done"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_11(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["XXdoneXX"]:
            self._perform_lazy_setup()

    def xǁFoundationLoggerǁ_perform_locked_setup__mutmut_12(self) -> None:
        """Perform setup within the lock."""
        # Double-check state after acquiring lock, as another thread might have finished.
        if self._is_configured_by_setup or (_LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["error"]):
            return

        # If error was set while waiting for lock, use fallback.
        if _LAZY_SETUP_STATE["error"]:
            self._setup_emergency_fallback()
            return

        # If still needs setup, perform lazy setup.
        if not _LAZY_SETUP_STATE["DONE"]:
            self._perform_lazy_setup()

    xǁFoundationLoggerǁ_perform_locked_setup__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_1": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_1,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_2": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_2,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_3": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_3,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_4": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_4,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_5": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_5,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_6": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_6,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_7": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_7,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_8": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_8,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_9": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_9,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_10": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_10,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_11": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_11,
        "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_12": xǁFoundationLoggerǁ_perform_locked_setup__mutmut_12,
    }

    def _perform_locked_setup(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_perform_locked_setup__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _perform_locked_setup.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_perform_locked_setup__mutmut_orig
    )
    xǁFoundationLoggerǁ_perform_locked_setup__mutmut_orig.__name__ = "xǁFoundationLoggerǁ_perform_locked_setup"

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_orig(self) -> None:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_1(self) -> None:
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
        if _LAZY_SETUP_STATE["done"] or not _LAZY_SETUP_STATE["error"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_2(self) -> None:
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
        if _LAZY_SETUP_STATE["XXdoneXX"] and not _LAZY_SETUP_STATE["error"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_3(self) -> None:
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
        if _LAZY_SETUP_STATE["DONE"] and not _LAZY_SETUP_STATE["error"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_4(self) -> None:
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
        if _LAZY_SETUP_STATE["done"] and _LAZY_SETUP_STATE["error"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_5(self) -> None:
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
        if _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["XXerrorXX"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_6(self) -> None:
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
        if _LAZY_SETUP_STATE["done"] and not _LAZY_SETUP_STATE["ERROR"]:
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

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_7(self) -> None:
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
            with get_lock_manager().acquire(None):
                self._perform_locked_setup()
        except Exception:
            # If lock acquisition fails (e.g., due to ordering violations), use emergency fallback
            self._setup_emergency_fallback()

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_8(self) -> None:
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
            with get_lock_manager().acquire("XXfoundation.logger.lazyXX"):
                self._perform_locked_setup()
        except Exception:
            # If lock acquisition fails (e.g., due to ordering violations), use emergency fallback
            self._setup_emergency_fallback()

    def xǁFoundationLoggerǁ_ensure_configured__mutmut_9(self) -> None:
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
            with get_lock_manager().acquire("FOUNDATION.LOGGER.LAZY"):
                self._perform_locked_setup()
        except Exception:
            # If lock acquisition fails (e.g., due to ordering violations), use emergency fallback
            self._setup_emergency_fallback()

    xǁFoundationLoggerǁ_ensure_configured__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_1": xǁFoundationLoggerǁ_ensure_configured__mutmut_1,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_2": xǁFoundationLoggerǁ_ensure_configured__mutmut_2,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_3": xǁFoundationLoggerǁ_ensure_configured__mutmut_3,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_4": xǁFoundationLoggerǁ_ensure_configured__mutmut_4,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_5": xǁFoundationLoggerǁ_ensure_configured__mutmut_5,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_6": xǁFoundationLoggerǁ_ensure_configured__mutmut_6,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_7": xǁFoundationLoggerǁ_ensure_configured__mutmut_7,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_8": xǁFoundationLoggerǁ_ensure_configured__mutmut_8,
        "xǁFoundationLoggerǁ_ensure_configured__mutmut_9": xǁFoundationLoggerǁ_ensure_configured__mutmut_9,
    }

    def _ensure_configured(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_ensure_configured__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_ensure_configured__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _ensure_configured.__signature__ = _mutmut_signature(xǁFoundationLoggerǁ_ensure_configured__mutmut_orig)
    xǁFoundationLoggerǁ_ensure_configured__mutmut_orig.__name__ = "xǁFoundationLoggerǁ_ensure_configured"

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_orig(self) -> None:
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

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_1(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = None
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_2(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["XXin_progressXX"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_3(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["IN_PROGRESS"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_4(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = False
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_5(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=None)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_6(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=True)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_7(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = None
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_8(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["XXerrorXX"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_9(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["ERROR"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_10(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = None

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_11(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["XXin_progressXX"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_12(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["IN_PROGRESS"] = False

    def xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_13(self) -> None:
        """Perform the actual lazy setup of the logging system."""
        from provide.foundation.logger.setup.coordinator import internal_setup

        try:
            _LAZY_SETUP_STATE["in_progress"] = True
            internal_setup(is_explicit_call=False)
        except Exception as e:
            _LAZY_SETUP_STATE["error"] = e
            self._setup_emergency_fallback()
        finally:
            _LAZY_SETUP_STATE["in_progress"] = True

    xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_1": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_1,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_2": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_2,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_3": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_3,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_4": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_4,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_5": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_5,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_6": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_6,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_7": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_7,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_8": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_8,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_9": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_9,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_10": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_10,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_11": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_11,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_12": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_12,
        "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_13": xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_13,
    }

    def _perform_lazy_setup(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _perform_lazy_setup.__signature__ = _mutmut_signature(xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_orig)
    xǁFoundationLoggerǁ_perform_lazy_setup__mutmut_orig.__name__ = "xǁFoundationLoggerǁ_perform_lazy_setup"

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_orig(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_1(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(None):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_2(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=None,
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_3(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=None,
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_4(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=None,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_5(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=None,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_6(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_7(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_8(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_9(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_10(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=None),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=True,
            )

    def xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_11(self) -> None:
        """Set up emergency fallback logging when normal setup fails."""
        from provide.foundation.utils.streams import get_safe_stderr

        with contextlib.suppress(Exception):
            structlog.configure(
                processors=[structlog.dev.ConsoleRenderer()],
                logger_factory=structlog.PrintLoggerFactory(file=get_safe_stderr()),
                wrapper_class=structlog.BoundLogger,
                cache_logger_on_first_use=False,
            )

    xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_1": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_1,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_2": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_2,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_3": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_3,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_4": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_4,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_5": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_5,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_6": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_6,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_7": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_7,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_8": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_8,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_9": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_9,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_10": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_10,
        "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_11": xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_11,
    }

    def _setup_emergency_fallback(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _setup_emergency_fallback.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_orig
    )
    xǁFoundationLoggerǁ_setup_emergency_fallback__mutmut_orig.__name__ = (
        "xǁFoundationLoggerǁ_setup_emergency_fallback"
    )

    def xǁFoundationLoggerǁget_logger__mutmut_orig(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "foundation.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def xǁFoundationLoggerǁget_logger__mutmut_1(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = None
        return structlog.get_logger().bind(logger_name=effective_name)

    def xǁFoundationLoggerǁget_logger__mutmut_2(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is None else "foundation.default"
        return structlog.get_logger().bind(logger_name=effective_name)

    def xǁFoundationLoggerǁget_logger__mutmut_3(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "XXfoundation.defaultXX"
        return structlog.get_logger().bind(logger_name=effective_name)

    def xǁFoundationLoggerǁget_logger__mutmut_4(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "FOUNDATION.DEFAULT"
        return structlog.get_logger().bind(logger_name=effective_name)

    def xǁFoundationLoggerǁget_logger__mutmut_5(self, name: str | None = None) -> Any:
        self._ensure_configured()
        effective_name = name if name is not None else "foundation.default"
        return structlog.get_logger().bind(logger_name=None)

    xǁFoundationLoggerǁget_logger__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁget_logger__mutmut_1": xǁFoundationLoggerǁget_logger__mutmut_1,
        "xǁFoundationLoggerǁget_logger__mutmut_2": xǁFoundationLoggerǁget_logger__mutmut_2,
        "xǁFoundationLoggerǁget_logger__mutmut_3": xǁFoundationLoggerǁget_logger__mutmut_3,
        "xǁFoundationLoggerǁget_logger__mutmut_4": xǁFoundationLoggerǁget_logger__mutmut_4,
        "xǁFoundationLoggerǁget_logger__mutmut_5": xǁFoundationLoggerǁget_logger__mutmut_5,
    }

    def get_logger(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁget_logger__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁget_logger__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_logger.__signature__ = _mutmut_signature(xǁFoundationLoggerǁget_logger__mutmut_orig)
    xǁFoundationLoggerǁget_logger__mutmut_orig.__name__ = "xǁFoundationLoggerǁget_logger"

    def xǁFoundationLoggerǁ_log_with_level__mutmut_orig(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
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

    def xǁFoundationLoggerǁ_log_with_level__mutmut_1(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = None
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_2(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop(None, "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_3(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", None)
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_4(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_5(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop(
            "_foundation_logger_name",
        )
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_6(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("XX_foundation_logger_nameXX", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_7(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_FOUNDATION_LOGGER_NAME", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_8(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "XXfoundationXX")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_9(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "FOUNDATION")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_10(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = None

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_11(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(None)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_12(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name != "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_13(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "XXtraceXX":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_14(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "TRACE":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_15(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = None
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_16(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["XX_foundation_level_hintXX"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_17(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_FOUNDATION_LEVEL_HINT"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_18(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.upper()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_19(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(None, **kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_20(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(**kwargs)
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_21(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(
                event,
            )
        else:
            getattr(log, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_22(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(None, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_23(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(**kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_24(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, level_method_name)(
                event,
            )

    def xǁFoundationLoggerǁ_log_with_level__mutmut_25(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(None, level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_26(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(log, None)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_27(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(level_method_name)(event, **kwargs)

    def xǁFoundationLoggerǁ_log_with_level__mutmut_28(
        self, level_method_name: str, event: str, **kwargs: Any
    ) -> None:
        self._ensure_configured()

        # Use the logger name from kwargs if provided, otherwise default
        logger_name = kwargs.pop("_foundation_logger_name", "foundation")
        log = self.get_logger(logger_name)

        # Handle trace level specially since PrintLogger doesn't have trace method
        if level_method_name == "trace":
            kwargs["_foundation_level_hint"] = TRACE_LEVEL_NAME.lower()
            log.msg(event, **kwargs)
        else:
            getattr(
                log,
            )(event, **kwargs)

    xǁFoundationLoggerǁ_log_with_level__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_log_with_level__mutmut_1": xǁFoundationLoggerǁ_log_with_level__mutmut_1,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_2": xǁFoundationLoggerǁ_log_with_level__mutmut_2,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_3": xǁFoundationLoggerǁ_log_with_level__mutmut_3,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_4": xǁFoundationLoggerǁ_log_with_level__mutmut_4,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_5": xǁFoundationLoggerǁ_log_with_level__mutmut_5,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_6": xǁFoundationLoggerǁ_log_with_level__mutmut_6,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_7": xǁFoundationLoggerǁ_log_with_level__mutmut_7,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_8": xǁFoundationLoggerǁ_log_with_level__mutmut_8,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_9": xǁFoundationLoggerǁ_log_with_level__mutmut_9,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_10": xǁFoundationLoggerǁ_log_with_level__mutmut_10,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_11": xǁFoundationLoggerǁ_log_with_level__mutmut_11,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_12": xǁFoundationLoggerǁ_log_with_level__mutmut_12,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_13": xǁFoundationLoggerǁ_log_with_level__mutmut_13,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_14": xǁFoundationLoggerǁ_log_with_level__mutmut_14,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_15": xǁFoundationLoggerǁ_log_with_level__mutmut_15,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_16": xǁFoundationLoggerǁ_log_with_level__mutmut_16,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_17": xǁFoundationLoggerǁ_log_with_level__mutmut_17,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_18": xǁFoundationLoggerǁ_log_with_level__mutmut_18,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_19": xǁFoundationLoggerǁ_log_with_level__mutmut_19,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_20": xǁFoundationLoggerǁ_log_with_level__mutmut_20,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_21": xǁFoundationLoggerǁ_log_with_level__mutmut_21,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_22": xǁFoundationLoggerǁ_log_with_level__mutmut_22,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_23": xǁFoundationLoggerǁ_log_with_level__mutmut_23,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_24": xǁFoundationLoggerǁ_log_with_level__mutmut_24,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_25": xǁFoundationLoggerǁ_log_with_level__mutmut_25,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_26": xǁFoundationLoggerǁ_log_with_level__mutmut_26,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_27": xǁFoundationLoggerǁ_log_with_level__mutmut_27,
        "xǁFoundationLoggerǁ_log_with_level__mutmut_28": xǁFoundationLoggerǁ_log_with_level__mutmut_28,
    }

    def _log_with_level(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_log_with_level__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_log_with_level__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _log_with_level.__signature__ = _mutmut_signature(xǁFoundationLoggerǁ_log_with_level__mutmut_orig)
    xǁFoundationLoggerǁ_log_with_level__mutmut_orig.__name__ = "xǁFoundationLoggerǁ_log_with_level"

    def xǁFoundationLoggerǁ_format_message_with_args__mutmut_orig(
        self, event: str | Any, args: tuple[Any, ...]
    ) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(event) % args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(event)

    def xǁFoundationLoggerǁ_format_message_with_args__mutmut_1(
        self, event: str | Any, args: tuple[Any, ...]
    ) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(event) / args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(event)

    def xǁFoundationLoggerǁ_format_message_with_args__mutmut_2(
        self, event: str | Any, args: tuple[Any, ...]
    ) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(None) % args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(event)

    def xǁFoundationLoggerǁ_format_message_with_args__mutmut_3(
        self, event: str | Any, args: tuple[Any, ...]
    ) -> str:
        """Format a log message with positional arguments using % formatting."""
        if args:
            try:
                return str(event) % args
            except (TypeError, ValueError):
                return f"{event} {args}"
        return str(None)

    xǁFoundationLoggerǁ_format_message_with_args__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁ_format_message_with_args__mutmut_1": xǁFoundationLoggerǁ_format_message_with_args__mutmut_1,
        "xǁFoundationLoggerǁ_format_message_with_args__mutmut_2": xǁFoundationLoggerǁ_format_message_with_args__mutmut_2,
        "xǁFoundationLoggerǁ_format_message_with_args__mutmut_3": xǁFoundationLoggerǁ_format_message_with_args__mutmut_3,
    }

    def _format_message_with_args(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁ_format_message_with_args__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁ_format_message_with_args__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _format_message_with_args.__signature__ = _mutmut_signature(
        xǁFoundationLoggerǁ_format_message_with_args__mutmut_orig
    )
    xǁFoundationLoggerǁ_format_message_with_args__mutmut_orig.__name__ = (
        "xǁFoundationLoggerǁ_format_message_with_args"
    )

    def xǁFoundationLoggerǁtrace__mutmut_orig(
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

    def xǁFoundationLoggerǁtrace__mutmut_1(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = None
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_2(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(None, args)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_3(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, None)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_4(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(args)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_5(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(
            event,
        )
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_6(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is None:
            kwargs["_foundation_logger_name"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_7(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is not None:
            kwargs["_foundation_logger_name"] = None
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_8(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is not None:
            kwargs["XX_foundation_logger_nameXX"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_9(
        self,
        event: str,
        *args: Any,
        _foundation_logger_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Log trace-level event for detailed debugging."""
        formatted_event = self._format_message_with_args(event, args)
        if _foundation_logger_name is not None:
            kwargs["_FOUNDATION_LOGGER_NAME"] = _foundation_logger_name
        self._log_with_level(TRACE_LEVEL_NAME.lower(), formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_10(
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
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_11(
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
        self._log_with_level(TRACE_LEVEL_NAME.lower(), None, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_12(
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
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_13(
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
        self._log_with_level(TRACE_LEVEL_NAME.lower(), **kwargs)

    def xǁFoundationLoggerǁtrace__mutmut_14(
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
        self._log_with_level(
            TRACE_LEVEL_NAME.lower(),
            formatted_event,
        )

    def xǁFoundationLoggerǁtrace__mutmut_15(
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
        self._log_with_level(TRACE_LEVEL_NAME.upper(), formatted_event, **kwargs)

    xǁFoundationLoggerǁtrace__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁtrace__mutmut_1": xǁFoundationLoggerǁtrace__mutmut_1,
        "xǁFoundationLoggerǁtrace__mutmut_2": xǁFoundationLoggerǁtrace__mutmut_2,
        "xǁFoundationLoggerǁtrace__mutmut_3": xǁFoundationLoggerǁtrace__mutmut_3,
        "xǁFoundationLoggerǁtrace__mutmut_4": xǁFoundationLoggerǁtrace__mutmut_4,
        "xǁFoundationLoggerǁtrace__mutmut_5": xǁFoundationLoggerǁtrace__mutmut_5,
        "xǁFoundationLoggerǁtrace__mutmut_6": xǁFoundationLoggerǁtrace__mutmut_6,
        "xǁFoundationLoggerǁtrace__mutmut_7": xǁFoundationLoggerǁtrace__mutmut_7,
        "xǁFoundationLoggerǁtrace__mutmut_8": xǁFoundationLoggerǁtrace__mutmut_8,
        "xǁFoundationLoggerǁtrace__mutmut_9": xǁFoundationLoggerǁtrace__mutmut_9,
        "xǁFoundationLoggerǁtrace__mutmut_10": xǁFoundationLoggerǁtrace__mutmut_10,
        "xǁFoundationLoggerǁtrace__mutmut_11": xǁFoundationLoggerǁtrace__mutmut_11,
        "xǁFoundationLoggerǁtrace__mutmut_12": xǁFoundationLoggerǁtrace__mutmut_12,
        "xǁFoundationLoggerǁtrace__mutmut_13": xǁFoundationLoggerǁtrace__mutmut_13,
        "xǁFoundationLoggerǁtrace__mutmut_14": xǁFoundationLoggerǁtrace__mutmut_14,
        "xǁFoundationLoggerǁtrace__mutmut_15": xǁFoundationLoggerǁtrace__mutmut_15,
    }

    def trace(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁtrace__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁtrace__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    trace.__signature__ = _mutmut_signature(xǁFoundationLoggerǁtrace__mutmut_orig)
    xǁFoundationLoggerǁtrace__mutmut_orig.__name__ = "xǁFoundationLoggerǁtrace"

    def xǁFoundationLoggerǁdebug__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = None
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(None, args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, None)
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(args)
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(
            event,
        )
        self._log_with_level("debug", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", None, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("debug", **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(
            "debug",
            formatted_event,
        )

    def xǁFoundationLoggerǁdebug__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("XXdebugXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁdebug__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log debug-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("DEBUG", formatted_event, **kwargs)

    xǁFoundationLoggerǁdebug__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁdebug__mutmut_1": xǁFoundationLoggerǁdebug__mutmut_1,
        "xǁFoundationLoggerǁdebug__mutmut_2": xǁFoundationLoggerǁdebug__mutmut_2,
        "xǁFoundationLoggerǁdebug__mutmut_3": xǁFoundationLoggerǁdebug__mutmut_3,
        "xǁFoundationLoggerǁdebug__mutmut_4": xǁFoundationLoggerǁdebug__mutmut_4,
        "xǁFoundationLoggerǁdebug__mutmut_5": xǁFoundationLoggerǁdebug__mutmut_5,
        "xǁFoundationLoggerǁdebug__mutmut_6": xǁFoundationLoggerǁdebug__mutmut_6,
        "xǁFoundationLoggerǁdebug__mutmut_7": xǁFoundationLoggerǁdebug__mutmut_7,
        "xǁFoundationLoggerǁdebug__mutmut_8": xǁFoundationLoggerǁdebug__mutmut_8,
        "xǁFoundationLoggerǁdebug__mutmut_9": xǁFoundationLoggerǁdebug__mutmut_9,
        "xǁFoundationLoggerǁdebug__mutmut_10": xǁFoundationLoggerǁdebug__mutmut_10,
        "xǁFoundationLoggerǁdebug__mutmut_11": xǁFoundationLoggerǁdebug__mutmut_11,
        "xǁFoundationLoggerǁdebug__mutmut_12": xǁFoundationLoggerǁdebug__mutmut_12,
    }

    def debug(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁdebug__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁdebug__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    debug.__signature__ = _mutmut_signature(xǁFoundationLoggerǁdebug__mutmut_orig)
    xǁFoundationLoggerǁdebug__mutmut_orig.__name__ = "xǁFoundationLoggerǁdebug"

    def xǁFoundationLoggerǁinfo__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = None
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(None, args)
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, None)
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(args)
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(
            event,
        )
        self._log_with_level("info", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", None, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("info", **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(
            "info",
            formatted_event,
        )

    def xǁFoundationLoggerǁinfo__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("XXinfoXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁinfo__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log info-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("INFO", formatted_event, **kwargs)

    xǁFoundationLoggerǁinfo__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁinfo__mutmut_1": xǁFoundationLoggerǁinfo__mutmut_1,
        "xǁFoundationLoggerǁinfo__mutmut_2": xǁFoundationLoggerǁinfo__mutmut_2,
        "xǁFoundationLoggerǁinfo__mutmut_3": xǁFoundationLoggerǁinfo__mutmut_3,
        "xǁFoundationLoggerǁinfo__mutmut_4": xǁFoundationLoggerǁinfo__mutmut_4,
        "xǁFoundationLoggerǁinfo__mutmut_5": xǁFoundationLoggerǁinfo__mutmut_5,
        "xǁFoundationLoggerǁinfo__mutmut_6": xǁFoundationLoggerǁinfo__mutmut_6,
        "xǁFoundationLoggerǁinfo__mutmut_7": xǁFoundationLoggerǁinfo__mutmut_7,
        "xǁFoundationLoggerǁinfo__mutmut_8": xǁFoundationLoggerǁinfo__mutmut_8,
        "xǁFoundationLoggerǁinfo__mutmut_9": xǁFoundationLoggerǁinfo__mutmut_9,
        "xǁFoundationLoggerǁinfo__mutmut_10": xǁFoundationLoggerǁinfo__mutmut_10,
        "xǁFoundationLoggerǁinfo__mutmut_11": xǁFoundationLoggerǁinfo__mutmut_11,
        "xǁFoundationLoggerǁinfo__mutmut_12": xǁFoundationLoggerǁinfo__mutmut_12,
    }

    def info(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁinfo__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁinfo__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    info.__signature__ = _mutmut_signature(xǁFoundationLoggerǁinfo__mutmut_orig)
    xǁFoundationLoggerǁinfo__mutmut_orig.__name__ = "xǁFoundationLoggerǁinfo"

    def xǁFoundationLoggerǁwarning__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = None
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(None, args)
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, None)
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(args)
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(
            event,
        )
        self._log_with_level("warning", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", None, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("warning", **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(
            "warning",
            formatted_event,
        )

    def xǁFoundationLoggerǁwarning__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("XXwarningXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁwarning__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log warning-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("WARNING", formatted_event, **kwargs)

    xǁFoundationLoggerǁwarning__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁwarning__mutmut_1": xǁFoundationLoggerǁwarning__mutmut_1,
        "xǁFoundationLoggerǁwarning__mutmut_2": xǁFoundationLoggerǁwarning__mutmut_2,
        "xǁFoundationLoggerǁwarning__mutmut_3": xǁFoundationLoggerǁwarning__mutmut_3,
        "xǁFoundationLoggerǁwarning__mutmut_4": xǁFoundationLoggerǁwarning__mutmut_4,
        "xǁFoundationLoggerǁwarning__mutmut_5": xǁFoundationLoggerǁwarning__mutmut_5,
        "xǁFoundationLoggerǁwarning__mutmut_6": xǁFoundationLoggerǁwarning__mutmut_6,
        "xǁFoundationLoggerǁwarning__mutmut_7": xǁFoundationLoggerǁwarning__mutmut_7,
        "xǁFoundationLoggerǁwarning__mutmut_8": xǁFoundationLoggerǁwarning__mutmut_8,
        "xǁFoundationLoggerǁwarning__mutmut_9": xǁFoundationLoggerǁwarning__mutmut_9,
        "xǁFoundationLoggerǁwarning__mutmut_10": xǁFoundationLoggerǁwarning__mutmut_10,
        "xǁFoundationLoggerǁwarning__mutmut_11": xǁFoundationLoggerǁwarning__mutmut_11,
        "xǁFoundationLoggerǁwarning__mutmut_12": xǁFoundationLoggerǁwarning__mutmut_12,
    }

    def warning(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁwarning__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁwarning__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    warning.__signature__ = _mutmut_signature(xǁFoundationLoggerǁwarning__mutmut_orig)
    xǁFoundationLoggerǁwarning__mutmut_orig.__name__ = "xǁFoundationLoggerǁwarning"

    def xǁFoundationLoggerǁerror__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = None
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(None, args)
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, None)
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(args)
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(
            event,
        )
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", None, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("error", **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(
            "error",
            formatted_event,
        )

    def xǁFoundationLoggerǁerror__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("XXerrorXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁerror__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("ERROR", formatted_event, **kwargs)

    xǁFoundationLoggerǁerror__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁerror__mutmut_1": xǁFoundationLoggerǁerror__mutmut_1,
        "xǁFoundationLoggerǁerror__mutmut_2": xǁFoundationLoggerǁerror__mutmut_2,
        "xǁFoundationLoggerǁerror__mutmut_3": xǁFoundationLoggerǁerror__mutmut_3,
        "xǁFoundationLoggerǁerror__mutmut_4": xǁFoundationLoggerǁerror__mutmut_4,
        "xǁFoundationLoggerǁerror__mutmut_5": xǁFoundationLoggerǁerror__mutmut_5,
        "xǁFoundationLoggerǁerror__mutmut_6": xǁFoundationLoggerǁerror__mutmut_6,
        "xǁFoundationLoggerǁerror__mutmut_7": xǁFoundationLoggerǁerror__mutmut_7,
        "xǁFoundationLoggerǁerror__mutmut_8": xǁFoundationLoggerǁerror__mutmut_8,
        "xǁFoundationLoggerǁerror__mutmut_9": xǁFoundationLoggerǁerror__mutmut_9,
        "xǁFoundationLoggerǁerror__mutmut_10": xǁFoundationLoggerǁerror__mutmut_10,
        "xǁFoundationLoggerǁerror__mutmut_11": xǁFoundationLoggerǁerror__mutmut_11,
        "xǁFoundationLoggerǁerror__mutmut_12": xǁFoundationLoggerǁerror__mutmut_12,
    }

    def error(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁerror__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁerror__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    error.__signature__ = _mutmut_signature(xǁFoundationLoggerǁerror__mutmut_orig)
    xǁFoundationLoggerǁerror__mutmut_orig.__name__ = "xǁFoundationLoggerǁerror"

    def xǁFoundationLoggerǁexception__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = None
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(None, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, None)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(args)
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(
            event,
        )
        kwargs["exc_info"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = None
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["XXexc_infoXX"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["EXC_INFO"] = True
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = False
        self._log_with_level("error", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", None, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_13(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("error", **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_14(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level(
            "error",
            formatted_event,
        )

    def xǁFoundationLoggerǁexception__mutmut_15(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("XXerrorXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁexception__mutmut_16(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log error-level event with exception traceback."""
        formatted_event = self._format_message_with_args(event, args)
        kwargs["exc_info"] = True
        self._log_with_level("ERROR", formatted_event, **kwargs)

    xǁFoundationLoggerǁexception__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁexception__mutmut_1": xǁFoundationLoggerǁexception__mutmut_1,
        "xǁFoundationLoggerǁexception__mutmut_2": xǁFoundationLoggerǁexception__mutmut_2,
        "xǁFoundationLoggerǁexception__mutmut_3": xǁFoundationLoggerǁexception__mutmut_3,
        "xǁFoundationLoggerǁexception__mutmut_4": xǁFoundationLoggerǁexception__mutmut_4,
        "xǁFoundationLoggerǁexception__mutmut_5": xǁFoundationLoggerǁexception__mutmut_5,
        "xǁFoundationLoggerǁexception__mutmut_6": xǁFoundationLoggerǁexception__mutmut_6,
        "xǁFoundationLoggerǁexception__mutmut_7": xǁFoundationLoggerǁexception__mutmut_7,
        "xǁFoundationLoggerǁexception__mutmut_8": xǁFoundationLoggerǁexception__mutmut_8,
        "xǁFoundationLoggerǁexception__mutmut_9": xǁFoundationLoggerǁexception__mutmut_9,
        "xǁFoundationLoggerǁexception__mutmut_10": xǁFoundationLoggerǁexception__mutmut_10,
        "xǁFoundationLoggerǁexception__mutmut_11": xǁFoundationLoggerǁexception__mutmut_11,
        "xǁFoundationLoggerǁexception__mutmut_12": xǁFoundationLoggerǁexception__mutmut_12,
        "xǁFoundationLoggerǁexception__mutmut_13": xǁFoundationLoggerǁexception__mutmut_13,
        "xǁFoundationLoggerǁexception__mutmut_14": xǁFoundationLoggerǁexception__mutmut_14,
        "xǁFoundationLoggerǁexception__mutmut_15": xǁFoundationLoggerǁexception__mutmut_15,
        "xǁFoundationLoggerǁexception__mutmut_16": xǁFoundationLoggerǁexception__mutmut_16,
    }

    def exception(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁexception__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁexception__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exception.__signature__ = _mutmut_signature(xǁFoundationLoggerǁexception__mutmut_orig)
    xǁFoundationLoggerǁexception__mutmut_orig.__name__ = "xǁFoundationLoggerǁexception"

    def xǁFoundationLoggerǁcritical__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = None
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(None, args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, None)
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(args)
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_5(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(
            event,
        )
        self._log_with_level("critical", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_6(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(None, formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_7(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", None, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_8(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_9(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("critical", **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_10(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level(
            "critical",
            formatted_event,
        )

    def xǁFoundationLoggerǁcritical__mutmut_11(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("XXcriticalXX", formatted_event, **kwargs)

    def xǁFoundationLoggerǁcritical__mutmut_12(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Log critical-level event."""
        formatted_event = self._format_message_with_args(event, args)
        self._log_with_level("CRITICAL", formatted_event, **kwargs)

    xǁFoundationLoggerǁcritical__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁcritical__mutmut_1": xǁFoundationLoggerǁcritical__mutmut_1,
        "xǁFoundationLoggerǁcritical__mutmut_2": xǁFoundationLoggerǁcritical__mutmut_2,
        "xǁFoundationLoggerǁcritical__mutmut_3": xǁFoundationLoggerǁcritical__mutmut_3,
        "xǁFoundationLoggerǁcritical__mutmut_4": xǁFoundationLoggerǁcritical__mutmut_4,
        "xǁFoundationLoggerǁcritical__mutmut_5": xǁFoundationLoggerǁcritical__mutmut_5,
        "xǁFoundationLoggerǁcritical__mutmut_6": xǁFoundationLoggerǁcritical__mutmut_6,
        "xǁFoundationLoggerǁcritical__mutmut_7": xǁFoundationLoggerǁcritical__mutmut_7,
        "xǁFoundationLoggerǁcritical__mutmut_8": xǁFoundationLoggerǁcritical__mutmut_8,
        "xǁFoundationLoggerǁcritical__mutmut_9": xǁFoundationLoggerǁcritical__mutmut_9,
        "xǁFoundationLoggerǁcritical__mutmut_10": xǁFoundationLoggerǁcritical__mutmut_10,
        "xǁFoundationLoggerǁcritical__mutmut_11": xǁFoundationLoggerǁcritical__mutmut_11,
        "xǁFoundationLoggerǁcritical__mutmut_12": xǁFoundationLoggerǁcritical__mutmut_12,
    }

    def critical(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁcritical__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁcritical__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    critical.__signature__ = _mutmut_signature(xǁFoundationLoggerǁcritical__mutmut_orig)
    xǁFoundationLoggerǁcritical__mutmut_orig.__name__ = "xǁFoundationLoggerǁcritical"

    def xǁFoundationLoggerǁbind__mutmut_orig(self, **kwargs: Any) -> Any:
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

    def xǁFoundationLoggerǁbind__mutmut_1(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, "_logger") or self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_2(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(None, "_logger") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_3(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, None) and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_4(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr("_logger") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_5(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if (
            hasattr(
                self,
            )
            and self._logger
        ):
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_6(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, "XX_loggerXX") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_7(self, **kwargs: Any) -> Any:
        """Create a new logger with additional context bound to it.

        Args:
            **kwargs: Key-value pairs to bind to the logger

        Returns:
            A new logger instance with the bound context

        """
        self._ensure_configured()
        # Get the actual structlog logger and bind context to it
        if hasattr(self, "_LOGGER") and self._logger:
            return self._logger.bind(**kwargs)
        # Fallback: get fresh logger and bind
        log = self.get_logger()
        return log.bind(**kwargs)

    def xǁFoundationLoggerǁbind__mutmut_8(self, **kwargs: Any) -> Any:
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
        log = None
        return log.bind(**kwargs)

    xǁFoundationLoggerǁbind__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁbind__mutmut_1": xǁFoundationLoggerǁbind__mutmut_1,
        "xǁFoundationLoggerǁbind__mutmut_2": xǁFoundationLoggerǁbind__mutmut_2,
        "xǁFoundationLoggerǁbind__mutmut_3": xǁFoundationLoggerǁbind__mutmut_3,
        "xǁFoundationLoggerǁbind__mutmut_4": xǁFoundationLoggerǁbind__mutmut_4,
        "xǁFoundationLoggerǁbind__mutmut_5": xǁFoundationLoggerǁbind__mutmut_5,
        "xǁFoundationLoggerǁbind__mutmut_6": xǁFoundationLoggerǁbind__mutmut_6,
        "xǁFoundationLoggerǁbind__mutmut_7": xǁFoundationLoggerǁbind__mutmut_7,
        "xǁFoundationLoggerǁbind__mutmut_8": xǁFoundationLoggerǁbind__mutmut_8,
    }

    def bind(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁbind__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁbind__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    bind.__signature__ = _mutmut_signature(xǁFoundationLoggerǁbind__mutmut_orig)
    xǁFoundationLoggerǁbind__mutmut_orig.__name__ = "xǁFoundationLoggerǁbind"

    def xǁFoundationLoggerǁunbind__mutmut_orig(self, *keys: str) -> Any:
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

    def xǁFoundationLoggerǁunbind__mutmut_1(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, "_logger") or self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_2(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(None, "_logger") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_3(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, None) and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_4(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr("_logger") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_5(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if (
            hasattr(
                self,
            )
            and self._logger
        ):
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_6(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, "XX_loggerXX") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_7(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and unbind context from it
        if hasattr(self, "_LOGGER") and self._logger:
            return self._logger.unbind(*keys)
        # Fallback: get fresh logger and unbind
        log = self.get_logger()
        return log.unbind(*keys)

    def xǁFoundationLoggerǁunbind__mutmut_8(self, *keys: str) -> Any:
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
        log = None
        return log.unbind(*keys)

    xǁFoundationLoggerǁunbind__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁunbind__mutmut_1": xǁFoundationLoggerǁunbind__mutmut_1,
        "xǁFoundationLoggerǁunbind__mutmut_2": xǁFoundationLoggerǁunbind__mutmut_2,
        "xǁFoundationLoggerǁunbind__mutmut_3": xǁFoundationLoggerǁunbind__mutmut_3,
        "xǁFoundationLoggerǁunbind__mutmut_4": xǁFoundationLoggerǁunbind__mutmut_4,
        "xǁFoundationLoggerǁunbind__mutmut_5": xǁFoundationLoggerǁunbind__mutmut_5,
        "xǁFoundationLoggerǁunbind__mutmut_6": xǁFoundationLoggerǁunbind__mutmut_6,
        "xǁFoundationLoggerǁunbind__mutmut_7": xǁFoundationLoggerǁunbind__mutmut_7,
        "xǁFoundationLoggerǁunbind__mutmut_8": xǁFoundationLoggerǁunbind__mutmut_8,
    }

    def unbind(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁunbind__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁunbind__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    unbind.__signature__ = _mutmut_signature(xǁFoundationLoggerǁunbind__mutmut_orig)
    xǁFoundationLoggerǁunbind__mutmut_orig.__name__ = "xǁFoundationLoggerǁunbind"

    def xǁFoundationLoggerǁtry_unbind__mutmut_orig(self, *keys: str) -> Any:
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

    def xǁFoundationLoggerǁtry_unbind__mutmut_1(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, "_logger") or self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_2(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(None, "_logger") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_3(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, None) and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_4(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr("_logger") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_5(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if (
            hasattr(
                self,
            )
            and self._logger
        ):
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_6(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, "XX_loggerXX") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_7(self, *keys: str) -> Any:
        """Create a new logger with specified keys removed from context.
        Does not raise an error if keys don't exist.

        Args:
            *keys: Context keys to remove

        Returns:
            A new logger instance without the specified keys

        """
        self._ensure_configured()
        # Get the actual structlog logger and try_unbind context from it
        if hasattr(self, "_LOGGER") and self._logger:
            return self._logger.try_unbind(*keys)
        # Fallback: get fresh logger and try_unbind
        log = self.get_logger()
        return log.try_unbind(*keys)

    def xǁFoundationLoggerǁtry_unbind__mutmut_8(self, *keys: str) -> Any:
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
        log = None
        return log.try_unbind(*keys)

    xǁFoundationLoggerǁtry_unbind__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFoundationLoggerǁtry_unbind__mutmut_1": xǁFoundationLoggerǁtry_unbind__mutmut_1,
        "xǁFoundationLoggerǁtry_unbind__mutmut_2": xǁFoundationLoggerǁtry_unbind__mutmut_2,
        "xǁFoundationLoggerǁtry_unbind__mutmut_3": xǁFoundationLoggerǁtry_unbind__mutmut_3,
        "xǁFoundationLoggerǁtry_unbind__mutmut_4": xǁFoundationLoggerǁtry_unbind__mutmut_4,
        "xǁFoundationLoggerǁtry_unbind__mutmut_5": xǁFoundationLoggerǁtry_unbind__mutmut_5,
        "xǁFoundationLoggerǁtry_unbind__mutmut_6": xǁFoundationLoggerǁtry_unbind__mutmut_6,
        "xǁFoundationLoggerǁtry_unbind__mutmut_7": xǁFoundationLoggerǁtry_unbind__mutmut_7,
        "xǁFoundationLoggerǁtry_unbind__mutmut_8": xǁFoundationLoggerǁtry_unbind__mutmut_8,
    }

    def try_unbind(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFoundationLoggerǁtry_unbind__mutmut_orig"),
            object.__getattribute__(self, "xǁFoundationLoggerǁtry_unbind__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    try_unbind.__signature__ = _mutmut_signature(xǁFoundationLoggerǁtry_unbind__mutmut_orig)
    xǁFoundationLoggerǁtry_unbind__mutmut_orig.__name__ = "xǁFoundationLoggerǁtry_unbind"

    def __setattr__(self, name: str, value: Any) -> None:
        """Override setattr to prevent accidental modification of logger state."""
        if hasattr(self, name) and name.startswith("_"):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_orig() -> FoundationLogger:
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


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_1() -> FoundationLogger:
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

    hub = None
    logger_instance = hub._component_registry.get("foundation.logger.instance", "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_2() -> FoundationLogger:
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
    logger_instance = None

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_3() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get(None, "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_4() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("foundation.logger.instance", None)

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_5() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_6() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get(
        "foundation.logger.instance",
    )

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_7() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("XXfoundation.logger.instanceXX", "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_8() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("FOUNDATION.LOGGER.INSTANCE", "singleton")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_9() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("foundation.logger.instance", "XXsingletonXX")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


# Global logger function - gets logger through Hub
def x_get_global_logger__mutmut_10() -> FoundationLogger:
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
    logger_instance = hub._component_registry.get("foundation.logger.instance", "SINGLETON")

    if logger_instance:
        return logger_instance

    # Emergency fallback - create standalone logger
    return FoundationLogger()


x_get_global_logger__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_global_logger__mutmut_1": x_get_global_logger__mutmut_1,
    "x_get_global_logger__mutmut_2": x_get_global_logger__mutmut_2,
    "x_get_global_logger__mutmut_3": x_get_global_logger__mutmut_3,
    "x_get_global_logger__mutmut_4": x_get_global_logger__mutmut_4,
    "x_get_global_logger__mutmut_5": x_get_global_logger__mutmut_5,
    "x_get_global_logger__mutmut_6": x_get_global_logger__mutmut_6,
    "x_get_global_logger__mutmut_7": x_get_global_logger__mutmut_7,
    "x_get_global_logger__mutmut_8": x_get_global_logger__mutmut_8,
    "x_get_global_logger__mutmut_9": x_get_global_logger__mutmut_9,
    "x_get_global_logger__mutmut_10": x_get_global_logger__mutmut_10,
}


def get_global_logger(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_global_logger__mutmut_orig, x_get_global_logger__mutmut_mutants, args, kwargs
    )
    return result


get_global_logger.__signature__ = _mutmut_signature(x_get_global_logger__mutmut_orig)
x_get_global_logger__mutmut_orig.__name__ = "x_get_global_logger"


class GlobalLoggerProxy:
    """Proxy object that forwards all attribute access to Hub-based logger."""

    def xǁGlobalLoggerProxyǁ__getattr____mutmut_orig(self, name: str) -> Any:
        return getattr(get_global_logger(), name)

    def xǁGlobalLoggerProxyǁ__getattr____mutmut_1(self, name: str) -> Any:
        return getattr(None, name)

    def xǁGlobalLoggerProxyǁ__getattr____mutmut_2(self, name: str) -> Any:
        return getattr(get_global_logger(), None)

    def xǁGlobalLoggerProxyǁ__getattr____mutmut_3(self, name: str) -> Any:
        return getattr(name)

    def xǁGlobalLoggerProxyǁ__getattr____mutmut_4(self, name: str) -> Any:
        return getattr(
            get_global_logger(),
        )

    xǁGlobalLoggerProxyǁ__getattr____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁ__getattr____mutmut_1": xǁGlobalLoggerProxyǁ__getattr____mutmut_1,
        "xǁGlobalLoggerProxyǁ__getattr____mutmut_2": xǁGlobalLoggerProxyǁ__getattr____mutmut_2,
        "xǁGlobalLoggerProxyǁ__getattr____mutmut_3": xǁGlobalLoggerProxyǁ__getattr____mutmut_3,
        "xǁGlobalLoggerProxyǁ__getattr____mutmut_4": xǁGlobalLoggerProxyǁ__getattr____mutmut_4,
    }

    def __getattr__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁ__getattr____mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁ__getattr____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __getattr__.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁ__getattr____mutmut_orig)
    xǁGlobalLoggerProxyǁ__getattr____mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁ__getattr__"

    # Forward common logger methods to help mypy
    def xǁGlobalLoggerProxyǁdebug__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(event, *args, **kwargs)

    # Forward common logger methods to help mypy
    def xǁGlobalLoggerProxyǁdebug__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(None, *args, **kwargs)

    # Forward common logger methods to help mypy
    def xǁGlobalLoggerProxyǁdebug__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(*args, **kwargs)

    # Forward common logger methods to help mypy
    def xǁGlobalLoggerProxyǁdebug__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(event, **kwargs)

    # Forward common logger methods to help mypy
    def xǁGlobalLoggerProxyǁdebug__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().debug(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁdebug__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁdebug__mutmut_1": xǁGlobalLoggerProxyǁdebug__mutmut_1,
        "xǁGlobalLoggerProxyǁdebug__mutmut_2": xǁGlobalLoggerProxyǁdebug__mutmut_2,
        "xǁGlobalLoggerProxyǁdebug__mutmut_3": xǁGlobalLoggerProxyǁdebug__mutmut_3,
        "xǁGlobalLoggerProxyǁdebug__mutmut_4": xǁGlobalLoggerProxyǁdebug__mutmut_4,
    }

    def debug(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁdebug__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁdebug__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    debug.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁdebug__mutmut_orig)
    xǁGlobalLoggerProxyǁdebug__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁdebug"

    def xǁGlobalLoggerProxyǁinfo__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(event, *args, **kwargs)

    def xǁGlobalLoggerProxyǁinfo__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(None, *args, **kwargs)

    def xǁGlobalLoggerProxyǁinfo__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(*args, **kwargs)

    def xǁGlobalLoggerProxyǁinfo__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(event, **kwargs)

    def xǁGlobalLoggerProxyǁinfo__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().info(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁinfo__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁinfo__mutmut_1": xǁGlobalLoggerProxyǁinfo__mutmut_1,
        "xǁGlobalLoggerProxyǁinfo__mutmut_2": xǁGlobalLoggerProxyǁinfo__mutmut_2,
        "xǁGlobalLoggerProxyǁinfo__mutmut_3": xǁGlobalLoggerProxyǁinfo__mutmut_3,
        "xǁGlobalLoggerProxyǁinfo__mutmut_4": xǁGlobalLoggerProxyǁinfo__mutmut_4,
    }

    def info(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁinfo__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁinfo__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    info.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁinfo__mutmut_orig)
    xǁGlobalLoggerProxyǁinfo__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁinfo"

    def xǁGlobalLoggerProxyǁwarning__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(event, *args, **kwargs)

    def xǁGlobalLoggerProxyǁwarning__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(None, *args, **kwargs)

    def xǁGlobalLoggerProxyǁwarning__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(*args, **kwargs)

    def xǁGlobalLoggerProxyǁwarning__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(event, **kwargs)

    def xǁGlobalLoggerProxyǁwarning__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().warning(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁwarning__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁwarning__mutmut_1": xǁGlobalLoggerProxyǁwarning__mutmut_1,
        "xǁGlobalLoggerProxyǁwarning__mutmut_2": xǁGlobalLoggerProxyǁwarning__mutmut_2,
        "xǁGlobalLoggerProxyǁwarning__mutmut_3": xǁGlobalLoggerProxyǁwarning__mutmut_3,
        "xǁGlobalLoggerProxyǁwarning__mutmut_4": xǁGlobalLoggerProxyǁwarning__mutmut_4,
    }

    def warning(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁwarning__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁwarning__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    warning.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁwarning__mutmut_orig)
    xǁGlobalLoggerProxyǁwarning__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁwarning"

    def xǁGlobalLoggerProxyǁerror__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(event, *args, **kwargs)

    def xǁGlobalLoggerProxyǁerror__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(None, *args, **kwargs)

    def xǁGlobalLoggerProxyǁerror__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(*args, **kwargs)

    def xǁGlobalLoggerProxyǁerror__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(event, **kwargs)

    def xǁGlobalLoggerProxyǁerror__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().error(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁerror__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁerror__mutmut_1": xǁGlobalLoggerProxyǁerror__mutmut_1,
        "xǁGlobalLoggerProxyǁerror__mutmut_2": xǁGlobalLoggerProxyǁerror__mutmut_2,
        "xǁGlobalLoggerProxyǁerror__mutmut_3": xǁGlobalLoggerProxyǁerror__mutmut_3,
        "xǁGlobalLoggerProxyǁerror__mutmut_4": xǁGlobalLoggerProxyǁerror__mutmut_4,
    }

    def error(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁerror__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁerror__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    error.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁerror__mutmut_orig)
    xǁGlobalLoggerProxyǁerror__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁerror"

    def xǁGlobalLoggerProxyǁcritical__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(event, *args, **kwargs)

    def xǁGlobalLoggerProxyǁcritical__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(None, *args, **kwargs)

    def xǁGlobalLoggerProxyǁcritical__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(*args, **kwargs)

    def xǁGlobalLoggerProxyǁcritical__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(event, **kwargs)

    def xǁGlobalLoggerProxyǁcritical__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().critical(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁcritical__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁcritical__mutmut_1": xǁGlobalLoggerProxyǁcritical__mutmut_1,
        "xǁGlobalLoggerProxyǁcritical__mutmut_2": xǁGlobalLoggerProxyǁcritical__mutmut_2,
        "xǁGlobalLoggerProxyǁcritical__mutmut_3": xǁGlobalLoggerProxyǁcritical__mutmut_3,
        "xǁGlobalLoggerProxyǁcritical__mutmut_4": xǁGlobalLoggerProxyǁcritical__mutmut_4,
    }

    def critical(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁcritical__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁcritical__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    critical.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁcritical__mutmut_orig)
    xǁGlobalLoggerProxyǁcritical__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁcritical"

    def xǁGlobalLoggerProxyǁexception__mutmut_orig(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(event, *args, **kwargs)

    def xǁGlobalLoggerProxyǁexception__mutmut_1(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(None, *args, **kwargs)

    def xǁGlobalLoggerProxyǁexception__mutmut_2(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(*args, **kwargs)

    def xǁGlobalLoggerProxyǁexception__mutmut_3(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(event, **kwargs)

    def xǁGlobalLoggerProxyǁexception__mutmut_4(self, event: str, *args: Any, **kwargs: Any) -> None:
        return get_global_logger().exception(
            event,
            *args,
        )

    xǁGlobalLoggerProxyǁexception__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁexception__mutmut_1": xǁGlobalLoggerProxyǁexception__mutmut_1,
        "xǁGlobalLoggerProxyǁexception__mutmut_2": xǁGlobalLoggerProxyǁexception__mutmut_2,
        "xǁGlobalLoggerProxyǁexception__mutmut_3": xǁGlobalLoggerProxyǁexception__mutmut_3,
        "xǁGlobalLoggerProxyǁexception__mutmut_4": xǁGlobalLoggerProxyǁexception__mutmut_4,
    }

    def exception(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁexception__mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁexception__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    exception.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁexception__mutmut_orig)
    xǁGlobalLoggerProxyǁexception__mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁexception"

    def __setattr__(self, name: str, value: Any) -> None:
        """Allow tests to set internal state on the underlying logger."""
        if name.startswith("_"):
            # For internal attributes, set them on the actual logger instance
            logger = get_global_logger()
            setattr(logger, name, value)
        else:
            super().__setattr__(name, value)

    def xǁGlobalLoggerProxyǁ__call____mutmut_orig(self, *args: Any, **kwargs: Any) -> Any:
        return get_global_logger().get_logger(*args, **kwargs)

    def xǁGlobalLoggerProxyǁ__call____mutmut_1(self, *args: Any, **kwargs: Any) -> Any:
        return get_global_logger().get_logger(**kwargs)

    def xǁGlobalLoggerProxyǁ__call____mutmut_2(self, *args: Any, **kwargs: Any) -> Any:
        return get_global_logger().get_logger(
            *args,
        )

    xǁGlobalLoggerProxyǁ__call____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGlobalLoggerProxyǁ__call____mutmut_1": xǁGlobalLoggerProxyǁ__call____mutmut_1,
        "xǁGlobalLoggerProxyǁ__call____mutmut_2": xǁGlobalLoggerProxyǁ__call____mutmut_2,
    }

    def __call__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁ__call____mutmut_orig"),
            object.__getattribute__(self, "xǁGlobalLoggerProxyǁ__call____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __call__.__signature__ = _mutmut_signature(xǁGlobalLoggerProxyǁ__call____mutmut_orig)
    xǁGlobalLoggerProxyǁ__call____mutmut_orig.__name__ = "xǁGlobalLoggerProxyǁ__call__"


# Global logger instance (now a proxy)
logger = GlobalLoggerProxy()


# <3 🧱🤝📝🪄
