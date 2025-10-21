# provide/foundation/utils/importer.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import sys
import threading

"""Lazy module importing utilities.

This module provides thread-safe lazy loading of optional modules to reduce
initial import overhead. It includes safeguards against circular imports,
import depth limits, and corrupted module states.
"""

# Thread-local storage for recursion guard to ensure thread safety
_thread_local = threading.local()

# Maximum depth for nested lazy imports to prevent stack overflow
MAX_LAZY_IMPORT_DEPTH = 5

# Modules that require special error handling with helpful install messages
SPECIAL_MODULES = {
    "cli": "CLI features require optional dependencies. Install with: pip install 'provide-foundation[cli]'",
    "transport": "HTTP/HTTPS transport requires optional dependencies. Install with: pip install 'provide-foundation[transport]'",
    "docs": "Documentation generation requires optional dependencies. Install with: pip install 'provide-foundation[docs]'",
}
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


def x_lazy_import__mutmut_orig(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_1(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = None

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_2(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_3(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(None, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_4(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, None):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_5(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr("getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_6(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, ):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_7(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "XXgetattr_in_progressXX"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_8(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "GETATTR_IN_PROGRESS"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_9(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = None
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_10(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = None
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_11(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 1
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_12(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = None

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_13(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth > MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_14(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = None
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_15(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join(None)
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_16(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = "XX -> XX".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_17(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            None
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_18(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name not in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_19(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = None
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_20(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join(None)
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_21(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = "XX -> XX".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_22(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            None
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_23(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(None)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_24(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth = 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_25(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth -= 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_26(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 2
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_27(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(None)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_28(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name not in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_29(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = None
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_30(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_31(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = None
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_32(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(None, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_33(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=None)
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_34(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_35(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, )
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_36(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=["XXXX"])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_37(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = None
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_38(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name not in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_39(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = None
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_40(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(None)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_41(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str) and (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_42(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str) and (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_43(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" or "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_44(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name != "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_45(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "XXcliXX" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_46(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "CLI" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_47(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "XXclickXX" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_48(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "CLICK" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_49(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" not in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_50(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" or "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_51(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name != "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_52(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "XXtransportXX" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_53(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "TRANSPORT" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_54(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "XXhttpxXX" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_55(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "HTTPX" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_56(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" not in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_57(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" or ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_58(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name != "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_59(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "XXdocsXX" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_60(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "DOCS" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_61(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str and "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_62(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("XXmkdocsXX" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_63(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("MKDOCS" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_64(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" not in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_65(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "XXmkdocstringsXX" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_66(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "MKDOCSTRINGS" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_67(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" not in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_68(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(None) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_69(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(None)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_70(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth = 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_71(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth += 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_72(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 2
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_73(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain or _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_74(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[+1] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_75(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-2] == name:
            _thread_local.import_chain.pop()


def x_lazy_import__mutmut_76(parent_module: str, name: str) -> object:
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)

    Commonly lazy-loaded modules:
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection
    - observability: Observability features

    Args:
        parent_module: The parent module name (e.g., "provide.foundation")
        name: Module name to lazy-load (e.g., "cli")

    Returns:
        The imported module

    Raises:
        AttributeError: If module is not allowed for lazy loading or circular import detected
        ImportError: If module import fails
        RecursionError: If import depth exceeds safe limits

    Note:
        Complexity is intentionally high to handle all edge cases
        in this critical import hook (recursion, corruption, depth limits).

    Example:
        >>> from provide.foundation.utils.importer import lazy_import
        >>> cli = lazy_import("provide.foundation", "cli")
    """
    # Build the full module name
    module_name = f"{parent_module}.{name}"

    # Initialize thread-local state if needed
    if not hasattr(_thread_local, "getattr_in_progress"):
        _thread_local.getattr_in_progress = set()
        _thread_local.import_depth = 0
        _thread_local.import_chain = []

    # Check recursion depth to prevent stack overflow from complex import chains
    if _thread_local.import_depth >= MAX_LAZY_IMPORT_DEPTH:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise RecursionError(
            f"Lazy import depth limit ({MAX_LAZY_IMPORT_DEPTH}) exceeded. "
            f"Import chain: {chain_str}. This indicates a complex nested import "
            f"that should be refactored or imported eagerly."
        )

    # Check if we've already entered recursion for this specific module
    # This prevents infinite loops when a module has been corrupted
    if name in _thread_local.getattr_in_progress:
        chain_str = " -> ".join([*_thread_local.import_chain, name])
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}' "
            f"(circular import detected in chain: {chain_str}). "
            f"Module may be corrupted in sys.modules."
        )

    # Set recursion guards
    _thread_local.getattr_in_progress.add(name)
    _thread_local.import_depth += 1
    _thread_local.import_chain.append(name)

    try:
        # Check if module is already in sys.modules but corrupted
        if module_name in sys.modules:
            existing_module = sys.modules[module_name]
            # If it exists and is valid, return it
            if existing_module is not None:
                return existing_module
            # If it's None or invalid, remove it so we can re-import
            del sys.modules[module_name]

        # Import the submodule with appropriate error handling
        try:
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
        except ImportError as e:
            # Provide helpful error messages for known optional dependencies
            if name in SPECIAL_MODULES:
                error_str = str(e)
                # Check if error is about missing dependency for this feature
                if (
                    (name == "cli" and "click" in error_str)
                    or (name == "transport" and "httpx" in error_str)
                    or (name == "docs" and ("mkdocs" in error_str or "mkdocstrings" in error_str))
                ):
                    raise ImportError(SPECIAL_MODULES[name]) from e
            raise
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] != name:
            _thread_local.import_chain.pop()

x_lazy_import__mutmut_mutants : ClassVar[MutantDict] = {
'x_lazy_import__mutmut_1': x_lazy_import__mutmut_1, 
    'x_lazy_import__mutmut_2': x_lazy_import__mutmut_2, 
    'x_lazy_import__mutmut_3': x_lazy_import__mutmut_3, 
    'x_lazy_import__mutmut_4': x_lazy_import__mutmut_4, 
    'x_lazy_import__mutmut_5': x_lazy_import__mutmut_5, 
    'x_lazy_import__mutmut_6': x_lazy_import__mutmut_6, 
    'x_lazy_import__mutmut_7': x_lazy_import__mutmut_7, 
    'x_lazy_import__mutmut_8': x_lazy_import__mutmut_8, 
    'x_lazy_import__mutmut_9': x_lazy_import__mutmut_9, 
    'x_lazy_import__mutmut_10': x_lazy_import__mutmut_10, 
    'x_lazy_import__mutmut_11': x_lazy_import__mutmut_11, 
    'x_lazy_import__mutmut_12': x_lazy_import__mutmut_12, 
    'x_lazy_import__mutmut_13': x_lazy_import__mutmut_13, 
    'x_lazy_import__mutmut_14': x_lazy_import__mutmut_14, 
    'x_lazy_import__mutmut_15': x_lazy_import__mutmut_15, 
    'x_lazy_import__mutmut_16': x_lazy_import__mutmut_16, 
    'x_lazy_import__mutmut_17': x_lazy_import__mutmut_17, 
    'x_lazy_import__mutmut_18': x_lazy_import__mutmut_18, 
    'x_lazy_import__mutmut_19': x_lazy_import__mutmut_19, 
    'x_lazy_import__mutmut_20': x_lazy_import__mutmut_20, 
    'x_lazy_import__mutmut_21': x_lazy_import__mutmut_21, 
    'x_lazy_import__mutmut_22': x_lazy_import__mutmut_22, 
    'x_lazy_import__mutmut_23': x_lazy_import__mutmut_23, 
    'x_lazy_import__mutmut_24': x_lazy_import__mutmut_24, 
    'x_lazy_import__mutmut_25': x_lazy_import__mutmut_25, 
    'x_lazy_import__mutmut_26': x_lazy_import__mutmut_26, 
    'x_lazy_import__mutmut_27': x_lazy_import__mutmut_27, 
    'x_lazy_import__mutmut_28': x_lazy_import__mutmut_28, 
    'x_lazy_import__mutmut_29': x_lazy_import__mutmut_29, 
    'x_lazy_import__mutmut_30': x_lazy_import__mutmut_30, 
    'x_lazy_import__mutmut_31': x_lazy_import__mutmut_31, 
    'x_lazy_import__mutmut_32': x_lazy_import__mutmut_32, 
    'x_lazy_import__mutmut_33': x_lazy_import__mutmut_33, 
    'x_lazy_import__mutmut_34': x_lazy_import__mutmut_34, 
    'x_lazy_import__mutmut_35': x_lazy_import__mutmut_35, 
    'x_lazy_import__mutmut_36': x_lazy_import__mutmut_36, 
    'x_lazy_import__mutmut_37': x_lazy_import__mutmut_37, 
    'x_lazy_import__mutmut_38': x_lazy_import__mutmut_38, 
    'x_lazy_import__mutmut_39': x_lazy_import__mutmut_39, 
    'x_lazy_import__mutmut_40': x_lazy_import__mutmut_40, 
    'x_lazy_import__mutmut_41': x_lazy_import__mutmut_41, 
    'x_lazy_import__mutmut_42': x_lazy_import__mutmut_42, 
    'x_lazy_import__mutmut_43': x_lazy_import__mutmut_43, 
    'x_lazy_import__mutmut_44': x_lazy_import__mutmut_44, 
    'x_lazy_import__mutmut_45': x_lazy_import__mutmut_45, 
    'x_lazy_import__mutmut_46': x_lazy_import__mutmut_46, 
    'x_lazy_import__mutmut_47': x_lazy_import__mutmut_47, 
    'x_lazy_import__mutmut_48': x_lazy_import__mutmut_48, 
    'x_lazy_import__mutmut_49': x_lazy_import__mutmut_49, 
    'x_lazy_import__mutmut_50': x_lazy_import__mutmut_50, 
    'x_lazy_import__mutmut_51': x_lazy_import__mutmut_51, 
    'x_lazy_import__mutmut_52': x_lazy_import__mutmut_52, 
    'x_lazy_import__mutmut_53': x_lazy_import__mutmut_53, 
    'x_lazy_import__mutmut_54': x_lazy_import__mutmut_54, 
    'x_lazy_import__mutmut_55': x_lazy_import__mutmut_55, 
    'x_lazy_import__mutmut_56': x_lazy_import__mutmut_56, 
    'x_lazy_import__mutmut_57': x_lazy_import__mutmut_57, 
    'x_lazy_import__mutmut_58': x_lazy_import__mutmut_58, 
    'x_lazy_import__mutmut_59': x_lazy_import__mutmut_59, 
    'x_lazy_import__mutmut_60': x_lazy_import__mutmut_60, 
    'x_lazy_import__mutmut_61': x_lazy_import__mutmut_61, 
    'x_lazy_import__mutmut_62': x_lazy_import__mutmut_62, 
    'x_lazy_import__mutmut_63': x_lazy_import__mutmut_63, 
    'x_lazy_import__mutmut_64': x_lazy_import__mutmut_64, 
    'x_lazy_import__mutmut_65': x_lazy_import__mutmut_65, 
    'x_lazy_import__mutmut_66': x_lazy_import__mutmut_66, 
    'x_lazy_import__mutmut_67': x_lazy_import__mutmut_67, 
    'x_lazy_import__mutmut_68': x_lazy_import__mutmut_68, 
    'x_lazy_import__mutmut_69': x_lazy_import__mutmut_69, 
    'x_lazy_import__mutmut_70': x_lazy_import__mutmut_70, 
    'x_lazy_import__mutmut_71': x_lazy_import__mutmut_71, 
    'x_lazy_import__mutmut_72': x_lazy_import__mutmut_72, 
    'x_lazy_import__mutmut_73': x_lazy_import__mutmut_73, 
    'x_lazy_import__mutmut_74': x_lazy_import__mutmut_74, 
    'x_lazy_import__mutmut_75': x_lazy_import__mutmut_75, 
    'x_lazy_import__mutmut_76': x_lazy_import__mutmut_76
}

def lazy_import(*args, **kwargs):
    result = _mutmut_trampoline(x_lazy_import__mutmut_orig, x_lazy_import__mutmut_mutants, args, kwargs)
    return result 

lazy_import.__signature__ = _mutmut_signature(x_lazy_import__mutmut_orig)
x_lazy_import__mutmut_orig.__name__ = 'x_lazy_import'


# <3 🧱🤝🧰🪄
