# provide/foundation/config/bootstrap.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Configuration schema discovery and registration for bootstrap.

This module provides functionality to discover all RuntimeConfig subclasses
and register them with the Hub's CONFIG_SCHEMA dimension during bootstrap.
"""

from __future__ import annotations

import importlib

from attrs import fields

from provide.foundation.config.env import RuntimeConfig
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


def x__import_config_modules__mutmut_orig() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_1() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = None

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_2() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "XXprovide.foundation.logger.config.loggingXX",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_3() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "PROVIDE.FOUNDATION.LOGGER.CONFIG.LOGGING",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_4() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "XXprovide.foundation.logger.config.telemetryXX",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_5() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "PROVIDE.FOUNDATION.LOGGER.CONFIG.TELEMETRY",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_6() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "XXprovide.foundation.transport.configXX",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_7() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "PROVIDE.FOUNDATION.TRANSPORT.CONFIG",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_8() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "XXprovide.foundation.integrations.openobserve.configXX",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_9() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "PROVIDE.FOUNDATION.INTEGRATIONS.OPENOBSERVE.CONFIG",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_10() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "XXprovide.foundation.streams.configXX",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_11() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "PROVIDE.FOUNDATION.STREAMS.CONFIG",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_12() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "XXprovide.foundation.serialization.configXX",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_13() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "PROVIDE.FOUNDATION.SERIALIZATION.CONFIG",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_14() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(None)
        except ImportError:
            # Module may not exist or have optional dependencies
            continue


def x__import_config_modules__mutmut_15() -> None:
    """Import all config modules to ensure RuntimeConfig subclasses are defined.

    This function walks through the provide.foundation package and imports
    all config modules so that their RuntimeConfig subclasses are loaded.
    """
    # Import known config modules explicitly
    config_modules = [
        "provide.foundation.logger.config.logging",
        "provide.foundation.logger.config.telemetry",
        "provide.foundation.transport.config",
        "provide.foundation.integrations.openobserve.config",
        "provide.foundation.streams.config",
        "provide.foundation.serialization.config",
    ]

    for module_name in config_modules:
        try:
            importlib.import_module(module_name)
        except ImportError:
            # Module may not exist or have optional dependencies
            break


x__import_config_modules__mutmut_mutants: ClassVar[MutantDict] = {
    "x__import_config_modules__mutmut_1": x__import_config_modules__mutmut_1,
    "x__import_config_modules__mutmut_2": x__import_config_modules__mutmut_2,
    "x__import_config_modules__mutmut_3": x__import_config_modules__mutmut_3,
    "x__import_config_modules__mutmut_4": x__import_config_modules__mutmut_4,
    "x__import_config_modules__mutmut_5": x__import_config_modules__mutmut_5,
    "x__import_config_modules__mutmut_6": x__import_config_modules__mutmut_6,
    "x__import_config_modules__mutmut_7": x__import_config_modules__mutmut_7,
    "x__import_config_modules__mutmut_8": x__import_config_modules__mutmut_8,
    "x__import_config_modules__mutmut_9": x__import_config_modules__mutmut_9,
    "x__import_config_modules__mutmut_10": x__import_config_modules__mutmut_10,
    "x__import_config_modules__mutmut_11": x__import_config_modules__mutmut_11,
    "x__import_config_modules__mutmut_12": x__import_config_modules__mutmut_12,
    "x__import_config_modules__mutmut_13": x__import_config_modules__mutmut_13,
    "x__import_config_modules__mutmut_14": x__import_config_modules__mutmut_14,
    "x__import_config_modules__mutmut_15": x__import_config_modules__mutmut_15,
}


def _import_config_modules(*args, **kwargs):
    result = _mutmut_trampoline(
        x__import_config_modules__mutmut_orig, x__import_config_modules__mutmut_mutants, args, kwargs
    )
    return result


_import_config_modules.__signature__ = _mutmut_signature(x__import_config_modules__mutmut_orig)
x__import_config_modules__mutmut_orig.__name__ = "x__import_config_modules"


def x__get_all_subclasses__mutmut_orig(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = set(cls.__subclasses__())
    for subclass in list(subclasses):
        subclasses.update(_get_all_subclasses(subclass))
    return subclasses


def x__get_all_subclasses__mutmut_1(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = None
    for subclass in list(subclasses):
        subclasses.update(_get_all_subclasses(subclass))
    return subclasses


def x__get_all_subclasses__mutmut_2(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = set(None)
    for subclass in list(subclasses):
        subclasses.update(_get_all_subclasses(subclass))
    return subclasses


def x__get_all_subclasses__mutmut_3(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = set(cls.__subclasses__())
    for subclass in list(None):
        subclasses.update(_get_all_subclasses(subclass))
    return subclasses


def x__get_all_subclasses__mutmut_4(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = set(cls.__subclasses__())
    for subclass in list(subclasses):
        subclasses.update(None)
    return subclasses


def x__get_all_subclasses__mutmut_5(cls: type) -> set[type]:
    """Recursively get all subclasses of a class.

    Args:
        cls: The base class

    Returns:
        Set of all subclasses

    """
    subclasses = set(cls.__subclasses__())
    for subclass in list(subclasses):
        subclasses.update(_get_all_subclasses(None))
    return subclasses


x__get_all_subclasses__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_all_subclasses__mutmut_1": x__get_all_subclasses__mutmut_1,
    "x__get_all_subclasses__mutmut_2": x__get_all_subclasses__mutmut_2,
    "x__get_all_subclasses__mutmut_3": x__get_all_subclasses__mutmut_3,
    "x__get_all_subclasses__mutmut_4": x__get_all_subclasses__mutmut_4,
    "x__get_all_subclasses__mutmut_5": x__get_all_subclasses__mutmut_5,
}


def _get_all_subclasses(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_all_subclasses__mutmut_orig, x__get_all_subclasses__mutmut_mutants, args, kwargs
    )
    return result


_get_all_subclasses.__signature__ = _mutmut_signature(x__get_all_subclasses__mutmut_orig)
x__get_all_subclasses__mutmut_orig.__name__ = "x__get_all_subclasses"


def x_discover_and_register_configs__mutmut_orig() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_1() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = None

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_2() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = None
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_3() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(None)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_4() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = None

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_5() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(None)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_6() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = None

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_7() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_8() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = None
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_9() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(None)
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_10() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split("XX.XX")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_11() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = None
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_12() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "XXcoreXX"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_13() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "CORE"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_14() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" or module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_15() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 or module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_16() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) > 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_17() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 4 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_18() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[1] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_19() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] != "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_20() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "XXprovideXX" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_21() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "PROVIDE" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_22() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[2] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_23() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] != "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_24() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "XXfoundationXX":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_25() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "FOUNDATION":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_26() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = None

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_27() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[3]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_28() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = None
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_29() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = True
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_30() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(None):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_31() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata and "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_32() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "XXenv_varXX" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_33() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "ENV_VAR" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_34() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" not in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_35() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "XXenv_prefixXX" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_36() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "ENV_PREFIX" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_37() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" not in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_38() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = None
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_39() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = False
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_40() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    return
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_41() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = None

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_42() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = False

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_43() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=None,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_44() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=None,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_45() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=None,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_46() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata=None,
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_47() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=None,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_48() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_49() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_50() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_51() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_52() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
        )


def x_discover_and_register_configs__mutmut_53() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "XXmoduleXX": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_54() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "MODULE": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_55() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "XXcategoryXX": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_56() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "CATEGORY": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_57() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "XXhas_env_varsXX": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_58() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "HAS_ENV_VARS": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_59() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "XXdocXX": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_60() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "DOC": config_cls.__doc__ or "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_61() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ and "",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_62() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "XXXX",
            },
            replace=True,  # Allow re-registration
        )


def x_discover_and_register_configs__mutmut_63() -> None:
    """Discover and register all RuntimeConfig subclasses with the Hub.

    This function should be called from bootstrap_foundation() after the Hub
    is initialized. It discovers all RuntimeConfig subclasses and registers
    them with the CONFIG_SCHEMA dimension.

    The function:
    1. Imports all known config modules
    2. Discovers all RuntimeConfig subclasses
    3. Registers each with the Hub's CONFIG_SCHEMA dimension
    """
    from provide.foundation.hub import get_hub
    from provide.foundation.hub.categories import ComponentCategory

    # Import config modules to ensure classes are defined
    _import_config_modules()

    # Get the hub
    hub = get_hub()

    # Check if already registered (idempotent)
    existing_names = hub._component_registry.list_dimension(ComponentCategory.CONFIG_SCHEMA.value)
    if existing_names:
        # Already registered, skip
        return

    # Discover all RuntimeConfig subclasses
    config_classes = _get_all_subclasses(RuntimeConfig)

    # Filter out the base RuntimeConfig class itself
    config_classes = {cls for cls in config_classes if cls is not RuntimeConfig}

    # Register each config class
    for config_cls in config_classes:
        # Extract category from module path
        # e.g., "provide.foundation.logger.config.logging" -> "logger"
        module_parts = config_cls.__module__.split(".")
        category = "core"
        if len(module_parts) >= 3 and module_parts[0] == "provide" and module_parts[1] == "foundation":
            category = module_parts[2]

        # Check if class has any env_var fields
        has_env_vars = False
        try:
            for attr in fields(config_cls):
                if "env_var" in attr.metadata or "env_prefix" in attr.metadata:
                    has_env_vars = True
                    break
        except Exception:
            # If we can't inspect fields, assume it might have env vars
            has_env_vars = True

        # Register with Hub
        hub._component_registry.register(
            name=config_cls.__name__,
            value=config_cls,
            dimension=ComponentCategory.CONFIG_SCHEMA.value,
            metadata={
                "module": config_cls.__module__,
                "category": category,
                "has_env_vars": has_env_vars,
                "doc": config_cls.__doc__ or "",
            },
            replace=False,  # Allow re-registration
        )


x_discover_and_register_configs__mutmut_mutants: ClassVar[MutantDict] = {
    "x_discover_and_register_configs__mutmut_1": x_discover_and_register_configs__mutmut_1,
    "x_discover_and_register_configs__mutmut_2": x_discover_and_register_configs__mutmut_2,
    "x_discover_and_register_configs__mutmut_3": x_discover_and_register_configs__mutmut_3,
    "x_discover_and_register_configs__mutmut_4": x_discover_and_register_configs__mutmut_4,
    "x_discover_and_register_configs__mutmut_5": x_discover_and_register_configs__mutmut_5,
    "x_discover_and_register_configs__mutmut_6": x_discover_and_register_configs__mutmut_6,
    "x_discover_and_register_configs__mutmut_7": x_discover_and_register_configs__mutmut_7,
    "x_discover_and_register_configs__mutmut_8": x_discover_and_register_configs__mutmut_8,
    "x_discover_and_register_configs__mutmut_9": x_discover_and_register_configs__mutmut_9,
    "x_discover_and_register_configs__mutmut_10": x_discover_and_register_configs__mutmut_10,
    "x_discover_and_register_configs__mutmut_11": x_discover_and_register_configs__mutmut_11,
    "x_discover_and_register_configs__mutmut_12": x_discover_and_register_configs__mutmut_12,
    "x_discover_and_register_configs__mutmut_13": x_discover_and_register_configs__mutmut_13,
    "x_discover_and_register_configs__mutmut_14": x_discover_and_register_configs__mutmut_14,
    "x_discover_and_register_configs__mutmut_15": x_discover_and_register_configs__mutmut_15,
    "x_discover_and_register_configs__mutmut_16": x_discover_and_register_configs__mutmut_16,
    "x_discover_and_register_configs__mutmut_17": x_discover_and_register_configs__mutmut_17,
    "x_discover_and_register_configs__mutmut_18": x_discover_and_register_configs__mutmut_18,
    "x_discover_and_register_configs__mutmut_19": x_discover_and_register_configs__mutmut_19,
    "x_discover_and_register_configs__mutmut_20": x_discover_and_register_configs__mutmut_20,
    "x_discover_and_register_configs__mutmut_21": x_discover_and_register_configs__mutmut_21,
    "x_discover_and_register_configs__mutmut_22": x_discover_and_register_configs__mutmut_22,
    "x_discover_and_register_configs__mutmut_23": x_discover_and_register_configs__mutmut_23,
    "x_discover_and_register_configs__mutmut_24": x_discover_and_register_configs__mutmut_24,
    "x_discover_and_register_configs__mutmut_25": x_discover_and_register_configs__mutmut_25,
    "x_discover_and_register_configs__mutmut_26": x_discover_and_register_configs__mutmut_26,
    "x_discover_and_register_configs__mutmut_27": x_discover_and_register_configs__mutmut_27,
    "x_discover_and_register_configs__mutmut_28": x_discover_and_register_configs__mutmut_28,
    "x_discover_and_register_configs__mutmut_29": x_discover_and_register_configs__mutmut_29,
    "x_discover_and_register_configs__mutmut_30": x_discover_and_register_configs__mutmut_30,
    "x_discover_and_register_configs__mutmut_31": x_discover_and_register_configs__mutmut_31,
    "x_discover_and_register_configs__mutmut_32": x_discover_and_register_configs__mutmut_32,
    "x_discover_and_register_configs__mutmut_33": x_discover_and_register_configs__mutmut_33,
    "x_discover_and_register_configs__mutmut_34": x_discover_and_register_configs__mutmut_34,
    "x_discover_and_register_configs__mutmut_35": x_discover_and_register_configs__mutmut_35,
    "x_discover_and_register_configs__mutmut_36": x_discover_and_register_configs__mutmut_36,
    "x_discover_and_register_configs__mutmut_37": x_discover_and_register_configs__mutmut_37,
    "x_discover_and_register_configs__mutmut_38": x_discover_and_register_configs__mutmut_38,
    "x_discover_and_register_configs__mutmut_39": x_discover_and_register_configs__mutmut_39,
    "x_discover_and_register_configs__mutmut_40": x_discover_and_register_configs__mutmut_40,
    "x_discover_and_register_configs__mutmut_41": x_discover_and_register_configs__mutmut_41,
    "x_discover_and_register_configs__mutmut_42": x_discover_and_register_configs__mutmut_42,
    "x_discover_and_register_configs__mutmut_43": x_discover_and_register_configs__mutmut_43,
    "x_discover_and_register_configs__mutmut_44": x_discover_and_register_configs__mutmut_44,
    "x_discover_and_register_configs__mutmut_45": x_discover_and_register_configs__mutmut_45,
    "x_discover_and_register_configs__mutmut_46": x_discover_and_register_configs__mutmut_46,
    "x_discover_and_register_configs__mutmut_47": x_discover_and_register_configs__mutmut_47,
    "x_discover_and_register_configs__mutmut_48": x_discover_and_register_configs__mutmut_48,
    "x_discover_and_register_configs__mutmut_49": x_discover_and_register_configs__mutmut_49,
    "x_discover_and_register_configs__mutmut_50": x_discover_and_register_configs__mutmut_50,
    "x_discover_and_register_configs__mutmut_51": x_discover_and_register_configs__mutmut_51,
    "x_discover_and_register_configs__mutmut_52": x_discover_and_register_configs__mutmut_52,
    "x_discover_and_register_configs__mutmut_53": x_discover_and_register_configs__mutmut_53,
    "x_discover_and_register_configs__mutmut_54": x_discover_and_register_configs__mutmut_54,
    "x_discover_and_register_configs__mutmut_55": x_discover_and_register_configs__mutmut_55,
    "x_discover_and_register_configs__mutmut_56": x_discover_and_register_configs__mutmut_56,
    "x_discover_and_register_configs__mutmut_57": x_discover_and_register_configs__mutmut_57,
    "x_discover_and_register_configs__mutmut_58": x_discover_and_register_configs__mutmut_58,
    "x_discover_and_register_configs__mutmut_59": x_discover_and_register_configs__mutmut_59,
    "x_discover_and_register_configs__mutmut_60": x_discover_and_register_configs__mutmut_60,
    "x_discover_and_register_configs__mutmut_61": x_discover_and_register_configs__mutmut_61,
    "x_discover_and_register_configs__mutmut_62": x_discover_and_register_configs__mutmut_62,
    "x_discover_and_register_configs__mutmut_63": x_discover_and_register_configs__mutmut_63,
}


def discover_and_register_configs(*args, **kwargs):
    result = _mutmut_trampoline(
        x_discover_and_register_configs__mutmut_orig,
        x_discover_and_register_configs__mutmut_mutants,
        args,
        kwargs,
    )
    return result


discover_and_register_configs.__signature__ = _mutmut_signature(x_discover_and_register_configs__mutmut_orig)
x_discover_and_register_configs__mutmut_orig.__name__ = "x_discover_and_register_configs"


# <3 🧱🤝⚙️🪄
