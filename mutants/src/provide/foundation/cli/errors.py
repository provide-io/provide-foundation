# provide/foundation/cli/errors.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""CLI adapter error classes.

Foundation-based errors for CLI adapter system.
"""

from __future__ import annotations

from provide.foundation.errors.base import FoundationError
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


class CLIError(FoundationError):
    """Base error for CLI adapter operations.

    Raised when CLI adapter operations fail.
    """

    def xǁCLIErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code."""
        return "CLI_ERROR"

    def xǁCLIErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code."""
        return "XXCLI_ERRORXX"

    def xǁCLIErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code."""
        return "cli_error"

    xǁCLIErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCLIErrorǁ_default_code__mutmut_1": xǁCLIErrorǁ_default_code__mutmut_1,
        "xǁCLIErrorǁ_default_code__mutmut_2": xǁCLIErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCLIErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCLIErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCLIErrorǁ_default_code__mutmut_orig)
    xǁCLIErrorǁ_default_code__mutmut_orig.__name__ = "xǁCLIErrorǁ_default_code"


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

    def xǁInvalidCLIHintErrorǁ__init____mutmut_orig(self, hint: str, param_name: str) -> None:
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

    def xǁInvalidCLIHintErrorǁ__init____mutmut_1(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            None,
            code="CLI_INVALID_HINT",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_2(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code=None,
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_3(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="CLI_INVALID_HINT",
            hint=None,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_4(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="CLI_INVALID_HINT",
            hint=hint,
            param_name=None,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_5(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            code="CLI_INVALID_HINT",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_6(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_7(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="CLI_INVALID_HINT",
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_8(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="CLI_INVALID_HINT",
            hint=hint,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_9(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="XXCLI_INVALID_HINTXX",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_10(self, hint: str, param_name: str) -> None:
        """Initialize with hint and parameter details.

        Args:
            hint: The invalid hint that was provided
            param_name: Name of the parameter with invalid hint

        """
        super().__init__(
            f"Invalid CLI hint '{hint}' for parameter '{param_name}'. Must be 'option' or 'argument'.",
            code="cli_invalid_hint",
            hint=hint,
            param_name=param_name,
        )
        self.hint = hint
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_11(self, hint: str, param_name: str) -> None:
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
        self.hint = None
        self.param_name = param_name

    def xǁInvalidCLIHintErrorǁ__init____mutmut_12(self, hint: str, param_name: str) -> None:
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
        self.param_name = None

    xǁInvalidCLIHintErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁInvalidCLIHintErrorǁ__init____mutmut_1": xǁInvalidCLIHintErrorǁ__init____mutmut_1,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_2": xǁInvalidCLIHintErrorǁ__init____mutmut_2,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_3": xǁInvalidCLIHintErrorǁ__init____mutmut_3,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_4": xǁInvalidCLIHintErrorǁ__init____mutmut_4,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_5": xǁInvalidCLIHintErrorǁ__init____mutmut_5,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_6": xǁInvalidCLIHintErrorǁ__init____mutmut_6,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_7": xǁInvalidCLIHintErrorǁ__init____mutmut_7,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_8": xǁInvalidCLIHintErrorǁ__init____mutmut_8,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_9": xǁInvalidCLIHintErrorǁ__init____mutmut_9,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_10": xǁInvalidCLIHintErrorǁ__init____mutmut_10,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_11": xǁInvalidCLIHintErrorǁ__init____mutmut_11,
        "xǁInvalidCLIHintErrorǁ__init____mutmut_12": xǁInvalidCLIHintErrorǁ__init____mutmut_12,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁInvalidCLIHintErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁInvalidCLIHintErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁInvalidCLIHintErrorǁ__init____mutmut_orig)
    xǁInvalidCLIHintErrorǁ__init____mutmut_orig.__name__ = "xǁInvalidCLIHintErrorǁ__init__"


class CLIAdapterNotFoundError(CLIError):
    """Raised when CLI adapter dependencies are missing.

    This error occurs when attempting to use a CLI framework adapter
    but the required framework package is not installed.

    Examples:
        >>> # Raises if Click not installed
        >>> adapter = get_cli_adapter('click')

    """

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_orig(
        self, framework: str, package: str | None = None
    ) -> None:
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

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_1(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = None
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="CLI_ADAPTER_NOT_FOUND",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_2(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package and framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="CLI_ADAPTER_NOT_FOUND",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_3(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            None,
            code="CLI_ADAPTER_NOT_FOUND",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_4(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code=None,
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_5(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="CLI_ADAPTER_NOT_FOUND",
            framework=None,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_6(self, framework: str, package: str | None = None) -> None:
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
            package=None,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_7(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            code="CLI_ADAPTER_NOT_FOUND",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_8(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_9(self, framework: str, package: str | None = None) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="CLI_ADAPTER_NOT_FOUND",
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_10(
        self, framework: str, package: str | None = None
    ) -> None:
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
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_11(
        self, framework: str, package: str | None = None
    ) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="XXCLI_ADAPTER_NOT_FOUNDXX",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_12(
        self, framework: str, package: str | None = None
    ) -> None:
        """Initialize with framework details.

        Args:
            framework: Name of the CLI framework (e.g., 'click')
            package: Optional package name to install

        """
        pkg = package or framework
        super().__init__(
            f"CLI adapter for '{framework}' requires: pip install 'provide-foundation[{pkg}]'",
            code="cli_adapter_not_found",
            framework=framework,
            package=pkg,
        )
        self.framework = framework
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_13(
        self, framework: str, package: str | None = None
    ) -> None:
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
        self.framework = None
        self.package = pkg

    def xǁCLIAdapterNotFoundErrorǁ__init____mutmut_14(
        self, framework: str, package: str | None = None
    ) -> None:
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
        self.package = None

    xǁCLIAdapterNotFoundErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_1": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_1,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_2": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_2,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_3": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_3,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_4": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_4,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_5": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_5,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_6": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_6,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_7": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_7,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_8": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_8,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_9": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_9,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_10": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_10,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_11": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_11,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_12": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_12,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_13": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_13,
        "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_14": xǁCLIAdapterNotFoundErrorǁ__init____mutmut_14,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁCLIAdapterNotFoundErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁCLIAdapterNotFoundErrorǁ__init____mutmut_orig)
    xǁCLIAdapterNotFoundErrorǁ__init____mutmut_orig.__name__ = "xǁCLIAdapterNotFoundErrorǁ__init__"


class CLIBuildError(CLIError):
    """Raised when CLI command/group building fails.

    This error occurs during the conversion of framework-agnostic
    CommandInfo to framework-specific CLI objects.
    """

    def xǁCLIBuildErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code."""
        return "CLI_BUILD_ERROR"

    def xǁCLIBuildErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code."""
        return "XXCLI_BUILD_ERRORXX"

    def xǁCLIBuildErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code."""
        return "cli_build_error"

    xǁCLIBuildErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁCLIBuildErrorǁ_default_code__mutmut_1": xǁCLIBuildErrorǁ_default_code__mutmut_1,
        "xǁCLIBuildErrorǁ_default_code__mutmut_2": xǁCLIBuildErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁCLIBuildErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁCLIBuildErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁCLIBuildErrorǁ_default_code__mutmut_orig)
    xǁCLIBuildErrorǁ_default_code__mutmut_orig.__name__ = "xǁCLIBuildErrorǁ_default_code"


__all__ = [
    "CLIAdapterNotFoundError",
    "CLIBuildError",
    "CLIError",
    "InvalidCLIHintError",
]


# <3 🧱🤝💻🪄
