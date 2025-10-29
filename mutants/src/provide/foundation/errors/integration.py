# provide/foundation/errors/integration.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Integration and network-related exceptions."""
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


class IntegrationError(FoundationError):
    """Raised when external service integration fails.

    Args:
        message: Error message describing the integration failure.
        service: Optional service name that failed.
        endpoint: Optional endpoint that was called.
        status_code: Optional HTTP status code.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise IntegrationError("API call failed")
        >>> raise IntegrationError("Auth failed", service="github", status_code=401)

    """

    def xǁIntegrationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = None
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault(None, {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", None)["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault({})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault(
                "context",
            )["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("XXcontextXX", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("CONTEXT", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["XXintegration.serviceXX"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["INTEGRATION.SERVICE"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = None
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault(None, {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", None)["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault({})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault(
                "context",
            )["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("XXcontextXX", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("CONTEXT", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["XXintegration.endpointXX"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["INTEGRATION.ENDPOINT"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = None
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault(None, {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", None)["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault({})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault(
                "context",
            )["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("XXcontextXX", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("CONTEXT", {})["integration.status_code"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["XXintegration.status_codeXX"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["INTEGRATION.STATUS_CODE"] = status_code
        super().__init__(message, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(None, **kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(**kwargs)

    def xǁIntegrationErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        service: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if service:
            kwargs.setdefault("context", {})["integration.service"] = service
        if endpoint:
            kwargs.setdefault("context", {})["integration.endpoint"] = endpoint
        if status_code:
            kwargs.setdefault("context", {})["integration.status_code"] = status_code
        super().__init__(
            message,
        )

    xǁIntegrationErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁIntegrationErrorǁ__init____mutmut_1": xǁIntegrationErrorǁ__init____mutmut_1,
        "xǁIntegrationErrorǁ__init____mutmut_2": xǁIntegrationErrorǁ__init____mutmut_2,
        "xǁIntegrationErrorǁ__init____mutmut_3": xǁIntegrationErrorǁ__init____mutmut_3,
        "xǁIntegrationErrorǁ__init____mutmut_4": xǁIntegrationErrorǁ__init____mutmut_4,
        "xǁIntegrationErrorǁ__init____mutmut_5": xǁIntegrationErrorǁ__init____mutmut_5,
        "xǁIntegrationErrorǁ__init____mutmut_6": xǁIntegrationErrorǁ__init____mutmut_6,
        "xǁIntegrationErrorǁ__init____mutmut_7": xǁIntegrationErrorǁ__init____mutmut_7,
        "xǁIntegrationErrorǁ__init____mutmut_8": xǁIntegrationErrorǁ__init____mutmut_8,
        "xǁIntegrationErrorǁ__init____mutmut_9": xǁIntegrationErrorǁ__init____mutmut_9,
        "xǁIntegrationErrorǁ__init____mutmut_10": xǁIntegrationErrorǁ__init____mutmut_10,
        "xǁIntegrationErrorǁ__init____mutmut_11": xǁIntegrationErrorǁ__init____mutmut_11,
        "xǁIntegrationErrorǁ__init____mutmut_12": xǁIntegrationErrorǁ__init____mutmut_12,
        "xǁIntegrationErrorǁ__init____mutmut_13": xǁIntegrationErrorǁ__init____mutmut_13,
        "xǁIntegrationErrorǁ__init____mutmut_14": xǁIntegrationErrorǁ__init____mutmut_14,
        "xǁIntegrationErrorǁ__init____mutmut_15": xǁIntegrationErrorǁ__init____mutmut_15,
        "xǁIntegrationErrorǁ__init____mutmut_16": xǁIntegrationErrorǁ__init____mutmut_16,
        "xǁIntegrationErrorǁ__init____mutmut_17": xǁIntegrationErrorǁ__init____mutmut_17,
        "xǁIntegrationErrorǁ__init____mutmut_18": xǁIntegrationErrorǁ__init____mutmut_18,
        "xǁIntegrationErrorǁ__init____mutmut_19": xǁIntegrationErrorǁ__init____mutmut_19,
        "xǁIntegrationErrorǁ__init____mutmut_20": xǁIntegrationErrorǁ__init____mutmut_20,
        "xǁIntegrationErrorǁ__init____mutmut_21": xǁIntegrationErrorǁ__init____mutmut_21,
        "xǁIntegrationErrorǁ__init____mutmut_22": xǁIntegrationErrorǁ__init____mutmut_22,
        "xǁIntegrationErrorǁ__init____mutmut_23": xǁIntegrationErrorǁ__init____mutmut_23,
        "xǁIntegrationErrorǁ__init____mutmut_24": xǁIntegrationErrorǁ__init____mutmut_24,
        "xǁIntegrationErrorǁ__init____mutmut_25": xǁIntegrationErrorǁ__init____mutmut_25,
        "xǁIntegrationErrorǁ__init____mutmut_26": xǁIntegrationErrorǁ__init____mutmut_26,
        "xǁIntegrationErrorǁ__init____mutmut_27": xǁIntegrationErrorǁ__init____mutmut_27,
        "xǁIntegrationErrorǁ__init____mutmut_28": xǁIntegrationErrorǁ__init____mutmut_28,
        "xǁIntegrationErrorǁ__init____mutmut_29": xǁIntegrationErrorǁ__init____mutmut_29,
        "xǁIntegrationErrorǁ__init____mutmut_30": xǁIntegrationErrorǁ__init____mutmut_30,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁIntegrationErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁIntegrationErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁIntegrationErrorǁ__init____mutmut_orig)
    xǁIntegrationErrorǁ__init____mutmut_orig.__name__ = "xǁIntegrationErrorǁ__init__"

    def xǁIntegrationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "INTEGRATION_ERROR"

    def xǁIntegrationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXINTEGRATION_ERRORXX"

    def xǁIntegrationErrorǁ_default_code__mutmut_2(self) -> str:
        return "integration_error"

    xǁIntegrationErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁIntegrationErrorǁ_default_code__mutmut_1": xǁIntegrationErrorǁ_default_code__mutmut_1,
        "xǁIntegrationErrorǁ_default_code__mutmut_2": xǁIntegrationErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁIntegrationErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁIntegrationErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁIntegrationErrorǁ_default_code__mutmut_orig)
    xǁIntegrationErrorǁ_default_code__mutmut_orig.__name__ = "xǁIntegrationErrorǁ_default_code"


class NetworkError(IntegrationError):
    """Raised for network-related failures.

    Args:
        message: Error message describing the network issue.
        host: Optional hostname or IP address.
        port: Optional port number.
        **kwargs: Additional context passed to IntegrationError.

    Examples:
        >>> raise NetworkError("Connection refused")
        >>> raise NetworkError("DNS resolution failed", host="api.example.com")

    """

    def xǁNetworkErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = None
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault(None, {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", None)["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault({})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault(
                "context",
            )["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("XXcontextXX", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("CONTEXT", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["XXnetwork.hostXX"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["NETWORK.HOST"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = None
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault(None, {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", None)["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault({})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault(
                "context",
            )["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("XXcontextXX", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("CONTEXT", {})["network.port"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["XXnetwork.portXX"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["NETWORK.PORT"] = port
        super().__init__(message, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(None, **kwargs)

    def xǁNetworkErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(**kwargs)

    def xǁNetworkErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        host: str | None = None,
        port: int | None = None,
        **kwargs: Any,
    ) -> None:
        if host:
            kwargs.setdefault("context", {})["network.host"] = host
        if port:
            kwargs.setdefault("context", {})["network.port"] = port
        super().__init__(
            message,
        )

    xǁNetworkErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁNetworkErrorǁ__init____mutmut_1": xǁNetworkErrorǁ__init____mutmut_1,
        "xǁNetworkErrorǁ__init____mutmut_2": xǁNetworkErrorǁ__init____mutmut_2,
        "xǁNetworkErrorǁ__init____mutmut_3": xǁNetworkErrorǁ__init____mutmut_3,
        "xǁNetworkErrorǁ__init____mutmut_4": xǁNetworkErrorǁ__init____mutmut_4,
        "xǁNetworkErrorǁ__init____mutmut_5": xǁNetworkErrorǁ__init____mutmut_5,
        "xǁNetworkErrorǁ__init____mutmut_6": xǁNetworkErrorǁ__init____mutmut_6,
        "xǁNetworkErrorǁ__init____mutmut_7": xǁNetworkErrorǁ__init____mutmut_7,
        "xǁNetworkErrorǁ__init____mutmut_8": xǁNetworkErrorǁ__init____mutmut_8,
        "xǁNetworkErrorǁ__init____mutmut_9": xǁNetworkErrorǁ__init____mutmut_9,
        "xǁNetworkErrorǁ__init____mutmut_10": xǁNetworkErrorǁ__init____mutmut_10,
        "xǁNetworkErrorǁ__init____mutmut_11": xǁNetworkErrorǁ__init____mutmut_11,
        "xǁNetworkErrorǁ__init____mutmut_12": xǁNetworkErrorǁ__init____mutmut_12,
        "xǁNetworkErrorǁ__init____mutmut_13": xǁNetworkErrorǁ__init____mutmut_13,
        "xǁNetworkErrorǁ__init____mutmut_14": xǁNetworkErrorǁ__init____mutmut_14,
        "xǁNetworkErrorǁ__init____mutmut_15": xǁNetworkErrorǁ__init____mutmut_15,
        "xǁNetworkErrorǁ__init____mutmut_16": xǁNetworkErrorǁ__init____mutmut_16,
        "xǁNetworkErrorǁ__init____mutmut_17": xǁNetworkErrorǁ__init____mutmut_17,
        "xǁNetworkErrorǁ__init____mutmut_18": xǁNetworkErrorǁ__init____mutmut_18,
        "xǁNetworkErrorǁ__init____mutmut_19": xǁNetworkErrorǁ__init____mutmut_19,
        "xǁNetworkErrorǁ__init____mutmut_20": xǁNetworkErrorǁ__init____mutmut_20,
        "xǁNetworkErrorǁ__init____mutmut_21": xǁNetworkErrorǁ__init____mutmut_21,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁNetworkErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁNetworkErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁNetworkErrorǁ__init____mutmut_orig)
    xǁNetworkErrorǁ__init____mutmut_orig.__name__ = "xǁNetworkErrorǁ__init__"

    def xǁNetworkErrorǁ_default_code__mutmut_orig(self) -> str:
        return "NETWORK_ERROR"

    def xǁNetworkErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXNETWORK_ERRORXX"

    def xǁNetworkErrorǁ_default_code__mutmut_2(self) -> str:
        return "network_error"

    xǁNetworkErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁNetworkErrorǁ_default_code__mutmut_1": xǁNetworkErrorǁ_default_code__mutmut_1,
        "xǁNetworkErrorǁ_default_code__mutmut_2": xǁNetworkErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁNetworkErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁNetworkErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁNetworkErrorǁ_default_code__mutmut_orig)
    xǁNetworkErrorǁ_default_code__mutmut_orig.__name__ = "xǁNetworkErrorǁ_default_code"


class TimeoutError(IntegrationError):
    """Raised when operations exceed time limits.

    Args:
        message: Error message describing the timeout.
        timeout_seconds: Optional timeout limit in seconds.
        elapsed_seconds: Optional actual elapsed time.
        **kwargs: Additional context passed to IntegrationError.

    Examples:
        >>> raise TimeoutError("Request timed out")
        >>> raise TimeoutError("Operation exceeded limit", timeout_seconds=30, elapsed_seconds=31.5)

    """

    def xǁTimeoutErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = None
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault(None, {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", None)["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault({})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault(
                "context",
            )["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("XXcontextXX", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("CONTEXT", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["XXtimeout.limitXX"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["TIMEOUT.LIMIT"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = None
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault(None, {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", None)["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault({})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault(
                "context",
            )["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("XXcontextXX", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("CONTEXT", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["XXtimeout.elapsedXX"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["TIMEOUT.ELAPSED"] = elapsed_seconds
        super().__init__(message, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(None, **kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(**kwargs)

    def xǁTimeoutErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        timeout_seconds: float | None = None,
        elapsed_seconds: float | None = None,
        **kwargs: Any,
    ) -> None:
        if timeout_seconds is not None:
            kwargs.setdefault("context", {})["timeout.limit"] = timeout_seconds
        if elapsed_seconds is not None:
            kwargs.setdefault("context", {})["timeout.elapsed"] = elapsed_seconds
        super().__init__(
            message,
        )

    xǁTimeoutErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTimeoutErrorǁ__init____mutmut_1": xǁTimeoutErrorǁ__init____mutmut_1,
        "xǁTimeoutErrorǁ__init____mutmut_2": xǁTimeoutErrorǁ__init____mutmut_2,
        "xǁTimeoutErrorǁ__init____mutmut_3": xǁTimeoutErrorǁ__init____mutmut_3,
        "xǁTimeoutErrorǁ__init____mutmut_4": xǁTimeoutErrorǁ__init____mutmut_4,
        "xǁTimeoutErrorǁ__init____mutmut_5": xǁTimeoutErrorǁ__init____mutmut_5,
        "xǁTimeoutErrorǁ__init____mutmut_6": xǁTimeoutErrorǁ__init____mutmut_6,
        "xǁTimeoutErrorǁ__init____mutmut_7": xǁTimeoutErrorǁ__init____mutmut_7,
        "xǁTimeoutErrorǁ__init____mutmut_8": xǁTimeoutErrorǁ__init____mutmut_8,
        "xǁTimeoutErrorǁ__init____mutmut_9": xǁTimeoutErrorǁ__init____mutmut_9,
        "xǁTimeoutErrorǁ__init____mutmut_10": xǁTimeoutErrorǁ__init____mutmut_10,
        "xǁTimeoutErrorǁ__init____mutmut_11": xǁTimeoutErrorǁ__init____mutmut_11,
        "xǁTimeoutErrorǁ__init____mutmut_12": xǁTimeoutErrorǁ__init____mutmut_12,
        "xǁTimeoutErrorǁ__init____mutmut_13": xǁTimeoutErrorǁ__init____mutmut_13,
        "xǁTimeoutErrorǁ__init____mutmut_14": xǁTimeoutErrorǁ__init____mutmut_14,
        "xǁTimeoutErrorǁ__init____mutmut_15": xǁTimeoutErrorǁ__init____mutmut_15,
        "xǁTimeoutErrorǁ__init____mutmut_16": xǁTimeoutErrorǁ__init____mutmut_16,
        "xǁTimeoutErrorǁ__init____mutmut_17": xǁTimeoutErrorǁ__init____mutmut_17,
        "xǁTimeoutErrorǁ__init____mutmut_18": xǁTimeoutErrorǁ__init____mutmut_18,
        "xǁTimeoutErrorǁ__init____mutmut_19": xǁTimeoutErrorǁ__init____mutmut_19,
        "xǁTimeoutErrorǁ__init____mutmut_20": xǁTimeoutErrorǁ__init____mutmut_20,
        "xǁTimeoutErrorǁ__init____mutmut_21": xǁTimeoutErrorǁ__init____mutmut_21,
        "xǁTimeoutErrorǁ__init____mutmut_22": xǁTimeoutErrorǁ__init____mutmut_22,
        "xǁTimeoutErrorǁ__init____mutmut_23": xǁTimeoutErrorǁ__init____mutmut_23,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTimeoutErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁTimeoutErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁTimeoutErrorǁ__init____mutmut_orig)
    xǁTimeoutErrorǁ__init____mutmut_orig.__name__ = "xǁTimeoutErrorǁ__init__"

    def xǁTimeoutErrorǁ_default_code__mutmut_orig(self) -> str:
        return "TIMEOUT_ERROR"

    def xǁTimeoutErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXTIMEOUT_ERRORXX"

    def xǁTimeoutErrorǁ_default_code__mutmut_2(self) -> str:
        return "timeout_error"

    xǁTimeoutErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁTimeoutErrorǁ_default_code__mutmut_1": xǁTimeoutErrorǁ_default_code__mutmut_1,
        "xǁTimeoutErrorǁ_default_code__mutmut_2": xǁTimeoutErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁTimeoutErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁTimeoutErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁTimeoutErrorǁ_default_code__mutmut_orig)
    xǁTimeoutErrorǁ_default_code__mutmut_orig.__name__ = "xǁTimeoutErrorǁ_default_code"


# <3 🧱🤝🐛🪄
