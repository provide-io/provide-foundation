# provide/foundation/hub/config.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import inspect
from typing import Any, TypeVar

from provide.foundation.config.base import BaseConfig
from provide.foundation.errors.decorators import resilient
from provide.foundation.hub.foundation import get_foundation_logger
from provide.foundation.hub.registry import RegistryEntry

"""Hub configuration management utilities.

Provides functions for resolving configuration values from registered sources,
loading configurations, and managing the configuration chain.
"""

T = TypeVar("T", bound=BaseConfig)
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


def _get_registry_and_lock() -> tuple[Any, Any]:
    """Get registry and ComponentCategory from components module."""
    from provide.foundation.hub.components import (
        ComponentCategory,
        get_component_registry,
    )

    return get_component_registry(), ComponentCategory


@resilient(fallback=None, suppress=(Exception,))
def resolve_config_value(key: str) -> Any:
    """Resolve configuration value using priority-ordered sources."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)

    # Try each source
    for entry in config_sources:
        source = entry.value
        if hasattr(source, "get_value"):
            # Try to get value, continue on error
            try:
                value = source.get_value(key)
                if value is not None:
                    return value
            except Exception as e:
                # Log but continue - config sources may legitimately not have this key
                get_foundation_logger().debug(
                    "Config source failed to get value",
                    source=entry.name,
                    key=key,
                    error=str(e),
                )
                continue

    return None


def x_get_config_chain__mutmut_orig() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_1() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = None

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_2() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = None
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_3() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(None)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_4() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = None

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_5() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension != ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_6() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=None, reverse=True)
    return config_sources


def x_get_config_chain__mutmut_7() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=None)
    return config_sources


def x_get_config_chain__mutmut_8() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(reverse=True)
    return config_sources


def x_get_config_chain__mutmut_9() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(
        key=lambda e: e.metadata.get("priority", 0),
    )
    return config_sources


def x_get_config_chain__mutmut_10() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: None, reverse=True)
    return config_sources


def x_get_config_chain__mutmut_11() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get(None, 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_12() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", None), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_13() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get(0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_14() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(
        key=lambda e: e.metadata.get(
            "priority",
        ),
        reverse=True,
    )
    return config_sources


def x_get_config_chain__mutmut_15() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_16() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_17() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 1), reverse=True)
    return config_sources


def x_get_config_chain__mutmut_18() -> list[RegistryEntry]:
    """Get configuration sources ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all config sources
    all_entries = list(registry)
    config_sources = [
        entry for entry in all_entries if entry.dimension == ComponentCategory.CONFIG_SOURCE.value
    ]

    # Sort by priority (highest first)
    config_sources.sort(key=lambda e: e.metadata.get("priority", 0), reverse=False)
    return config_sources


x_get_config_chain__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_config_chain__mutmut_1": x_get_config_chain__mutmut_1,
    "x_get_config_chain__mutmut_2": x_get_config_chain__mutmut_2,
    "x_get_config_chain__mutmut_3": x_get_config_chain__mutmut_3,
    "x_get_config_chain__mutmut_4": x_get_config_chain__mutmut_4,
    "x_get_config_chain__mutmut_5": x_get_config_chain__mutmut_5,
    "x_get_config_chain__mutmut_6": x_get_config_chain__mutmut_6,
    "x_get_config_chain__mutmut_7": x_get_config_chain__mutmut_7,
    "x_get_config_chain__mutmut_8": x_get_config_chain__mutmut_8,
    "x_get_config_chain__mutmut_9": x_get_config_chain__mutmut_9,
    "x_get_config_chain__mutmut_10": x_get_config_chain__mutmut_10,
    "x_get_config_chain__mutmut_11": x_get_config_chain__mutmut_11,
    "x_get_config_chain__mutmut_12": x_get_config_chain__mutmut_12,
    "x_get_config_chain__mutmut_13": x_get_config_chain__mutmut_13,
    "x_get_config_chain__mutmut_14": x_get_config_chain__mutmut_14,
    "x_get_config_chain__mutmut_15": x_get_config_chain__mutmut_15,
    "x_get_config_chain__mutmut_16": x_get_config_chain__mutmut_16,
    "x_get_config_chain__mutmut_17": x_get_config_chain__mutmut_17,
    "x_get_config_chain__mutmut_18": x_get_config_chain__mutmut_18,
}


def get_config_chain(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_config_chain__mutmut_orig, x_get_config_chain__mutmut_mutants, args, kwargs
    )
    return result


get_config_chain.__signature__ = _mutmut_signature(x_get_config_chain__mutmut_orig)
x_get_config_chain__mutmut_orig.__name__ = "x_get_config_chain"


@resilient(fallback={}, context_provider=lambda: {"function": "load_all_configs"})
async def load_all_configs() -> dict[str, Any]:
    """Load configurations from all registered sources."""
    configs = {}
    chain = get_config_chain()

    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                if inspect.iscoroutinefunction(source.load_config):
                    source_config = await source.load_config()
                else:
                    source_config = source.load_config()

                if source_config:
                    configs.update(source_config)
            except Exception as e:
                get_foundation_logger().warning(
                    "Config source failed to load", source=entry.name, error=str(e)
                )

    return configs


def x_load_config_from_registry__mutmut_orig(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_1(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = None

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_2(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = None

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_3(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = None
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_4(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = None
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_5(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(None, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_6(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, None):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_7(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr("load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_8(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(
            source,
        ):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_9(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "XXload_configXX"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_10(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "LOAD_CONFIG"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_11(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(None):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_12(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        None,
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_13(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=None,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_14(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_15(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_16(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "XXSkipping async config source in sync contextXX",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_17(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_18(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "SKIPPING ASYNC CONFIG SOURCE IN SYNC CONTEXT",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_19(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    break

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_20(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = None
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_21(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(None)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_22(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    None,
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_23(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=None,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_24(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=None,
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_25(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_26(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_27(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_28(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "XXFailed to load config from sourceXX",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_29(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_30(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "FAILED TO LOAD CONFIG FROM SOURCE",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_31(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(None),
                )

    # Create config instance
    return config_class.from_dict(config_data)


def x_load_config_from_registry__mutmut_32(config_class: type[T]) -> T:
    """Load configuration from registry sources.

    Args:
        config_class: Configuration class to instantiate

    Returns:
        Configuration instance loaded from registry sources

    """
    _registry, _ComponentCategory = _get_registry_and_lock()

    # Get configuration data from registry
    config_data = {}

    # Load from all config sources
    chain = get_config_chain()
    for entry in chain:
        source = entry.value
        if hasattr(source, "load_config"):
            try:
                # Skip async sources in sync context
                if inspect.iscoroutinefunction(source.load_config):
                    get_foundation_logger().debug(
                        "Skipping async config source in sync context",
                        source=entry.name,
                    )
                    continue

                source_data = source.load_config()
                if source_data:
                    config_data.update(source_data)
            except Exception as e:
                get_foundation_logger().warning(
                    "Failed to load config from source",
                    source=entry.name,
                    error=str(e),
                )

    # Create config instance
    return config_class.from_dict(None)


x_load_config_from_registry__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_config_from_registry__mutmut_1": x_load_config_from_registry__mutmut_1,
    "x_load_config_from_registry__mutmut_2": x_load_config_from_registry__mutmut_2,
    "x_load_config_from_registry__mutmut_3": x_load_config_from_registry__mutmut_3,
    "x_load_config_from_registry__mutmut_4": x_load_config_from_registry__mutmut_4,
    "x_load_config_from_registry__mutmut_5": x_load_config_from_registry__mutmut_5,
    "x_load_config_from_registry__mutmut_6": x_load_config_from_registry__mutmut_6,
    "x_load_config_from_registry__mutmut_7": x_load_config_from_registry__mutmut_7,
    "x_load_config_from_registry__mutmut_8": x_load_config_from_registry__mutmut_8,
    "x_load_config_from_registry__mutmut_9": x_load_config_from_registry__mutmut_9,
    "x_load_config_from_registry__mutmut_10": x_load_config_from_registry__mutmut_10,
    "x_load_config_from_registry__mutmut_11": x_load_config_from_registry__mutmut_11,
    "x_load_config_from_registry__mutmut_12": x_load_config_from_registry__mutmut_12,
    "x_load_config_from_registry__mutmut_13": x_load_config_from_registry__mutmut_13,
    "x_load_config_from_registry__mutmut_14": x_load_config_from_registry__mutmut_14,
    "x_load_config_from_registry__mutmut_15": x_load_config_from_registry__mutmut_15,
    "x_load_config_from_registry__mutmut_16": x_load_config_from_registry__mutmut_16,
    "x_load_config_from_registry__mutmut_17": x_load_config_from_registry__mutmut_17,
    "x_load_config_from_registry__mutmut_18": x_load_config_from_registry__mutmut_18,
    "x_load_config_from_registry__mutmut_19": x_load_config_from_registry__mutmut_19,
    "x_load_config_from_registry__mutmut_20": x_load_config_from_registry__mutmut_20,
    "x_load_config_from_registry__mutmut_21": x_load_config_from_registry__mutmut_21,
    "x_load_config_from_registry__mutmut_22": x_load_config_from_registry__mutmut_22,
    "x_load_config_from_registry__mutmut_23": x_load_config_from_registry__mutmut_23,
    "x_load_config_from_registry__mutmut_24": x_load_config_from_registry__mutmut_24,
    "x_load_config_from_registry__mutmut_25": x_load_config_from_registry__mutmut_25,
    "x_load_config_from_registry__mutmut_26": x_load_config_from_registry__mutmut_26,
    "x_load_config_from_registry__mutmut_27": x_load_config_from_registry__mutmut_27,
    "x_load_config_from_registry__mutmut_28": x_load_config_from_registry__mutmut_28,
    "x_load_config_from_registry__mutmut_29": x_load_config_from_registry__mutmut_29,
    "x_load_config_from_registry__mutmut_30": x_load_config_from_registry__mutmut_30,
    "x_load_config_from_registry__mutmut_31": x_load_config_from_registry__mutmut_31,
    "x_load_config_from_registry__mutmut_32": x_load_config_from_registry__mutmut_32,
}


def load_config_from_registry(*args, **kwargs):
    result = _mutmut_trampoline(
        x_load_config_from_registry__mutmut_orig, x_load_config_from_registry__mutmut_mutants, args, kwargs
    )
    return result


load_config_from_registry.__signature__ = _mutmut_signature(x_load_config_from_registry__mutmut_orig)
x_load_config_from_registry__mutmut_orig.__name__ = "x_load_config_from_registry"


__all__ = [
    "get_config_chain",
    "load_all_configs",
    "load_config_from_registry",
    "resolve_config_value",
]


# <3 🧱🤝🌐🪄
