#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Dependency-related exceptions."""

from typing import Any

from provide.foundation.errors.base import FoundationError


class DependencyError(FoundationError):
    """Raised when an optional dependency is required but not installed.

    Args:
        package: Name of the missing package
        feature: Optional feature name that requires the package
        install_command: Optional custom installation command
        **kwargs: Additional context passed to FoundationError

    Examples:
        >>> raise DependencyError("cryptography", feature="crypto")
        >>> raise DependencyError("requests", install_command="pip install requests")

    """

    def __init__(
        self,
        package: str,
        *,
        feature: str | None = None,
        install_command: str | None = None,
        **kwargs: Any,
    ) -> None:
        # Determine the installation command
        # Feature takes priority over custom install_command
        if feature:
            cmd = f"pip install 'provide-foundation[{feature}]'"
        elif install_command:
            cmd = install_command
        else:
            cmd = f"pip install {package}"

        # Create the error message
        message = f"Optional dependency '{package}' is required for this feature. Install with: {cmd}"

        # Add context
        context = kwargs.setdefault("context", {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "DEPENDENCY_MISSING"


class DependencyMismatchError(FoundationError):
    """Raised when a dependency version doesn't meet requirements.

    Args:
        package: Name of the package with version mismatch
        required_version: Required version or constraint
        current_version: Currently installed version
        **kwargs: Additional context passed to FoundationError

    Examples:
        >>> raise DependencyMismatchError("cryptography", ">=3.0.0", "2.9.2")

    """

    def __init__(
        self,
        package: str,
        *,
        required_version: str,
        current_version: str,
        **kwargs: Any,
    ) -> None:
        message = (
            f"Package '{package}' version {current_version} does not meet "
            f"requirement {required_version}. Please upgrade with: "
            f"pip install '{package}{required_version}'"
        )

        # Add context
        context = kwargs.setdefault("context", {})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def _default_code(self) -> str:
        return "DEPENDENCY_VERSION_MISMATCH"


# 🧱🏗️🔚
