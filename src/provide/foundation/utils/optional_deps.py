#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

"""Centralized optional dependency handling with automatic stub creation.

This module provides utilities to handle optional dependencies in a DRY way,
reducing the repetitive try/except ImportError pattern across deps.py files.
"""


class OptionalDependency:
    """Handles loading of optional dependencies with automatic stub generation.

    This centralizes the try/except ImportError pattern and provides
    automatic stub creation when dependencies are missing.

    Examples:
        >>> # Simple package import
        >>> click_dep = OptionalDependency("click", "cli")
        >>> click = click_dep.import_package()
        >>> has_click = click_dep.is_available()

        >>> # Import specific symbols from a module
        >>> crypto_dep = OptionalDependency("cryptography", "crypto")
        >>> Certificate, create_self_signed = crypto_dep.import_symbols(
        ...     "provide.foundation.crypto.certificates",
        ...     ["Certificate", "create_self_signed"]
        ... )
    """

    def __init__(self, package_name: str, feature_name: str) -> None:
        """Initialize optional dependency handler.

        Args:
            package_name: Name of the optional package (e.g., "click", "cryptography")
            feature_name: Foundation feature name (e.g., "cli", "crypto")
        """
        self.package_name = package_name
        self.feature_name = feature_name
        self._available: bool | None = None

    def is_available(self) -> bool:
        """Check if the optional dependency is available.

        Returns:
            True if package can be imported, False otherwise
        """
        if self._available is None:
            try:
                __import__(self.package_name)
                self._available = True
            except ImportError:
                self._available = False
        return self._available

    def import_package(self) -> Any:
        """Import the package or return a stub module.

        Returns:
            The actual package if available, otherwise a stub that raises DependencyError

        Example:
            >>> dep = OptionalDependency("click", "cli")
            >>> click = dep.import_package()  # Real click module or stub
        """
        if self.is_available():
            return __import__(self.package_name)

        # Return stub module
        from provide.foundation.utils.stubs import create_module_stub

        return create_module_stub(self.package_name, self.feature_name)

    def import_symbols(
        self,
        module_path: str,
        symbols: list[str],
        *,
        create_stubs: bool = True,
    ) -> list[Any]:
        """Import specific symbols from a module or create stubs.

        Args:
            module_path: Full module path (e.g., "provide.foundation.crypto.certificates")
            symbols: List of symbol names to import
            create_stubs: Whether to create stubs for missing symbols (default: True)

        Returns:
            List of imported symbols or stubs in the same order as requested

        Example:
            >>> dep = OptionalDependency("cryptography", "crypto")
            >>> Certificate, CertificateConfig = dep.import_symbols(
            ...     "provide.foundation.crypto.certificates",
            ...     ["Certificate", "CertificateConfig"]
            ... )
        """
        try:
            module = __import__(module_path, fromlist=symbols)
            return [getattr(module, symbol) for symbol in symbols]
        except ImportError:
            if not create_stubs:
                raise

            # Create appropriate stubs
            from provide.foundation.utils.stubs import (
                create_dependency_stub,
                create_function_stub,
            )

            stubs = []
            for symbol in symbols:
                # Heuristic: if symbol starts with lowercase, it's likely a function
                if symbol[0].islower():
                    stubs.append(create_function_stub(self.package_name, self.feature_name))
                else:
                    stubs.append(create_dependency_stub(self.package_name, self.feature_name))

            return stubs


def load_optional_dependency(
    package_name: str,
    feature_name: str,
    *,
    module_path: str | None = None,
    symbols: list[str] | None = None,
) -> tuple[bool, Any | list[Any]]:
    """Convenience function to load an optional dependency.

    This is a one-shot function that combines availability checking
    and import/stub creation.

    Args:
        package_name: Name of the optional package
        feature_name: Foundation feature name
        module_path: Optional module path for importing specific symbols
        symbols: Optional list of symbols to import from module

    Returns:
        Tuple of (is_available, imported_content)
        - is_available: Boolean indicating if package is available
        - imported_content: Either the package/module or list of symbols/stubs

    Examples:
        >>> # Import entire package
        >>> has_click, click = load_optional_dependency("click", "cli")

        >>> # Import specific symbols
        >>> has_crypto, (Certificate, CertificateConfig) = load_optional_dependency(
        ...     "cryptography",
        ...     "crypto",
        ...     module_path="provide.foundation.crypto.certificates",
        ...     symbols=["Certificate", "CertificateConfig"]
        ... )
    """
    dep = OptionalDependency(package_name, feature_name)
    is_available = dep.is_available()

    if module_path and symbols:
        # Import specific symbols
        imported = dep.import_symbols(module_path, symbols)
        return is_available, imported

    # Import entire package
    imported = dep.import_package()
    return is_available, imported


__all__ = [
    "OptionalDependency",
    "load_optional_dependency",
]

# 🧱🏗️🔚
