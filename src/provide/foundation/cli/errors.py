#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI adapter error classes.

Foundation-based errors for CLI adapter system."""

from __future__ import annotations

from provide.foundation.errors.base import FoundationError


class CLIError(FoundationError):
    """Base error for CLI adapter operations.

    Raised when CLI adapter operations fail.
    """

    def _default_code(self) -> str:
        """Return default error code."""
        return "CLI_ERROR"


class InvalidCLIHintError(CLIError):
    """Raised when an invalid CLI hint is provided in Annotated.

    This error occurs when a parameter uses typing.Annotated with an
    invalid CLI rendering hint. Valid hints are 'option' and 'argument'.

    Examples:
        >>> # Valid usage
        >>> def cmd(user: Annotated[str, 'option']): ...

        >>> # Invalid - will raise InvalidCLIHintError
        >>> def cmd(user: Annotated[str, 'invalid']): ...

    """

    def __init__(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="CLI_INVALID_HINT",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name


class CLIAdapterNotFoundError(CLIError):
    """Raised when CLI adapter dependencies are missing.

    This error occurs when attempting to use a CLI framework adapter
    but the required framework package is not installed.

    Examples:
        >>> # Raises if Click not installed
        >>> adapter = get_cli_adapter('click')

    """

    def __init__(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="CLI_ADAPTER_NOT_FOUND",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg


class CLIBuildError(CLIError):
    """Raised when CLI command/group building fails.

    This error occurs during the conversion of framework-agnostic
    CommandInfo to framework-specific CLI objects.
    """

    def _default_code(self) -> str:
        """Return default error code."""
        return "CLI_BUILD_ERROR"


__all__ = [
    "CLIAdapterNotFoundError",
    "CLIBuildError",
    "CLIError",
    "InvalidCLIHintError",
]

# 🧱🏗️🔚
