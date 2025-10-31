#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any, Never

from provide.foundation.errors import DependencyError

"""Utilities for creating dependency stubs with helpful error messages."""


def create_dependency_stub(package: str, feature: str) -> type:
    """Create a stub class that raises DependencyError on instantiation or use.

    Args:
        package: Name of the missing package (e.g., "httpx", "cryptography")
        feature: Foundation feature name (e.g., "transport", "crypto")

    Returns:
        A stub class that raises DependencyError when instantiated or used

    Example:
        >>> HTTPTransport = create_dependency_stub("httpx", "transport")
        >>> transport = HTTPTransport()  # Raises DependencyError with install instructions
    """

    class DependencyStub:
        """Stub class for missing optional dependency."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise DependencyError(package, feature=feature)

        def __new__(cls, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        @classmethod
        def __class_getitem__(cls, item: Any) -> Never:
            raise DependencyError(package, feature=feature)

    DependencyStub.__name__ = f"{feature.capitalize()}Stub"
    DependencyStub.__qualname__ = f"{feature.capitalize()}Stub"

    return DependencyStub


def create_function_stub(package: str, feature: str) -> Any:
    """Create a stub function that raises DependencyError when called.

    Args:
        package: Name of the missing package (e.g., "httpx", "mkdocs")
        feature: Foundation feature name (e.g., "transport", "docs")

    Returns:
        A stub function that raises DependencyError when called

    Example:
        >>> generate_docs = create_function_stub("mkdocs", "docs")
        >>> generate_docs()  # Raises DependencyError with install instructions
    """

    def stub_function(*args: Any, **kwargs: Any) -> Never:
        raise DependencyError(package, feature=feature)

    stub_function.__name__ = f"{feature}_stub"
    stub_function.__qualname__ = f"{feature}_stub"

    return stub_function


def create_module_stub(package: str, feature: str) -> Any:
    """Create a stub module-like object that raises DependencyError on attribute access.

    Args:
        package: Name of the missing package (e.g., "httpx")
        feature: Foundation feature name (e.g., "transport")

    Returns:
        A stub object that raises DependencyError on any attribute access

    Example:
        >>> httpx = create_module_stub("httpx", "transport")
        >>> httpx.AsyncClient()  # Raises DependencyError with install instructions
    """

    class ModuleStub:
        """Stub module for missing optional dependency."""

        def __getattr__(self, name: str) -> Never:
            raise DependencyError(package, feature=feature)

        def __call__(self, *args: Any, **kwargs: Any) -> Never:
            raise DependencyError(package, feature=feature)

    ModuleStub.__name__ = f"{package}_stub"
    ModuleStub.__qualname__ = f"{package}_stub"

    return ModuleStub()


__all__ = [
    "create_dependency_stub",
    "create_function_stub",
    "create_module_stub",
]

# 🧱🏗️🔚
