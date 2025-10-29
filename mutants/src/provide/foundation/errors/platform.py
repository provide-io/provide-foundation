# provide/foundation/errors/platform.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Platform detection and system-related exceptions."""
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


class PlatformError(FoundationError):
    """Raised when platform detection or system operations fail.

    Args:
        message: Error message describing the platform issue.
        platform: Optional platform identifier.
        operation: Optional operation that failed.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise PlatformError("Failed to detect OS")
        >>> raise PlatformError("Unsupported platform", platform="freebsd")

    """

    def xǁPlatformErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = None
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault(None, {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", None)["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault({})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault(
                "context",
            )["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("XXcontextXX", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("CONTEXT", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["XXplatform.nameXX"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["PLATFORM.NAME"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = None
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault(None, {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", None)["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault({})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault(
                "context",
            )["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("XXcontextXX", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("CONTEXT", {})["platform.operation"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["XXplatform.operationXX"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["PLATFORM.OPERATION"] = operation
        super().__init__(message, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(None, **kwargs)

    def xǁPlatformErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(**kwargs)

    def xǁPlatformErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        platform: str | None = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        if platform:
            kwargs.setdefault("context", {})["platform.name"] = platform
        if operation:
            kwargs.setdefault("context", {})["platform.operation"] = operation
        super().__init__(
            message,
        )

    xǁPlatformErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPlatformErrorǁ__init____mutmut_1": xǁPlatformErrorǁ__init____mutmut_1,
        "xǁPlatformErrorǁ__init____mutmut_2": xǁPlatformErrorǁ__init____mutmut_2,
        "xǁPlatformErrorǁ__init____mutmut_3": xǁPlatformErrorǁ__init____mutmut_3,
        "xǁPlatformErrorǁ__init____mutmut_4": xǁPlatformErrorǁ__init____mutmut_4,
        "xǁPlatformErrorǁ__init____mutmut_5": xǁPlatformErrorǁ__init____mutmut_5,
        "xǁPlatformErrorǁ__init____mutmut_6": xǁPlatformErrorǁ__init____mutmut_6,
        "xǁPlatformErrorǁ__init____mutmut_7": xǁPlatformErrorǁ__init____mutmut_7,
        "xǁPlatformErrorǁ__init____mutmut_8": xǁPlatformErrorǁ__init____mutmut_8,
        "xǁPlatformErrorǁ__init____mutmut_9": xǁPlatformErrorǁ__init____mutmut_9,
        "xǁPlatformErrorǁ__init____mutmut_10": xǁPlatformErrorǁ__init____mutmut_10,
        "xǁPlatformErrorǁ__init____mutmut_11": xǁPlatformErrorǁ__init____mutmut_11,
        "xǁPlatformErrorǁ__init____mutmut_12": xǁPlatformErrorǁ__init____mutmut_12,
        "xǁPlatformErrorǁ__init____mutmut_13": xǁPlatformErrorǁ__init____mutmut_13,
        "xǁPlatformErrorǁ__init____mutmut_14": xǁPlatformErrorǁ__init____mutmut_14,
        "xǁPlatformErrorǁ__init____mutmut_15": xǁPlatformErrorǁ__init____mutmut_15,
        "xǁPlatformErrorǁ__init____mutmut_16": xǁPlatformErrorǁ__init____mutmut_16,
        "xǁPlatformErrorǁ__init____mutmut_17": xǁPlatformErrorǁ__init____mutmut_17,
        "xǁPlatformErrorǁ__init____mutmut_18": xǁPlatformErrorǁ__init____mutmut_18,
        "xǁPlatformErrorǁ__init____mutmut_19": xǁPlatformErrorǁ__init____mutmut_19,
        "xǁPlatformErrorǁ__init____mutmut_20": xǁPlatformErrorǁ__init____mutmut_20,
        "xǁPlatformErrorǁ__init____mutmut_21": xǁPlatformErrorǁ__init____mutmut_21,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPlatformErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁPlatformErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁPlatformErrorǁ__init____mutmut_orig)
    xǁPlatformErrorǁ__init____mutmut_orig.__name__ = "xǁPlatformErrorǁ__init__"

    def xǁPlatformErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PLATFORM_ERROR"

    def xǁPlatformErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPLATFORM_ERRORXX"

    def xǁPlatformErrorǁ_default_code__mutmut_2(self) -> str:
        return "platform_error"

    xǁPlatformErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPlatformErrorǁ_default_code__mutmut_1": xǁPlatformErrorǁ_default_code__mutmut_1,
        "xǁPlatformErrorǁ_default_code__mutmut_2": xǁPlatformErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPlatformErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁPlatformErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁPlatformErrorǁ_default_code__mutmut_orig)
    xǁPlatformErrorǁ_default_code__mutmut_orig.__name__ = "xǁPlatformErrorǁ_default_code"


# <3 🧱🤝🐛🪄
