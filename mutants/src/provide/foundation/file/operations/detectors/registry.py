# provide/foundation/file/operations/detectors/registry.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Registry for file operation detectors."""

from __future__ import annotations

from provide.foundation.file.operations.detectors.protocol import DetectorFunc
from provide.foundation.hub.registry import Registry

"""File operation detector registry.

Provides a centralized registry for file operation detector functions,
allowing both built-in and custom detectors to be registered with priorities.
"""

_detector_registry: Registry | None = None
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_get_detector_registry__mutmut_orig() -> Registry:
    """Get the global detector registry singleton.

    Returns:
        Registry instance for file operation detectors
    """
    global _detector_registry
    if _detector_registry is None:
        _detector_registry = Registry()
    return _detector_registry


def x_get_detector_registry__mutmut_1() -> Registry:
    """Get the global detector registry singleton.

    Returns:
        Registry instance for file operation detectors
    """
    global _detector_registry
    if _detector_registry is not None:
        _detector_registry = Registry()
    return _detector_registry


def x_get_detector_registry__mutmut_2() -> Registry:
    """Get the global detector registry singleton.

    Returns:
        Registry instance for file operation detectors
    """
    global _detector_registry
    if _detector_registry is None:
        _detector_registry = None
    return _detector_registry

x_get_detector_registry__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_detector_registry__mutmut_1': x_get_detector_registry__mutmut_1, 
    'x_get_detector_registry__mutmut_2': x_get_detector_registry__mutmut_2
}

def get_detector_registry(*args, **kwargs):
    result = _mutmut_trampoline(x_get_detector_registry__mutmut_orig, x_get_detector_registry__mutmut_mutants, args, kwargs)
    return result 

get_detector_registry.__signature__ = _mutmut_signature(x_get_detector_registry__mutmut_orig)
x_get_detector_registry__mutmut_orig.__name__ = 'x_get_detector_registry'


def x_register_detector__mutmut_orig(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_1(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "XXXX",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_2(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = None
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_3(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=None,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_4(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=None,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_5(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension=None,
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_6(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata=None,
    )


def x_register_detector__mutmut_7(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_8(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_9(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_10(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        )


def x_register_detector__mutmut_11(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="XXfile_operation_detectorXX",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_12(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="FILE_OPERATION_DETECTOR",
        metadata={
            "priority": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_13(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "XXpriorityXX": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_14(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "PRIORITY": priority,
            "description": description,
        },
    )


def x_register_detector__mutmut_15(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "XXdescriptionXX": description,
        },
    )


def x_register_detector__mutmut_16(
    name: str,
    func: DetectorFunc,
    priority: int,
    description: str = "",
) -> None:
    """Register a file operation detector function.

    Args:
        name: Unique detector name (e.g., "detect_atomic_save")
        func: Detector function conforming to DetectorFunc protocol
        priority: Execution priority (0-100, higher = earlier execution)
        description: Human-readable description of what pattern is detected

    Raises:
        AlreadyExistsError: If detector name already registered

    Example:
        >>> def detect_custom_pattern(events):
        ...     # Custom detection logic
        ...     return FileOperation(...) if pattern_found else None
        >>>
        >>> register_detector(
        ...     name="detect_custom",
        ...     func=detect_custom_pattern,
        ...     priority=75,
        ...     description="Detects custom file operation pattern"
        ... )
    """
    registry = get_detector_registry()
    registry.register(
        name=name,
        value=func,
        dimension="file_operation_detector",
        metadata={
            "priority": priority,
            "DESCRIPTION": description,
        },
    )

x_register_detector__mutmut_mutants : ClassVar[MutantDict] = {
'x_register_detector__mutmut_1': x_register_detector__mutmut_1, 
    'x_register_detector__mutmut_2': x_register_detector__mutmut_2, 
    'x_register_detector__mutmut_3': x_register_detector__mutmut_3, 
    'x_register_detector__mutmut_4': x_register_detector__mutmut_4, 
    'x_register_detector__mutmut_5': x_register_detector__mutmut_5, 
    'x_register_detector__mutmut_6': x_register_detector__mutmut_6, 
    'x_register_detector__mutmut_7': x_register_detector__mutmut_7, 
    'x_register_detector__mutmut_8': x_register_detector__mutmut_8, 
    'x_register_detector__mutmut_9': x_register_detector__mutmut_9, 
    'x_register_detector__mutmut_10': x_register_detector__mutmut_10, 
    'x_register_detector__mutmut_11': x_register_detector__mutmut_11, 
    'x_register_detector__mutmut_12': x_register_detector__mutmut_12, 
    'x_register_detector__mutmut_13': x_register_detector__mutmut_13, 
    'x_register_detector__mutmut_14': x_register_detector__mutmut_14, 
    'x_register_detector__mutmut_15': x_register_detector__mutmut_15, 
    'x_register_detector__mutmut_16': x_register_detector__mutmut_16
}

def register_detector(*args, **kwargs):
    result = _mutmut_trampoline(x_register_detector__mutmut_orig, x_register_detector__mutmut_mutants, args, kwargs)
    return result 

register_detector.__signature__ = _mutmut_signature(x_register_detector__mutmut_orig)
x_register_detector__mutmut_orig.__name__ = 'x_register_detector'


def x_get_all_detectors__mutmut_orig() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_1() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = None

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_2() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = None

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_3() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension != "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_4() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "XXfile_operation_detectorXX"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_5() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "FILE_OPERATION_DETECTOR"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_6() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = None

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_7() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        None,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_8() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=None,
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_9() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=None,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_10() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_11() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_12() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_13() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: None,
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_14() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get(None, 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_15() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", None),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_16() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get(0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_17() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", ),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_18() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("XXpriorityXX", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_19() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("PRIORITY", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_20() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 1),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_21() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=False,
    )

    return [(e.name, e.value, e.metadata.get("priority", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_22() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get(None, 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_23() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", None)) for e in sorted_entries]


def x_get_all_detectors__mutmut_24() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get(0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_25() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", )) for e in sorted_entries]


def x_get_all_detectors__mutmut_26() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("XXpriorityXX", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_27() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("PRIORITY", 0)) for e in sorted_entries]


def x_get_all_detectors__mutmut_28() -> list[tuple[str, DetectorFunc, int]]:
    """Get all registered detectors sorted by priority (highest first).

    Returns:
        List of tuples: (name, detector_func, priority)
    """
    registry = get_detector_registry()

    # Collect all entries from the file_operation_detector dimension
    entries = [entry for entry in registry if entry.dimension == "file_operation_detector"]

    # Sort by priority (highest first)
    sorted_entries = sorted(
        entries,
        key=lambda e: e.metadata.get("priority", 0),
        reverse=True,
    )

    return [(e.name, e.value, e.metadata.get("priority", 1)) for e in sorted_entries]

x_get_all_detectors__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_all_detectors__mutmut_1': x_get_all_detectors__mutmut_1, 
    'x_get_all_detectors__mutmut_2': x_get_all_detectors__mutmut_2, 
    'x_get_all_detectors__mutmut_3': x_get_all_detectors__mutmut_3, 
    'x_get_all_detectors__mutmut_4': x_get_all_detectors__mutmut_4, 
    'x_get_all_detectors__mutmut_5': x_get_all_detectors__mutmut_5, 
    'x_get_all_detectors__mutmut_6': x_get_all_detectors__mutmut_6, 
    'x_get_all_detectors__mutmut_7': x_get_all_detectors__mutmut_7, 
    'x_get_all_detectors__mutmut_8': x_get_all_detectors__mutmut_8, 
    'x_get_all_detectors__mutmut_9': x_get_all_detectors__mutmut_9, 
    'x_get_all_detectors__mutmut_10': x_get_all_detectors__mutmut_10, 
    'x_get_all_detectors__mutmut_11': x_get_all_detectors__mutmut_11, 
    'x_get_all_detectors__mutmut_12': x_get_all_detectors__mutmut_12, 
    'x_get_all_detectors__mutmut_13': x_get_all_detectors__mutmut_13, 
    'x_get_all_detectors__mutmut_14': x_get_all_detectors__mutmut_14, 
    'x_get_all_detectors__mutmut_15': x_get_all_detectors__mutmut_15, 
    'x_get_all_detectors__mutmut_16': x_get_all_detectors__mutmut_16, 
    'x_get_all_detectors__mutmut_17': x_get_all_detectors__mutmut_17, 
    'x_get_all_detectors__mutmut_18': x_get_all_detectors__mutmut_18, 
    'x_get_all_detectors__mutmut_19': x_get_all_detectors__mutmut_19, 
    'x_get_all_detectors__mutmut_20': x_get_all_detectors__mutmut_20, 
    'x_get_all_detectors__mutmut_21': x_get_all_detectors__mutmut_21, 
    'x_get_all_detectors__mutmut_22': x_get_all_detectors__mutmut_22, 
    'x_get_all_detectors__mutmut_23': x_get_all_detectors__mutmut_23, 
    'x_get_all_detectors__mutmut_24': x_get_all_detectors__mutmut_24, 
    'x_get_all_detectors__mutmut_25': x_get_all_detectors__mutmut_25, 
    'x_get_all_detectors__mutmut_26': x_get_all_detectors__mutmut_26, 
    'x_get_all_detectors__mutmut_27': x_get_all_detectors__mutmut_27, 
    'x_get_all_detectors__mutmut_28': x_get_all_detectors__mutmut_28
}

def get_all_detectors(*args, **kwargs):
    result = _mutmut_trampoline(x_get_all_detectors__mutmut_orig, x_get_all_detectors__mutmut_mutants, args, kwargs)
    return result 

get_all_detectors.__signature__ = _mutmut_signature(x_get_all_detectors__mutmut_orig)
x_get_all_detectors__mutmut_orig.__name__ = 'x_get_all_detectors'


def x_clear_detector_registry__mutmut_orig() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = get_detector_registry()
    registry.clear("file_operation_detector")


def x_clear_detector_registry__mutmut_1() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = None
    registry.clear("file_operation_detector")


def x_clear_detector_registry__mutmut_2() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = get_detector_registry()
    registry.clear(None)


def x_clear_detector_registry__mutmut_3() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = get_detector_registry()
    registry.clear("XXfile_operation_detectorXX")


def x_clear_detector_registry__mutmut_4() -> None:
    """Clear all registered detectors (primarily for testing)."""
    registry = get_detector_registry()
    registry.clear("FILE_OPERATION_DETECTOR")

x_clear_detector_registry__mutmut_mutants : ClassVar[MutantDict] = {
'x_clear_detector_registry__mutmut_1': x_clear_detector_registry__mutmut_1, 
    'x_clear_detector_registry__mutmut_2': x_clear_detector_registry__mutmut_2, 
    'x_clear_detector_registry__mutmut_3': x_clear_detector_registry__mutmut_3, 
    'x_clear_detector_registry__mutmut_4': x_clear_detector_registry__mutmut_4
}

def clear_detector_registry(*args, **kwargs):
    result = _mutmut_trampoline(x_clear_detector_registry__mutmut_orig, x_clear_detector_registry__mutmut_mutants, args, kwargs)
    return result 

clear_detector_registry.__signature__ = _mutmut_signature(x_clear_detector_registry__mutmut_orig)
x_clear_detector_registry__mutmut_orig.__name__ = 'x_clear_detector_registry'


__all__ = [
    "clear_detector_registry",
    "get_all_detectors",
    "get_detector_registry",
    "register_detector",
]


# <3 🧱🤝📄🪄
