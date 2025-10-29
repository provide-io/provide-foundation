# provide/foundation/hub/processors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.hub.registry import RegistryEntry

"""Hub processor pipeline management utilities.

Provides functions for managing log processors and processing stages
in the Hub registry system.
"""
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


def _get_registry_and_lock() -> Any:
    """Get registry and ComponentCategory from components module."""
    from provide.foundation.hub.components import (
        ComponentCategory,
        get_component_registry,
    )

    return get_component_registry(), ComponentCategory


def x_get_processor_pipeline__mutmut_orig() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_1() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = None

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_2() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = None
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_3() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(None)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_4() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = None

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_5() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension != ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_6() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=None, reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_7() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=None)
    return processors


def x_get_processor_pipeline__mutmut_8() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_9() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(
        key=lambda e: e.metadata.get("priority", 0),
    )
    return processors


def x_get_processor_pipeline__mutmut_10() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: None, reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_11() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get(None, 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_12() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", None), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_13() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get(0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_14() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(
        key=lambda e: e.metadata.get(
            "priority",
        ),
        reverse=True,
    )
    return processors


def x_get_processor_pipeline__mutmut_15() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("XXpriorityXX", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_16() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("PRIORITY", 0), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_17() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 1), reverse=True)
    return processors


def x_get_processor_pipeline__mutmut_18() -> list[RegistryEntry]:
    """Get log processors ordered by priority."""
    registry, ComponentCategory = _get_registry_and_lock()

    # Get all processors
    all_entries = list(registry)
    processors = [entry for entry in all_entries if entry.dimension == ComponentCategory.PROCESSOR.value]

    # Sort by priority (highest first)
    processors.sort(key=lambda e: e.metadata.get("priority", 0), reverse=False)
    return processors


x_get_processor_pipeline__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_processor_pipeline__mutmut_1": x_get_processor_pipeline__mutmut_1,
    "x_get_processor_pipeline__mutmut_2": x_get_processor_pipeline__mutmut_2,
    "x_get_processor_pipeline__mutmut_3": x_get_processor_pipeline__mutmut_3,
    "x_get_processor_pipeline__mutmut_4": x_get_processor_pipeline__mutmut_4,
    "x_get_processor_pipeline__mutmut_5": x_get_processor_pipeline__mutmut_5,
    "x_get_processor_pipeline__mutmut_6": x_get_processor_pipeline__mutmut_6,
    "x_get_processor_pipeline__mutmut_7": x_get_processor_pipeline__mutmut_7,
    "x_get_processor_pipeline__mutmut_8": x_get_processor_pipeline__mutmut_8,
    "x_get_processor_pipeline__mutmut_9": x_get_processor_pipeline__mutmut_9,
    "x_get_processor_pipeline__mutmut_10": x_get_processor_pipeline__mutmut_10,
    "x_get_processor_pipeline__mutmut_11": x_get_processor_pipeline__mutmut_11,
    "x_get_processor_pipeline__mutmut_12": x_get_processor_pipeline__mutmut_12,
    "x_get_processor_pipeline__mutmut_13": x_get_processor_pipeline__mutmut_13,
    "x_get_processor_pipeline__mutmut_14": x_get_processor_pipeline__mutmut_14,
    "x_get_processor_pipeline__mutmut_15": x_get_processor_pipeline__mutmut_15,
    "x_get_processor_pipeline__mutmut_16": x_get_processor_pipeline__mutmut_16,
    "x_get_processor_pipeline__mutmut_17": x_get_processor_pipeline__mutmut_17,
    "x_get_processor_pipeline__mutmut_18": x_get_processor_pipeline__mutmut_18,
}


def get_processor_pipeline(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_processor_pipeline__mutmut_orig, x_get_processor_pipeline__mutmut_mutants, args, kwargs
    )
    return result


get_processor_pipeline.__signature__ = _mutmut_signature(x_get_processor_pipeline__mutmut_orig)
x_get_processor_pipeline__mutmut_orig.__name__ = "x_get_processor_pipeline"


def x_get_processors_for_stage__mutmut_orig(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("stage") == stage]


def x_get_processors_for_stage__mutmut_1(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = None
    return [entry for entry in pipeline if entry.metadata.get("stage") == stage]


def x_get_processors_for_stage__mutmut_2(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get(None) == stage]


def x_get_processors_for_stage__mutmut_3(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("XXstageXX") == stage]


def x_get_processors_for_stage__mutmut_4(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("STAGE") == stage]


def x_get_processors_for_stage__mutmut_5(stage: str) -> list[RegistryEntry]:
    """Get processors for a specific processing stage."""
    pipeline = get_processor_pipeline()
    return [entry for entry in pipeline if entry.metadata.get("stage") != stage]


x_get_processors_for_stage__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_processors_for_stage__mutmut_1": x_get_processors_for_stage__mutmut_1,
    "x_get_processors_for_stage__mutmut_2": x_get_processors_for_stage__mutmut_2,
    "x_get_processors_for_stage__mutmut_3": x_get_processors_for_stage__mutmut_3,
    "x_get_processors_for_stage__mutmut_4": x_get_processors_for_stage__mutmut_4,
    "x_get_processors_for_stage__mutmut_5": x_get_processors_for_stage__mutmut_5,
}


def get_processors_for_stage(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_processors_for_stage__mutmut_orig, x_get_processors_for_stage__mutmut_mutants, args, kwargs
    )
    return result


get_processors_for_stage.__signature__ = _mutmut_signature(x_get_processors_for_stage__mutmut_orig)
x_get_processors_for_stage__mutmut_orig.__name__ = "x_get_processors_for_stage"


__all__ = [
    "get_processor_pipeline",
    "get_processors_for_stage",
]


# <3 🧱🤝🌐🪄
