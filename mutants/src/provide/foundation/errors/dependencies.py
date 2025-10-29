# provide/foundation/errors/dependencies.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Dependency-related exceptions."""

from typing import Any

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

    def xǁDependencyErrorǁ__init____mutmut_orig(
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

    def xǁDependencyErrorǁ__init____mutmut_1(
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
            cmd = None
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

    def xǁDependencyErrorǁ__init____mutmut_2(
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
            cmd = None
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

    def xǁDependencyErrorǁ__init____mutmut_3(
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
            cmd = None

        # Create the error message
        message = f"Optional dependency '{package}' is required for this feature. Install with: {cmd}"

        # Add context
        context = kwargs.setdefault("context", {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_4(
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
        message = None

        # Add context
        context = kwargs.setdefault("context", {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_5(
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
        context = None
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_6(
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
        context = kwargs.setdefault(None, {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_7(
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
        context = kwargs.setdefault("context", None)
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_8(
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
        context = kwargs.setdefault({})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_9(
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
        context = kwargs.setdefault(
            "context",
        )
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_10(
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
        context = kwargs.setdefault("XXcontextXX", {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_11(
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
        context = kwargs.setdefault("CONTEXT", {})
        context["dependency.package"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_12(
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
        context["dependency.package"] = None
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_13(
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
        context["XXdependency.packageXX"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_14(
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
        context["DEPENDENCY.PACKAGE"] = package
        context["dependency.install_command"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_15(
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
        context["dependency.install_command"] = None
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_16(
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
        context["XXdependency.install_commandXX"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_17(
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
        context["DEPENDENCY.INSTALL_COMMAND"] = cmd
        if feature:
            context["dependency.feature"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_18(
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
            context["dependency.feature"] = None

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_19(
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
            context["XXdependency.featureXX"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_20(
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
            context["DEPENDENCY.FEATURE"] = feature

        super().__init__(message, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_21(
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

        super().__init__(None, **kwargs)

    def xǁDependencyErrorǁ__init____mutmut_22(
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

        super().__init__(**kwargs)

    def xǁDependencyErrorǁ__init____mutmut_23(
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

        super().__init__(
            message,
        )

    xǁDependencyErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDependencyErrorǁ__init____mutmut_1": xǁDependencyErrorǁ__init____mutmut_1,
        "xǁDependencyErrorǁ__init____mutmut_2": xǁDependencyErrorǁ__init____mutmut_2,
        "xǁDependencyErrorǁ__init____mutmut_3": xǁDependencyErrorǁ__init____mutmut_3,
        "xǁDependencyErrorǁ__init____mutmut_4": xǁDependencyErrorǁ__init____mutmut_4,
        "xǁDependencyErrorǁ__init____mutmut_5": xǁDependencyErrorǁ__init____mutmut_5,
        "xǁDependencyErrorǁ__init____mutmut_6": xǁDependencyErrorǁ__init____mutmut_6,
        "xǁDependencyErrorǁ__init____mutmut_7": xǁDependencyErrorǁ__init____mutmut_7,
        "xǁDependencyErrorǁ__init____mutmut_8": xǁDependencyErrorǁ__init____mutmut_8,
        "xǁDependencyErrorǁ__init____mutmut_9": xǁDependencyErrorǁ__init____mutmut_9,
        "xǁDependencyErrorǁ__init____mutmut_10": xǁDependencyErrorǁ__init____mutmut_10,
        "xǁDependencyErrorǁ__init____mutmut_11": xǁDependencyErrorǁ__init____mutmut_11,
        "xǁDependencyErrorǁ__init____mutmut_12": xǁDependencyErrorǁ__init____mutmut_12,
        "xǁDependencyErrorǁ__init____mutmut_13": xǁDependencyErrorǁ__init____mutmut_13,
        "xǁDependencyErrorǁ__init____mutmut_14": xǁDependencyErrorǁ__init____mutmut_14,
        "xǁDependencyErrorǁ__init____mutmut_15": xǁDependencyErrorǁ__init____mutmut_15,
        "xǁDependencyErrorǁ__init____mutmut_16": xǁDependencyErrorǁ__init____mutmut_16,
        "xǁDependencyErrorǁ__init____mutmut_17": xǁDependencyErrorǁ__init____mutmut_17,
        "xǁDependencyErrorǁ__init____mutmut_18": xǁDependencyErrorǁ__init____mutmut_18,
        "xǁDependencyErrorǁ__init____mutmut_19": xǁDependencyErrorǁ__init____mutmut_19,
        "xǁDependencyErrorǁ__init____mutmut_20": xǁDependencyErrorǁ__init____mutmut_20,
        "xǁDependencyErrorǁ__init____mutmut_21": xǁDependencyErrorǁ__init____mutmut_21,
        "xǁDependencyErrorǁ__init____mutmut_22": xǁDependencyErrorǁ__init____mutmut_22,
        "xǁDependencyErrorǁ__init____mutmut_23": xǁDependencyErrorǁ__init____mutmut_23,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDependencyErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁDependencyErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁDependencyErrorǁ__init____mutmut_orig)
    xǁDependencyErrorǁ__init____mutmut_orig.__name__ = "xǁDependencyErrorǁ__init__"

    def xǁDependencyErrorǁ_default_code__mutmut_orig(self) -> str:
        return "DEPENDENCY_MISSING"

    def xǁDependencyErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXDEPENDENCY_MISSINGXX"

    def xǁDependencyErrorǁ_default_code__mutmut_2(self) -> str:
        return "dependency_missing"

    xǁDependencyErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDependencyErrorǁ_default_code__mutmut_1": xǁDependencyErrorǁ_default_code__mutmut_1,
        "xǁDependencyErrorǁ_default_code__mutmut_2": xǁDependencyErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDependencyErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁDependencyErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁDependencyErrorǁ_default_code__mutmut_orig)
    xǁDependencyErrorǁ_default_code__mutmut_orig.__name__ = "xǁDependencyErrorǁ_default_code"


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

    def xǁDependencyMismatchErrorǁ__init____mutmut_orig(
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

    def xǁDependencyMismatchErrorǁ__init____mutmut_1(
        self,
        package: str,
        *,
        required_version: str,
        current_version: str,
        **kwargs: Any,
    ) -> None:
        message = None

        # Add context
        context = kwargs.setdefault("context", {})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_2(
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
        context = None
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_3(
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
        context = kwargs.setdefault(None, {})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_4(
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
        context = kwargs.setdefault("context", None)
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_5(
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
        context = kwargs.setdefault({})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_6(
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
        context = kwargs.setdefault(
            "context",
        )
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_7(
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
        context = kwargs.setdefault("XXcontextXX", {})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_8(
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
        context = kwargs.setdefault("CONTEXT", {})
        context["dependency.package"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_9(
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
        context["dependency.package"] = None
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_10(
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
        context["XXdependency.packageXX"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_11(
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
        context["DEPENDENCY.PACKAGE"] = package
        context["dependency.required_version"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_12(
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
        context["dependency.required_version"] = None
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_13(
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
        context["XXdependency.required_versionXX"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_14(
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
        context["DEPENDENCY.REQUIRED_VERSION"] = required_version
        context["dependency.current_version"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_15(
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
        context["dependency.current_version"] = None

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_16(
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
        context["XXdependency.current_versionXX"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_17(
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
        context["DEPENDENCY.CURRENT_VERSION"] = current_version

        super().__init__(message, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_18(
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

        super().__init__(None, **kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_19(
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

        super().__init__(**kwargs)

    def xǁDependencyMismatchErrorǁ__init____mutmut_20(
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

        super().__init__(
            message,
        )

    xǁDependencyMismatchErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDependencyMismatchErrorǁ__init____mutmut_1": xǁDependencyMismatchErrorǁ__init____mutmut_1,
        "xǁDependencyMismatchErrorǁ__init____mutmut_2": xǁDependencyMismatchErrorǁ__init____mutmut_2,
        "xǁDependencyMismatchErrorǁ__init____mutmut_3": xǁDependencyMismatchErrorǁ__init____mutmut_3,
        "xǁDependencyMismatchErrorǁ__init____mutmut_4": xǁDependencyMismatchErrorǁ__init____mutmut_4,
        "xǁDependencyMismatchErrorǁ__init____mutmut_5": xǁDependencyMismatchErrorǁ__init____mutmut_5,
        "xǁDependencyMismatchErrorǁ__init____mutmut_6": xǁDependencyMismatchErrorǁ__init____mutmut_6,
        "xǁDependencyMismatchErrorǁ__init____mutmut_7": xǁDependencyMismatchErrorǁ__init____mutmut_7,
        "xǁDependencyMismatchErrorǁ__init____mutmut_8": xǁDependencyMismatchErrorǁ__init____mutmut_8,
        "xǁDependencyMismatchErrorǁ__init____mutmut_9": xǁDependencyMismatchErrorǁ__init____mutmut_9,
        "xǁDependencyMismatchErrorǁ__init____mutmut_10": xǁDependencyMismatchErrorǁ__init____mutmut_10,
        "xǁDependencyMismatchErrorǁ__init____mutmut_11": xǁDependencyMismatchErrorǁ__init____mutmut_11,
        "xǁDependencyMismatchErrorǁ__init____mutmut_12": xǁDependencyMismatchErrorǁ__init____mutmut_12,
        "xǁDependencyMismatchErrorǁ__init____mutmut_13": xǁDependencyMismatchErrorǁ__init____mutmut_13,
        "xǁDependencyMismatchErrorǁ__init____mutmut_14": xǁDependencyMismatchErrorǁ__init____mutmut_14,
        "xǁDependencyMismatchErrorǁ__init____mutmut_15": xǁDependencyMismatchErrorǁ__init____mutmut_15,
        "xǁDependencyMismatchErrorǁ__init____mutmut_16": xǁDependencyMismatchErrorǁ__init____mutmut_16,
        "xǁDependencyMismatchErrorǁ__init____mutmut_17": xǁDependencyMismatchErrorǁ__init____mutmut_17,
        "xǁDependencyMismatchErrorǁ__init____mutmut_18": xǁDependencyMismatchErrorǁ__init____mutmut_18,
        "xǁDependencyMismatchErrorǁ__init____mutmut_19": xǁDependencyMismatchErrorǁ__init____mutmut_19,
        "xǁDependencyMismatchErrorǁ__init____mutmut_20": xǁDependencyMismatchErrorǁ__init____mutmut_20,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDependencyMismatchErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁDependencyMismatchErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁDependencyMismatchErrorǁ__init____mutmut_orig)
    xǁDependencyMismatchErrorǁ__init____mutmut_orig.__name__ = "xǁDependencyMismatchErrorǁ__init__"

    def xǁDependencyMismatchErrorǁ_default_code__mutmut_orig(self) -> str:
        return "DEPENDENCY_VERSION_MISMATCH"

    def xǁDependencyMismatchErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXDEPENDENCY_VERSION_MISMATCHXX"

    def xǁDependencyMismatchErrorǁ_default_code__mutmut_2(self) -> str:
        return "dependency_version_mismatch"

    xǁDependencyMismatchErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁDependencyMismatchErrorǁ_default_code__mutmut_1": xǁDependencyMismatchErrorǁ_default_code__mutmut_1,
        "xǁDependencyMismatchErrorǁ_default_code__mutmut_2": xǁDependencyMismatchErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁDependencyMismatchErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁDependencyMismatchErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁDependencyMismatchErrorǁ_default_code__mutmut_orig)
    xǁDependencyMismatchErrorǁ_default_code__mutmut_orig.__name__ = "xǁDependencyMismatchErrorǁ_default_code"


# <3 🧱🤝🐛🪄
