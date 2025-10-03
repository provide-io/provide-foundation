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

# Modules that are safe to lazy-load (do not trigger recursive lookups)
# These modules have been verified to not cause import cycles
LAZY_LOADABLE_MODULES = frozenset(["cli", "crypto", "docs", "formatting", "metrics"])


def lazy_import(parent_module: str, name: str) -> object:  # noqa: C901
    """Import a module lazily with comprehensive safety checks.

    This function provides thread-safe lazy loading with protection against:
    - Circular imports (tracks import chains)
    - Stack overflow (enforces maximum depth)
    - Corrupted module states (validates sys.modules)
    - Invalid module requests (allowlist enforcement)

    Safe lazy-loaded modules (verified no import cycles):
    - cli: Requires optional 'click' dependency
    - crypto: Cryptographic utilities
    - docs: Documentation generation
    - formatting: Text formatting utilities
    - metrics: Metrics collection

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

    # Verify module is in the allowed lazy-load list
    if name not in LAZY_LOADABLE_MODULES:
        available = ", ".join(sorted(LAZY_LOADABLE_MODULES))
        raise AttributeError(
            f"module '{parent_module}' has no attribute '{name}'. "
            f"Only these modules support lazy loading: {available}"
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
        if name == "cli":
            try:
                mod = __import__(module_name, fromlist=[""])
                sys.modules[module_name] = mod
                return mod
            except ImportError as e:
                if "click" in str(e):
                    raise ImportError(
                        "CLI features require optional dependencies. Install with: "
                        "pip install 'provide-foundation[cli]'",
                    ) from e
                raise
        else:
            # Standard import for other allowed modules
            mod = __import__(module_name, fromlist=[""])
            sys.modules[module_name] = mod
            return mod
    finally:
        # Always clear recursion guards in reverse order
        _thread_local.getattr_in_progress.discard(name)
        _thread_local.import_depth -= 1
        if _thread_local.import_chain and _thread_local.import_chain[-1] == name:
            _thread_local.import_chain.pop()
