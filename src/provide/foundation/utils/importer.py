#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def lazy_import(parent_module: str, name: str) -> object:
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


# 🧱🏗️🔚
