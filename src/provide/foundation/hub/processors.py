#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.hub.registry import RegistryEntry

"""Hub processor pipeline management utilities.

Provides functions for managing log processors and processing stages
in the Hub registry system.
"""


def _get_registry_and_lock() -> Any:
    """Get registry and ComponentCategory from components module."""
    from provide.foundation.hub.components import (
        ComponentCategory,
        get_component_registry,
    )

    return get_component_registry(), ComponentCategory


def get_processor_pipeline() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def get_processors_for_stage(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("stage") == stage]


__all__ = [
    "get_processor_pipeline",
    "get_processors_for_stage",
]

# 🧱🏗️🔚
