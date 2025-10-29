# provide/foundation/errors/profiling.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Profiling-related exceptions."""
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


class ProfilingError(FoundationError):
    """Raised when profiling operations fail.

    Args:
        message: Error message describing the profiling issue.
        component: Optional profiling component that caused the error.
        sample_rate: Optional sample rate when the error occurred.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ProfilingError("Profiling initialization failed")
        >>> raise ProfilingError("Invalid sample rate", sample_rate=1.5)

    """

    def xǁProfilingErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = None
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault(None, {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", None)["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault({})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault(
                "context",
            )["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("XXcontextXX", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("CONTEXT", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["XXprofiling.componentXX"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["PROFILING.COMPONENT"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = None
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault(None, {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", None)["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault({})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault(
                "context",
            )["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("XXcontextXX", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("CONTEXT", {})["profiling.sample_rate"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["XXprofiling.sample_rateXX"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["PROFILING.SAMPLE_RATE"] = sample_rate
        super().__init__(message, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(None, **kwargs)

    def xǁProfilingErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(**kwargs)

    def xǁProfilingErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        component: str | None = None,
        sample_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if component:
            kwargs.setdefault("context", {})["profiling.component"] = component
        if sample_rate is not None:
            kwargs.setdefault("context", {})["profiling.sample_rate"] = sample_rate
        super().__init__(
            message,
        )

    xǁProfilingErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁProfilingErrorǁ__init____mutmut_1": xǁProfilingErrorǁ__init____mutmut_1,
        "xǁProfilingErrorǁ__init____mutmut_2": xǁProfilingErrorǁ__init____mutmut_2,
        "xǁProfilingErrorǁ__init____mutmut_3": xǁProfilingErrorǁ__init____mutmut_3,
        "xǁProfilingErrorǁ__init____mutmut_4": xǁProfilingErrorǁ__init____mutmut_4,
        "xǁProfilingErrorǁ__init____mutmut_5": xǁProfilingErrorǁ__init____mutmut_5,
        "xǁProfilingErrorǁ__init____mutmut_6": xǁProfilingErrorǁ__init____mutmut_6,
        "xǁProfilingErrorǁ__init____mutmut_7": xǁProfilingErrorǁ__init____mutmut_7,
        "xǁProfilingErrorǁ__init____mutmut_8": xǁProfilingErrorǁ__init____mutmut_8,
        "xǁProfilingErrorǁ__init____mutmut_9": xǁProfilingErrorǁ__init____mutmut_9,
        "xǁProfilingErrorǁ__init____mutmut_10": xǁProfilingErrorǁ__init____mutmut_10,
        "xǁProfilingErrorǁ__init____mutmut_11": xǁProfilingErrorǁ__init____mutmut_11,
        "xǁProfilingErrorǁ__init____mutmut_12": xǁProfilingErrorǁ__init____mutmut_12,
        "xǁProfilingErrorǁ__init____mutmut_13": xǁProfilingErrorǁ__init____mutmut_13,
        "xǁProfilingErrorǁ__init____mutmut_14": xǁProfilingErrorǁ__init____mutmut_14,
        "xǁProfilingErrorǁ__init____mutmut_15": xǁProfilingErrorǁ__init____mutmut_15,
        "xǁProfilingErrorǁ__init____mutmut_16": xǁProfilingErrorǁ__init____mutmut_16,
        "xǁProfilingErrorǁ__init____mutmut_17": xǁProfilingErrorǁ__init____mutmut_17,
        "xǁProfilingErrorǁ__init____mutmut_18": xǁProfilingErrorǁ__init____mutmut_18,
        "xǁProfilingErrorǁ__init____mutmut_19": xǁProfilingErrorǁ__init____mutmut_19,
        "xǁProfilingErrorǁ__init____mutmut_20": xǁProfilingErrorǁ__init____mutmut_20,
        "xǁProfilingErrorǁ__init____mutmut_21": xǁProfilingErrorǁ__init____mutmut_21,
        "xǁProfilingErrorǁ__init____mutmut_22": xǁProfilingErrorǁ__init____mutmut_22,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁProfilingErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁProfilingErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁProfilingErrorǁ__init____mutmut_orig)
    xǁProfilingErrorǁ__init____mutmut_orig.__name__ = "xǁProfilingErrorǁ__init__"

    def xǁProfilingErrorǁ_default_code__mutmut_orig(self) -> str:
        return "PROFILING_ERROR"

    def xǁProfilingErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXPROFILING_ERRORXX"

    def xǁProfilingErrorǁ_default_code__mutmut_2(self) -> str:
        return "profiling_error"

    xǁProfilingErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁProfilingErrorǁ_default_code__mutmut_1": xǁProfilingErrorǁ_default_code__mutmut_1,
        "xǁProfilingErrorǁ_default_code__mutmut_2": xǁProfilingErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁProfilingErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁProfilingErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁProfilingErrorǁ_default_code__mutmut_orig)
    xǁProfilingErrorǁ_default_code__mutmut_orig.__name__ = "xǁProfilingErrorǁ_default_code"


class SamplingError(ProfilingError):
    """Raised when sampling operations fail.

    Args:
        message: Sampling error message.
        sample_rate: The sample rate that caused the error.
        samples_processed: Optional number of samples processed.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise SamplingError("Invalid sample rate", sample_rate=1.5)
        >>> raise SamplingError("Sampling buffer overflow", samples_processed=1000)

    """

    def xǁSamplingErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = None
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault(None, {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", None)["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault({})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault(
                "context",
            )["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("XXcontextXX", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("CONTEXT", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["XXsampling.rateXX"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["SAMPLING.RATE"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = None
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault(None, {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", None)["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault({})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault(
                "context",
            )["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("XXcontextXX", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("CONTEXT", {})["sampling.processed"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["XXsampling.processedXX"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["SAMPLING.PROCESSED"] = samples_processed
        super().__init__(message, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(None, **kwargs)

    def xǁSamplingErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(**kwargs)

    def xǁSamplingErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        sample_rate: float | None = None,
        samples_processed: int | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            kwargs.setdefault("context", {})["sampling.rate"] = sample_rate
        if samples_processed is not None:
            kwargs.setdefault("context", {})["sampling.processed"] = samples_processed
        super().__init__(
            message,
        )

    xǁSamplingErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSamplingErrorǁ__init____mutmut_1": xǁSamplingErrorǁ__init____mutmut_1,
        "xǁSamplingErrorǁ__init____mutmut_2": xǁSamplingErrorǁ__init____mutmut_2,
        "xǁSamplingErrorǁ__init____mutmut_3": xǁSamplingErrorǁ__init____mutmut_3,
        "xǁSamplingErrorǁ__init____mutmut_4": xǁSamplingErrorǁ__init____mutmut_4,
        "xǁSamplingErrorǁ__init____mutmut_5": xǁSamplingErrorǁ__init____mutmut_5,
        "xǁSamplingErrorǁ__init____mutmut_6": xǁSamplingErrorǁ__init____mutmut_6,
        "xǁSamplingErrorǁ__init____mutmut_7": xǁSamplingErrorǁ__init____mutmut_7,
        "xǁSamplingErrorǁ__init____mutmut_8": xǁSamplingErrorǁ__init____mutmut_8,
        "xǁSamplingErrorǁ__init____mutmut_9": xǁSamplingErrorǁ__init____mutmut_9,
        "xǁSamplingErrorǁ__init____mutmut_10": xǁSamplingErrorǁ__init____mutmut_10,
        "xǁSamplingErrorǁ__init____mutmut_11": xǁSamplingErrorǁ__init____mutmut_11,
        "xǁSamplingErrorǁ__init____mutmut_12": xǁSamplingErrorǁ__init____mutmut_12,
        "xǁSamplingErrorǁ__init____mutmut_13": xǁSamplingErrorǁ__init____mutmut_13,
        "xǁSamplingErrorǁ__init____mutmut_14": xǁSamplingErrorǁ__init____mutmut_14,
        "xǁSamplingErrorǁ__init____mutmut_15": xǁSamplingErrorǁ__init____mutmut_15,
        "xǁSamplingErrorǁ__init____mutmut_16": xǁSamplingErrorǁ__init____mutmut_16,
        "xǁSamplingErrorǁ__init____mutmut_17": xǁSamplingErrorǁ__init____mutmut_17,
        "xǁSamplingErrorǁ__init____mutmut_18": xǁSamplingErrorǁ__init____mutmut_18,
        "xǁSamplingErrorǁ__init____mutmut_19": xǁSamplingErrorǁ__init____mutmut_19,
        "xǁSamplingErrorǁ__init____mutmut_20": xǁSamplingErrorǁ__init____mutmut_20,
        "xǁSamplingErrorǁ__init____mutmut_21": xǁSamplingErrorǁ__init____mutmut_21,
        "xǁSamplingErrorǁ__init____mutmut_22": xǁSamplingErrorǁ__init____mutmut_22,
        "xǁSamplingErrorǁ__init____mutmut_23": xǁSamplingErrorǁ__init____mutmut_23,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSamplingErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁSamplingErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁSamplingErrorǁ__init____mutmut_orig)
    xǁSamplingErrorǁ__init____mutmut_orig.__name__ = "xǁSamplingErrorǁ__init__"

    def xǁSamplingErrorǁ_default_code__mutmut_orig(self) -> str:
        return "SAMPLING_ERROR"

    def xǁSamplingErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXSAMPLING_ERRORXX"

    def xǁSamplingErrorǁ_default_code__mutmut_2(self) -> str:
        return "sampling_error"

    xǁSamplingErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁSamplingErrorǁ_default_code__mutmut_1": xǁSamplingErrorǁ_default_code__mutmut_1,
        "xǁSamplingErrorǁ_default_code__mutmut_2": xǁSamplingErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁSamplingErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁSamplingErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁSamplingErrorǁ_default_code__mutmut_orig)
    xǁSamplingErrorǁ_default_code__mutmut_orig.__name__ = "xǁSamplingErrorǁ_default_code"


class ExporterError(ProfilingError):
    """Raised when metric export operations fail.

    Args:
        message: Export error message.
        exporter_name: Optional name of the exporter that failed.
        endpoint: Optional endpoint URL that failed.
        retry_count: Optional number of retries attempted.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise ExporterError("Failed to connect to Prometheus")
        >>> raise ExporterError("Export timeout", exporter_name="datadog", retry_count=3)

    """

    def xǁExporterErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = None
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault(None, {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", None)["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault({})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault(
                "context",
            )["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("XXcontextXX", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("CONTEXT", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["XXexporter.nameXX"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["EXPORTER.NAME"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = None
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault(None, {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", None)["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault({})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault(
                "context",
            )["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("XXcontextXX", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("CONTEXT", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["XXexporter.endpointXX"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["EXPORTER.ENDPOINT"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = None
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault(None, {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", None)["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault({})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault(
                "context",
            )["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("XXcontextXX", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("CONTEXT", {})["exporter.retry_count"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["XXexporter.retry_countXX"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["EXPORTER.RETRY_COUNT"] = retry_count
        super().__init__(message, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(None, **kwargs)

    def xǁExporterErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(**kwargs)

    def xǁExporterErrorǁ__init____mutmut_31(
        self,
        message: str,
        *,
        exporter_name: str | None = None,
        endpoint: str | None = None,
        retry_count: int | None = None,
        **kwargs: Any,
    ) -> None:
        if exporter_name:
            kwargs.setdefault("context", {})["exporter.name"] = exporter_name
        if endpoint:
            kwargs.setdefault("context", {})["exporter.endpoint"] = endpoint
        if retry_count is not None:
            kwargs.setdefault("context", {})["exporter.retry_count"] = retry_count
        super().__init__(
            message,
        )

    xǁExporterErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁExporterErrorǁ__init____mutmut_1": xǁExporterErrorǁ__init____mutmut_1,
        "xǁExporterErrorǁ__init____mutmut_2": xǁExporterErrorǁ__init____mutmut_2,
        "xǁExporterErrorǁ__init____mutmut_3": xǁExporterErrorǁ__init____mutmut_3,
        "xǁExporterErrorǁ__init____mutmut_4": xǁExporterErrorǁ__init____mutmut_4,
        "xǁExporterErrorǁ__init____mutmut_5": xǁExporterErrorǁ__init____mutmut_5,
        "xǁExporterErrorǁ__init____mutmut_6": xǁExporterErrorǁ__init____mutmut_6,
        "xǁExporterErrorǁ__init____mutmut_7": xǁExporterErrorǁ__init____mutmut_7,
        "xǁExporterErrorǁ__init____mutmut_8": xǁExporterErrorǁ__init____mutmut_8,
        "xǁExporterErrorǁ__init____mutmut_9": xǁExporterErrorǁ__init____mutmut_9,
        "xǁExporterErrorǁ__init____mutmut_10": xǁExporterErrorǁ__init____mutmut_10,
        "xǁExporterErrorǁ__init____mutmut_11": xǁExporterErrorǁ__init____mutmut_11,
        "xǁExporterErrorǁ__init____mutmut_12": xǁExporterErrorǁ__init____mutmut_12,
        "xǁExporterErrorǁ__init____mutmut_13": xǁExporterErrorǁ__init____mutmut_13,
        "xǁExporterErrorǁ__init____mutmut_14": xǁExporterErrorǁ__init____mutmut_14,
        "xǁExporterErrorǁ__init____mutmut_15": xǁExporterErrorǁ__init____mutmut_15,
        "xǁExporterErrorǁ__init____mutmut_16": xǁExporterErrorǁ__init____mutmut_16,
        "xǁExporterErrorǁ__init____mutmut_17": xǁExporterErrorǁ__init____mutmut_17,
        "xǁExporterErrorǁ__init____mutmut_18": xǁExporterErrorǁ__init____mutmut_18,
        "xǁExporterErrorǁ__init____mutmut_19": xǁExporterErrorǁ__init____mutmut_19,
        "xǁExporterErrorǁ__init____mutmut_20": xǁExporterErrorǁ__init____mutmut_20,
        "xǁExporterErrorǁ__init____mutmut_21": xǁExporterErrorǁ__init____mutmut_21,
        "xǁExporterErrorǁ__init____mutmut_22": xǁExporterErrorǁ__init____mutmut_22,
        "xǁExporterErrorǁ__init____mutmut_23": xǁExporterErrorǁ__init____mutmut_23,
        "xǁExporterErrorǁ__init____mutmut_24": xǁExporterErrorǁ__init____mutmut_24,
        "xǁExporterErrorǁ__init____mutmut_25": xǁExporterErrorǁ__init____mutmut_25,
        "xǁExporterErrorǁ__init____mutmut_26": xǁExporterErrorǁ__init____mutmut_26,
        "xǁExporterErrorǁ__init____mutmut_27": xǁExporterErrorǁ__init____mutmut_27,
        "xǁExporterErrorǁ__init____mutmut_28": xǁExporterErrorǁ__init____mutmut_28,
        "xǁExporterErrorǁ__init____mutmut_29": xǁExporterErrorǁ__init____mutmut_29,
        "xǁExporterErrorǁ__init____mutmut_30": xǁExporterErrorǁ__init____mutmut_30,
        "xǁExporterErrorǁ__init____mutmut_31": xǁExporterErrorǁ__init____mutmut_31,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁExporterErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁExporterErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁExporterErrorǁ__init____mutmut_orig)
    xǁExporterErrorǁ__init____mutmut_orig.__name__ = "xǁExporterErrorǁ__init__"

    def xǁExporterErrorǁ_default_code__mutmut_orig(self) -> str:
        return "EXPORTER_ERROR"

    def xǁExporterErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXEXPORTER_ERRORXX"

    def xǁExporterErrorǁ_default_code__mutmut_2(self) -> str:
        return "exporter_error"

    xǁExporterErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁExporterErrorǁ_default_code__mutmut_1": xǁExporterErrorǁ_default_code__mutmut_1,
        "xǁExporterErrorǁ_default_code__mutmut_2": xǁExporterErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁExporterErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁExporterErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁExporterErrorǁ_default_code__mutmut_orig)
    xǁExporterErrorǁ_default_code__mutmut_orig.__name__ = "xǁExporterErrorǁ_default_code"


class MetricsError(ProfilingError):
    """Raised when metrics collection operations fail.

    Args:
        message: Metrics error message.
        metric_name: Optional name of the metric that failed.
        metric_value: Optional value that caused the error.
        **kwargs: Additional context passed to ProfilingError.

    Examples:
        >>> raise MetricsError("Invalid metric value")
        >>> raise MetricsError("Metric overflow", metric_name="latency_ms")

    """

    def xǁMetricsErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = None
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault(None, {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", None)["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault({})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault(
                "context",
            )["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("XXcontextXX", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("CONTEXT", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["XXmetrics.nameXX"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["METRICS.NAME"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = None
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault(None, {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", None)["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault({})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault(
                "context",
            )["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("XXcontextXX", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("CONTEXT", {})["metrics.value"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["XXmetrics.valueXX"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["METRICS.VALUE"] = metric_value
        super().__init__(message, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(None, **kwargs)

    def xǁMetricsErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(**kwargs)

    def xǁMetricsErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        metric_name: str | None = None,
        metric_value: Any = None,
        **kwargs: Any,
    ) -> None:
        if metric_name:
            kwargs.setdefault("context", {})["metrics.name"] = metric_name
        if metric_value is not None:
            kwargs.setdefault("context", {})["metrics.value"] = metric_value
        super().__init__(
            message,
        )

    xǁMetricsErrorǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁMetricsErrorǁ__init____mutmut_1": xǁMetricsErrorǁ__init____mutmut_1,
        "xǁMetricsErrorǁ__init____mutmut_2": xǁMetricsErrorǁ__init____mutmut_2,
        "xǁMetricsErrorǁ__init____mutmut_3": xǁMetricsErrorǁ__init____mutmut_3,
        "xǁMetricsErrorǁ__init____mutmut_4": xǁMetricsErrorǁ__init____mutmut_4,
        "xǁMetricsErrorǁ__init____mutmut_5": xǁMetricsErrorǁ__init____mutmut_5,
        "xǁMetricsErrorǁ__init____mutmut_6": xǁMetricsErrorǁ__init____mutmut_6,
        "xǁMetricsErrorǁ__init____mutmut_7": xǁMetricsErrorǁ__init____mutmut_7,
        "xǁMetricsErrorǁ__init____mutmut_8": xǁMetricsErrorǁ__init____mutmut_8,
        "xǁMetricsErrorǁ__init____mutmut_9": xǁMetricsErrorǁ__init____mutmut_9,
        "xǁMetricsErrorǁ__init____mutmut_10": xǁMetricsErrorǁ__init____mutmut_10,
        "xǁMetricsErrorǁ__init____mutmut_11": xǁMetricsErrorǁ__init____mutmut_11,
        "xǁMetricsErrorǁ__init____mutmut_12": xǁMetricsErrorǁ__init____mutmut_12,
        "xǁMetricsErrorǁ__init____mutmut_13": xǁMetricsErrorǁ__init____mutmut_13,
        "xǁMetricsErrorǁ__init____mutmut_14": xǁMetricsErrorǁ__init____mutmut_14,
        "xǁMetricsErrorǁ__init____mutmut_15": xǁMetricsErrorǁ__init____mutmut_15,
        "xǁMetricsErrorǁ__init____mutmut_16": xǁMetricsErrorǁ__init____mutmut_16,
        "xǁMetricsErrorǁ__init____mutmut_17": xǁMetricsErrorǁ__init____mutmut_17,
        "xǁMetricsErrorǁ__init____mutmut_18": xǁMetricsErrorǁ__init____mutmut_18,
        "xǁMetricsErrorǁ__init____mutmut_19": xǁMetricsErrorǁ__init____mutmut_19,
        "xǁMetricsErrorǁ__init____mutmut_20": xǁMetricsErrorǁ__init____mutmut_20,
        "xǁMetricsErrorǁ__init____mutmut_21": xǁMetricsErrorǁ__init____mutmut_21,
        "xǁMetricsErrorǁ__init____mutmut_22": xǁMetricsErrorǁ__init____mutmut_22,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁMetricsErrorǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁMetricsErrorǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁMetricsErrorǁ__init____mutmut_orig)
    xǁMetricsErrorǁ__init____mutmut_orig.__name__ = "xǁMetricsErrorǁ__init__"

    def xǁMetricsErrorǁ_default_code__mutmut_orig(self) -> str:
        return "METRICS_ERROR"

    def xǁMetricsErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXMETRICS_ERRORXX"

    def xǁMetricsErrorǁ_default_code__mutmut_2(self) -> str:
        return "metrics_error"

    xǁMetricsErrorǁ_default_code__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁMetricsErrorǁ_default_code__mutmut_1": xǁMetricsErrorǁ_default_code__mutmut_1,
        "xǁMetricsErrorǁ_default_code__mutmut_2": xǁMetricsErrorǁ_default_code__mutmut_2,
    }

    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁMetricsErrorǁ_default_code__mutmut_orig"),
            object.__getattribute__(self, "xǁMetricsErrorǁ_default_code__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    _default_code.__signature__ = _mutmut_signature(xǁMetricsErrorǁ_default_code__mutmut_orig)
    xǁMetricsErrorǁ_default_code__mutmut_orig.__name__ = "xǁMetricsErrorǁ_default_code"


# <3 🧱🤝🐛🪄
