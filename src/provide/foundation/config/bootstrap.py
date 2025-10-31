#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Configuration schema discovery and registration for bootstrap.

This module provides functionality to discover all RuntimeConfig subclasses
and register them with the Hub's CONFIG_SCHEMA dimension during bootstrap."""

from __future__ import annotations

import importlib

from attrs import fields

from provide.foundation.config.env import RuntimeConfig


def _import_config_modules() -> None:
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


def _get_all_subclasses(cls: type) -> set[type]:
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


def discover_and_register_configs() -> None:
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


# 🧱🏗️🔚
