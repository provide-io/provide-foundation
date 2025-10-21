# provide/foundation/logger/factories.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# factories.py
#
import threading
from typing import Any

"""Logger factory functions and simple setup utilities.

Circular Dependency Mitigation
-------------------------------
This module uses thread-local state to break circular dependencies between
the logger and hub systems. The _is_initializing flag prevents recursive
imports during Foundation initialization.

Design Pattern:
1. Check thread-local flag to detect initialization recursion
2. If already initializing, return basic structlog logger (fast path)
3. Otherwise, attempt to get configured logger from Hub
4. On any error (ImportError, RecursionError), fall back to basic structlog
5. Always clear the flag in finally block to prevent state poisoning

This pattern allows modules to safely import get_logger() without creating
circular dependencies, at the cost of some initialization complexity.
"""

_is_initializing = threading.local()
# Maximum recursion depth before forcing fallback (safety limit)
_MAX_RECURSION_DEPTH = 3
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


def x_get_logger__mutmut_orig(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_1(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = None

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_2(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(None, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_3(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, None, 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_4(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", None)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_5(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr("depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_6(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_7(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", )

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_8(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "XXdepthXX", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_9(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "DEPTH", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_10(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 1)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_11(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth >= 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_12(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 1:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_13(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(None)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_14(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth > _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_15(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(None)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_16(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = None

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_17(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth - 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_18(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 2

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_19(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = None
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_20(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(None)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_21(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(None)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, depth)


def x_get_logger__mutmut_22(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = None


def x_get_logger__mutmut_23(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(None, depth)


def x_get_logger__mutmut_24(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, None)


def x_get_logger__mutmut_25(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(depth)


def x_get_logger__mutmut_26(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(0, )


def x_get_logger__mutmut_27(name: str | None = None) -> Any:
    """Get a logger instance through Hub with circular import protection.

    This function provides access to the global logger instance. It is preserved
    for backward compatibility but should be avoided in new application code in
    favor of explicit Dependency Injection.

    Circular Import Protection:
        Uses thread-local state to detect recursive initialization and falls
        back to basic structlog when circular dependencies are detected.

    Args:
        name: Logger name (e.g., __name__ from a module)

    Returns:
        Configured structlog logger instance

    Note:
        For building testable and maintainable applications, the recommended
        approach is to inject a logger instance via a `Container`. See the
        Dependency Injection guide for more information.
    """
    # Track recursion depth to prevent infinite loops
    depth = getattr(_is_initializing, "depth", 0)

    # Check if we're already in the middle of initialization to prevent circular import
    if depth > 0:
        # Already initializing - use fallback to break circular dependency
        import structlog

        return structlog.get_logger(name)

    # Safety check: enforce maximum recursion depth
    if depth >= _MAX_RECURSION_DEPTH:
        import structlog

        return structlog.get_logger(name)

    try:
        # Increment recursion depth
        _is_initializing.depth = depth + 1

        from provide.foundation.hub.manager import get_hub

        hub = get_hub()
        return hub.get_foundation_logger(name)
    except (ImportError, RecursionError):
        # Fallback to basic structlog if hub is not available or circular import detected
        import structlog

        return structlog.get_logger(name)
    finally:
        # Always decrement depth counter to allow future attempts
        _is_initializing.depth = max(1, depth)

x_get_logger__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_logger__mutmut_1': x_get_logger__mutmut_1, 
    'x_get_logger__mutmut_2': x_get_logger__mutmut_2, 
    'x_get_logger__mutmut_3': x_get_logger__mutmut_3, 
    'x_get_logger__mutmut_4': x_get_logger__mutmut_4, 
    'x_get_logger__mutmut_5': x_get_logger__mutmut_5, 
    'x_get_logger__mutmut_6': x_get_logger__mutmut_6, 
    'x_get_logger__mutmut_7': x_get_logger__mutmut_7, 
    'x_get_logger__mutmut_8': x_get_logger__mutmut_8, 
    'x_get_logger__mutmut_9': x_get_logger__mutmut_9, 
    'x_get_logger__mutmut_10': x_get_logger__mutmut_10, 
    'x_get_logger__mutmut_11': x_get_logger__mutmut_11, 
    'x_get_logger__mutmut_12': x_get_logger__mutmut_12, 
    'x_get_logger__mutmut_13': x_get_logger__mutmut_13, 
    'x_get_logger__mutmut_14': x_get_logger__mutmut_14, 
    'x_get_logger__mutmut_15': x_get_logger__mutmut_15, 
    'x_get_logger__mutmut_16': x_get_logger__mutmut_16, 
    'x_get_logger__mutmut_17': x_get_logger__mutmut_17, 
    'x_get_logger__mutmut_18': x_get_logger__mutmut_18, 
    'x_get_logger__mutmut_19': x_get_logger__mutmut_19, 
    'x_get_logger__mutmut_20': x_get_logger__mutmut_20, 
    'x_get_logger__mutmut_21': x_get_logger__mutmut_21, 
    'x_get_logger__mutmut_22': x_get_logger__mutmut_22, 
    'x_get_logger__mutmut_23': x_get_logger__mutmut_23, 
    'x_get_logger__mutmut_24': x_get_logger__mutmut_24, 
    'x_get_logger__mutmut_25': x_get_logger__mutmut_25, 
    'x_get_logger__mutmut_26': x_get_logger__mutmut_26, 
    'x_get_logger__mutmut_27': x_get_logger__mutmut_27
}

def get_logger(*args, **kwargs):
    result = _mutmut_trampoline(x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs)
    return result 

get_logger.__signature__ = _mutmut_signature(x_get_logger__mutmut_orig)
x_get_logger__mutmut_orig.__name__ = 'x_get_logger'


# <3 🧱🤝📝🪄
